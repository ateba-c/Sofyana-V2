import random
from .base import _tagged_shuffle_mc

# ── conversion tables ─────────────────────────────────────────────────────────
# (from_unit, to_unit, factor, label_en, label_fr)

LENGTH = [
    ('km',  'm',   1000,   'km → m',   'km en m'),
    ('m',   'km',  0.001,  'm → km',   'm en km'),
    ('m',   'cm',  100,    'm → cm',   'm en cm'),
    ('cm',  'm',   0.01,   'cm → m',   'cm en m'),
    ('cm',  'mm',  10,     'cm → mm',  'cm en mm'),
    ('mm',  'cm',  0.1,    'mm → cm',  'mm en cm'),
    ('m',   'mm',  1000,   'm → mm',   'm en mm'),
    ('mm',  'm',   0.001,  'mm → m',   'mm en m'),
]

MASS = [
    ('kg',  'g',   1000,   'kg → g',   'kg en g'),
    ('g',   'kg',  0.001,  'g → kg',   'g en kg'),
    ('g',   'mg',  1000,   'g → mg',   'g en mg'),
    ('mg',  'g',   0.001,  'mg → g',   'mg en g'),
    ('kg',  'mg',  1e6,    'kg → mg',  'kg en mg'),
]

VOLUME = [
    ('kL',  'L',   1000,   'kL → L',   'kL en L'),
    ('L',   'kL',  0.001,  'L → kL',   'L en kL'),
    ('L',   'mL',  1000,   'L → mL',   'L en mL'),
    ('mL',  'L',   0.001,  'mL → L',   'mL en L'),
    ('kL',  'mL',  1e6,    'kL → mL',  'kL en mL'),
]

# Indices of "easy" (×1000) conversions within each table
_EASY_LENGTH = [0, 6]    # km→m, m→mm
_EASY_MASS   = [0, 2]    # kg→g, g→mg
_EASY_VOLUME = [0, 2]    # kL→L, L→mL

# Indices of "hard" (×0.001 / multi-step) conversions
_HARD_LENGTH = [1, 3, 5, 7]  # all ÷1000
_HARD_MASS   = [1, 3, 4]
_HARD_VOLUME = [1, 3, 4]


def _nice_val(result, factor):
    """Format a conversion result without trailing zeros."""
    if result == int(result):
        return str(int(result))
    return f'{result:g}'


