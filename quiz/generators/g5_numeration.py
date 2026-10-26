"""
g5_numeration.py — Grade-5 numeration generators (content_g5.md Ch.4 + Ch.6).

Topics:
  g5_large_integer_gen   QCM         – read/write integers up to 999 999
  g5_decimal_write_gen   typed       – write decimal from verbal description (to thousandths)
  g5_decimal_forms_gen   mix_match   – match decimal ↔ decomposition ↔ fraction
  g5_number_line_gen     QCM + SVG   – identify the value of a point on a number line
"""
import random
from .base import _tagged_shuffle_mc


# ─────────────────────────────────────────────────────────────────────────────
# Number-to-words helpers
# ─────────────────────────────────────────────────────────────────────────────

_FR_ONES = [
    '', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf',
    'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize',
    'dix-sept', 'dix-huit', 'dix-neuf',
]
_FR_TENS = ['', 'dix', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante']
_EN_ONES = [
    '', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen', 'nineteen',
]
_EN_TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


def _to_fr(n):
    """French number words for 0 ≤ n ≤ 999 999."""
    if n == 0: return 'zéro'
    if n < 0:  return 'moins ' + _to_fr(-n)
    if n < 20: return _FR_ONES[n]
    if n < 70:
        t, u = divmod(n, 10)
        base = _FR_TENS[t]
        if u == 0:  return base
        if u == 1:  return base + '-et-un'
        return base + '-' + _to_fr(u)
    if n < 80:
        # 70-79: soixante-dix, soixante-et-onze, soixante-douze…
        u = n - 60
        if u == 11: return 'soixante-et-onze'
        return 'soixante-' + _to_fr(10 + (n % 10))
    if n < 90:
        u = n - 80
        if u == 0: return 'quatre-vingts'
        return 'quatre-vingt-' + _to_fr(u)
    if n < 100:
        return 'quatre-vingt-' + _to_fr(n - 80)
    if n < 1000:
        h, r = divmod(n, 100)
        if h == 1: prefix = 'cent'
        else:      prefix = _to_fr(h) + ' cent'
        if r == 0: return prefix + ('s' if h > 1 else '')
        return prefix + ' ' + _to_fr(r)
    if n < 1_000_000:
        th, r = divmod(n, 1000)
        if th == 1: prefix = 'mille'
        else:       prefix = _to_fr(th) + ' mille'
        if r == 0:  return prefix
        return prefix + ' ' + _to_fr(r)
    return str(n)


def _to_en(n):
    """English number words for 0 ≤ n ≤ 999 999."""
    if n == 0: return 'zero'
    if n < 20: return _EN_ONES[n]
    if n < 100:
        t, u = divmod(n, 10)
        return _EN_TENS[t] + ('-' + _EN_ONES[u] if u else '')
    if n < 1000:
        h, r = divmod(n, 100)
        return _EN_ONES[h] + ' hundred' + (' ' + _to_en(r) if r else '')
    if n < 1_000_000:
        th, r = divmod(n, 1000)
        return _to_en(th) + ' thousand' + (' ' + _to_en(r) if r else '')
    return str(n)


def _fmt_n(n):
    """Format large integer with non-breaking space separator (French style)."""
    s = str(n)
    if len(s) > 3:
        # Insert space every 3 digits from the right
        groups = []
        while s:
            groups.append(s[-3:])
            s = s[:-3]
        return ' '.join(reversed(groups))
    return str(n)


# ─────────────────────────────────────────────────────────────────────────────
# g5_large_integer_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_large_integer_gen(level='easy'):
    """QCM — read large integers; show number, choose word form."""
    if level == 'easy':
        n = random.randint(10_000, 99_999)
    elif level == 'medium':
        n = random.randint(100_000, 999_999)
    else:
        n = random.randint(100_000, 999_999)
        # Zero digit in one position for extra confusion
        digits = list(str(n))
        pos = random.randint(1, len(digits) - 2)
        digits[pos] = '0'
        n = int(''.join(digits))
        if n < 100_000:
            n += 100_000

    correct_fr = _to_fr(n)

    # Generate distractors: swap digits, off by thousands, etc.
    distractors = set()
    # Swap two adjacent digits
    s = str(n)
    for i in range(len(s) - 1):
        alt = list(s)
        alt[i], alt[i+1] = alt[i+1], alt[i]
        alt_n = int(''.join(alt))
        if alt_n != n and alt_n > 0:
            distractors.add(alt_n)
    # ±1 thousands
    distractors.add(n + 1000)
    distractors.add(abs(n - 1000))
    # ±100
    distractors.add(n + 100)

    distractors = [d for d in distractors if d != n and 0 < d < 1_000_000]
    random.shuffle(distractors)
    distractors = distractors[:4]

    tagged_candidates = [
        ((_to_fr(d), _to_en(d)), 'wrong_group',
         'Read each group of digits carefully: thousands, then hundreds.',
         'Lis chaque groupe de chiffres attentivement : milliers, puis centaines.')
        for d in distractors
    ]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        f"Comment lit-on le nombre **{_fmt_n(n)}** ?",
        'prompt_en':        f"How do you read the number **{_fmt_n(n)}**?",
        'hint_fr':          'Sépare le nombre en deux groupes : les milliers et les unités simples.',
        'hint_en':          'Split the number into two groups: thousands and simple units.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc((correct_fr, _to_en(n)), tagged_candidates),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Split {_fmt_n(n)} into groups of three from the right: thousands | units.\n'
            f'Step 2: Read the thousands group, then the units group.\n'
            f'Answer: {_fmt_n(n)} = {_to_en(n)}'
        ),
        'explanation_fr': (
            f'Étape 1 : Sépare {_fmt_n(n)} en groupes de trois depuis la droite : milliers | unités.\n'
            f'Étape 2 : Lis le groupe des milliers, puis le groupe des unités.\n'
            f'Réponse : {_fmt_n(n)} = {correct_fr}'
        ),
        'correct_answers':  [correct_fr],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_decimal_write_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_decimal_write_gen(level='easy'):
    """Typed — write a decimal number from a verbal description (to thousandths)."""
    if level == 'easy':
        # Tenths only: "3 dixièmes" → 0,3
        n = random.randint(1, 9)
        desc_fr = f"{n} dixième{'s' if n > 1 else ''}"
        desc_en = f"{n} tenth{'s' if n > 1 else ''}"
        correct = f"0,{n}"
        parts = [(n, 10, 'dixième', 'tenth')]
    elif level == 'medium':
        # Units + tenths + hundredths
        u  = random.randint(0, 9)
        d  = random.randint(0, 9)
        c  = random.randint(1, 9)
        desc_fr = (f"{u} unité{'s' if u > 1 else ''}, {d} dixième{'s' if d != 1 else ''} "
                   f"et {c} centième{'s' if c > 1 else ''}")
        desc_en = (f"{u} one{'s' if u != 1 else ''}, {d} tenth{'s' if d != 1 else ''} "
                   f"and {c} hundredth{'s' if c > 1 else ''}")
        correct = f"{u},{d}{c}"
        parts = [(u, 1, 'unité', 'one'), (d, 10, 'dixième', 'tenth'), (c, 100, 'centième', 'hundredth')]
    else:
        # Full: units + tenths + hundredths + thousandths
        u  = random.randint(1, 9)
        d  = random.randint(0, 9)
        c  = random.randint(0, 9)
        m  = random.randint(1, 9)
        desc_fr = (f"{u} unité{'s' if u > 1 else ''}, {d} dixième{'s' if d != 1 else ''}, "
                   f"{c} centième{'s' if c > 1 else ''} et {m} millième{'s' if m > 1 else ''}")
        desc_en = (f"{u} one{'s' if u != 1 else ''}, {d} tenth{'s' if d != 1 else ''}, "
                   f"{c} hundredth{'s' if c != 1 else ''} and {m} thousandth{'s' if m > 1 else ''}")
        correct = f"{u},{d}{c}{m}"
        parts = [(u, 1, 'unité', 'one'), (d, 10, 'dixième', 'tenth'), (c, 100, 'centième', 'hundredth'),
                 (m, 1000, 'millième', 'thousandth')]

    correct_dot = correct.replace(',', '.')

    def val(k, den):
        if den == 1:
            return str(k), str(k)
        places = len(str(den)) - 1
        v = f'0.{k:0{places}d}'
        return v.replace('.', ','), v
    steps_fr = [f"{k} {fr}{'s' if k > 1 else ''} = {val(k, den)[0]}" for k, den, fr, en in parts]
    steps_en = [f"{k} {en}{'s' if k != 1 else ''} = {val(k, den)[1]}" for k, den, fr, en in parts]
    sum_fr = ' + '.join(val(k, den)[0] for k, den, _, _ in parts)
    sum_en = ' + '.join(val(k, den)[1] for k, den, _, _ in parts)
    places_used = len(parts) - (1 if parts[0][1] == 1 else 0)
    hint_fr = ('Juste après la virgule : les dixièmes' + (', puis les centièmes' if places_used > 1 else '')
               + (', puis les millièmes' if places_used > 2 else '') + '. Écris 0 pour une position vide.')
    hint_en = ('Right after the decimal point: the tenths' + (', then the hundredths' if places_used > 1 else '')
               + (', then the thousandths' if places_used > 2 else '') + '. Write 0 for an empty place.')
    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Écris en chiffres : **{desc_fr}**",
        'prompt_en':        f"Write in digits: **{desc_en}**",
        'hint_fr':          hint_fr,
        'hint_en':          hint_en,
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': '\n'.join([f'Step 1: {"; ".join(steps_en)}.']
                                    + ([f'Step 2: {sum_en} = {correct_dot}'] if len(parts) > 1 else [])
                                    + [f'Answer: {correct_dot}']),
        'explanation_fr': '\n'.join([f'Étape 1 : {" ; ".join(steps_fr)}.']
                                    + ([f'Étape 2 : {sum_fr} = {correct}'] if len(parts) > 1 else [])
                                    + [f'Réponse : {correct}']),
        'correct_answers':  [correct, correct_dot],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_decimal_forms_gen
