"""
g4_geometry.py — Grade-4 geometry generators (content_g4.md §5).

Topics:
  g4_lines_gen                  QCM + SVG – parallel / perpendicular / intersecting (drawing or definition)
  g4_quadrilateral_name_gen     QCM + SVG – name the quadrilateral from its drawing
  g4_quadrilateral_riddle_gen   QCM       – "J'ai 4 côtés égaux et 4 angles droits. Qui suis-je ?"
  g4_quadrilateral_match_gen    mix_match – definitions ↔ names
  g4_quadrilateral_count_gen    typed     – how many pairs of parallel sides / right angles / equal sides

Quadrilateral names follow the INCLUSIVE hierarchy: a square is also a
rectangle, a rhombus and a parallelogram; a rectangle and a rhombus are
parallelograms.  A trapezoid has exactly one pair of parallel sides (it may
have right angles or equal sides).  Where several names are true, questions
ask for « le nom le plus précis », and every riddle has exactly one most
precise answer (checked in quiz/test_qa_fixes_geometry.py).
"""
import random
from .base import _tagged_shuffle_mc

# ─────────────────────────────────────────────────────────────────────────────
# Lines
# ─────────────────────────────────────────────────────────────────────────────

# Mutually exclusive labels: perpendicular lines are also intersecting, so the
# third relation is « sécantes non perpendiculaires ».
_LINES = {
    'parallel': ('parallèles', 'parallel'),
    'perpendicular': ('perpendiculaires', 'perpendicular'),
    'intersecting': ('sécantes non perpendiculaires', 'intersecting, not perpendicular'),
}
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
        ("Les deux traits de la lettre « X », qui se croisent sans former d'angle droit, sont des droites…",
         "The two strokes of the letter “X”, which cross without forming a right angle, are lines that are…"),
    ],
}
_LINE_EXPL_FR = {
    'parallel': 'Parallèles : elles ne se croisent jamais et gardent le même écart.',
    'perpendicular': 'Perpendiculaires : elles se croisent en formant un angle droit (90°). '
                     'Elles sont aussi sécantes, mais « perpendiculaires » est plus précis.',
    'intersecting': 'Sécantes non perpendiculaires : elles se croisent en un point, sans angle droit.',
}
_LINE_EXPL_EN = {
    'parallel': 'Parallel: they never meet and keep the same distance apart.',
    'perpendicular': 'Perpendicular: they cross forming a right angle (90°). '
                     'They also intersect, but “perpendicular” is more precise.',
    'intersecting': 'Intersecting, not perpendicular: they cross at one point, without a right angle.',
}


