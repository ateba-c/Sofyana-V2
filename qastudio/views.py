import csv
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_POST

from quiz.generators import LEVEL_NAMES
from quiz.models import Skill, SkillDomain
from quiz.views import _check_practice, _topic_card_groups

from . import ai_review, certification, proposals, sampling, services, taxonomy
from .models import CRITERIA, AIReview, AuditEntry, CertificationEvent, QuestionSample, ReviewerProfile, SkillCertification


# ── access ────────────────────────────────────────────────────────────────────

def _profile(request):
    prof = services.profile_for(request.user)
    if prof is None:
        raise PermissionDenied('QA Studio: no reviewer profile')
    return prof


def _master(request):
    prof = _profile(request)
    if not prof.is_master:
        raise PermissionDenied('QA Studio: master reviewers only')
    return prof


def _viewer(request, prof):
    """Who the Studio is showing: yourself, or (masters) another reviewer's scope, read-only."""
    as_id = request.GET.get('as')
    if as_id and prof.is_master:
        other = ReviewerProfile.objects.filter(pk=as_id).select_related('user').first()
        if other:
            return other, True
    return prof, request.GET.get('global') == '1'


def _sample(request, pk):
    prof = _profile(request)
    sample = get_object_or_404(QuestionSample.objects.select_related('skill', 'skill__domain'), pk=pk)
    readable = prof.is_master or services.can_act(prof, sample) or request.GET.get('global') == '1' \
        or request.POST.get('global') == '1'
    if not readable:
        raise PermissionDenied('QA Studio: out of scope')
    return prof, sample


def _qs(request, **override):
    """Keep the Studio's navigation state (skill, tab, lang, as, global) across links."""
    params = {k: request.GET.get(k) for k in ('skill', 'tab', 'lang', 'as', 'global', 'band', 'cat') if request.GET.get(k)}
    params.update({k: v for k, v in override.items() if v is not None})
    params = {k: v for k, v in params.items() if v != ''}
    return '?' + '&'.join(f'{k}={v}' for k, v in params.items()) if params else ''


# ── the 3-panel workspace ─────────────────────────────────────────────────────

