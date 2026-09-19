"""
g4_numeration.py — Grade-4 numeration generators (content_g4.md §1–2).

Topics:
  g4_roman_to_arabic_gen   typed (integer) – read a Roman numeral
  g4_arabic_to_roman_gen   typed (text)    – write a number in Roman numerals
  g4_roman_match_gen       mix_match       – pair Roman ↔ Arabic numerals
  g4_digit_position_gen    QCM             – which position does a digit occupy?
  g4_digit_value_gen       typed (integer) – value of a digit in a 4–5 digit number
  g4_expanded_form_gen     QCM             – multiplicative expanded notation
  g4_count_groups_gen      typed (integer) – "combien de centaines dans 33 264 ?"
  g4_grouping_problem_gen  typed (integer) – scenario: N jars of 100 + M jars of 10 …

Difficulty:
  easy   → I, V, X (1–39)          / 4-digit numbers
  medium → + L, C (1–399)          / 5-digit numbers
  hard   → + D, M (1–3999)         / 5-digit numbers with zeros, "chiffre" vs "nombre"
"""
import random
from .base import _tagged_shuffle_mc
from . import scenarios as sc

# ─────────────────────────────────────────────────────────────────────────────
# Roman numeral helpers
# ─────────────────────────────────────────────────────────────────────────────

_ROMAN = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'),
]
_ROMAN_VAL = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}


def to_roman(n):
    """Integer 1–3999 → canonical Roman numeral."""
    out = []
    for val, sym in _ROMAN:
        while n >= val:
            out.append(sym)
            n -= val
    return ''.join(out)


def from_roman(s):
    """Roman numeral → integer (assumes well-formed input)."""
    total, prev = 0, 0
    for ch in reversed(s.upper()):
        v = _ROMAN_VAL[ch]
        if v < prev:
            total -= v
        else:
            total += v
            prev = v
    return total


def _roman_terms(s):
    """'XXVII' → ['10', '10', '5', '1', '1'];  'CMXC' → ['(1000 − 100)', '(100 − 10)']."""
    terms, i = [], 0
    s = s.upper()
    while i < len(s):
        v = _ROMAN_VAL[s[i]]
        if i + 1 < len(s) and _ROMAN_VAL[s[i + 1]] > v:
            terms.append(f'({_ROMAN_VAL[s[i + 1]]} − {v})')
            i += 2
        else:
            terms.append(str(v))
            i += 1
    return terms


def _expanded_terms(n):
    """555 → ['500', '50', '5'] (non-zero place values, high to low)."""
    parts, place = [], 1
    while n:
        n, d = divmod(n, 10)
        if d:
            parts.append(d * place)
        place *= 10
    return [str(p) for p in reversed(parts)]


def _roman_pool(level):
    if level == 'easy':
        return random.randint(1, 39)
    if level == 'medium':
        return random.randint(40, 399)
    # hard: favour numbers that use D / M and a subtractive pair
    return random.choice([random.randint(400, 3999), random.randint(900, 1999)])


def _roman_distractors(n):
    """Plausible wrong readings/writings of n as (arabic, roman) pairs."""
    cands = set()
    r = to_roman(n)
    # Reading subtractive pairs additively: IX → 11, XC → 110, CM → 1100
    add_read = sum(_ROMAN_VAL[c] for c in r)
    if add_read != n:
        cands.add(add_read)
    for d in (n + 1, n - 1, n + 10, n - 10, n + 5, n - 5, n + 100, n - 100, n + 1000):
        if 1 <= d <= 3999:
            cands.add(d)
    cands.discard(n)
    lst = list(cands)
    random.shuffle(lst)
    return lst


# ─────────────────────────────────────────────────────────────────────────────
# g4_roman_to_arabic_gen
# ─────────────────────────────────────────────────────────────────────────────

_ROMAN_CONTEXTS = [
    # (fr, en) — where a kid meets Roman numerals; {r} = the numeral
    ("Sur la façade d'un vieux bâtiment, on lit l'année **{r}**.",
     "On the front of an old building you can read the year **{r}**."),
    ("Le chapitre **{r}** d'un livre.",
     "Chapter **{r}** of a book."),
    ("Une horloge indique **{r}**.",
     "A clock face shows **{r}**."),
    ("Le roi Louis **{r}**.",
     "King Louis **{r}**."),
    ("La **{r}**e édition des Jeux olympiques.",
     "The **{r}**th edition of the Olympic Games."),
    ("Le film s'appelle « Rocky **{r}** ».",
     "The movie is called “Rocky **{r}**”."),
]