def g4_lines_gen(level='easy'):
    pool = ['parallel', 'perpendicular'] if level == 'easy' else ['parallel', 'perpendicular', 'intersecting']
    relation = random.choice(pool)
    by_definition = level == 'hard' and random.random() < 0.6
    tagged = [
        (_LINES[r], 'wrong_relation',
         'Parallel: never meet. Perpendicular: cross at 90°. Intersecting, not perpendicular: cross without a right angle.',
         'Parallèles : jamais en contact. Perpendiculaires : angle droit. Sécantes non perpendiculaires : se croisent sans angle droit.')
        for r in ['parallel', 'perpendicular', 'intersecting'] if r != relation
    ]
    tagged += [
        (('horizontales', 'horizontal'), 'irrelevant_property',
         'Horizontal describes direction, not the relation between two lines.',
         "« Horizontales » décrit une direction, pas la relation entre deux droites."),
        (('courbes', 'curved'), 'irrelevant_property', 'These are straight lines.', 'Ce sont des droites, pas des courbes.'),
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
        'hint_fr':          'Les droites se croisent-elles ? Si oui, forment-elles un angle droit ? '
                            'Choisis la réponse la plus précise.',
        'hint_en':          'Do the lines cross? If they do, do they form a right angle? '
                            'Choose the most precise answer.',
        'show_illustration': show,
        'shape_data':       shape_data,
        'choices':          _tagged_shuffle_mc(_LINES[relation], tagged),
        'pairs':            [],
        'explanation_en':   _LINE_EXPL_EN[relation],
        'explanation_fr':   _LINE_EXPL_FR[relation],
        'correct_answers':  list(_LINES[relation]),
        'time_limit':       25, 'points': 1,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Quadrilaterals
# ─────────────────────────────────────────────────────────────────────────────

# Feature vectors of the possible quadrilaterals (parallel pairs, right angles,
# 4 equal sides).  A trapezoid has exactly one pair of parallel sides.
SQ, RECT, RHO, PARA, TRAP = 'sq', 'rect', 'rho', 'para', 'trap'

# kind → names, the set of feature vectors the NAME covers (inclusive),
#        properties of the DRAWN figure (quiz.geometry_utils 'quadrilateral'),
#        its general definition, and riddles (each tagged with the set of
#        quadrilaterals that satisfy it — used to check the most precise name).
QUADS = {
    'square': {
        'fr': 'carré', 'en': 'square', 'covers': {SQ},
        'parallel_pairs': 2, 'right_angles': 4, 'equal_sides': 4,
        'gen': ('4 côtés égaux et 4 angles droits', '4 equal sides and 4 right angles'),
        'defs': [
            ("J'ai 4 côtés égaux et 4 angles droits.", 'I have 4 equal sides and 4 right angles.', {SQ}),
            ("J'ai 2 paires de côtés parallèles, tous mes côtés sont égaux et tous mes angles sont droits.",
             'I have 2 pairs of parallel sides, all my sides are equal and all my angles are right angles.', {SQ}),
        ],
    },
    'rectangle': {
        'fr': 'rectangle', 'en': 'rectangle', 'covers': {SQ, RECT},
        'parallel_pairs': 2, 'right_angles': 4, 'equal_sides': 2,
        'gen': ('4 angles droits (ses côtés opposés sont égaux)', '4 right angles (its opposite sides are equal)'),
        'defs': [
            ("J'ai 4 angles droits et mes côtés opposés sont égaux, mais mes 4 côtés ne sont pas tous égaux.",
             'I have 4 right angles and my opposite sides are equal, but my 4 sides are not all equal.', {RECT}),
            ("J'ai 4 angles droits.", 'I have 4 right angles.', {SQ, RECT}),
        ],
    },
    'parallelogram': {
        'fr': 'parallélogramme', 'en': 'parallelogram', 'covers': {SQ, RECT, RHO, PARA},
        'parallel_pairs': 2, 'right_angles': 0, 'equal_sides': 2,
        'gen': ('2 paires de côtés parallèles (ses côtés opposés sont égaux)',
                '2 pairs of parallel sides (its opposite sides are equal)'),
        'defs': [
            ("J'ai 2 paires de côtés parallèles.", 'I have 2 pairs of parallel sides.', {SQ, RECT, RHO, PARA}),
            ("Mes côtés opposés sont parallèles et de même longueur.",
             'My opposite sides are parallel and the same length.', {SQ, RECT, RHO, PARA}),
        ],
    },
    'rhombus': {
        'fr': 'losange', 'en': 'rhombus', 'covers': {SQ, RHO},
        'parallel_pairs': 2, 'right_angles': 0, 'equal_sides': 4,
        'gen': ('4 côtés égaux', '4 equal sides'),
        'defs': [
            ("J'ai 4 côtés égaux.", 'I have 4 equal sides.', {SQ, RHO}),
            ("J'ai 2 paires de côtés parallèles et 4 côtés égaux, mais je ne suis pas un carré.",
             'I have 2 pairs of parallel sides and 4 equal sides, but I am not a square.', {RHO}),
        ],
    },
    'trapezoid': {
        'fr': 'trapèze', 'en': 'trapezoid', 'covers': {TRAP},
        # the drawn trapezoid is isosceles, without right angles
        'parallel_pairs': 1, 'right_angles': 0, 'equal_sides': 2,
        'gen': ('une seule paire de côtés parallèles', 'exactly one pair of parallel sides'),
        'defs': [
            ("J'ai une seule paire de côtés parallèles.", 'I have exactly one pair of parallel sides.', {TRAP}),
            ("Seulement 2 de mes 4 côtés sont parallèles.", 'Only 2 of my 4 sides are parallel.', {TRAP}),
        ],
    },
}
_KINDS = list(QUADS)
# A kind is a special case of every other kind whose name covers it.
_SUPER = {k: [j for j in _KINDS if j != k and QUADS[k]['covers'] <= QUADS[j]['covers']] for k in _KINDS}


def most_precise(satisfying):
    """Names that are true for every quadrilateral in ``satisfying``, keeping only the most precise one(s)."""
    true = [k for k in _KINDS if satisfying <= QUADS[k]['covers']]
    return [k for k in true if not any(QUADS[j]['covers'] < QUADS[k]['covers'] for j in true)]


def _drawn_fr(k):
    """Properties of the drawn figure (not general rules)."""
    q = QUADS[k]
    pp, ra = q['parallel_pairs'], q['right_angles']
    sides = {'square': '4 côtés égaux', 'rhombus': '4 côtés égaux', 'rectangle': 'des côtés opposés égaux',
             'parallelogram': 'des côtés opposés égaux', 'trapezoid': ''}[k]
    angles = f'{ra} angles droits' if ra else 'aucun angle droit'
    pairs = f"{pp} paire{'s' if pp > 1 else ''} de côtés parallèles"
    return f'{pairs}, {angles} et {sides}' if sides else f'{pairs} et {angles}'


def _drawn_en(k):
    q = QUADS[k]
    pp, ra = q['parallel_pairs'], q['right_angles']
    sides = {'square': '4 equal sides', 'rhombus': '4 equal sides', 'rectangle': 'equal opposite sides',
             'parallelogram': 'equal opposite sides', 'trapezoid': ''}[k]
    angles = f'{ra} right angles' if ra else 'no right angle'
    pairs = f"{pp} pair{'s' if pp > 1 else ''} of parallel sides"
    return f'{pairs}, {angles} and {sides}' if sides else f'{pairs} and {angles}'


def _art_fr(k):
    return f"un {QUADS[k]['fr']}"


def _art_en(k):
    en = QUADS[k]['en']
    return ('an ' if en[0] in 'aeiou' else 'a ') + en


def _gen_fr(k):
    return f"{_art_fr(k).capitalize()} a {QUADS[k]['gen'][0]}."


def _gen_en(k):
    return f"{_art_en(k).capitalize()} has {QUADS[k]['gen'][1]}."


def _precise_note(kind):
    """« C'est aussi un rectangle…, mais « carré » est le nom le plus précis. »"""
    sup = _SUPER[kind]
    if not sup:
        return '', ''
    fr = ', '.join(_art_fr(k) for k in sup)
    en = ', '.join(_art_en(k) for k in sup)
    return (f" C'est aussi {fr}, mais « {QUADS[kind]['fr']} » est le nom le plus précis.",
            f' It is also {en}, but “{QUADS[kind]["en"]}” is the most precise name.')


def _kind_distractors(kind):
    out = []
    for k in _KINDS:
        if k == kind:
            continue
        if k in _SUPER[kind]:
            fb = (f'True, but not the most precise name: {_art_en(kind)} is a special {QUADS[k]["en"]}.',
                  f"C'est vrai, mais ce n'est pas le nom le plus précis : {_art_fr(kind)} est un {QUADS[k]['fr']} particulier.")
        else:
            fb = (_gen_en(k), _gen_fr(k))
        out.append(((QUADS[k]['fr'], QUADS[k]['en']), 'wrong_quadrilateral', fb[0], fb[1]))
    return out


def g4_quadrilateral_name_gen(level='easy'):
    pool = {'easy': ['square', 'rectangle', 'trapezoid'],
            'medium': _KINDS, 'hard': _KINDS}[level]
    kind = random.choice(pool)
    # Hard: no helper marks (right-angle squares, tick marks) and a random rotation.
    marks = level != 'hard'
    rotate = random.choice([0, 0, 15, -20, 35, 90]) if level != 'easy' else 0
    note = _precise_note(kind)
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        'Quel est le nom le plus précis de ce quadrilatère ?',
        'prompt_en':        'What is the most precise name for this quadrilateral?',
        'hint_fr':          'Regarde les côtés parallèles (flèches), les côtés égaux (petits traits) et les angles droits (petits carrés).',
        'hint_en':          'Look at the parallel sides (arrows), equal sides (tick marks) and right angles (small squares).',
        'show_illustration': True,
        'shape_data':       [{'type': 'quadrilateral', 'kind': kind, 'marks': marks, 'rotate': rotate}],
        'choices':          _tagged_shuffle_mc((QUADS[kind]['fr'], QUADS[kind]['en']), _kind_distractors(kind)),
        'pairs':            [],
        'explanation_en':   f'This shape has {_drawn_en(kind)}: it is {_art_en(kind)}.{note[1]}',
        'explanation_fr':   f'Cette figure a {_drawn_fr(kind)} : c’est {_art_fr(kind)}.{note[0]}',
        'correct_answers':  [QUADS[kind]['fr'], QUADS[kind]['en']],
        'time_limit':       25, 'points': 1,
    }


