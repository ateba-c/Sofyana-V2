"""
AI pre-review (advisory layer between the linter and the human reviewer).

Per skill, three kinds of LLM calls through quiz.ai.client (DeepSeek by default,
Claude via LLM_BASE_URL / QA_AI_MODEL):

1. SOLVE    — the model answers each problem *without* the answer key.  Code then
              compares its answer with the key: mismatch = wrong key or ambiguous
              problem; several correct choices = ambiguous problem.
2. REVIEW   — the model sees everything (key, hint, explanation, solver result) and
              judges the 6 rubric criteria, with a suggested rewrite when needed.
3. DIAGNOSE — one call over all samples of the skill: recurring generator defects
              and a concrete fix for the developer.

The AI is advisory: it never changes a sample's status or certification.

LLM calls are pure functions over prepared dicts (safe to run in threads);
database reads/writes happen in the calling thread (SQLite dislikes concurrent writers).
"""
import json
import logging
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta

from django.conf import settings
from django.db import close_old_connections
from django.utils import timezone

from quiz.ai import client as llm
from quiz.answers import check_answer

from . import proposals, sampling
from .models import CRITERIA, CRITERIA_KEYS, AIReview, AuditEntry, QuestionSample, SkillDiagnosis

log = logging.getLogger(__name__)

_NUMBERING = re.compile(r'^\s*\d+\s*[.)]\s+')
CHUNK = 4                       # samples per solve / review call (halved automatically on failure)
MAX_TOKENS = 16000              # reasoning models (deepseek-flash) think before answering: leave room
CALL_TIMEOUT = 240              # seconds; long thinking must not hit the client's 60 s default and retry
PENDING_TIMEOUT = timedelta(minutes=10)


def is_enabled():
    return llm.is_configured()


def model_name():
    return getattr(settings, 'QA_AI_MODEL', '') or settings.LLM_MODEL


# ── what the model sees ───────────────────────────────────────────────────────

_SHAPE_DROP = {'svg'}
_NUM = re.compile(r'-?\d+\.\d+')
ILLUSTRATION_CAP = 6000         # characters per illustration (a full canvas is ~1–3 kB once compacted)


def _r(v):
    return round(v) if isinstance(v, float) else v


def _mark_text(m):
    """One canvas primitive as a short line: 'line 18,38→302,38 #334155', 'path M 69,14 L 85,54 Z fill=#DBEAFE'."""
    t = m.get('type')
    if t == 'path':
        d = _NUM.sub(lambda x: str(round(float(x.group()))), str(m.get('d', '')))
        return f"path {d} fill={m.get('fill', 'none')}" + (' dashed' if m.get('dash') else '')
    if t in ('line', 'dashed'):
        return f"{t} {_r(m.get('x1'))},{_r(m.get('y1'))}→{_r(m.get('x2'))},{_r(m.get('y2'))} {m.get('color', '')}".rstrip()
    if t == 'dot':
        return f"dot {_r(m.get('x'))},{_r(m.get('y'))} r={_r(m.get('r', 4))} {m.get('fill', '')}".rstrip()
    if t == 'rect':
        return f"rect x={_r(m.get('x'))} y={_r(m.get('y'))} w={_r(m.get('w'))} h={_r(m.get('h'))} fill={m.get('fill', 'none')}"
    if t == 'circle':
        return f"circle c={_r(m.get('cx'))},{_r(m.get('cy'))} r={_r(m.get('r'))} fill={m.get('fill', 'none')}"
    if t == 'pie_slice':
        return f"pie_slice c={_r(m.get('cx'))},{_r(m.get('cy'))} r={_r(m.get('r'))} from {_r(m.get('lx1'))},{_r(m.get('ly1'))} to {_r(m.get('lx2'))},{_r(m.get('ly2'))} fill={m.get('fill')}"
    return json.dumps({k: _r(v) for k, v in m.items()}, ensure_ascii=False, default=str)