@login_required
def studio(request, pk=None):
    prof = _profile(request)
    viewer, read_only_global = _viewer(request, prof)
    in_scope = services.scoped_skills(viewer)
    nav_skills = Skill.objects.select_related('domain') if read_only_global else in_scope

    rows = services.skill_rows(nav_skills)
    bands = sorted({(r['path'][0]['id'], r['path'][0]['title_fr']) for r in rows})
    band = request.GET.get('band', '')
    cats = sorted({(r['path'][2]['id'], r['path'][2]['title_fr']) for r in rows if not band or r['path'][0]['id'] == band},
                  key=lambda x: x[1])
    cat = request.GET.get('cat', '')
    visible_rows = [r for r in rows if (not band or r['path'][0]['id'] == band) and (not cat or r['path'][2]['id'] == cat)]

    skill_slug = request.GET.get('skill', '')
    skill = nav_skills.filter(slug=skill_slug).first() if skill_slug else None
    ai_on = ai_review.is_enabled()
    if ai_on:
        ai_review.expire_stale_pending()
    tab = request.GET.get('tab', 'todo')
    if tab not in services.TABS and not (ai_on and tab in ('ai_issues', 'ai_clean')):
        tab = 'todo'
    queue_skills = nav_skills.filter(pk=skill.pk) if skill else nav_skills.filter(slug__in=[r['skill'].slug for r in visible_rows])
    items = list(services.queue(queue_skills, tab)[:200])

    sample = None
    if pk is not None:
        _, sample = _sample(request, pk)
        if services.refresh(sample):          # generator changed since this sample was reviewed
            sample.refresh_from_db()
    elif items:
        sample = items[0]
    elif tab == 'todo':
        sample = services.next_sample(queue_skills, skill=skill)

    ctx = {
        'prof': prof, 'viewer': viewer, 'is_master': prof.is_master,
        'read_only': read_only_global or viewer != prof,
        'global_mode': request.GET.get('global') == '1',
        'metrics': services.global_metrics(in_scope),
        'rows': visible_rows, 'bands': bands, 'band': band, 'cats': cats, 'cat': cat,
        'skill': skill, 'tab': tab, 'items': items, 'sample': sample,
        'tabs': [('todo', 'À faire')] + ([('ai_issues', 'IA ⚠'), ('ai_clean', 'IA ✓')] if ai_on else [])
                + [('flagged', 'Signalés'), ('approved', 'Validés'), ('all', 'Tous')],
        'ai_on': ai_on, 'ai_model': ai_review.model_name() if ai_on else '',
        'agreement': ai_review.agreement(in_scope) if ai_on else None,
        'diagnosis': ai_review.latest_diagnosis(skill) if (ai_on and skill) else None,
        'ai_to_review': len(ai_review.samples_needing_review(skill)) if (ai_on and skill) else 0,
        'lang': request.GET.get('lang', 'fr') if request.GET.get('lang') in ('fr', 'en') else 'fr',
        'criteria': CRITERIA,
        'reviewers': ReviewerProfile.objects.select_related('user').order_by('user__username') if prof.is_master else [],
        'all_skills': Skill.objects.select_related('domain').order_by('domain__grade', 'domain__order', 'order') if prof.is_master else [],
        'all_domains': SkillDomain.objects.order_by('grade', 'order') if prof.is_master else [],
        'gate_enabled': certification.gate_enabled(),
        'events': CertificationEvent.objects.select_related('skill')[:8] if prof.is_master else [],
        'qs': _qs(request),
        'flash': request.session.pop('qa_flash', None),
    }
    if sample is not None:
        cert = certification.cert_for(sample.skill)
        can_act = (not ctx['read_only']) and services.can_act(prof, sample)
        ctx.update({
            'cert': cert,
            'cert_pct': min(100, round(cert.approved_count / cert.threshold * 100)) if cert.threshold else 100,
            'path': taxonomy.path(sample.skill),
            'can_act': can_act,
            'level_name': LEVEL_NAMES.get(sample.level, (sample.level, sample.level))[1],
            'audit': sample.audit.select_related('user')[:30],
            'editor_json': json.dumps(sample.proposal or proposals.from_payload(sample.payload), ensure_ascii=False),
            'original_json': json.dumps(proposals.from_payload(sample.payload), ensure_ascii=False),
            'has_proposal': bool(sample.proposal),
            'checklist_json': json.dumps(sample.checklist),
            'lint_by_criterion': {k: [f for f in sample.lint if f['criterion'] == k] for k, *_ in CRITERIA},
            'sample_qs': _qs(request, skill=request.GET.get('skill') or sample.skill.slug),
        })
        if ai_on:
            ai = ai_review.latest_review(sample)
            ctx.update({
                'ai': ai,
                'ai_current': bool(ai and (ai.pending or ai.fingerprint == sample.fingerprint)),
                'ai_suggestion_json': json.dumps(ai.suggestion, ensure_ascii=False) if (ai and ai.suggestion) else 'null',
                'ai_criteria_json': json.dumps(ai.criteria if ai and not ai.pending else {}, ensure_ascii=False),
            })
    return render(request, 'qastudio/studio.html', ctx)


# ── child-app simulator (iframe) ──────────────────────────────────────────────

def _sim_question(request, sample, lang, draft):
    payload = sample.payload
    if draft:
        payload = proposals.apply(payload, request.session.get(f'qa_draft_{sample.pk}') or sample.proposal)
    q = sampling.render_question(payload, sample.skill.slug, lang)
    request.session[f'qa_q_{sample.pk}'] = q
    return q


@xframe_options_sameorigin       # shown inside the Studio's phone frame (same origin only)
@login_required
def sim_frame(request, pk):
    """The real practice page (quiz/practice.html), whose htmx calls are redirected to this sample."""
    _, sample = _sample(request, pk)
    lang = request.GET.get('lang') if request.GET.get('lang') in ('fr', 'en') else 'fr'
    slug = sample.skill.slug
    levels = sampling.levels_for(sample.skill)
    return render(request, 'qastudio/sim_frame.html', {
        'sample': sample, 'topic': slug, 'level': sample.level, 'lang': lang,
        'topic_info': {'slug': slug, 'name_fr': sample.skill.name_fr or sample.skill.name_en, 'name_en': sample.skill.name_en},
        'topic_groups': _topic_card_groups(None),
        'levels': [(lv, LEVEL_NAMES[lv][0], LEVEL_NAMES[lv][1]) for lv in levels if lv in LEVEL_NAMES],
        'resolution_unlocked': True, 'locked_notice': '',
        'parent_assignments': [], 'recommendations': [],
        'draft': request.GET.get('draft') == '1',
        'student': None,
    })


@login_required
def sim_question(request, pk):
    _, sample = _sample(request, pk)
    lang = request.GET.get('lang') if request.GET.get('lang') in ('fr', 'en') else 'fr'
    q = _sim_question(request, sample, lang, request.GET.get('draft') == '1')
    return render(request, 'partials/practice_question.html', {
        'question': q, 'topic': sample.skill.slug, 'level': sample.level, 'lang': lang,
    })


