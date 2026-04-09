import random
from .base import _shuffle_mc, _tagged_shuffle_mc, _unique

# ── level ranges ─────────────────────────────────────────────────────────────

_INT_RANGES = {
    'easy':   (1,   20),
    'medium': (10,  500),
    'hard':   (100, 4999),
}

_DEC_PLACES = {
    'easy':   1,
    'medium': 1,
    'hard':   2,
}


def _fmt(fmt, a, b, op, result='?'):
    return [{'type': 'expression', 'op1': str(a), 'operator': op,
             'op2': str(b), 'result': str(result), 'format': fmt}]


def _expr_shape(a, b, op, level):
    fmt = 'vertical' if level in ('medium', 'hard') else 'horizontal'
    return _fmt(fmt, a, b, op)


# ── integer generators ────────────────────────────────────────────────────────

def add_gen(level='medium'):
    lo, hi = _INT_RANGES.get(level, _INT_RANGES['medium'])
    a = random.randint(lo, hi)
    b = random.randint(lo, hi)
    result = a + b
    choices = _tagged_shuffle_mc(str(result), [
        (str(result - 1), 'off_by_one', 'Very close! Check your carrying.', 'Très proche ! Vérifie ta retenue.'),
        (str(result + 1), 'off_by_one', 'Very close! Check your carrying.', 'Très proche ! Vérifie ta retenue.'),
        (str(result - 10), 'place_value', 'Watch out for place values when carrying tens.', 'Attention aux valeurs de position lors du report des dizaines.'),
        (str(result + 10), 'place_value', 'Watch out for place values when carrying tens.', 'Attention aux valeurs de position lors du report des dizaines.'),
        (str(a - b if a >= b else b - a), 'wrong_operation', 'You subtracted instead of adding!', "Tu as soustrait au lieu d'additionner !"),
        (str(a % 10 + b % 10), 'digit_error', "You added just the units digits — don't forget the rest!", "Tu n'as additionné que les unités — n'oublie pas le reste !"),
        (str(result + 100), 'place_value', "Check your place values — you're off by 100.", 'Vérifie tes valeurs de position — tu t\'es trompé(e) de 100.'),
    ])
    return {
        'q_type':        'multiple_choice',
        'prompt_en':     f'What is {a} + {b}?',
        'prompt_fr':     f'Combien font {a} + {b} ?',
        'hint_en':       f'Add {a} and {b} together.',
        'hint_fr':       f'Additionnez {a} et {b}.',
        'shape_data':    _expr_shape(a, b, '+', level),
        'choices':       choices,
        'correct_answers': [str(result)],
        'time_limit':    30,
        'points':        1,
        'explanation_en': (
            f'Step 1: Write the numbers one above the other, lining up place values.\n'
            f'Step 2: Add each column from right to left, carrying when needed.\n'
            f'Answer: {a} + {b} = {result}'
        ),
        'explanation_fr': (
            f'Étape 1 : Écris les nombres l\'un au-dessus de l\'autre en alignant les rangs.\n'
            f'Étape 2 : Additionne chaque colonne de droite à gauche, en retenant si nécessaire.\n'
            f'Réponse : {a} + {b} = {result}'
        ),
    }


