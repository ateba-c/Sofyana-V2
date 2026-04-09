"""
g5_arithmetic.py — Grade-5 arithmetic generators (content_g5.md Ch.4).

Topics:
  g5_order_ops_gen       QCM   – order of operations (PEMDAS)
  g5_div_decimal_gen     typed – natural ÷ small int = finite decimal
  g5_decimal_mult_gen    typed – decimal × natural
  g5_decimal_div_gen     typed – decimal ÷ natural (≤ 10)

Difficulty scales length/complexity of expressions and magnitudes.
"""
import random
from .base import _tagged_shuffle_mc

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _fmt_decimal(value, decimals):
    """Format float with `decimals` places, comma separator."""
    s = f"{value:.{decimals}f}"
    return s.replace('.', ',')


def _make_decimal_div(b_choices, q_min, q_max, decimals):
    """
    Return (a_int, b, q_str) where a_int ÷ b = q (finite decimal with `decimals` places).
    Strategy: choose q_scaled (integer), compute a = b * q_scaled / 10^d if integer.
    """
    scale = 10 ** decimals
    for _ in range(300):
        b = random.choice(b_choices)
        q_scaled = random.randint(q_min * scale, q_max * scale)
        if b * q_scaled % scale == 0:
            a = b * q_scaled // scale
            q_str = _fmt_decimal(q_scaled / scale, decimals)
            return a, b, q_str
    return None