@login_required
@require_POST
def sim_check(request, pk):
    _, sample = _sample(request, pk)
    lang = request.POST.get('lang') if request.POST.get('lang') in ('fr', 'en') else 'fr'
    q = request.session.get(f'qa_q_{sample.pk}') or _sim_question(request, sample, lang, False)
    answer = request.POST.get('answer', '').strip()
    correct = _check_practice(q, answer)
    try:
        answer_index = int(answer)
    except (TypeError, ValueError):
        answer_index = None
    misconception = ''
    error_type = ''
    if q.get('q_type') == 'multiple_choice' and not correct and answer_index is not None:
        try:
            chosen = q['choices'][answer_index]
            error_type = chosen.get('error_type', '')
            misconception = chosen.get(f'feedback_{lang}') or chosen.get('feedback_en', '')
        except (IndexError, KeyError):
            pass
    answer_data = None
    if q.get('q_type') in ('ordering', 'sorting'):
        try:
            submitted = json.loads(answer) if answer else []
            order = {it['label']: it['order'] for it in q.get('items', [])}
            answer_data = [{'label': lb, 'submitted_pos': i + 1, 'correct_pos': order.get(lb, 0),
                            'is_correct': order.get(lb, 0) == i + 1} for i, lb in enumerate(submitted)]
        except (ValueError, TypeError):
            answer_data = []
    elif q.get('q_type') == 'mix_match':
        try:
            submitted = json.loads(answer) if answer else {}
            answer_data = [{'left': p['left'], 'right_correct': p['right'], 'right_submitted': submitted.get(p['left'], ''),
                            'is_correct': submitted.get(p['left']) == p['right']} for p in q.get('pairs', [])]
        except (ValueError, TypeError):
            answer_data = []
    return render(request, 'partials/practice_feedback.html', {
        'correct': correct, 'streak': 1 if correct else 0, 'total': 1, 'correct_count': 1 if correct else 0,
        'wrong_streak': 0 if correct else 1, 'stars_earned': 0, 'total_stars': 0,
        'explanation': q.get(f'explanation_{lang}') or q.get('explanation_en', ''),
        'misconception_feedback': misconception, 'error_type': error_type,
        'question': q, 'answer': answer, 'answer_index': answer_index, 'answer_data': answer_data,
        'topic': sample.skill.slug, 'level': sample.level, 'lang': lang,
        'suggested_action': None, 'suggested_level': sample.level, 'suggested_topic': None,
        'level_name': LEVEL_NAMES.get(sample.level, (sample.level, sample.level))[1 if lang == 'fr' else 0],
        'suggested_level_name': '', 'resolution_just_unlocked': False,
    })


@login_required
@require_POST
def sim_draft(request, pk):
    """Store the editor's unsaved draft so the simulator can render it (no page reload)."""
    _, sample = _sample(request, pk)
    try:
        draft = proposals.clean(json.loads(request.body or b'{}'))
    except ValueError:
        return HttpResponse(status=400)
    request.session[f'qa_draft_{sample.pk}'] = draft
    return HttpResponse(status=204)


# ── reviewer actions ──────────────────────────────────────────────────────────

def _back(request, sample, nxt=None):
    qs = request.POST.get('qs', '')
    if nxt is not None:
        return redirect(reverse('qastudio:sample', args=[nxt.pk]) + qs)
    return redirect(reverse('qastudio:sample', args=[sample.pk]) + qs)


def _flash(request, msg, level='ok'):
    request.session['qa_flash'] = {'msg': msg, 'level': level}


@login_required
@require_POST
def vote(request, pk):
    prof, sample = _sample(request, pk)
    action = request.POST.get('action')
    checklist = {k: request.POST.get(f'c_{k}') == 'on' for k, *_ in CRITERIA}
    try:
        cert = services.vote(sample, request.user, action, checklist, request.POST.get('note', ''))
    except services.QAError as exc:
        _flash(request, str(exc), 'error')
        return _back(request, sample)
    labels = {'approve': 'Approuvée', 'rework': 'Envoyée en retouche', 'reject': 'Rejetée', 'reopen': 'Remise à faire'}
    _flash(request, f'{sample.code} : {labels.get(action, action)} · {sample.skill.slug} {cert.approved_count}/{cert.threshold}'
                    + (' — compétence certifiée 🎉' if cert.state == 'CERTIFIED' and action == 'approve' else ''))
    skill_filter = sample.skill if request.POST.get('stay_on_skill') == '1' else None
    nxt = services.next_sample(services.scoped_skills(prof), current=sample, skill=skill_filter)
    return _back(request, sample, nxt)


