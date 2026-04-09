import re
import random
from fractions import Fraction as _Frac


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _frac_str(n, d):
    """Simplified fraction as 'n/d' or just 'n' if d==1."""
    if d == 0:
        return '0'
    g = _gcd(abs(n), abs(d))
    n, d = n // g, d // g
    return str(n) if d == 1 else f'{n}/{d}'


def _is_positive(s):
    """
    Return True if string s represents a value strictly > 0.
    Unparseable strings (e.g. '9π') pass through so they are never filtered.
    """
    try:
        if '/' in s:
            return int(s.split('/')[0]) > 0
        return float(s) > 0
    except (ValueError, TypeError):
        return True   # keep things like '9π', '12π', etc.


def _shuffle_mc(correct_str, candidates):
    """
    Build a 5-item MC choices list with the correct answer at a random position.
    Only positive (> 0) candidates are accepted.
    """
    seen = {str(correct_str)}
    pool = []
    for c in candidates:
        s = str(c)
        if s not in seen and _is_positive(s):
            seen.add(s)
            pool.append(s)
        if len(pool) == 4:
            break
    # Fallback padding — always positive
    pad = 1
    while len(pool) < 4:
        try:
            base_val = abs(int(float(
                correct_str.split('/')[0] if '/' in correct_str else correct_str
            )))
        except (ValueError, AttributeError):
            base_val = 1
        s = str(base_val + pad * 37)
        if s not in seen:
            seen.add(s)
            pool.append(s)
        pad += 1
    choices = [{'label': d, 'correct': False, 'error_type': '', 'feedback_en': '', 'feedback_fr': ''}
               for d in pool[:4]]
    pos = random.randint(0, 4)
    choices.insert(pos, {'label': str(correct_str), 'correct': True, 'error_type': '', 'feedback_en': '', 'feedback_fr': ''})
    return choices[:5]


def _tagged_shuffle_mc(correct_str, tagged_candidates):
    """
    Build a 5-item MC choices list with misconception metadata on wrong choices.

    tagged_candidates: list of either:
      - str / number: plain distractor (no metadata)
      - (label, error_type, feedback_en, feedback_fr): fully tagged distractor
      - (label, error_type): distractor with error type but no custom feedback

    Returns list of dicts: {label, correct, error_type, feedback_en, feedback_fr}
    """
    seen = {str(correct_str)}
    pool = []
    for c in tagged_candidates:
        if isinstance(c, tuple):
            label = str(c[0])
            error_type = c[1] if len(c) > 1 else ''
            fb_en = c[2] if len(c) > 2 else ''
            fb_fr = c[3] if len(c) > 3 else ''
        else:
            label, error_type, fb_en, fb_fr = str(c), '', '', ''
        if label not in seen and _is_positive(label):
            seen.add(label)
            pool.append({'label': label, 'correct': False,
                         'error_type': error_type, 'feedback_en': fb_en, 'feedback_fr': fb_fr})
        if len(pool) == 4:
            break
    # Fallback padding — always positive, no misconception tag
    pad = 1
    while len(pool) < 4:
        try:
            base_val = abs(int(float(
                correct_str.split('/')[0] if '/' in correct_str else correct_str
            )))
        except (ValueError, AttributeError):
            base_val = 1
        s = str(base_val + pad * 37)
        if s not in seen:
            seen.add(s)
            pool.append({'label': s, 'correct': False, 'error_type': 'distractor',
                         'feedback_en': '', 'feedback_fr': ''})
        pad += 1
    pos = random.randint(0, 4)
    pool.insert(pos, {'label': str(correct_str), 'correct': True,
                      'error_type': '', 'feedback_en': '', 'feedback_fr': ''})
    return pool[:5]


def _normalize_answer(s: str) -> str:
    """
    Canonicalize a student's typed answer for comparison.
    - Replace comma-decimal with dot  ("3,14" → "3.14")
    - Strip trailing unit labels     ("12 cm" → "12", "3/4 m" → "3/4")
    - Simplify fractions             ("4/6" → "2/3")
    - Strip leading zeros on integers ("007" → "7")
    """
    s = str(s).strip()
    s = s.replace(',', '.')
    s = re.sub(r'[a-zA-Z°\s]+$', '', s).strip()
    if '/' in s:
        try:
            f = _Frac(s)
            return _frac_str(f.numerator, f.denominator)
        except Exception:
            pass
    try:
        if '.' not in s and s.lstrip('-').lstrip('0'):
            return str(int(s))
    except ValueError:
        pass
    return s


def _unique(*groups):
    """Flatten groups into a deduped list, keeping only positive (> 0) values."""
    seen = set()
    out = []
    for g in groups:
        for x in g:
            s = str(x)
            if s not in seen and _is_positive(s):
                seen.add(s)
                out.append(s)
    return out