def g4_roman_to_arabic_gen(level='easy'):
    n = _roman_pool(level)
    r = to_roman(n)
    terms = _roman_terms(r)
    use_ctx = random.random() < 0.5
    if use_ctx and 1 <= n <= 30:
        ctx_fr, ctx_en = random.choice(_ROMAN_CONTEXTS)
        prompt_fr = ctx_fr.format(r=r) + " Quel nombre est écrit en chiffres romains ?"
        prompt_en = ctx_en.format(r=r) + " Which number is written in Roman numerals?"
    else:
        prompt_fr = f"Écris en chiffres arabes le nombre romain **{r}**."
        prompt_en = f"Write the Roman numeral **{r}** using Arabic digits."

    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000. '
                            'Un petit symbole placé AVANT un plus grand se soustrait (IV = 4).',
        'hint_en':          'I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000. '
                            'A smaller symbol BEFORE a bigger one is subtracted (IV = 4).',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Give each symbol its value; a smaller symbol before a bigger one is subtracted.\n'
            f'Step 2: {r} = {" + ".join(terms)}\n'
            f'Answer: {sc.fmt_n(n)}'
        ),
        'explanation_fr': (
            f'Étape 1 : Donne sa valeur à chaque symbole ; un petit symbole placé avant un plus grand se soustrait.\n'
            f'Étape 2 : {r} = {" + ".join(terms)}\n'
            f'Réponse : {sc.fmt_n(n)}'
        ),
        'correct_answers':  [str(n)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_arabic_to_roman_gen
# ─────────────────────────────────────────────────────────────────────────────

def g4_arabic_to_roman_gen(level='easy'):
    n = _roman_pool(level)
    r = to_roman(n)
    exp = _expanded_terms(n)
    exp_roman = [to_roman(int(t)) for t in exp]

    return {
        'q_type':           'text_input',
        'answer_type':      'text',
        'prompt_fr':        f"Écris le nombre **{sc.fmt_n(n)}** en chiffres romains.",
        'prompt_en':        f"Write the number **{sc.fmt_n(n)}** in Roman numerals.",
        'hint_fr':          f"Décompose d'abord : {sc.fmt_n(n)} = {' + '.join(exp)}. "
                            'Puis écris chaque partie en symboles romains.',
        'hint_en':          f"Expand first: {sc.fmt_n(n)} = {' + '.join(exp)}. "
                            'Then write each part with Roman symbols.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Expanded form: {sc.fmt_n(n)} = {" + ".join(exp)}\n'
            f'Step 2: Each part in Roman symbols: {" + ".join(exp_roman)}\n'
            f'Answer: {r}'
        ),
        'explanation_fr': (
            f'Étape 1 : Forme développée : {sc.fmt_n(n)} = {" + ".join(exp)}\n'
            f'Étape 2 : Chaque partie en symboles romains : {" + ".join(exp_roman)}\n'
            f'Réponse : {r}'
        ),
        'correct_answers':  [r],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_roman_match_gen
# ─────────────────────────────────────────────────────────────────────────────

def g4_roman_match_gen(level='easy'):
    count = 3 if level == 'easy' else 4
    nums = set()
    while len(nums) < count:
        nums.add(_roman_pool(level))
    nums = sorted(nums)
    random.shuffle(nums)
    pairs = [{'left': to_roman(n), 'right': sc.fmt_n(n)} for n in nums]
    return {
        'q_type':           'mix_match',
        'prompt_fr':        'Associe chaque nombre romain à sa valeur.',
        'prompt_en':        'Match each Roman numeral to its value.',
        'hint_fr':          'Additionne les symboles de gauche à droite ; soustrais un petit symbole placé avant un plus grand.',
        'hint_en':          'Add the symbols left to right; subtract a smaller symbol placed before a bigger one.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            pairs,
        'explanation_en':   '\n'.join(f'{to_roman(n)} = {" + ".join(_roman_terms(to_roman(n)))} = {sc.fmt_n(n)}' for n in sorted(nums)),
        'explanation_fr':   '\n'.join(f'{to_roman(n)} = {" + ".join(_roman_terms(to_roman(n)))} = {sc.fmt_n(n)}' for n in sorted(nums)),
        'correct_answers':  [p['right'] for p in pairs],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Place value helpers
# ─────────────────────────────────────────────────────────────────────────────

_POS_FR = ['unités', 'dizaines', 'centaines', 'unités de mille', 'dizaines de mille', 'centaines de mille']
_POS_EN = ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'hundred thousands']


def _pick_number(level, unique_digits=True):
    """A 4-digit (easy) or 5-digit (medium/hard) number; hard has a zero inside."""
    while True:
        if level == 'easy':
            n = random.randint(1000, 9999)
        elif level == 'medium':
            n = random.randint(10_000, 99_999)
        else:
            digits = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(4)]
            digits[random.randint(1, 3)] = 0
            n = int(''.join(map(str, digits)))
        s = str(n)
        if not unique_digits or len(set(s)) == len(s):
            return n


