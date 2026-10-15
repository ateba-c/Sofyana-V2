"""
geometry_plus.py — curriculum upgrade WP5 (geometry), 2026-10.

Solids from pictures, prisms vs pyramids, nets, convex polygons, triangles,
circles, symmetry, translation, friezes, congruent figures, grid maps and
placing points. Pictures come from ``quiz.illustrations``; answers that are a
picture use letters A–E drawn under each panel.
"""
import random

from quiz import illustrations as I
from .kit import mc, typed, pick

L5 = list('ABCDE')

# ── solids ───────────────────────────────────────────────────────────────────

POLY = ['cube', 'rect-prism', 'tri-prism', 'pent-prism', 'hex-prism',
        'square-pyramid', 'tri-pyramid', 'pent-pyramid', 'hex-pyramid']
ROUND = ['cylinder', 'cone', 'sphere']

NAME = {
    'cube':           ('cube', 'cube'),
    'rect-prism':     ('prisme à base rectangulaire', 'rectangular prism'),
    'tri-prism':      ('prisme à base triangulaire', 'triangular prism'),
    'pent-prism':     ('prisme à base pentagonale', 'pentagonal prism'),
    'hex-prism':      ('prisme à base hexagonale', 'hexagonal prism'),
    'square-pyramid': ('pyramide à base carrée', 'square pyramid'),
    'tri-pyramid':    ('pyramide à base triangulaire', 'triangular pyramid'),
    'pent-pyramid':   ('pyramide à base pentagonale', 'pentagonal pyramid'),
    'hex-pyramid':    ('pyramide à base hexagonale', 'hexagonal pyramid'),
    'cylinder':       ('cylindre', 'cylinder'),
    'cone':           ('cône', 'cone'),
    'sphere':         ('boule', 'sphere'),
}
FAMILY = {k: ('prisme', 'prism') if k.endswith('prism') else ('pyramide', 'pyramid') if k.endswith('pyramid') else NAME[k]
          for k in NAME}


def art(kind, name=None):
    """« un cube » / « une pyramide à base carrée » — (fr, en)."""
    fr, en = name or NAME[kind]
    return (('une ' if fr.startswith('pyramide') or fr == 'boule' else 'un ') + fr,
            ('an ' if en[0] in 'aeiou' else 'a ') + en)


# Faces of each polyhedron: (count, shape) pairs — (fr singular, fr plural, en singular, en plural)
SHAPES = {
    'sq': ('carré', 'carrés', 'square', 'squares'),
    'rect': ('rectangle', 'rectangles', 'rectangle', 'rectangles'),
    'tri': ('triangle', 'triangles', 'triangle', 'triangles'),
    'pent': ('pentagone', 'pentagones', 'pentagon', 'pentagons'),
    'hex': ('hexagone', 'hexagones', 'hexagon', 'hexagons'),
}
FACES = {
    'cube': [(6, 'sq')], 'rect-prism': [(6, 'rect')],
    'tri-prism': [(2, 'tri'), (3, 'rect')], 'pent-prism': [(2, 'pent'), (5, 'rect')],
    'hex-prism': [(2, 'hex'), (6, 'rect')],
    'square-pyramid': [(1, 'sq'), (4, 'tri')], 'tri-pyramid': [(4, 'tri')],
    'pent-pyramid': [(1, 'pent'), (5, 'tri')], 'hex-pyramid': [(1, 'hex'), (6, 'tri')],
}
# faces, vertices, edges
FVE = {'cube': (6, 8, 12), 'rect-prism': (6, 8, 12), 'tri-prism': (5, 6, 9), 'pent-prism': (7, 10, 15),
       'hex-prism': (8, 12, 18), 'square-pyramid': (5, 5, 8), 'tri-pyramid': (4, 4, 6),
       'pent-pyramid': (6, 6, 10), 'hex-pyramid': (7, 7, 12)}


def faces_label(spec):
    fr = ' et '.join(f'{n} {SHAPES[s][0 if n == 1 else 1]}' for n, s in spec)
    en = ' and '.join(f'{n} {SHAPES[s][2 if n == 1 else 3]}' for n, s in spec)
    return fr, en


def _solid_panels(kinds, color=None):
    c, boxes = I.panels(len(kinds), 104, 100)
    for k, box in zip(kinds, boxes):
        I.draw_solid(c, k, box, color or pick(I.PALETTE[:4]))
    return c.shape()


def _letters_mc(prompt, kinds, correct_i, hint, explanation, shape):
    correct = L5[correct_i]
    return mc(prompt, correct, [x for x in L5 if x != correct], hint, explanation, shape=shape)


def g3_solid_picture_gen(level='easy'):
    """Name a solid from its drawing (141, 142, 143)."""
    color = pick(I.PALETTE[:4])
    if level == 'easy':
        kind = pick(['cube', 'sphere', 'cylinder', 'cone', 'square-pyramid', 'rect-prism', 'tri-prism'])
        correct = FAMILY[kind]
        pool = [NAME['cube'], NAME['sphere'], NAME['cylinder'], NAME['cone'], ('pyramide', 'pyramid'), ('prisme', 'prism')]
        return mc(('Quel est ce solide ?', 'What is this solid?'), correct, [p for p in pool if p != correct],
                  ('Regarde les faces : sont-elles plates ou courbes ? Combien de bases ?',
                   'Look at the faces: flat or curved? How many bases?'),
                  (f'C’est {art(kind, correct)[0]}.', f'It is {art(kind, correct)[1]}.'),
                  shape=I.solid(kind, color))
    if level == 'medium' and random.random() < 0.5:
        kind = pick(POLY + ROUND)
        return mc(('Quel est le nom exact de ce solide ?', 'What is the exact name of this solid?'),
                  NAME[kind], [NAME[k] for k in random.sample([k for k in NAME if k != kind], 6)],
                  ('Un prisme a 2 bases identiques ; une pyramide a 1 base et un sommet. Le nom dit la forme de la base.',
                   'A prism has 2 matching bases; a pyramid has 1 base and an apex. The name tells the shape of the base.'),
                  (f'C’est {art(kind)[0]}.', f'It is {art(kind)[1]}.'),
                  shape=I.solid(kind, color))
    if level == 'medium':
        kinds = random.sample(POLY[:6] + ROUND, 5)
        i = random.randrange(5)
        a = art(kinds[i])
        return _letters_mc((f'Quelle figure montre {a[0]} ?', f'Which picture shows {a[1]}?'), kinds, i,
                           ('Compare les bases et les faces de chaque solide.', 'Compare the bases and faces of each solid.'),
                           (f'La figure {L5[i]} est {a[0]}.', f'Picture {L5[i]} is {a[1]}.'),
                           _solid_panels(kinds))
    if random.random() < 0.5:
        # 143 — which faces does this solid have?
        kind = pick(POLY)
        others = [faces_label(FACES[k]) for k in POLY if FACES[k] != FACES[kind]]
        extra = [faces_label([(2, 'sq'), (4, 'tri')]), faces_label([(1, 'tri'), (3, 'rect')]),
                 faces_label([(2, 'hex'), (5, 'rect')])]
        return mc(('Quelles sont les faces de ce solide ?', 'What faces does this solid have?'),
                  faces_label(FACES[kind]), random.sample(others, 4) + extra,
                  ('Compte aussi les faces cachées (traits pointillés).', 'Count the hidden faces too (dashed lines).'),
                  (f'{art(kind)[0].capitalize()} a {faces_label(FACES[kind])[0]}.',
                   f'{art(kind)[1].capitalize()} has {faces_label(FACES[kind])[1]}.'),
                  shape=I.solid(kind, color))
    # 142 — curved and flat surfaces
    target = pick(ROUND)
    desc = {'sphere': ('n’a qu’une surface courbe, aucune face plane', 'has only a curved surface, no flat face'),
            'cone': ('a une surface courbe et une seule face plane', 'has a curved surface and only one flat face'),
            'cylinder': ('a une surface courbe et deux faces planes', 'has a curved surface and two flat faces')}[target]
    kinds = [k for k in ROUND] + random.sample(POLY[:6], 2)
    random.shuffle(kinds)
    i = kinds.index(target)
    return _letters_mc((f'Quel solide {desc[0]} ?', f'Which solid {desc[1]}?'), kinds, i,
                       ('Une face plane est toute plate ; une surface courbe peut rouler.',
                        'A flat face is perfectly flat; a curved surface can roll.'),
                       (f'La figure {L5[i]} : {art(target)[0]}.', f'Picture {L5[i]}: {art(target)[1]}.'),
                       _solid_panels(kinds))


