"""
QA Studio operations: scope / permissions, ingestion, votes, generator-change
detection, queues and export.  Views and management commands go through here.
"""
from django.db.models import Count, Q
from django.utils import timezone

from quiz.models import Skill

from . import certification, sampling, taxonomy
from .lint import checklist_from_lint, lint_payload
from .models import CRITERIA_KEYS, AuditEntry, QuestionSample, ReviewerProfile

APPROVE, REWORK, REJECT, REOPEN = 'approve', 'rework', 'reject', 'reopen'


class QAError(Exception):
    """A refused action, with a message for the reviewer."""


# ── permissions & scope ───────────────────────────────────────────────────────

def profile_for(user):
    if not user.is_authenticated:
        return None
    prof = getattr(user, 'qa_profile', None)
    if prof is None and user.is_superuser:
        prof, _ = ReviewerProfile.objects.get_or_create(
            user=user, defaults={'role': ReviewerProfile.MASTER, 'all_skills': True})
    return prof


def is_master(user):
    prof = profile_for(user)
    return bool(prof and prof.is_master)


def scoped_skills(prof):
    """Skills a reviewer may act on."""
    qs = Skill.objects.select_related('domain')
    if prof is None:
        return qs.none()
    if prof.is_master or prof.all_skills:
        return qs
    cond = Q(pk__in=prof.skills.values('pk')) | Q(domain__in=prof.domains.all())
    if prof.grades:
        cond |= Q(domain__grade__in=prof.grades)
    return qs.filter(cond)


def can_act(prof, sample):
    return prof is not None and scoped_skills(prof).filter(pk=sample.skill_id).exists()


# ── ingestion ─────────────────────────────────────────────────────────────────

def ingest(skill, count, user=None):
    """Create ``count`` new samples for a skill, spread over its levels. Returns the new samples."""
    levels = sampling.levels_for(skill)
    known = set(QuestionSample.objects.filter(skill=skill).values_list('fingerprint', flat=True))
    created, attempts = [], 0
    while len(created) < count and attempts < count * 6:
        level = levels[(len(created) + attempts) % len(levels)]
        attempts += 1
        seed = sampling.new_seed()
        payload = sampling.generate(skill.slug, level, seed)
        fp = sampling.fingerprint(payload)
        if fp in known:                       # same problem already in the bank
            continue
        known.add(fp)
        created.append(_store(skill, level, seed, payload, fp, user))
    certification.cert_for(skill)
    return created


def _store(skill, level, seed, payload, fp, user):
    findings = lint_payload(payload, skill.slug)
    errors = [f for f in findings if f['severity'] == 'error']
    s = QuestionSample.objects.create(
        skill=skill, level=level, seed=seed, payload=payload, fingerprint=fp,
        status=QuestionSample.FLAGGED if errors else QuestionSample.UNREVIEWED,
        lint=findings, checklist=checklist_from_lint(findings),
    )
    AuditEntry.objects.create(sample=s, user=user, action='created', note=f'{skill.slug} · {level} · seed {seed}')
    if errors:
        AuditEntry.objects.create(sample=s, user=None, action='lint_flagged',
                                  note='; '.join(f"{f['rule']}: {f['message']}" for f in errors)[:2000])
    return s


# ── generator-change detection ────────────────────────────────────────────────

def refresh(sample):
    """Re-run the generator with the sample's seed. If the output changed, the review no longer applies."""
    try:
        payload = sampling.generate(sample.skill.slug, sample.level, sample.seed)
    except KeyError:
        return False
    fp = sampling.fingerprint(payload)
    if fp == sample.fingerprint:
        return False
    previous = sample.status
    findings = lint_payload(payload, sample.skill.slug)
    sample.payload, sample.fingerprint, sample.lint = payload, fp, findings
    sample.stale = True
    sample.checklist = checklist_from_lint(findings)
    if any(f['severity'] == 'error' for f in findings):
        sample.status = QuestionSample.FLAGGED
    else:
        sample.status = QuestionSample.UNREVIEWED
    sample.save()
    AuditEntry.objects.create(sample=sample, user=None, action='generator_changed',
                              note=f'Le générateur a changé : la question a été régénérée (statut précédent : {previous}).')
    if previous == QuestionSample.APPROVED:
        certification.recompute(sample.skill)
    return True


