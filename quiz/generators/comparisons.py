import random
from fractions import Fraction
from .base import _frac_str, _tagged_shuffle_mc

# ── shared helper ─────────────────────────────────────────────────────────────

def _cmp_choices(correct_sym):
    """Build a 3-choice comparison MC list with misconception metadata."""
    syms = ['<', '>', '=']
    wrong_syms = [s for s in syms if s != correct_sym]

    # Assign error types to each wrong symbol
    def _wrong_meta(sym, correct):
        if (sym == '>' and correct == '<') or (sym == '<' and correct == '>'):
            return (
                'reversed_comparison',
                "You have the comparison backwards — check which number is larger.",
                "Tu as inversé la comparaison — vérifie quel nombre est le plus grand.",
            )
        # sym == '=' when correct is < or >
        return (
            'wrong_operation',
            "The numbers are not equal — compare them more carefully.",
            "Les nombres ne sont pas égaux — compare-les plus attentivement.",
        )

    tagged_candidates = []
    for ws in wrong_syms:
        err, fb_en, fb_fr = _wrong_meta(ws, correct_sym)
        tagged_candidates.append((ws, err, fb_en, fb_fr))

    # _tagged_shuffle_mc expects at most 4 wrong candidates for a 5-slot list,
    # but comparison only has 2 wrong options — that is fine, fallback pads
    # won't be hit since we always have exactly 2 candidates and need only 2.
    # We use a custom build here to keep exactly 3 choices total.
    random.shuffle(tagged_candidates)
    choices = [
        {
            'label': c[0],
            'correct': False,
            'error_type': c[1],
            'feedback_en': c[2],
            'feedback_fr': c[3],
        }
        for c in tagged_candidates
    ]
    pos = random.randint(0, len(choices))
    choices.insert(pos, {
        'label': correct_sym,
        'correct': True,
        'error_type': '',
        'feedback_en': '',
        'feedback_fr': '',
    })
    return choices


def _sym(a, b):
    if a < b:
        return '<'
    elif a > b:
        return '>'
    return '='


def _cmp_result(q, correct_sym, op1, op2, lang):
    """Build a complete question dict for a comparison."""
    sym_word = {
        '<': ('less than', 'inférieur à'),
        '>': ('greater than', 'supérieur à'),
        '=': ('equal to', 'égal à'),
    }
    en, fr = sym_word[correct_sym]
    return {
        'q_type':         'multiple_choice',
        'prompt_en':      f'Compare: {q["a_str"]} __ {q["b_str"]} — choose the correct symbol.',
        'prompt_fr':      f'Comparez : {q["a_str"]} __ {q["b_str"]} — choisissez le bon symbole.',
        'hint_en':        q.get('hint_en', 'Think about the relative sizes.'),
        'hint_fr':        q.get('hint_fr', 'Pensez aux tailles relatives.'),
        'shape_data':     [{'type': 'fraction_expr', 'op1': op1, 'operator': '□',
                            'op2': op2, 'format': 'compare'}],
        'choices':        _cmp_choices(correct_sym),
        'correct_answers': [correct_sym],
        'time_limit':     20,
        'points':         1,
        'explanation_en': (
            f'Step 1: Convert both values to the same form if needed.\n'
            f'Step 2: Compare them: {q["a_str"]} is {en} {q["b_str"]}.\n'
            f'Answer: {q["a_str"]} {correct_sym} {q["b_str"]}'
        ),
        'explanation_fr': (
            f'Étape 1 : Convertis les deux valeurs sous la même forme si nécessaire.\n'
            f'Étape 2 : Compare-les : {q["a_str"]} est {fr} {q["b_str"]}.\n'
            f'Réponse : {q["a_str"]} {correct_sym} {q["b_str"]}'
        ),
    }


# ── ordering helper ───────────────────────────────────────────────────────────

