"""
numeration.py — Grade-3 number-sense generators.

Topics (from content.md Thème 1, sections 1-3):
  read_number_gen         QCM     – read {n} in French words
  write_number_gen        typed   – write in digits from French words
  digit_position_gen      QCM     – which position holds digit d in n?
  digit_value_gen         typed   – what is the value of digit d in n?
  expanded_form_gen       typed   – compute a+b+c+d expanded form
  decomposition_match_gen mix_match – number ↔ decomposition string
  base10_match_gen        mix_match – number ↔ "X centaines Y dizaines Z unités"
  build_number_gen        ordering  – sort place-value tiles into ascending order
  order_numbers_gen       ordering  – order 4-5 numbers from smallest to largest

Difficulty governs the numeric range:
  easy   → 3-digit numbers (100-999)
  medium → 4-digit numbers, no internal zeros (1000-9999)
  hard   → 4-digit numbers, may include internal zeros
"""

import random
from .base import _tagged_shuffle_mc

# ─── French / English number words ────────────────────────────────────────────

_ONES_FR = [
    'zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept',
    'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze',
    'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf',
]
_TENS_FR = {
    2: 'vingt', 3: 'trente', 4: 'quarante',
    5: 'cinquante', 6: 'soixante',
}

_ONES_EN = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
    'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
    'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
]
_TENS_EN = [
    '', '', 'twenty', 'thirty', 'forty',
    'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
]


def _to_fr(n: int) -> str:
    """Integer 0-9 999 → French words."""
    if n < 20:
        return _ONES_FR[n]
    if n < 70:
        t, u = divmod(n, 10)
        tw = _TENS_FR[t]
        if u == 0:
            return tw
        if u == 1:
            return f'{tw} et un'
        return f'{tw}-{_ONES_FR[u]}'
    if n < 80:
        rem = n - 60  # 10-19
        if rem == 11:
            return 'soixante et onze'
        return f'soixante-{_ONES_FR[rem]}'
    if n < 100:
        rem = n - 80  # 0-19
        if rem == 0:
            return 'quatre-vingts'
        return f'quatre-vingt-{_ONES_FR[rem]}'
    if n < 200:
        rest = n - 100
        return 'cent' if rest == 0 else f'cent {_to_fr(rest)}'
    if n < 1000:
        c, rest = divmod(n, 100)
        c_word = _ONES_FR[c]
        if rest == 0:
            return f'{c_word} cents'
        return f'{c_word} cent {_to_fr(rest)}'
    if n < 2000:
        rest = n - 1000
        return 'mille' if rest == 0 else f'mille {_to_fr(rest)}'
    m, rest = divmod(n, 1000)
    m_word = _ONES_FR[m]
    return f'{m_word} mille' if rest == 0 else f'{m_word} mille {_to_fr(rest)}'


def _to_en(n: int) -> str:
    """Integer 0-9 999 → English words."""
    if n < 20:
        return _ONES_EN[n]
    if n < 100:
        t, u = divmod(n, 10)
        if u == 0:
            return _TENS_EN[t]
        return f'{_TENS_EN[t]}-{_ONES_EN[u]}'
    if n < 1000:
        c, rest = divmod(n, 100)
        s = f'{_ONES_EN[c]} hundred'
        if rest:
            s += f' {_to_en(rest)}'
        return s
    m, rest = divmod(n, 1000)
    s = f'{_to_en(m)} thousand'
    if rest:
        s += f' {_to_en(rest)}'
    return s


# ─── level ranges ──────────────────────────────────────────────────────────────

