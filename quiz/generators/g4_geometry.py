"""
g4_geometry.py — Grade-4 geometry generators (content_g4.md §5).

Topics:
  g4_lines_gen                  QCM + SVG – parallel / perpendicular / intersecting (drawing or definition)
  g4_quadrilateral_name_gen     QCM + SVG – name the quadrilateral from its drawing
  g4_quadrilateral_riddle_gen   QCM       – "J'ai 4 côtés égaux et 4 angles droits. Qui suis-je ?"
  g4_quadrilateral_match_gen    mix_match – definitions ↔ names
  g4_quadrilateral_count_gen    typed     – how many pairs of parallel sides / right angles / equal sides
"""
import random
from .base import _tagged_shuffle_mc

# ─────────────────────────────────────────────────────────────────────────────
# Lines
# ─────────────────────────────────────────────────────────────────────────────

_LINES_FR = {'parallel': 'parallèles', 'perpendicular': 'perpendiculaires', 'intersecting': 'sécantes'}
_LINES_EN = {'parallel': 'parallel', 'perpendicular': 'perpendicular', 'intersecting': 'intersecting'}
_LINE_DEFS = {
    'parallel': [
        ("Deux droites qui ne se rencontrent jamais, même en les prolongeant, sont…",
         "Two lines that never meet, even when extended, are…"),
        ("Deux droites qui gardent toujours le même écart entre elles sont…",
         "Two lines that always stay the same distance apart are…"),
        ("Les deux rails d'un chemin de fer sont…",
         "The two rails of a railway track are…"),
    ],
    'perpendicular': [
        ("Deux droites qui se croisent en formant un angle droit (90°) sont…",
         "Two lines that cross forming a right angle (90°) are…"),
        ("Un mur et le plancher d'une pièce forment des droites…",
         "A wall and the floor of a room form lines that are…"),
        ("Les deux traits du signe « + » sont…",
         "The two strokes of a “+” sign are…"),
    ],
    'intersecting': [
        ("Deux droites qui se croisent en un point sans former d'angle droit sont…",
         "Two lines that cross at a point without forming a right angle are…"),
        ("Les deux traits de la lettre « X » sont des droites…",
         "The two strokes of the letter “X” are lines that are…"),
    ],
}
_LINE_EXPL_FR = {
    'parallel': 'Parallèles : elles ne se croisent jamais et gardent le même écart.',
    'perpendicular': 'Perpendiculaires : elles se croisent en formant un angle droit (90°).',
    'intersecting': 'Sécantes : elles se croisent en un point (sans angle droit).',
}
_LINE_EXPL_EN = {
    'parallel': 'Parallel: they never meet and keep the same distance apart.',
    'perpendicular': 'Perpendicular: they cross forming a right angle (90°).',
    'intersecting': 'Intersecting: they cross at one point (no right angle).',
}


def g4_lines_gen(level='easy'):
    pool = ['parallel', 'perpendicular'] if level == 'easy' else ['parallel', 'perpendicular', 'intersecting']
    relation = random.choice(pool)
    by_definition = level == 'hard' and random.random() < 0.6
    correct = _LINES_FR[relation]
    tagged = [
        (_LINES_FR[r], 'wrong_relation',
         'Parallel: never meet. Perpendicular: cross at 90°. Intersecting: cross without a right angle.',
         'Parallèles : jamais en contact. Perpendiculaires : angle droit. Sécantes : se croisent sans angle droit.')
        for r in ['parallel', 'perpendicular', 'intersecting'] if r != relation
    ]
    tagged += [
        ('horizontales', 'irrelevant_property', 'Horizontal describes direction, not the relation between two lines.',
         "« Horizontales » décrit une direction, pas la relation entre deux droites."),
        ('courbes', 'irrelevant_property', 'These are straight lines.', 'Ce sont des droites, pas des courbes.'),
    ]
    if by_definition:
        d_fr, d_en = random.choice(_LINE_DEFS[relation])
        prompt_fr, prompt_en = d_fr, d_en
        shape_data, show = [], False
    else:
        prompt_fr = 'Ces deux droites sont…'
        prompt_en = 'These two lines are…'
        shape_data, show = [{'type': 'line_pair', 'relation': relation}], True
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Parallèles = jamais en contact. Perpendiculaires = angle droit. Sécantes = se croisent.',
        'hint_en':          'Parallel = never meet. Perpendicular = right angle. Intersecting = they cross.',
        'show_illustration': show,
        'shape_data':       shape_data,
        'choices':          _tagged_shuffle_mc(correct, tagged),
        'pairs':            [],
        'explanation_en':   _LINE_EXPL_EN[relation],
        'explanation_fr':   _LINE_EXPL_FR[relation],
        'correct_answers':  [correct, _LINES_EN[relation]],
        'time_limit':       25, 'points': 1,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Quadrilaterals
