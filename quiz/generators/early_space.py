"""
early_space.py — curriculum upgrade WP1, grades 1–2: shapes, space, measurement,
time, fractions, data and chance (2026-10).
"""
import math
import random

from quiz import illustrations as I
from .kit import mc, typed, ordering, pick
from .measurement import _fmt_time

L5 = list('ABCDE')
SHAPE_NAMES = {'square': ('carré', 'square'), 'rectangle': ('rectangle', 'rectangle'), 'triangle': ('triangle', 'triangle'),
               'rhombus': ('losange', 'rhombus'), 'circle': ('cercle', 'circle')}
COLOR_NAMES = {I.BLUE: ('bleu', 'blue'), I.RED: ('rouge', 'red'), I.GREEN: ('vert', 'green'), I.AMBER: ('jaune', 'yellow')}


def _letters(prompt, i, hint, explanation, shape):
    return mc(prompt, L5[i], [x for x in L5 if x != L5[i]], hint, explanation, shape=shape)


# ── E1.17 Shape patterns ─────────────────────────────────────────────────────

def g1_shape_pattern_gen(level='easy'):
    """What comes next in a pattern of shapes and colours? (105, 167)"""
    kinds = random.sample(['circle', 'square', 'triangle', 'rhombus'], 3)
    cols = random.sample([I.BLUE, I.RED, I.GREEN, I.AMBER], 3)
    unit = {'easy': [0, 1], 'medium': pick([[0, 0, 1], [0, 1, 1], [0, 1, 2]]), 'hard': pick([[0, 1, 2, 1], [0, 0, 1, 2], [0, 1, 1, 2]])}[level]
    tiles = [(kinds[u], cols[u] if level != 'hard' else cols[(u + 1) % 3]) for u in unit]
    shown = len(unit) * 2 + random.randint(0, len(unit) - 1)
    seq = [tiles[k % len(tiles)] for k in range(shown + 1)]
    ans = seq[shown]
    c = I.Canvas(min(shown + 1, 9) * 44 + 8, 54, max_h=70, css_w='max-w-lg')
    for k, (kind, col) in enumerate(seq[-9:][:-1] if shown >= 9 else seq[:-1]):
        I.draw_plane_shape(c, kind, (4 + k * 44, 6, 40, 40), col)
    last = min(shown, 8)
    c.rect(4 + last * 44 + 2, 8, 36, 36, fill='#FFFFFF', stroke=I.PURPLE, sw=2, rx=6)
    c.text(4 + last * 44 + 20, 33, '?', size=20, bold=True, color=I.PURPLE)
    opts = [ans]
    pool = [(k, cl) for k in kinds for cl in cols]
    random.shuffle(pool)
    for o in pool:
        if o not in opts:
            opts.append(o)
        if len(opts) == 5:
            break
    order = list(range(5))
    random.shuffle(order)
    cp, boxes = I.panels(5, 70, 60)
    for j, box in zip(order, boxes):
        I.draw_plane_shape(cp, opts[j][0], box, opts[j][1])
    i = order.index(0)
    name = SHAPE_NAMES[ans[0]]
    colname = COLOR_NAMES[ans[1]]
    return _letters(('Qu’est-ce qui vient ensuite ?', 'What comes next?'), i,
                    ('Trouve le motif qui se répète, puis continue-le.', 'Find the part that repeats, then continue it.'),
                    (f'Le motif se répète : ensuite vient un {name[0]} {colname[0]} ({L5[i]}).', f'The pattern repeats: next comes a {colname[1]} {name[1]} ({L5[i]}).'),
                    [c.shape(), cp.shape()])


# ── E1.18 Name the shape ─────────────────────────────────────────────────────

