"""
g5_arithmetic.py — Grade-5 arithmetic generators (content_g5.md Ch.4).

Topics:
  g5_order_ops_gen       QCM   – order of operations
  g5_div_decimal_gen     typed – natural ÷ small int = finite decimal
  g5_decimal_mult_gen    typed – decimal × natural
  g5_decimal_div_gen     typed – decimal ÷ natural (≤ 10)

Difficulty scales length/complexity of expressions and magnitudes.
Every number is written with a decimal comma in French and a decimal point in
English; explanations show the real steps of each calculation.
"""
import random
from .base import _tagged_shuffle_mc

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

_PLACE = {1: ('dixièmes', 'tenths'), 2: ('centièmes', 'hundredths'), 3: ('millièmes', 'thousandths'),
          4: ('dix-millièmes', 'ten-thousandths')}


def _dec(scaled, places):
    """scaled / 10**places as (fr, en) without useless trailing zeros: (2650, 3) → ('2,65', '2.65')."""
    s = str(scaled).rjust(places + 1, '0')
    whole, frac = s[:-places] if places else s, s[-places:] if places else ''
    frac = frac.rstrip('0')
    if not frac:
        return whole, whole
    return f'{whole},{frac}', f'{whole}.{frac}'


def _plural(n, fr_one, fr_many, en_one, en_many):
    return (f'{n} {fr_one if n == 1 else fr_many}', f'{n} {en_one if n == 1 else en_many}')


def _long_division(scaled, places, b):
    """
    Long division of (scaled / 10**places) by b, written step by step.
    Returns (steps_fr, steps_en, quotient_scaled, quotient_places).
    """
    s = str(scaled).rjust(places + 1, '0')
    whole = int(s[:-places]) if places else scaled
    digits = [int(c) for c in s[-places:]] if places else []
    q0, rem = divmod(whole, b)
    fr = [f'Partie entière : {whole} ÷ {b} = {q0}, reste {rem}.']
    en = [f'Whole part: {whole} ÷ {b} = {q0}, remainder {rem}.']
    q_digits = []
    k = 0
    while (k < len(digits) or rem) and k < 6:
        d = digits[k] if k < len(digits) else 0
        cur = rem * 10 + d
        qd, rem = divmod(cur, b)
        q_digits.append(qd)
        pfr, pen = _PLACE.get(k + 1, ('', ''))
        extra_fr = '' if k < len(digits) else ' (on ajoute un 0)'
        extra_en = '' if k < len(digits) else ' (write a 0)'
        fr.append(f'{cur} {pfr} ÷ {b} = {qd} {pfr}, reste {rem}{extra_fr}.')
        en.append(f'{cur} {pen} ÷ {b} = {qd} {pen}, remainder {rem}{extra_en}.')
        k += 1
    qp = len(q_digits)
    q_scaled = q0 * 10 ** qp + int(''.join(map(str, q_digits)) or 0)
    return fr, en, q_scaled, qp


