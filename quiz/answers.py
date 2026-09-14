"""
Typed answer checking — the single source of truth for "is this answer right?".

Every problem declares (or we infer) an ``answer_type``.  The same type drives
both the server-side comparison and the input widget shown to the student, so
what the front end accepts and what the back end compares can never drift apart.

Comparison is by *value*, never by string:  "6" == "6.0" == "6,0" == "6 cm",
"1/2" == "2/4" == "0.5",  "1 h 30 min" == "90 min",  "(3, 4)" == "3,4".

Conventions (Québec French first, English tolerated):
- A comma is always a DECIMAL separator ("3,5" → 3.5). Thousands are grouped
  with spaces ("1 234"), never with commas.
- Trailing units, currency signs and words are ignored for numeric types.
"""
import re
import unicodedata
from fractions import Fraction

ANSWER_TYPES = [
    ('integer',    'Integer'),
    ('decimal',    'Decimal number'),
    ('fraction',   'Fraction'),
    ('money',      'Money amount'),
    ('duration',   'Duration (h / min)'),
    ('coordinate', 'Coordinate pair (x, y)'),
    ('symbol',     'Comparison symbol (<, >, =)'),
    ('text',       'Free text / word'),
]
NUMERIC_TYPES = {'integer', 'decimal', 'fraction', 'money'}

_UNICODE_MINUS = '−'
_SPACES = '   '          # nbsp, narrow nbsp, thin space
_CURRENCY = '$€£'

_DURATION_RE = re.compile(
    r'^\s*(?:(\d+)\s*(?:h(?:eures?|ours?|rs?|r)?|:))?\s*(?:(\d+)\s*(?:min(?:utes?)?|m|mn)?)?\s*$',
    re.IGNORECASE)
_COORD_RE = re.compile(r'^\s*\(?\s*(-?[\d.,]+)\s*[;,]\s*(-?[\d.,]+)\s*\)?\s*$')
_MIXED_RE = re.compile(r'^(-?)(\d+)\s+(\d+)\s*/\s*(\d+)$')
_FRAC_RE = re.compile(r'^(-?\d+)\s*/\s*(-?\d+)$')
_SYMBOLS = {'<', '>', '=', '≤', '≥', '≠'}


# ── low-level normalisation ──────────────────────────────────────────────────

def _clean(s) -> str:
    s = '' if s is None else str(s)
    for ch in _SPACES:
        s = s.replace(ch, ' ')
    s = s.replace(_UNICODE_MINUS, '-')
    return re.sub(r'\s+', ' ', s).strip()


def _strip_units(s: str) -> str:
    """Drop currency signs, unit words, degree/exponent marks from a numeric string."""
    s = s.strip()
    s = s.strip(_CURRENCY).strip()
    # Trailing unit words / symbols: "12 cm", "5 m²", "20 °C".  Only strip when
    # no digit follows the unit, so "1 h 20 min" is NOT reduced to "1".
    s = re.sub(r'\s*[a-zA-Zµ°²³]+[^\d]*$', '', s).strip()
    s = s.strip(_CURRENCY).strip()
    return s


def parse_number(s):
    """
    Parse a student-typed numeric string into a Fraction (exact), or None.
    Accepts integers, decimals (dot or comma), simple fractions, mixed numbers,
    thousands grouped with spaces, and trailing units.
    """
    s = _clean(s)
    if not s:
        return None
    s = _strip_units(s)
    if not s:
        return None
    m = _MIXED_RE.match(s)
    if m:
        sign, whole, num, den = m.groups()
        if int(den) == 0:
            return None
        val = Fraction(int(whole)) + Fraction(int(num), int(den))
        return -val if sign else val
    m = _FRAC_RE.match(s)
    if m:
        num, den = int(m.group(1)), int(m.group(2))
        if den == 0:
            return None
        return Fraction(num, den)
    # thousands with spaces: "1 234 567" → "1234567" (only groups of 3)
    if re.fullmatch(r'-?\d{1,3}(?: \d{3})+(?:[.,]\d+)?', s):
        s = s.replace(' ', '')
    s = s.replace(',', '.')
    if re.fullmatch(r'-?\d+\.', s):          # "3." → "3"
        s = s[:-1]
    if re.fullmatch(r'-?\d+(?:\.\d+)?', s) or re.fullmatch(r'-?\.\d+', s):
        try:
            return Fraction(s)
        except (ValueError, ZeroDivisionError):
            return None
    return None


def parse_duration(s):
    """'1 h 30 min' / '1h30' / '1:30' / '90 min' / '2 h' → minutes (int), or None."""
    s = _clean(s).lower()
    if not s:
        return None
    m = _DURATION_RE.match(s)
    if not m or (m.group(1) is None and m.group(2) is None):
        return None
    hours = int(m.group(1) or 0)
    mins = int(m.group(2) or 0)
    # "2 h" alone → 120; "45" alone (no unit) → treat as minutes
    return hours * 60 + mins


def parse_coordinate(s):
    s = _clean(s)
    m = _COORD_RE.match(s)
    if not m:
        return None
    x, y = parse_number(m.group(1)), parse_number(m.group(2))
    if x is None or y is None:
        return None
    return (x, y)


