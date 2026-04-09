"""
word_problems.py — Grade-3 contextual / operation-sense generators.

Topics:
  word_problem_gen          QCM    – a + b − c in monster/candy context (T1_S6)
  multiply_context_gen      QCM    – identify multiplication in grouping context (T2_S12)
  repeated_addition_gen     mix_match – repeated addition ↔ multiplication (T2_S12)
  division_sharing_gen      QCM    – equal-sharing division context (T2_S12)
  choose_operation_gen      QCM    – which operation to use first (JR)
  read_decimal_gen          typed  – write a decimal in digits from French words (T2_S14)

Difficulty for numeric exercises:
  easy   → small numbers, one-step
  medium → medium numbers, two-step
  hard   → larger numbers, multi-step
"""

import random
from .base import _tagged_shuffle_mc

# ─── helper: decimal to French words ─────────────────────────────────────────

_INT_FR_ONES = [
    'zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept',
    'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze',
    'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf',
]
_INT_FR_TENS = {2: 'vingt', 3: 'trente', 4: 'quarante',
                5: 'cinquante', 6: 'soixante'}


def _int_to_fr(n: int) -> str:
    if n < 20:
        return _INT_FR_ONES[n]
    if n < 70:
        t, u = divmod(n, 10)
        tw = _INT_FR_TENS[t]
        if u == 0:
            return tw
        if u == 1:
            return f'{tw} et un'
        return f'{tw}-{_INT_FR_ONES[u]}'
    if n < 80:
        rem = n - 60
        return 'soixante et onze' if rem == 11 else f'soixante-{_INT_FR_ONES[rem]}'
    if n < 100:
        rem = n - 80
        return 'quatre-vingts' if rem == 0 else f'quatre-vingt-{_INT_FR_ONES[rem]}'
    if n < 200:
        rest = n - 100
        return 'cent' if rest == 0 else f'cent {_int_to_fr(rest)}'
    if n < 1000:
        c, rest = divmod(n, 100)
        return f'{_INT_FR_ONES[c]} cent{"s" if rest == 0 else ""}{" " + _int_to_fr(rest) if rest else ""}'
    if n < 2000:
        rest = n - 1000
        return 'mille' if rest == 0 else f'mille {_int_to_fr(rest)}'
    m, rest = divmod(n, 1000)
    m_word = _INT_FR_ONES[m] if m < len(_INT_FR_ONES) else str(m)
    return f'{m_word} mille' if rest == 0 else f'{m_word} mille {_int_to_fr(rest)}'


_DEC_PLACE_NAMES_FR = {1: 'dixième', 2: 'centième', 3: 'millième', 4: 'dix-millième'}
_DEC_PLACE_NAMES_EN = {1: 'tenth', 2: 'hundredth', 3: 'thousandth', 4: 'ten-thousandth'}


def _decimal_to_words(integer_part: int, decimal_str: str):
    """Return (fr_words, en_words) for integer_part.decimal_str."""
    places = len(decimal_str)
    dec_val = int(decimal_str)
    int_fr = _int_to_fr(integer_part)
    int_en = str(integer_part)  # simplified for English
    dec_fr = _int_to_fr(dec_val)
    place_fr = _DEC_PLACE_NAMES_FR.get(places, f'{places} décimales')
    place_en = _DEC_PLACE_NAMES_EN.get(places, f'{places} decimal places')
    # Pluralise French place name
    if dec_val > 1:
        place_fr += 's'
        place_en += 's'
    words_fr = f'{int_fr} virgule {dec_fr}' if dec_val else f'{int_fr}'
    words_en = f'{int_en} point {decimal_str}' if dec_val else f'{int_en}'
    return words_fr, words_en


# ─── 1. word_problem_gen ─────────────────────────────────────────────────────

