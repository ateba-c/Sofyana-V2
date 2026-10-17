"""
Subtopic (skill) certification state machine — spec §3.

    approved < N, never certified   → LOCKED
    approved ≥ N                    → CERTIFIED   (emits EVENT_SUBTOPIC_CERTIFIED)
    approved < N, was certified     → DEGRADED    (emits EVENT_SUBTOPIC_DEGRADED)

"Approved" counts only samples whose generator output is still what the reviewer
saw (``stale=False``).  When the gate is on (settings.QA_GATE_ENABLED) only live
skills (``SkillCertification.is_live``) are shown to students.
"""
import hashlib
import hmac
import json
import logging
import threading
import urllib.request

from django.conf import settings
from django.db import transaction
from django.dispatch import Signal
from django.utils import timezone

from .models import CertificationEvent, QuestionSample, SkillCertification

log = logging.getLogger(__name__)

EVENT_CERTIFIED = 'EVENT_SUBTOPIC_CERTIFIED'
EVENT_DEGRADED = 'EVENT_SUBTOPIC_DEGRADED'
EVENT_OVERRIDE = 'EVENT_SUBTOPIC_OVERRIDE'

# Django signal for in-process listeners: sender=SkillCertification, cert=…, event=…
subtopic_transition = Signal()


def cert_for(skill):
    cert, _ = SkillCertification.objects.get_or_create(skill=skill)
    return cert


def approved_count(skill):
    return QuestionSample.objects.filter(skill=skill, status=QuestionSample.APPROVED, stale=False).count()


def recompute(skill):
    """Recount approved samples, move the state machine, emit events. Returns the certification."""
    with transaction.atomic():
        cert = cert_for(skill)
        before_state, before_live = cert.state, cert.is_live
        cert.approved_count = approved_count(skill)
        if cert.approved_count >= cert.threshold:
            cert.state = SkillCertification.CERTIFIED
            if before_state != SkillCertification.CERTIFIED:
                cert.certified_at = timezone.now()
        elif before_state in (SkillCertification.CERTIFIED, SkillCertification.DEGRADED):
            cert.state = SkillCertification.DEGRADED
        else:
            cert.state = SkillCertification.LOCKED
        cert.save()
    if cert.state != before_state:
        event = EVENT_CERTIFIED if cert.state == SkillCertification.CERTIFIED else (
            EVENT_DEGRADED if cert.state == SkillCertification.DEGRADED else None)
        if event:
            _emit(cert, event, before_state)
    if cert.is_live != before_live:
        _invalidate_taxonomy()
    return cert


def set_override(cert, override, user=None):
    before_live = cert.is_live
    cert.override = override
    cert.save(update_fields=['override', 'updated_at'])
    _emit(cert, EVENT_OVERRIDE, cert.state, extra={'override': override or 'none',
                                                  'by': user.username if user else ''})
    if cert.is_live != before_live:
        _invalidate_taxonomy()


def _invalidate_taxonomy():
    from quiz import taxonomy
    taxonomy.invalidate()


def _emit(cert, event, from_state, extra=None):
    payload = {
        'event': event,
        'subtopic_id': cert.skill.slug,
        'title': cert.skill.name_fr or cert.skill.name_en,
        'from_state': from_state,
        'to_state': cert.state,
        'is_live': cert.is_live,
        'approved': cert.approved_count,
        'threshold': cert.threshold,
        'timestamp': timezone.now().isoformat(),
        **(extra or {}),
    }
    ev = CertificationEvent.objects.create(
        skill=cert.skill, event=event, from_state=from_state, to_state=cert.state,
        approved=cert.approved_count, threshold=cert.threshold,
    )
    subtopic_transition.send(sender=SkillCertification, cert=cert, event=event, payload=payload)
    url = getattr(settings, 'QA_WEBHOOK_URL', '')
    if url:
        # fire-and-forget: a slow receiver must never block a reviewer's click
        threading.Thread(target=_post_webhook, args=(url, payload, ev.pk), daemon=True).start()


def _post_webhook(url, payload, event_pk):
    body = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Sofyana-QA-Studio'}
    secret = getattr(settings, 'QA_WEBHOOK_SECRET', '')
    if secret:
        headers['X-Sofyana-Signature'] = 'sha256=' + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = f'HTTP {resp.status}'
    except Exception as exc:          # recorded on the event, never raised
        status = f'error: {exc.__class__.__name__}'[:60]
        log.warning('QA webhook %s failed: %s', url, exc)
    CertificationEvent.objects.filter(pk=event_pk).update(webhook_status=status)


def live_slugs():
    """Skills students may see when the gate is on."""
    live = set()
    for cert in SkillCertification.objects.select_related('skill'):
        if cert.is_live:
            live.add(cert.skill.slug)
    return live


def gate_enabled():
    return getattr(settings, 'QA_GATE_ENABLED', False)


def is_skill_live(slug):
    if not gate_enabled():
        return True
    cert = SkillCertification.objects.filter(skill__slug=slug).first()
    return bool(cert and cert.is_live)