def subtract_gen(level='medium'):
    lo, hi = _INT_RANGES.get(level, _INT_RANGES['medium'])
    # Build result > 0 directly, then derive a and b
    result = random.randint(1, hi - lo)
    b      = random.randint(lo, hi - result)
    a      = result + b
    choices = _tagged_shuffle_mc(str(result), [
        (str(result + 1), 'off_by_one', 'Very close! Check your borrowing.', 'Très proche ! Vérifie ton emprunt.'),
        (str(result + 10), 'place_value', 'Watch out for place values when borrowing tens.', 'Attention aux valeurs de position lors de l\'emprunt des dizaines.'),
        (str(result + 100), 'place_value', "Check your place values — you're off by 100.", 'Vérifie tes valeurs de position — tu t\'es trompé(e) de 100.'),
        (str(a + b), 'wrong_operation', 'You added instead of subtracting!', 'Tu as additionné au lieu de soustraire !'),
        (str(b), 'wrong_operation', 'You used the subtracted number instead of the result!', 'Tu as utilisé le nombre soustrait au lieu du résultat !'),
        (str(a), 'wrong_operation', 'You used the starting number instead of computing the difference!', 'Tu as utilisé le nombre de départ au lieu de calculer la différence !'),
    ])
    return {
        'q_type':        'multiple_choice',
        'prompt_en':     f'What is {a} − {b}?',
        'prompt_fr':     f'Combien font {a} − {b} ?',
        'hint_en':       f'Subtract {b} from {a}.',
        'hint_fr':       f'Soustrayez {b} de {a}.',
        'shape_data':    _expr_shape(a, b, '−', level),
        'choices':       choices,
        'correct_answers': [str(result)],
        'time_limit':    30,
        'points':        1,
        'explanation_en': (
            f'Step 1: Write {a} − {b}, aligning place values.\n'
            f'Step 2: Subtract each column from right to left, borrowing when needed.\n'
            f'Answer: {a} − {b} = {result}'
        ),
        'explanation_fr': (
            f'Étape 1 : Écris {a} − {b} en alignant les rangs.\n'
            f'Étape 2 : Soustrait chaque colonne de droite à gauche, en empruntant si nécessaire.\n'
            f'Réponse : {a} − {b} = {result}'
        ),
    }


def multiply_gen(level='medium'):
    lo, hi = _INT_RANGES.get(level, _INT_RANGES['medium'])
    if level == 'easy':
        a = random.randint(1, 12)
        b = random.randint(1, 12)
    elif level == 'medium':
        a = random.randint(10, 99)
        b = random.randint(2, 20)
    else:
        a = random.randint(100, 999)
        b = random.randint(2, 99)
    result = a * b
    choices = _tagged_shuffle_mc(str(result), [
        (str(result + a), 'partial_product', f"You're one group of {b} off.", f'Tu as un groupe de {b} de trop ou de moins.'),
        (str(result - b), 'partial_product', f"You're one group of {b} off.", f'Tu as un groupe de {b} de trop ou de moins.'),
        (str(a + b), 'wrong_operation', 'You added instead of multiplying!', 'Tu as additionné au lieu de multiplier !'),
        (str(a * (b + 1)), 'factor_error', 'Check your factor — off by 1.', 'Vérifie ton facteur — décalé de 1.'),
        (str(a * (b - 1)), 'factor_error', 'Check your factor — off by 1.', 'Vérifie ton facteur — décalé de 1.'),
        (str(result + 10), 'off_by_ten', 'Watch out for place values in your partial products.', 'Attention aux valeurs de position dans tes produits partiels.'),
        (str(result - 10), 'off_by_ten', 'Watch out for place values in your partial products.', 'Attention aux valeurs de position dans tes produits partiels.'),
    ])
    return {
        'q_type':        'multiple_choice',
        'prompt_en':     f'What is {a} × {b}?',
        'prompt_fr':     f'Combien font {a} × {b} ?',
        'hint_en':       f'Multiply {a} by {b}.',
        'hint_fr':       f'Multipliez {a} par {b}.',
        'shape_data':    _expr_shape(a, b, '×', level),
        'choices':       choices,
        'correct_answers': [str(result)],
        'time_limit':    45,
        'points':        2,
        'explanation_en': (
            f'Step 1: Multiply {a} × {b}.\n'
            f'Step 2: Multiply the ones digit of {b} by {a}, then the tens digit, shifting left each time.\n'
            f'Step 3: Add the partial products.\n'
            f'Answer: {a} × {b} = {result}'
        ),
        'explanation_fr': (
            f'Étape 1 : Multiplie {a} × {b}.\n'
            f'Étape 2 : Multiplie le chiffre des unités de {b} par {a}, puis les dizaines, en décalant à gauche.\n'
            f'Étape 3 : Additionne les produits partiels.\n'
            f'Réponse : {a} × {b} = {result}'
        ),
    }