def g1_name_shape_gen(level='easy'):
    """Square, rectangle, triangle, rhombus, circle (154, 155)."""
    kind = pick(list(SHAPE_NAMES))
    if level == 'hard':
        riddles = {'square': ('J’ai 4 côtés tous pareils et 4 coins droits.', 'I have 4 equal sides and 4 square corners.'),
                   'rectangle': ('J’ai 4 côtés et 4 coins droits, mais mes côtés ne sont pas tous pareils.', 'I have 4 sides and 4 square corners, but my sides are not all equal.'),
                   'triangle': ('J’ai 3 côtés et 3 coins.', 'I have 3 sides and 3 corners.'),
                   'rhombus': ('J’ai 4 côtés tous pareils, mais pas de coin droit.', 'I have 4 equal sides but no square corner.'),
                   'circle': ('Je suis tout rond : je n’ai ni côté ni coin.', 'I am perfectly round: no sides and no corners.')}
        return mc((f'Qui suis-je ? {riddles[kind][0]}', f'Who am I? {riddles[kind][1]}'),
                  SHAPE_NAMES[kind], [v for k, v in SHAPE_NAMES.items() if k != kind],
                  ('Compte les côtés, puis regarde les coins.', 'Count the sides, then look at the corners.'),
                  (f'C’est un {SHAPE_NAMES[kind][0]}.', f'It is a {SHAPE_NAMES[kind][1]}.'))
    if level == 'medium':
        kinds = list(SHAPE_NAMES)
        random.shuffle(kinds)
        c, boxes = I.panels(5, 90, 80)
        for k, box in zip(kinds, boxes):
            I.draw_plane_shape(c, k, box, pick([I.BLUE, I.RED, I.GREEN, I.AMBER]), rot=random.uniform(-0.5, 0.5))
        i = kinds.index(kind)
        return _letters((f'Où est le **{SHAPE_NAMES[kind][0]}** ?', f'Where is the **{SHAPE_NAMES[kind][1]}**?'), i,
                        ('Regarde le nombre de côtés et les coins.', 'Look at the number of sides and the corners.'),
                        (f'Le {SHAPE_NAMES[kind][0]} est la figure {L5[i]}.', f'The {SHAPE_NAMES[kind][1]} is shape {L5[i]}.'), c.shape())
    c = I.Canvas(150, 130, max_h=140, css_w='max-w-[10rem]')
    I.draw_plane_shape(c, kind, (10, 10, 130, 110), pick([I.BLUE, I.RED, I.GREEN, I.AMBER]), rot=random.uniform(-0.6, 0.6),
                       stretch=random.uniform(0.8, 1.2))
    return mc(('Comment s’appelle cette figure ?', 'What is this shape called?'), SHAPE_NAMES[kind], [v for k, v in SHAPE_NAMES.items() if k != kind],
              ('Compte les côtés.', 'Count the sides.'), (f'C’est un {SHAPE_NAMES[kind][0]}.', f'It is a {SHAPE_NAMES[kind][1]}.'), shape=c.shape())


# ── E1.19 Open / closed, curved / broken lines ───────────────────────────────

def g1_open_closed_lines_gen(level='easy'):
    """Closed or open lines, curved or broken (153, 156)."""
    combos = [(True, True), (True, False), (False, True), (False, False)]
    if level == 'easy':
        target = (True, None) if random.random() < 0.5 else (False, None)
        good = (target[0], pick([True, False]))
        bad = [(not target[0], cv) for cv in (True, False)] * 2
        specs = [good] + bad
        q = (('Quelle ligne est **fermée** ?', 'Which line is **closed**?') if target[0] else ('Quelle ligne est **ouverte** ?', 'Which line is **open**?'))
        expl = (('Une ligne fermée n’a pas de bout : on peut en faire le tour.', 'A closed line has no ends: you can go all the way around.') if target[0]
                else ('Une ligne ouverte a deux bouts.', 'An open line has two ends.'))
    else:
        good = pick(combos)
        specs = [good] + [c for c in combos if c != good] + [pick([c for c in combos if c != good])]
        words = ({True: 'fermée', False: 'ouverte'}, {True: 'courbe', False: 'brisée'})
        words_en = ({True: 'closed', False: 'open'}, {True: 'curved', False: 'broken (straight pieces)'})
        q = (f'Quelle ligne est **{words[1][good[1]]}** et **{words[0][good[0]]}** ?', f'Which line is **{words_en[1][good[1]]}** and **{words_en[0][good[0]]}**?')
        expl = ('Fermée : pas de bout. Courbe : arrondie. Brisée : faite de segments droits.', 'Closed: no ends. Curved: rounded. Broken: made of straight pieces.')
    order = list(range(5))
    random.shuffle(order)
    c, boxes = I.panels(5, 100, 80)
    for j, box in zip(order, boxes):
        I.draw_line_kind(c, box, *specs[j])
    i = order.index(0)
    return _letters(q, i, expl, (f'C’est la ligne {L5[i]}.', f'It is line {L5[i]}.'), c.shape())


# ── E1.20 Everyday objects and solids ────────────────────────────────────────

OBJECTS = [('⚽', 'un ballon', 'a ball', 'sphere'), ('🌍', 'un globe', 'a globe', 'sphere'), ('🥫', 'une boîte de conserve', 'a can', 'cylinder'),
           ('🕯️', 'une chandelle', 'a candle', 'cylinder'), ('🎲', 'un dé', 'a dice', 'cube'), ('🧊', 'un glaçon', 'an ice cube', 'cube'),
           ('🍦', 'un cornet de crème glacée', 'an ice-cream cone', 'cone'), ('🥳', 'un chapeau de fête', 'a party hat', 'cone'),
           ('📦', 'une boîte en carton', 'a cardboard box', 'rect-prism')]