def _ordering_variant(labels, values, direction, time_limit=30, points=2):
    """
    Build a generic ordering question dict.

    labels  : list of display strings, already in the correct sorted order
    values  : (unused externally, just for documentation) corresponding numeric values
    direction: 'asc' or 'desc'
    """
    direction_en = 'smallest to largest' if direction == 'asc' else 'largest to smallest'
    direction_fr = 'du plus petit au plus grand' if direction == 'asc' else 'du plus grand au plus petit'
    correct_str = ', '.join(labels)
    items = [{'label': lbl, 'order': i + 1} for i, lbl in enumerate(labels)]
    return {
        'q_type':          'ordering',
        'prompt_en':       f'Sort these numbers from {direction_en}.',
        'prompt_fr':       f'Rangez ces nombres {direction_fr}.',
        'hint_en':         'Compare each pair of numbers to determine their relative order.',
        'hint_fr':         'Comparez chaque paire de nombres pour déterminer leur ordre relatif.',
        'shape_data':      [],
        'items':           items,
        'correct_answers': [],
        'time_limit':      time_limit,
        'points':          points,
        'explanation_en':  (
            f'Step 1: Compare each number.\n'
            f'Step 2: Order {direction_en}.\n'
            f'Answer: {correct_str}'
        ),
        'explanation_fr':  (
            f'Étape 1 : Compare chaque nombre.\n'
            f'Étape 2 : Ordonne {direction_fr}.\n'
            f'Réponse : {correct_str}'
        ),
    }


# ── integer comparison ────────────────────────────────────────────────────────

def _int_ordering(level):
    if level == 'easy':
        nums = random.sample(range(1, 51), 4)
    elif level == 'medium':
        nums = random.sample(range(-50, 51), 5)
    else:
        nums = random.sample(range(-999, 1000), 5)

    direction = 'asc'
    if level == 'hard':
        direction = random.choice(['asc', 'desc'])

    sorted_nums = sorted(nums, reverse=(direction == 'desc'))
    labels = [str(n) for n in sorted_nums]
    return _ordering_variant(labels, sorted_nums, direction)


def compare_int_gen(level='medium'):
    if random.random() < 0.30:
        return _int_ordering(level)

    if level == 'easy':
        a = random.randint(1, 100)
        b = random.randint(1, 100)
    elif level == 'medium':
        a = random.randint(-100, 100)
        b = random.randint(-100, 100)
    else:
        a = random.randint(-9999, 9999)
        b = random.randint(-9999, 9999)
    correct = _sym(a, b)
    q = {
        'a_str': str(a),
        'b_str': str(b),
        'hint_en': 'Larger numbers are further right on a number line.',
        'hint_fr': "Les grands nombres sont plus à droite sur la droite des nombres.",
    }
    return _cmp_result(q, correct, str(a), str(b), 'en')


# ── decimal comparison ────────────────────────────────────────────────────────

def _decimal_ordering(level):
    if level == 'easy':
        # 4 decimals with 1 decimal place, drawn without replacement
        candidates = [round(v / 10, 1) for v in range(1, 100)]
        nums = random.sample(candidates, 4)
        sorted_nums = sorted(nums)
        labels = [f'{n:.1f}' for n in sorted_nums]
        return _ordering_variant(labels, sorted_nums, 'asc')

    elif level == 'medium':
        # 5 decimals with 2 decimal places
        candidates = [round(v / 100, 2) for v in range(1, 1000)]
        nums = random.sample(candidates, 5)
        sorted_nums = sorted(nums)
        labels = [f'{n:.2f}' for n in sorted_nums]
        return _ordering_variant(labels, sorted_nums, 'asc')

    else:
        # Hard: tricky decimals that look similar
        tricky_pools = [
            [0.3, 0.30, 0.305, 0.31, 0.35],
            [0.1, 0.10, 0.101, 0.11, 0.15],
            [0.5, 0.50, 0.505, 0.51, 0.55],
            [0.9, 0.90, 0.901, 0.91, 0.99],
            [1.0, 1.01, 1.1, 1.10, 1.11],
            [0.2, 0.20, 0.201, 0.21, 0.25],
        ]
        pool = random.choice(tricky_pools)
        nums = random.sample(pool, 5)
        sorted_nums = sorted(nums)
        # Format with enough precision to show the difference
        labels = [f'{n:.3f}'.rstrip('0').rstrip('.') if '.' in f'{n:.3f}' else f'{n:.3f}'
                  for n in sorted_nums]
        # Ensure labels are distinct and meaningful; fall back to g-format
        labels = [f'{n:g}' for n in sorted_nums]
        return _ordering_variant(labels, sorted_nums, 'asc')