# ─────────────────────────────────────────────────────────────────────────────

# kind → (fr, en, pairs_parallel, right_angles, equal_sides_desc, definitions)
QUADS = {
    'square': {
        'fr': 'carré', 'en': 'square', 'parallel_pairs': 2, 'right_angles': 4, 'equal_sides': 4,
        'defs': [
            ("J'ai 4 côtés égaux et 4 angles droits.", 'I have 4 equal sides and 4 right angles.'),
            ("J'ai 2 paires de côtés parallèles, tous mes côtés sont égaux et tous mes angles sont droits.",
             'I have 2 pairs of parallel sides, all my sides are equal and all my angles are right angles.'),
        ],
    },
    'rectangle': {
        'fr': 'rectangle', 'en': 'rectangle', 'parallel_pairs': 2, 'right_angles': 4, 'equal_sides': 2,
        'defs': [
            ("J'ai 4 angles droits et mes côtés opposés sont égaux, mais mes 4 côtés ne sont pas tous égaux.",
             'I have 4 right angles and my opposite sides are equal, but my 4 sides are not all equal.'),
            ("J'ai 2 paires de côtés parallèles et 4 angles droits, mais je ne suis pas un carré.",
             'I have 2 pairs of parallel sides and 4 right angles, but I am not a square.'),
        ],
    },
    'parallelogram': {
        'fr': 'parallélogramme', 'en': 'parallelogram', 'parallel_pairs': 2, 'right_angles': 0, 'equal_sides': 2,
        'defs': [
            ("J'ai 2 paires de côtés parallèles, mais aucun angle droit et mes 4 côtés ne sont pas tous égaux.",
             'I have 2 pairs of parallel sides, but no right angles and my 4 sides are not all equal.'),
            ("Mes côtés opposés sont parallèles et égaux, mais mes angles ne sont pas droits.",
             'My opposite sides are parallel and equal, but my angles are not right angles.'),
        ],
    },
    'rhombus': {
        'fr': 'losange', 'en': 'rhombus', 'parallel_pairs': 2, 'right_angles': 0, 'equal_sides': 4,
        'defs': [
            ("J'ai 4 côtés égaux, mais aucun angle droit.", 'I have 4 equal sides, but no right angles.'),
            ("J'ai 2 paires de côtés parallèles et 4 côtés égaux, mais je ne suis pas un carré.",
             'I have 2 pairs of parallel sides and 4 equal sides, but I am not a square.'),
        ],
    },
    'trapezoid': {
        'fr': 'trapèze', 'en': 'trapezoid', 'parallel_pairs': 1, 'right_angles': 0, 'equal_sides': 0,
        'defs': [
            ("J'ai une seule paire de côtés parallèles.", 'I have exactly one pair of parallel sides.'),
            ("Seulement 2 de mes 4 côtés sont parallèles.", 'Only 2 of my 4 sides are parallel.'),
        ],
    },
}
_KINDS = list(QUADS)