SOLID_SIMPLE = {'sphere': ('boule', 'sphere'), 'cylinder': ('cylindre', 'cylinder'), 'cube': ('cube', 'cube'), 'cone': ('cône', 'cone'),
                'rect-prism': ('prisme', 'prism'), 'square-pyramid': ('pyramide', 'pyramid')}


def g1_solid_objects_gen(level='easy'):
    """Everyday objects ↔ solids; what rolls (139, 141, 142)."""
    if level == 'easy':
        icon, fr, en, kind = pick(OBJECTS)
        return mc((f'{icon} {fr.capitalize()} ressemble à quel solide ?', f'{icon} {en.capitalize()} looks like which solid?'),
                  SOLID_SIMPLE[kind], [v for k, v in SOLID_SIMPLE.items() if k != kind],
                  ('Pense à sa forme : rond partout, rond avec des bouts plats, des faces carrées…', 'Think of its shape: round all over, round with flat ends, square faces…'),
                  (f'{fr.capitalize()} ressemble à un{"e" if kind == "sphere" else ""} {SOLID_SIMPLE[kind][0]}.', f'{en.capitalize()} looks like a {SOLID_SIMPLE[kind][1]}.'))
    if level == 'medium':
        kind = pick(list(SOLID_SIMPLE))
        return mc(('Comment s’appelle ce solide ?', 'What is this solid called?'), SOLID_SIMPLE[kind], [v for k, v in SOLID_SIMPLE.items() if k != kind],
                  ('Regarde s’il est rond ou s’il a des faces plates.', 'Check whether it is round or has flat faces.'),
                  (f'C’est un{"e" if kind in ("sphere", "square-pyramid") else ""} {SOLID_SIMPLE[kind][0]}.', f'It is a {SOLID_SIMPLE[kind][1]}.'),
                  shape=I.solid(kind, pick([I.BLUE, I.GREEN, I.AMBER])))
    flat = pick(['cube', 'rect-prism', 'square-pyramid', 'tri-prism'])
    kinds = ['sphere', 'cylinder', 'cone', pick(['sphere', 'cylinder']), flat]
    random.shuffle(kinds)
    c, boxes = I.panels(5, 100, 96)
    for k, box in zip(kinds, boxes):
        I.draw_solid(c, k, box, pick([I.BLUE, I.GREEN, I.AMBER, I.PURPLE]))
    i = kinds.index(flat)
    return _letters(('Quel solide **ne peut pas rouler** ? (Il ne fait que glisser.)', 'Which solid **cannot roll**? (It can only slide.)'), i,
                    ('Un solide roule s’il a une surface courbe.', 'A solid rolls if it has a curved surface.'),
                    (f'Le solide {L5[i]} n’a que des faces plates : il glisse mais ne roule pas.', f'Solid {L5[i]} has only flat faces: it slides but does not roll.'),
                    c.shape())


# ── E1.21 Position words ─────────────────────────────────────────────────────

SCENE = [('🐱', 'le chat', 'the cat'), ('🐶', 'le chien', 'the dog'), ('🌳', 'l’arbre', 'the tree'), ('🏠', 'la maison', 'the house'),
         ('⚽', 'le ballon', 'the ball'), ('🌸', 'la fleur', 'the flower'), ('🚗', 'la voiture', 'the car'), ('⭐', 'l’étoile', 'the star'),
         ('🍎', 'la pomme', 'the apple')]


def _de(name):
    return 'du ' + name[3:] if name.startswith('le ') else 'de ' + name


def g1_position_words_gen(level='easy'):
    """Left/right, above/below, between (132)."""
    items = random.sample(SCENE, 9)
    cols, rows = (3, 1) if level == 'easy' else (3, 3)
    grid = {}
    k = 0
    for r in range(rows):
        for cc in range(cols):
            grid[(cc, r)] = items[k]
            k += 1
    pic = I.grid(cols, rows, cell=46, icons={p: it[0] for p, it in grid.items()})
    rels = [('à gauche', 'to the left of', (-1, 0)), ('à droite', 'to the right of', (1, 0))]
    if rows > 1:
        rels += [('au-dessus', 'above', (0, -1)), ('en dessous', 'below', (0, 1))]
    while True:
        (x, y), ref = random.choice(list(grid.items()))
        fr_rel, en_rel, (dx, dy) = pick(rels)
        target = grid.get((x + dx, y + dy))
        if target:
            break
    if level == 'hard' and cols == 3:
        mid_y = random.randrange(rows)
        a, b, t = grid[(0, mid_y)], grid[(2, mid_y)], grid[(1, mid_y)]
        return mc((f'Qu’est-ce qui est **entre** {a[1]} {a[0]} et {b[1]} {b[0]} ?', f'What is **between** {a[2]} {a[0]} and {b[2]} {b[0]}?'),
                  (f'{t[0]} {t[1]}', f'{t[0]} {t[2]}'), [(f'{it[0]} {it[1]}', f'{it[0]} {it[2]}') for it in items if it != t][:6],
                  ('Entre = au milieu des deux.', 'Between = in the middle of the two.'),
                  (f'{t[1].capitalize()} est entre les deux.', f'{t[2].capitalize()} is between them.'), shape=pic)
    return mc((f'Qu’est-ce qui est **{fr_rel}** {_de(ref[1])} {ref[0]} ?', f'What is **{en_rel}** {ref[2]} {ref[0]}?'),
              (f'{target[0]} {target[1]}', f'{target[0]} {target[2]}'),
              [(f'{it[0]} {it[1]}', f'{it[0]} {it[2]}') for it in items if it not in (target, ref)][:6],
              ('Ta main gauche est du côté gauche de l’image.', 'Your left hand is on the left side of the picture.'),
              (f'{target[1].capitalize()} est {fr_rel} {_de(ref[1])}.', f'{target[2].capitalize()} is {en_rel} {ref[2]}.'), shape=pic)