def _canvas_text(sh):
    lines = [f"canvas {sh.get('vw')}×{sh.get('vh')} px (y grows downward)"]
    lines += [_mark_text(m) for m in sh.get('marks') or [] if isinstance(m, dict)]
    lines += [f"text {lb.get('text')!r} at {_r(lb.get('x'))},{_r(lb.get('y'))}" for lb in sh.get('labels') or [] if isinstance(lb, dict)]
    return '\n'.join(lines)


def _shape_summary(shapes):
    """The illustration as the model can read it: canvas pictures become one SVG primitive per line, other
    shapes stay JSON. Nothing geometric is dropped (a truncated picture made the model report 'empty canvas')."""
    out = []
    for sh in shapes or []:
        if not isinstance(sh, dict):
            continue
        if sh.get('type') == 'canvas':
            text = _canvas_text(sh)
        else:
            slim = {k: v for k, v in sh.items() if k not in _SHAPE_DROP}
            text = _NUM.sub(lambda x: str(round(float(x.group()), 1)), json.dumps(slim, ensure_ascii=False, default=str))
        out.append(text[:ILLUSTRATION_CAP] + ('…' if len(text) > ILLUSTRATION_CAP else ''))
    return out


def _shuffled(labels, seed):
    """Ordering items as the child sees them: shuffled (never already in the answer order), stable per sample."""
    import random
    rng = random.Random(seed)
    out = list(labels)
    for _ in range(10):
        rng.shuffle(out)
        if out != list(labels) or len(set(labels)) < 2:
            break
    return out


def describe(sample, with_key):
    """The sample as the child sees it, in both languages. ``with_key=False`` hides every trace of the answer."""
    slug = sample.skill.slug
    fr = sampling.render_question(sample.payload, slug, 'fr')
    en = sampling.render_question(sample.payload, slug, 'en')
    d = {'id': sample.code, 'level': sample.level, 'type': fr.get('q_type')}
    for lang, q in (('fr', fr), ('en', en)):
        v = {'prompt': q.get(f'prompt_{lang}', '')}
        if q.get('table'):
            v['table'] = q['table']
        if q.get('bullets'):
            v['list'] = q['bullets']
        if q.get('choices'):
            v['choices'] = [f"{i + 1}. {c.get('label', '')}" for i, c in enumerate(q['choices'])]
        if q.get('items'):
            labels = [it['label'] for it in q['items']]
            v['items_to_order'] = labels if with_key else _shuffled(labels, sample.code)
        if q.get('pairs'):
            v['left'] = [p['left'] for p in q['pairs']]
            v['right_options'] = sorted({p['right'] for p in q['pairs']})
        if q.get('q_type') == 'text_input':
            v['answer_format'] = (q.get('input') or {}).get('hint', '') or q.get('answer_type', '')
        if with_key:
            v['hint'] = q.get(f'hint_{lang}', '')
            v['explanation'] = q.get(f'explanation_{lang}', '')
        d[lang] = v
    if fr.get('shape_data'):
        d['illustration'] = _shape_summary(fr['shape_data'])
    if with_key:
        key = {'accepted_answers': fr.get('correct_answers', [])}
        idx = sampling.correct_index(fr)
        if idx is not None:
            key['correct_choice'] = idx + 1
            key['distractor_rationales'] = {
                str(i + 1): c.get('error_type') or c.get('feedback_fr') or ''
                for i, c in enumerate(fr.get('choices') or []) if not c.get('correct')}
        if fr.get('items'):
            key['correct_order'] = [it['label'] for it in sorted(fr['items'], key=lambda x: x['order'])]
        if fr.get('pairs'):
            key['correct_matches'] = {p['left']: p['right'] for p in fr['pairs']}
        d['answer_key'] = key
    return d, fr


# ── prompts ───────────────────────────────────────────────────────────────────