def word_problem_gen(level: str = 'medium') -> dict:
    """
    QCM — monster / candy 2-3 step problem: a + b − c.
    Result must be non-negative.
    """
    if level == 'easy':
        a = random.randint(10, 50)
        b = random.randint(5, 30)
        c = random.randint(1, a + b)
    elif level == 'medium':
        a = random.randint(50, 300)
        b = random.randint(20, 200)
        c = random.randint(10, a + b)
    else:
        a = random.randint(200, 800)
        b = random.randint(100, 500)
        c = random.randint(50, a + b)

    result = a + b - c
    if result < 0:
        c = a + b  # ensure non-negative, result = 0

    result = a + b - c

    choices = _tagged_shuffle_mc(str(result), [
        (str(a + b + c),
         'wrong_operation',
         'You added all three — the last number should be subtracted.',
         'Tu as tout additionné — le dernier nombre doit être soustrait.'),
        (str(a - b - c if a - b - c > 0 else a + b),
         'wrong_operation',
         'Re-read the problem: first add, then subtract.',
         'Relis le problème : d\'abord additionne, puis soustrais.'),
        (str(a + b),
         'forgot_subtraction',
         'You forgot to give away the candies at the end.',
         'Tu as oublié de soustraire les bonbons donnés.'),
        (str(a - c if a >= c else a + c),
         'ignored_b',
         'Did you forget the candies won in the middle step?',
         'As-tu oublié les bonbons gagnés au milieu ?'),
    ])

    themes_fr = [
        (f'Un monstre a **{a}** bonbons. Il en gagne **{b}** puis en donne **{c}**. '
         f'Combien lui en reste-t-il ?'),
        (f'Une fée a **{a}** étoiles. Elle en trouve **{b}** de plus, puis en perd **{c}**. '
         f'Combien en a-t-elle maintenant ?'),
    ]
    themes_en = [
        (f'A monster has **{a}** candies. It wins **{b}** more, then gives away **{c}**. '
         f'How many does it have left?'),
        (f'A fairy has **{a}** stars. She finds **{b}** more, then loses **{c}**. '
         f'How many does she have now?'),
    ]
    idx = random.randint(0, len(themes_fr) - 1)

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': themes_fr[idx],
        'prompt_en': themes_en[idx],
        'hint_fr': 'Lis chaque étape : d\'abord additionne, puis soustrais.',
        'hint_en': 'Read each step: first add, then subtract.',
        'shape_data': [],
        'choices': choices,
        'correct_answers': [str(result)],
        'time_limit': 40,
        'points': 2,
        'explanation_fr': f'Étape 1 : {a} + {b} = {a + b}\nÉtape 2 : {a + b} − {c} = **{result}**',
        'explanation_en': f'Step 1: {a} + {b} = {a + b}\nStep 2: {a + b} − {c} = **{result}**',
    }


# ─── 2. multiply_context_gen ──────────────────────────────────────────────────

def multiply_context_gen(level: str = 'medium') -> dict:
    """
    QCM — g equal groups of k items: which operation represents the situation?
    Students pick the multiplication expression.
    """
    if level == 'easy':
        g = random.randint(2, 5)
        k = random.randint(2, 6)
    elif level == 'medium':
        g = random.randint(3, 10)
        k = random.randint(3, 10)
    else:
        g = random.randint(6, 12)
        k = random.randint(6, 12)

    correct = f'{g} × {k}'
    total = g * k

    choices = _tagged_shuffle_mc(correct, [
        (f'{g} + {k}',
         'add_instead_of_multiply',
         'Equal groups call for multiplication, not addition.',
         'Des groupes égaux s\'expriment par une multiplication, pas une addition.'),
        (f'{total} ÷ {g}',
         'wrong_operation',
         'Division undoes multiplication — here you multiply to find the total.',
         'La division défait la multiplication — ici tu cherches le total.'),
        (f'{g} − {k}',
         'wrong_operation',
         'There is no subtraction here: all groups are combined.',
         'Il n\'y a pas de soustraction : tous les groupes s\'accumulent.'),
        (f'{k} × {g + 1}',
         'off_by_one_group',
         'Count the number of groups again.',
         'Recompte le nombre de groupes.'),
    ])

    scenarios_fr = [
        f'Un pirate a **{g}** sacs. Chaque sac contient **{k}** pièces. '
        f'Quelle opération représente cette situation ?',
        f'Il y a **{g}** rangées de **{k}** coffres. '
        f'Quelle opération donne le nombre total de coffres ?',
    ]
    scenarios_en = [
        f'A pirate has **{g}** bags. Each bag contains **{k}** coins. '
        f'Which operation represents this situation?',
        f'There are **{g}** rows of **{k}** chests. '
        f'Which operation gives the total number of chests?',
    ]
    idx = random.randint(0, len(scenarios_fr) - 1)

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': scenarios_fr[idx],
        'prompt_en': scenarios_en[idx],
        'hint_fr': 'Quand on a plusieurs groupes identiques, on multiplie.',
        'hint_en': 'When you have several equal groups, you multiply.',
        'shape_data': [],
        'choices': choices,
        'correct_answers': [correct, f'{k} × {g}'],   # commutative
        'time_limit': 30,
        'points': 1,
        'explanation_fr': (
            f'{g} groupes de {k} → {g} × {k} = {total}.\n'
            f'La multiplication représente des groupes égaux.'
        ),
        'explanation_en': (
            f'{g} groups of {k} → {g} × {k} = {total}.\n'
            f'Multiplication represents equal groups.'
        ),
    }


