"""
approximation.py — Grade-3 rounding and counting generators.

Topics (content.md Thème 2, section 11):
  round_ten_gen       QCM    – round {n} to the nearest 10
  round_hundred_gen   typed  – round {n} to the nearest 100
  count_groups_gen    QCM    – g groups of k objects + r alone = total?

Difficulty:
  easy   → smaller numbers / closer distractors
  medium → larger numbers
  hard   → edge cases (e.g. x5 for rounding, maximum group sizes)
"""

import random
from .base import _tagged_shuffle_mc


def _round_to(n: int, base: int) -> int:
    """Round n to the nearest multiple of base; a half rounds UP (school rule: 45 → 50).

    Python's round() is banker's rounding (round(4.5) == 4), so it is not used here.
    """
    return (n + base // 2) // base * base


# ─── 1. round_ten_gen ─────────────────────────────────────────────────────────

def round_ten_gen(level: str = 'medium') -> dict:
    """
    QCM — round n to the nearest 10.
    Distractors: lower ten, upper ten, truncation, wrong hundred.
    """
    # Grade 3: numbers stay below 1000.  A multiple of 10 needs no rounding: skip it.
    if level == 'easy':
        n = random.randint(11, 99)
    elif level == 'medium':
        n = random.randint(100, 994)
    else:
        # hard: the tricky halves (…5) and units 5-9 that push into the next ten
        n = random.choice([random.randint(10, 99) * 10 + 5,
                           random.randint(10, 98) * 10 + random.randint(5, 9)])
    if n % 10 == 0:
        n += random.randint(1, 9)

    result = _round_to(n, 10)
    lower  = (n // 10) * 10          # always round down
    upper  = lower + 10              # always round up
    other  = upper if result == lower else lower
    beyond = other + (other - result)            # one more ten in the wrong direction
    away   = result + (result - other)           # one ten past the answer

    tagged = [
        (str(other),
         'wrong_direction',
         'Check the units digit: 0-4 round down, 5-9 round up.',
         'Regarde les unités : 0-4 → on descend, 5-9 → on monte.'),
        (str(n),
         'no_rounding',
         'You did not round — check the units digit.',
         'Tu n\'as pas arrondi — regarde le chiffre des unités.'),
        (str(_round_to(n, 100)),
         'wrong_base',
         'You rounded to the nearest hundred, not ten.',
         'Tu as arrondi à la centaine, pas à la dizaine.'),
    ]
    for v in (away, beyond, result + 20, result + 30):
        tagged.append((str(v), 'place_value',
                       'You rounded to the wrong ten.',
                       'Tu as arrondi à la mauvaise dizaine.'))
    choices = _tagged_shuffle_mc(str(result), tagged)

    units = n % 10
    rule_fr = ('≥ 5 → on arrondit à la dizaine supérieure'
               if units >= 5 else
               '< 5 → on arrondit à la dizaine inférieure')
    rule_en = ('≥ 5 → round up to the next ten'
               if units >= 5 else
               '< 5 → round down to the previous ten')

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f'Arrondis **{n}** à la dizaine la plus proche.',
        'prompt_en': f'Round **{n}** to the nearest ten.',
        'hint_fr': 'Regarde le chiffre des unités (0-4 → descend, 5-9 → monte).',
        'hint_en': 'Look at the units digit (0-4 → round down, 5-9 → round up).',
        'shape_data': [],
        'choices': choices,
        'correct_answers': [str(result)],
        'time_limit': 25,
        'points': 1,
        'explanation_fr': (
            f'{n} → chiffre des unités = {units} ({rule_fr}).\n'
            f'Réponse : **{result}**'
        ),
        'explanation_en': (
            f'{n} → units digit = {units} ({rule_en}).\n'
            f'Answer: **{result}**'
        ),
    }


# ─── 2. round_hundred_gen ─────────────────────────────────────────────────────

def round_hundred_gen(level: str = 'medium') -> dict:
    """
    Typed — round n to the nearest 100.
    """
    # Grade 3: numbers stay below 1000 (the answer may be 1000 itself).
    if level in ('easy', 'medium'):
        n = random.randint(101, 999)
        if n % 100 == 0:
            n += random.randint(1, 99)
    else:
        # Hard: deliberately choose numbers near the x50 boundary
        n = random.randint(1, 9) * 100 + random.randint(40, 60)

    result = _round_to(n, 100)

    tens = (n // 10) % 10
    rule_fr = ('≥ 5 → on arrondit à la centaine supérieure'
               if tens >= 5 else
               '< 5 → on arrondit à la centaine inférieure')
    rule_en = ('≥ 5 → round up to the next hundred'
               if tens >= 5 else
               '< 5 → round down to the previous hundred')

    return {
        'q_type': 'text_input',
        'prompt_fr': f'Arrondis **{n}** à la centaine la plus proche.',
        'prompt_en': f'Round **{n}** to the nearest hundred.',
        'hint_fr': 'Regarde le chiffre des dizaines (0-4 → descend, 5-9 → monte).',
        'hint_en': 'Look at the tens digit (0-4 → round down, 5-9 → round up).',
        'shape_data': [],
        'choices': [],
        'correct_answers': [str(result)],
        'time_limit': 25,
        'points': 1,
        'explanation_fr': (
            f'{n} → chiffre des dizaines = {tens} ({rule_fr}).\n'
            f'Réponse : **{result}**'
        ),
        'explanation_en': (
            f'{n} → tens digit = {tens} ({rule_en}).\n'
            f'Answer: **{result}**'
        ),
    }


# ─── 3. count_groups_gen ──────────────────────────────────────────────────────

def count_groups_gen(level: str = 'medium') -> dict:
    """
    QCM — g groups of k objects, r objects alone → total = g×k + r.
    Distractors target common confusions: add instead of multiply, forget remainder.
    """
    if level == 'easy':
        g = random.randint(2, 5)
        k = random.randint(2, 6)
        r = random.randint(0, 4)
    elif level == 'medium':
        g = random.randint(3, 8)
        k = random.randint(3, 10)
        r = random.randint(0, 9)
    else:
        g = random.randint(5, 10)
        k = random.randint(5, 12)
        r = random.randint(1, 9)

    total = g * k + r

    def _t(v, err, en, fr):
        return (str(v), err, en, fr)

    if r:
        tagged = [
            _t(g + k + r, 'add_instead_of_multiply',
               'You added the groups and objects — multiply the groups by the size first!',
               'Tu as additionné au lieu de multiplier — commence par la multiplication !'),
            _t(g * k, 'forgot_remainder',
               'You forgot to add the loose objects.', 'Tu as oublié d\'ajouter les objets à part.'),
            _t(g * (k + r), 'wrong_grouping',
               'The loose objects are not part of the groups.', 'Les objets à part ne font pas partie des groupes.'),
            _t((g + 1) * k + r, 'off_by_one_group', 'Check the number of groups.', 'Vérifie le nombre de groupes.'),
            _t((g - 1) * k + r, 'off_by_one_group', 'Check the number of groups.', 'Vérifie le nombre de groupes.'),
            _t(g * (k + 1) + r, 'off_by_one_size', 'Check the size of each group.', 'Vérifie la taille de chaque groupe.'),
            _t(total + 1, 'calculation', 'Check your multiplication fact.', 'Vérifie ta table de multiplication.'),
            _t(total - 1, 'calculation', 'Check your multiplication fact.', 'Vérifie ta table de multiplication.'),
            _t((g + 2) * k + r, 'off_by_one_group', 'Count the groups again.', 'Recompte les groupes.'),
        ]
    else:
        tagged = [
            _t(g + k, 'add_instead_of_multiply',
               'You added the number of groups and the group size — multiply them!',
               'Tu as additionné le nombre de groupes et la taille d\'un groupe — multiplie-les !'),
            _t((g - 1) * k, 'off_by_one_group', 'You forgot one group.', 'Tu as oublié un groupe.'),
            _t((g + 1) * k, 'off_by_one_group', 'You counted one group too many.', 'Tu as compté un groupe de trop.'),
            _t(g * (k + 1), 'off_by_one_size', 'Check the size of each group.', 'Vérifie la taille de chaque groupe.'),
            _t(g * (k - 1), 'off_by_one_size', 'Check the size of each group.', 'Vérifie la taille de chaque groupe.'),
            _t(g * k + 1, 'calculation', 'Check your multiplication fact.', 'Vérifie ta table de multiplication.'),
            _t(g * k - 1, 'calculation', 'Check your multiplication fact.', 'Vérifie ta table de multiplication.'),
            _t((g + 2) * k, 'off_by_one_group', 'Count the groups again.', 'Recompte les groupes.'),
        ]
    choices = _tagged_shuffle_mc(str(total), tagged)

    themes = [
        # (plural fr, singular fr, plural en, singular en, feminine noun?, container fr, container en)
        ('biscuits', 'biscuit', 'biscuits', 'biscuit', False, 'boîtes', 'boxes'),
        ('pièces', 'pièce', 'coins', 'coin', True, 'sacs', 'bags'),
        ('bonbons', 'bonbon', 'candies', 'candy', False, 'sachets', 'pouches'),
        ('billes', 'bille', 'marbles', 'marble', True, 'pots', 'jars'),
    ]
    obj_fr, one_fr, obj_en, one_en, fem, cont_fr, cont_en = random.choice(themes)
    loose_fr = f'{r} {obj_fr if r > 1 else one_fr} à part'
    loose_en = f'{r} loose {obj_en if r > 1 else one_en}'

    prompt_fr = (
        f'Il y a **{g}** {cont_fr} de **{k}** {obj_fr} '
        f'et **{loose_fr}**. '
        f'Combien y a-t-il de {obj_fr} en tout ?'
    ) if r > 0 else (
        f'Il y a **{g}** {cont_fr} de **{k}** {obj_fr}. '
        f'Combien y a-t-il de {obj_fr} en tout ?'
    )
    prompt_en = (
        f'There are **{g}** {cont_en} of **{k}** {obj_en} '
        f'and **{loose_en}**. '
        f'How many {obj_en} are there in total?'
    ) if r > 0 else (
        f'There are **{g}** {cont_en} of **{k}** {obj_en}. '
        f'How many {obj_en} are there in total?'
    )

    # One equality per step — never "4 × 6 = 24 + 4 = 28", which claims 24 = 28.
    if r:
        expl_fr = f'Étape 1 : {g} × {k} = {g * k}\nÉtape 2 : {g * k} + {r} = **{total}**'
        expl_en = f'Step 1: {g} × {k} = {g * k}\nStep 2: {g * k} + {r} = **{total}**'
        hint_fr = 'Multiplie le nombre de groupes par la taille d\'un groupe, puis ajoute les objets à part.'
        hint_en = 'Multiply the number of groups by the group size, then add the loose objects.'
    else:
        expl_fr = f'{g} groupes de {k} : {g} × {k} = **{total}**'
        expl_en = f'{g} groups of {k}: {g} × {k} = **{total}**'
        hint_fr = 'Multiplie le nombre de groupes par la taille de chaque groupe.'
        hint_en = 'Multiply the number of groups by each group size.'

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': prompt_fr,
        'prompt_en': prompt_en,
        'hint_fr': hint_fr,
        'hint_en': hint_en,
        'shape_data': [],
        'choices': choices,
        'correct_answers': [str(total)],
        'time_limit': 30,
        'points': 1,
        'explanation_fr': expl_fr,
        'explanation_en': expl_en,
    }