SOLVE_SYSTEM = """You are a careful elementary-school math teacher in Québec. Solve each problem exactly as a strong
grade-{grade} student would, using only what the student sees (prompt, table, list, illustration data, choices).
The illustration is given as a list of SVG primitives (path / line / dot / rect / circle / pie_slice / text, pixel
coordinates, y grows downward): rebuild the picture from them. It is complete; do not call it missing or truncated
unless the list really has no marks.
Problems are shown in French and English; they are the same problem.

For each problem return:
- "id": the problem id
- "answer": your final answer as short text (for choices: the label of the correct choice)
- "correct_choices": for multiple choice, the NUMBERS of every choice that is a correct answer to the question as
  written. List more than one if several choices are defensible. Empty for other types.
- "order": for ordering problems, the items in the correct order (exact labels)
- "matches": for matching problems, an object {left label: right option}
- "confident": true/false
- "ambiguous": true if the question can reasonably be read in more than one way, or information is missing
- "note": one short sentence in French when ambiguous, not confident, or the problem is broken; otherwise ""

Return {"results": [ ... ]}."""

REVIEW_SYSTEM = """You review generated math questions for Sofyana, a Québec French/English practice app for children
(grade {grade}). Each question is shown exactly as the child sees it, with its answer key, distractor rationales, hint and
explanation, plus the result of an independent solver that did NOT see the key, and the automatic lint findings.

Judge each question on these 6 criteria (true = OK):
- rendering: no raw delimiters (| \\n {{ }} **), no markup or programming values, nothing garbled.
- clarity: one clear question, no repeated sentences or data, vocabulary right for grade {grade}, correct grammar
  (plurals, articles, French elision), natural Québec French (e.g. « soccer », not « football »; space before : ; ? !)
  and natural Canadian English. Each version entirely in its own language. No needless length.
- structure: more than two related data values are shown as a table or list, not as an inline string.
- accuracy: the math and the answer key are correct; distractors are distinct, plausible child mistakes (no random
  filler numbers); primary-school rules: no negative numbers, no square roots, numbers within grade-{grade} limits.
- ambiguity: exactly one defensible answer; no hidden assumption. Take the solver result seriously: if it disagrees with
  the key or found several correct choices, find out why.
- hint_quality: the hint helps the child start without giving the answer; the explanation shows the actual working
  for THIS problem (not a generic template).

For each question return:
- "id"
- "criteria": {{"rendering": {{"ok": bool, "reason": "…"}}, … all 6 …}} — reason in French, short, concrete, quoting the
  problem text; "" when ok.
- "verdict": "clean" (publishable as is), "minor" (style issues a child would get past) or "major" (wrong, ambiguous,
  confusing or broken for a child)
- "summary": one or two sentences in French for the human reviewer.
- "suggestion": null when clean; otherwise a corrected version of the question:
  {{"prompt_fr", "prompt_en", "hint_fr", "hint_en",
    "format_type": "PLAIN_TEXT" | "MARKDOWN_TABLE" | "BULLET_LIST",
    "table": {{"headers": [[fr, en], …], "rows": [[[fr, en], …], …]}}   (when MARKDOWN_TABLE),
    "bullets": [[fr, en], …]   (when BULLET_LIST),
    "choices": [{{"label_fr", "label_en", "correct": bool}}, …]   (multiple choice only, same number of choices,
                labels WITHOUT the "1." numbering shown to you)}}
  Keep the same mathematical content and difficulty. Only change the correct answer if the key is wrong, and say so in
  the summary. Prompts may use **bold**.

Return {{"results": [ … ]}}."""