# ─── 3. repeated_addition_gen ─────────────────────────────────────────────────

def repeated_addition_gen(level: str = 'medium') -> dict:
    """
    Mix & match — match each repeated addition to its multiplication.
    3-4 pairs.
    """
    count = 3 if level == 'easy' else 4

    if level == 'easy':
        factors = random.sample(range(2, 7), count)
        repeats = random.sample(range(2, 6), count)
    elif level == 'medium':
        factors = random.sample(range(2, 10), count)
        repeats = random.sample(range(2, 9), count)
    else:
        factors = random.sample(range(3, 12), count)
        repeats = random.sample(range(3, 11), count)

    pairs = []
    seen = set()
    for i in range(count):
        f, r = factors[i], repeats[i]
        key = (f, r)
        if key in seen:
            continue
        seen.add(key)
        addition_str = ' + '.join([str(f)] * r)
        mult_str = f'{r} × {f}'
        pairs.append({'left': addition_str, 'right': mult_str})

    pairs = pairs[:count]

    return {
        'q_type': 'mix_match',
        'prompt_fr': 'Associe chaque addition répétée à la multiplication correspondante.',
        'prompt_en': 'Match each repeated addition to its multiplication.',
        'hint_fr': 'Compte combien de fois le même nombre se répète.',
        'hint_en': 'Count how many times the same number is repeated.',
        'shape_data': [],
        'choices': [],
        'pairs': pairs,
        'correct_answers': [p['right'] for p in pairs],
        'time_limit': 40,
        'points': len(pairs),
        'explanation_fr': '\n'.join(f'{p["left"]} = {p["right"]}' for p in pairs),
        'explanation_en': '\n'.join(f'{p["left"]} = {p["right"]}' for p in pairs),
    }


# ─── 4. division_sharing_gen ──────────────────────────────────────────────────