# ─────────────────────────────────────────────────────────────────────────────

_DECIMAL_PAIRS = [
    # (decimal_str, fraction_str, decomp_fr, decomp_en)
    ('0,1',  '1/10',  '1 dixième',                     '1 tenth'),
    ('0,2',  '2/10',  '2 dixièmes',                    '2 tenths'),
    ('0,5',  '5/10',  '5 dixièmes',                    '5 tenths'),
    ('0,25', '25/100','2 dixièmes et 5 centièmes',     '2 tenths and 5 hundredths'),
    ('0,75', '75/100','7 dixièmes et 5 centièmes',     '7 tenths and 5 hundredths'),
    ('0,3',  '3/10',  '3 dixièmes',                    '3 tenths'),
    ('1,5',  '15/10', '1 unité et 5 dixièmes',         '1 one and 5 tenths'),
    ('2,4',  '24/10', '2 unités et 4 dixièmes',        '2 ones and 4 tenths'),
    ('0,125','125/1000','1 dixième, 2 centièmes et 5 millièmes', '1 tenth, 2 hundredths and 5 thousandths'),
    ('3,14', '314/100','3 unités, 1 dixième et 4 centièmes',    '3 ones, 1 tenth and 4 hundredths'),
    ('0,04', '4/100', '4 centièmes',                   '4 hundredths'),
    ('1,25', '125/100','1 unité, 2 dixièmes et 5 centièmes',   '1 one, 2 tenths and 5 hundredths'),
]