DIAGNOSE_SYSTEM = """You are a senior developer and math educator reviewing ONE question generator of Sofyana (Québec
French/English math practice, grade {grade}). You receive all sampled questions of the skill (with answer keys) and the
per-question review findings. Questions come from code, so look for RECURRING defects of the generator — what will keep
happening for future questions — rather than one-off accidents.

Return {{"summary": "2-3 sentences in French on the overall quality of this generator",
         "issues": [{{"title": "short French title",
                      "criterion": one of rendering|clarity|structure|accuracy|ambiguity|hint_quality,
                      "severity": "major" | "minor",
                      "samples": ["Q-…", …],
                      "fix": "precise instruction for the developer in French (what to change in the generator)"}}]}}
Return an empty issues list when the generator is fine. Do not report something that only appears in one sample unless
it is a math error or a broken question."""


def _fill(template, grade):
    return template.replace('{grade}', str(grade)).replace('{{', '{').replace('}}', '}')


# ── comparing the solver with the key ─────────────────────────────────────────

def compare(q, res):
    """{status: match|mismatch|multiple|unsure|none, ai_answer, key, note, …}"""
    if not isinstance(res, dict):
        return {'status': 'none', 'ai_answer': '', 'key': '', 'note': 'Pas de réponse du solveur.'}
    qt = q.get('q_type')
    out = {'ai_answer': str(res.get('answer', ''))[:200], 'note': str(res.get('note') or '')[:400],
           'confident': bool(res.get('confident', True)), 'ambiguous': bool(res.get('ambiguous'))}
    if qt == 'multiple_choice':
        idx = sampling.correct_index(q)
        out['key'] = q['choices'][idx]['label'] if idx is not None else ''
        picks = set()
        for x in res.get('correct_choices') or []:
            try:
                n = int(x) - 1
            except (TypeError, ValueError):
                continue
            if 0 <= n < len(q.get('choices') or []):
                picks.add(n)
        if not picks:                     # fall back on the answer text
            for i, c in enumerate(q.get('choices') or []):
                if str(c.get('label', '')).strip().lower() == out['ai_answer'].strip().lower():
                    picks.add(i)
        out['ai_choices'] = sorted(p + 1 for p in picks)
        if not picks:
            status = 'unsure'
        elif idx not in picks:
            status = 'mismatch'
        elif len(picks) > 1:
            status = 'multiple'
        else:
            status = 'match'
    elif qt == 'text_input':
        answers = [str(a) for a in q.get('correct_answers') or []]
        out['key'] = answers[0] if answers else ''
        if not out['ai_answer']:
            status = 'unsure'
        else:
            status = 'match' if check_answer(out['ai_answer'], answers, q.get('answer_type')) else 'mismatch'
    elif qt in ('ordering', 'sorting'):
        key = [it['label'] for it in sorted(q.get('items') or [], key=lambda x: x['order'])]
        out['key'] = ' < '.join(key)
        got = [str(x) for x in res.get('order') or []]
        out['ai_answer'] = ' < '.join(got) or out['ai_answer']
        status = 'unsure' if not got else ('match' if got == key else 'mismatch')
    elif qt == 'mix_match':
        key = {p['left']: p['right'] for p in q.get('pairs') or []}
        out['key'] = '; '.join(f'{k} → {v}' for k, v in key.items())
        got = res.get('matches') if isinstance(res.get('matches'), dict) else {}
        out['ai_answer'] = '; '.join(f'{k} → {v}' for k, v in got.items()) or out['ai_answer']
        status = 'unsure' if not got else ('match' if all(str(got.get(k, '')) == v for k, v in key.items()) else 'mismatch')
    else:
        out['key'] = ''
        status = 'none'
    if status == 'match' and (out['ambiguous'] or not out['confident']):
        status = 'unsure'
    out['status'] = status
    return out


SOLVER_RISK = {'mismatch': 40, 'multiple': 40, 'unsure': 10, 'match': 0, 'none': 0}


def risk_of(verdict, criteria, solver, lint):
    r = {'major': 50, 'minor': 20}.get(verdict, 0)
    r += 5 * sum(1 for c in criteria.values() if not c.get('ok', True))
    r += SOLVER_RISK.get(solver.get('status'), 0)
    if any(f.get('severity') == 'error' for f in lint or []):
        r += 20
    return min(100, r)