def g3_prism_or_pyramid_gen(level='easy'):
    """Classify prisms and pyramids, name them by their base; polyhedron vocabulary (145, 152)."""
    color = pick(I.PALETTE[:4])
    if level == 'easy':
        kind = pick(POLY[1:])
        fam = FAMILY[kind]
        pool = [('prisme', 'prism'), ('pyramide', 'pyramid'), NAME['cylinder'], NAME['cone'], NAME['sphere']]
        return mc(('Ce solide est-il un prisme ou une pyramide ?', 'Is this solid a prism or a pyramid?'),
                  fam, [p for p in pool if p != fam],
                  ('Un prisme a 2 bases pareilles reliées par des rectangles. Une pyramide a 1 base et des triangles qui se rejoignent en un sommet.',
                   'A prism has 2 matching bases joined by rectangles. A pyramid has 1 base and triangles meeting at an apex.'),
                  (f'C’est {art(kind, fam)[0]} : {"2 bases et des faces rectangulaires" if fam[0] == "prisme" else "1 base et des faces triangulaires"}.',
                   f'It is {art(kind, fam)[1]}: {"2 bases and rectangular faces" if fam[1] == "prism" else "1 base and triangular faces"}.'),
                  shape=I.solid(kind, color))
    if level == 'medium':
        kind = pick(POLY[1:])
        base = kind.split('-')[0]
        twin = f'{base}-{"pyramid" if kind.endswith("prism") else "prism"}'
        same_family = [k for k in POLY[1:] if k.split('-')[1] == kind.split('-')[1] and k != kind]
        distractors = ([NAME[twin]] if twin in NAME else []) + [NAME[k] for k in same_family]
        distractors += [NAME[k] for k in POLY[1:] if k != kind]
        return mc(('Quel est le nom de ce solide ?', 'What is the name of this solid?'),
                  NAME[kind], distractors,
                  ('D’abord : prisme ou pyramide ? Ensuite : quelle est la forme de la base ?',
                   'First: prism or pyramid? Then: what shape is the base?'),
                  (f'C’est {art(kind)[0]}.', f'It is {art(kind)[1]}.'),
                  shape=I.solid(kind, color))
    if random.random() < 0.5:
        kind = pick(POLY[2:])
        n_b = FACES[kind][0]
        if kind.endswith('prism'):
            b = SHAPES[FACES[kind][0][1]]
            riddle = (f'Je suis un polyèdre. J’ai 2 bases en forme de {b[0]} et {FACES[kind][1][0]} faces rectangulaires. Qui suis-je ?',
                      f'I am a polyhedron. I have 2 {b[3]} as bases and {FACES[kind][1][0]} rectangular faces. Who am I?')
        elif kind == 'tri-pyramid':
            riddle = ('Je suis un polyèdre. J’ai 4 faces, toutes des triangles, et 4 sommets. Qui suis-je ?',
                      'I am a polyhedron. I have 4 faces, all triangles, and 4 vertices. Who am I?')
        else:
            b = SHAPES[n_b[1]]
            riddle = (f'Je suis un polyèdre. J’ai une base en forme de {b[0]} et {FACES[kind][1][0]} faces triangulaires qui se rejoignent en un sommet. Qui suis-je ?',
                      f'I am a polyhedron. I have a {b[2]} base and {FACES[kind][1][0]} triangular faces meeting at one apex. Who am I?')
        return mc(riddle, NAME[kind], [NAME[k] for k in POLY[1:] if k != kind],
                  ('Deux bases → prisme. Une base et un sommet → pyramide.', 'Two bases → prism. One base and an apex → pyramid.'),
                  (f'C’est {art(kind)[0]}.', f'It is {art(kind)[1]}.'))
    # 152 — polyhedron: a solid made only of flat polygon faces
    odd = pick(ROUND)
    kinds = random.sample(POLY, 4) + [odd]
    random.shuffle(kinds)
    i = kinds.index(odd)
    return _letters_mc(('Lequel de ces solides n’est **pas** un polyèdre ?', 'Which of these solids is **not** a polyhedron?'),
                       kinds, i,
                       ('Un polyèdre n’a que des faces planes en forme de polygones.', 'A polyhedron has only flat faces shaped like polygons.'),
                       (f'La figure {L5[i]} ({art(odd)[0]}) a une surface courbe : ce n’est pas un polyèdre.',
                        f'Picture {L5[i]} ({art(odd)[1]}) has a curved surface: it is not a polyhedron.'),
                       _solid_panels(kinds))


# ── nets ─────────────────────────────────────────────────────────────────────

def _net_panels(specs, color=None):
    """specs: [(kind, variant)]"""
    c, boxes = I.panels(len(specs), 120, 110)
    for (k, v), box in zip(specs, boxes):
        I.draw_net(c, k, box, color or BLUE, v)
    return c.shape()


def _solid_and_nets(kind, specs, i, prompt, hint, explanation, color):
    pic = I.solid(kind, color, size=120)
    return _letters_mc(prompt, specs, i, hint, explanation, [pic, _net_panels(specs, color)])


def g3_net_match_gen(level='easy'):
    """Match a net with its prism (146, 147, 150)."""
    color = pick(I.PALETTE[:4])
    pool = ['cube', 'rect-prism', 'cylinder'] if level == 'easy' else ['cube', 'rect-prism', 'tri-prism', 'pent-prism', 'hex-prism', 'cylinder']
    kind = pick(pool)
    if level != 'hard':
        distractors = [NAME[k] for k in ['cube', 'rect-prism', 'tri-prism', 'hex-prism', 'cylinder', 'cone', 'square-pyramid'] if k != kind]
        return mc(('Ce **développement** se replie pour former quel solide ?', 'This **net** folds up into which solid?'),
                  NAME[kind], distractors,
                  ('Un développement montre toutes les faces à plat. Compte les bases et regarde leur forme.',
                   'A net shows every face laid flat. Count the bases and look at their shape.'),
                  (f'Replié, ce développement donne {art(kind)[0]}.',
                   f'Folded up, this net makes {art(kind)[1]}.'),
                  shape=I.net(kind, color, variant=random.randrange(3)))
    others = [k for k in ['cube', 'rect-prism', 'tri-prism', 'pent-prism', 'hex-prism', 'square-pyramid', 'cylinder', 'cone'] if k != kind]
    specs = [(kind, random.randrange(3))] + [(k, random.randrange(3)) for k in random.sample(others, 4)]
    random.shuffle(specs)
    i = [s[0] for s in specs].index(kind)
    return _solid_and_nets(kind, specs, i,
                           (f'Quel développement correspond à ce solide ({NAME[kind][0]}) ?', f'Which net matches this solid ({NAME[kind][1]})?'),
                           ('Les bases du solide doivent apparaître dans le développement, avec le bon nombre de faces.',
                            'The solid’s bases must appear in the net, with the right number of faces.'),
                           (f'Le développement {L5[i]} : il a les mêmes faces que {art(kind)[0]}.',
                            f'Net {L5[i]}: it has the same faces as {art(kind)[1]}.'), color)


