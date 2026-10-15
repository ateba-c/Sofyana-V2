"""
measurement_plus.py — curriculum upgrade WP6 (measurement), 2026-10.

Rulers in cm/mm, estimating lengths, area by counting squares and area units,
volume by counting cubes and volume units, comparing angles, the protractor,
balance scales and masses, capacities and measuring jugs, thermometers for
grades 3–4. Positive temperatures only (no negatives, decision D2 pending).
"""
import random

from quiz import illustrations as I
from .kit import mc, typed, ordering, pick, N

L5 = list('ABCDE')


def _letters(prompt, i, hint, explanation, shape):
    return mc(prompt, L5[i], [x for x in L5 if x != L5[i]], hint, explanation, shape=shape)


# ── G3 · Ruler in cm and mm ──────────────────────────────────────────────────

def g3_ruler_mm_gen(level='easy'):
    """Read a length on a ruler: whole cm, then mm, then not starting at 0 (175, 176)."""
    obj = pick(['pencil', 'ribbon'])
    name = {'pencil': ('le crayon', 'the pencil'), 'ribbon': ('le ruban', 'the ribbon')}[obj]
    if level == 'easy':
        L = random.randint(3, 9) * 10
        pic = I.ruler(10, 0, L, mm_ticks=False, obj=obj)
        return typed((f'Combien de centimètres mesure {name[0]} ?', f'How many centimetres long is {name[1]}?'),
                     [L // 10], 'integer',
                     ('Le bout gauche est sur le 0 : lis le nombre sous le bout droit.', 'The left end is on 0: read the number under the right end.'),
                     (f'{name[0].capitalize()} va de 0 à {L // 10} : {L // 10} cm.', f'{name[1].capitalize()} goes from 0 to {L // 10}: {L // 10} cm.'),
                     shape=pic)
    if level == 'medium':
        L = random.randint(21, 89)
        while L % 10 == 0:
            L = random.randint(21, 89)
        pic = I.ruler(10, 0, L, obj=obj)
        return typed((f'Combien de **millimètres** mesure {name[0]} ?', f'How many **millimetres** long is {name[1]}?'),
                     [L], 'integer',
                     ('1 cm = 10 mm. Compte les centimètres entiers, puis les petits traits.', '1 cm = 10 mm. Count the whole centimetres, then the small marks.'),
                     ([f'{L // 10} cm = {L // 10 * 10} mm', f'{L // 10 * 10} mm + {L % 10} mm = {L} mm'],
                      [f'{L // 10} cm = {L // 10 * 10} mm', f'{L // 10 * 10} mm + {L % 10} mm = {L} mm']),
                     shape=pic)
    start = random.randint(1, 4) * 10 + random.choice([0, 0, 5])
    L = random.randint(25, 105 - start)
    if random.random() < 0.5:
        L = L - L % 5 if L % 5 else L
    pic = I.ruler(12, start, L, obj=obj)
    a, b = start, start + L
    return typed((f'{name[0].capitalize()} ne commence pas au 0. Combien de millimètres mesure-t-il ?',
                  f'{name[1].capitalize()} does not start at 0. How many millimetres long is it?'),
                 [L], 'integer',
                 ('Lis où il commence et où il finit (en mm), puis fais la différence.', 'Read where it starts and ends (in mm), then subtract.'),
                 ([f'Début : {a} mm, fin : {b} mm', f'{b} − {a} = {L} mm'], [f'Start: {a} mm, end: {b} mm', f'{b} − {a} = {L} mm']),
                 shape=pic)


# ── G5 · Estimate lengths (km too) ───────────────────────────────────────────

LENGTHS = [  # (fr, en, value, unit)
    ('la longueur d’un crayon', 'the length of a pencil', 15, 'cm'),
    ('la hauteur d’une porte', 'the height of a door', 2, 'm'),
    ('la longueur d’une fourmi', 'the length of an ant', 5, 'mm'),
    ('la largeur d’un ongle', 'the width of a fingernail', 1, 'cm'),
    ('la longueur d’un autobus', 'the length of a bus', 12, 'm'),
    ('la distance entre deux villes voisines', 'the distance between two nearby towns', 30, 'km'),
    ('l’épaisseur d’une pièce de monnaie', 'the thickness of a coin', 2, 'mm'),
    ('la longueur d’une feuille de papier', 'the length of a sheet of paper', 28, 'cm'),
    ('la longueur d’un terrain de soccer', 'the length of a soccer field', 100, 'm'),
    ('la distance d’un marathon', 'the length of a marathon', 42, 'km'),
    ('la hauteur d’un enfant de 10 ans', 'the height of a 10-year-old child', 14, 'dm'),
    ('la longueur d’une gomme à effacer', 'the length of an eraser', 4, 'cm'),
    ('la hauteur d’une table', 'the height of a table', 7, 'dm'),
    ('la longueur d’une piscine olympique', 'the length of an Olympic pool', 50, 'm'),
    ('la longueur d’une trombone', 'the length of a paper clip', 3, 'cm'),
]
UNITS = ['mm', 'cm', 'dm', 'm', 'km']
MM = {'mm': 1, 'cm': 10, 'dm': 100, 'm': 1000, 'km': 1_000_000}


def g5_estimate_length_gen(level='easy'):
    """Choose a realistic length, units mm to km (177)."""
    fr, en, v, u = pick(LENGTHS)
    if level in ('easy', 'medium'):
        correct = f'{v} {u}'
        wrong = [f'{v} {x}' for x in UNITS if x != u]
        return mc((f'Quelle est la mesure la plus probable pour {fr} ?', f'What is the most likely measure for {en}?'),
                  correct, wrong,
                  ('Pense à des repères : 1 mm ≈ épaisseur d’un trait, 1 cm ≈ largeur d’un doigt, 1 m ≈ un grand pas, 1 km ≈ 15 minutes de marche.',
                   'Think of benchmarks: 1 mm ≈ a pencil line, 1 cm ≈ a finger’s width, 1 m ≈ a big step, 1 km ≈ a 15-minute walk.'),
                  (f'{fr.capitalize()} mesure environ {v} {u}.', f'{en.capitalize()} is about {v} {u}.'))
    # hard: order three lengths written with different units
    base = random.choice([2, 3, 4, 5, 6, 8])
    pool = [(base, 'km'), (base * 100, 'm'), (base * 10, 'm'), (base, 'm'), (base * 10, 'dm'), (base * 1000, 'cm')]
    pool = [p for p in pool if p[1] != 'm' or p[0] < 100000]
    chosen = []
    for p in random.sample(pool, len(pool)):
        if all(p[0] * MM[p[1]] != q[0] * MM[q[1]] for q in chosen):
            chosen.append(p)
        if len(chosen) == 4:
            break
    chosen.sort(key=lambda p: p[0] * MM[p[1]])
    labels = [f'{N(a)} {b}' for a, b in chosen]
    return ordering(('Range ces longueurs de la plus courte à la plus longue.', 'Order these lengths from shortest to longest.'),
                    labels,
                    ('Convertis tout dans la même unité (par exemple en mètres).', 'Convert everything to the same unit (for example metres).'),
                    ([f'{l} = {N(a * MM[b] // 1000)} m' for l, (a, b) in zip(labels, chosen)],
                     [f'{l} = {N(a * MM[b] // 1000)} m' for l, (a, b) in zip(labels, chosen)]))


# ── G3 · Area by counting squares ────────────────────────────────────────────

def _blob(n, w, h):
    cells = {(random.randrange(w), random.randrange(h))}
    while len(cells) < n:
        x, y = random.choice(sorted(cells))
        nb = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        p = (x + nb[0], y + nb[1])
        if 0 <= p[0] < w and 0 <= p[1] < h:
            cells.add(p)
    return cells


def g3_area_count_squares_gen(level='easy'):
    """Area of a figure on a grid, in squares (184, 186)."""
    color = I.SHADES[pick([I.BLUE, I.GREEN, I.AMBER, I.PURPLE])][2]
    cols, rows = 9, 7
    halves = []
    if level == 'easy':
        a, b = random.randint(2, 5), random.randint(2, 4)
        x0, y0 = random.randint(0, cols - a), random.randint(0, rows - b)
        cells = {(x0 + i, y0 + j) for i in range(a) for j in range(b)}
    else:
        cells = _blob(random.randint(8, 16) if level == 'medium' else random.randint(8, 14), cols, rows)
        if level == 'hard':
            # add an even number of half squares (triangles) on free cells next to the figure
            free = sorted({(x + dx, y + dy) for x, y in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                           if 0 <= x + dx < cols and 0 <= y + dy < rows} - cells)
            halves = random.sample(free, min(len(free), random.choice([2, 4])))
            if len(halves) % 2:
                halves = halves[:-1]
    c = I.Canvas(cols * 26 + 12, rows * 26 + 12, max_h=200, css_w='max-w-sm')
    cell, gx, gy = I.draw_grid(c, (6, 6, cols * 26, rows * 26), cols, rows, cells={p: color for p in cells}, cell=26)
    for x, y in halves:
        X, Y = gx + x * cell, gy + y * cell
        corner = random.randrange(4)
        tri = [[(X, Y), (X + cell, Y), (X, Y + cell)], [(X, Y), (X + cell, Y), (X + cell, Y + cell)],
               [(X + cell, Y), (X + cell, Y + cell), (X, Y + cell)], [(X, Y), (X + cell, Y + cell), (X, Y + cell)]][corner]
        c.poly(tri, fill=color, stroke=I.INK, sw=1)
    total = len(cells) + len(halves) // 2
    if halves:
        expl = ([f'{len(cells)} carrés entiers', f'{len(halves)} demi-carrés = {len(halves) // 2} carré{"s" if len(halves) > 2 else ""}', f'Aire = {total} carrés'],
                [f'{len(cells)} whole squares', f'{len(halves)} half squares = {len(halves) // 2} square{"s" if len(halves) > 2 else ""}', f'Area = {total} squares'])
    elif level == 'easy':
        a = max(x for x, _ in cells) - min(x for x, _ in cells) + 1
        b = len(cells) // a
        expl = ([f'{b} rangées de {a} carrés', f'{b} × {a} = {total} carrés'], [f'{b} rows of {a} squares', f'{b} × {a} = {total} squares'])
    else:
        expl = ([f'On compte les carrés colorés un par un : {total}.'], [f'Count the coloured squares one by one: {total}.'])
    return typed(('Quelle est l’**aire** de la figure colorée, en carrés ?' + (' (Deux demi-carrés font un carré.)' if halves else ''),
                  'What is the **area** of the coloured shape, in squares?' + (' (Two half squares make one square.)' if halves else '')),
                 [total], 'integer',
                 ('L’aire, c’est le nombre de carrés qui recouvrent la surface.', 'Area is the number of squares that cover the surface.'),
                 expl, shape=c.shape())


# ── G5 · Area units (cm², dm², m²) ───────────────────────────────────────────

AREAS = [  # (fr, en, unit)
    ('le plancher de la classe', 'the classroom floor', 'm²'),
    ('un timbre-poste', 'a postage stamp', 'cm²'),
    ('la couverture d’un livre', 'the cover of a book', 'dm²'),
    ('un terrain de basketball', 'a basketball court', 'm²'),
    ('l’ongle de ton pouce', 'your thumbnail', 'cm²'),
    ('une feuille de papier', 'a sheet of paper', 'dm²'),
    ('le mur d’une chambre', 'a bedroom wall', 'm²'),
    ('une carte à jouer', 'a playing card', 'cm²'),
]


def g5_area_units_gen(level='easy'):
    """Area with units: choose the unit, compute in cm²/m², convert m² ↔ dm² ↔ cm² (185, 187)."""
    if level == 'easy':
        fr, en, u = pick(AREAS)
        return mc((f'Quelle unité choisirais-tu pour mesurer l’aire de {fr} ?', f'Which unit would you use to measure the area of {en}?'),
                  u, [x for x in ['cm²', 'dm²', 'm²', 'cm', 'm'] if x != u],
                  ('Une aire se mesure en unités carrées. cm² : tout petit, dm² : la taille d’une main, m² : un grand carré au sol.',
                   'Area is measured in square units. cm²: tiny, dm²: about a hand, m²: a big square on the floor.'),
                  (f'Pour {fr}, on utilise le {u}.', f'For {en}, use {u}.'))
    if level == 'medium':
        u = pick(['cm', 'm', 'dm'])
        a, b = random.randint(3, 12), random.randint(2, 9)
        pic = I.Canvas(220, 140, max_h=150, css_w='max-w-xs')
        k = min(170 / a, 100 / b)
        x0, y0 = (220 - a * k) / 2, (140 - b * k) / 2 - 6
        pic.rect(x0, y0, a * k, b * k, fill=I.SHADES[I.TEAL][1], stroke=I.INK, sw=2)
        pic.text(x0 + a * k / 2, y0 + b * k + 16, f'{a} {u}', size=13, bold=True)
        pic.text(x0 + a * k + 6, y0 + b * k / 2 + 4, f'{b} {u}', size=13, bold=True, anchor='start')
        return typed((f'Quelle est l’aire de ce rectangle ? Écris l’unité ({u}²).', f'What is the area of this rectangle? Write the unit ({u}²).'),
                     [f'{a * b} {u}²', f'{a * b} {u}2', str(a * b)], 'integer',
                     ('Aire d’un rectangle = longueur × largeur, en unités carrées.', 'Area of a rectangle = length × width, in square units.'),
                     (f'{a} × {b} = {a * b} {u}²', f'{a} × {b} = {a * b} {u}²'), shape=pic.shape())
    kind = pick(['m2-dm2', 'dm2-cm2', 'dm2-m2', 'cm2-dm2'])
    n = random.randint(2, 9)
    if kind == 'm2-dm2':
        q, ans, why = (f'{n} m² = ? dm²', f'{n} m² = ? dm²'), n * 100, (f'1 m² = 100 dm² → {n} × 100 = {n * 100} dm²',) * 2
    elif kind == 'dm2-cm2':
        q, ans, why = (f'{n} dm² = ? cm²', f'{n} dm² = ? cm²'), n * 100, (f'1 dm² = 100 cm² → {n} × 100 = {n * 100} cm²',) * 2
    elif kind == 'dm2-m2':
        q, ans, why = (f'{n * 100} dm² = ? m²', f'{n * 100} dm² = ? m²'), n, (f'100 dm² = 1 m² → {n * 100} ÷ 100 = {n} m²',) * 2
    else:
        q, ans, why = (f'{n * 100} cm² = ? dm²', f'{n * 100} cm² = ? dm²'), n, (f'100 cm² = 1 dm² → {n * 100} ÷ 100 = {n} dm²',) * 2
    return typed((f'Complète : **{q[0]}**', f'Fill in: **{q[1]}**'), [ans], 'integer',
                 ('Un carré de 1 dm de côté contient 10 × 10 = 100 carrés de 1 cm de côté.',
                  'A square 1 dm wide holds 10 × 10 = 100 squares 1 cm wide.'),
                 why)


# ── G3 · Volume by counting cubes ────────────────────────────────────────────

def g3_volume_count_cubes_gen(level='easy'):
    """Volume of a stack of unit cubes (188, 190)."""
    color = pick([I.BLUE, I.GREEN, I.AMBER, I.PURPLE])
    if level == 'easy':
        heights = [[random.randint(1, 3) for _ in range(random.randint(2, 4))]]
        hidden = ('', '')
    elif level == 'medium':
        cols = random.randint(2, 3)
        back = [random.randint(1, 3) for _ in range(cols)]
        front = [random.randint(1, b) for b in back]          # front towers never higher: all tops visible
        heights = [back, front]
        hidden = (' Les tours cachées touchent le sol : aucune tour ne flotte.', ' Hidden towers stand on the floor: nothing floats.')
    else:
        a, b, h = random.randint(2, 4), random.randint(2, 3), random.randint(2, 3)
        heights = [[h] * a for _ in range(b)]
        hidden = (' C’est un prisme plein.', ' It is a solid box.')
    total = sum(map(sum, heights))
    if level == 'hard':
        expl = ([f'{a} × {b} = {a * b} cubes par étage', f'{h} étages : {a * b} × {h} = {total} cubes'],
                [f'{a} × {b} = {a * b} cubes per layer', f'{h} layers: {a * b} × {h} = {total} cubes'])
    else:
        towers = ' + '.join(str(x) for row in heights for x in row)
        expl = ([f'On additionne les tours : {towers} = {total} cubes'], [f'Add the towers: {towers} = {total} cubes'])
    return typed((f'Combien de petits cubes forment ce solide ? (Son volume, en cubes.){hidden[0]}',
                  f'How many small cubes make this solid? (Its volume, in cubes.){hidden[1]}'),
                 [total], 'integer',
                 ('Compte tour par tour, ou étage par étage.', 'Count tower by tower, or layer by layer.'),
                 expl, shape=I.cube_stack(heights, color))


# ── G6 · Volume units (cm³, dm³, L) ──────────────────────────────────────────

def g6_volume_units_gen(level='easy'):
    """cm³, dm³, m³; 1 dm³ = 1 L = 1000 cm³; volume of a box (189, 191)."""
    if level == 'easy':
        items = [('un dé à jouer', 'a dice', 'cm³'), ('une boîte à chaussures', 'a shoebox', 'dm³'),
                 ('une salle de classe', 'a classroom', 'm³'), ('un morceau de sucre', 'a sugar cube', 'cm³'),
                 ('un carton de lait de 1 L', 'a 1 L milk carton', 'dm³'), ('un camion de déménagement', 'a moving truck', 'm³')]
        fr, en, u = pick(items)
        return mc((f'Quelle unité convient le mieux pour mesurer le volume de {fr} ?',
                   f'Which unit best fits the volume of {en}?'),
                  u, [x for x in ['cm³', 'dm³', 'm³', 'cm²', 'm'] if x != u],
                  ('Un volume se mesure en unités cubes : cm³ (un petit dé), dm³ (un litre), m³ (un très grand cube).',
                   'Volume is measured in cubic units: cm³ (a small dice), dm³ (a litre), m³ (a very big cube).'),
                  (f'Pour {fr}, on utilise le {u}.', f'For {en}, use {u}.'))
    if level == 'medium':
        a, b, h = random.randint(2, 10), random.randint(2, 6), random.randint(2, 5)
        return typed((f'Une boîte mesure {a} cm de long, {b} cm de large et {h} cm de haut. Quel est son volume en cm³ ?',
                      f'A box is {a} cm long, {b} cm wide and {h} cm high. What is its volume in cm³?'),
                     [f'{a * b * h} cm³', f'{a * b * h} cm3', str(a * b * h)], 'integer',
                     ('Volume = longueur × largeur × hauteur.', 'Volume = length × width × height.'),
                     (f'{a} × {b} × {h} = {a * b * h} cm³', f'{a} × {b} × {h} = {a * b * h} cm³'))
    kind = pick(['dm3-l', 'l-cm3', 'cm3-ml', 'dm3-cm3', 'box-l'])
    n = random.randint(2, 9)
    if kind == 'dm3-l':
        return typed((f'Complète : **{n} dm³ = ? L**', f'Fill in: **{n} dm³ = ? L**'), [n], 'integer',
                     ('1 dm³ contient exactement 1 litre.', '1 dm³ holds exactly 1 litre.'), (f'{n} dm³ = {n} L',) * 2)
    if kind == 'l-cm3':
        return typed((f'Complète : **{n} L = ? cm³**', f'Fill in: **{n} L = ? cm³**'), [n * 1000], 'integer',
                     ('1 L = 1 dm³ = 1000 cm³.', '1 L = 1 dm³ = 1000 cm³.'), (f'{n} × 1000 = {N(n * 1000)} cm³',) * 2)
    if kind == 'cm3-ml':
        v = random.randint(2, 9) * 50
        return typed((f'Complète : **{v} cm³ = ? mL**', f'Fill in: **{v} cm³ = ? mL**'), [v], 'integer',
                     ('1 cm³ contient 1 mL.', '1 cm³ holds 1 mL.'), (f'{v} cm³ = {v} mL',) * 2)
    if kind == 'dm3-cm3':
        return typed((f'Complète : **{n} dm³ = ? cm³**', f'Fill in: **{n} dm³ = ? cm³**'), [n * 1000], 'integer',
                     ('Un cube de 1 dm de côté contient 10 × 10 × 10 = 1000 cubes de 1 cm.', 'A cube 1 dm wide holds 10 × 10 × 10 = 1000 one-centimetre cubes.'),
                     (f'{n} × 1000 = {N(n * 1000)} cm³',) * 2)
    a, b = pick([(10, 10), (20, 10), (20, 20), (10, 30), (20, 30)])
    h = pick([10, 20, 30])
    litres = a * b * h // 1000
    return typed((f'Un aquarium mesure {a} cm × {b} cm × {h} cm. Combien de litres d’eau peut-il contenir ?',
                  f'A fish tank measures {a} cm × {b} cm × {h} cm. How many litres of water can it hold?'),
                 [litres], 'integer',
                 ('Calcule le volume en cm³, puis 1000 cm³ = 1 L.', 'Work out the volume in cm³, then 1000 cm³ = 1 L.'),
                 ([f'{a} × {b} × {h} = {N(a * b * h)} cm³', f'{N(a * b * h)} ÷ 1000 = {litres} L'],
                  [f'{a} × {b} × {h} = {N(a * b * h)} cm³', f'{N(a * b * h)} ÷ 1000 = {litres} L']))


# ── G4 · Compare angles ──────────────────────────────────────────────────────

def g4_compare_angles_gen(level='easy'):
    """Compare angles: the opening counts, not the length of the rays (192, 193)."""
    if level == 'easy':
        degs = random.sample([20, 45, 70, 100, 135, 160], 5)
        rays = [0.9] * 5
    elif level == 'medium':
        degs = random.sample(range(25, 166, 20), 5)
        rays = [random.choice([0.45, 0.6, 0.95]) for _ in degs]
    else:
        base = random.randint(50, 110)
        degs = random.sample([base - 20, base - 10, base, base + 10, base + 20], 5)
        rays = [random.choice([0.4, 0.55, 0.95]) for _ in degs]
    want_big = random.random() < 0.5
    target = max(degs) if want_big else min(degs)
    if level != 'easy':
        # the trap: the largest angle gets the shortest rays (or the smallest the longest)
        i = degs.index(target)
        rays[i] = 0.42 if want_big else 0.98
    c, boxes = I.panels(5, 100, 90)
    for d, r, box in zip(degs, rays, boxes):
        I.draw_angle(c, box, d, ray=r, rot=random.choice([0, 10, 20, 30]) if level == 'hard' else 0)
    i = degs.index(target)
    word = ('le plus grand', 'the largest') if want_big else ('le plus petit', 'the smallest')
    return _letters((f'Quel angle est **{word[0]}** ?', f'Which angle is **{word[1]}**?'), i,
                    ('Compare l’ouverture entre les deux côtés. La longueur des côtés ne compte pas !',
                     'Compare how wide the two arms open. The length of the arms does not matter!'),
                    (f'L’angle {L5[i]} est {"le plus ouvert" if want_big else "le moins ouvert"}.',
                     f'Angle {L5[i]} opens {"the most" if want_big else "the least"}.'),
                    c.shape())


# ── G6 · Protractor ──────────────────────────────────────────────────────────

def g6_protractor_gen(level='easy'):
    """Read an angle on a protractor; estimate an angle in degrees (194, 195)."""
    if level == 'easy':
        d = random.choice(range(20, 171, 10))
        return typed(('Combien de degrés mesure l’angle rouge ?', 'How many degrees is the red angle?'),
                     [f'{d}°', str(d)], 'integer',
                     ('Un côté est sur le 0. Lis le nombre où passe l’autre côté.', 'One arm is on 0. Read the number where the other arm crosses.'),
                     (f'L’angle mesure {d}°.', f'The angle measures {d}°.'), shape=I.protractor(d))
    if level == 'medium':
        d = random.choice([x for x in range(15, 176, 5) if x % 10])
        left = random.random() < 0.5
        return typed(('Combien de degrés mesure l’angle rouge ?' + (' (Attention : il part de la gauche.)' if left else ''),
                      'How many degrees is the red angle?' + (' (Careful: it starts on the left.)' if left else '')),
                     [f'{d}°', str(d)], 'integer',
                     ('Pars du côté posé sur le 0 et compte de 10 en 10, puis de 5.' + (' Utilise l’échelle intérieure.' if left else ''),
                      'Start from the arm on 0 and count by tens, then by fives.' + (' Use the inner scale.' if left else '')),
                     ((f'Lu sur l’échelle intérieure : {d}°.' if left else f'L’angle mesure {d}°.'),
                      (f'Read on the inner scale: {d}°.' if left else f'The angle measures {d}°.')),
                     shape=I.protractor(d, base_left=left, show_inner=left))
    d = random.choice([30, 45, 60, 90, 120, 135, 150])
    c = I.Canvas(200, 140, max_h=150, css_w='max-w-[13rem]')
    I.draw_angle(c, (10, 10, 180, 120), d, ray=0.9, rot=random.choice([0, 15, 30]))
    opts = [f'environ {x}°' for x in (30, 45, 60, 90, 120, 135, 150, 170)]
    opts_en = [f'about {x}°' for x in (30, 45, 60, 90, 120, 135, 150, 170)]
    pairs = list(zip(opts, opts_en))
    correct = (f'environ {d}°', f'about {d}°')
    near = sorted(pairs, key=lambda p: abs(int(p[0].split()[1][:-1]) - d))
    return mc(('Sans rapporteur, estime cet angle.', 'Without a protractor, estimate this angle.'),
              correct, [p for p in near if p != correct][:6],
              ('Compare avec un angle droit (90°) : plus petit ou plus grand ? La moitié d’un angle droit fait 45°.',
               'Compare with a right angle (90°): smaller or bigger? Half a right angle is 45°.'),
              (f'L’angle mesure environ {d}°' + (' : c’est un angle droit.' if d == 90 else '.'),
               f'The angle is about {d}°' + (': a right angle.' if d == 90 else '.')),
              shape=c.shape())


# ── G3 · Balance scale and masses ────────────────────────────────────────────

FRUITS = [('🍎', 'pomme', 'apple', 150), ('🍐', 'poire', 'pear', 200), ('🍊', 'orange', 'orange', 250),
          ('🥕', 'carotte', 'carrot', 50), ('🍋', 'citron', 'lemon', 100), ('🥔', 'pomme de terre', 'potato', 200)]
# fr: (le/la/l’ …, un/une …, plural, masculine?) — en plural
FRUIT_FR = {'pomme': ('la pomme', 'une pomme', 'pommes', False), 'poire': ('la poire', 'une poire', 'poires', False),
            'orange': ('l’orange', 'une orange', 'oranges', False), 'carotte': ('la carotte', 'une carotte', 'carottes', False),
            'citron': ('le citron', 'un citron', 'citrons', True),
            'pomme de terre': ('la pomme de terre', 'une pomme de terre', 'pommes de terre', False)}
FRUIT_EN_PL = {'apple': 'apples', 'pear': 'pears', 'orange': 'oranges', 'carrot': 'carrots', 'lemon': 'lemons', 'potato': 'potatoes'}
MASSES = [('un trombone', 'a paper clip', 1, 'g'), ('une pomme', 'an apple', 150, 'g'), ('un enfant de 9 ans', 'a 9-year-old child', 30, 'kg'),
          ('un dictionnaire', 'a dictionary', 1, 'kg'), ('un sac de farine', 'a bag of flour', 2, 'kg'),
          ('une gomme à effacer', 'an eraser', 20, 'g'), ('un vélo', 'a bicycle', 12, 'kg'), ('une tranche de pain', 'a slice of bread', 30, 'g')]


def _weights(total):
    out = []
    for w in (500, 200, 100, 50, 20, 10):
        while total >= w and len(out) < 5:
            out.append(w)
            total -= w
    return out


def g3_balance_scale_gen(level='easy'):
    """Balance scales and estimating masses (200, 201, 202)."""
    if level == 'easy':
        icon, fr, en, m = pick(FRUITS)
        ws = _weights(m)
        de = 'du ' + fr if FRUIT_FR[fr][3] else 'de ' + FRUIT_FR[fr][0]
        return typed((f'La balance est en équilibre. Quelle est la masse {de} {icon} ?',
                      f'The scale is balanced. What is the mass of the {en} {icon}?'),
                     [f'{m} g', str(m)], 'integer',
                     ('En équilibre : les deux plateaux ont la même masse. Additionne les masses marquées.',
                      'Balanced: both pans have the same mass. Add up the weights.'),
                     (f'{" + ".join(map(str, ws))} = {m} g', f'{" + ".join(map(str, ws))} = {m} g'),
                     shape=I.balance([icon], [f'{w} g' for w in ws]))
    if level == 'medium':
        if random.random() < 0.5:
            fr, en, v, u = pick(MASSES)
            wrong_u = 'kg' if u == 'g' else 'g'
            correct = f'{v} {u}'
            alts = [f'{v} {wrong_u}', f'{v * 10} {u}', f'{v * 100} {u}', f'{v * 1000} {u}' if u == 'g' else f'{v * 100} g']
            return mc((f'Quelle est la masse la plus probable de {fr} ?', f'What is the most likely mass of {en}?'),
                      correct, alts,
                      ('Repères : un trombone ≈ 1 g, une pomme ≈ 150 g, un litre d’eau ≈ 1 kg.',
                       'Benchmarks: a paper clip ≈ 1 g, an apple ≈ 150 g, a litre of water ≈ 1 kg.'),
                      (f'{fr.capitalize()} a une masse d’environ {v} {u}.', f'{en.capitalize()} has a mass of about {v} {u}.'))
        (i1, f1, e1, m1), (i2, f2, e2, m2) = random.sample([f for f in FRUITS if f[3] != 200] + [FRUITS[1]], 2)
        while m1 == m2:
            (i1, f1, e1, m1), (i2, f2, e2, m2) = random.sample(FRUITS, 2)
        tilt = -1 if m1 > m2 else 1
        heavy = (f1, e1) if m1 > m2 else (f2, e2)
        light = (f2, e2) if m1 > m2 else (f1, e1)
        def lourd(f, word):
            art, _, _, masc = FRUIT_FR[f]
            return f'{art[0].upper()}{art[1:]} est plus {word if masc else word + "e" if word == "lourd" else "légère"}.'
        opts = [(lourd(heavy[0], 'lourd'), f'The {heavy[1]} is heavier.'),
                (lourd(light[0], 'lourd'), f'The {light[1]} is heavier.'),
                ('Les deux ont la même masse.', 'They have the same mass.'),
                (lourd(heavy[0], 'léger'), f'The {heavy[1]} is lighter.'),
                ('On ne peut pas savoir.', 'We cannot tell.')]
        return mc(('Que nous apprend la balance ?', 'What does the scale tell us?'),
                  opts[0], opts[1:],
                  ('Le plateau le plus lourd descend.', 'The heavier pan goes down.'),
                  (f'Le plateau {"du " + heavy[0] if FRUIT_FR[heavy[0]][3] else "de " + FRUIT_FR[heavy[0]][0]} descend : {lourd(heavy[0], "lourd")[0].lower()}{lourd(heavy[0], "lourd")[1:]}',
                   f'The {heavy[1]}’s pan goes down: it is heavier.'),
                  shape=I.balance([i1], [i2], tilt))
    icon, fr, en, m = pick(FRUITS)
    k = random.choice([2, 3, 4])
    total = m * k
    ws = _weights(total)
    if sum(ws) != total:
        ws = [total]
    if random.random() < 0.5 or total < 1000:
        _, _, pl, masc = FRUIT_FR[fr]
        return typed((f'La balance est en équilibre. Les {pl} ont {"tous" if masc else "toutes"} la même masse. Quelle est la masse {"d’un" if masc else "d’une"} {fr} ?',
                      f'The scale is balanced. All the {FRUIT_EN_PL[en]} have the same mass. What is the mass of one {en}?'),
                     [f'{m} g', str(m)], 'integer',
                     ('Trouve d’abord la masse totale, puis partage-la entre les fruits.', 'First find the total mass, then share it among the fruit.'),
                     ([f'Total : {" + ".join(map(str, ws))} = {total} g', f'{total} ÷ {k} = {m} g'],
                      [f'Total: {" + ".join(map(str, ws))} = {total} g', f'{total} ÷ {k} = {m} g']),
                     shape=I.balance([icon] * k, [f'{w} g' for w in ws]))
    return typed((f'Combien de grammes font {k} kg et {m} g ?', f'How many grams are {k} kg and {m} g?'),
                 [k * 1000 + m], 'integer',
                 ('1 kg = 1000 g.', '1 kg = 1000 g.'),
                 (f'{k} × 1000 + {m} = {N(k * 1000 + m)} g',) * 2)


# ── G3 · Capacity ────────────────────────────────────────────────────────────

CAPACITIES = [('une cuillère à thé', 'a teaspoon', 5, 'mL'), ('un verre', 'a glass', 250, 'mL'),
              ('une bouteille d’eau', 'a water bottle', 1, 'L'), ('une baignoire', 'a bathtub', 150, 'L'),
              ('un seau', 'a bucket', 10, 'L'), ('une canette de jus', 'a juice can', 355, 'mL'),
              ('un arrosoir', 'a watering can', 5, 'L'), ('un compte-gouttes', 'an eye dropper', 1, 'mL')]


def g3_capacity_estimate_gen(level='easy'):
    """How many cups fill the jug; read a measuring jug; estimate capacities (196, 197, 199)."""
    if level == 'easy':
        cup = pick([100, 200, 250, 500])
        n = random.randint(2, 6) if cup < 500 else random.randint(2, 4)
        jug_ml = cup * n
        jug_txt = f'{jug_ml // 1000} L' if jug_ml % 1000 == 0 else f'{jug_ml} mL'
        return typed((f'Un verre contient {cup} mL. Combien de verres faut-il pour remplir une carafe de {jug_txt} ?',
                      f'A glass holds {cup} mL. How many glasses does it take to fill a {jug_txt} jug?'),
                     [n], 'integer',
                     ('Compte de ' + str(cup) + ' en ' + str(cup) + ' jusqu’à la capacité de la carafe. (1 L = 1000 mL)',
                      f'Count by {cup}s up to the jug’s capacity. (1 L = 1000 mL)'),
                     (f'{N(jug_ml)} mL ÷ {cup} mL = {n} verres', f'{N(jug_ml)} mL ÷ {cup} mL = {n} glasses'))
    if level == 'medium':
        cap, step = pick([(500, 50), (1000, 100), (1000, 50), (2000, 250)])
        label = 100 if step == 50 and cap == 500 else 200 if step == 100 else 100 if step == 50 else 500
        level_ml = random.randrange(step, cap, step)
        return typed(('Quelle quantité de liquide y a-t-il dans la tasse à mesurer, en mL ?', 'How much liquid is in the measuring jug, in mL?'),
                     [f'{level_ml} mL', str(level_ml)], 'integer',
                     (f'Chaque petit trait vaut {step} mL.', f'Each small mark is {step} mL.'),
                     (f'Le liquide arrive au trait de {level_ml} mL.', f'The liquid reaches the {level_ml} mL mark.'),
                     shape=I.jug(cap, level_ml, step, label))
    fr, en, v, u = pick(CAPACITIES)
    other = 'mL' if u == 'L' else 'L'
    return mc((f'Quelle est la capacité la plus probable de {fr} ?', f'What is the most likely capacity of {en}?'),
              f'{v} {u}', [f'{v} {other}', f'{N(v * 10)} {u}', f'{N(v * 100)} {u}', f'{N(v * 1000)} {u}' if u == 'L' else f'{N(v * 10)} L'],
              ('Repères : une cuillère ≈ 5 mL, un verre ≈ 250 mL, une grande bouteille ≈ 1 L.',
               'Benchmarks: a spoon ≈ 5 mL, a glass ≈ 250 mL, a big bottle ≈ 1 L.'),
              (f'{fr.capitalize()} contient environ {v} {u}.', f'{en.capitalize()} holds about {v} {u}.'))


# ── G3 · Thermometer (positive temperatures) ─────────────────────────────────

def g3_thermometer_gen(level='easy'):
    """Read a thermometer and reason about temperatures, 0 °C and above (208, 209)."""
    if level == 'easy':
        t = random.choice(range(0, 41, 5))
        shape = {'type': 'thermometer', 'temp': t, 'min_temp': 0, 'max_temp': 40, 'step': 5}
    elif level == 'medium':
        t = random.choice(range(0, 41, 2))
        shape = {'type': 'thermometer', 'temp': t, 'min_temp': 0, 'max_temp': 40, 'step': 10, 'minor': 2}
    else:
        a = random.randint(3, 25)
        d = random.randint(2, 12)
        if random.random() < 0.5 or a <= d:
            return typed((f'Le matin, il fait {a} °C. L’après-midi, la température monte de {d} degrés. Quelle température fait-il l’après-midi ?',
                          f'In the morning it is {a} °C. In the afternoon the temperature rises by {d} degrees. What is the afternoon temperature?'),
                         [f'{a + d} °C', str(a + d)], 'integer',
                         ('« Monte » : on ajoute.', '“Rises”: add.'),
                         (f'{a} + {d} = {a + d} °C', f'{a} + {d} = {a + d} °C'))
        return typed((f'À midi, il fait {a} °C. Le soir, la température baisse de {d} degrés. Quelle température fait-il le soir ?',
                      f'At noon it is {a} °C. In the evening the temperature drops by {d} degrees. What is the evening temperature?'),
                     [f'{a - d} °C', str(a - d)], 'integer',
                     ('« Baisse » : on soustrait.', '“Drops”: subtract.'),
                     (f'{a} − {d} = {a - d} °C', f'{a} − {d} = {a - d} °C'))
    return typed(('Quelle température indique ce thermomètre ?', 'What temperature does this thermometer show?'),
                 [f'{t} °C', str(t)], 'integer',
                 ('Trouve combien vaut chaque petit trait, puis lis le haut du liquide.', 'Work out what each small mark is worth, then read the top of the liquid.'),
                 (f'Le liquide arrive à {t} °C.', f'The liquid reaches {t} °C.'),
                 shape=shape)