def divide_gen(level='medium'):
    if level == 'easy':
        b = random.randint(1, 12)
        q = random.randint(1, 12)
    elif level == 'medium':
        b = random.randint(2, 25)
        q = random.randint(2, 50)
    else:
        b = random.randint(2, 99)
        q = random.randint(2, 200)
    a = q * b
    result = q
    choices = _tagged_shuffle_mc(str(result), [
        (str(q + 1), 'quotient_error', f'Very close! Check how many times {b} fits into {a}.', f'Très proche ! Vérifie combien de fois {b} entre dans {a}.'),
        (str(q - 1), 'quotient_error', f'Very close! Check how many times {b} fits into {a}.', f'Très proche ! Vérifie combien de fois {b} entre dans {a}.'),
        (str(b), 'wrong_operation', 'You returned the divisor instead of the quotient!', 'Tu as retourné le diviseur au lieu du quotient !'),
        (str(a - q), 'wrong_operation', 'You subtracted instead of dividing!', 'Tu as soustrait au lieu de diviser !'),
        (str(a // (b + 1)), 'quotient_error', f'Very close! Check how many times {b} fits into {a}.', f'Très proche ! Vérifie combien de fois {b} entre dans {a}.'),
        (str(q + 10), 'off_by_ten', 'Check your long division — you may have a place value error.', 'Vérifie ta division — tu as peut-être une erreur de valeur de position.'),
        (str(q - 10), 'off_by_ten', 'Check your long division — you may have a place value error.', 'Vérifie ta division — tu as peut-être une erreur de valeur de position.'),
    ])
    return {
        'q_type':        'multiple_choice',
        'prompt_en':     f'What is {a} ÷ {b}?',
        'prompt_fr':     f'Combien font {a} ÷ {b} ?',
        'hint_en':       f'How many times does {b} go into {a}?',
        'hint_fr':       f'Combien de fois {b} entre dans {a} ?',
        'shape_data':    _expr_shape(a, b, '÷', level),
        'choices':       choices,
        'correct_answers': [str(result)],
        'time_limit':    45,
        'points':        2,
        'explanation_en': (
            f'Step 1: Ask — how many times does {b} fit into {a}?\n'
            f'Step 2: Check: {b} × {result} = {a} ✓\n'
            f'Answer: {a} ÷ {b} = {result}'
        ),
        'explanation_fr': (
            f'Étape 1 : Combien de fois {b} entre dans {a} ?\n'
            f'Étape 2 : Vérification : {b} × {result} = {a} ✓\n'
            f'Réponse : {a} ÷ {b} = {result}'
        ),
    }


# ── decimal helpers ───────────────────────────────────────────────────────────

def _dec_rand(lo, hi, places):
    factor = 10 ** places
    return random.randint(int(lo * factor), int(hi * factor)) / factor


def _dec_fmt(val, places):
    return f'{val:.{places}f}'


def decimal_add_gen(level='medium'):
    places = _DEC_PLACES.get(level, 1)
    lo, hi = (0.1, 9.9) if level == 'easy' else (0.1, 99.9)
    a = _dec_rand(lo, hi, places)
    b = _dec_rand(lo, hi, places)
    result = round(a + b, places)
    a_s, b_s, r_s = _dec_fmt(a, places), _dec_fmt(b, places), _dec_fmt(result, places)
    r = result
    choices = _tagged_shuffle_mc(r_s, [
        (_dec_fmt(r * 10, places), 'decimal_shift', 'Moved the decimal point the wrong way.', 'Tu as déplacé la virgule dans le mauvais sens.'),
        (_dec_fmt(r / 10, places + 1), 'decimal_shift', 'Moved the decimal point the wrong way.', 'Tu as déplacé la virgule dans le mauvais sens.'),
        (_dec_fmt(round(r + 1, places), places), 'off_by_one', 'Very close! Check your carrying with decimals.', 'Très proche ! Vérifie ta retenue avec les décimales.'),
        (_dec_fmt(round(r - 1, places), places), 'off_by_one', 'Very close! Check your carrying with decimals.', 'Très proche ! Vérifie ta retenue avec les décimales.'),
        (_dec_fmt(round(r + 0.1, places), places), 'digit_error', 'Check the tenths column — you may be off by one tenth.', 'Vérifie la colonne des dixièmes — tu t\'es peut-être trompé(e) d\'un dixième.'),
        (_dec_fmt(round(r - 0.1, places), places), 'digit_error', 'Check the tenths column — you may be off by one tenth.', 'Vérifie la colonne des dixièmes — tu t\'es peut-être trompé(e) d\'un dixième.'),
    ])
    return {
        'q_type':        'multiple_choice',
        'prompt_en':     f'What is {a_s} + {b_s}?',
        'prompt_fr':     f'Combien font {a_s} + {b_s} ?',
        'hint_en':       'Line up the decimal points when adding.',
        'hint_fr':       "Alignez les virgules d\u00e9cimales lors de l\u2019addition.",
        'shape_data':    [{'type': 'expression', 'op1': a_s, 'operator': '+',
                           'op2': b_s, 'result': '?', 'format': 'horizontal'}],
        'choices':       choices,
        'correct_answers': [r_s],
        'time_limit':    30,
        'points':        1,
        'explanation_en': (
            f'Step 1: Line up the decimal points: {a_s} and {b_s}.\n'
            f'Step 2: Add each column from right to left.\n'
            f'Answer: {a_s} + {b_s} = {r_s}'
        ),
        'explanation_fr': (
            f'Étape 1 : Aligne les virgules : {a_s} et {b_s}.\n'
            f'Étape 2 : Additionne chaque colonne de droite à gauche.\n'
            f'Réponse : {a_s} + {b_s} = {r_s}'
        ),
    }


def decimal_subtract_gen(level='medium'):
    places = _DEC_PLACES.get(level, 1)
    lo, hi = (0.1, 9.9) if level == 'easy' else (0.1, 99.9)
    # Build result > 0 directly, then derive a and b
    result = _dec_rand(lo, hi * 0.4, places)
    b      = _dec_rand(lo, hi * 0.5, places)
    a      = round(result + b, places)
    r_s = _dec_fmt(result, places)
    a_s, b_s = _dec_fmt(a, places), _dec_fmt(b, places)
    r = result
    choices = _tagged_shuffle_mc(r_s, [
        (_dec_fmt(r * 10, places), 'decimal_shift', 'Moved the decimal point the wrong way.', 'Tu as déplacé la virgule dans le mauvais sens.'),
        (_dec_fmt(r / 10, places + 1), 'decimal_shift', 'Moved the decimal point the wrong way.', 'Tu as déplacé la virgule dans le mauvais sens.'),
        (_dec_fmt(round(r + 1, places), places), 'off_by_one', 'Very close! Check your borrowing with decimals.', 'Très proche ! Vérifie ton emprunt avec les décimales.'),
        (_dec_fmt(round(r - 1, places), places), 'off_by_one', 'Very close! Check your borrowing with decimals.', 'Très proche ! Vérifie ton emprunt avec les décimales.'),
        (_dec_fmt(round(r + 0.1, places), places), 'digit_error', 'Check the tenths column — you may be off by one tenth.', 'Vérifie la colonne des dixièmes — tu t\'es peut-être trompé(e) d\'un dixième.'),
        (_dec_fmt(round(r - 0.1, places), places), 'digit_error', 'Check the tenths column — you may be off by one tenth.', 'Vérifie la colonne des dixièmes — tu t\'es peut-être trompé(e) d\'un dixième.'),
    ])
    return {
        'q_type':        'multiple_choice',
        'prompt_en':     f'What is {a_s} − {b_s}?',
        'prompt_fr':     f'Combien font {a_s} − {b_s} ?',
        'hint_en':       'Line up the decimal points when subtracting.',
        'hint_fr':       'Alignez les virgules décimales lors de la soustraction.',
        'shape_data':    [{'type': 'expression', 'op1': a_s, 'operator': '−',
                           'op2': b_s, 'result': '?', 'format': 'horizontal'}],
        'choices':       choices,
        'correct_answers': [r_s],
        'time_limit':    30,
        'points':        1,
        'explanation_en': (
            f'Step 1: Line up the decimal points: {a_s} − {b_s}.\n'
            f'Step 2: Subtract each column from right to left, borrowing when needed.\n'
            f'Answer: {a_s} − {b_s} = {r_s}'
        ),
        'explanation_fr': (
            f'Étape 1 : Aligne les virgules : {a_s} − {b_s}.\n'
            f'Étape 2 : Soustrait de droite à gauche, en empruntant si nécessaire.\n'
            f'Réponse : {a_s} − {b_s} = {r_s}'
        ),
    }


def decimal_multiply_gen(level='medium'):
    places = _DEC_PLACES.get(level, 1)
    if level == 'easy':
        a = _dec_rand(1.0, 9.9, 1)
        b = random.randint(2, 9)
    elif level == 'medium':
        a = _dec_rand(1.0, 99.9, 1)
        b = random.randint(2, 20)
    else:
        a = _dec_rand(1.0, 99.9, 2)
        b = _dec_rand(1.0, 9.9, 1)
    result = round(a * b, places + 1)
    a_s = _dec_fmt(a, places)
    b_s = str(b) if isinstance(b, int) else _dec_fmt(b, 1)
    r_s = f'{result:g}'
    r = result
    choices = _tagged_shuffle_mc(r_s, [
        (_dec_fmt(r * 10, places), 'decimal_shift', 'Moved the decimal point the wrong way.', 'Tu as déplacé la virgule dans le mauvais sens.'),
        (_dec_fmt(r / 10, places + 1), 'decimal_shift', 'Moved the decimal point the wrong way.', 'Tu as déplacé la virgule dans le mauvais sens.'),
        (_dec_fmt(round(r + 1, places), places), 'off_by_one', 'Very close! Check your decimal placement.', 'Très proche ! Vérifie le placement de ta virgule.'),
        (_dec_fmt(round(r - 1, places), places), 'off_by_one', 'Very close! Check your decimal placement.', 'Très proche ! Vérifie le placement de ta virgule.'),
        (_dec_fmt(round(r + 0.1, places), places), 'digit_error', 'Check the tenths column — you may be off by one tenth.', 'Vérifie la colonne des dixièmes — tu t\'es peut-être trompé(e) d\'un dixième.'),
        (_dec_fmt(round(r - 0.1, places), places), 'digit_error', 'Check the tenths column — you may be off by one tenth.', 'Vérifie la colonne des dixièmes — tu t\'es peut-être trompé(e) d\'un dixième.'),
    ])
    return {
        'q_type':        'multiple_choice',
        'prompt_en':     f'What is {a_s} × {b_s}?',
        'prompt_fr':     f'Combien font {a_s} × {b_s} ?',
        'hint_en':       'Multiply as integers, then count total decimal places.',
        'hint_fr':       'Multipliez comme des entiers, puis comptez les décimales.',
        'shape_data':    [{'type': 'expression', 'op1': a_s, 'operator': '×',
                           'op2': b_s, 'result': '?', 'format': 'horizontal'}],
        'choices':       choices,
        'correct_answers': [r_s],
        'time_limit':    45,
        'points':        2,
        'explanation_en': (
            f'Step 1: Multiply as if whole numbers: ignore the decimal point first.\n'
            f'Step 2: Count total decimal places in {a_s} and {b_s}, then place the decimal in the result.\n'
            f'Answer: {a_s} × {b_s} = {r_s}'
        ),
        'explanation_fr': (
            f'Étape 1 : Multiplie comme des entiers — ignore la virgule d\'abord.\n'
            f'Étape 2 : Compte le total des décimales dans {a_s} et {b_s}, puis place la virgule dans le résultat.\n'
            f'Réponse : {a_s} × {b_s} = {r_s}'
        ),
    }


def decimal_divide_gen(level='medium'):
    places = _DEC_PLACES.get(level, 1)
    if level == 'easy':
        b = random.choice([2, 4, 5, 10])
        q = _dec_rand(1.0, 9.9, 1)
    elif level == 'medium':
        b = random.choice([2, 4, 5, 10, 20, 25])
        q = _dec_rand(1.0, 99.9, 1)
    else:
        b = random.choice([2, 4, 5, 8, 10, 25, 50])
        q = _dec_rand(1.0, 99.9, 2)
    a = round(q * b, places)
    result = q
    a_s = _dec_fmt(a, places)
    b_s = str(b)
    r_s = f'{result:g}'
    r = result
    choices = _tagged_shuffle_mc(r_s, [
        (_dec_fmt(r * 10, places), 'decimal_shift', 'Moved the decimal point the wrong way.', 'Tu as déplacé la virgule dans le mauvais sens.'),
        (_dec_fmt(r / 10, places + 1), 'decimal_shift', 'Moved the decimal point the wrong way.', 'Tu as déplacé la virgule dans le mauvais sens.'),
        (_dec_fmt(round(r + 1, places), places), 'off_by_one', 'Very close! Check your decimal placement.', 'Très proche ! Vérifie le placement de ta virgule.'),
        (_dec_fmt(round(r - 1, places), places), 'off_by_one', 'Very close! Check your decimal placement.', 'Très proche ! Vérifie le placement de ta virgule.'),
        (_dec_fmt(round(r + 0.1, places), places), 'digit_error', 'Check the tenths column — you may be off by one tenth.', 'Vérifie la colonne des dixièmes — tu t\'es peut-être trompé(e) d\'un dixième.'),
        (_dec_fmt(round(r - 0.1, places), places), 'digit_error', 'Check the tenths column — you may be off by one tenth.', 'Vérifie la colonne des dixièmes — tu t\'es peut-être trompé(e) d\'un dixième.'),
    ])
    return {
        'q_type':        'multiple_choice',
        'prompt_en':     f'What is {a_s} ÷ {b_s}?',
        'prompt_fr':     f'Combien font {a_s} ÷ {b_s} ?',
        'hint_en':       'Divide as integers, then adjust the decimal point.',
        'hint_fr':       'Divisez comme des entiers, puis ajustez la virgule décimale.',
        'shape_data':    [{'type': 'expression', 'op1': a_s, 'operator': '÷',
                           'op2': b_s, 'result': '?', 'format': 'horizontal'}],
        'choices':       choices,
        'correct_answers': [r_s],
        'time_limit':    45,
        'points':        2,
        'explanation_en': (
            f'Step 1: Divide as if whole numbers: {a_s} ÷ {b_s}.\n'
            f'Step 2: Adjust the decimal point — count the decimal places and shift accordingly.\n'
            f'Answer: {a_s} ÷ {b_s} = {r_s}'
        ),
        'explanation_fr': (
            f'Étape 1 : Divise comme des entiers : {a_s} ÷ {b_s}.\n'
            f'Étape 2 : Ajuste la virgule — compte les décimales et décale en conséquence.\n'
            f'Réponse : {a_s} ÷ {b_s} = {r_s}'
        ),
    }