def _pick_n(level: str) -> int:
    """Random number appropriate to the difficulty level."""
    if level == 'easy':
        # 3-digit, avoid leading-zero confusion
        return random.randint(100, 999)
    elif level == 'medium':
        # 4-digit, tens digit ≠ 0 (no internal zeros)
        n = random.randint(1000, 9999)
        while (n // 10) % 10 == 0 or (n // 100) % 10 == 0:
            n = random.randint(1000, 9999)
        return n
    else:  # hard
        # 4-digit, may have internal zeros — tests place-value robustness
        return random.randint(1000, 9999)


# ─── 1. read_number_gen ────────────────────────────────────────────────────────

def read_number_gen(level: str = 'medium') -> dict:
    """
    QCM — given digits, choose the correct French reading.
    Distractors: permutations of place values.
    """
    n = _pick_n(level)
    correct_fr = _to_fr(n)
    correct_en = _to_en(n)

    # Build plausible distractors by tweaking place values
    def _distract_variants():
        variants = []
        c, d, u = (n // 100) % 10, (n // 10) % 10, n % 10
        th = n // 1000

        # Swap hundreds and tens
        if level in ('medium', 'hard') and th > 0:
            v = th * 1000 + d * 100 + c * 10 + u
        else:
            v = c * 100 + d + u * 10  # swap d and u
        if v != n and 100 <= v <= 9999:
            variants.append((v, 'inversion',
                             'Check the position of each digit.',
                             'Vérifie la position de chaque chiffre.'))

        # Off by one hundred
        v2 = n + 100
        if v2 <= 9999:
            variants.append((v2, 'place_value',
                             'Watch out for the hundreds.',
                             'Attention aux centaines.'))

        # Off by one thousand (for 4-digit numbers)
        if n >= 1000:
            v3 = n - 1000
            if v3 >= 100:
                variants.append((v3, 'place_value',
                                 'Did you forget the thousands?',
                                 'As-tu oublié les milliers ?'))

        # Replace units digit
        u_new = (u + 3) % 10
        v4 = n - u + u_new
        if v4 != n:
            variants.append((v4, 'digit_error',
                             'Reread the units digit.',
                             'Relis le chiffre des unités.'))

        return variants

    distractors = _distract_variants()
    # Build choices list manually (labels are words)
    seen = {correct_fr}
    pool = []
    for (dv, etype, fb_en, fb_fr) in distractors:
        lbl_fr = _to_fr(dv)
        if lbl_fr not in seen:
            seen.add(lbl_fr)
            pool.append({
                'label': lbl_fr,
                'correct': False,
                'error_type': etype,
                'feedback_en': fb_en,
                'feedback_fr': fb_fr,
            })
        if len(pool) == 4:
            break
    # Padding with nearby numbers if needed
    pad = 1
    while len(pool) < 4:
        v = n + pad * 11
        if v <= 9999:
            lbl = _to_fr(v)
            if lbl not in seen:
                seen.add(lbl)
                pool.append({'label': lbl, 'correct': False,
                             'error_type': 'distractor', 'feedback_en': '', 'feedback_fr': ''})
        pad += 1
    pos = random.randint(0, 4)
    pool.insert(pos, {'label': correct_fr, 'correct': True,
                      'error_type': '', 'feedback_en': '', 'feedback_fr': ''})
    choices = pool[:5]

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f'Comment lit-on le nombre **{n}** ?',
        'prompt_en': f'How do you read the number **{n}**?',
        'hint_fr': 'Lis chaque groupe : milliers, centaines, dizaines, unités.',
        'hint_en': 'Read each group: thousands, hundreds, tens, units.',
        'shape_data': [],
        'choices': choices,
        'correct_answers': [correct_fr],
        'time_limit': 30,
        'points': 1,
        'explanation_fr': (
            f'Le nombre {n} se lit : {correct_fr}.\n'
            f'Lis de gauche à droite : milliers → centaines → dizaines → unités.'
        ),
        'explanation_en': (
            f'The number {n} is read: {correct_en}.\n'
            f'Read left to right: thousands → hundreds → tens → units.'
        ),
    }


# ─── 2. write_number_gen ──────────────────────────────────────────────────────

def write_number_gen(level: str = 'medium') -> dict:
    """
    Typed — given French words, write the digits.
    """
    n = _pick_n(level)
    words_fr = _to_fr(n)
    words_en = _to_en(n)

    return {
        'q_type': 'text_input',
        'prompt_fr': f'Écris en chiffres : **{words_fr}**',
        'prompt_en': f'Write in digits: **{words_fr}**',
        'hint_fr': 'Identifie les milliers, centaines, dizaines et unités.',
        'hint_en': 'Identify the thousands, hundreds, tens, and units.',
        'shape_data': [],
        'choices': [],
        'correct_answers': [str(n)],
        'time_limit': 30,
        'points': 1,
        'explanation_fr': f'"{words_fr}" s\'écrit {n} en chiffres.',
        'explanation_en': f'"{words_en}" is written {n} in digits.',
    }


# ─── 3. digit_position_gen ────────────────────────────────────────────────────

_POSITIONS_FR = {0: 'unités', 1: 'dizaines', 2: 'centaines', 3: 'milliers'}
_POSITIONS_EN = {0: 'units', 1: 'tens', 2: 'hundreds', 3: 'thousands'}


def digit_position_gen(level: str = 'medium') -> dict:
    """
    QCM — given n and a digit d (non-zero, unique in n), identify its position.
    """
    # Ensure digit appears exactly once and is non-zero
    for _ in range(200):
        n = _pick_n(level)
        digits = [n % 10, (n // 10) % 10, (n // 100) % 10, (n // 1000) % 10]
        # Non-zero digits appearing exactly once
        candidates = [pos for pos in range(4) if digits[pos] != 0 and digits.count(digits[pos]) == 1]
        if candidates:
            pos_idx = random.choice(candidates)
            d = digits[pos_idx]
            break
    else:
        n, pos_idx, d = 312, 2, 3  # fallback

    correct_fr = _POSITIONS_FR[pos_idx]
    correct_en = _POSITIONS_EN[pos_idx]

    # Distractors: adjacent positions
    other_pos = [p for p in range(4) if p != pos_idx]
    random.shuffle(other_pos)
    distractors = [
        (_POSITIONS_FR[p], 'wrong_position',
         f"Count from the right: units=0, tens=1, hundreds=2, thousands=3.",
         f"Compte depuis la droite : unités=0, dizaines=1, centaines=2, milliers=3.")
        for p in other_pos[:3]
    ]
    # 4th distractor: "mille" confuse
    distractors.append(('dizaine de milliers', 'wrong_position',
                        'There are no ten-thousands here.', 'Il n\'y a pas de dizaine de milliers ici.'))

    seen = {correct_fr}
    pool = []
    for (lbl, etype, fb_en, fb_fr) in distractors:
        if lbl not in seen:
            seen.add(lbl)
            pool.append({'label': lbl, 'correct': False,
                         'error_type': etype, 'feedback_en': fb_en, 'feedback_fr': fb_fr})
        if len(pool) == 4:
            break

    insert_pos = random.randint(0, 4)
    pool.insert(insert_pos, {'label': correct_fr, 'correct': True,
                              'error_type': '', 'feedback_en': '', 'feedback_fr': ''})
    choices = pool[:5]

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f'Dans le nombre {n}, quelle est la position du chiffre {d} ?',
        'prompt_en': f'In the number {n}, what is the position of the digit {d}?',
        'hint_fr': 'Lis de droite à gauche : unités, dizaines, centaines, milliers.',
        'hint_en': 'Read right to left: units, tens, hundreds, thousands.',
        'shape_data': [],
        'choices': choices,
        'correct_answers': [correct_fr],
        'time_limit': 25,
        'points': 1,
        'explanation_fr': (
            f'Dans {n}, le chiffre {d} est en position des **{correct_fr}**.\n'
            f'Compte de droite à gauche : unités (pos 0), dizaines (pos 1), '
            f'centaines (pos 2), milliers (pos 3).'
        ),
        'explanation_en': (
            f'In {n}, the digit {d} is in the **{correct_en}** position.\n'
            f'Count from the right: units (pos 0), tens (pos 1), '
            f'hundreds (pos 2), thousands (pos 3).'
        ),
    }


# ─── 4. digit_value_gen ───────────────────────────────────────────────────────

def digit_value_gen(level: str = 'medium') -> dict:
    """
    Typed — given n and a digit d, find its place value (e.g. digit 3 in 312 → 300).
    """
    multipliers = [1, 10, 100, 1000]

    for _ in range(200):
        n = _pick_n(level)
        digits = [n % 10, (n // 10) % 10, (n // 100) % 10, (n // 1000) % 10]
        candidates = [pos for pos in range(4) if digits[pos] != 0 and digits.count(digits[pos]) == 1]
        if candidates:
            pos_idx = random.choice(candidates)
            d = digits[pos_idx]
            value = d * multipliers[pos_idx]
            break
    else:
        n, d, value = 312, 3, 300

    pos_fr = _POSITIONS_FR[pos_idx]
    pos_en = _POSITIONS_EN[pos_idx]

    return {
        'q_type': 'text_input',
        'prompt_fr': f'Dans le nombre **{n}**, quelle est la valeur du chiffre **{d}** ?',
        'prompt_en': f'In the number **{n}**, what is the value of the digit **{d}**?',
        'hint_fr': f'Le chiffre {d} est en position des {pos_fr}.',
        'hint_en': f'The digit {d} is in the {pos_en} position.',
        'shape_data': [],
        'choices': [],
        'correct_answers': [str(value)],
        'time_limit': 25,
        'points': 1,
        'explanation_fr': (
            f'Le chiffre {d} est en position des {pos_fr}.\n'
            f'Sa valeur = {d} × {multipliers[pos_idx]} = **{value}**.'
        ),
        'explanation_en': (
            f'The digit {d} is in the {pos_en} position.\n'
            f'Its value = {d} × {multipliers[pos_idx]} = **{value}**.'
        ),
    }


# ─── 5. expanded_form_gen ─────────────────────────────────────────────────────

def expanded_form_gen(level: str = 'medium') -> dict:
    """
    Typed — given an expanded form like 300 + 10 + 2, compute the number.
    """
    n = _pick_n(level)

    # Build expanded form parts (skip zero positions)
    parts = []
    if n >= 1000:
        parts.append(f'{(n // 1000) * 1000}')
    if (n // 100) % 10:
        parts.append(f'{((n // 100) % 10) * 100}')
    if (n // 10) % 10:
        parts.append(f'{((n // 10) % 10) * 10}')
    if n % 10:
        parts.append(f'{n % 10}')
    if not parts:
        parts = ['0']

    expanded = ' + '.join(parts)

    return {
        'q_type': 'text_input',
        'prompt_fr': f'Calcule : **{expanded}**',
        'prompt_en': f'Calculate: **{expanded}**',
        'hint_fr': 'Additionne les milliers, centaines, dizaines et unités séparément.',
        'hint_en': 'Add the thousands, hundreds, tens and units separately.',
        'shape_data': [],
        'choices': [],
        'correct_answers': [str(n)],
        'time_limit': 25,
        'points': 1,
        'explanation_fr': f'{expanded} = **{n}**',
        'explanation_en': f'{expanded} = **{n}**',
    }


# ─── 6. decomposition_match_gen ───────────────────────────────────────────────

def decomposition_match_gen(level: str = 'medium') -> dict:
    """
    Mix & match — match each number to its expanded decomposition.
    3-4 pairs to avoid cognitive overload.
    """
    count = 3 if level == 'easy' else 4

    numbers = []
    seen = set()
    while len(numbers) < count:
        n = _pick_n(level)
        if n not in seen:
            seen.add(n)
            numbers.append(n)

    def _expand(n):
        parts = []
        if n >= 1000:
            parts.append(f'{(n // 1000) * 1000}')
        if (n // 100) % 10:
            parts.append(f'{((n // 100) % 10) * 100}')
        if (n // 10) % 10:
            parts.append(f'{((n // 10) % 10) * 10}')
        if n % 10:
            parts.append(f'{n % 10}')
        return ' + '.join(parts) if parts else '0'

    pairs = [{'left': str(n), 'right': _expand(n)} for n in numbers]

    return {
        'q_type': 'mix_match',
        'prompt_fr': 'Relie chaque nombre à sa décomposition.',
        'prompt_en': 'Match each number to its decomposition.',
        'hint_fr': 'Décompose chaque nombre en milliers, centaines, dizaines et unités.',
        'hint_en': 'Break each number into thousands, hundreds, tens and units.',
        'shape_data': [],
        'choices': [],
        'pairs': pairs,
        'correct_answers': [p['right'] for p in pairs],
        'time_limit': 45,
        'points': count,
        'explanation_fr': '\n'.join(f'{p["left"]} = {p["right"]}' for p in pairs),
        'explanation_en': '\n'.join(f'{p["left"]} = {p["right"]}' for p in pairs),
    }


# ─── 7. base10_match_gen ──────────────────────────────────────────────────────

def base10_match_gen(level: str = 'medium') -> dict:
    """
    Mix & match — match each number to its centaines/dizaines/unités description.
    3-4 pairs.
    """
    count = 3 if level == 'easy' else 4

    numbers = []
    seen = set()
    while len(numbers) < count:
        n = _pick_n(level)
        if n not in seen:
            seen.add(n)
            numbers.append(n)

    def _base10_fr(n):
        th = n // 1000
        c = (n // 100) % 10
        d = (n // 10) % 10
        u = n % 10
        parts = []
        if th:
            parts.append(f'{th} millier{"s" if th > 1 else ""}')
        if c:
            parts.append(f'{c} centaine{"s" if c > 1 else ""}')
        if d:
            parts.append(f'{d} dizaine{"s" if d > 1 else ""}')
        if u:
            parts.append(f'{u} unité{"s" if u > 1 else ""}')
        return ' '.join(parts) if parts else '0 unité'

    pairs = [{'left': str(n), 'right': _base10_fr(n)} for n in numbers]

    return {
        'q_type': 'mix_match',
        'prompt_fr': 'Associe chaque nombre à sa représentation en base 10.',
        'prompt_en': 'Match each number to its base-10 representation.',
        'hint_fr': 'Compte les milliers, centaines, dizaines et unités de chaque nombre.',
        'hint_en': 'Count the thousands, hundreds, tens and units of each number.',
        'shape_data': [],
        'choices': [],
        'pairs': pairs,
        'correct_answers': [p['right'] for p in pairs],
        'time_limit': 45,
        'points': count,
        'explanation_fr': '\n'.join(f'{p["left"]} → {p["right"]}' for p in pairs),
        'explanation_en': '\n'.join(f'{p["left"]} → {p["right"]}' for p in pairs),
    }


# ─── 8. build_number_gen (ordering q_type) ────────────────────────────────────

def build_number_gen(level: str = 'medium') -> dict:
    """
    Ordering — given shuffled place-value tiles, arrange them to build the number.
    The "tiles" are the positional values (e.g. 300, 10, 2).
    Student drags tiles into ascending order of value.
    """
    n = _pick_n(level)

    tiles = []
    if n >= 1000 and (n // 1000) > 0:
        tiles.append((n // 1000) * 1000)
    if (n // 100) % 10:
        tiles.append(((n // 100) % 10) * 100)
    if (n // 10) % 10:
        tiles.append(((n // 10) % 10) * 10)
    if n % 10:
        tiles.append(n % 10)

    # Add one distractor tile
    distractor = tiles[0] + random.choice([100, 10, 1])
    while distractor in tiles:
        distractor += 10
    tiles_with_extra = tiles + [distractor]
    random.shuffle(tiles_with_extra)

    # items: only the correct tiles, sorted ascending for correct order
    correct_tiles = sorted(tiles)
    items = [{'label': str(t), 'order': i + 1} for i, t in enumerate(correct_tiles)]

    return {
        'q_type': 'ordering',
        'prompt_fr': f'Range ces blocs du plus petit au plus grand pour former {n}.',
        'prompt_en': f'Sort these blocks from smallest to largest to build {n}.',
        'hint_fr': 'Les milliers ont la plus grande valeur, les unités la plus petite.',
        'hint_en': 'Thousands have the highest value, units the lowest.',
        'shape_data': [],
        'choices': [],
        'items': items,
        'correct_answers': [str(t) for t in correct_tiles],
        'time_limit': 40,
        'points': 1,
        'explanation_fr': f'Les blocs de {n} sont : {" + ".join(str(t) for t in reversed(correct_tiles))}',
        'explanation_en': f'The blocks of {n} are: {" + ".join(str(t) for t in reversed(correct_tiles))}',
    }


# ─── 9. order_numbers_gen ─────────────────────────────────────────────────────

def order_numbers_gen(level: str = 'medium') -> dict:
    """
    Ordering — drag 4-5 numbers into ascending order.
    Difficulty controls how "close" the numbers are.
    """
    count = 4 if level == 'easy' else 5

    if level == 'easy':
        # Hundreds, spaced 10-150 apart
        base = random.randint(100, 800)
        gaps = sorted(random.sample(range(10, 200), count - 1))
        nums = [base] + [base + g for g in gaps]
    elif level == 'medium':
        # Mix of 3- and 4-digit numbers
        nums = sorted(random.sample(range(500, 5000), count))
    else:
        # 4-digit numbers, potentially close
        base = random.randint(1000, 8000)
        gaps = sorted(random.sample(range(1, 500), count - 1))
        nums = [base] + [base + g for g in gaps]

    # Ensure uniqueness and sort
    nums = sorted(list(set(nums)))[:count]
    items = [{'label': str(n), 'order': i + 1} for i, n in enumerate(nums)]

    return {
        'q_type': 'ordering',
        'prompt_fr': 'Range ces nombres du plus petit au plus grand.',
        'prompt_en': 'Sort these numbers from smallest to largest.',
        'hint_fr': 'Compare d\'abord les chiffres des milliers, puis des centaines.',
        'hint_en': 'Compare the thousands digit first, then the hundreds digit.',
        'shape_data': [],
        'choices': [],
        'items': items,
        'correct_answers': [str(n) for n in nums],
        'time_limit': 35,
        'points': 1,
        'explanation_fr': f'Ordre croissant : {" < ".join(str(n) for n in nums)}',
        'explanation_en': f'Ascending order: {" < ".join(str(n) for n in nums)}',
    }