@login_required
@require_POST
def save_proposal(request, pk):
    prof, sample = _sample(request, pk)
    try:
        if request.POST.get('clear') == '1':
            services.save_proposal(sample, request.user, None)
            _flash(request, 'Correction annulée.')
        else:
            prop = proposals.clean(json.loads(request.POST.get('proposal') or '{}'))
            if not proposals.differs(sample.payload, prop):
                services.save_proposal(sample, request.user, None)
                _flash(request, 'Aucune différence avec la question générée : rien à enregistrer.', 'warn')
            else:
                services.save_proposal(sample, request.user, prop, request.POST.get('note', ''))
                _flash(request, 'Correction enregistrée. Envoyez la question en retouche pour la transmettre.')
    except (ValueError, services.QAError) as exc:
        _flash(request, str(exc), 'error')
    request.session.pop(f'qa_draft_{sample.pk}', None)
    return _back(request, sample)


@login_required
@require_POST
def add_comment(request, pk):
    _, sample = _sample(request, pk)
    try:
        services.comment(sample, request.user, request.POST.get('text', ''))
    except services.QAError as exc:
        _flash(request, str(exc), 'error')
    return _back(request, sample)


# ── AI pre-review ──────────────────────────────────────────────────────────────

@login_required
@require_POST
def ai_sample(request, pk):
    """Run the AI on this one sample (background; the page polls ai_status)."""
    prof, sample = _sample(request, pk)
    if not ai_review.is_enabled():
        _flash(request, "IA non configurée (clé LLM manquante).", 'error')
    elif not (prof.is_master or services.can_act(prof, sample)):
        raise PermissionDenied
    elif not AIReview.objects.filter(sample=sample, pending=True).exists():
        ai_review.start_background(sample.skill, [sample], with_diagnosis=False)
    return _back(request, sample)


@login_required
@require_POST
def ai_skill(request, slug):
    """Master: AI review of every sample of the skill not reviewed yet (or all with force=1), then a diagnosis."""
    _master(request)
    skill = get_object_or_404(Skill.objects.select_related('domain'), slug=slug)
    if not ai_review.is_enabled():
        _flash(request, "IA non configurée (clé LLM manquante).", 'error')
    elif skill.ai_diagnoses.filter(pending=True).exists():
        _flash(request, 'Une analyse IA de cette compétence est déjà en cours.', 'warn')
    else:
        samples = ai_review.samples_needing_review(skill, force=request.POST.get('force') == '1')
        ai_review.start_background(skill, samples, with_diagnosis=True)
        _flash(request, f'Analyse IA lancée : {len(samples)} question(s) + diagnostic du générateur. '
                        'Les résultats apparaissent dans une à deux minutes.')
    return redirect(reverse('qastudio:studio') + request.POST.get('qs', ''))


@login_required
def ai_status(request):
    """Polled by the Studio while an analysis runs: {pending: n}."""
    _profile(request)
    ai_review.expire_stale_pending()
    q = AIReview.objects.filter(pending=True)
    if request.GET.get('sample'):
        q = q.filter(sample_id=request.GET['sample'])
    n = q.count()
    if request.GET.get('skill'):
        from .models import SkillDiagnosis
        n += SkillDiagnosis.objects.filter(skill__slug=request.GET['skill'], pending=True).count()
    return JsonResponse({'pending': n})


# ── master tools ──────────────────────────────────────────────────────────────

@login_required
@require_POST
def ingest(request, slug):
    _master(request)
    skill = get_object_or_404(Skill, slug=slug)
    try:
        n = max(1, min(50, int(request.POST.get('count', '10'))))
    except ValueError:
        n = 10
    created = services.ingest(skill, n, request.user)
    flagged = sum(1 for s in created if s.status == QuestionSample.FLAGGED)
    _flash(request, f'{len(created)} échantillons générés pour {slug} ({flagged} signalés par le linter).')
    return redirect(reverse('qastudio:studio') + request.POST.get('qs', ''))


@login_required
@require_POST
def skill_settings(request, slug):
    _master(request)
    skill = get_object_or_404(Skill, slug=slug)
    cert = certification.cert_for(skill)
    try:
        threshold = int(request.POST.get('threshold', cert.threshold))
        if threshold < 1:
            raise ValueError
    except ValueError:
        _flash(request, 'Seuil invalide.', 'error')
        return redirect(reverse('qastudio:studio') + request.POST.get('qs', ''))
    if threshold != cert.threshold:
        cert.threshold = threshold
        cert.save(update_fields=['threshold', 'updated_at'])
        certification.recompute(skill)
    override = request.POST.get('override', cert.override)
    if override in ('', 'lock', 'unlock') and override != cert.override:
        certification.set_override(cert, override, request.user)
    _flash(request, f'{slug} : seuil {cert.threshold}, forçage « {cert.get_override_display()} ».')
    return redirect(reverse('qastudio:studio') + request.POST.get('qs', ''))