def g4_net_pyramid_gen(level='easy'):
    """Match a net with its pyramid (148)."""
    color = pick(I.PALETTE[:4])
    pyr = ['square-pyramid', 'tri-pyramid', 'pent-pyramid', 'hex-pyramid']
    kind = pick(pyr[:2] if level == 'easy' else pyr)
    if level == 'easy' or (level == 'medium' and random.random() < 0.5):
        distractors = [NAME[k] for k in pyr if k != kind] + [NAME['cone'], NAME[kind.split('-')[0] + '-prism'] if kind != 'square-pyramid' else NAME['cube']]
        return mc(('Ce développement se replie pour former quel solide ?', 'This net folds up into which solid?'),
                  NAME[kind], distractors,
                  ('La face du milieu est la base ; les triangles autour se rejoignent en un sommet.',
                   'The middle face is the base; the triangles around it meet at the apex.'),
                  (f'Une base et {FACES[kind][-1][0]} triangles : {art(kind)[0]}.' if kind != 'tri-pyramid'
                   else 'Quatre triangles : une pyramide à base triangulaire.',
                   f'One base and {FACES[kind][-1][0]} triangles: {art(kind)[1]}.' if kind != 'tri-pyramid'
                   else 'Four triangles: a triangular pyramid.'),
                  shape=I.net(kind, color))
    if level == 'medium':
        base = kind.split('-')[0]
        wrong = [(base + '-prism' if base != 'square' else 'cube', 0), ('bad-pyramid', 0), ('cone', 0),
                 (pick([k for k in pyr if k != kind]), 0)]
        specs = [(kind, 0)] + wrong
        random.shuffle(specs)
        i = [s[0] for s in specs].index(kind)
        return _solid_and_nets(kind, specs, i,
                               (f'Quel développement correspond à cette pyramide ({NAME[kind][0]}) ?',
                                f'Which net matches this pyramid ({NAME[kind][1]})?'),
                               ('Il faut la bonne base et un triangle sur chacun de ses côtés.',
                                'You need the right base and one triangle on each of its sides.'),
                               (f'Le développement {L5[i]}.', f'Net {L5[i]}.'), color)
    n = FVE[kind][0] - 1
    ask = pick(['tri', 'faces'])
    if ask == 'tri':
        ans = n if kind != 'tri-pyramid' else 4
        return typed((f'Combien de triangles y a-t-il dans le développement d’une {NAME[kind][0]} ?',
                      f'How many triangles are in the net of a {NAME[kind][1]}?'),
                     [ans], 'integer',
                     ('Une pyramide a un triangle sur chaque côté de sa base.', 'A pyramid has one triangle on each side of its base.'),
                     (f'La base a {n} côtés → {n} triangles' + (' (et la base est aussi un triangle : 4).' if kind == 'tri-pyramid' else '.'),
                      f'The base has {n} sides → {n} triangles' + (' (and the base is a triangle too: 4).' if kind == 'tri-pyramid' else '.')))
    return typed((f'Combien de faces en tout a le développement d’une {NAME[kind][0]} ?',
                  f'How many faces in all does the net of a {NAME[kind][1]} have?'),
                 [FVE[kind][0]], 'integer',
                 ('Compte la base, puis un triangle par côté de la base.', 'Count the base, then one triangle per side of the base.'),
                 (f'1 base + {n} triangles = {FVE[kind][0]} faces.', f'1 base + {n} triangles = {FVE[kind][0]} faces.'))


def g6_polyhedron_net_gen(level='easy'):
    """Convex polyhedron ↔ net; faces/vertices/edges from a net (149, 150)."""
    color = pick(I.PALETTE[:4])
    if level == 'easy':
        kind = pick(POLY)
        others = [k for k in POLY if k != kind]
        specs = [(kind, random.randrange(3))] + [(k, 0) for k in random.sample(others, 4)]
        random.shuffle(specs)
        i = [s[0] for s in specs].index(kind)
        return _solid_and_nets(kind, specs, i,
                               ('Quel développement se replie pour former ce polyèdre ?', 'Which net folds up into this polyhedron?'),
                               ('Compare la forme et le nombre des faces.', 'Compare the shape and number of faces.'),
                               (f'Le développement {L5[i]} a {faces_label(FACES[kind])[0]}, comme {art(kind)[0]}.',
                                f'Net {L5[i]} has {faces_label(FACES[kind])[1]}, like {art(kind)[1]}.'), color)
    if level == 'medium':
        # same faces, only one arrangement folds
        if random.random() < 0.6:
            specs = [('cube', random.randrange(3))] + [('bad-cube', v) for v in range(3)] + [('rect-prism', 0)]
            kind = 'cube'
        else:
            specs = [('square-pyramid', 0), ('bad-pyramid', 0), ('cube', 1), ('tri-pyramid', 0), ('pent-pyramid', 0)]
            kind = 'square-pyramid'
        random.shuffle(specs)
        i = [s[0] for s in specs].index(kind)
        return _letters_mc((f'Lequel de ces dessins se replie vraiment en {art(kind)[0]} ?',
                            f'Which of these drawings really folds up into a {NAME[kind][1]}?'),
                           specs, i,
                           ('Imagine que tu plies les faces : deux faces ne doivent jamais se superposer et il ne doit manquer aucune face.',
                            'Imagine folding the faces: no two faces may overlap and no face may be missing.'),
                           (f'Seul le dessin {L5[i]} se replie sans trou ni superposition.',
                            f'Only drawing {L5[i]} folds up with no gap and no overlap.'),
                           _net_panels(specs, color))
    kind = pick(POLY[2:])
    f, v, e = FVE[kind]
    what = pick(['faces', 'sommets', 'arêtes'])
    ans, en = {'faces': (f, 'faces'), 'sommets': (v, 'vertices'), 'arêtes': (e, 'edges')}[what]
    return typed((f'On replie ce développement. Combien de **{what}** aura le polyèdre obtenu ?',
                  f'This net is folded up. How many **{en}** will the polyhedron have?'),
                 [ans], 'integer',
                 ('Reconnais d’abord le solide. Relation d’Euler : faces + sommets − arêtes = 2.',
                  'First recognise the solid. Euler’s rule: faces + vertices − edges = 2.'),
                 ([f'C’est {art(kind)[0]}.', f'{f} faces, {v} sommets, {e} arêtes ({f} + {v} − {e} = 2).'],
                  [f'It is {art(kind)[1]}.', f'{f} faces, {v} vertices, {e} edges ({f} + {v} − {e} = 2).']),
                 shape=I.net(kind, color, variant=random.randrange(2)))


# ── convex polygons ──────────────────────────────────────────────────────────

def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def is_convex(pts):
    n = len(pts)
    signs = {_cross(pts[i], pts[(i + 1) % n], pts[(i + 2) % n]) > 0 for i in range(n)}
    return len(signs) == 1


def convex_polygon(n):
    import math
    while True:
        angles = sorted(random.uniform(0, 2 * math.pi) for _ in range(n))
        gaps = [(angles[(i + 1) % n] - angles[i]) % (2 * math.pi) for i in range(n)]
        if min(gaps) > 0.6 and max(gaps) < 2.6:
            return [(math.cos(a), math.sin(a)) for a in angles]