def _build_conversion(table, level, easy_indices, hard_indices):
    if level == 'easy':
        conv = table[random.choice(easy_indices)]
    elif level == 'hard':
        conv = random.choice(table)
    else:  # medium — anything
        conv = random.choice(table)

    from_u, to_u, factor, label_en, label_fr = conv

    # Generate a nice round value
    if factor >= 1:
        base = random.randint(1, 20)
        value = base * (int(factor) // 100 if factor >= 100 else 1)
        if value == 0:
            value = base
        value = base  # simple integer
    else:
        # result should be an integer (e.g. 500 cm → 5 m)
        result_val = random.randint(1, 20)
        value = result_val / factor  # value * factor = result_val

    result = round(value * factor, 6)

    v_str = _nice_val(value, factor)
    r_str = _nice_val(result, factor)

    # Also accept formatted with spaces (e.g. "3 500")
    correct_answers = [r_str]
    if ' ' not in r_str and len(r_str) > 3 and r_str.isdigit():
        # Add space-formatted version
        correct_answers.append(f'{int(r_str):,}'.replace(',', ' '))

    # Build tagged distractors for informational use
    tagged_distractors = _conversion_distractors(value, result, factor)

    return {
        'q_type':         'text_input',
        'prompt_en':      f'Convert {v_str} {from_u} to {to_u}. Give the answer in {to_u}.',
        'prompt_fr':      f'Convertissez {v_str} {from_u} en {to_u}. Donnez la réponse en {to_u}.',
        'hint_en':        f'Multiply by {factor:g} to convert from {from_u} to {to_u}.'
                          if factor >= 1 else
                          f'Divide by {1/factor:g} to convert from {from_u} to {to_u}.',
        'hint_fr':        f'Multipliez par {factor:g} pour convertir de {from_u} en {to_u}.'
                          if factor >= 1 else
                          f'Divisez par {1/factor:g} pour convertir de {from_u} en {to_u}.',
        'shape_data':     [],
        'choices':        [],
        'correct_answers': correct_answers,
        'time_limit':     45,
        'points':         2,
        'explanation_en': (
            f'Step 1: Recall the conversion factor: 1 {from_u} = {factor:g} {to_u}.\n'
            f'Step 2: Multiply: {v_str} × {factor:g} = {r_str}.\n'
            f'Answer: {v_str} {from_u} = {r_str} {to_u}'
        ),
        'explanation_fr': (
            f'Étape 1 : Rappelle le facteur de conversion : 1 {from_u} = {factor:g} {to_u}.\n'
            f'Étape 2 : Multiplie : {v_str} × {factor:g} = {r_str}.\n'
            f'Réponse : {v_str} {from_u} = {r_str} {to_u}'
        ),
    }


def _conversion_distractors(value, result, factor):
    """Wrong answers based on common power-of-10 errors, returned as tagged tuples."""
    r_str = _nice_val(result, factor)
    tagged = []

    # ×10 instead of ×1000
    d1 = _nice_val(value * 10, 10)
    if d1 != r_str:
        tagged.append((
            d1,
            'wrong_unit',
            "Wrong conversion factor — check the relationship between these units.",
            "Mauvais facteur de conversion — vérifie la relation entre ces unités.",
        ))

    # ×100 instead of ×1000
    d2 = _nice_val(value * 100, 100)
    if d2 != r_str:
        tagged.append((
            d2,
            'wrong_unit',
            "Wrong conversion factor — check the relationship between these units.",
            "Mauvais facteur de conversion — vérifie la relation entre ces unités.",
        ))

    # reversed: divide instead of multiply (and vice versa)
    if factor >= 1:
        d3 = _nice_val(value / factor, factor)
    else:
        d3 = _nice_val(value * (1 / factor), 1 / factor)
    if d3 != r_str:
        tagged.append((
            d3,
            'no_conversion',
            "You went the wrong direction — check if you should multiply or divide.",
            "Tu es allé dans le mauvais sens — vérifie si tu dois multiplier ou diviser.",
        ))

    # no conversion at all — used raw value
    d4 = _nice_val(value, 1)
    if d4 != r_str:
        tagged.append((
            d4,
            'no_conversion',
            "You forgot to convert! Apply the conversion factor.",
            "Tu as oublié de convertir ! Applique le facteur de conversion.",
        ))

    # off-by-one zero
    if result >= 10:
        d5 = _nice_val(result / 10, 10)
        if d5 != r_str:
            tagged.append((
                d5,
                'off_by_one',
                "Very close — check your calculation.",
                "Très proche — vérifie ton calcul.",
            ))
        d6 = _nice_val(result * 10, 10)
        if d6 != r_str:
            tagged.append((
                d6,
                'off_by_one',
                "Very close — check your calculation.",
                "Très proche — vérifie ton calcul.",
            ))
    else:
        d5 = _nice_val(result + 10, 10)
        if d5 != r_str:
            tagged.append((
                d5,
                'off_by_one',
                "Very close — check your calculation.",
                "Très proche — vérifie ton calcul.",
            ))
        d6 = _nice_val(result * 100, 100)
        if d6 != r_str:
            tagged.append((
                d6,
                'off_by_one',
                "Very close — check your calculation.",
                "Très proche — vérifie ton calcul.",
            ))

    return tagged


# ── mix_match helpers ─────────────────────────────────────────────────────────

def _conversion_match(table_name, level):
    """Return a mix_match question for the given conversion domain and level."""

    if table_name == 'length':
        if level == 'easy':
            pairs = [
                {'left': '1 km',  'right': '1000 m'},
                {'left': '1 m',   'right': '100 cm'},
                {'left': '1 cm',  'right': '10 mm'},
            ]
        elif level == 'medium':
            pairs = [
                {'left': '500 cm', 'right': '5 m'},
                {'left': '3 km',   'right': '3000 m'},
                {'left': '250 mm', 'right': '25 cm'},
                {'left': '2 m',    'right': '200 cm'},
            ]
        else:  # hard
            pairs = [
                {'left': '2500 m',  'right': '2.5 km'},
                {'left': '0.5 km',  'right': '500 m'},
                {'left': '350 cm',  'right': '3.5 m'},
                {'left': '1500 mm', 'right': '150 cm'},
            ]
        prompt_en = 'Match each measurement to its equivalent.'
        prompt_fr = 'Associez chaque mesure à son équivalent.'
        hint_en   = 'Use the conversion factors: 1 km = 1000 m, 1 m = 100 cm, 1 cm = 10 mm.'
        hint_fr   = 'Utilisez les facteurs : 1 km = 1000 m, 1 m = 100 cm, 1 cm = 10 mm.'

    elif table_name == 'mass':
        if level == 'easy':
            pairs = [
                {'left': '1 kg',  'right': '1000 g'},
                {'left': '1 g',   'right': '1000 mg'},
                {'left': '2 kg',  'right': '2000 g'},
            ]
        elif level == 'medium':
            pairs = [
                {'left': '500 g',  'right': '0.5 kg'},
                {'left': '3 kg',   'right': '3000 g'},
                {'left': '250 mg', 'right': '0.25 g'},
                {'left': '4 g',    'right': '4000 mg'},
            ]
        else:  # hard
            pairs = [
                {'left': '2500 g',  'right': '2.5 kg'},
                {'left': '0.5 kg',  'right': '500 g'},
                {'left': '750 mg',  'right': '0.75 g'},
                {'left': '1500 g',  'right': '1.5 kg'},
            ]
        prompt_en = 'Match each mass to its equivalent.'
        prompt_fr = 'Associez chaque masse à son équivalent.'
        hint_en   = 'Use the conversion factors: 1 kg = 1000 g, 1 g = 1000 mg.'
        hint_fr   = 'Utilisez les facteurs : 1 kg = 1000 g, 1 g = 1000 mg.'

    else:  # volume
        if level == 'easy':
            pairs = [
                {'left': '1 kL',  'right': '1000 L'},
                {'left': '1 L',   'right': '1000 mL'},
                {'left': '2 kL',  'right': '2000 L'},
            ]
        elif level == 'medium':
            pairs = [
                {'left': '500 L',   'right': '0.5 kL'},
                {'left': '3 kL',    'right': '3000 L'},
                {'left': '250 mL',  'right': '0.25 L'},
                {'left': '4 L',     'right': '4000 mL'},
            ]
        else:  # hard
            pairs = [
                {'left': '2500 L',  'right': '2.5 kL'},
                {'left': '0.5 kL',  'right': '500 L'},
                {'left': '750 mL',  'right': '0.75 L'},
                {'left': '1500 L',  'right': '1.5 kL'},
            ]
        prompt_en = 'Match each volume to its equivalent.'
        prompt_fr = 'Associez chaque volume à son équivalent.'
        hint_en   = 'Use the conversion factors: 1 kL = 1000 L, 1 L = 1000 mL.'
        hint_fr   = 'Utilisez les facteurs : 1 kL = 1000 L, 1 L = 1000 mL.'

    explanation_en = 'Correct pairs:\n' + '\n'.join(
        f'{p["left"]} = {p["right"]}' for p in pairs
    )
    explanation_fr = 'Paires correctes :\n' + '\n'.join(
        f'{p["left"]} = {p["right"]}' for p in pairs
    )

    return {
        'q_type':          'mix_match',
        'prompt_en':       prompt_en,
        'prompt_fr':       prompt_fr,
        'hint_en':         hint_en,
        'hint_fr':         hint_fr,
        'shape_data':      [],
        'pairs':           pairs,
        'correct_answers': [],
        'time_limit':      45,
        'points':          3,
        'explanation_en':  explanation_en,
        'explanation_fr':  explanation_fr,
    }


def convert_length_gen(level='medium'):
    if random.random() < 0.40:
        return _conversion_match('length', level)
    return _build_conversion(LENGTH, level, _EASY_LENGTH, _HARD_LENGTH)


def convert_mass_gen(level='medium'):
    if random.random() < 0.40:
        return _conversion_match('mass', level)
    return _build_conversion(MASS, level, _EASY_MASS, _HARD_MASS)


def convert_volume_gen(level='medium'):
    if random.random() < 0.40:
        return _conversion_match('volume', level)
    return _build_conversion(VOLUME, level, _EASY_VOLUME, _HARD_VOLUME)