def division_sharing_gen(level: str = 'medium') -> dict:
    """
    QCM — total objects shared equally among groups: how many each?
    """
    if level == 'easy':
        groups  = random.randint(2, 5)
        per_grp = random.randint(1, 6)
    elif level == 'medium':
        groups  = random.randint(3, 8)
        per_grp = random.randint(2, 10)
    else:
        groups  = random.randint(5, 12)
        per_grp = random.randint(5, 12)

    total = groups * per_grp

    choices = _tagged_shuffle_mc(str(per_grp), [
        (str(total - groups),
         'wrong_operation',
         'You subtracted instead of dividing — share equally!',
         'Tu as soustrait au lieu de partager — divise en parts égales !'),
        (str(total + groups),
         'wrong_operation',
         'You added instead of dividing.',
         'Tu as additionné au lieu de diviser.'),
        (str(groups),
         'answer_confusion',
         'You gave the number of groups, not the share per group.',
         'Tu as donné le nombre de groupes, pas la part de chacun.'),
        (str(per_grp + 1),
         'off_by_one',
         'Close! Check your division.',
         'Presque ! Vérifie ta division.'),
    ])

    themes_fr = [
        f'**{total}** pièces sont partagées entre **{groups}** pirates. '
        f'Combien chaque pirate reçoit-il ?',
        f'**{total}** bonbons sont distribués équitablement dans **{groups}** sacs. '
        f'Combien y a-t-il de bonbons dans chaque sac ?',
    ]
    themes_en = [
        f'**{total}** coins are shared equally among **{groups}** pirates. '
        f'How many does each pirate receive?',
        f'**{total}** candies are placed equally into **{groups}** bags. '
        f'How many candies are in each bag?',
    ]
    idx = random.randint(0, len(themes_fr) - 1)

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': themes_fr[idx],
        'prompt_en': themes_en[idx],
        'hint_fr': f'Divise {total} par {groups}.',
        'hint_en': f'Divide {total} by {groups}.',
        'shape_data': [],
        'choices': choices,
        'correct_answers': [str(per_grp)],
        'time_limit': 30,
        'points': 1,
        'explanation_fr': (
            f'Partager {total} en {groups} parts égales : '
            f'{total} ÷ {groups} = **{per_grp}**'
        ),
        'explanation_en': (
            f'Share {total} into {groups} equal parts: '
            f'{total} ÷ {groups} = **{per_grp}**'
        ),
    }


# ─── 5. choose_operation_gen ─────────────────────────────────────────────────

def choose_operation_gen(level: str = 'medium') -> dict:
    """
    QCM — read a word problem and choose the operation to use first.
    Scenarios cycle through all four operations.
    """
    _SCENARIOS = [
        # (type, prompt_fr, prompt_en, answer_fr, answer_en, distractors_fr, distractors_en)
        ('add',
         lambda a, b: (
             f'Léa a **{a}** billes. Elle en reçoit **{b}** de plus. '
             f'Quelle est la première opération à faire ?',
             f'Léa has **{a}** marbles. She gets **{b}** more. '
             f'What is the first operation to use?',
         ),
         'addition', 'addition',
         ['soustraction', 'multiplication', 'division'],
         ['subtraction', 'multiplication', 'division']),
        ('sub',
         lambda a, b: (
             f'Il y a **{a}** élèves. **{b}** partent. '
             f'Quelle opération permet de trouver combien il en reste ?',
             f'There are **{a}** students. **{b}** leave. '
             f'Which operation finds how many remain?',
         ),
         'soustraction', 'subtraction',
         ['addition', 'multiplication', 'division'],
         ['addition', 'multiplication', 'division']),
        ('mul',
         lambda a, b: (
             f'Il y a **{a}** rangées de **{b}** arbres. '
             f'Quelle opération compte le nombre total d\'arbres ?',
             f'There are **{a}** rows of **{b}** trees. '
             f'Which operation counts the total number of trees?',
         ),
         'multiplication', 'multiplication',
         ['addition', 'soustraction', 'division'],
         ['addition', 'subtraction', 'division']),
        ('div',
         lambda a, b: (
             f'**{a}** images sont réparties en **{b}** albums égaux. '
             f'Quelle opération trouve le nombre d\'images par album ?',
             f'**{a}** pictures are placed into **{b}** equal albums. '
             f'Which operation finds pictures per album?',
         ),
         'division', 'division',
         ['addition', 'soustraction', 'multiplication'],
         ['addition', 'subtraction', 'multiplication']),
    ]

    if level == 'easy':
        a, b = random.randint(5, 20), random.randint(2, 10)
    elif level == 'medium':
        a, b = random.randint(20, 100), random.randint(3, 15)
    else:
        a, b = random.randint(100, 500), random.randint(5, 20)

    sc = random.choice(_SCENARIOS)
    _, make_prompt, ans_fr, ans_en, dist_fr, dist_en = sc
    prompt_fr, prompt_en = make_prompt(a, b)

    dist_lbl = dist_fr[:]
    random.shuffle(dist_lbl)
    candidates = [(d, 'wrong_operation',
                   'Re-read the problem: look for keywords like "more", "less", "share", "groups".',
                   'Relis le problème : cherche les mots "de plus", "de moins", "partage", "groupes".')
                  for d in dist_lbl[:4]]

    seen = {ans_fr}
    pool = []
    for (lbl, etype, fb_en, fb_fr) in candidates:
        if lbl not in seen:
            seen.add(lbl)
            pool.append({'label': lbl, 'correct': False,
                         'error_type': etype, 'feedback_en': fb_en, 'feedback_fr': fb_fr})
        if len(pool) == 4:
            break
    # Pad if needed
    extras = ['addition', 'soustraction', 'multiplication', 'division']
    for e in extras:
        if len(pool) >= 4:
            break
        if e not in seen:
            seen.add(e)
            pool.append({'label': e, 'correct': False,
                         'error_type': 'wrong_operation', 'feedback_en': '', 'feedback_fr': ''})

    insert = random.randint(0, 4)
    pool.insert(insert, {'label': ans_fr, 'correct': True,
                         'error_type': '', 'feedback_en': '', 'feedback_fr': ''})

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': prompt_fr,
        'prompt_en': prompt_en,
        'hint_fr': 'Cherche les mots-clés : de plus, de moins, groupes, partage.',
        'hint_en': 'Look for keywords: more, less, groups, share.',
        'shape_data': [],
        'choices': pool[:5],
        'correct_answers': [ans_fr, ans_en],
        'time_limit': 35,
        'points': 1,
        'explanation_fr': f'La bonne opération est : **{ans_fr}**.',
        'explanation_en': f'The correct operation is: **{ans_en}**.',
    }