def _pick_position(n, pos_idx=None):
    """Return (index, digit) for a digit position (0 = ones) of n; skips zero digits."""
    s = str(n)[::-1]
    choices = [i for i, d in enumerate(s) if d != '0']
    if pos_idx is not None and pos_idx in choices:
        i = pos_idx
    else:
        i = random.choice(choices)
    return i, int(s[i])


# ─────────────────────────────────────────────────────────────────────────────
# g4_digit_position_gen
# ─────────────────────────────────────────────────────────────────────────────

def g4_digit_position_gen(level='easy'):
    n = _pick_number(level, unique_digits=True)
    i, d = _pick_position(n)
    k = len(str(n))
    correct = _POS_FR[i]
    tagged = [
        (_POS_FR[j], 'wrong_position',
         'Count positions from the right: ones, tens, hundreds, thousands, ten thousands.',
         'Compte les positions à partir de la droite : unités, dizaines, centaines, unités de mille, dizaines de mille.')
        for j in range(k) if j != i
    ]
    if len(tagged) < 4:
        tagged.append((_POS_FR[k], 'wrong_position', 'That position is beyond this number.', 'Cette position dépasse ce nombre.'))
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        f"Dans le nombre **{sc.fmt_n(n)}**, quelle position occupe le chiffre **{d}** ?",
        'prompt_en':        f"In the number **{sc.fmt_n(n)}**, which position does the digit **{d}** occupy?",
        'hint_fr':          'Lis les positions de droite à gauche : unités, dizaines, centaines, unités de mille, dizaines de mille.',
        'hint_en':          'Read the positions from right to left: ones, tens, hundreds, thousands, ten thousands.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(correct, tagged),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Starting from the right, the positions are: {", ".join(_POS_EN[:k])}.\n'
            f'Step 2: The digit {d} is the {i + 1}{"st" if i == 0 else "nd" if i == 1 else "rd" if i == 2 else "th"} digit from the right.\n'
            f'Answer: {_POS_EN[i]} ({correct})'
        ),
        'explanation_fr': (
            f'Étape 1 : En partant de la droite, les positions sont : {", ".join(_POS_FR[:k])}.\n'
            f'Étape 2 : Le chiffre {d} est le {i + 1}{"er" if i == 0 else "e"} chiffre à partir de la droite.\n'
            f'Réponse : {correct}'
        ),
        'correct_answers':  [correct, _POS_EN[i]],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_digit_value_gen
# ─────────────────────────────────────────────────────────────────────────────