# ── E1.22 Same shape and size ────────────────────────────────────────────────

def g1_same_shape_size_gen(level='easy'):
    """Find the figure that is exactly the same (same shape, same size) (166)."""
    kind = pick(['triangle', 'rectangle', 'rhombus', 'pentagon'])
    rot0 = 0 if level == 'easy' else random.uniform(0, 0.3)
    c, boxes = I.panels(6, 92, 86, cols=3, letters=[('Modèle', 'Model')] + L5)
    model_scale = 0.7
    opts = [('same', 0.7, kind, 1.0, rot0 if level == 'easy' else rot0 + pick([math.pi / 2, math.pi, 0.6])),
            ('big', 1.0, kind, 1.0, rot0), ('small', 0.45, kind, 1.0, rot0),
            ('other', 0.7, pick([k for k in ['triangle', 'rectangle', 'rhombus', 'pentagon', 'hexagon'] if k != kind]), 1.0, rot0),
            ('thin', 0.7, kind, 0.55, rot0)]
    if kind == 'rhombus':
        opts[4] = ('square', 0.7, 'square', 1.0, rot0 + math.pi / 4)
    order = list(range(5))
    random.shuffle(order)
    col = pick([I.BLUE, I.GREEN, I.AMBER])

    def draw(box, k, scale, stretch_, rot):
        bx, by, bw, bh = box
        # squash first (any kind), then turn: a squashed shape is never the same shape
        base = [(x * stretch_, y) for x, y in I.plane_shape_pts(k)]
        cs, sn = math.cos(rot), math.sin(rot)
        pts = [(x * cs - y * sn, x * sn + y * cs) for x, y in base]
        # fixed pixels per unit so sizes compare across panels
        ppu = 20 * scale / 0.7
        cx, cy = bx + bw / 2, by + bh / 2
        c.poly([(cx + x * ppu, cy + y * ppu) for x, y in pts], fill=I.SHADES[col][1], stroke=I.INK, sw=2)

    draw(boxes[0], kind, model_scale, 1.0, rot0)
    for j, box in zip(order, boxes[1:]):
        _, scale, k, st, rot = opts[j]
        draw(box, k, scale, st, rot)
    i = order.index(0)
    return _letters(('Quelle figure est **pareille** au modèle : même forme et même taille ?', 'Which shape is **the same** as the model: same shape and same size?'), i,
                    ('Une figure tournée reste la même figure. Mais plus grande ou plus petite, ce n’est plus pareil.',
                     'A turned shape is still the same shape. But bigger or smaller is not the same.'),
                    (f'La figure {L5[i]} a la même forme et la même taille.', f'Shape {L5[i]} has the same shape and size.'), c.shape())


# ── E1.23 Compare lengths / E1.24 Non-standard units / E1.25 Ruler in cm ────

