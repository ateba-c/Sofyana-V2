import random
from fractions import Fraction
from .base import _frac_str, _shuffle_mc, _tagged_shuffle_mc

# ── level denominator pools ───────────────────────────────────────────────────

_EASY_DENS   = [2, 3, 4, 5, 6]
_MEDIUM_DENS = [2, 3, 4, 5, 6, 8, 10]
_HARD_DENS   = [3, 4, 5, 6, 7, 8, 9, 10, 12]

_DENS = {
    'easy':   _EASY_DENS,
    'medium': _MEDIUM_DENS,
    'hard':   _HARD_DENS,
}


def _rand_frac(dens, same_den=None, max_num=None):
    """Return (n, d) for a positive proper fraction."""
    d = same_den if same_den else random.choice(dens)
    max_n = max_num or (d - 1)
    n = random.randint(1, max(1, max_n))
    return n, d


def _frac_shape(n1, d1, op, n2, d2):
    return [{
        'type': 'fraction_expr',
        'op1': {'num': n1, 'den': d1},
        'operator': op,
        'op2': {'num': n2, 'den': d2},
        'result': {'num': '?', 'den': '?'},
        'format': 'operation',
    }]


def _build_two_fracs(level):
    """Return two Fraction objects (f1, f2) appropriate for the level."""
    dens = _DENS.get(level, _DENS['medium'])
    if level == 'easy':
        d = random.choice(dens)
        n1 = random.randint(1, d - 1)
        n2 = random.randint(1, d - 1)
        return Fraction(n1, d), Fraction(n2, d)
    else:
        d1 = random.choice(dens)
        d2 = random.choice(dens)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        return Fraction(n1, d1), Fraction(n2, d2)


def fraction_add_gen(level='medium'):
    f1, f2 = _build_two_fracs(level)
    result = f1 + f2
    rs = _frac_str(result.numerator, result.denominator)
    n1, d1 = f1.numerator, f1.denominator
    n2, d2 = f2.numerator, f2.denominator
    rn, rd = result.numerator, result.denominator

    tagged_candidates = [
        (
            _frac_str(n1 + n2, d1 + d2),
            'add_across',
            "Don't add the denominators! Find a common denominator first.",
            "N'additionne pas les dénominateurs ! Trouve d'abord un dénominateur commun.",
        ),
        (
            _frac_str(n1 + n2, d1),
            'denominator_confusion',
            "You kept the wrong denominator — find the least common denominator.",
            "Tu as gardé le mauvais dénominateur — trouve le plus petit commun multiple.",
        ),
        (
            _frac_str(rn + 1, rd),
            'off_by_one',
            "Very close — check your numerator arithmetic.",
            "Très proche — vérifie ton calcul sur le numérateur.",
        ),
        (
            _frac_str(abs(rn - 1), rd),
            'off_by_one',
            "Very close — check your numerator arithmetic.",
            "Très proche — vérifie ton calcul sur le numérateur.",
        ),
        (
            str(n1 + n2),
            'wrong_operation',
            "You forgot the fractions and just added the numerators!",
            "Tu as oublié les fractions et n'as additionné que les numérateurs !",
        ),
    ]
    choices = _tagged_shuffle_mc(rs, tagged_candidates)
    a_s = _frac_str(n1, d1)
    b_s = _frac_str(n2, d2)
    return {
        'q_type':         'multiple_choice',
        'prompt_en':      f'Calculate: {a_s} + {b_s}',
        'prompt_fr':      f'Calculez : {a_s} + {b_s}',
        'hint_en':        'Find a common denominator first, then add the numerators.',
        'hint_fr':        'Trouvez un dénominateur commun, puis additionnez les numérateurs.',
        'shape_data':     _frac_shape(n1, d1, '+', n2, d2),
        'choices':        choices,
        'correct_answers': [rs],
        'time_limit':     45,
        'points':         2,
        'explanation_en': (
            f'Step 1: Find a common denominator for {d1} and {d2}.\n'
            f'Step 2: Convert both fractions: {a_s} and {b_s} → same denominator.\n'
            f'Step 3: Add the numerators, keep the denominator, then simplify.\n'
            f'Answer: {a_s} + {b_s} = {rs}'
        ),
        'explanation_fr': (
            f'Étape 1 : Trouve un dénominateur commun pour {d1} et {d2}.\n'
            f'Étape 2 : Convertis les deux fractions : {a_s} et {b_s} → même dénominateur.\n'
            f'Étape 3 : Additionne les numérateurs, garde le dénominateur, puis simplifie.\n'
            f'Réponse : {a_s} + {b_s} = {rs}'
        ),
    }