# ─────────────────────────────────────────────────────────────────────────────
# g5_order_ops_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_order_ops_gen(level='easy'):
    """QCM — compute an expression respecting order of operations."""
    if level == 'easy':
        # a + b × c
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        a = random.randint(1, 15)
        correct = a + b * c
        expr_fr = f"{a} + {b} × {c}"
        wrong_lr = (a + b) * c         # left-to-right error
        wrong2   = a + b + c
        wrong3   = a * b + c
        wrong4   = a + b * c - 1
    elif level == 'medium':
        kind = random.choice(['parens', 'double_mult'])
        if kind == 'parens':
            # (a + b) × c
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            c = random.randint(2, 8)
            correct  = (a + b) * c
            expr_fr  = f"({a} + {b}) × {c}"
            wrong_lr = a + b * c
            wrong2   = a * b * c
            wrong3   = (a + b) + c
            wrong4   = (a + b) * c + c
        else:
            # a × b + c × d
            a = random.randint(2, 8)
            b = random.randint(2, 6)
            c = random.randint(2, 8)
            d = random.randint(2, 6)
            correct  = a * b + c * d
            expr_fr  = f"{a} × {b} + {c} × {d}"
            wrong_lr = a * (b + c) * d
            wrong2   = (a + c) * (b + d)
            wrong3   = a * b * c * d
            wrong4   = a * b + c + d
    else:
        # (a + b) × c - d  or  a × (b + c) ÷ d
        kind = random.choice(['sub', 'div'])
        if kind == 'sub':
            a = random.randint(2, 8)
            b = random.randint(2, 8)
            c = random.randint(2, 6)
            d = random.randint(1, 10)
            correct = (a + b) * c - d
            while correct <= 0:
                d = random.randint(1, 5)
                correct = (a + b) * c - d
            expr_fr  = f"({a} + {b}) × {c} - {d}"
            wrong_lr = a + b * c - d
            wrong2   = (a + b) * (c - d)
            wrong3   = (a + b) * c + d
            wrong4   = (a + b) * c - d + 1
        else:
            # a × (b + c) ÷ d, ensure divisible
            d = random.choice([2, 3, 4, 5])
            b = random.randint(1, 5)
            c = random.randint(1, 5)
            # pick a so that a*(b+c) divisible by d
            bc = b + c
            a = d * random.randint(1, 4)
            correct  = a * bc // d
            expr_fr  = f"{a} × ({b} + {c}) ÷ {d}"
            wrong_lr = a * b + c // d
            wrong2   = a * bc * d
            wrong3   = a + bc // d
            wrong4   = a * bc // d + 1

    tagged_candidates = [
        (str(wrong_lr), 'left_to_right',
         'Apply multiplication before addition (or respect parentheses first).',
         'Effectue les multiplications avant les additions (ou les parenthèses en premier).'),
        (str(wrong2), 'wrong_operation', 'Check which operation to do first.',
         "Vérifie quelle opération faire en premier."),
        (str(wrong3), 'wrong_operation', 'Check which operation to do first.',
         "Vérifie quelle opération faire en premier."),
        (str(wrong4), 'off_by_one', 'Recheck your arithmetic.',
         'Recalcule soigneusement.'),
    ]
    # de-duplicate
    seen = set()
    unique_cand = []
    for c_tuple in tagged_candidates:
        if c_tuple[0] not in seen and c_tuple[0] != str(correct):
            seen.add(c_tuple[0])
            unique_cand.append(c_tuple)

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        f"Calcule : **{expr_fr}**",
        'prompt_en':        f"Calculate: **{expr_fr}**",
        'hint_fr':          'Parenthèses → Multiplications/Divisions → Additions/Soustractions.',
        'hint_en':          'Parentheses → Multiplication/Division → Addition/Subtraction.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(str(correct), unique_cand[:4]),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Apply order of operations to: {expr_fr}\n'
            f'Step 2: Parentheses first (if any).\n'
            f'Step 3: Multiplications and divisions left to right.\n'
            f'Step 4: Additions and subtractions left to right.\n'
            f'Answer: {expr_fr} = {correct}'
        ),
        'explanation_fr': (
            f'Étape 1 : Applique la priorité des opérations à : {expr_fr}\n'
            f'Étape 2 : Parenthèses en premier (si présentes).\n'
            f'Étape 3 : Multiplications et divisions de gauche à droite.\n'
            f'Étape 4 : Additions et soustractions de gauche à droite.\n'
            f'Réponse : {expr_fr} = {correct}'
        ),
        'correct_answers':  [str(correct)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_div_decimal_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_div_decimal_gen(level='easy'):
    """Typed — natural ÷ small int = finite decimal quotient."""
    if level == 'easy':
        result = _make_decimal_div([2, 4, 5], 1, 9, 1)
    elif level == 'medium':
        result = _make_decimal_div([2, 4, 5, 8, 10], 5, 30, 2)
    else:
        result = _make_decimal_div([2, 4, 5, 8, 10], 10, 99, 3)

    if result is None:
        result = (7, 4, '1,75')  # fallback
    a, b, q_str = result

    correct_dot = q_str.replace(',', '.')
    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Calcule : **{a} ÷ {b}**",
        'prompt_en':        f"Calculate: **{a} ÷ {b}**",
        'hint_fr':          'Continue la division après le reste en ajoutant des dixièmes, centièmes, millièmes…',
        'hint_en':          'Continue the division past the remainder by adding tenths, hundredths, thousandths…',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Divide {a} ÷ {b} using long division.\n'
            f'Step 2: When you reach a remainder, add a decimal point and continue with tenths (×10).\n'
            f'Step 3: Keep dividing until the remainder is 0.\n'
            f'Answer: {a} ÷ {b} = {q_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Divise {a} ÷ {b} par la méthode de la division posée.\n'
            f'Étape 2 : Quand tu obtiens un reste, place la virgule et continue avec les dixièmes (×10).\n'
            f'Étape 3 : Continue jusqu\'à ce que le reste soit 0.\n'
            f'Réponse : {a} ÷ {b} = {q_str}'
        ),
        'correct_answers':  [q_str, correct_dot],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_decimal_mult_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_decimal_mult_gen(level='easy'):
    """Typed — decimal × natural."""
    if level == 'easy':
        # 1 decimal place, small multiplier
        dec_places = 1
        b = random.randint(2, 6)
        q_scaled = random.randint(11, 49)   # tenths, ensures product < 30
        a_scaled = q_scaled                  # a = q_scaled / 10
    elif level == 'medium':
        dec_places = 2
        b = random.randint(2, 9)
        q_scaled = random.randint(101, 999)
    else:
        dec_places = random.choice([2, 3])
        b = random.randint(2, 12)
        scale = 10 ** dec_places
        q_scaled = random.randint(scale + 1, 9 * scale - 1)

    scale = 10 ** dec_places
    a_str = _fmt_decimal(q_scaled / scale, dec_places)
    product = q_scaled * b
    correct_str = _fmt_decimal(product / scale, dec_places).rstrip('0').rstrip(',')
    # also accept dot notation
    correct_dot = correct_str.replace(',', '.')

    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Calcule : **{a_str} × {b}**",
        'prompt_en':        f"Calculate: **{a_str} × {b}**",
        'hint_fr':          "Multiplie comme des entiers, puis place la virgule correctement.",
        'hint_en':          "Multiply as whole numbers, then place the decimal point correctly.",
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Ignore the decimal point and multiply as whole numbers: {q_scaled} × {b} = {product}.\n'
            f'Step 2: Count the decimal places in {a_str} = {dec_places} decimal place(s).\n'
            f'Step 3: Place the decimal point {dec_places} place(s) from the right.\n'
            f'Answer: {a_str} × {b} = {correct_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Ignore la virgule et multiplie comme des entiers : {q_scaled} × {b} = {product}.\n'
            f'Étape 2 : Compte les décimales dans {a_str} = {dec_places} décimale(s).\n'
            f'Étape 3 : Place la virgule à {dec_places} position(s) depuis la droite.\n'
            f'Réponse : {a_str} × {b} = {correct_str}'
        ),
        'correct_answers':  [correct_str, correct_dot],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_decimal_div_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_decimal_div_gen(level='easy'):
    """Typed — decimal ÷ natural (divisor ≤ 10)."""
    if level == 'easy':
        result = _make_decimal_div([2, 4, 5], 1, 9, 1)
        # But dividend is now a decimal: a = result * b (decimal)
        # Reuse same helper but now a is the decimal, result is simpler
    elif level == 'medium':
        result = _make_decimal_div([2, 4, 5, 8], 5, 30, 2)
    else:
        result = _make_decimal_div([2, 4, 5, 8, 10], 10, 99, 3)

    if result is None:
        result = (35, 4, '8,75')

    # result = (a_int, b, q_str) means a_int ÷ b = q_str
    # For decimal division: dividend = decimal, result = simpler decimal
    # We invert: dividend = q_str (decimal), divisor = b, result = a/b...
    # Actually let's use a different construction: dividend = q*b (decimal), divisor = b, result = q
    a_int, b, q_str = result
    dec_places = len(q_str.split(',')[1]) if ',' in q_str else 0

    # Make the dividend a decimal by dividing a_int by 10
    dividend_scaled = a_int * 10
    q_bigger_str = _fmt_decimal(dividend_scaled / 10 / b, dec_places + 1)
    # Simplify: just use a_int/b=q and say the dividend is the decimal form of a_int
    # dividend = decimal number, e.g. 7.5, b=5, result=1.5
    q_val = a_int / b
    dividend_str = _fmt_decimal(a_int / 10, 1)   # e.g., 7,5
    result_str   = _fmt_decimal(q_val / 10, dec_places + 1).rstrip('0').rstrip(',')
    result_dot   = result_str.replace(',', '.')

    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Calcule : **{dividend_str} ÷ {b}**",
        'prompt_en':        f"Calculate: **{dividend_str} ÷ {b}**",
        'hint_fr':          "Garde la virgule alignée pendant la division.",
        'hint_en':          "Keep the decimal point aligned during the division.",
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Set up {dividend_str} ÷ {b}.\n'
            f'Step 2: Place the decimal point in the quotient directly above the decimal in the dividend.\n'
            f'Step 3: Divide digit by digit, keeping the decimal aligned.\n'
            f'Answer: {dividend_str} ÷ {b} = {result_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Pose la division {dividend_str} ÷ {b}.\n'
            f'Étape 2 : Place la virgule dans le quotient directement au-dessus de celle du dividende.\n'
            f'Étape 3 : Divise chiffre par chiffre en gardant la virgule alignée.\n'
            f'Réponse : {dividend_str} ÷ {b} = {result_str}'
        ),
        'correct_answers':  [result_str, result_dot],
    }