def g1_compare_lengths_gen(level='easy'):
    """Longer/shorter; order three objects (172)."""
    n = 5 if level != 'hard' else 3
    lens = random.sample(range(3, 13), n)
    want_long = random.random() < 0.5
    h = n * 34 + 10
    c = I.Canvas(300, h, max_h=h + 10, css_w='max-w-md')
    misalign = level == 'medium'
    for k, L in enumerate(lens):
        y = 8 + k * 34
        x = 40 + (random.randint(0, 40) if misalign else 0)
        c.text(18, y + 18, L5[k], size=14, bold=True, color=I.PURPLE)
        c.rect(x, y + 6, L * 18, 16, fill=I.SHADES[pick([I.BLUE, I.RED, I.GREEN, I.AMBER])][2], stroke=I.INK, sw=1.5, rx=8)
    if level == 'hard':
        order = sorted(range(n), key=lambda k: lens[k])
        return ordering(('Range les rubans du plus court au plus long.', 'Order the ribbons from shortest to longest.'),
                        [L5[k] for k in order],
                        ('Compare les bouts de droite : ils partent tous du même endroit.', 'Compare the right ends: they all start at the same place.'),
                        (' < '.join(L5[k] for k in order),) * 2, shape=c.shape())
    i = lens.index(max(lens) if want_long else min(lens))
    word = ('le plus long', 'the longest') if want_long else ('le plus court', 'the shortest')
    return _letters((f'Quel ruban est **{word[0]}** ?', f'Which ribbon is **{word[1]}**?'), i,
                    (('Attention : les rubans ne commencent pas tous au même endroit. Compare leur vraie longueur.',
                      'Careful: the ribbons do not all start at the same place. Compare their real length.') if misalign else
                     ('Ils commencent au même endroit : regarde où ils finissent.', 'They start at the same place: look where they end.')),
                    (f'Le ruban {L5[i]} est {word[0]}.', f'Ribbon {L5[i]} is {word[1]}.'), c.shape())


def g1_measure_units_gen(level='easy'):
    """How many paper clips long? (174)"""
    n = random.randint(2, 5) if level == 'easy' else random.randint(4, 8)
    if level == 'hard':
        k = random.randint(2, 5)
        return typed((f'Une gomme mesure 2 trombones. Un crayon mesure {k} gommes. Combien de trombones mesure le crayon ?',
                      f'An eraser is 2 paper clips long. A pencil is {k} erasers long. How many paper clips long is the pencil?'),
                     [2 * k], 'integer', ('Chaque gomme vaut 2 trombones.', 'Each eraser is worth 2 paper clips.'),
                     (f'{k} × 2 = {2 * k} trombones', f'{k} × 2 = {2 * k} paper clips'))
    return typed(('Combien de trombones mesure le ruban ?', 'How many paper clips long is the ribbon?'), [n], 'integer',
                 ('Compte les trombones placés sous le ruban, du début à la fin.', 'Count the clips under the ribbon, from start to end.'),
                 (f'Le ruban mesure {n} trombones.', f'The ribbon is {n} paper clips long.'), shape=I.clip_measure(n))


def g2_ruler_cm_gen(level='easy'):
    """Read a length in centimetres (175, 181)."""
    obj = pick(['pencil', 'ribbon'])
    name = {'pencil': ('le crayon', 'the pencil'), 'ribbon': ('le ruban', 'the ribbon')}[obj]
    L = random.randint(2, 9)
    start = 0 if level == 'easy' else random.randint(1, 4)
    if level == 'hard':
        L = random.randint(3, 10)
        start = random.randint(1, 5)
    pic = I.ruler(15 if level == 'hard' else 10, start * 10, L * 10, mm_ticks=False, obj=obj)
    return typed((f'Combien de centimètres mesure {name[0]} ?', f'How many centimetres long is {name[1]}?'), [L], 'integer',
                 (('Le bout gauche est sur le 0.', 'The left end is on 0.') if start == 0 else
                  ('Il ne commence pas au 0 : compte les centimètres entre les deux bouts.', 'It does not start at 0: count the centimetres between the two ends.')),
                 ((f'De 0 à {L} : {L} cm.', f'From 0 to {L}: {L} cm.') if start == 0 else
                  (f'De {start} à {start + L} : {start + L} − {start} = {L} cm.', f'From {start} to {start + L}: {start + L} − {start} = {L} cm.')),
                 shape=pic)


# ── E1.26 Clock: o'clock and half past ───────────────────────────────────────

def g1_clock_hour_half_gen(level='easy'):
    """O’clock and half past (204, 206)."""
    h = random.randint(1, 12)
    m = 0 if level == 'easy' else random.choice([0, 30])
    fr, en = _fmt_time(h, m)
    en = en.replace(' AM', '').replace(' PM', '')
    if level == 'hard':
        words_fr = f'{h} heure{"s" if h > 1 else ""}' + (' et demie' if m else '')
        words_en = f'half past {h}' if m else f'{h} o’clock'
        return _clock_panels(h, m, words_fr, words_en)
    wrong = set()
    for dh, dm in [(h % 12 + 1, m), ((h - 2) % 12 + 1, m), (h, 30 - m if m in (0, 30) else 0), ((h % 12) + 1, 30 - m), (12 if h != 12 else 6, m)]:
        if (dh, dm) != (h, m):
            f2, e2 = _fmt_time(dh, dm)
            wrong.add((f2, e2.replace(' AM', '').replace(' PM', '')))
    return mc(('Quelle heure est-il ?', 'What time is it?'), (fr, en), sorted(wrong),
              ('La petite aiguille montre l’heure. La grande aiguille sur le 12 : heure juste ; sur le 6 : et demie.',
               'The short hand shows the hour. Long hand on 12: o’clock; on 6: half past.'),
              ((f'Grande aiguille sur le {"6" if m else "12"} : il est {fr}.'), (f'Long hand on {"6" if m else "12"}: it is {en}.')),
              shape={'type': 'clock', 'hours': h, 'minutes': m})