def fraction_subtract_gen(level='medium'):
    # Ensure f1 > f2 strictly so result > 0
    for _ in range(50):
        f1, f2 = _build_two_fracs(level)
        if f1 > f2:
            break
    else:
        # Fallback: force f1 > f2 with same denominator
        dens = _DENS.get(level, _DENS['medium'])
        d  = random.choice(dens)
        n2 = random.randint(1, d - 1)
        n1 = random.randint(n2 + 1, d)
        f1, f2 = Fraction(n1, d), Fraction(n2, d)
    result = f1 - f2
    rs = _frac_str(result.numerator, result.denominator)
    n1, d1 = f1.numerator, f1.denominator
    n2, d2 = f2.numerator, f2.denominator
    rn, rd = result.numerator, result.denominator

    tagged_candidates = [
        (
            _frac_str(abs(n1 - n2), d1 + d2),
            'add_across',
            "Don't add the denominators! Find a common denominator first.",
            "N'additionne pas les dénominateurs ! Trouve d'abord un dénominateur commun.",
        ),
        (
            _frac_str(abs(n1 - n2), d1),
            'denominator_confusion',
            "You kept the wrong denominator — find the least common denominator.",
            "Tu as gardé le mauvais dénominateur — trouve le plus petit commun multiple.",
        ),
        (
            _frac_str(rn + 1, rd),
            'off_by_one',
            "Very close — check your numerator arithmetic.",
            "Très proche — vérifie ton calcul sur le numérateur.",
        ),
        (
            _frac_str(abs(rn - 1), rd),
            'off_by_one',
            "Very close — check your numerator arithmetic.",
            "Très proche — vérifie ton calcul sur le numérateur.",
        ),
        (
            str(n1 + n2),
            'wrong_operation',
            "You forgot the fractions and just added the numerators!",
            "Tu as oublié les fractions et n'as additionné que les numérateurs !",
        ),
    ]
    choices = _tagged_shuffle_mc(rs, tagged_candidates)
    a_s = _frac_str(n1, d1)
    b_s = _frac_str(n2, d2)
    return {
        'q_type':         'multiple_choice',
        'prompt_en':      f'Calculate: {a_s} − {b_s}',
        'prompt_fr':      f'Calculez : {a_s} − {b_s}',
        'hint_en':        'Find a common denominator, then subtract the numerators.',
        'hint_fr':        'Trouvez un dénominateur commun, puis soustrayez les numérateurs.',
        'shape_data':     _frac_shape(n1, d1, '−', n2, d2),
        'choices':        choices,
        'correct_answers': [rs],
        'time_limit':     45,
        'points':         2,
        'explanation_en': (
            f'Step 1: Find a common denominator for {d1} and {d2}.\n'
            f'Step 2: Convert both fractions to the same denominator.\n'
            f'Step 3: Subtract the numerators, keep the denominator, then simplify.\n'
            f'Answer: {a_s} − {b_s} = {rs}'
        ),
        'explanation_fr': (
            f'Étape 1 : Trouve un dénominateur commun pour {d1} et {d2}.\n'
            f'Étape 2 : Convertis les deux fractions au même dénominateur.\n'
            f'Étape 3 : Soustrait les numérateurs, garde le dénominateur, puis simplifie.\n'
            f'Réponse : {a_s} − {b_s} = {rs}'
        ),
    }