def _clean_criteria(raw):
    out = {}
    raw = raw if isinstance(raw, dict) else {}
    for k in CRITERIA_KEYS:
        c = raw.get(k)
        if isinstance(c, dict):
            out[k] = {'ok': bool(c.get('ok', True)), 'reason': str(c.get('reason') or '')[:400]}
        elif isinstance(c, bool):
            out[k] = {'ok': c, 'reason': ''}
        else:
            out[k] = {'ok': True, 'reason': ''}
    return out


def _results(reply):
    rows = reply.get('results') if isinstance(reply, dict) else reply
    return {str(r.get('id')): r for r in rows or [] if isinstance(r, dict) and r.get('id')}


# ── LLM work (thread-safe: no database access) ────────────────────────────────

def _batched(system, key, entries, skill, model, max_tokens):
    """
    One call for ``entries``; if the reply is empty, cut off or not JSON (reasoning models can
    spend their whole output budget thinking), split the batch in two and retry, down to one entry.
    Returns ({id: result}, error message or '').
    """
    try:
        out = _results(llm.complete_json(
            system, json.dumps({'skill': skill, key: entries}, ensure_ascii=False),
            max_tokens=max_tokens, model=model, timeout=CALL_TIMEOUT))
        missing = [e for e in entries if e['id'] not in out]
        if missing and len(entries) > 1 and len(missing) < len(entries):
            more, err = _batched(system, key, missing, skill, model, max_tokens)
            out.update(more)
        return out, ''
    except Exception as exc:
        if len(entries) > 1:
            mid = len(entries) // 2
            a, ea = _batched(system, key, entries[:mid], skill, model, max_tokens)
            b, eb = _batched(system, key, entries[mid:], skill, model, max_tokens)
            return {**a, **b}, ea or eb
        log.warning('AI call failed for %s: %s', skill, exc)
        return {}, f'{exc.__class__.__name__}: {exc}'[:300]


def analyse(job, model):
    """job = {'grade', 'skill', 'items': [{'id', 'pk', 'blind', 'full', 'q', 'lint'}]} → {pk: review dict}"""
    grade = job['grade'] or '3-6'
    reviews = {}
    for start in range(0, len(job['items']), CHUNK):
        chunk = job['items'][start:start + CHUNK]
        solved, solve_error = _batched(_fill(SOLVE_SYSTEM, grade), 'problems', [it['blind'] for it in chunk],
                                       job['skill'], model, MAX_TOKENS)
        comparisons = {it['id']: compare(it['q'], solved.get(it['id'])) for it in chunk}
        payload = [dict(it['full'], independent_solver=comparisons[it['id']],
                        automatic_lint=[f"{f['rule']}: {f['message']}" for f in it['lint']])
                   for it in chunk]
        reviewed, review_error = _batched(_fill(REVIEW_SYSTEM, grade), 'questions', payload,
                                          job['skill'], model, MAX_TOKENS)
        for it in chunk:
            r = reviewed.get(it['id'])
            solver = comparisons[it['id']]
            if not isinstance(r, dict):
                reviews[it['pk']] = {'verdict': AIReview.ERROR, 'criteria': {}, 'solver': solver, 'summary': '',
                                     'suggestion': None,
                                     'error': review_error or solve_error or "Pas de résultat de l'IA pour cette question."}
                continue
            criteria = _clean_criteria(r.get('criteria'))
            verdict = r.get('verdict') if r.get('verdict') in ('clean', 'minor', 'major') else 'minor'
            if verdict == 'clean' and not all(c['ok'] for c in criteria.values()):
                verdict = 'minor'
            if solver['status'] in ('mismatch', 'multiple') and verdict == 'clean':
                verdict = 'major'           # the solver disagrees with the key: never call that clean
            sugg = proposals.clean(r['suggestion']) if isinstance(r.get('suggestion'), dict) else None
            for c in (sugg or {}).get('choices') or []:
                # choices are numbered for the model (« 2. 155 »): the numbers are not part of the label
                c['label_fr'] = _NUMBERING.sub('', c['label_fr'])
                c['label_en'] = _NUMBERING.sub('', c['label_en'])
            reviews[it['pk']] = {'verdict': verdict, 'criteria': criteria, 'solver': solver,
                                 'summary': str(r.get('summary') or '')[:1000],
                                 'suggestion': sugg if verdict != 'clean' else None, 'error': solve_error}
    return reviews