# ─── 6. read_decimal_gen ──────────────────────────────────────────────────────

def read_decimal_gen(level: str = 'medium') -> dict:
    """
    Typed — given French words for a decimal, write the digits.
    Max 2 decimal places (money-safe), up to 4 for hard level.
    """
    if level == 'easy':
        int_part  = random.randint(0, 9)
        dec_places = 1
        dec_digit  = random.randint(1, 9)
        dec_str    = str(dec_digit)
    elif level == 'medium':
        int_part  = random.randint(0, 99)
        dec_places = 2
        dec_digit  = random.randint(10, 99)
        dec_str    = str(dec_digit)
    else:
        int_part  = random.randint(0, 99)
        dec_places = random.choice([3, 4])
        dec_digit  = random.randint(10 ** (dec_places - 1), 10 ** dec_places - 1)
        dec_str    = str(dec_digit)

    words_fr, words_en = _decimal_to_words(int_part, dec_str)
    correct_str = f'{int_part}.{dec_str}'
    # Accept both comma and dot notation
    correct_comma = f'{int_part},{dec_str}'

    return {
        'q_type': 'text_input',
        'prompt_fr': f'Écris en chiffres : **{words_fr}**',
        'prompt_en': f'Write in digits: **{words_fr}**',
        'hint_fr': 'La virgule sépare la partie entière de la partie décimale.',
        'hint_en': 'The decimal point separates the whole part from the decimal part.',
        'shape_data': [],
        'choices': [],
        'correct_answers': [correct_str, correct_comma],
        'time_limit': 30,
        'points': 1,
        'explanation_fr': f'"{words_fr}" s\'écrit **{correct_str}** en chiffres.',
        'explanation_en': f'"{words_en}" is written **{correct_str}** in digits.',
    }


# ─────────────────────────────────────────────────────────────────────────────
# fraction_to_decimal_gen  (content2.md Thème 4, section 21)
# ─────────────────────────────────────────────────────────────────────────────

