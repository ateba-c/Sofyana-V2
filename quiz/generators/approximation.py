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
    """Round n to the nearest multiple of base."""
    return base * round(n / base)


# ─── 1. round_ten_gen ─────────────────────────────────────────────────────────

def round_ten_gen(level: str = 'medium') -> dict:
    """
    QCM — round n to the nearest 10.
    Distractors: lower ten, upper ten, truncation, wrong hundred.
    """
    if level == 'easy':
        n = random.randint(11, 99)
    elif level == 'medium':
        n = random.randint(100, 999)
    else:
        n = random.randint(1000, 9999)

    result = _round_to(n, 10)
    lower  = (n // 10) * 10          # truncation (always round down)
    upper  = lower + 10              # always round up
    trunc  = lower                   # same as lower — use different value
    off    = result + 10 if result + 10 <= 9999 else result - 10

    choices = _tagged_shuffle_mc(str(result), [
        (str(upper if result == lower else lower),
         'wrong_direction',
         'Check the units digit: 0-4 round down, 5-9 round up.',
         'Regarde les unités : 0-4 → on descend, 5-9 → on monte.'),
        (str(off),
         'place_value',
         'You rounded to the wrong ten.',
         'Tu as arrondi à la mauvaise dizaine.'),
        (str(n),
         'no_rounding',
         'You did not round — check the units digit.',
         'Tu n\'as pas arrondi — regarde le chiffre des unités.'),
        (str(_round_to(n, 100)),
         'wrong_base',
         'You rounded to the nearest hundred, not ten.',
         'Tu as arrondi à la centaine, pas à la dizaine.'),
    ])

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
    if level == 'easy':
        n = random.randint(101, 999)
    elif level == 'medium':
        n = random.randint(1000, 9999)
    else:
        # Hard: deliberately choose numbers near x50 boundary
        base = random.randint(10, 99) * 100
        n = base + random.randint(40, 60)
        n = min(n, 9999)

    result = _round_to(n, 100)
    if result > 9999:
        result = 9900

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

    choices = _tagged_shuffle_mc(str(total), [
        (str(g + k + r),
         'add_instead_of_multiply',
         'You added the groups and objects — multiply the groups by the size first!',
         'Tu as additionné au lieu de multiplier — commence par g × k !'),
        (str(g * k),
         'forgot_remainder',
         'You forgot to add the remaining objects.',
         'Tu as oublié d\'ajouter les objets isolés.'),
        (str(g * (k + r)),
         'wrong_grouping',
         'Only the leftover objects are alone — do not include them in the groups.',
         'Seuls les objets isolés ne font pas partie des groupes.'),
        (str((g + 1) * k + r),
         'off_by_one_group',
         'Check the number of groups.',
         'Vérifie le nombre de groupes.'),
    ])

    themes = [
        ('biscuits', 'biscuits', 'boîtes', 'boxes'),
        ('pièces', 'coins', 'sacs', 'bags'),
        ('bonbons', 'candies', 'sachets', 'pouches'),
        ('billes', 'marbles', 'pots', 'jars'),
    ]
    obj_fr, obj_en, cont_fr, cont_en = random.choice(themes)

    prompt_fr = (
        f'Il y a **{g}** {cont_fr} de **{k}** {obj_fr} '
        f'et **{r}** {obj_fr} seul{"s" if r > 1 else ""}. '
        f'Combien y a-t-il de {obj_fr} en tout ?'
    ) if r > 0 else (
        f'Il y a **{g}** {cont_fr} de **{k}** {obj_fr}. '
        f'Combien y a-t-il de {obj_fr} en tout ?'
    )
    prompt_en = (
        f'There are **{g}** {cont_en} of **{k}** {obj_en} '
        f'and **{r}** loose {obj_en}. '
        f'How many {obj_en} are there in total?'
    ) if r > 0 else (
        f'There are **{g}** {cont_en} of **{k}** {obj_en}. '
        f'How many {obj_en} are there in total?'
    )

    expl_fr = f'{g} × {k} = {g * k}'
    expl_fr += f' + {r} = **{total}**' if r else f' = **{total}**'
    expl_en = f'{g} × {k} = {g * k}'
    expl_en += f' + {r} = **{total}**' if r else f' = **{total}**'

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': prompt_fr,
        'prompt_en': prompt_en,
        'hint_fr': 'Multiplie d\'abord le nombre de groupes par la taille de chaque groupe.',
        'hint_en': 'First multiply the number of groups by each group size.',
        'shape_data': [],
        'choices': choices,
        'correct_answers': [str(total)],
        'time_limit': 30,
        'points': 1,
        'explanation_fr': expl_fr,
        'explanation_en': expl_en,
    }