def g5_decimal_forms_gen(level='easy'):
    """mix_match — pair decimal notation with its decomposition or fraction."""
    if level == 'easy':
        pool  = _DECIMAL_PAIRS[:6]
        count = 3
    elif level == 'medium':
        pool  = _DECIMAL_PAIRS[:9]
        count = 4
    else:
        pool  = _DECIMAL_PAIRS
        count = 4

    chosen = random.sample(pool, min(count, len(pool)))
    # Mix: left=decimal, right=decomposition (alternate with fraction for variety)
    pairs, lines_fr, lines_en = [], [], []
    for dec_str, frac_str, decomp_fr, decomp_en in chosen:
        dec_en = dec_str.replace(',', '.')
        if random.random() < 0.5:
            pairs.append({'left': dec_str, 'left_en': dec_en, 'right': decomp_fr, 'right_en': decomp_en})
            lines_fr.append(f'{dec_str} = {decomp_fr}')
            lines_en.append(f'{dec_en} = {decomp_en}')
        else:
            pairs.append({'left': dec_str, 'left_en': dec_en, 'right': frac_str, 'right_en': frac_str})
            lines_fr.append(f'{dec_str} = {frac_str} ({len(dec_str.split(",")[1])} chiffre(s) après la virgule → sur {frac_str.split("/")[1]})'
                            .replace('1 chiffre(s)', '1 chiffre').replace('chiffre(s)', 'chiffres'))
            lines_en.append(f'{dec_en} = {frac_str} ({len(dec_str.split(",")[1])} digit(s) after the point → over {frac_str.split("/")[1]})'
                            .replace('1 digit(s)', '1 digit').replace('digit(s)', 'digits'))
    thousandths = any(len(p['left'].split(',')[1]) == 3 for p in pairs)

    return {
        'q_type':           'mix_match',
        'prompt_fr':        'Associe chaque nombre décimal à sa bonne représentation.',
        'prompt_en':        'Match each decimal number to its correct representation.',
        'hint_fr':          'Ne confonds pas dixièmes (1 chiffre après la virgule) et centièmes (2 chiffres)'
                            + (', ni millièmes (3 chiffres).' if thousandths else '.'),
        'hint_en':          "Don't confuse tenths (1 decimal place) and hundredths (2 decimal places)"
                            + (', or thousandths (3 decimal places).' if thousandths else '.'),
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            pairs,
        'explanation_en':   '\n'.join(lines_en),
        'explanation_fr':   '\n'.join(lines_fr),
        'correct_answers':  [p['right'] for p in pairs],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_number_line_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_number_line_gen(level='easy'):
    """QCM + SVG — identify the value of a point on a graduated number line."""
    if level == 'easy':
        start = random.choice([0, 100, 200, 500])
        step  = random.choice([10, 25, 50])
        n_ticks = random.randint(5, 8)
    elif level == 'medium':
        start = random.choice([0, 1000, 5000])
        step  = random.choice([100, 250, 500])
        n_ticks = random.randint(5, 8)
    else:
        start = random.randint(0, 90) * 100
        step  = random.choice([10, 25, 50, 100])
        n_ticks = random.randint(6, 10)

    end    = start + step * (n_ticks - 1)
    # Pick a point on one of the ticks (never a labelled one)
    tick_idx = random.randint(2 if level == 'medium' else 1, n_ticks - 2)
    target = start + tick_idx * step
    if level == 'easy':
        labels = [start + i * step for i in range(n_ticks) if i != tick_idx]
    elif level == 'medium':
        labels = [start, start + step, end]
    else:
        labels = [start, end]

    correct_str = str(target)

    # Distractors: adjacent ticks, wrong steps
    tagged_candidates = [
        (str(target - step), 'one_step_left',
         'Count the steps carefully from the start.',
         'Compte les graduations soigneusement depuis le début.'),
        (str(target + step), 'one_step_right',
         'Count the steps carefully from the start.',
         'Compte les graduations soigneusement depuis le début.'),
        (str(target - 2 * step), 'two_steps_off',
         'Find the step size first, then count.',
         'Trouve d\'abord le pas, puis compte.'),
        (str(start), 'at_origin',
         'The point is not at the start of the line.',
         'Le point ne se trouve pas au début de la droite.'),
        (str(target + 2 * step), 'two_steps_off',
         'Find the step size first, then count.',
         "Trouve d'abord le pas, puis compte."),
        (str(start + tick_idx * step * 2), 'double_step',
         'Find the step size first, then count.',
         "Trouve d'abord le pas, puis compte."),
        (str(tick_idx * step) if start else None, 'forgot_start',
         'Start counting from the first number of the line.',
         'Commence à compter à partir du premier nombre de la droite.'),
        (str(end), 'at_end',
         'The point is not at the end of the line.',
         'Le point ne se trouve pas au bout de la droite.'),
    ]
    seen = {correct_str}
    tagged_candidates = [c for c in tagged_candidates
                         if c[0] is not None and int(c[0]) >= 0 and c[0] not in seen and not seen.add(c[0])]
    steps_en = 'step' if tick_idx == 1 else 'steps'

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        "Quel nombre correspond au point indiqué sur cette droite numérique ?",
        'prompt_en':        "Which number corresponds to the marked point on this number line?",
        'hint_fr':          "Trouve d'abord le pas : écart entre deux nombres écrits ÷ nombre d'intervalles. Puis compte les graduations.",
        'hint_en':          'Find the step first: gap between two written numbers ÷ number of intervals. Then count the ticks.',
        'show_illustration': True,
        'shape_data':       [{
            'type':      'number_line_svg',
            'nl_start':  start,
            'nl_end':    end,
            'nl_step':   step,
            'nl_target': target,
            'nl_labels': labels,
        }],
        'choices':          _tagged_shuffle_mc(correct_str, tagged_candidates[:4]),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Find the starting value ({start}) and the end value ({end}).\n'
            f'Step 2: Count the number of intervals between tick marks: each step = {step}.\n'
            f'Step 3: Count {tick_idx} {steps_en} from {start}: {start} + {tick_idx} × {step} = {target}.\n'
            f'Answer: {target}'
        ),
        'explanation_fr': (
            f'Étape 1 : Repère la valeur de départ ({start}) et la valeur finale ({end}).\n'
            f'Étape 2 : Identifie le pas entre deux graduations : chaque pas = {step}.\n'
            f'Étape 3 : Compte {tick_idx} pas depuis {start} : {start} + {tick_idx} × {step} = {target}.\n'
            f'Réponse : {target}'
        ),
        'correct_answers':  [correct_str],
    }