def fraction_multiply_gen(level='medium'):
    f1, f2 = _build_two_fracs(level)
    result = f1 * f2
    rs = _frac_str(result.numerator, result.denominator)
    n1, d1 = f1.numerator, f1.denominator
    n2, d2 = f2.numerator, f2.denominator

    tagged_candidates = [
        (
            _frac_str(n1 + n2, d1 + d2),
            'add_across',
            "For multiplication, multiply tops and bottoms — don't add!",
            "Pour la multiplication, multiplie numérateur et dénominateur — ne les additionne pas !",
        ),
        (
            _frac_str(n1 + n2, d1 * d2),
            'numerator_confusion',
            "You added the numerators but should have multiplied them.",
            "Tu as additionné les numérateurs, mais tu aurais dû les multiplier.",
        ),
        (
            _frac_str(n1 * n2, d1 + d2),
            'denominator_confusion',
            "You added the denominators — multiply them instead!",
            "Tu as additionné les dénominateurs — multiplie-les !",
        ),
        (
            _frac_str(n1 * n2 + 1, d1 * d2),
            'off_by_one',
            "Almost right — check your numerator multiplication.",
            "Presque juste — vérifie la multiplication du numérateur.",
        ),
        (
            _frac_str(n1 * d2, d1 * n2),
            'forgot_flip',
            "That's the division result — don't flip for multiplication!",
            "C'est le résultat de la division — ne retourne pas pour la multiplication !",
        ),
        (
            str(n1 * n2),
            'denominator_confusion',
            "You multiplied the numerators but forgot the denominators!",
            "Tu as multiplié les numérateurs mais tu as oublié les dénominateurs !",
        ),
    ]
    choices = _tagged_shuffle_mc(rs, tagged_candidates)
    a_s = _frac_str(n1, d1)
    b_s = _frac_str(n2, d2)
    return {
        'q_type':         'multiple_choice',
        'prompt_en':      f'Calculate: {a_s} × {b_s}',
        'prompt_fr':      f'Calculez : {a_s} × {b_s}',
        'hint_en':        'Multiply numerators together and denominators together.',
        'hint_fr':        'Multipliez les numérateurs entre eux et les dénominateurs entre eux.',
        'shape_data':     _frac_shape(n1, d1, '×', n2, d2),
        'choices':        choices,
        'correct_answers': [rs],
        'time_limit':     45,
        'points':         2,
        'explanation_en': (
            f'Step 1: Multiply the numerators: {n1} × {n2} = {n1 * n2}.\n'
            f'Step 2: Multiply the denominators: {d1} × {d2} = {d1 * d2}.\n'
            f'Step 3: Simplify the result if possible.\n'
            f'Answer: {a_s} × {b_s} = {rs}'
        ),
        'explanation_fr': (
            f'Étape 1 : Multiplie les numérateurs : {n1} × {n2} = {n1 * n2}.\n'
            f'Étape 2 : Multiplie les dénominateurs : {d1} × {d2} = {d1 * d2}.\n'
            f'Étape 3 : Simplifie le résultat si possible.\n'
            f'Réponse : {a_s} × {b_s} = {rs}'
        ),
    }


def fraction_divide_gen(level='medium'):
    f1, f2 = _build_two_fracs(level)
    result = f1 / f2
    rs = _frac_str(result.numerator, result.denominator)
    n1, d1 = f1.numerator, f1.denominator
    n2, d2 = f2.numerator, f2.denominator
    # "forgot to flip" mistake = f1 * f2
    no_flip = f1 * f2

    tagged_candidates = [
        (
            _frac_str(no_flip.numerator, no_flip.denominator),
            'forgot_flip',
            "You forgot to flip the second fraction! Division = multiply by reciprocal.",
            "Tu as oublié d'inverser la deuxième fraction ! Division = multiplier par l'inverse.",
        ),
        (
            _frac_str(n1 * n2, d1 * d2),
            'wrong_operation',
            "You multiplied instead of dividing.",
            "Tu as multiplié au lieu de diviser.",
        ),
        (
            _frac_str(result.numerator + 1, result.denominator),
            'off_by_one',
            "Very close — check your simplification.",
            "Très proche — vérifie ta simplification.",
        ),
        (
            _frac_str(n1, n2),
            'denominator_confusion',
            "You used the numerators as a fraction — remember to use the reciprocal.",
            "Tu as utilisé les numérateurs comme fraction — souviens-toi de l'inverse.",
        ),
        (
            _frac_str(d1, d2),
            'denominator_confusion',
            "You used the denominators as a fraction — remember to use the reciprocal.",
            "Tu as utilisé les dénominateurs comme fraction — souviens-toi de l'inverse.",
        ),
    ]
    choices = _tagged_shuffle_mc(rs, tagged_candidates)
    a_s = _frac_str(n1, d1)
    b_s = _frac_str(n2, d2)
    return {
        'q_type':         'multiple_choice',
        'prompt_en':      f'Calculate: {a_s} ÷ {b_s}',
        'prompt_fr':      f'Calculez : {a_s} ÷ {b_s}',
        'hint_en':        'Multiply by the reciprocal: flip the second fraction, then multiply.',
        'hint_fr':        "Multipliez par l'inverse : retournez la deuxième fraction, puis multipliez.",
        'shape_data':     _frac_shape(n1, d1, '÷', n2, d2),
        'choices':        choices,
        'correct_answers': [rs],
        'time_limit':     60,
        'points':         3,
        'explanation_en': (
            f'Step 1: Flip the second fraction (its reciprocal): {b_s} → {_frac_str(d2, n2)}.\n'
            f'Step 2: Change division to multiplication: {a_s} × {_frac_str(d2, n2)}.\n'
            f'Step 3: Multiply numerators ({n1} × {d2}) and denominators ({d1} × {n2}), then simplify.\n'
            f'Answer: {a_s} ÷ {b_s} = {rs}'
        ),
        'explanation_fr': (
            f'Étape 1 : Inverse la deuxième fraction : {b_s} → {_frac_str(d2, n2)}.\n'
            f'Étape 2 : Change la division en multiplication : {a_s} × {_frac_str(d2, n2)}.\n'
            f'Étape 3 : Multiplie les numérateurs ({n1} × {d2}) et les dénominateurs ({d1} × {n2}), puis simplifie.\n'
            f'Réponse : {a_s} ÷ {b_s} = {rs}'
        ),
    }


