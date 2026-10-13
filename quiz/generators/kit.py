"""
kit.py — small builders shared by the curriculum-upgrade generators (2026-10).

Every generator returns the same problem dict as the legacy ones; these helpers
only remove the boilerplate:

    mc(correct, distractors, ...)     → multiple choice, always 5 distinct choices
    typed(answers, answer_type, ...)  → text input
    ordering(labels_in_order, ...)    → drag-to-order
    match(pairs, ...)                 → mix & match

Labels may be plain strings or (fr, en) pairs. Distractors may be a label or a
4-tuple (label, error_type, feedback_en, feedback_fr). ``pad`` is a callable that
returns one more plausible distractor; it is called until 4 distinct ones exist,
so a choice list is never padded with unrelated numbers.
"""
import random
from fractions import Fraction

from .base import _choice, _split_label


def _key(label):
    return _split_label(label)[0]


def mc_choices(correct, distractors, pad=None):
    seen = {_key(correct)}
    pool = []
    for d in distractors:
        if d is None:
            continue
        # A 4-tuple is a tagged distractor; a 2-tuple is always a (fr, en) label.
        if isinstance(d, tuple) and len(d) == 4:
            label, err, fb_en, fb_fr = d
        else:
            label, err, fb_en, fb_fr = d, '', '', ''
        k = _key(label)
        if k in seen:
            continue
        seen.add(k)
        pool.append(_choice(label, False, err or 'distractor', fb_en, fb_fr))
        if len(pool) == 4:
            break
    tries = 0
    while len(pool) < 4 and pad is not None and tries < 200:
        tries += 1
        label = pad()
        k = _key(label)
        if k not in seen:
            seen.add(k)
            pool.append(_choice(label, False, 'distractor'))
    if len(pool) < 4:
        raise ValueError(f'not enough distractors for {correct!r}: {pool}')
    pool.insert(random.randint(0, 4), _choice(correct, True))
    return pool


def _base(q_type, prompt, hint, explanation, correct_answers, shape=None, **extra):
    """prompt/hint/explanation are (fr, en) pairs; explanation may be a pair of lists (steps)."""
    ex_fr, ex_en = explanation
    if isinstance(ex_fr, (list, tuple)):
        ex_fr = '\n'.join(ex_fr)
    if isinstance(ex_en, (list, tuple)):
        ex_en = '\n'.join(ex_en)
    shapes = shape if isinstance(shape, list) else ([shape] if shape else [])
    q = {
        'q_type': q_type,
        'prompt_fr': prompt[0], 'prompt_en': prompt[1],
        'hint_fr': hint[0], 'hint_en': hint[1],
        'explanation_fr': ex_fr, 'explanation_en': ex_en,
        'shape_data': shapes, 'show_illustration': bool(shapes),
        'choices': [], 'pairs': [],
        'correct_answers': correct_answers,
        'time_limit': extra.pop('time_limit', 45), 'points': extra.pop('points', 1),
    }
    q.update(extra)
    return q


def mc(prompt, correct, distractors, hint, explanation, shape=None, pad=None, **extra):
    choices = mc_choices(correct, distractors, pad)
    fr, en = _split_label(correct)
    answers = [fr] + ([en] if en and en != fr else [])
    return _base('multiple_choice', prompt, hint, explanation, answers, shape, choices=choices, **extra)


def typed(prompt, answers, answer_type, hint, explanation, shape=None, **extra):
    answers = [str(a) for a in (answers if isinstance(answers, (list, tuple)) else [answers])]
    return _base('text_input', prompt, hint, explanation, answers, shape, answer_type=answer_type, **extra)


def ordering(prompt, labels_in_order, hint, explanation, shape=None, **extra):
    items = []
    for i, label in enumerate(labels_in_order):
        fr, en = _split_label(label)
        it = {'label': fr, 'order': i + 1}
        if en is not None:
            it['label_en'] = en
        items.append(it)
    return _base('ordering', prompt, hint, explanation, [it['label'] for it in items], shape, items=items, **extra)


def match(prompt, pairs, hint, explanation, shape=None, **extra):
    """pairs: [(left, right)], each side a label or (fr, en)."""
    out = []
    for left, right in pairs:
        lf, le = _split_label(left)
        rf, re_ = _split_label(right)
        p = {'left': lf, 'right': rf}
        if le is not None:
            p['left_en'] = le
        if re_ is not None:
            p['right_en'] = re_
        out.append(p)
    return _base('mix_match', prompt, hint, explanation, [p['right'] for p in out], shape, pairs=out, **extra)


# ── numbers & words ─────────────────────────────────────────────────────────

def N(n):
    """Group digits with a narrow no-break space: 12 345 (no grouping under 10 000? keep 4-digit plain)."""
    s = str(n)
    if len(s) <= 4:
        return s
    out = ''
    while len(s) > 3:
        out = ' ' + s[-3:] + out
        s = s[:-3]
    return s + out


def dec(x, places=None):
    """Decimal as (fr, en) strings: 2,5 / 2.5 (trailing zeros kept if places given)."""
    s = f'{x:.{places}f}' if places is not None else f'{x:g}'
    return s.replace('.', ','), s


def frac(n, d):
    return f'{n}/{d}'


def simplest(n, d):
    f = Fraction(n, d)
    return f'{f.numerator}/{f.denominator}' if f.denominator != 1 else str(f.numerator)


_DEN_FR = {2: ('demi', 'demis'), 3: ('tiers', 'tiers'), 4: ('quart', 'quarts')}
_DEN_EN = {2: ('half', 'halves'), 3: ('third', 'thirds'), 4: ('quarter', 'quarters')}
_ORD_FR = {5: 'cinquième', 6: 'sixième', 7: 'septième', 8: 'huitième', 9: 'neuvième', 10: 'dixième',
           11: 'onzième', 12: 'douzième', 100: 'centième'}
_ORD_EN = {5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth',
           11: 'eleventh', 12: 'twelfth', 100: 'hundredth'}
_NUM_FR = ['zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze']
_NUM_EN = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']


def frac_words(n, d):
    """(fr, en) words for n/d with small n: « trois quarts » / "three quarters"."""
    if d in _DEN_FR:
        fr = _DEN_FR[d][0 if n == 1 else 1]
        en = _DEN_EN[d][0 if n == 1 else 1]
    else:
        fr = _ORD_FR[d] + ('' if n == 1 else 's')
        en = _ORD_EN[d] + ('' if n == 1 else 's')
    nfr = 'un' if n == 1 else _NUM_FR[n]
    if d == 2 and n == 1:
        return 'un demi', 'one half'
    return f'{nfr} {fr}', f'{_NUM_EN[n]} {en}'


def pick(seq):
    return random.choice(seq)