def concave_polygon(n, depth):
    """A non-convex polygon: one vertex of a convex polygon pushed inward (depth 0.3 subtle … 0.9 obvious)."""
    while True:
        pts = convex_polygon(n)
        i = random.randrange(n)
        a, b = pts[i - 1], pts[(i + 1) % n]
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        # move vertex i past the chord a–b, towards the centre
        pts[i] = (m[0] * (1 - depth), m[1] * (1 - depth))
        if not is_convex(pts):
            return pts


def g3_convex_gen(level='easy'):
    """Convex and non-convex polygons (157)."""
    depth = {'easy': 0.85, 'medium': 0.6, 'hard': 0.35}[level]
    want_convex = level != 'easy' and random.random() < 0.5
    polys = []
    for k in range(5):
        n = random.randint(4, 7) if level != 'easy' else random.randint(4, 6)
        polys.append(convex_polygon(n) if (k == 0) == want_convex else concave_polygon(n, depth))
    order = list(range(5))
    random.shuffle(order)
    polys = [polys[j] for j in order]
    i = order.index(0)
    c, boxes = I.panels(5, 100, 92)
    for p, box in zip(polys, boxes):
        I.draw_polygon(c, p, box, pick(I.PALETTE[:4]))
    word = ('convexe', 'convex') if want_convex else ('non convexe', 'non-convex')
    return _letters_mc((f'Quel polygone est **{word[0]}** ?', f'Which polygon is **{word[1]}**?'), polys, i,
                       ('Un polygone non convexe a un « creux » : un angle rentrant qui pointe vers l’intérieur.',
                        'A non-convex polygon has a “dent”: a corner pointing inwards.'),
                       ((f'Le polygone {L5[i]} n’a aucun creux : il est convexe. Les autres ont un angle rentrant.' if want_convex
                         else f'Le polygone {L5[i]} a un angle rentrant (un creux) : il est non convexe.'),
                        (f'Polygon {L5[i]} has no dent: it is convex. The others have a corner pointing inwards.' if want_convex
                         else f'Polygon {L5[i]} has a corner pointing inwards (a dent): it is non-convex.')),
                       c.shape())


# ── triangles ────────────────────────────────────────────────────────────────

TRI_TYPES = {
    'equi':        ('équilatéral', 'equilateral'),
    'iso-right':   ('isocèle et rectangle', 'isosceles and right'),
    'iso':         ('isocèle, non rectangle', 'isosceles, not right'),
    'scal-right':  ('scalène et rectangle', 'scalene and right'),
    'scal':        ('scalène, non rectangle', 'scalene, not right'),
}


def _triangle_of(kind):
    """Vertices (y down), equal-side tick groups, right-angle vertex, side lengths, angles."""
    import math
    if kind == 'equi':
        s = pick([4, 5, 6, 7, 8])
        pts = [(0, 0), (s, 0), (s / 2, -s * math.sqrt(3) / 2)]
        return pts, {0: 1, 1: 1, 2: 1}, None, (s, s, s), (60, 60, 60)
    if kind == 'iso-right':
        s = pick([3, 4, 5, 6])
        pts = [(0, 0), (s, 0), (0, -s)]
        return pts, {0: 1, 2: 1}, 0, (s, None, s), (90, 45, 45)
    if kind == 'scal-right':
        a, b, h = pick([(3, 4, 5), (6, 8, 10), (5, 12, 13), (4, 3, 5), (8, 6, 10)])
        pts = [(0, 0), (a, 0), (0, -b)]
        return pts, {}, 0, (a, h, b), None
    if kind == 'iso':
        base, apex = pick([(4, 6), (6, 5), (6, 8), (8, 6), (4, 7)])
        hgt = math.sqrt(apex ** 2 - (base / 2) ** 2)
        pts = [(0, 0), (base, 0), (base / 2, -hgt)]
        return pts, {1: 1, 2: 1}, None, (base, apex, apex), None
    a, b, cc = pick([(4, 6, 7), (5, 7, 9), (6, 8, 9), (5, 6, 8), (7, 8, 10)])
    # place side a on the base, third vertex from the two other lengths
    x = (a * a + cc * cc - b * b) / (2 * a)
    y = math.sqrt(max(cc * cc - x * x, 0.1))
    pts = [(0, 0), (a, 0), (x, -y)]
    return pts, {}, None, (a, b, cc), None


def g6_triangle_type_gen(level='easy'):
    """Classify triangles by sides and by angles (162, 163, 165)."""
    kind = pick(list(TRI_TYPES))
    pts, ticks, right, sides, _ang = _triangle_of(kind)
    hint = ('Regarde d’abord les côtés (3 égaux, 2 égaux ou aucun), puis cherche un angle droit.',
            'First look at the sides (3 equal, 2 equal or none), then look for a right angle.')
    expl_fr = {'equi': 'Trois côtés égaux : triangle équilatéral (il n’a jamais d’angle droit).',
               'iso-right': 'Deux côtés égaux et un angle droit : triangle isocèle et rectangle.',
               'iso': 'Deux côtés égaux, pas d’angle droit : triangle isocèle.',
               'scal-right': 'Trois côtés différents et un angle droit : triangle scalène et rectangle.',
               'scal': 'Trois côtés différents, pas d’angle droit : triangle scalène.'}[kind]
    expl_en = {'equi': 'Three equal sides: equilateral triangle (it never has a right angle).',
               'iso-right': 'Two equal sides and a right angle: isosceles right triangle.',
               'iso': 'Two equal sides, no right angle: isosceles triangle.',
               'scal-right': 'Three different sides and a right angle: scalene right triangle.',
               'scal': 'Three different sides, no right angle: scalene triangle.'}[kind]
    distractors = [v for k, v in TRI_TYPES.items() if k != kind]
    if level == 'easy':
        return mc(('Quel est ce triangle ? (Les petits traits montrent les côtés égaux.)',
                   'What kind of triangle is this? (The small marks show equal sides.)'),
                  TRI_TYPES[kind], distractors, hint, (expl_fr, expl_en),
                  shape=I.triangle(pts, ticks=ticks, right_at=right, color=pick(I.PALETTE[:4])))
    if level == 'medium':
        labels = [f'{s} cm' if s else '' for s in sides]
        return mc(('Quel est ce triangle ? Utilise les longueurs.', 'What kind of triangle is this? Use the lengths.'),
                  TRI_TYPES[kind], distractors, hint, (expl_fr, expl_en),
                  shape=I.triangle(pts, right_at=right, labels=labels, color=pick(I.PALETTE[:4])))
    if kind in ('equi', 'iso-right') or random.random() < 0.5:
        if kind == 'equi':
            angs = '60°, 60° et 60°', '60°, 60° and 60°'
        elif kind == 'iso-right':
            angs = '90°, 45° et 45°', '90°, 45° and 45°'
        elif kind == 'scal-right':
            a = random.choice([30, 35, 40, 50, 55, 60, 25, 65])
            angs = f'90°, {a}° et {90 - a}°', f'90°, {a}° and {90 - a}°'
        elif kind == 'iso':
            a = random.choice([40, 50, 70, 75, 80, 35])
            angs = f'{a}°, {a}° et {180 - 2 * a}°', f'{a}°, {a}° and {180 - 2 * a}°'
        else:
            a, b = random.choice([(40, 60), (50, 70), (35, 65), (30, 70), (45, 75), (55, 80)])
            angs = f'{a}°, {b}° et {180 - a - b}°', f'{a}°, {b}° and {180 - a - b}°'
        return mc((f'Les angles d’un triangle mesurent {angs[0]}. Quel est ce triangle ?',
                   f'The angles of a triangle measure {angs[1]}. What kind of triangle is it?'),
                  TRI_TYPES[kind], distractors,
                  ('Deux angles égaux ↔ deux côtés égaux. Un angle de 90° → triangle rectangle.',
                   'Two equal angles ↔ two equal sides. A 90° angle → right triangle.'),
                  (expl_fr, expl_en))
    s = [x for x in sides if x] if kind != 'scal-right' else list(sides)
    s_txt = (f'{s[0]} cm, {s[1]} cm et {s[2]} cm', f'{s[0]} cm, {s[1]} cm and {s[2]} cm')
    extra = (' Il a un angle droit.', ' It has a right angle.') if right is not None else (' Il n’a pas d’angle droit.', ' It has no right angle.')
    return mc((f'Les côtés d’un triangle mesurent {s_txt[0]}.{extra[0]} Quel est ce triangle ?',
               f'The sides of a triangle measure {s_txt[1]}.{extra[1]} What kind of triangle is it?'),
              TRI_TYPES[kind], distractors, hint, (expl_fr, expl_en))


