"""
Reviewer rewrites ("proposals").

A proposal is what the reviewer wants the question to look like.  It is never
served to students (questions are generated); it is the precise, visual spec a
developer uses to fix the generator, and the simulator previews it.

Shape (every key optional):
    {
      "format_type": "PLAIN_TEXT" | "MARKDOWN_TABLE" | "BULLET_LIST",
      "prompt_fr": "...", "prompt_en": "...",
      "hint_fr": "...",   "hint_en": "...",
      "table":   {"headers": [[fr, en], ...], "rows": [[[fr, en], ...], ...]},
      "bullets": [[fr, en], ...],
      "choices": [{"label_fr": "...", "label_en": "...", "correct": true}, ...]
    }
"""
import copy

FORMATS = ['PLAIN_TEXT', 'MARKDOWN_TABLE', 'BULLET_LIST', 'IMAGE_PROMPT']


def _pair(v):
    if isinstance(v, (list, tuple)) and len(v) == 2:
        return [str(v[0]), str(v[1])]
    return [str(v), str(v)]


def from_payload(payload):
    """The editor's starting point: the generator's own question, in proposal shape."""
    p = payload or {}
    if p.get('table'):
        fmt = 'MARKDOWN_TABLE'
    elif p.get('bullets'):
        fmt = 'BULLET_LIST'
    elif p.get('shape_data'):
        fmt = 'IMAGE_PROMPT'
    else:
        fmt = 'PLAIN_TEXT'
    t = p.get('table') or {}
    return {
        'format_type': fmt,
        'prompt_fr': p.get('prompt_fr', ''), 'prompt_en': p.get('prompt_en', ''),
        'hint_fr': p.get('hint_fr', ''), 'hint_en': p.get('hint_en', ''),
        'table': {'headers': [_pair(h) for h in t.get('headers') or []],
                  'rows': [[_pair(c) for c in row] for row in t.get('rows') or []]},
        'bullets': [_pair(b) for b in p.get('bullets') or []],
        'choices': [{'label_fr': str(c.get('label', '')),
                     'label_en': str(c.get('label_en') or c.get('label', '')),
                     'correct': bool(c.get('correct'))}
                    for c in p.get('choices') or []],
    }


def clean(raw):
    """Validate / normalise a proposal posted by the editor."""
    if not isinstance(raw, dict):
        return None
    out = {'format_type': raw.get('format_type') if raw.get('format_type') in FORMATS else 'PLAIN_TEXT'}
    for k in ('prompt_fr', 'prompt_en', 'hint_fr', 'hint_en'):
        out[k] = str(raw.get(k) or '')[:2000]
    t = raw.get('table') or {}
    out['table'] = {'headers': [_pair(h) for h in (t.get('headers') or [])[:6]],
                    'rows': [[_pair(c) for c in (row or [])[:6]] for row in (t.get('rows') or [])[:20]]}
    out['bullets'] = [_pair(b) for b in (raw.get('bullets') or [])[:20]]
    out['choices'] = [{'label_fr': str(c.get('label_fr', ''))[:300], 'label_en': str(c.get('label_en', ''))[:300],
                       'correct': bool(c.get('correct'))}
                      for c in (raw.get('choices') or [])[:5] if isinstance(c, dict)]
    return out


def apply(payload, proposal):
    """The generator payload with the proposal applied — what the simulator renders."""
    q = copy.deepcopy(payload)
    if not proposal:
        return q
    for k in ('prompt_fr', 'prompt_en', 'hint_fr', 'hint_en'):
        if proposal.get(k) is not None:
            q[k] = proposal[k]
    fmt = proposal.get('format_type')
    q.pop('table', None)
    q.pop('bullets', None)
    if fmt == 'MARKDOWN_TABLE' and (proposal.get('table') or {}).get('rows'):
        q['table'] = proposal['table']
    elif fmt == 'BULLET_LIST' and proposal.get('bullets'):
        q['bullets'] = proposal['bullets']
    if q.get('q_type') == 'multiple_choice' and proposal.get('choices'):
        old = q.get('choices') or []
        new = []
        for i, c in enumerate(proposal['choices']):
            base = dict(old[i]) if i < len(old) else {'error_type': '', 'feedback_en': '', 'feedback_fr': ''}
            base.update({'label': c['label_fr'], 'label_en': c['label_en'] or c['label_fr'], 'correct': c['correct']})
            new.append(base)
        q['choices'] = new
        q['correct_answers'] = [c['label_fr'] for c in proposal['choices'] if c['correct']]
    return q


def differs(payload, proposal):
    return bool(proposal) and clean(proposal) != clean(from_payload(payload))
