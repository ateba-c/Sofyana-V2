"""
g6_fractions.py — Grade-6 fractions on the number line (content_g6.md §6).

Topics:
  g6_fraction_on_line_gen   QCM + SVG        – which fraction is at the "?" point (proper & improper)
  g6_fraction_between_gen   QCM              – 5/3 lies between which two whole numbers?
  g6_fraction_order_gen     ordering         – sort fractions with the same denominator (proper & improper)
"""
import random
from .base import _tagged_shuffle_mc
from . import scenarios as sc  # noqa: F401  (kept for parity; fractions need no story)


def _setup(level):
    if level == 'easy':
        d = random.choice([2, 3, 4, 5])
        units = 1
        num = random.randint(1, d - 1)
    elif level == 'medium':
        d = random.choice([3, 4, 5, 6, 7, 8])
        units = 2
        num = random.randint(1, 2 * d - 1)
    else:
        d = random.choice([5, 6, 7, 8, 9, 10])
        units = 3
        num = random.randint(d + 1, 3 * d - 1)      # always improper
    return d, units, num


def _frac(n, d):
    return f'{n}/{d}'


def g6_fraction_on_line_gen(level='easy'):
    d, units, num = _setup(level)
    correct = _frac(num, d)
    tagged = [
        (_frac(num + 1, d), 'off_by_one', 'Count the tick marks from 0 again.', 'Recompte les graduations à partir de 0.'),
        (_frac(max(1, num - 1), d), 'off_by_one', 'Count the tick marks from 0 again.', 'Recompte les graduations à partir de 0.'),
        (_frac(num, d + 1), 'wrong_denominator', 'The denominator is the number of equal parts in ONE unit.', "Le dénominateur est le nombre de parts égales dans UNE unité."),
        (_frac(num, d - 1) if d > 2 else _frac(num, d + 2), 'wrong_denominator', 'The denominator is the number of equal parts in ONE unit.', "Le dénominateur est le nombre de parts égales dans UNE unité."),
        (_frac(num % d if num % d else 1, d), 'ignored_units', 'Past 1 keep counting: the numerator keeps growing.', 'Après 1, continue à compter : le numérateur continue à grandir.'),
        (_frac(d, num) if num != d else _frac(d, num + 1), 'swapped', 'Numerator on top, denominator below.', 'Numérateur en haut, dénominateur en bas.'),
    ]
    seen = {correct}
    tagged = [t for t in tagged if t[0] not in seen and not seen.add(t[0])]
    whole, rem = divmod(num, d)
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': "Quelle fraction se trouve au point « ? » sur cette droite numérique ?",
        'prompt_en': "Which fraction is at the “?” point on this number line?",
        'hint_fr': f"Chaque unité est partagée en {d} parts égales : le dénominateur est {d}. Compte les graduations depuis 0 pour trouver le numérateur.",
        'hint_en': f"Each unit is split into {d} equal parts: the denominator is {d}. Count the tick marks from 0 to find the numerator.",
        'show_illustration': True,
        'shape_data': [{'type': 'fraction_number_line', 'denominator': d, 'units': units, 'target': num}],
        'choices': _tagged_shuffle_mc(correct, tagged), 'pairs': [],
        'explanation_en': f'Each unit has {d} parts → denominator {d}. The point is {num} tick(s) after 0 → {correct}' + (f' = {whole} + {rem}/{d}' if whole and rem else f' = {whole}' if whole else '') + '.',
        'explanation_fr': f'Chaque unité a {d} parts → dénominateur {d}. Le point est à {num} graduation(s) après 0 → {correct}' + (f' = {whole} + {rem}/{d}' if whole and rem else f' = {whole}' if whole else '') + '.',
        'correct_answers': [correct],
    }