def normalize_text(s) -> str:
    """Case-, accent- and punctuation-insensitive form for word answers."""
    s = _clean(s).casefold()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r'[\s\.\!\?\;\:]+$', '', s)          # trailing punctuation
    s = re.sub(r"[’']", "'", s)
    return re.sub(r'\s+', ' ', s).strip()


# ── inference for problems that don't declare a type ────────────────────────

def infer_answer_type(correct_answers) -> str:
    """
    Guess the answer type from the accepted answers of a legacy generator.
    Explicit ``answer_type`` on a problem always wins over this.
    """
    answers = [_clean(a) for a in (correct_answers or []) if _clean(a)]
    if not answers:
        return 'text'
    if all(a in _SYMBOLS for a in answers):
        return 'symbol'
    if any(_COORD_RE.match(a) and '(' in a for a in answers):
        return 'coordinate'
    if any(re.search(r'\d\s*(h|min)\b', a, re.IGNORECASE) for a in answers):
        return 'duration'
    if any(ch in a for a in answers for ch in _CURRENCY):
        return 'money'
    parsed = [parse_number(a) for a in answers]
    if all(p is not None for p in parsed):
        if any('/' in a for a in answers):
            return 'fraction'
        if all(p.denominator == 1 for p in parsed) and not any(re.search(r'[.,]\d', a) for a in answers):
            return 'integer'
        return 'decimal'
    return 'text'


# ── the check ────────────────────────────────────────────────────────────────

def check_answer(submitted, correct_answers, answer_type=None) -> bool:
    """
    True if ``submitted`` matches any of ``correct_answers`` under ``answer_type``.
    Falls back to a tolerant text comparison whenever typed parsing fails, so a
    mistyped type can never make a correct answer fail.
    """
    correct_answers = [c for c in (correct_answers or []) if _clean(c)]
    if not correct_answers:
        return False
    answer_type = answer_type or infer_answer_type(correct_answers)
    sub_clean = _clean(submitted)
    if not sub_clean:
        return False

    if answer_type in NUMERIC_TYPES:
        sub = parse_number(sub_clean)
        if sub is not None:
            for c in correct_answers:
                if parse_number(c) == sub:
                    return True

    elif answer_type == 'duration':
        sub = parse_duration(sub_clean)
        if sub is not None:
            for c in correct_answers:
                if parse_duration(c) == sub:
                    return True

    elif answer_type == 'coordinate':
        sub = parse_coordinate(sub_clean)
        if sub is not None:
            for c in correct_answers:
                if parse_coordinate(c) == sub:
                    return True

    elif answer_type == 'symbol':
        s = sub_clean.replace(' ', '')
        s = {'=<': '≤', '<=': '≤', '=>': '≥', '>=': '≥', '==': '='}.get(s, s)
        for c in correct_answers:
            if _clean(c).replace(' ', '') == s:
                return True

    # Universal fallback: tolerant text equality, then numeric equality.
    norm = normalize_text(sub_clean)
    for c in correct_answers:
        if normalize_text(c) == norm:
            return True
    sub_num = parse_number(sub_clean)
    if sub_num is not None and answer_type not in ('duration', 'coordinate'):
        for c in correct_answers:
            if parse_number(c) == sub_num:
                return True
    return False


# ── front-end input spec ─────────────────────────────────────────────────────

def input_spec(answer_type, lang='en') -> dict:
    """
    What the text input should look like for this answer type.  Keys:
    ``inputmode`` (mobile keyboard), ``placeholder``, ``pattern`` (soft, client
    side only), ``hint`` (short format reminder shown under the field).
    """
    fr = lang == 'fr'
    specs = {
        'integer':    dict(inputmode='numeric', pattern=r'[-0-9 ]*',
                           placeholder='12',
                           hint='Un nombre entier' if fr else 'A whole number'),
        'decimal':    dict(inputmode='decimal', pattern=r'[-0-9 .,]*',
                           placeholder='3,5' if fr else '3.5',
                           hint='Utilise la virgule pour les décimales' if fr else 'Use a dot or comma for decimals'),
        'money':      dict(inputmode='decimal', pattern=r'[-0-9 .,$€]*',
                           placeholder='4,50' if fr else '4.50',
                           hint='Montant en dollars, ex. 4,50' if fr else 'Amount in dollars, e.g. 4.50'),
        'fraction':   dict(inputmode='text', pattern=r'[-0-9 /.,]*',
                           placeholder='3/4',
                           hint='Écris la fraction avec /, ex. 3/4' if fr else 'Write the fraction with /, e.g. 3/4'),
        'duration':   dict(inputmode='text', pattern=r'[0-9 hminHMIN:]*',
                           placeholder='1 h 30 min',
                           hint='Ex. 1 h 30 min ou 90 min' if fr else 'e.g. 1 h 30 min or 90 min'),
        'coordinate': dict(inputmode='text', pattern=r'[-0-9 (),;]*',
                           placeholder='(3, 4)',
                           hint='Écris x, y — ex. (3, 4)' if fr else 'Write x, y — e.g. (3, 4)'),
        'symbol':     dict(inputmode='text', pattern=r'[<>=≤≥ ]*',
                           placeholder='<  >  =',
                           hint='Tape <, > ou =' if fr else 'Type <, > or ='),
        'text':       dict(inputmode='text', pattern='',
                           placeholder='Ta réponse…' if fr else 'Your answer…',
                           hint=''),
    }
    return dict(specs.get(answer_type) or specs['text'], answer_type=answer_type or 'text')