def _props_fr(k):
    q = QUADS[k]
    pp = q['parallel_pairs']
    ra = q['right_angles']
    es = q['equal_sides']
    return (f"{pp} paire{'s' if pp > 1 else ''} de côtés parallèles, "
            f"{ra if ra else 'aucun'} angle{'s' if ra > 1 else ''} droit{'s' if ra > 1 else ''}, "
            f"{'4 côtés égaux' if es == 4 else 'côtés opposés égaux' if es == 2 else 'côtés de longueurs différentes'}")


def _props_en(k):
    q = QUADS[k]
    pp = q['parallel_pairs']
    ra = q['right_angles']
    es = q['equal_sides']
    return (f"{pp} pair{'s' if pp > 1 else ''} of parallel sides, "
            f"{ra if ra else 'no'} right angle{'s' if ra != 1 else ''}, "
            f"{'4 equal sides' if es == 4 else 'opposite sides equal' if es == 2 else 'sides of different lengths'}")


def _kind_distractors(kind):
    return [
        (QUADS[k]['fr'], 'wrong_quadrilateral',
         f'A {QUADS[k]["en"]} has {_props_en(k)}.',
         f'Un {QUADS[k]["fr"]} a {_props_fr(k)}.')
        for k in _KINDS if k != kind
    ]


def g4_quadrilateral_name_gen(level='easy'):
    pool = {'easy': ['square', 'rectangle', 'trapezoid'],
            'medium': _KINDS, 'hard': _KINDS}[level]
    kind = random.choice(pool)
    # Hard: no helper marks (right-angle squares, tick marks) and a random rotation.
    marks = level != 'hard'
    rotate = random.choice([0, 0, 15, -20, 35, 90]) if level != 'easy' else 0
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        'Quel est le nom de ce quadrilatère ?',
        'prompt_en':        'What is the name of this quadrilateral?',
        'hint_fr':          'Regarde les côtés parallèles (flèches), les côtés égaux (petits traits) et les angles droits (petits carrés).',
        'hint_en':          'Look at the parallel sides (arrows), equal sides (tick marks) and right angles (small squares).',
        'show_illustration': True,
        'shape_data':       [{'type': 'quadrilateral', 'kind': kind, 'marks': marks, 'rotate': rotate}],
        'choices':          _tagged_shuffle_mc(QUADS[kind]['fr'], _kind_distractors(kind)),
        'pairs':            [],
        'explanation_en':   f'This shape has {_props_en(kind)} → {QUADS[kind]["en"]}.',
        'explanation_fr':   f'Cette figure a {_props_fr(kind)} → {QUADS[kind]["fr"]}.',
        'correct_answers':  [QUADS[kind]['fr'], QUADS[kind]['en']],
        'time_limit':       25, 'points': 1,
    }