def fraction_to_decimal_gen(level='easy'):
    """
    QCM — recognise that x/10 = 0,x  (dixièmes / tenths).
    easy   → 1/10 to 9/10
    medium → 1/10 to 9/10, some with leading zero context
    hard   → also includes x/100 = 0,0x and improper (12/10 = 1,2)
    """
    import random as _r
    from .base import _tagged_shuffle_mc as _mc

    if level in ('easy', 'medium'):
        numerator   = _r.randint(1, 9)
        denominator = 10
        correct     = f'0,{numerator}'
        tagged_candidates = [
            (f'{numerator},0',   'digit_swap',    "The numerator goes after the decimal comma.", "Le numérateur se place après la virgule décimale."),
            (f'0,0{numerator}',  'extra_zero',    "With tenths there is only one decimal place.", "Les dixièmes ont une seule décimale."),
            (str(numerator),      'missing_comma', "Don't forget the decimal comma.", "N'oublie pas la virgule décimale."),
            (f'10,{numerator}',  'reversed',      "The denominator tells you the place value, not the units digit.", "Le dénominateur indique la valeur de position."),
        ]
    else:
        # Hard: mix of /10 and /100, or improper tenths
        kind = _r.choice(['tenths', 'hundredths', 'improper'])
        if kind == 'tenths':
            numerator   = _r.randint(1, 9)
            denominator = 10
            correct     = f'0,{numerator}'
            tagged_candidates = [
                (f'{numerator},0',  'digit_swap', "Numerator goes after the decimal.", "Le numérateur se place après la virgule."),
                (f'0,0{numerator}', 'extra_zero', "Tenths have one decimal place.", "Les dixièmes ont une seule décimale."),
                (str(numerator),     'missing_comma', "Add the decimal comma.", "Ajoute la virgule."),
                (f'{numerator}/{denominator}', 'fraction_kept', "Write it as a decimal, not a fraction.", "Écris-le en décimal, pas en fraction."),
            ]
        elif kind == 'hundredths':
            numerator   = _r.randint(1, 9)
            denominator = 100
            correct     = f'0,0{numerator}'
            tagged_candidates = [
                (f'0,{numerator}',  'wrong_place', "Hundredths have TWO decimal places.", "Les centièmes ont DEUX décimales."),
                (f'{numerator},0',  'digit_swap',  "The numerator goes after the decimal.", "Le numérateur se place après la virgule."),
                (str(numerator),      'missing_comma', "Don't forget the decimal comma.", "N'oublie pas la virgule."),
                (f'100,{numerator}','reversed',    "The denominator gives the place value.", "Le dénominateur indique la valeur de position."),
            ]
        else:  # improper tenths: 12/10 = 1,2
            numerator   = _r.randint(11, 19)
            denominator = 10
            whole       = numerator // 10
            dec         = numerator % 10
            correct     = f'{whole},{dec}'
            tagged_candidates = [
                (f'0,{numerator}',  'too_small',  "The numerator is greater than 10 — the result is more than 1.", "Le numérateur dépasse 10 — le résultat est plus grand que 1."),
                (str(whole),         'missing_dec', "There is a remainder after dividing by 10.", "Il y a un reste après la division par 10."),
                (f'1,{numerator}',  'digit_swap',  "Only the remainder goes after the decimal comma.", "Seul le reste se place après la virgule."),
                (f'{numerator},0',  'reversed',   "Divide the numerator by the denominator.", "Divise le numérateur par le dénominateur."),
            ]

    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       f'Le nombre {numerator}/{denominator} s\'écrit aussi :',
        'prompt_en':       f'The number {numerator}/{denominator} can also be written as:',
        'hint_fr':         'Les dixièmes correspondent à la première décimale (après la virgule).',
        'hint_en':         'Tenths are the first decimal place (after the decimal point).',
        'show_illustration': False,
        'shape_data':      [],
        'choices':         _mc(correct, tagged_candidates),
        'pairs':           [],
        'explanation_en': (
            f'Step 1: {numerator}/{denominator} means {numerator} part(s) out of {denominator}.\n'
            f'Step 2: Divide numerator by denominator: {numerator} ÷ {denominator} = {correct.replace(",", ".")}.\n'
            f'Answer: {numerator}/{denominator} = {correct}'
        ),
        'explanation_fr': (
            f'Étape 1 : {numerator}/{denominator} signifie {numerator} partie(s) sur {denominator}.\n'
            f'Étape 2 : Divise le numérateur par le dénominateur : {numerator} ÷ {denominator} = {correct}.\n'
            f'Réponse : {numerator}/{denominator} = {correct}'
        ),
        'correct_answers': [correct],
    }