def g6_fraction_between_gen(level='easy'):
    if level == 'easy':
        d = random.choice([2, 3, 4, 5]); num = random.randint(d + 1, 2 * d - 1)
    elif level == 'medium':
        d = random.choice([3, 4, 5, 6, 7]); num = random.randint(d + 1, 3 * d - 1)
    else:
        d = random.choice([4, 5, 6, 7, 8, 9]); num = random.randint(2 * d + 1, 5 * d - 1)
    if num % d == 0:
        num += 1
    lo = num // d
    correct = f'{lo} et {lo + 1}'
    tagged = [(f'{lo + 1} et {lo + 2}', 'off_by_one', 'How many whole units fit in the fraction?', "Combien d'unités entières entrent dans la fraction ?"),
              (f'{max(0, lo - 1)} et {lo}', 'off_by_one', 'How many whole units fit in the fraction?', "Combien d'unités entières entrent dans la fraction ?"),
              (f'{num - d} et {num}', 'confused_numerator', 'Divide the numerator by the denominator.', 'Divise le numérateur par le dénominateur.'),
              ('0 et 1', 'thinks_proper', f'{num}/{d} is bigger than 1 because {num} > {d}.', f'{num}/{d} est plus grand que 1 car {num} > {d}.'),
              (f'{d} et {d + 1}', 'confused_denominator', 'Divide the numerator by the denominator.', 'Divise le numérateur par le dénominateur.')]
    seen = {correct}
    tagged = [t for t in tagged if t[0] not in seen and not seen.add(t[0])]
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f"Sur une droite numérique, la fraction **{num}/{d}** se situe entre quels deux nombres entiers ?",
        'prompt_en': f"On a number line, the fraction **{num}/{d}** lies between which two whole numbers?",
        'hint_fr': f"Combien de fois {d} entre dans {num} ? {d} × {lo} = {d * lo} ≤ {num} < {d * (lo + 1)}.",
        'hint_en': f"How many times does {d} go into {num}? {d} × {lo} = {d * lo} ≤ {num} < {d * (lo + 1)}.",
        'show_illustration': False, 'shape_data': [],
        'choices': _tagged_shuffle_mc(correct, tagged), 'pairs': [],
        'explanation_en': f'{num} ÷ {d} = {lo} remainder {num - d * lo} → {num}/{d} = {lo} + {num - d * lo}/{d}, between {lo} and {lo + 1}.',
        'explanation_fr': f'{num} ÷ {d} = {lo} reste {num - d * lo} → {num}/{d} = {lo} + {num - d * lo}/{d}, entre {lo} et {lo + 1}.',
        'correct_answers': [correct, f'{lo} and {lo + 1}'],
    }


def g6_fraction_order_gen(level='easy'):
    if level == 'easy':
        d = random.choice([5, 7, 9]); pool = range(1, d); count = 4
    elif level == 'medium':
        d = random.choice([5, 6, 7, 8, 9]); pool = range(1, 2 * d); count = 5
    else:
        d = random.choice([6, 7, 8, 9, 10]); pool = range(1, 3 * d); count = 5
    nums = sorted(random.sample(list(pool), count))
    desc = level == 'hard' and random.random() < 0.5
    ordered = nums[::-1] if desc else nums
    items = [{'label': _frac(n, d), 'order': i + 1} for i, n in enumerate(ordered)]
    return {
        'q_type': 'ordering',
        'prompt_fr': f"Range ces fractions en ordre **{'décroissant' if desc else 'croissant'}**, comme sur une droite numérique.",
        'prompt_en': f"Sort these fractions in **{'descending' if desc else 'ascending'}** order, as on a number line.",
        'hint_fr': f"Même dénominateur ({d}) : compare seulement les numérateurs. Une fraction dont le numérateur dépasse {d} est plus grande que 1.",
        'hint_en': f"Same denominator ({d}): compare only the numerators. A fraction whose numerator is above {d} is bigger than 1.",
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'items': items, 'correct_answers': [i['label'] for i in items], 'time_limit': 40, 'points': 1,
        'explanation_en': (' > ' if desc else ' < ').join(_frac(n, d) for n in ordered),
        'explanation_fr': (' > ' if desc else ' < ').join(_frac(n, d) for n in ordered),
    }