def g4_quadrilateral_riddle_gen(level='easy'):
    pool = {'easy': ['square', 'rectangle', 'trapezoid'], 'medium': _KINDS, 'hard': _KINDS}[level]
    kind = random.choice(pool)
    if level == 'hard' and random.random() < 0.5:
        # Reverse riddle: name → pick the riddle whose most precise answer is this name
        correct_fr, correct_en, _ = random.choice(QUADS[kind]['defs'])
        tagged = []
        for k in _KINDS:
            if k == kind:
                continue
            d_fr, d_en, _ = random.choice(QUADS[k]['defs'])
            tagged.append(((d_fr, d_en), 'wrong_property',
                           f'The most precise answer to this riddle is {_art_en(k)}.',
                           f'La réponse la plus précise à cette devinette est {_art_fr(k)}.'))
        return {
            'q_type':           'multiple_choice',
            'prompt_fr':        f'Pour quelle devinette « Qui suis-je ? » le nom le plus précis est-il **{QUADS[kind]["fr"]}** ?',
            'prompt_en':        f'For which “Who am I?” riddle is the most precise name **{QUADS[kind]["en"]}**?',
            'hint_fr':          'Pour chaque phrase, cherche le nom le plus précis qui convient. '
                                'Une phrase qui en dit trop peu décrit un quadrilatère plus général.',
            'hint_en':          'For each sentence, find the most precise name that fits. '
                                'A sentence that says too little describes a more general quadrilateral.',
            'show_illustration': False, 'shape_data': [],
            'choices':          _tagged_shuffle_mc((correct_fr, correct_en), tagged),
            'pairs':            [],
            'explanation_en':   f'“{correct_en}” → {_art_en(kind)}. {_gen_en(kind)}',
            'explanation_fr':   f'« {correct_fr} » → {_art_fr(kind)}. {_gen_fr(kind)}',
            'correct_answers':  [correct_fr, correct_en],
        }
    d_fr, d_en, _ = random.choice(QUADS[kind]['defs'])
    note = _precise_note(kind)
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        f'{d_fr} Qui suis-je ? (Donne le nom le plus précis.)',
        'prompt_en':        f'{d_en} Who am I? (Give the most precise name.)',
        'hint_fr':          'Combien de paires de côtés parallèles ? Des angles droits ? Des côtés tous égaux ? '
                            'Garde seulement ce que la devinette dit vraiment.',
        'hint_en':          'How many pairs of parallel sides? Any right angles? All sides equal? '
                            'Use only what the riddle really says.',
        'show_illustration': False, 'shape_data': [],
        'choices':          _tagged_shuffle_mc((QUADS[kind]['fr'], QUADS[kind]['en']), _kind_distractors(kind)),
        'pairs':            [],
        'explanation_en':   f'{d_en} → {_art_en(kind)}. {_gen_en(kind)}{note[1]}',
        'explanation_fr':   f'{d_fr} → {_art_fr(kind)}. {_gen_fr(kind)}{note[0]}',
        'correct_answers':  [QUADS[kind]['fr'], QUADS[kind]['en']],
    }