# ─────────────────────────────────────────────────────────────────────────────
# number_classify_gen  (content2.md Thème 4, section 24)
# ─────────────────────────────────────────────────────────────────────────────

def _is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def number_classify_gen(level='easy'):
    """
    QCM — classify a number as Pair / Impair / Pair et Premier / Impair et Premier.
    The five choices are always the same; only the correct answer changes.
    easy   → numbers 2-20
    medium → numbers 2-50
    hard   → numbers 2-100
    """
    import random as _r

    max_n = 20 if level == 'easy' else (50 if level == 'medium' else 100)
    n = _r.randint(2, max_n)

    even    = (n % 2 == 0)
    prime   = _is_prime(n)

    if even and prime:                # only n=2 in range
        ans_fr, ans_en = "Pair et Premier",   "Even and Prime"
    elif even:
        ans_fr, ans_en = "Pair",              "Even"
    elif prime:
        ans_fr, ans_en = "Impair et Premier", "Odd and Prime"
    else:
        ans_fr, ans_en = "Impair",            "Odd"

    fixed_fr = ["Pair", "Impair", "Pair et Premier", "Impair et Premier", "Aucune de ces réponses"]
    fixed_en = ["Even", "Odd",   "Even and Prime",   "Odd and Prime",     "None of these"]

    # Shuffle the choices
    idxs = list(range(len(fixed_fr)))
    _r.shuffle(idxs)

    choices = []
    for i in idxs:
        fr_label = fixed_fr[i]
        en_label = fixed_en[i]
        correct  = (fr_label == ans_fr)
        if correct:
            fb_fr, fb_en = '', ''
        elif 'Premier' in fr_label and not prime:
            fb_fr = f'{n} n\'est pas un nombre premier (il a plus de 2 diviseurs).'
            fb_en = f'{n} is not a prime number (it has more than 2 factors).'
        elif fr_label == "Pair" and not even:
            fb_fr = f'{n} est impair — il ne se divise pas par 2 sans reste.'
            fb_en = f'{n} is odd — it does not divide evenly by 2.'
        elif fr_label == "Impair" and even:
            fb_fr = f'{n} est pair — il se divise par 2 sans reste.'
            fb_en = f'{n} is even — it divides evenly by 2.'
        else:
            fb_fr = 'Relis les définitions de pair, impair et premier.'
            fb_en = 'Review the definitions of even, odd, and prime.'

        choices.append({
            'value':      fr_label,
            'label_fr':  fr_label,
            'label_en':  en_label,
            'correct':   correct,
            'error_type':  '' if correct else 'wrong_classification',
            'feedback_fr': fb_fr,
            'feedback_en': fb_en,
        })

    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       f'Le nombre {n} est :',
        'prompt_en':       f'The number {n} is:',
        'hint_fr':         'Pair = divisible par 2. Premier = exactement 2 diviseurs (1 et lui-même).',
        'hint_en':         'Even = divisible by 2. Prime = exactly 2 factors (1 and itself).',
        'show_illustration': False,
        'shape_data':      [],
        'choices':         choices,
        'pairs':           [],
        'explanation_en': (
            f'Step 1: Is {n} divisible by 2? {"Yes — it is even." if even else "No — it is odd."}\n'
            f'Step 2: Does {n} have exactly 2 factors (1 and itself)? {"Yes — it is prime." if prime else "No — it is not prime."}\n'
            f'Answer: {n} is {ans_en}'
        ),
        'explanation_fr': (
            f'Étape 1 : {n} est-il divisible par 2 ? {"Oui — il est pair." if even else "Non — il est impair."}\n'
            f'Étape 2 : {n} a-t-il exactement 2 diviseurs (1 et lui-même) ? {"Oui — il est premier." if prime else "Non — il n\'est pas premier."}\n'
            f'Réponse : {n} est {ans_fr}'
        ),
        'correct_answers': [ans_fr],
    }