def g4_quadrilateral_riddle_gen(level='easy'):
    pool = {'easy': ['square', 'rectangle', 'trapezoid'], 'medium': _KINDS, 'hard': _KINDS}[level]
    kind = random.choice(pool)
    if level == 'hard' and random.random() < 0.5:
        # Reverse riddle: name → pick the correct description
        correct_fr, correct_en = random.choice(QUADS[kind]['defs'])
        tagged = [(random.choice(QUADS[k]['defs'])[0], 'wrong_property',
                   f'That describes a {QUADS[k]["en"]}.', f'Cela décrit un {QUADS[k]["fr"]}.')
                  for k in _KINDS if k != kind]
        return {
            'q_type':           'multiple_choice',
            'prompt_fr':        f'Quelle phrase décrit un **{QUADS[kind]["fr"]}** ?',
            'prompt_en':        f'Which sentence describes a **{QUADS[kind]["en"]}**?',
            'hint_fr':          f'Un {QUADS[kind]["fr"]} a {_props_fr(kind)}.',
            'hint_en':          f'A {QUADS[kind]["en"]} has {_props_en(kind)}.',
            'show_illustration': False, 'shape_data': [],
            'choices':          _tagged_shuffle_mc(correct_fr, tagged),
            'pairs':            [],
            'explanation_en':   f'A {QUADS[kind]["en"]}: {_props_en(kind)}.',
            'explanation_fr':   f'Un {QUADS[kind]["fr"]} : {_props_fr(kind)}.',
            'correct_answers':  [correct_fr, correct_en],
        }
    d_fr, d_en = random.choice(QUADS[kind]['defs'])
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        f'{d_fr} Qui suis-je ?',
        'prompt_en':        f'{d_en} Who am I?',
        'hint_fr':          'Pense aux côtés parallèles, aux côtés égaux et aux angles droits de chaque quadrilatère.',
        'hint_en':          'Think about the parallel sides, equal sides and right angles of each quadrilateral.',
        'show_illustration': False, 'shape_data': [],
        'choices':          _tagged_shuffle_mc(QUADS[kind]['fr'], _kind_distractors(kind)),
        'pairs':            [],
        'explanation_en':   f'{d_en} → {QUADS[kind]["en"]} ({_props_en(kind)}).',
        'explanation_fr':   f'{d_fr} → {QUADS[kind]["fr"]} ({_props_fr(kind)}).',
        'correct_answers':  [QUADS[kind]['fr'], QUADS[kind]['en']],
    }


def g4_quadrilateral_match_gen(level='easy'):
    count = 3 if level == 'easy' else 4 if level == 'medium' else 5
    kinds = random.sample(_KINDS, count)
    pairs = [{'left': random.choice(QUADS[k]['defs'])[0], 'right': QUADS[k]['fr']} for k in kinds]
    return {
        'q_type':           'mix_match',
        'prompt_fr':        'Associe chaque description au bon quadrilatère.',
        'prompt_en':        'Match each description to the right quadrilateral.',
        'hint_fr':          'Compte les paires de côtés parallèles, les côtés égaux et les angles droits.',
        'hint_en':          'Count the pairs of parallel sides, the equal sides and the right angles.',
        'show_illustration': False, 'shape_data': [],
        'choices':          [],
        'pairs':            pairs,
        'explanation_en':   '\n'.join(f'{QUADS[k]["en"]}: {_props_en(k)}' for k in kinds),
        'explanation_fr':   '\n'.join(f'{QUADS[k]["fr"]} : {_props_fr(k)}' for k in kinds),
        'correct_answers':  [p['right'] for p in pairs],
    }


def g4_quadrilateral_count_gen(level='easy'):
    kind = random.choice(_KINDS)
    prop = random.choice(['parallel_pairs', 'right_angles'] if level == 'easy'
                         else ['parallel_pairs', 'right_angles', 'equal_sides'])
    q = QUADS[kind]
    answer = q[prop]
    q_fr = {'parallel_pairs': 'Combien de paires de côtés parallèles',
            'right_angles': "Combien d'angles droits",
            'equal_sides': 'Au minimum, combien de côtés de même longueur'}[prop]
    q_en = {'parallel_pairs': 'How many pairs of parallel sides',
            'right_angles': 'How many right angles',
            'equal_sides': 'At least how many sides of the same length'}[prop]
    show = level != 'hard'
    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        f"{q_fr} un **{q['fr']}** a-t-il ?",
        'prompt_en':        f"{q_en} does a **{q['en']}** have?",
        'hint_fr':          f"Un {q['fr']} : {_props_fr(kind)}.",
        'hint_en':          f"A {q['en']}: {_props_en(kind)}.",
        'show_illustration': show,
        'shape_data':       [{'type': 'quadrilateral', 'kind': kind, 'marks': True, 'rotate': 0}] if show else [],
        'choices':          [],
        'pairs':            [],
        'explanation_en':   f'A {q["en"]} has {_props_en(kind)}. Answer: {answer}',
        'explanation_fr':   f'Un {q["fr"]} a {_props_fr(kind)}. Réponse : {answer}',
        'correct_answers':  [str(answer)],
    }