def _clock_panels(h, m, words_fr, words_en):
    times = [(h, m), (h, 30 - m), (h % 12 + 1, m), ((h + 5) % 12 + 1, m), ((h + 2) % 12 + 1, 30 - m)]
    seen, specs = set(), []
    for t in times:
        if t not in seen:
            seen.add(t)
            specs.append(t)
    while len(specs) < 5:
        t = (random.randint(1, 12), random.choice([0, 30]))
        if t not in seen:
            seen.add(t)
            specs.append(t)
    order = list(range(5))
    random.shuffle(order)
    shapes = [{'type': 'clock', 'hours': specs[j][0], 'minutes': specs[j][1], 'title': L5[k]} for k, j in enumerate(order)]
    i = order.index(0)
    return mc((f'Quelle horloge indique **{words_fr}** ?', f'Which clock shows **{words_en}**?'), L5[i], [x for x in L5 if x != L5[i]],
              ('Petite aiguille = heure ; grande aiguille sur le 12 = heure juste, sur le 6 = et demie.',
               'Short hand = hour; long hand on 12 = o’clock, on 6 = half past.'),
              (f'L’horloge {L5[i]}.', f'Clock {L5[i]}.'), shape=shapes)


# ── E1.27 Calendar ───────────────────────────────────────────────────────────

DAYS_FR = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
DAYS_EN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTHS_FR = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def g1_calendar_gen(level='easy'):
    """Days, months, seasons, yesterday/tomorrow (207)."""
    kind = pick(['tomorrow', 'yesterday', 'days-week'] if level == 'easy' else
                ['tomorrow', 'yesterday', 'month-after', 'month-before'] if level == 'medium' else
                ['in-days', 'month-after', 'months-year', 'season'])
    if kind in ('tomorrow', 'yesterday', 'in-days'):
        d = random.randrange(7)
        k = 1 if kind == 'tomorrow' else -1 if kind == 'yesterday' else random.randint(2, 4)
        ans = (d + k) % 7
        q = {'tomorrow': (f'Aujourd’hui, c’est {DAYS_FR[d]}. Quel jour serons-nous **demain** ?', f'Today is {DAYS_EN[d]}. What day will it be **tomorrow**?'),
             'yesterday': (f'Aujourd’hui, c’est {DAYS_FR[d]}. Quel jour étions-nous **hier** ?', f'Today is {DAYS_EN[d]}. What day was it **yesterday**?'),
             'in-days': (f'Aujourd’hui, c’est {DAYS_FR[d]}. Quel jour serons-nous dans **{k} jours** ?', f'Today is {DAYS_EN[d]}. What day will it be in **{k} days**?')}[kind]
        return mc(q, (DAYS_FR[ans], DAYS_EN[ans]), [(DAYS_FR[x], DAYS_EN[x]) for x in range(7) if x != ans][:6],
                  ('Récite les jours de la semaine dans l’ordre : lundi, mardi, mercredi…', 'Say the days of the week in order: Monday, Tuesday, Wednesday…'),
                  (f'Réponse : {DAYS_FR[ans]}.', f'Answer: {DAYS_EN[ans]}.'))
    if kind == 'days-week':
        return typed(('Combien de jours y a-t-il dans une semaine ?', 'How many days are there in a week?'), [7], 'integer',
                     ('Lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche.', 'Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.'),
                     ('Une semaine a 7 jours.', 'A week has 7 days.'))
    if kind == 'months-year':
        return typed(('Combien de mois y a-t-il dans une année ?', 'How many months are there in a year?'), [12], 'integer',
                     ('De janvier à décembre.', 'From January to December.'), ('Une année a 12 mois.', 'A year has 12 months.'))
    if kind in ('month-after', 'month-before'):
        mth = random.randrange(12)
        k = 1 if kind == 'month-after' else -1
        ans = (mth + k) % 12
        return mc(((f'Quel mois vient **après** {MONTHS_FR[mth]} ?' if k > 0 else f'Quel mois vient **avant** {MONTHS_FR[mth]} ?'),
                   (f'Which month comes **after** {MONTHS_EN[mth]}?' if k > 0 else f'Which month comes **before** {MONTHS_EN[mth]}?')),
                  (MONTHS_FR[ans], MONTHS_EN[ans]), [(MONTHS_FR[x], MONTHS_EN[x]) for x in random.sample([x for x in range(12) if x != ans], 6)],
                  ('Récite les mois dans l’ordre, de janvier à décembre.', 'Say the months in order, January to December.'),
                  (f'Réponse : {MONTHS_FR[ans]}.', f'Answer: {MONTHS_EN[ans]}.'))
    seasons = [(('l’hiver', 'winter'), 'décembre, janvier, février', 'December, January, February', 'il neige souvent', 'it often snows'),
               (('le printemps', 'spring'), 'mars, avril, mai', 'March, April, May', 'la neige fond et les fleurs poussent', 'the snow melts and flowers grow'),
               (('l’été', 'summer'), 'juin, juillet, août', 'June, July, August', 'il fait chaud et l’école est finie', 'it is hot and school is out'),
               (('l’automne', 'autumn'), 'septembre, octobre, novembre', 'September, October, November', 'les feuilles tombent des arbres', 'leaves fall from the trees')]
    s = pick(seasons)
    return mc((f'Pendant quelle saison {s[3]} (au Canada) ?', f'In which season {s[4]} (in Canada)?'), s[0],
              [x[0] for x in seasons if x != s] + [('la nuit', 'night-time')],
              ('Il y a quatre saisons : hiver, printemps, été, automne.', 'There are four seasons: winter, spring, summer, autumn.'),
              (f'C’est {s[0][0]} ({s[1]}).', f'It is {s[0][1]} ({s[2]}).'))