def g4_digit_value_gen(level='easy'):
    n = _pick_number(level, unique_digits=True)
    i, d = _pick_position(n)
    value = d * 10 ** i
    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        f"Dans le nombre **{sc.fmt_n(n)}**, quelle est la valeur du chiffre **{d}** ?",
        'prompt_en':        f"In the number **{sc.fmt_n(n)}**, what is the value of the digit **{d}**?",
        'hint_fr':          f"Le chiffre {d} est à la position des {_POS_FR[i]}.",
        'hint_en':          f"The digit {d} is in the {_POS_EN[i]} position.",
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: The digit {d} is in the {_POS_EN[i]} position.\n'
            f'Step 2: Its value is {d} × {sc.fmt_n(10 ** i)} = {sc.fmt_n(value)}.\n'
            f'Answer: {sc.fmt_n(value)}'
        ),
        'explanation_fr': (
            f'Étape 1 : Le chiffre {d} est à la position des {_POS_FR[i]}.\n'
            f'Étape 2 : Sa valeur est {d} × {sc.fmt_n(10 ** i)} = {sc.fmt_n(value)}.\n'
            f'Réponse : {sc.fmt_n(value)}'
        ),
        'correct_answers':  [str(value)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_expanded_form_gen
# ─────────────────────────────────────────────────────────────────────────────

def _mult_expansion(n):
    """87156 → '(8 × 10 000) + (7 × 1 000) + (1 × 100) + (5 × 10) + (6 × 1)' (zero digits skipped)."""
    parts = []
    s = str(n)
    k = len(s)
    for idx, ch in enumerate(s):
        d = int(ch)
        if d == 0:
            continue
        place = 10 ** (k - 1 - idx)
        parts.append(f'({d} × {sc.fmt_n(place)})')
    return ' + '.join(parts)


def _wrong_expansions(n):
    """Misconception-tagged wrong multiplicative decompositions of n."""
    s = str(n)
    k = len(s)
    out = []
    # 1. every multiplier shifted one place down (8 × 1 000 instead of 8 × 10 000)
    parts = [f'({int(ch)} × {sc.fmt_n(10 ** (k - 2 - idx))})' for idx, ch in enumerate(s) if ch != '0' and k - 2 - idx >= 0]
    out.append((' + '.join(parts), 'place_shift',
                'Each digit was matched to the place value one step too small.',
                'Chaque chiffre a été associé à une position trop petite.'))
    # 2. two digits swapped
    digs = [int(c) for c in s]
    i, j = random.sample(range(k), 2)
    digs[i], digs[j] = digs[j], digs[i]
    swapped = int(''.join(map(str, digs)))
    if swapped != n:
        out.append((_mult_expansion(swapped), 'digits_swapped',
                    'Two digits are in the wrong order.', 'Deux chiffres ont été inversés.'))
    # 3. a term missing
    plist = _mult_expansion(n).split(' + ')
    if len(plist) > 2:
        drop = random.randrange(len(plist))
        out.append((' + '.join(p for q, p in enumerate(plist) if q != drop), 'missing_term',
                    'One place value is missing.', 'Une position a été oubliée.'))
    # 4. digits used as raw values (8 + 7 + 1 + 5 + 6 style) — mimic "digit × wrong place"
    alt = [f'({int(ch)} × {sc.fmt_n(10 ** idx)})' for idx, ch in enumerate(s) if ch != '0']
    out.append((' + '.join(alt), 'reversed_places',
                'The place values are reversed (ones on the left).',
                'Les positions sont inversées (unités à gauche).'))
    return out


def g4_expanded_form_gen(level='easy'):
    n = _pick_number(level, unique_digits=False)
    if random.random() < 0.5:
        # Number → decomposition
        correct = _mult_expansion(n)
        tagged = [t for t in _wrong_expansions(n) if t[0] and t[0] != correct]
        prompt_fr = f"Quelle est la décomposition du nombre **{sc.fmt_n(n)}** ?"
        prompt_en = f"Which is the expanded form of **{sc.fmt_n(n)}**?"
        answers = [correct]
    else:
        # Decomposition → number
        correct = sc.fmt_n(n)
        s = str(n)
        k = len(s)
        cands = set()
        digs = [int(c) for c in s]
        for _ in range(6):
            d2 = digs[:]
            i, j = random.sample(range(k), 2)
            d2[i], d2[j] = d2[j], d2[i]
            v = int(''.join(map(str, d2)))
            if v != n and len(str(v)) == k:
                cands.add(v)
        cands.add(n // 10)
        cands.add(n + 10 ** (k - 2))
        tagged = [(sc.fmt_n(c), 'wrong_recompose',
                   'Add the value of every term carefully.',
                   'Additionne soigneusement la valeur de chaque terme.') for c in cands if c != n]
        prompt_fr = f"Quel nombre est décomposé ainsi : **{_mult_expansion(n)}** ?"
        prompt_en = f"Which number has this expanded form: **{_mult_expansion(n)}**?"
        answers = [str(n)]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Chaque chiffre est multiplié par la valeur de sa position : unités × 1, dizaines × 10, centaines × 100…',
        'hint_en':          'Each digit is multiplied by its place value: ones × 1, tens × 10, hundreds × 100…',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(correct, tagged),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Write each non-zero digit of {sc.fmt_n(n)} with its place value.\n'
            f'Step 2: {sc.fmt_n(n)} = {_mult_expansion(n)}\n'
            f'Answer: {correct}'
        ),
        'explanation_fr': (
            f'Étape 1 : Écris chaque chiffre non nul de {sc.fmt_n(n)} avec la valeur de sa position.\n'
            f'Étape 2 : {sc.fmt_n(n)} = {_mult_expansion(n)}\n'
            f'Réponse : {correct}'
        ),
        'correct_answers':  answers,
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_count_groups_gen — "Combien y a-t-il de centaines dans 33 264 ?" → 332
# ─────────────────────────────────────────────────────────────────────────────

_GROUP_FR = {1: 'dizaines', 2: 'centaines', 3: 'unités de mille', 4: 'dizaines de mille'}
_GROUP_EN = {1: 'tens', 2: 'hundreds', 3: 'thousands', 4: 'ten thousands'}


def g4_count_groups_gen(level='easy'):
    n = _pick_number(level, unique_digits=False)
    k = len(str(n))
    if level == 'easy':
        i = random.choice([1, 2])
    elif level == 'medium':
        i = random.choice([1, 2, 3])
    else:
        i = random.choice([1, 2, 3, 4])
    i = min(i, k - 1)
    ask_digit = level == 'hard' and random.random() < 0.4

    if ask_digit:
        # "chiffre des centaines" → single digit
        digit = (n // 10 ** i) % 10
        prompt_fr = f"Dans **{sc.fmt_n(n)}**, quel est le **chiffre** des {_GROUP_FR[i]} ?"
        prompt_en = f"In **{sc.fmt_n(n)}**, what is the **{_GROUP_EN[i]} digit**?"
        answer = digit
        expl_en = (f'Step 1: "The {_GROUP_EN[i]} digit" means ONE digit: the one in the {_GROUP_EN[i]} position.\n'
                   f'Step 2: Counting from the right, that digit is {digit}.\n'
                   f'Answer: {digit}')
        expl_fr = (f'Étape 1 : « Le chiffre des {_GROUP_FR[i]} » désigne UN seul chiffre : celui à la position des {_GROUP_FR[i]}.\n'
                   f'Étape 2 : En comptant depuis la droite, ce chiffre est {digit}.\n'
                   f'Réponse : {digit}')
        hint_fr = 'Le « chiffre » est un seul symbole ; le « nombre de » compte tous les groupes.'
        hint_en = 'The "digit" is a single symbol; the "number of" counts all the groups.'
    else:
        answer = n // 10 ** i
        prompt_fr = f"Combien y a-t-il de **{_GROUP_FR[i]}** dans **{sc.fmt_n(n)}** ?"
        prompt_en = f"How many **{_GROUP_EN[i]}** are there in **{sc.fmt_n(n)}**?"
        expl_en = (f'Step 1: "How many {_GROUP_EN[i]}" means: count ALL the groups of {sc.fmt_n(10 ** i)} in {sc.fmt_n(n)}.\n'
                   f'Step 2: Cover the {i} digit(s) to the right of the {_GROUP_EN[i]} position: what remains is {sc.fmt_n(answer)}.\n'
                   f'Check: {sc.fmt_n(answer)} × {sc.fmt_n(10 ** i)} = {sc.fmt_n(answer * 10 ** i)} and {sc.fmt_n(n)} − {sc.fmt_n(answer * 10 ** i)} = {n - answer * 10 ** i}.\n'
                   f'Answer: {sc.fmt_n(answer)}')
        expl_fr = (f'Étape 1 : « Combien de {_GROUP_FR[i]} » veut dire : compte TOUS les groupes de {sc.fmt_n(10 ** i)} dans {sc.fmt_n(n)}.\n'
                   f'Étape 2 : Cache le(s) {i} chiffre(s) à droite de la position des {_GROUP_FR[i]} : il reste {sc.fmt_n(answer)}.\n'
                   f'Vérification : {sc.fmt_n(answer)} × {sc.fmt_n(10 ** i)} = {sc.fmt_n(answer * 10 ** i)} et {sc.fmt_n(n)} − {sc.fmt_n(answer * 10 ** i)} = {n - answer * 10 ** i}.\n'
                   f'Réponse : {sc.fmt_n(answer)}')
        hint_fr = f'Attention : on demande le NOMBRE de {_GROUP_FR[i]}, pas seulement le chiffre. Cache les chiffres à droite de cette position.'
        hint_en = f'Careful: it asks for the NUMBER of {_GROUP_EN[i]}, not just the digit. Cover the digits to the right of that position.'

    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          hint_fr,
        'hint_en':          hint_en,
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en':   expl_en,
        'explanation_fr':   expl_fr,
        'correct_answers':  [str(answer)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_grouping_problem_gen — scenario: "3 pots de 100 vis et 7 pots de 10 vis"
# ─────────────────────────────────────────────────────────────────────────────

def g4_grouping_problem_gen(level='easy'):
    # Groups of 1 000 only make sense for small objects (screws, beads…), not animals.
    key, thing = sc.pick_thing(None if level != 'hard' else 'object')
    cat = thing[5]
    cont = sc.pick_container(cat)
    verb_fr, verb_en, _ = sc.pick_verb(cat)
    if random.random() < 0.6:
        who_fr, gender = sc.pick_actor()
        who_en = who_fr
    else:
        who_fr, who_en, gender = sc.pick_role()
        who_fr = who_fr[0].upper() + who_fr[1:]
        who_en = who_en[0].upper() + who_en[1:]

    # groups: list of (count_of_containers, size_per_container)
    if level == 'easy':
        groups = [(random.randint(1, 9), 100), (random.randint(1, 9), 10)]
        loose = 0
    elif level == 'medium':
        groups = [(random.randint(1, 9), 100), (random.randint(1, 9), 10)]
        loose = random.randint(1, 9)
    else:
        groups = [(random.randint(1, 9), 1000), (random.randint(1, 12), 100), (random.randint(1, 15), 10)]
        loose = random.randint(0, 9)
    random.shuffle(groups)
    total = sum(c * s for c, s in groups) + loose

    def phrase(lang):
        parts = []
        for c, s in groups:
            if lang == 'fr':
                parts.append(f"**{c}** {sc.cont(cont, c, 'fr')} de **{sc.fmt_n(s)}** {sc.noun(thing, s, 'fr')}")
            else:
                parts.append(f"**{c}** {sc.cont(cont, c, 'en')} of **{sc.fmt_n(s)}** {sc.noun(thing, s, 'en')}")
        if loose:
            parts.append(f"**{loose}** {sc.noun(thing, loose, lang)}" +
                         (' en vrac' if lang == 'fr' else ' loose'))
        if lang == 'fr':
            return ', '.join(parts[:-1]) + ' et ' + parts[-1] if len(parts) > 1 else parts[0]
        return ', '.join(parts[:-1]) + ' and ' + parts[-1] if len(parts) > 1 else parts[0]

    prompt_fr = (f"{who_fr} {verb_fr} {phrase('fr')}. "
                 f"Combien de {sc.noun(thing, 2, 'fr')} cela fait-il en tout ?")
    prompt_en = (f"{who_en} {verb_en} {phrase('en')}. "
                 f"How many {sc.noun(thing, 2, 'en')} is that in total?")

    steps = ' + '.join(f'({c} × {sc.fmt_n(s)})' for c, s in groups) + (f' + {loose}' if loose else '')
    values = ' + '.join(sc.fmt_n(c * s) for c, s in groups) + (f' + {loose}' if loose else '')

    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Calcule chaque groupe séparément (nombre de contenants × quantité par contenant), puis additionne tout.',
        'hint_en':          'Work out each group separately (number of containers × amount per container), then add everything.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Each group = containers × amount per container: {steps}\n'
            f'Step 2: {values} = {sc.fmt_n(total)}\n'
            f'Answer: {sc.fmt_n(total)} {sc.noun(thing, total, "en")}'
        ),
        'explanation_fr': (
            f'Étape 1 : Chaque groupe = nombre de contenants × quantité par contenant : {steps}\n'
            f'Étape 2 : {values} = {sc.fmt_n(total)}\n'
            f'Réponse : {sc.fmt_n(total)} {sc.noun(thing, total, "fr")}'
        ),
        'correct_answers':  [str(total)],
    }