def diagnose(job, reviews, model):
    """One call over every sample of the skill (with per-sample findings) → generator-level issues."""
    findings = []
    for it in job['items']:
        r = reviews.get(it['pk'])
        if r and r['verdict'] != AIReview.ERROR:
            findings.append({'id': it['id'], 'verdict': r['verdict'], 'summary': r['summary'],
                             'failed': [k for k, c in (r['criteria'] or {}).items() if not c.get('ok', True)],
                             'solver': (r['solver'] or {}).get('status')})
    try:
        d = llm.complete_json(
            _fill(DIAGNOSE_SYSTEM, job['grade'] or '3-6'),
            json.dumps({'skill': job['skill'], 'questions': [it['full'] for it in job['items']], 'findings': findings},
                       ensure_ascii=False),
            max_tokens=MAX_TOKENS, model=model, timeout=CALL_TIMEOUT)
    except Exception as exc:
        log.warning('AI diagnosis failed for %s: %s', job['skill'], exc)
        return {'summary': '', 'issues': [], 'error': f'{exc.__class__.__name__}: {exc}'[:300]}
    issues = []
    for i in (d.get('issues') if isinstance(d, dict) else None) or []:
        if isinstance(i, dict) and i.get('title'):
            issues.append({'title': str(i['title'])[:200],
                           'criterion': i.get('criterion') if i.get('criterion') in CRITERIA_KEYS else 'clarity',
                           'severity': 'major' if i.get('severity') == 'major' else 'minor',
                           'samples': [str(x) for x in (i.get('samples') or [])][:20],
                           'fix': str(i.get('fix') or '')[:1500]})
    return {'summary': str(d.get('summary') or '')[:1500] if isinstance(d, dict) else '', 'issues': issues, 'error': ''}


def _work(job, diag_job, model):
    reviews = analyse(job, model) if job['items'] else {}
    diag = diagnose(diag_job, {**diag_job['prior'], **reviews}, model) if diag_job is not None else None
    return reviews, diag


# ── database side ─────────────────────────────────────────────────────────────

def _review_dict(r):
    return {'verdict': r.verdict, 'criteria': r.criteria, 'solver': r.solver, 'summary': r.summary}


def build_job(skill, samples):
    items = []
    for s in samples:
        blind, _ = describe(s, with_key=False)
        full, fr = describe(s, with_key=True)
        items.append({'id': s.code, 'pk': s.pk, 'blind': blind, 'full': full, 'q': fr, 'lint': s.lint})
    return {'skill': f'{skill.slug} — {skill.name_fr or skill.name_en}', 'grade': skill.domain.grade, 'items': items}


def live_samples(skill):
    return list(QuestionSample.objects.filter(skill=skill).exclude(status=QuestionSample.REJECTED)
                .select_related('skill', 'skill__domain').order_by('id'))


def build_diag_job(skill):
    """Every live sample of the skill, plus their existing current reviews (not paid for twice)."""
    samples = live_samples(skill)
    job = build_job(skill, samples)
    job['prior'] = {pk: _review_dict(r) for pk, r in current_reviews(samples).items()
                    if not r.pending and r.verdict != AIReview.ERROR}
    job['samples'] = samples
    return job