# ─────────────────────────────────────────────────────────────────────────────
# fraction_collection_gen  (content3.md Bloc E, section E1)
# ─────────────────────────────────────────────────────────────────────────────

_COLLECTION_CONTEXTS = [
    # (category_fr, category_en, item_a_fr, item_b_fr, item_a_en, item_b_en)
    ("animaux", "animals", "chats", "oiseaux", "cats", "birds"),
    ("fruits",  "fruits",  "pommes", "oranges", "apples", "oranges"),
    ("jouets",  "toys",    "voitures", "balles", "cars",   "balls"),
    ("élèves",  "students","filles", "garçons", "girls",  "boys"),
    ("formes",  "shapes",  "carrés", "triangles", "squares", "triangles"),
    ("fleurs",  "flowers", "roses",  "tulipes",  "roses",  "tulips"),
]


def fraction_collection_gen(level='easy'):
    import random as _r
    from .base import _tagged_shuffle_mc as _mc

    if level == 'easy':
        total = _r.randint(3, 8)
    elif level == 'medium':
        total = _r.randint(6, 12)
    else:
        total = _r.randint(8, 20)

    # Pick a split: part_b is what the question asks about
    part_b = _r.randint(1, total - 1)
    part_a = total - part_b

    ctx = _r.choice(_COLLECTION_CONTEXTS)
    cat_fr, cat_en, item_a_fr, item_b_fr, item_a_en, item_b_en = ctx

    # Correct fraction: part_b / total
    from math import gcd as _gcd
    g = _gcd(part_b, total)
    num_r, den_r = part_b // g, total // g
    correct = f'{part_b}/{total}'
    correct_reduced = f'{num_r}/{den_r}'

    # Accept both forms
    correct_answers = [correct]
    if correct_reduced != correct:
        correct_answers.append(correct_reduced)

    # Distractors
    tagged_candidates = [
        (f'{part_a}/{total}', 'complement',
         f'That is the fraction of {item_a_en}, not {item_b_en}.',
         f"C'est la fraction des {item_a_fr}, pas des {item_b_fr}."),
        (f'{part_b}/{part_a}', 'ratio_not_fraction',
         'A fraction compares part to the TOTAL, not part to the other part.',
         'Une fraction compare la partie au TOTAL, pas aux autres éléments.'),
        (f'{total}/{part_b}', 'inverted',
         'The numerator is the part, the denominator is the total.',
         'Le numérateur est la partie, le dénominateur est le total.'),
        (f'{part_b + 1}/{total}', 'off_by_one',
         'Count carefully.',
         'Compte bien.'),
    ]

    prompt_fr = (f"Dans un groupe de {total} {cat_fr}, il y a {part_a} {item_a_fr} "
                 f"et {part_b} {item_b_fr}. "
                 f"Quelle fraction des {cat_fr} sont des {item_b_fr} ?")
    prompt_en = (f"In a group of {total} {cat_en}, there are {part_a} {item_a_en} "
                 f"and {part_b} {item_b_en}. "
                 f"What fraction of the {cat_en} are {item_b_en}?")

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Fraction = (nombre de la partie visée) / (total du groupe)',
        'hint_en':          'Fraction = (count of the targeted part) / (total in the group)',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _mc(correct, tagged_candidates),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Count the {item_b_en}: {part_b} out of {total} total {cat_en}.\n'
            f'Step 2: Write as a fraction: {item_b_en} / total = {part_b}/{total}.\n'
            f'Answer: {correct}'
        ),
        'explanation_fr': (
            f'Étape 1 : Compte les {item_b_fr} : {part_b} sur {total} {cat_fr} au total.\n'
            f'Étape 2 : Écris en fraction : {item_b_fr} / total = {part_b}/{total}.\n'
            f'Réponse : {correct}'
        ),
        'correct_answers':  correct_answers,
    }