def g4_quadrilateral_match_gen(level='easy'):
    count = 3 if level == 'easy' else 4 if level == 'medium' else 5
    kinds = random.sample(_KINDS, count)
    pairs = []
    for k in kinds:
        d_fr, d_en, _ = random.choice(QUADS[k]['defs'])
        pairs.append({'left': d_fr, 'left_en': d_en, 'right': QUADS[k]['fr'], 'right_en': QUADS[k]['en']})
    return {
        'q_type':           'mix_match',
        'prompt_fr':        'Associe chaque description au nom le plus précis du quadrilatère.',
        'prompt_en':        'Match each description to the most precise name of the quadrilateral.',
        'hint_fr':          'Compte les paires de côtés parallèles, les côtés égaux et les angles droits.',
        'hint_en':          'Count the pairs of parallel sides, the equal sides and the right angles.',
        'show_illustration': False, 'shape_data': [],
        'choices':          [],
        'pairs':            pairs,
        'explanation_en':   '\n'.join(_gen_en(k) for k in kinds),
        'explanation_fr':   '\n'.join(_gen_fr(k) for k in kinds),
        'correct_answers':  [p['right'] for p in pairs],
    }


_COUNT_Q = {
    'parallel_pairs': ('Combien de paires de côtés parallèles', 'How many pairs of parallel sides'),
    'right_angles': ("Combien d'angles droits", 'How many right angles'),
    'equal_sides': ('Combien de côtés de même longueur', 'How many sides of the same length'),
}
_COUNT_HINT = {
    'parallel_pairs': ('Regarde les côtés opposés deux par deux : se croiseraient-ils si on les prolongeait ?',
                       'Look at the opposite sides two at a time: would they ever meet if you extended them?'),
    'right_angles': ('Observe chaque coin : un petit carré montre un angle droit.',
                     'Look at each corner: a small square shows a right angle.'),
    'equal_sides': ('Les petits traits montrent les côtés de même longueur.',
                    'The small tick marks show the sides of the same length.'),
}
_COUNT_EXPL = {
    'parallel_pairs': ('Ce {name} a {n} paire{s} de côtés opposés qui ne se croisent jamais : {n} paire{s} de côtés parallèles.',
                       'This {name} has {n} pair{s} of opposite sides that never meet: {n} pair{s} of parallel sides.'),
    'right_angles': ('On voit {n} petit{s} carré{s} dans les coins : {n} angle{s} droit{s}.',
                     'There {are} {n} small square{s} in the corners: {n} right angle{s}.'),
    'equal_sides': ('Les petits traits montrent {n} côtés de même longueur.',
                    'The tick marks show {n} sides of the same length.'),
}