def compare_decimal_gen(level='medium'):
    if random.random() < 0.30:
        return _decimal_ordering(level)

    if level == 'easy':
        # 1 decimal place
        a = round(random.randint(1, 99) / 10, 1)
        b = round(random.randint(1, 99) / 10, 1)
    elif level == 'medium':
        # 2 decimal places, include tricky same-looking numbers
        a = round(random.randint(1, 999) / 100, 2)
        b = round(random.randint(1, 999) / 100, 2)
        # occasionally generate tricky pair
        if random.random() < 0.3:
            base = round(random.randint(1, 99) / 10, 1)
            a = base
            b = round(base + random.choice([-0.01, 0.01, 0.09, -0.09]), 2)
    else:
        # hard: tricky decimals e.g. 0.7 vs 0.70 vs 0.700
        pairs = [
            (0.7, 0.70), (0.50, 0.5), (1.20, 1.2),
            (0.3, 0.30), (2.10, 2.1), (0.08, 0.080),
            (1.005, 1.05), (0.99, 1.0), (0.101, 0.11),
            (0.9, 0.90), (3.14, 3.140), (0.123, 0.1230),
        ]
        a, b = random.choice(pairs)
    correct = _sym(a, b)
    a_s = f'{a:g}'
    b_s = f'{b:g}'
    q = {
        'a_str': a_s,
        'b_str': b_s,
        'hint_en': 'Compare digit by digit from left to right.',
        'hint_fr': 'Comparez chiffre par chiffre de gauche à droite.',
    }
    return _cmp_result(q, correct, a_s, b_s, 'en')


# ── fraction comparison ───────────────────────────────────────────────────────

_EASY_DENS   = [2, 3, 4, 5, 6]
_MEDIUM_DENS = [2, 3, 4, 5, 6, 8, 10]
_HARD_DENS   = [3, 4, 5, 6, 7, 8, 9, 10, 12]


def _fraction_ordering(level):
    if level == 'easy':
        # 4 fractions with the same denominator
        d = random.choice(_EASY_DENS)
        numerators = random.sample(range(1, d + 1), min(4, d))
        # Pad if the denominator is too small to give 4 distinct numerators
        while len(numerators) < 4:
            extra = random.randint(1, d * 2)
            numerators.append(extra)
        fracs = [Fraction(n, d) for n in numerators[:4]]
        sorted_fracs = sorted(fracs)
        labels = [_frac_str(f.numerator, f.denominator) for f in sorted_fracs]
        values = [float(f) for f in sorted_fracs]
        return _ordering_variant(labels, values, 'asc')

    elif level == 'medium':
        # 5 fractions with different denominators
        dens = random.sample(_MEDIUM_DENS, min(5, len(_MEDIUM_DENS)))
        fracs = [Fraction(random.randint(1, d), d) for d in dens[:5]]
        sorted_fracs = sorted(set(fracs))
        # Ensure we have 5 distinct values; retry individual fractions if needed
        while len(sorted_fracs) < 5:
            d = random.choice(_MEDIUM_DENS)
            fracs.append(Fraction(random.randint(1, d), d))
            sorted_fracs = sorted(set(fracs))
        sorted_fracs = sorted_fracs[:5]
        labels = [_frac_str(f.numerator, f.denominator) for f in sorted_fracs]
        values = [float(f) for f in sorted_fracs]
        return _ordering_variant(labels, values, 'asc')

    else:
        # Hard: 5 fractions with varied denominators from _HARD_DENS
        fracs = set()
        attempts = 0
        while len(fracs) < 5 and attempts < 50:
            d = random.choice(_HARD_DENS)
            fracs.add(Fraction(random.randint(1, d), d))
            attempts += 1
        sorted_fracs = sorted(fracs)[:5]
        labels = [_frac_str(f.numerator, f.denominator) for f in sorted_fracs]
        values = [float(f) for f in sorted_fracs]
        return _ordering_variant(labels, values, 'asc')