def refresh_all(skills=None):
    qs = QuestionSample.objects.select_related('skill')
    if skills is not None:
        qs = qs.filter(skill__in=skills)
    changed = 0
    touched = set()
    for s in qs.iterator():
        if refresh(s):
            changed += 1
            touched.add(s.skill_id)
    for skill in Skill.objects.filter(pk__in=touched):
        certification.recompute(skill)
    return changed


# ── votes & edits ─────────────────────────────────────────────────────────────

def clean_checklist(raw):
    return {k: bool(raw.get(k)) for k in CRITERIA_KEYS if k in raw}


def vote(sample, user, action, checklist=None, note=''):
    prof = profile_for(user)
    if not can_act(prof, sample):
        raise QAError("Cette compétence n'est pas dans votre périmètre.")
    checklist = clean_checklist(checklist or {})
    note = (note or '').strip()
    if action == APPROVE:
        missing = [k for k in CRITERIA_KEYS if not checklist.get(k)]
        if missing:
            raise QAError('Cochez les 6 critères avant d’approuver (manquants : ' + ', '.join(missing) + ').')
        if sample.proposal:
            raise QAError('Une correction est proposée pour cette question : envoyez-la en retouche, '
                          'ou annulez la correction avant d’approuver.')
        sample.status = QuestionSample.APPROVED
    elif action == REWORK:
        if not note and not sample.proposal:
            raise QAError('Expliquez la retouche demandée (commentaire ou correction proposée).')
        sample.status = QuestionSample.FLAGGED
    elif action == REJECT:
        if not note:
            raise QAError('Indiquez pourquoi la question est rejetée.')
        sample.status = QuestionSample.REJECTED
    elif action == REOPEN:
        sample.status = QuestionSample.UNREVIEWED
    else:
        raise QAError(f'Action inconnue : {action}')
    sample.checklist = checklist
    sample.stale = False
    sample.reviewed_by, sample.reviewed_at = user, timezone.now()
    sample.save()
    AuditEntry.objects.create(sample=sample, user=user, action=action, note=note)
    return certification.recompute(sample.skill)


def save_proposal(sample, user, proposal, note=''):
    prof = profile_for(user)
    if not can_act(prof, sample):
        raise QAError("Cette compétence n'est pas dans votre périmètre.")
    sample.proposal = proposal or None
    sample.save(update_fields=['proposal', 'updated_at'])
    AuditEntry.objects.create(sample=sample, user=user, action='proposal_saved' if proposal else 'proposal_cleared',
                              note=note)


def comment(sample, user, text):
    text = (text or '').strip()
    if not text:
        raise QAError('Commentaire vide.')
    if profile_for(user) is None:
        raise QAError('Accès refusé.')
    AuditEntry.objects.create(sample=sample, user=user, action='comment', note=text[:4000])


# ── queues ────────────────────────────────────────────────────────────────────

TABS = {
    'todo':     [QuestionSample.UNREVIEWED],
    'flagged':  [QuestionSample.FLAGGED],
    'approved': [QuestionSample.APPROVED],
    'all':      None,
}


def queue(skills, tab='todo'):
    qs = QuestionSample.objects.filter(skill__in=skills).select_related('skill', 'skill__domain')
    statuses = TABS.get(tab)
    if statuses:
        qs = qs.filter(status__in=statuses)
    return qs.order_by('skill__domain__grade', 'skill__domain__order', 'skill__order', 'level', 'id')


def next_sample(skills, current=None, skill=None):
    """Spec §4.2: unreviewed first; once exhausted, fall back to re-reviewing approved samples."""
    base = QuestionSample.objects.filter(skill__in=skills)
    if skill is not None:
        base = base.filter(skill=skill)
    if current is not None:
        base = base.exclude(pk=current.pk)
    for statuses in ([QuestionSample.UNREVIEWED], [QuestionSample.APPROVED]):
        qs = base.filter(status__in=statuses)
        if statuses == [QuestionSample.APPROVED]:
            qs = qs.order_by('reviewed_at', 'id')            # least recently reviewed first
        else:
            qs = qs.order_by('skill__domain__grade', 'skill__order', 'id')
        s = qs.first()
        if s:
            return s
    return None