# ── fraction_shape_gen ────────────────────────────────────────────────────────

def fraction_shape_gen(level='medium'):
    """
    QCM + SVG -- given a fraction bar or circle with some parts coloured,
    identify the fraction shown.

    Difficulty controls denominator range and distractor closeness:
      easy   -> denominator 2-4, clear shape
      medium -> denominator 3-6
      hard   -> denominator 4-8
    """
    import random
    from quiz.generators.base import _tagged_shuffle_mc, _frac_str

    if level == 'easy':
        denominator = random.randint(2, 4)
    elif level == 'medium':
        denominator = random.randint(3, 6)
    else:
        denominator = random.randint(4, 8)

    numerator = random.randint(1, denominator)
    shape_kind = random.choice(['fraction_bar', 'fraction_circle'])
    correct = _frac_str(numerator, denominator)

    # Distractors
    def _d(n, d):
        if d < 1 or n < 0 or n > d:
            return None
        return _frac_str(n, d)

    candidates = []
    # Invert numerator/denominator
    inv = _d(denominator, numerator) if numerator != denominator else None
    if inv and inv != correct:
        candidates.append((inv, 'num_den_swap',
                           'The denominator = total parts; numerator = coloured parts.',
                           'Le denominateur = total de parts; numerateur = parts coloriees.'))
    # Off by one numerator
    for delta in [1, -1]:
        v = _d(numerator + delta, denominator)
        if v and v != correct:
            candidates.append((v, 'off_by_one',
                                'Count the coloured parts again.',
                                'Recompte les parts coloriees.'))
    # Different denominator (same numerator)
    v = _d(numerator, denominator + 1) if denominator < 8 else _d(numerator, denominator - 1)
    if v and v != correct:
        candidates.append((v, 'wrong_denominator',
                           'Count all parts (coloured + uncoloured).',
                           'Compte toutes les parts (coloriees + non coloriees).'))
    # Complement
    comp = _d(denominator - numerator, denominator)
    if comp and comp != correct:
        candidates.append((comp, 'complement_error',
                           'You counted the uncoloured parts instead.',
                           'Tu as compte les parts non coloriees.'))

    choices = _tagged_shuffle_mc(correct, candidates)

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': 'Quelle fraction de la figure est coloriee ?',
        'prompt_en': 'What fraction of the figure is coloured?',
        'hint_fr': 'Numerateur = parts coloriees. Denominateur = nombre total de parts.',
        'hint_en': 'Numerator = coloured parts. Denominator = total number of parts.',
        'shape_data': [{'type': shape_kind,
                        'numerator': numerator,
                        'denominator': denominator}],
        'show_illustration': True,
        'choices': choices,
        'correct_answers': [correct],
        'time_limit': 25, 'points': 1,
        'explanation_fr': (
            f'{numerator} part(s) coloriee(s) sur {denominator} en tout '
            f'-> fraction = {correct}'
        ),
        'explanation_en': (
            f'{numerator} coloured part(s) out of {denominator} total '
            f'-> fraction = {correct}'
        ),
    }