# ── E1.28 Half, third, quarter ───────────────────────────────────────────────

FRAC_WORDS = {2: ('un demi', 'one half'), 3: ('un tiers', 'one third'), 4: ('un quart', 'one quarter')}


def g1_half_third_quarter_gen(level='easy'):
    """Everyday fractions: a half, a third, a quarter; equal parts (026, 039)."""
    if level == 'medium':
        d = pick([2, 3, 4])
        # unequal cuts are obviously unequal (a 6-year-old must see it at a glance)
        UNEQUAL = {2: [[0.25], [0.72]], 3: [[0.15, 0.45], [0.5, 0.82]], 4: [[0.1, 0.25, 0.6], [0.35, 0.55, 0.9]]}
        specs = [('equal', d, None)] + [('unequal', d, cuts) for cuts in UNEQUAL[d]] + [('equal', x, None) for x in (2, 3, 4) if x != d]
        order = list(range(5))
        random.shuffle(order)
        c, boxes = I.panels(5, 100, 70)
        for j, box in zip(order, boxes):
            kind, dd, fracs = specs[j]
            x0, y0, w, h = box
            if kind == 'equal':
                cuts = [w * k / dd for k in range(dd + 1)]
            else:
                cuts = [0] + [w * f for f in fracs] + [w]
            for k in range(dd):
                c.rect(x0 + cuts[k], y0 + 10, cuts[k + 1] - cuts[k], h - 20, fill=I.SHADES[I.GREEN][2] if k == 0 else '#FFFFFF', stroke=I.INK, sw=1.8)
        i = order.index(0)
        return _letters((f'Où la partie colorée est-elle **{FRAC_WORDS[d][0]}** ?', f'Where is the coloured part **{FRAC_WORDS[d][1]}**?'), i,
                        (f'Il faut {d} parts **égales**.', f'You need {d} **equal** parts.'),
                        (f'Figure {L5[i]} : {d} parts égales, une colorée.', f'Shape {L5[i]}: {d} equal parts, one coloured.'), c.shape())
    d = pick([2, 3, 4])
    if level == 'hard':
        n = random.choice([4, 6, 8, 12])
        while n % d:
            n = random.choice([4, 6, 8, 12])
        return typed((f'Combien font {FRAC_WORDS[d][0]} de {n} billes ?', f'What is {FRAC_WORDS[d][1]} of {n} marbles?'), [n // d], 'integer',
                     (f'Partage les {n} billes en {d} groupes égaux.', f'Share the {n} marbles into {d} equal groups.'),
                     (f'{n} ÷ {d} = {n // d}', f'{n} ÷ {d} = {n // d}'), shape=I.collection(n, n // d))
    shape = I.fraction_circle(1, d) if random.random() < 0.5 else I.fraction_bars([(1, d)])
    return mc(('Quelle partie de la figure est colorée ?', 'What part of the shape is coloured?'), FRAC_WORDS[d],
              [v for k, v in FRAC_WORDS.items() if k != d] + [('deux demis', 'two halves'), ('le tout', 'the whole')],
              ('Compte les parts égales.', 'Count the equal parts.'),
              (f'{d} parts égales, une colorée : {FRAC_WORDS[d][0]}.', f'{d} equal parts, one coloured: {FRAC_WORDS[d][1]}.'), shape=shape)


# ── E1.29 Pictograph (one picture = one) ─────────────────────────────────────

def g1_pictograph_gen(level='easy'):
    """Read a pictograph where each picture is one (212, 218)."""
    cats = random.sample([('Chats', 'Cats'), ('Chiens', 'Dogs'), ('Poissons', 'Fish'), ('Lapins', 'Rabbits')], 3)
    icon = pick(['🙂', '⭐', '🐾'])
    vals = random.sample(range(1, 9), 3)
    pic = I.pictograph(cats, vals, icon, 1)
    i, j = random.sample(range(3), 2)
    if level == 'easy':
        return typed((f'Chaque {icon} est un enfant. Combien d’enfants préfèrent les **{cats[i][0].lower()}** ?',
                      f'Each {icon} is one child. How many children like **{cats[i][1].lower()}** best?'),
                     [vals[i]], 'integer', ('Compte les images de la ligne.', 'Count the pictures in the row.'),
                     (f'{vals[i]} enfants.', f'{vals[i]} children.'), shape=pic)
    if level == 'medium':
        best = vals.index(max(vals))
        return mc((f'Chaque {icon} est un enfant. Quel animal est le **plus aimé** ?', f'Each {icon} is one child. Which pet is the **most popular**?'),
                  cats[best], [c for c in cats if c != cats[best]] + [('Oiseaux', 'Birds'), ('Tortues', 'Turtles')],
                  ('Cherche la ligne la plus longue.', 'Look for the longest row.'),
                  (f'{cats[best][0]} : {max(vals)} enfants.', f'{cats[best][1]}: {max(vals)} children.'), shape=pic)
    a, b = (i, j) if vals[i] > vals[j] else (j, i)
    return typed((f'Chaque {icon} est un enfant. Combien d’enfants de plus aiment les {cats[a][0].lower()} que les {cats[b][0].lower()} ?',
                  f'Each {icon} is one child. How many more children like {cats[a][1].lower()} than {cats[b][1].lower()}?'),
                 [vals[a] - vals[b]], 'integer', ('Compare les deux lignes.', 'Compare the two rows.'),
                 (f'{vals[a]} − {vals[b]} = {vals[a] - vals[b]}',) * 2, shape=pic)


# ── E1.30 Certain, possible, impossible ──────────────────────────────────────

RED, BLUE_, YEL = '#EF4444', '#3B82F6', '#FACC15'


def g1_certain_possible_impossible_gen(level='easy'):
    """Certain / possible / impossible with bags of marbles (225, 229)."""
    want = pick(['impossible', 'certain'] if level == 'easy' else ['impossible', 'certain', 'possible'])
    if want == 'impossible':
        good = [(BLUE_, random.randint(3, 6))] if level == 'easy' else [(BLUE_, random.randint(2, 4)), (YEL, random.randint(1, 3))]
        bads = [[(RED, 1), (BLUE_, 4)], [(RED, 3), (BLUE_, 2)], [(RED, 5)], [(RED, 2), (YEL, 2)], [(RED, 1), (YEL, 3), (BLUE_, 1)]]
        q = ('Dans quel sac est-il **impossible** de tirer une bille rouge ?', 'From which bag is it **impossible** to pick a red marble?')
        why = ('Impossible : il n’y a aucune bille rouge dans le sac.', 'Impossible: there is no red marble in the bag.')
    elif want == 'certain':
        good = [(RED, random.randint(3, 6))]
        bads = [[(RED, 4), (BLUE_, 1)], [(BLUE_, 4)], [(RED, 2), (YEL, 2)], [(RED, 3), (BLUE_, 3)], [(YEL, 3), (RED, 1)]]
        q = ('Dans quel sac est-il **certain** de tirer une bille rouge ?', 'From which bag are you **certain** to pick a red marble?')
        why = ('Certain : toutes les billes du sac sont rouges.', 'Certain: every marble in the bag is red.')
    else:
        good = [(RED, random.randint(1, 3)), (BLUE_, random.randint(1, 3))]
        bads = [[(RED, 5)], [(BLUE_, 4)], [(YEL, 3)], [(RED, 4)], [(BLUE_, 2), (YEL, 2)]]
        q = ('Dans quel sac est-il **possible, mais pas certain**, de tirer une bille rouge ?', 'From which bag is it **possible but not certain** to pick a red marble?')
        why = ('Possible mais pas certain : il y a des rouges ET d’autres couleurs.', 'Possible but not certain: there are red marbles AND other colours.')
    bags = [good] + random.sample(bads, 4)
    order = list(range(5))
    random.shuffle(order)
    c, boxes = I.panels(5, 100, 96)
    for j, box in zip(order, boxes):
        I.draw_bag(c, box, bags[j])
    i = order.index(0)
    return _letters(q, i, ('Regarde les couleurs dans chaque sac.', 'Look at the colours in each bag.'), (f'Sac {L5[i]}. {why[0]}', f'Bag {L5[i]}. {why[1]}'), c.shape())