# ─────────────────────────────────────────────────────────────────────────────
# g5_order_ops_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_order_ops_gen(level='easy'):
    """QCM — compute an expression respecting order of operations."""
    if level == 'easy':
        # a + b × c
        b, c, a = random.randint(2, 9), random.randint(2, 9), random.randint(1, 15)
        correct = a + b * c
        expr = f"{a} + {b} × {c}"
        steps = ([f'{b} × {c} = {b * c}', f'{a} + {b * c} = {correct}'],
                 [f'{b} × {c} = {b * c}', f'{a} + {b * c} = {correct}'])
        wrong = [((a + b) * c, 'left_to_right'), (a + b + c, 'wrong_operation'), (a * b + c, 'wrong_operation'),
                 (a + b * (c + 1), 'calculation'), (a + b * (c - 1), 'calculation'), (correct + 10, 'calculation')]
    elif level == 'medium':
        kind = random.choice(['parens', 'double_mult'])
        if kind == 'parens':
            # (a + b) × c
            a, b, c = random.randint(2, 10), random.randint(2, 10), random.randint(2, 8)
            correct = (a + b) * c
            expr = f"({a} + {b}) × {c}"
            steps = ([f'Parenthèses : {a} + {b} = {a + b}', f'{a + b} × {c} = {correct}'],
                     [f'Parentheses: {a} + {b} = {a + b}', f'{a + b} × {c} = {correct}'])
            wrong = [(a + b * c, 'left_to_right'), (a * b * c, 'wrong_operation'), (a + b + c, 'wrong_operation'),
                     (a * c + b, 'ignored_parentheses'), ((a + b) * (c + 1), 'calculation'), ((a + b) * (c - 1), 'calculation')]
        else:
            # a × b + c × d
            a, b, c, d = random.randint(2, 8), random.randint(2, 6), random.randint(2, 8), random.randint(2, 6)
            correct = a * b + c * d
            expr = f"{a} × {b} + {c} × {d}"
            steps = ([f'{a} × {b} = {a * b}', f'{c} × {d} = {c * d}', f'{a * b} + {c * d} = {correct}'],
                     [f'{a} × {b} = {a * b}', f'{c} × {d} = {c * d}', f'{a * b} + {c * d} = {correct}'])
            wrong = [((a * b + c) * d, 'left_to_right'), (a * (b + c) * d, 'wrong_operation'), (a * b + c + d, 'wrong_operation'),
                     ((a + c) * (b + d), 'wrong_operation'), (correct + c, 'calculation'), (correct - 1, 'calculation')]
    else:
        kind = random.choice(['sub', 'div'])
        if kind == 'sub':
            # (a + b) × c − d
            a, b, c, d = random.randint(2, 8), random.randint(2, 8), random.randint(2, 6), random.randint(1, 10)
            correct = (a + b) * c - d
            expr = f"({a} + {b}) × {c} − {d}"
            steps = ([f'Parenthèses : {a} + {b} = {a + b}', f'{a + b} × {c} = {(a + b) * c}', f'{(a + b) * c} − {d} = {correct}'],
                     [f'Parentheses: {a} + {b} = {a + b}', f'{a + b} × {c} = {(a + b) * c}', f'{(a + b) * c} − {d} = {correct}'])
            wrong = [(a + b * c - d, 'ignored_parentheses'), ((a + b) * c + d, 'wrong_operation'),
                     ((a + b) * (c - d) if c >= d else None, 'wrong_order'), ((a + b) * c - d + 1, 'calculation'),
                     (a + b + c - d if a + b + c >= d else None, 'wrong_operation'), ((a + b) * (c + 1) - d, 'calculation')]
        else:
            # a × (b + c) ÷ d, divisible
            d = random.choice([2, 3, 4, 5])
            b, c = random.randint(1, 5), random.randint(1, 5)
            a = d * random.randint(1, 4)
            bc = b + c
            correct = a * bc // d
            expr = f"{a} × ({b} + {c}) ÷ {d}"
            steps = ([f'Parenthèses : {b} + {c} = {bc}', f'{a} × {bc} = {a * bc}', f'{a * bc} ÷ {d} = {correct}'],
                     [f'Parentheses: {b} + {c} = {bc}', f'{a} × {bc} = {a * bc}', f'{a * bc} ÷ {d} = {correct}'])
            wrong = [(a * b + c, 'ignored_parentheses'), (a * bc * d, 'wrong_operation'), (a + bc, 'wrong_operation'),
                     (correct + 1, 'calculation'), (a * bc, 'forgot_division'), (correct + d, 'calculation')]

    fb = {
        'left_to_right': ('Do multiplications before additions — not simply left to right.',
                          'Effectue les multiplications avant les additions — pas simplement de gauche à droite.'),
        'ignored_parentheses': ('Start with the parentheses.', 'Commence par les parenthèses.'),
        'wrong_operation': ('Check which operation to do first.', 'Vérifie quelle opération faire en premier.'),
        'wrong_order': ('Follow the order: parentheses, then × and ÷, then + and −.',
                        'Respecte l’ordre : parenthèses, puis × et ÷, puis + et −.'),
        'forgot_division': ('You forgot the last step.', 'Tu as oublié la dernière étape.'),
        'calculation': ('Recheck your arithmetic.', 'Recalcule soigneusement.'),
    }
    wrong += [(correct + 1, 'calculation'), (correct - 1, 'calculation'), (correct + 2, 'calculation')]
    tagged = [(str(v), err) + fb[err] for v, err in wrong if v is not None and v > 0 and v != correct]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        f"Calcule : **{expr}**",
        'prompt_en':        f"Calculate: **{expr}**",
        'hint_fr':          'Parenthèses → multiplications et divisions → additions et soustractions.',
        'hint_en':          'Parentheses → multiplication and division → addition and subtraction.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(str(correct), tagged),
        'pairs':            [],
        'explanation_fr':   '\n'.join(steps[0] + [f'Réponse : {expr} = **{correct}**']),
        'explanation_en':   '\n'.join(steps[1] + [f'Answer: {expr} = **{correct}**']),
        'correct_answers':  [str(correct)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_div_decimal_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_div_decimal_gen(level='easy'):
    """Typed — natural ÷ small int = finite decimal quotient (never a whole number)."""
    if level == 'easy':
        divisors, lo, hi, places = [2, 4, 5], 1, 9, 1
    elif level == 'medium':
        divisors, lo, hi, places = [2, 4, 5, 8], 5, 30, 2
    else:
        divisors, lo, hi, places = [4, 8], 10, 99, 3
    scale = 10 ** places
    while True:
        b = random.choice(divisors)
        q_scaled = random.randint(lo * scale, hi * scale)
        if b * q_scaled % scale == 0 and q_scaled % scale:
            break
    a = b * q_scaled // scale

    steps_fr, steps_en, qs, qp = _long_division(a, 0, b)
    q_fr, q_en = _dec(qs, qp)
    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Calcule : **{a} ÷ {b}**",
        'prompt_en':        f"Calculate: **{a} ÷ {b}**",
        'hint_fr':          (f'{a} ÷ {b} = {a // b}, reste {a % b}. Place la virgule, puis transforme le reste '
                             f'en dixièmes : {a % b * 10} dixièmes ÷ {b}…'),
        'hint_en':          (f'{a} ÷ {b} = {a // b}, remainder {a % b}. Write the decimal point, then turn the remainder '
                             f'into tenths: {a % b * 10} tenths ÷ {b}…'),
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_fr':   '\n'.join(steps_fr + [f'Réponse : {a} ÷ {b} = **{q_fr}**']),
        'explanation_en':   '\n'.join(steps_en + [f'Answer: {a} ÷ {b} = **{q_en}**']),
        'correct_answers':  [q_fr, q_en],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_decimal_mult_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_decimal_mult_gen(level='easy'):
    """Typed — decimal × natural."""
    if level == 'easy':
        dec_places = 1
        b = random.randint(2, 6)
        q_scaled = random.randint(11, 49)
    elif level == 'medium':
        dec_places = 2
        b = random.randint(2, 9)
        q_scaled = random.randint(101, 999)
    else:
        dec_places = random.choice([2, 3])
        b = random.randint(2, 12)
        scale = 10 ** dec_places
        q_scaled = random.randint(scale + 1, 9 * scale - 1)
    while q_scaled % 10 == 0:                     # 1,20 would really have 1 decimal place
        q_scaled += 1

    a_fr, a_en = _dec(q_scaled, dec_places)
    product = q_scaled * b
    p_fr, p_en = _dec(product, dec_places)
    n_fr, n_en = _plural(dec_places, 'décimale', 'décimales', 'decimal place', 'decimal places')
    pos_fr, pos_en = _plural(dec_places, 'rang', 'rangs', 'place', 'places')
    raw = str(product).rjust(dec_places + 1, '0')
    placed = f'{raw[:-dec_places]},{raw[-dec_places:]}'

    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Calcule : **{a_fr} × {b}**",
        'prompt_en':        f"Calculate: **{a_en} × {b}**",
        'hint_fr':          f"Calcule {q_scaled} × {b} comme des entiers, puis place la virgule ({n_fr} dans {a_fr}).",
        'hint_en':          f"Work out {q_scaled} × {b} as whole numbers, then place the decimal point ({n_en} in {a_en}).",
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_fr': (
            f'Étape 1 : Sans la virgule, multiplie comme des entiers : {q_scaled} × {b} = {product}.\n'
            f'Étape 2 : {a_fr} a {n_fr}.\n'
            f'Étape 3 : Place la virgule à {pos_fr} depuis la droite : {placed}.\n'
            f'Réponse : {a_fr} × {b} = **{p_fr}**'
        ),
        'explanation_en': (
            f'Step 1: Ignore the decimal point and multiply as whole numbers: {q_scaled} × {b} = {product}.\n'
            f'Step 2: {a_en} has {n_en}.\n'
            f'Step 3: Place the decimal point {pos_en} from the right: {placed.replace(",", ".")}.\n'
            f'Answer: {a_en} × {b} = **{p_en}**'
        ),
        'correct_answers':  [p_fr, p_en],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_decimal_div_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_decimal_div_gen(level='easy'):
    """Typed — decimal ÷ natural; both the dividend and the quotient are true decimals."""
    if level == 'easy':
        divisors, lo, hi, places = [2, 4, 5], 2, 99, 1          # quotient in tenths: 0,2 … 9,9
    elif level == 'medium':
        divisors, lo, hi, places = [2, 4, 5, 8], 100, 3000, 2   # quotient in hundredths: 1,00 … 30,00
    else:
        divisors, lo, hi, places = [3, 6, 7, 8, 9], 1000, 9999, 2
    scale = 10 ** places
    while True:
        b = random.choice(divisors)
        q_scaled = random.randint(lo, hi)
        d_scaled = q_scaled * b                          # dividend, same number of places
        if q_scaled % scale and d_scaled % scale:        # neither is a whole number
            break
    # Write the dividend without useless trailing zeros (10,80 → 10,8).
    d_places = places
    while d_scaled % 10 == 0:
        d_scaled //= 10
        d_places -= 1
    d_fr, d_en = _dec(d_scaled, d_places)

    steps_fr, steps_en, qs, qp = _long_division(d_scaled, d_places, b)
    q_fr, q_en = _dec(qs, qp)
    whole = d_scaled // 10 ** d_places
    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Calcule : **{d_fr} ÷ {b}**",
        'prompt_en':        f"Calculate: **{d_en} ÷ {b}**",
        'hint_fr':          (f'Commence par la partie entière : combien de fois {b} entre-t-il dans {whole} ? '
                             f'Place la virgule dans le quotient au moment de passer aux dixièmes.'),
        'hint_en':          (f'Start with the whole part: how many times does {b} go into {whole}? '
                             f'Write the decimal point in the quotient when you move on to the tenths.'),
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_fr':   '\n'.join(steps_fr + [f'Réponse : {d_fr} ÷ {b} = **{q_fr}**']),
        'explanation_en':   '\n'.join(steps_en + [f'Answer: {d_en} ÷ {b} = **{q_en}**']),
        'correct_answers':  [q_fr, q_en],
    }