def save_reviews(samples, reviews, model, pending=None):
    by_pk = {s.pk: s for s in samples}
    pending = pending or {}
    for pk, r in reviews.items():
        s = by_pk[pk]
        risk = 0 if r['verdict'] == AIReview.ERROR else risk_of(r['verdict'], r['criteria'], r['solver'], s.lint)
        fields = dict(fingerprint=s.fingerprint, model=model, verdict=r['verdict'], risk=risk, criteria=r['criteria'],
                      summary=r['summary'], solver=r['solver'], suggestion=r['suggestion'], error=r['error'],
                      pending=False)
        if pk in pending:
            AIReview.objects.filter(pk=pending[pk]).update(**fields)
        else:
            AIReview.objects.create(sample=s, **fields)
        if r['verdict'] != AIReview.ERROR:
            AuditEntry.objects.create(sample=s, user=None, action='ai_review',
                                      note=f"{r['verdict']} · risque {risk} · {r['summary']}"[:2000])


def save_diagnosis(skill, diag_job, diag, model, pending_pk=None):
    fields = dict(model=model, sample_ids=[s.code for s in diag_job['samples']],
                  fingerprints=[s.fingerprint for s in diag_job['samples']],
                  summary=diag['summary'], issues=diag['issues'], error=diag['error'], pending=False)
    if pending_pk:
        SkillDiagnosis.objects.filter(pk=pending_pk).update(**fields)
    else:
        SkillDiagnosis.objects.create(skill=skill, **fields)


def samples_needing_review(skill, force=False):
    samples = live_samples(skill)
    if force:
        return samples
    done = set(AIReview.objects.filter(sample__skill=skill, pending=False).exclude(verdict=AIReview.ERROR)
               .values_list('sample_id', 'fingerprint'))
    return [s for s in samples if (s.pk, s.fingerprint) not in done]


def diagnosis_is_current(skill, samples):
    last = latest_diagnosis(skill)
    return bool(last and not last.pending and not last.error
                and sorted(last.fingerprints) == sorted(s.fingerprint for s in samples))


def run_skills(skills, workers=4, force=False, with_diagnosis=True, progress=None):
    """Synchronous batch (management command): LLM calls in a thread pool, database writes in this thread."""
    model = model_name()
    jobs = []
    for skill in skills:
        samples = samples_needing_review(skill, force)
        diag_job = None
        if with_diagnosis:
            diag_job = build_diag_job(skill)
            if not samples and not force and diagnosis_is_current(skill, diag_job['samples']):
                diag_job = None
        if not samples and diag_job is None:
            continue
        jobs.append((skill, samples, build_job(skill, samples), diag_job))
    done = 0
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(_work, job, diag_job, model): (skill, samples, diag_job)
                   for skill, samples, job, diag_job in jobs}
        for fut in as_completed(futures):
            skill, samples, diag_job = futures[fut]
            try:
                reviews, diag = fut.result()
            except Exception as exc:          # never lose the whole batch for one skill
                log.exception('AI review crashed for %s', skill.slug)
                if progress:
                    progress(skill, None, exc)
                continue
            save_reviews(samples, reviews, model)
            if diag is not None:
                save_diagnosis(skill, diag_job, diag, model)
            done += 1
            if progress:
                progress(skill, reviews, None)
    return done, len(jobs)


# ── background runs from the Studio (one thread, results polled from the DB) ───

def start_background(skill, samples, with_diagnosis):
    """Create 'pending' rows now (visible to every gunicorn worker), fill them in a thread."""
    model = model_name()
    pending = {s.pk: AIReview.objects.create(sample=s, fingerprint=s.fingerprint, model=model,
                                             verdict=AIReview.PENDING, pending=True).pk for s in samples}
    diag_job = build_diag_job(skill) if with_diagnosis else None
    diag_pk = SkillDiagnosis.objects.create(skill=skill, model=model, pending=True).pk if with_diagnosis else None
    job = build_job(skill, samples)

    def work():
        close_old_connections()
        try:
            reviews, diag = _work(job, diag_job, model)
            save_reviews(samples, reviews, model, pending)
            if diag is not None:
                save_diagnosis(skill, diag_job, diag, model, diag_pk)
        except Exception as exc:
            log.exception('background AI review failed for %s', skill.slug)
            err = f'{exc.__class__.__name__}: {exc}'[:300]
            AIReview.objects.filter(pk__in=pending.values(), pending=True).update(
                pending=False, verdict=AIReview.ERROR, error=err)
            if diag_pk:
                SkillDiagnosis.objects.filter(pk=diag_pk, pending=True).update(pending=False, error=err)
        finally:
            close_old_connections()

    t = threading.Thread(target=work, daemon=True)
    t.start()
    return t