def skill_rows(skills):
    """Per-skill counts for the navigation panel."""
    counts = {}
    for row in (QuestionSample.objects.filter(skill__in=skills)
                .values('skill_id', 'status').annotate(n=Count('id'))):
        counts.setdefault(row['skill_id'], {})[row['status']] = row['n']
    certs = {c.skill_id: c for c in certification.SkillCertification.objects.filter(skill__in=skills)}
    rows = []
    for sk in skills.select_related('domain').order_by('domain__grade', 'domain__order', 'order', 'id'):
        c = counts.get(sk.pk, {})
        cert = certs.get(sk.pk)
        threshold = cert.threshold if cert else certification.SkillCertification._meta.get_field('threshold').get_default()
        approved = c.get(QuestionSample.APPROVED, 0)
        rows.append({
            'skill': sk,
            'path': taxonomy.path(sk),
            'approved': approved,
            'threshold': threshold,
            'pct': min(100, round(approved / threshold * 100)) if threshold else 100,
            'todo': c.get(QuestionSample.UNREVIEWED, 0),
            'flagged': c.get(QuestionSample.FLAGGED, 0),
            'rejected': c.get(QuestionSample.REJECTED, 0),
            'total': sum(c.values()),
            'state': cert.state if cert else 'LOCKED',
            'override': cert.override if cert else '',
            'live': cert.is_live if cert else False,
        })
    return rows


def global_metrics(skills):
    qs = QuestionSample.objects.filter(skill__in=skills)
    by = dict(qs.values_list('status').annotate(n=Count('id')))
    certs = certification.SkillCertification.objects.filter(skill__in=skills)
    return {
        'skills': skills.count(),
        'certified': certs.filter(state='CERTIFIED').count(),
        'degraded': certs.filter(state='DEGRADED').count(),
        'todo': by.get(QuestionSample.UNREVIEWED, 0),
        'flagged': by.get(QuestionSample.FLAGGED, 0),
        'approved': by.get(QuestionSample.APPROVED, 0),
        'rejected': by.get(QuestionSample.REJECTED, 0),
        'total': sum(by.values()),
    }


# ── export (spec §7.1 question schema) ────────────────────────────────────────

def export_item(sample, lang='fr'):
    q = sampling.render_question(sample.payload, sample.skill.slug, lang)
    table = q.get('table')
    if table:
        head = '| ' + ' | '.join(table['headers']) + ' |\n|' + '---|' * len(table['headers'])
        body = '\n'.join('| ' + ' | '.join(r) + ' |' for r in table['rows'])
        raw, fmt = q.get(f'prompt_{lang}', '') + '\n\n' + head + '\n' + body, 'MARKDOWN_TABLE'
    else:
        raw, fmt = q.get(f'prompt_{lang}', ''), ('IMAGE_PROMPT' if q.get('shape_data') else 'PLAIN_TEXT')
    options = [{'id': f'opt{i + 1}', 'label': str(c.get('label', '')),
                'distractor_rationale': c.get(f'feedback_{lang}') or c.get('error_type', '')}
               for i, c in enumerate(q.get('choices') or [])]
    level_tier = {'easy': 1, 'medium': 2, 'hard': 3, 'resolution': 3}
    return {
        'id': sample.code,
        'taxonomy': taxonomy.ids(sample.skill),
        'difficulty_tier': level_tier.get(sample.level, 1),
        'level': sample.level,
        'seed': sample.seed,
        'q_type': q.get('q_type'),
        'prompt': {'raw_text': raw, 'format_type': fmt},
        'options': options,
        'correct_option_index': sampling.correct_index(q),
        'correct_answers': q.get('correct_answers', []),
        'hint': q.get(f'hint_{lang}', ''),
        'status': sample.status,
        'quality_checklist': {k: bool(sample.checklist.get(k)) for k in CRITERIA_KEYS},
        'lint': sample.lint,
        'proposal': sample.proposal,
        'audit_trail': [
            {'reviewer_id': str(a.user_id or 'system'), 'reviewer_name': a.actor,
             'timestamp': a.created_at.isoformat(), 'action': a.action, 'note': a.note}
            for a in sample.audit.all()
        ],
    }