def g4_quadrilateral_count_gen(level='easy'):
    """Count a property of the DRAWN figure (always shown), so the key never depends on a general rule."""
    props = ['parallel_pairs', 'right_angles'] if level == 'easy' else ['parallel_pairs', 'right_angles', 'equal_sides']
    prop = random.choice(props)
    # « How many sides of the same length » is only unambiguous when all 4 are equal.
    kinds = ['square', 'rhombus'] if prop == 'equal_sides' else _KINDS
    kind = random.choice(kinds)
    q = QUADS[kind]
    answer = q[prop]
    rotate = random.choice([0, 15, -20, 35, 90]) if level == 'hard' else 0
    s = '' if answer == 1 else 's'
    expl_fr = _COUNT_EXPL[prop][0].format(n=answer, s=s, name=q['fr'])
    expl_en = _COUNT_EXPL[prop][1].format(n=answer, s=s, name=q['en'], are='is' if answer == 1 else 'are')
    if prop == 'right_angles' and answer == 0:
        expl_fr, expl_en = 'Aucun coin n’a de petit carré : 0 angle droit.', 'No corner has a small square: 0 right angles.'
    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        f"{_COUNT_Q[prop][0]} ce {q['fr']} a-t-il ?",
        'prompt_en':        f"{_COUNT_Q[prop][1]} does this {q['en']} have?",
        'hint_fr':          _COUNT_HINT[prop][0],
        'hint_en':          _COUNT_HINT[prop][1],
        'show_illustration': True,
        'shape_data':       [{'type': 'quadrilateral', 'kind': kind, 'marks': True, 'rotate': rotate}],
        'choices':          [],
        'pairs':            [],
        'explanation_en':   f'{expl_en} Answer: {answer}',
        'explanation_fr':   f'{expl_fr} Réponse : {answer}',
        'correct_answers':  [str(answer)],
    }