@login_required
@require_POST
def team(request):
    master = _master(request)
    username = (request.POST.get('username') or '').strip()
    if not username:
        _flash(request, "Nom d'utilisateur requis.", 'error')
        return redirect(reverse('qastudio:studio') + request.POST.get('qs', ''))
    user = User.objects.filter(username__iexact=username).first()
    password = request.POST.get('password') or ''
    if user is None:
        if len(password) < 8:
            _flash(request, 'Nouveau réviseur : mot de passe de 8 caractères minimum.', 'error')
            return redirect(reverse('qastudio:studio') + request.POST.get('qs', ''))
        user = User.objects.create_user(username=username, password=password, email=request.POST.get('email', ''))
    elif password:
        user.set_password(password)
    full = (request.POST.get('full_name') or '').strip()
    if full:
        user.first_name, _, user.last_name = full.partition(' ')
    if request.POST.get('email'):
        user.email = request.POST['email']
    user.save()
    prof, _ = ReviewerProfile.objects.get_or_create(user=user)
    prof.role = ReviewerProfile.MASTER if request.POST.get('role') == ReviewerProfile.MASTER else ReviewerProfile.REVIEWER
    prof.all_skills = request.POST.get('all_skills') == 'on'
    prof.grades = sorted({int(g) for g in request.POST.getlist('grades') if g.isdigit()})
    prof.save()
    prof.domains.set(SkillDomain.objects.filter(pk__in=request.POST.getlist('domains')))
    prof.skills.set(Skill.objects.filter(pk__in=request.POST.getlist('skills')))
    _flash(request, f'Réviseur {user.username} enregistré ({prof.get_role_display()}).')
    return redirect(reverse('qastudio:studio') + request.POST.get('qs', ''))


@login_required
@require_POST
def refresh_all(request):
    _master(request)
    n = services.refresh_all()
    _flash(request, f'Générateurs vérifiés : {n} échantillon(s) régénéré(s) parce que le code a changé.')
    return redirect(reverse('qastudio:studio') + request.POST.get('qs', ''))


@login_required
def export(request, fmt):
    _master(request)
    qs = QuestionSample.objects.select_related('skill', 'skill__domain').prefetch_related('audit__user')
    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)
    if request.GET.get('skill'):
        qs = qs.filter(skill__slug=request.GET['skill'])
    lang = request.GET.get('lang') if request.GET.get('lang') in ('fr', 'en') else 'fr'
    items = [services.export_item(s, lang) for s in qs]
    if fmt == 'json':
        resp = JsonResponse({'items': items,
                             'subtopics': [{'id': c.skill.slug, **taxonomy.ids(c.skill), 'title': c.skill.name_fr,
                                            'min_approved_threshold': c.threshold, 'current_approved_count': c.approved_count,
                                            'state': c.state, 'is_certified_for_students': c.is_live,
                                            'assigned_reviewers': [p.user.username for p in c.skill.qa_reviewers.select_related('user')]}
                                           for c in SkillCertification.objects.select_related('skill', 'skill__domain')]},
                            json_dumps_params={'ensure_ascii': False, 'indent': 2})
        resp['Content-Disposition'] = 'attachment; filename="sofyana-qa.json"'
        return resp
    if fmt != 'csv':
        raise Http404
    resp = HttpResponse(content_type='text/csv; charset=utf-8')
    resp['Content-Disposition'] = 'attachment; filename="sofyana-qa.csv"'
    resp.write('﻿')
    w = csv.writer(resp)
    w.writerow(['id', 'level_id', 'domain_id', 'category_id', 'subtopic_id', 'level', 'seed', 'status', 'prompt',
                'format', 'options', 'correct_option_index', 'hint', 'lint', 'has_proposal'])
    for it in items:
        t = it['taxonomy']
        w.writerow([it['id'], t['level_id'], t['domain_id'], t['category_id'], t['subtopic_id'], it['level'], it['seed'],
                    it['status'], it['prompt']['raw_text'], it['prompt']['format_type'],
                    ' / '.join(o['label'] for o in it['options']), it['correct_option_index'], it['hint'],
                    '; '.join(f"{f['rule']} {f['message']}" for f in it['lint']), bool(it['proposal'])])
    return resp