def compare_fraction_gen(level='medium'):
    if random.random() < 0.30:
        return _fraction_ordering(level)

    if level == 'easy':
        # same denominator
        d = random.choice(_EASY_DENS)
        n1 = random.randint(1, d)
        n2 = random.randint(1, d)
        f1, f2 = Fraction(n1, d), Fraction(n2, d)
    elif level == 'medium':
        dens = _MEDIUM_DENS
        d1 = random.choice(dens)
        d2 = random.choice([x for x in dens if x != d1] or dens)
        n1 = random.randint(1, d1)
        n2 = random.randint(1, d2)
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
    else:
        dens = _HARD_DENS
        d1 = random.choice(dens)
        d2 = random.choice(dens)
        n1 = random.randint(1, d1)
        n2 = random.randint(1, d2)
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
    correct = _sym(f1, f2)
    a_s = _frac_str(f1.numerator, f1.denominator)
    b_s = _frac_str(f2.numerator, f2.denominator)
    q = {
        'a_str': a_s,
        'b_str': b_s,
        'hint_en': 'Convert both fractions to a common denominator to compare.',
        'hint_fr': 'Convertissez les deux fractions au même dénominateur pour comparer.',
    }
    op1 = {'num': f1.numerator, 'den': f1.denominator}
    op2 = {'num': f2.numerator, 'den': f2.denominator}
    return _cmp_result(q, correct, op1, op2, 'en')


# ── mixed comparison (decimal vs fraction) ────────────────────────────────────

_MIXED_PAIRS = [
    # (a_val, b_val, a_str, b_str, a_display, b_display)
    (0.5,   0.5,   '0.5',  '1/2',  '0.5',               {'num': 1, 'den': 2}),
    (0.75,  0.75,  '3/4',  '0.75', {'num': 3, 'den': 4}, '0.75'),
    (0.8,   0.75,  '0.8',  '3/4',  '0.8',               {'num': 3, 'den': 4}),
    (0.333, 0.5,   '1/3',  '0.5',  {'num': 1, 'den': 3}, '0.5'),
    (0.25,  0.3,   '1/4',  '0.3',  {'num': 1, 'den': 4}, '0.3'),
    (0.6,   0.625, '0.6',  '5/8',  '0.6',               {'num': 5, 'den': 8}),
    (1.0,   1.0,   '4/4',  '1.0',  {'num': 4, 'den': 4}, '1.0'),
    (0.125, 0.25,  '1/8',  '1/4',  {'num': 1, 'den': 8}, {'num': 1, 'den': 4}),
    (0.4,   0.4,   '2/5',  '0.4',  {'num': 2, 'den': 5}, '0.4'),
    (0.667, 0.75,  '2/3',  '3/4',  {'num': 2, 'den': 3}, {'num': 3, 'den': 4}),
    (0.9,   0.875, '0.9',  '7/8',  '0.9',               {'num': 7, 'den': 8}),
    (1.5,   1.5,   '3/2',  '1.5',  {'num': 3, 'den': 2}, '1.5'),
    (0.2,   0.25,  '1/5',  '1/4',  {'num': 1, 'den': 5}, {'num': 1, 'den': 4}),
    (0.7,   0.7,   '7/10', '0.7',  {'num': 7, 'den': 10}, '0.7'),
]


def _mixed_ordering(level):
    """Sort 4 mixed decimal/fraction items from _MIXED_PAIRS ascending."""
    if level == 'easy':
        pool = _MIXED_PAIRS[:5]
    elif level == 'medium':
        pool = _MIXED_PAIRS[:10]
    else:
        pool = _MIXED_PAIRS

    chosen = random.sample(pool, min(4, len(pool)))
    # Sort by a_val (index 0) ascending
    sorted_items = sorted(chosen, key=lambda x: x[0])
    # Use a_str (index 2) as the display label
    labels = [item[2] for item in sorted_items]
    values = [item[0] for item in sorted_items]
    return _ordering_variant(labels, values, 'asc')


def compare_mixed_gen(level='medium'):
    if level in ('medium', 'hard') and random.random() < 0.30:
        return _mixed_ordering(level)

    if level == 'easy':
        pool = _MIXED_PAIRS[:5]
    elif level == 'medium':
        pool = _MIXED_PAIRS[:10]
    else:
        pool = _MIXED_PAIRS
    a_val, b_val, a_str, b_str, a_display, b_display = random.choice(pool)
    correct = _sym(float(a_val), float(b_val))
    q = {
        'a_str': a_str,
        'b_str': b_str,
        'hint_en': 'Convert both values to the same form (decimal or fraction) to compare.',
        'hint_fr': 'Convertissez les deux valeurs sous la même forme (décimal ou fraction) pour comparer.',
    }
    return _cmp_result(q, correct, a_display, b_display, 'en')