# ── circle ───────────────────────────────────────────────────────────────────

CIRCLE_PARTS = {
    'radius':        ('rayon', 'radius'),
    'diameter':      ('diamètre', 'diameter'),
    'chord':         ('corde', 'chord'),
    'circumference': ('circonférence', 'circumference'),
    'central-angle': ('angle au centre', 'central angle'),
}


def g6_circle_parts_gen(level='easy'):
    """Radius, diameter, chord, circumference, central angle; d = 2 × r (164, 165)."""
    if level == 'easy':
        part = pick(list(CIRCLE_PARTS))
        expl = {'radius': ('Le rayon relie le centre O à un point du cercle.', 'The radius joins the centre O to a point on the circle.'),
                'diameter': ('Le diamètre traverse le cercle en passant par le centre O.', 'The diameter crosses the circle through the centre O.'),
                'chord': ('Une corde relie deux points du cercle sans passer par le centre.', 'A chord joins two points of the circle without going through the centre.'),
                'circumference': ('La circonférence est le tour du cercle (sa longueur).', 'The circumference is the distance around the circle.'),
                'central-angle': ('L’angle au centre a son sommet au centre O, entre deux rayons.', 'A central angle has its vertex at the centre O, between two radii.')}[part]
        return mc(('Comment s’appelle la partie en rouge ?', 'What is the part shown in red called?'),
                  CIRCLE_PARTS[part], [v for k, v in CIRCLE_PARTS.items() if k != part],
                  ('Le point O est le centre du cercle.', 'Point O is the centre of the circle.'), expl,
                  shape=I.circle_parts(part, color=pick(I.PALETTE[:4]), angle=random.choice([50, 70, 90, 110])))
    if level == 'medium':
        r = random.randint(2, 15)
        if random.random() < 0.5:
            return typed((f'Le rayon de ce cercle mesure {r} cm. Combien mesure son diamètre ?',
                          f'The radius of this circle is {r} cm. How long is its diameter?'),
                         [r * 2], 'integer',
                         ('Le diamètre vaut deux rayons.', 'The diameter is two radii long.'),
                         (f'd = 2 × r = 2 × {r} = {2 * r} cm', f'd = 2 × r = 2 × {r} = {2 * r} cm'),
                         shape=I.circle_parts('radius', value=f'{r} cm'))
        return typed((f'Le diamètre de ce cercle mesure {2 * r} cm. Combien mesure son rayon ?',
                      f'The diameter of this circle is {2 * r} cm. How long is its radius?'),
                     [r], 'integer',
                     ('Le rayon est la moitié du diamètre.', 'The radius is half of the diameter.'),
                     (f'r = d ÷ 2 = {2 * r} ÷ 2 = {r} cm', f'r = d ÷ 2 = {2 * r} ÷ 2 = {r} cm'),
                     shape=I.circle_parts('diameter', value=f'{2 * r} cm'))
    if random.random() < 0.5:
        n = pick([2, 3, 4, 5, 6, 8, 9, 10, 12])
        return typed((f'Une pizza ronde est coupée en {n} parts égales à partir du centre. Combien de degrés mesure l’angle au centre de chaque part ?',
                      f'A round pizza is cut into {n} equal slices from the centre. How many degrees is the central angle of each slice?'),
                     [360 // n], 'integer',
                     ('Un tour complet autour du centre mesure 360°.', 'A full turn around the centre is 360°.'),
                     (f'360° ÷ {n} = {360 // n}°', f'360° ÷ {n} = {360 // n}°'))
    r = random.randint(3, 25)
    a = pick(['d-from-r', 'r-from-d', 'two-r'])
    if a == 'two-r':
        return typed((f'Deux cercles identiques sont posés côte à côte, sans espace, sur une ligne droite. Chacun a un rayon de {r} cm. Quelle longueur occupent-ils ?',
                      f'Two identical circles sit side by side on a straight line with no gap. Each has a radius of {r} cm. How long a stretch do they cover?'),
                     [4 * r], 'integer',
                     ('Chaque cercle occupe son diamètre.', 'Each circle covers its diameter.'),
                     (f'Un diamètre = 2 × {r} = {2 * r} cm ; deux diamètres = {4 * r} cm.', f'One diameter = 2 × {r} = {2 * r} cm; two diameters = {4 * r} cm.'))
    if a == 'd-from-r':
        return typed((f'Une roue a un rayon de {r} cm. Quel est son diamètre ?', f'A wheel has a radius of {r} cm. What is its diameter?'),
                     [2 * r], 'integer', ('d = 2 × r', 'd = 2 × r'),
                     (f'2 × {r} = {2 * r} cm', f'2 × {r} = {2 * r} cm'))
    return typed((f'Une table ronde a un diamètre de {2 * r} dm. Quel est son rayon ?', f'A round table has a diameter of {2 * r} dm. What is its radius?'),
                 [r], 'integer', ('r = d ÷ 2', 'r = d ÷ 2'),
                 (f'{2 * r} ÷ 2 = {r} dm', f'{2 * r} ÷ 2 = {r} dm'))


# ── square-grid motifs (symmetry, translation, friezes, congruence) ─────────

def _norm(cells):
    mx, my = min(x for x, _ in cells), min(y for _, y in cells)
    return frozenset((x - mx, y - my) for x, y in cells)


def _mirror_v(cells):
    return _norm({(-x, y) for x, y in cells})


def _mirror_h(cells):
    return _norm({(x, -y) for x, y in cells})


def _rot90(cells):
    return _norm({(-y, x) for x, y in cells})


def _connected(cells):
    cells = set(cells)
    start = next(iter(cells))
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n in cells and n not in seen:
                seen.add(n)
                todo.append(n)
    return len(seen) == len(cells)


def motif(n_cells, w=3, h=3, asymmetric=True):
    """A connected set of cells in a w×h box with no line of symmetry and no half-turn symmetry."""
    while True:
        cells = _norm(set(random.sample([(x, y) for x in range(w) for y in range(h)], n_cells)))
        if not _connected(cells):
            continue
        if asymmetric:
            rot180 = _mirror_h(_mirror_v(cells))
            if cells in (_mirror_v(cells), _mirror_h(cells), rot180, _rot90(cells)):
                continue
        return cells


def _size(cells):
    return max(x for x, _ in cells) + 1, max(y for _, y in cells) + 1


def _place(cells, dx, dy, color):
    return {(x + dx, y + dy): color for x, y in cells}


def g3_symmetry_axis_gen(level='easy'):
    """Lines of symmetry: spot the axis, complete a figure, count axes (168, 170)."""
    blue, red = I.SHADES[I.BLUE][2], I.SHADES[I.RED][2]
    if level == 'easy':
        # which dashed line is an axis of symmetry?
        c, boxes = I.panels(5, 104, 104)
        good = random.randrange(5)
        for k, box in enumerate(boxes):
            half = motif(random.randint(3, 4), 3, 4, asymmetric=False)
            vertical = random.random() < 0.5
            if k == good:
                full = set(half) | {(5 - x, y) for x, y in half}
            elif k % 2:
                full = set(half) | {(x + 3, y) for x, y in half}      # copied, not mirrored
                if _mirror_v(full) == _norm(full):
                    full = set(half) | {(5 - x, y) for x, y in half} | {(0, 4)}
            else:
                full = set(half) | {(5 - x, y) for x, y in half} | {(random.choice([0, 1, 2]), 4)}  # one extra square
            cells = {(x, y) if vertical else (y, x): blue for x, y in full}
            I.draw_grid(c, box, 6, 6, cells=cells, axis=('v', 3) if vertical else ('h', 3))
        return _letters_mc(('Dans quelle figure la ligne rouge est-elle un **axe de symétrie** ?',
                            'In which picture is the red line a **line of symmetry**?'),
                           boxes, good,
                           ('Plie la figure le long de la ligne : les deux moitiés doivent se superposer exactement.',
                            'Fold the picture along the line: both halves must match exactly.'),
                           (f'Figure {L5[good]} : chaque carré a son reflet à la même distance de l’autre côté de la ligne.',
                            f'Picture {L5[good]}: every square has its mirror image at the same distance on the other side.'),
                           c.shape())
    if level == 'medium':
        while True:
            half = set(motif(random.randint(4, 5), 3, 4, asymmetric=True))
            mirror = {(5 - x, y) for x, y in half}
            gone = random.choice(sorted(mirror))
            spare = random.choice([(x, y) for x in range(3, 6) for y in range(5) if (x, y) not in mirror])
            options = [mirror,
                       {(x + 3, y) for x, y in half},                    # copied, not mirrored
                       {(5 - x, 4 - y) for x, y in half},                # mirrored and upside down
                       (mirror - {gone}) | {spare},                      # one square misplaced
                       {(5 - x, y) for x, y in _mirror_h(half)}]
            if len({frozenset(o) for o in options}) == 5:
                break
        main = I.grid(6, 5, cell=20, cells=_place(half, 0, 0, blue), axis=('v', 3))
        order = list(range(5))
        random.shuffle(order)
        c, boxes = I.panels(5, 104, 96)
        for j, box in zip(order, boxes):
            cells = _place(half, 0, 0, blue)
            cells.update({p: red for p in options[j]})
            I.draw_grid(c, box, 6, 5, cells=cells, axis=('v', 3))
        i = order.index(0)
        return _letters_mc(('Quelle figure complète correctement le dessin par **réflexion** sur la ligne rouge ?',
                            'Which picture correctly completes the drawing by **reflection** in the red line?'),
                           boxes, i,
                           ('Chaque carré doit se retrouver à la même distance de la ligne, de l’autre côté (comme dans un miroir).',
                            'Each square must land the same distance from the line, on the other side (like in a mirror).'),
                           (f'Figure {L5[i]} : c’est l’image dans un miroir posé sur la ligne rouge.',
                            f'Picture {L5[i]}: it is the mirror image in the red line.'),
                           [main, c.shape()])
    import math
    shapes = {
        'square': ([(0, 0), (1, 0), (1, 1), (0, 1)], 4, ('un carré', 'a square')),
        'rect': ([(0, 0), (2, 0), (2, 1), (0, 1)], 2, ('un rectangle', 'a rectangle')),
        'equi': ([(0, 0), (2, 0), (1, -math.sqrt(3))], 3, ('un triangle équilatéral', 'an equilateral triangle')),
        'iso': ([(0, 0), (2, 0), (1, -2.4)], 1, ('un triangle isocèle', 'an isosceles triangle')),
        'scal': ([(0, 0), (3, 0), (0.9, -1.7)], 0, ('un triangle scalène', 'a scalene triangle')),
        'rhombus': ([(0, -1), (1.5, 0), (0, 1), (-1.5, 0)], 2, ('un losange', 'a rhombus')),
        'para': ([(0, 0), (2, 0), (2.8, -1.2), (0.8, -1.2)], 0, ('un parallélogramme', 'a parallelogram')),
        'pent': (I._ngon(5), 5, ('un pentagone régulier', 'a regular pentagon')),
        'hex': (I._ngon(6), 6, ('un hexagone régulier', 'a regular hexagon')),
    }
    key = pick(list(shapes))
    pts, axes, name = shapes[key]
    c = I.Canvas(170, 150, max_h=160, css_w='max-w-[12rem]')
    I.draw_polygon(c, pts, (10, 10, 150, 130), pick(I.PALETTE[:4]))
    return typed((f'Combien d’axes de symétrie a cette figure ({name[0]}) ?', f'How many lines of symmetry does this shape ({name[1]}) have?'),
                 [axes], 'integer',
                 ('Cherche toutes les lignes de pliage où les deux moitiés se superposent. Il peut y en avoir 0.',
                  'Look for every fold line where both halves match. There may be none.'),
                 (f'{name[0].capitalize()} a {axes} axe{"s" if axes > 1 else ""} de symétrie.',
                  f'{name[1].capitalize()} has {axes} line{"s" if axes != 1 else ""} of symmetry.'),
                 shape=c.shape())


def _dir_words(dx, dy):
    """dy > 0 = up. Returns (fr, en)."""
    parts_fr, parts_en = [], []
    if dx:
        parts_fr.append(f'{abs(dx)} carreau{"x" if abs(dx) > 1 else ""} vers la {"droite" if dx > 0 else "gauche"}')
        parts_en.append(f'{abs(dx)} square{"s" if abs(dx) > 1 else ""} {"right" if dx > 0 else "left"}')
    if dy:
        parts_fr.append(f'{abs(dy)} carreau{"x" if abs(dy) > 1 else ""} vers le {"haut" if dy > 0 else "bas"}')
        parts_en.append(f'{abs(dy)} square{"s" if abs(dy) > 1 else ""} {"up" if dy > 0 else "down"}')
    return ' et '.join(parts_fr), ' and '.join(parts_en)


def g6_translation_gen(level='easy'):
    """Translations on a grid: describe the arrow, tell translation from reflection, image of a point (169, 171)."""
    blue, green = I.SHADES[I.BLUE][2], I.SHADES[I.GREEN][2]
    if level == 'hard' and random.random() < 0.5:
        x, y = random.randint(0, 6), random.randint(0, 6)
        dx, dy = random.randint(-x if x else 1, 5), random.randint(-y if y else 1, 5)
        if dx == 0 and dy == 0:
            dx = 3
        w = _dir_words(dx, dy)
        nx, ny = x + dx, y + dy
        return typed((f'Le point A ({x}, {y}) glisse de {w[0]}. Quelles sont les coordonnées de son image ? (Écris x, y)',
                      f'Point A ({x}, {y}) slides {w[1]}. What are the coordinates of its image? (Write x, y)'),
                     [f'({nx}, {ny})', f'{nx}, {ny}', f'{nx},{ny}', f'({nx},{ny})'], 'text',
                     ('Vers la droite : x augmente ; vers le haut : y augmente.', 'Right: x goes up; up: y goes up.'),
                     ([f'x : {x} {"+" if dx >= 0 else "−"} {abs(dx)} = {nx}', f'y : {y} {"+" if dy >= 0 else "−"} {abs(dy)} = {ny}', f'Image : ({nx}, {ny})'],
                      [f'x: {x} {"+" if dx >= 0 else "−"} {abs(dx)} = {nx}', f'y: {y} {"+" if dy >= 0 else "−"} {abs(dy)} = {ny}', f'Image: ({nx}, {ny})']))
    m = motif(random.randint(4, 5), 3, 3)
    mw, mh = _size(m)
    cols, rows = 11, 7
    if level == 'easy':
        if random.random() < 0.5:
            dx, dy = random.choice([-1, 1]) * random.randint(3, 6), 0
        else:
            dx, dy = 0, random.choice([-1, 1]) * random.randint(3, 4)
    else:
        dx, dy = random.choice([-1, 1]) * random.randint(2, 5), random.choice([-1, 1]) * random.randint(1, 3)
    while abs(dx) <= mw and abs(dy) <= mh:        # leave a gap between the two copies
        if dx:
            dx += 1 if dx > 0 else -1
        else:
            dy += 1 if dy > 0 else -1
    # place the motif so both copies fit (screen rows go down; dy > 0 means up)
    x0 = random.randint(max(0, -dx), cols - mw - max(0, dx))
    y0 = random.randint(max(0, dy), rows - mh - max(0, -dy))
    if level == 'medium' and random.random() < 0.5:
        # translation or reflection?
        is_tr = random.random() < 0.5
        img = {(x + dx, y - dy) for x, y in m} if is_tr else {(mw - 1 - x + dx, y - dy) for x, y in m}
        cells = _place(m, x0, y0, blue)
        cells.update({(x + x0, y + y0): green for x, y in img})
        correct = ('une translation', 'a translation') if is_tr else ('une réflexion', 'a reflection')
        return mc(('La figure bleue a été transformée en la figure verte. Par quelle transformation ?',
                   'The blue shape was moved onto the green shape. Which transformation was used?'),
                  correct, [('une translation', 'a translation'), ('une réflexion', 'a reflection'),
                            ('un agrandissement', 'an enlargement'), ('une réduction', 'a reduction'),
                            ('aucune : les figures sont différentes', 'none: the shapes are different')],
                  ('Une translation fait glisser la figure sans la retourner. Une réflexion la retourne comme dans un miroir.',
                   'A translation slides the shape without flipping it. A reflection flips it like a mirror.'),
                  (('La figure verte est la même, orientée de la même façon : elle a glissé (translation).',
                    'The green shape is the same and faces the same way: it slid (translation).') if is_tr else
                   ('La figure verte est retournée, comme dans un miroir : c’est une réflexion.',
                    'The green shape is flipped, like in a mirror: it is a reflection.')),
                  shape=I.grid(cols, rows, cell=20, cells=cells))
    cells = _place(m, x0, y0, blue)
    cells.update(_place(m, x0 + dx, y0 - dy, green))
    w = _dir_words(dx, dy)
    wrongs = [_dir_words(-dx, -dy), _dir_words(dx + (1 if dx > 0 else -1) if dx else 1, dy),
              _dir_words(dx, dy + (1 if dy > 0 else -1) if dy else 1), _dir_words(dy, dx) if dx != dy else _dir_words(dx * 2, dy),
              _dir_words(-dx, dy) if dx and dy else _dir_words(dx - (1 if dx > 0 else -1) if dx else 2, dy)]
    return mc(('La figure bleue a glissé jusqu’à la figure verte. Décris la **translation**.',
               'The blue shape slid onto the green shape. Describe the **translation**.'),
              w, wrongs,
              ('Choisis un coin de la figure bleue et compte les carreaux jusqu’au même coin de la figure verte.',
               'Pick one corner of the blue shape and count the squares to the same corner of the green shape.'),
              (f'Chaque carré a glissé de {w[0]}.', f'Every square slid {w[1]}.'),
              shape=I.grid(cols, rows, cell=20, cells=cells))


def _tile_panel(c, box, cells, color, size=3):
    I.draw_grid(c, box, size, size, cells={p: color for p in cells})


def g3_frieze_gen(level='easy'):
    """Friezes made by translation or reflection: what comes next? (167, 168, 169)"""
    m = motif(random.randint(3, 4), 3, 3)
    w, h = 3, 3
    mv = frozenset((w - 1 - x, y) for x, y in m)
    mh = frozenset((x, h - 1 - y) for x, y in m)
    rot = frozenset((w - 1 - x, h - 1 - y) for x, y in m)
    colors = [I.SHADES[I.BLUE][2], I.SHADES[I.AMBER][2]]
    if level == 'easy':
        seq = [(m, colors[0])] * 5
        rule = ('par translation : le même motif glisse et se répète', 'by translation: the same motif slides and repeats')
    elif level == 'medium':
        seq = [(m if k % 2 == 0 else mv, colors[0]) for k in range(5)]
        rule = ('par réflexion : chaque motif est le reflet du précédent', 'by reflection: each motif is the mirror image of the one before')
    else:
        seq = [(m if k % 2 == 0 else mh, colors[k % 2]) for k in range(5)]
        rule = ('par réflexion (miroir horizontal) et en alternant les couleurs', 'by reflection (horizontal mirror), alternating colours')
    shown = random.choice([3, 4])                 # so the answer is not always the first tile
    c = I.Canvas((shown + 1) * 62 + 8, 70, max_h=90, css_w='max-w-md')
    for k in range(shown):
        _tile_panel(c, (4 + k * 62, 4, 58, 58), seq[k][0], seq[k][1])
    c.rect(4 + shown * 62 + 2, 6, 54, 54, fill='#FFFFFF', stroke=I.PURPLE, sw=2, rx=6)
    c.text(4 + shown * 62 + 29, 42, '?', size=26, bold=True, color=I.PURPLE)
    ans_cells, ans_col = seq[shown]
    pool = [(m, colors[0]), (mv, colors[0]), (mh, colors[0]), (rot, colors[0]), (m, colors[1]), (mh, colors[1]), (mv, colors[1])]
    opts = [(ans_cells, ans_col)]
    for o in pool:
        if all(not (o[0] == p[0] and o[1] == p[1]) for p in opts):
            opts.append(o)
        if len(opts) == 5:
            break
    order = list(range(5))
    random.shuffle(order)
    cp, boxes = I.panels(5, 80, 70)
    for j, box in zip(order, boxes):
        _tile_panel(cp, box, opts[j][0], opts[j][1])
    i = order.index(0)
    return _letters_mc(('Cette frise suit une régularité. Quelle tuile vient ensuite ?', 'This frieze follows a pattern. Which tile comes next?'),
                       boxes, i,
                       ('Compare chaque tuile avec la précédente : glisse-t-elle, ou est-elle retournée comme dans un miroir ?',
                        'Compare each tile with the one before: does it slide, or is it flipped like in a mirror?'),
                       (f'La frise est construite {rule[0]}. La tuile suivante est la {L5[i]}.',
                        f'The frieze is built {rule[1]}. The next tile is {L5[i]}.'),
                       [c.shape(), cp.shape()])


def g3_congruent_gen(level='easy'):
    """Congruent (isometric) figures: same shape and same size (166)."""
    blue = I.SHADES[I.BLUE][2]
    m = motif(5, 3, 3) if level != 'easy' else motif(4, 3, 3)
    if level == 'easy':
        same = m
    elif level == 'medium':
        same = _rot90(m)
    else:
        same = pick([_rot90(_rot90(m)), _mirror_v(m), _rot90(_mirror_h(m))])
    wrong = []
    big = _norm({(2 * x + a, 2 * y + b) for x, y in m for a in (0, 1) for b in (0, 1)})   # same shape, twice as big
    while len(wrong) < 3:
        cells = set(m)
        cells.discard(random.choice(list(cells)))
        free = [(x, y) for x in range(4) for y in range(4) if (x, y) not in cells and
                any((x + a, y + b) in cells for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        cells.add(random.choice(free))
        cand = _norm(cells)
        variants = {m, _rot90(m), _rot90(_rot90(m)), _rot90(_rot90(_rot90(m))), _mirror_v(m), _mirror_h(m),
                    _rot90(_mirror_v(m)), _rot90(_mirror_h(m))}
        if cand not in variants and cand not in wrong and _connected(cand):
            wrong.append(_rot90(cand) if level != 'easy' else cand)
    opts = [(same, 4), (big, 8)] + [(w, 4) for w in wrong]
    order = list(range(5))
    random.shuffle(order)
    # The model sits in the same picture as the options so every square has the same size.
    c, boxes = I.panels(6, 96, 96, cols=3, letters=[('Modèle', 'Model')] + L5)
    tiles = [(m, 4, blue)] + [(opts[j][0], opts[j][1], I.SHADES[I.GREEN][2]) for j in order]
    for k, ((cells, g, col), box) in enumerate(zip(tiles, boxes)):
        gw, gh = _size(cells)
        size = max(4, gw, gh) if g == 4 else max(gw, gh) + 1
        x0, y0, bw, bh = box
        cell = min(bw, bh) / 7
        span = size * cell
        I.draw_grid(c, (x0 + (bw - span) / 2, y0 + (bh - span) / 2, span, span), size, size,
                    cells=_place(cells, 0, 0, col), cell=cell)
    i = order.index(0)
    return _letters_mc(('Quelle figure est **isométrique** au modèle (même forme et même taille) ?',
                        'Which shape is **congruent** to the model (same shape and same size)?'),
                       boxes, i,
                       ('Compte les carrés et compare la forme. On peut tourner ou retourner la figure, mais pas l’agrandir.',
                        'Count the squares and compare the shape. You may turn or flip it, but not make it bigger.'),
                       (f'La figure {L5[i]} a la même forme et la même taille que le modèle' + (' (elle est tournée ou retournée).' if level != 'easy' else '.'),
                        f'Shape {L5[i]} has the same shape and size as the model' + (' (it is turned or flipped).' if level != 'easy' else '.')),
                       c.shape())


# ── grid map & first-quadrant points ─────────────────────────────────────────

MAP_ICONS = [('🌳', 'l’arbre', 'the tree'), ('🏠', 'la maison', 'the house'), ('⭐', 'l’étoile', 'the star'),
             ('🐶', 'le chien', 'the dog'), ('🚗', 'la voiture', 'the car'), ('🍎', 'la pomme', 'the apple'),
             ('⚽', 'le ballon', 'the ball'), ('🌸', 'la fleur', 'the flower'), ('🐱', 'le chat', 'the cat')]


def _de(name):
    if name.startswith('le '):
        return 'du ' + name[3:]
    return 'de ' + name


def g3_grid_map_gen(level='easy'):
    """Locate squares on a plan (B3) and follow directions (133)."""
    cols, rows = (5, 4) if level == 'easy' else (6, 5)
    letters = 'ABCDEF'[:cols]
    icons = random.sample(MAP_ICONS, 6)
    spots = random.sample([(x, y) for x in range(cols) for y in range(rows)], 6)
    placed = {s: ic[0] for s, ic in zip(spots, icons)}
    name = lambda p: f'{letters[p[0]]}{p[1] + 1}'
    pic = I.grid(cols, rows, cell=30, col_labels=list(letters), row_labels=[str(r + 1) for r in range(rows)], icons=placed)
    if level == 'easy':
        k = random.randrange(6)
        p = spots[k]
        alts = [f'{letters[p[1]]}{p[0] + 1}' if p[1] < cols and p[0] < rows else None,
                *(name(q) for q in spots if q != p)]
        alts += [name(((p[0] + 1) % cols, p[1])), name((p[0], (p[1] + 1) % rows))]
        return mc((f'Dans quelle case se trouve {icons[k][1]} {icons[k][0]} ?', f'Which square is {icons[k][2]} {icons[k][0]} in?'),
                  name(p), alts,
                  ('Lis d’abord la lettre de la colonne, puis le chiffre de la ligne.', 'Read the column letter first, then the row number.'),
                  (f'{icons[k][0]} est dans la colonne {letters[p[0]]} et la ligne {p[1] + 1} : case {name(p)}.',
                   f'{icons[k][0]} is in column {letters[p[0]]} and row {p[1] + 1}: square {name(p)}.'),
                  shape=pic)
    label = lambda ic: (f'{ic[0]} {ic[1]}', f'{ic[0]} {ic[2]}')
    if level == 'medium':
        k = random.randrange(6)
        return mc((f'Qu’y a-t-il dans la case {name(spots[k])} ?', f'What is in square {name(spots[k])}?'),
                  label(icons[k]), [label(ic) for j, ic in enumerate(icons) if j != k],
                  ('Trouve la colonne (lettre), puis descends jusqu’à la ligne (chiffre).', 'Find the column (letter), then go down to the row (number).'),
                  (f'Colonne {letters[spots[k][0]]}, ligne {spots[k][1] + 1} : {icons[k][1]}.',
                   f'Column {letters[spots[k][0]]}, row {spots[k][1] + 1}: {icons[k][2]}.'),
                  shape=pic)
    for _ in range(200):
        s, t = random.sample(range(6), 2)
        dx, dy = spots[t][0] - spots[s][0], spots[s][1] - spots[t][1]     # dy > 0 = up the page
        if dx and dy:
            break
    w = _dir_words(dx, dy)
    w = (w[0].replace('carreaux', 'cases').replace('carreau', 'case'), w[1])
    return mc((f'Pars {_de(icons[s][1])} {icons[s][0]}. Avance de {w[0]}. Où arrives-tu ?',
               f'Start at {icons[s][2]} {icons[s][0]}. Move {w[1]}. Where do you end up?'),
              label(icons[t]), [label(ic) for j, ic in enumerate(icons) if j not in (s, t)],
              ('Avance une case à la fois avec ton doigt.', 'Move one square at a time with your finger.'),
              (f'De {name(spots[s])}, on arrive en {name(spots[t])} : {icons[t][1]}.',
               f'From {name(spots[s])} you reach {name(spots[t])}: {icons[t][2]}.'),
              shape=pic)


def cartesian_place_point_gen(level='easy'):
    """Which point is at (x, y)? First quadrant (135)."""
    size = {'easy': 5, 'medium': 7, 'hard': 9}[level]
    while True:
        x, y = random.randint(1, size - 1), random.randint(1, size - 1)
        if level == 'easy' or x != y:
            break
    cands = [(y, x), (x + 1, y), (x, y - 1), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x - 1, y)]
    others = []
    for p in cands:
        if 0 <= p[0] <= size and 0 <= p[1] <= size and p != (x, y) and p not in others:
            others.append(p)
    others = others[:4]
    pts = [(x, y)] + others
    random.shuffle(pts)
    names = {p: L5[k] for k, p in enumerate(pts)}
    correct = names[(x, y)]
    return mc((f'Quel point a pour coordonnées ({x}, {y}) ?', f'Which point is at ({x}, {y})?'),
              correct, [l for l in L5 if l != correct],
              ('Le premier nombre se lit sur l’axe horizontal (x), le deuxième sur l’axe vertical (y).',
               'The first number is on the horizontal axis (x), the second on the vertical axis (y).'),
              (f'Avance de {x} vers la droite, puis monte de {y} : c’est le point {correct}.',
               f'Go {x} to the right, then {y} up: it is point {correct}.'),
              shape=I.grid(size, size, cell=24 if size < 9 else 20, axes_numbers=True, points=names))