def expire_stale_pending():
    """A server restart kills background threads: don't show 'running' forever."""
    cutoff = timezone.now() - PENDING_TIMEOUT
    AIReview.objects.filter(pending=True, created_at__lt=cutoff).update(
        pending=False, verdict=AIReview.ERROR, error='Analyse interrompue (redémarrage du serveur ?)')
    SkillDiagnosis.objects.filter(pending=True, created_at__lt=cutoff).update(
        pending=False, error='Analyse interrompue (redémarrage du serveur ?)')


# ── reading ───────────────────────────────────────────────────────────────────

def latest_review(sample):
    return sample.ai_reviews.first()


def current_reviews(samples):
    """{sample_pk: latest AIReview} for reviews still matching the sample's current output (or running)."""
    out = {}
    fps = {s.pk: s.fingerprint for s in samples}
    for r in AIReview.objects.filter(sample_id__in=fps).order_by('sample_id', '-created_at', '-id'):
        if r.sample_id not in out and (r.pending or r.fingerprint == fps[r.sample_id]):
            out[r.sample_id] = r
    return out


def latest_diagnosis(skill):
    return skill.ai_diagnoses.first()


def agreement(skills):
    """
    How often the AI agrees with human decisions (calibration).  Overall: AI 'clean'
    vs human APPROVED.  Per criterion: only samples whose reviewer engaged with the
    checklist (approved = all six OK; rework/reject with at least one box ticked:
    unticked boxes = failed).
    """
    decided = list(QuestionSample.objects.filter(skill__in=skills, reviewed_by__isnull=False)
                   .filter(status__in=[QuestionSample.APPROVED, QuestionSample.FLAGGED, QuestionSample.REJECTED])
                   .select_related('skill'))
    reviews = current_reviews(decided)
    overall = {'n': 0, 'agree': 0, 'missed': 0, 'false_alarm': 0}
    per = {k: {'n': 0, 'agree': 0, 'missed': 0, 'false_alarm': 0} for k in CRITERIA_KEYS}
    missed = []
    for s in decided:
        r = reviews.get(s.pk)
        if not r or r.pending or r.verdict == AIReview.ERROR:
            continue
        human_ok = s.status == QuestionSample.APPROVED
        ai_ok = r.verdict == AIReview.CLEAN
        overall['n'] += 1
        if human_ok == ai_ok:
            overall['agree'] += 1
        elif ai_ok:
            overall['missed'] += 1
            if len(missed) < 8:
                missed.append(s)
        else:
            overall['false_alarm'] += 1
        if not (human_ok or any(s.checklist.get(k) for k in CRITERIA_KEYS)):
            continue
        for k in CRITERIA_KEYS:
            h = True if human_ok else bool(s.checklist.get(k))
            a = r.criteria.get(k, {}).get('ok', True)
            per[k]['n'] += 1
            if h == a:
                per[k]['agree'] += 1
            elif a:
                per[k]['missed'] += 1
            else:
                per[k]['false_alarm'] += 1

    def pct(d):
        return round(d['agree'] / d['n'] * 100) if d['n'] else None

    return {'overall': dict(overall, pct=pct(overall)),
            'criteria': [dict(per[k], key=k, label=label, pct=pct(per[k])) for k, label, _ in CRITERIA],
            'missed_examples': missed}
