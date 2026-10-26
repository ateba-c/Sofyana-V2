"""
integers_plus.py — grade 6 integers (WP9, decision D2 settled 2026-10-26: negative numbers are allowed where they
occur naturally — temperatures, altitude below sea level, basement floors, the number line and the 4-quadrant plane).

No arithmetic drills on signed numbers: the only "operations" are rises / drops of temperature or moves on a line,
which the audit lists under reading and locating integers (QC-056→061, QC-136).

    g6-integer-thermometer   read thermometers below zero; rises and drops that cross 0
    g6-integer-number-line   locate integers on a number line
    g6-integer-compare       compare integers (<, >) in context
    g6-integer-order         order integers
    g6-integer-read          read, write and name integers; translate a situation into an integer
    g6-cartesian-4q          points in the four quadrants of the Cartesian plane
"""
import random

from ..illustrations import Canvas, BLUE, RED, PURPLE, INK, SOFT
from .kit import mc, typed, ordering

MINUS = '−'


def s(n):
    """Integer with a real minus sign: s(-4) → '−4'."""
    return f'{MINUS}{abs(n)}' if n < 0 else str(n)


def ans(n, unit=''):
    """Accepted answers for a signed integer: '−4', '-4' (and with the unit)."""
    out = [s(n), str(n)]
    if unit:
        out += [f'{s(n)} {unit}', f'{n} {unit}']
    return list(dict.fromkeys(out))


def word_fr(n):
    return f'moins {abs(n)}' if n < 0 else (f'plus {n}' if n > 0 else 'zéro')


def word_en(n):
    return f'negative {abs(n)}' if n < 0 else (f'positive {n}' if n > 0 else 'zero')


# ── pictures ─────────────────────────────────────────────────────────────────

def thermometer(temp, lo, hi, step, minor=None):
    shape = {'type': 'thermometer', 'temp': temp, 'min_temp': lo, 'max_temp': hi, 'step': step}
    if minor:
        shape['minor'] = minor
    return shape


def int_line(lo, hi, step, point=None, labels_every=1, w=330):
    """Number line from lo to hi with a tick every ``step``; labels every ``labels_every`` ticks; '?' at ``point``."""
    c = Canvas(w, 74, max_h=90, css_w='max-w-md')
    x0, x1, y = 18, w - 18, 38
    c.line(x0, y, x1, y, sw=2.5)
    n = (hi - lo) // step
    seg = (x1 - x0) / n
    for i in range(n + 1):
        v = lo + i * step
        x = x0 + i * seg
        big = i % labels_every == 0
        c.line(x, y - (9 if big else 5), x, y + (9 if big else 5), sw=2.5 if big else 1.5,
               color=RED if v == 0 else INK)
        if big:
            c.text(x, y + 26, s(v), size=12, bold=True, color=RED if v == 0 else INK)
    if point is not None:
        xp = x0 + (point - lo) / step * seg
        c.dot(xp, y, r=6, fill=BLUE)
        c.text(xp, y - 14, '?', size=15, bold=True, color=BLUE)
    return c.shape()


def plane(points, size=5, cell=26):
    """Cartesian plane from −size to +size on both axes, points = {label: (x, y)}."""
    w = h = 2 * size * cell + 40
    c = Canvas(w, h, max_h=300, css_w='max-w-sm')
    ox, oy = w / 2, h / 2
    for k in range(-size, size + 1):
        c.line(ox + k * cell, oy - size * cell, ox + k * cell, oy + size * cell, color=SOFT, sw=1, opacity=0.9)
        c.line(ox - size * cell, oy + k * cell, ox + size * cell, oy + k * cell, color=SOFT, sw=1, opacity=0.9)
    c.line(ox - size * cell - 8, oy, ox + size * cell + 8, oy, color=INK, sw=2)
    c.line(ox, oy + size * cell + 8, ox, oy - size * cell - 8, color=INK, sw=2)
    c.text(ox + size * cell + 12, oy + 4, 'x', size=12, bold=True, anchor='start')
    c.text(ox + 6, oy - size * cell - 10, 'y', size=12, bold=True, anchor='start')
    for k in range(-size, size + 1):
        if k == 0:
            continue
        c.text(ox + k * cell, oy + 15, s(k), size=10, bold=True)
        c.text(ox - 5, oy - k * cell + 4, s(k), size=10, bold=True, anchor='end')
    c.text(ox - 5, oy + 15, '0', size=10, bold=True, anchor='end')
    for label, (x, y) in points.items():
        X, Y = ox + x * cell, oy - y * cell
        c.dot(X, Y, r=5, fill=PURPLE)
        c.text(X + 7, Y - 7, label, size=14, bold=True, color=PURPLE, anchor='start')
    return c.shape()


# ── contexts (naturally signed) ──────────────────────────────────────────────

CITIES = ['Québec', 'Montréal', 'Chibougamau', 'Gaspé', 'Iqaluit', 'Kuujjuaq', 'Rouyn-Noranda', 'Sherbrooke']


def _context(lo=-30, hi=30):
    """A value with a natural sign and its description, as (value, fr, en, unit)."""
    kind = random.choice(['temp', 'temp', 'floor', 'sea'])
    if kind == 'temp':
        v = random.randint(lo, hi)
        city = random.choice(CITIES)
        return v, f'{city} : {s(v)} °C', f'{city}: {s(v)} °C', '°C'
    if kind == 'floor':
        v = random.choice([x for x in range(-4, 9) if x])
        return v, f'étage {s(v)}', f'floor {s(v)}', ''
    v = random.choice([x for x in range(-60, 61, 5) if x])
    return v, f'{s(v)} m', f'{s(v)} m', 'm'


# ── generators ───────────────────────────────────────────────────────────────

def g6_integer_thermometer_gen(level='easy'):
    """Read thermometers below zero; rises / drops that cross zero (QC-056, 058, 059)."""
    if level in ('easy', 'medium'):
        if level == 'easy':
            t = random.choice([v for v in range(-20, 21, 5) if v < 0 or random.random() < 0.3])
            shape = thermometer(t, -20, 20, 5)
        else:
            t = random.choice([v for v in range(-20, 21, 2) if v < 0 or random.random() < 0.3])
            shape = thermometer(t, -20, 20, 10, minor=2)
        return typed(('Quelle température indique ce thermomètre ?', 'What temperature does this thermometer show?'),
                     ans(t, '°C'), 'signed',
                     ('Sous le 0, les nombres sont négatifs : plus on descend, plus il fait froid.',
                      'Below 0 the numbers are negative: the lower you go, the colder it is.'),
                     (f'Le liquide s’arrête {"sous" if t < 0 else "au-dessus de"} 0, à {s(t)} °C.' if t else 'Le liquide s’arrête à 0 °C.',
                      f'The liquid stops {"below" if t < 0 else "above"} 0, at {s(t)} °C.' if t else 'The liquid stops at 0 °C.'),
                     shape=shape)
    city = random.choice(CITIES)
    kind = random.choice(['rise', 'drop', 'gap'])
    if kind == 'rise':
        a = random.randint(-15, -1)
        d = random.randint(2, 20)
        b = a + d
        return typed((f'À {city}, il fait {s(a)} °C le matin. La température monte de {d} degrés. Quelle température fait-il ensuite ?',
                      f'In {city} it is {s(a)} °C in the morning. The temperature rises by {d} degrees. What is the temperature then?'),
                     ans(b, '°C'), 'signed',
                     ('« Monte » : avance vers le haut du thermomètre (vers les nombres plus grands).', '“Rises”: move up the thermometer (towards bigger numbers).'),
                     ([f'De {s(a)} à 0 : {abs(a)} degrés', f'Il reste {d} − {abs(a)} = {d - abs(a)} degrés' if b >= 0 else f'{d} degrés ne suffisent pas pour atteindre 0',
                       f'Réponse : {s(b)} °C'],
                      [f'From {s(a)} to 0: {abs(a)} degrees', f'{d} − {abs(a)} = {d - abs(a)} degrees left' if b >= 0 else f'{d} degrees are not enough to reach 0',
                       f'Answer: {s(b)} °C']),
                     shape=thermometer(a, -20, 20, 10, minor=2))
    if kind == 'drop':
        a = random.randint(1, 15)
        d = random.randint(a + 1, a + 15)
        b = a - d
        return typed((f'À {city}, il fait {a} °C à midi. Le soir, la température baisse de {d} degrés. Quelle température fait-il le soir ?',
                      f'In {city} it is {a} °C at noon. In the evening the temperature drops by {d} degrees. What is the evening temperature?'),
                     ans(b, '°C'), 'signed',
                     ('Descends d’abord jusqu’à 0, puis continue sous 0.', 'First go down to 0, then keep going below 0.'),
                     ([f'De {a} à 0 : {a} degrés', f'Encore {d} − {a} = {d - a} degrés sous 0', f'Réponse : {s(b)} °C'],
                      [f'From {a} to 0: {a} degrees', f'Another {d} − {a} = {d - a} degrees below 0', f'Answer: {s(b)} °C']))
    a = random.randint(-18, -1)
    b = random.randint(1, 18)
    return typed((f'La nuit, il fait {s(a)} °C à {city}. Le jour, il fait {b} °C. Quel est l’écart entre les deux températures ?',
                  f'At night it is {s(a)} °C in {city}. During the day it is {b} °C. What is the gap between the two temperatures?'),
                 [f'{b - a} °C', str(b - a)], 'integer',
                 ('Compte les degrés de la température négative jusqu’à 0, puis de 0 jusqu’à la température positive.',
                  'Count the degrees from the negative temperature up to 0, then from 0 up to the positive one.'),
                 ([f'De {s(a)} à 0 : {abs(a)} degrés', f'De 0 à {b} : {b} degrés', f'{abs(a)} + {b} = {b - a} °C'],
                  [f'From {s(a)} to 0: {abs(a)} degrees', f'From 0 to {b}: {b} degrees', f'{abs(a)} + {b} = {b - a} °C']))


def g6_integer_number_line_gen(level='easy'):
    """Locate integers on a number line (QC-058)."""
    if level == 'easy':
        lo = random.choice([-10, -8, -6, -5])
        p = random.choice([v for v in range(lo, -lo + 1) if v < 0])
        shape = int_line(lo, -lo, 1, p, labels_every=5 if lo in (-10, -5) else 2)
    elif level == 'medium':
        step = random.choice([2, 5])
        lo = -10 * step // 2 if step == 2 else -25
        p = random.choice([v for v in range(lo, -lo + 1, step) if v < 0 and v % (step * 5)])
        shape = int_line(lo, -lo, step, p, labels_every=5)
    else:
        start = random.randint(-6, 6)
        d = random.randint(3, 9)
        left = random.random() < 0.6
        end = start - d if left else start + d
        if end >= 0 and start >= 0:
            start, end = start - 6, end - 6
        return typed((f'Sur une droite numérique, pars de {s(start)} et avance de {d} unités vers la {"gauche" if left else "droite"}. Sur quel nombre arrives-tu ?',
                      f'On a number line, start at {s(start)} and move {d} units to the {"left" if left else "right"}. Which number do you land on?'),
                     ans(end), 'signed',
                     ('Vers la gauche, les nombres diminuent ; vers la droite, ils augmentent.', 'To the left numbers get smaller; to the right they get bigger.'),
                     ([f'{s(start)} {"−" if left else "+"} {d} unités → {s(end)}', f'Réponse : {s(end)}'],
                      [f'{s(start)} {"−" if left else "+"} {d} units → {s(end)}', f'Answer: {s(end)}']),
                     shape=int_line(-15, 15, 1, None, labels_every=5))
    return typed(('Quel nombre est placé au point « ? » sur cette droite numérique ?', 'Which number is at the point “?” on this number line?'),
                 ans(p), 'signed',
                 ('Trouve ce que vaut un petit intervalle, puis compte à partir de 0 ou d’un nombre écrit.',
                  'Work out what one small step is worth, then count from 0 or from a written number.'),
                 (f'Le point est à gauche de 0 : c’est un nombre négatif, {s(p)}.', f'The point is left of 0, so it is a negative number: {s(p)}.'),
                 shape=shape)


def _pair(level):
    if level == 'easy':
        a = random.randint(-12, -1)
        b = random.choice([random.randint(1, 12), 0])
    elif level == 'medium':
        a, b = random.sample([v for v in range(-20, 0)], 2)
    else:
        a = random.randint(-40, -2)
        b = random.choice([-a, a + random.choice([-1, 1]) * random.randint(1, 5)])
        if b == a:
            b = a - 1
    if random.random() < 0.5:
        a, b = b, a
    return a, b


def g6_integer_compare_gen(level='easy'):
    """Compare integers with < and > (QC-059)."""
    a, b = _pair(level)
    sym = '<' if a < b else '>'
    ctx = random.choice(['plain', 'temp', 'sea']) if level != 'easy' else random.choice(['plain', 'temp'])
    if ctx == 'temp':
        p = (f'Quel symbole complète la phrase ? {s(a)} °C ___ {s(b)} °C', f'Which symbol completes the sentence? {s(a)} °C ___ {s(b)} °C')
    elif ctx == 'sea':
        p = (f'Un plongeur est à {s(a)} m, un autre à {s(b)} m (0 m = niveau de la mer). Quel symbole va entre les deux altitudes ? {s(a)} ___ {s(b)}',
             f'One diver is at {s(a)} m, another at {s(b)} m (0 m = sea level). Which symbol goes between the two altitudes? {s(a)} ___ {s(b)}')
    else:
        p = (f'Quel symbole va entre ces deux nombres ? {s(a)} ___ {s(b)}', f'Which symbol goes between these two numbers? {s(a)} ___ {s(b)}')
    big, small = max(a, b), min(a, b)
    why_fr = (f'{s(small)} est plus à gauche sur la droite numérique que {s(big)}' +
              (' : entre deux nombres négatifs, celui qui est le plus loin de 0 est le plus petit.' if big < 0 else '.'))
    why_en = (f'{s(small)} is further left on the number line than {s(big)}' +
              ('; between two negative numbers, the one further from 0 is the smaller.' if big < 0 else '.'))
    other = '>' if sym == '<' else '<'
    return mc(p, sym, [(other, 'reversed', 'Bigger digits do not mean a bigger negative number.', 'Un plus grand chiffre ne veut pas dire un plus grand nombre négatif.'),
                       ('=', 'equal', '', '')],
              ('Imagine les deux nombres sur une droite numérique : le plus à droite est le plus grand.',
               'Picture both numbers on a number line: the one further right is bigger.'),
              ([why_fr, f'{s(a)} {sym} {s(b)}'], [why_en, f'{s(a)} {sym} {s(b)}']),
              pad=lambda: random.choice(['≤', '≥']), answer_type='symbol')


def g6_integer_order_gen(level='easy'):
    """Order integers, increasing or decreasing (QC-060)."""
    n = 4 if level == 'easy' else 5
    span = {'easy': 10, 'medium': 25, 'hard': 60}[level]
    vals = random.sample([v for v in range(-span, span + 1)], n)
    if not any(v < 0 for v in vals):
        vals[0] = -random.randint(1, span)
    if level == 'hard':                       # opposites side by side make it harder
        k = random.randint(2, span)
        vals[:2] = [k, -k]
        vals = list(dict.fromkeys(vals))
        while len(vals) < n:
            v = random.randint(-span, span)
            if v not in vals:
                vals.append(v)
    up = random.random() < 0.6
    order = sorted(vals, reverse=not up)
    temps = random.random() < 0.5
    unit = ' °C' if temps else ''
    labels = [f'{s(v)}{unit}' for v in order]
    if temps:
        p = (f'Range ces températures de la plus {"froide" if up else "chaude"} à la plus {"chaude" if up else "froide"}.',
             f'Put these temperatures in order from the {"coldest" if up else "warmest"} to the {"warmest" if up else "coldest"}.')
    else:
        p = (f'Range ces nombres dans l’ordre {"croissant" if up else "décroissant"}.',
             f'Put these numbers in {"increasing" if up else "decreasing"} order.')
    return ordering(p, labels,
                    ('Les nombres négatifs viennent avant 0 ; parmi eux, le plus loin de 0 est le plus petit.',
                     'Negative numbers come before 0; among them, the one furthest from 0 is the smallest.'),
                    (' < '.join(s(v) for v in sorted(vals)) if up else ' > '.join(s(v) for v in sorted(vals, reverse=True)),
                     ' < '.join(s(v) for v in sorted(vals)) if up else ' > '.join(s(v) for v in sorted(vals, reverse=True))))


_SITUATIONS = [
    # (fr, en, value)
    ('un plongeur à {n} m sous le niveau de la mer', 'a diver {n} m below sea level', -1),
    ('un avion à {n} m au-dessus du niveau de la mer', 'a plane {n} m above sea level', 1),
    ('le {n}e sous-sol d’un stationnement', 'level {n} of an underground car park', -1),
    ('le {n}e étage d’un immeuble', 'floor {n} of a building', 1),
    ('{n} degrés sous zéro', '{n} degrees below zero', -1),
    ('{n} degrés au-dessus de zéro', '{n} degrees above zero', 1),
]


def g6_integer_read_gen(level='easy'):
    """Read, write and name integers; translate a situation (QC-057, 061)."""
    kind = random.choice(['read', 'sign'] if level == 'easy' else ['situation', 'read', 'opposite'] if level == 'medium' else ['situation', 'opposite', 'which_negative'])
    if kind == 'read':
        n = -random.randint(2, 99)
        d = [(word_fr(-n), word_en(-n)), (f'{abs(n)} moins', f'{abs(n)} minus'), (word_fr(n - 1), word_en(n - 1))]
        return mc((f'Comment lit-on le nombre {s(n)} ?', f'How do you read the number {s(n)}?'),
                  (word_fr(n), word_en(n)), d,
                  ('Le signe « − » devant un nombre se lit « moins ».', 'The “−” sign in front of a number is read “negative”.'),
                  (f'{s(n)} se lit « {word_fr(n)} ».', f'{s(n)} is read “{word_en(n)}”.'),
                  pad=lambda: (lambda m: (word_fr(m), word_en(m)))(n + random.choice([-10, 1, 10, 2])))
    if kind == 'sign':
        n = random.choice([v for v in range(-30, 31) if v])
        pos = n > 0
        return mc((f'Le nombre {s(n)} est-il positif ou négatif ?', f'Is the number {s(n)} positive or negative?'),
                  ('Positif', 'Positive') if pos else ('Négatif', 'Negative'),
                  [('Négatif', 'Negative') if pos else ('Positif', 'Positive'), ('Ni l’un ni l’autre', 'Neither')],
                  ('Un nombre négatif s’écrit avec le signe « − » ; il est plus petit que 0.', 'A negative number is written with a “−” sign; it is less than 0.'),
                  (f'{s(n)} est {"plus grand" if pos else "plus petit"} que 0 : il est {"positif" if pos else "négatif"}.',
                   f'{s(n)} is {"greater" if pos else "less"} than 0, so it is {"positive" if pos else "negative"}.'),
                  pad=lambda: random.choice([('Égal à zéro', 'Equal to zero'), ('Un nombre décimal', 'A decimal number')]))
    if kind == 'opposite':
        n = random.choice([v for v in range(-50, 51) if v])
        return typed((f'Quel est l’opposé de {s(n)} ? (le nombre à la même distance de 0, de l’autre côté)',
                      f'What is the opposite of {s(n)}? (the number at the same distance from 0, on the other side)'),
                     ans(-n), 'signed',
                     ('Garde la même distance à 0 et change de côté.', 'Keep the same distance from 0 and switch sides.'),
                     (f'{s(n)} est à {abs(n)} unités de 0 ; de l’autre côté on trouve {s(-n)}.', f'{s(n)} is {abs(n)} units from 0; on the other side is {s(-n)}.'))
    if kind == 'which_negative':
        sits = random.sample(_SITUATIONS, 4)
        if not any(x[2] < 0 for x in sits):
            sits[0] = random.choice([x for x in _SITUATIONS if x[2] < 0])
        if sum(x[2] < 0 for x in sits) > 1:
            neg = [x for x in sits if x[2] < 0][0]
            sits = [neg] + [x for x in _SITUATIONS if x[2] > 0][:3]
        k = random.randint(2, 9)
        lab = lambda x: (x[0].format(n=k), x[1].format(n=k))
        correct = next(x for x in sits if x[2] < 0)
        return mc(('Laquelle de ces situations se représente par un nombre négatif ?', 'Which of these situations is shown with a negative number?'),
                  lab(correct), [lab(x) for x in sits if x is not correct],
                  ('Sous zéro, sous le sol ou sous le niveau de la mer : nombre négatif.', 'Below zero, below ground or below sea level: negative number.'),
                  (f'« {lab(correct)[0]} » se note {s(-k)}.', f'“{lab(correct)[1]}” is written {s(-k)}.'),
                  pad=lambda: (f'{random.randint(2, 20)} élèves dans une classe', f'{random.randint(2, 20)} students in a class'))
    sit = random.choice(_SITUATIONS)
    k = random.randint(2, 9) if 'étage' in sit[0] or 'sous-sol' in sit[0] else random.choice(range(5, 205, 5))
    v = sit[2] * k
    return typed((f'Écris un nombre entier pour représenter : {sit[0].format(n=k)}.', f'Write an integer for: {sit[1].format(n=k)}.'),
                 ans(v) + ([f'+{v}'] if v > 0 else []), 'signed',
                 ('Au-dessus de 0 (ou du sol, ou de la mer) : positif. En dessous : négatif.', 'Above 0 (or ground, or sea level): positive. Below: negative.'),
                 (f'{"En dessous" if v < 0 else "Au-dessus"} de la référence, donc {s(v)}.', f'{"Below" if v < 0 else "Above"} the reference, so {s(v)}.'))


def _pt(size, quad=None):
    """A point strictly inside the grid (the border would collide with the axis numbers)."""
    while True:
        x, y = random.randint(1 - size, size - 1), random.randint(1 - size, size - 1)
        if x and y and (quad is None or _quadrant(x, y) == quad):
            return x, y


def _quadrant(x, y):
    return 1 if x > 0 and y > 0 else 2 if x < 0 < y else 3 if x < 0 and y < 0 else 4


ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}


def g6_cartesian_4q_gen(level='easy'):
    """Points in the four quadrants (QC-058, 136)."""
    size = 5
    if level == 'easy':
        quads = random.sample([2, 3, 4, 1], 4)
        pts = {}
        for lab, q in zip('ABCD', quads):
            p = _pt(size, q)
            while p in pts.values():
                p = _pt(size, q)
            pts[lab] = p
        lab = random.choice([l for l in pts if _quadrant(*pts[l]) != 1])
        x, y = pts[lab]
        key = f'({s(x)}, {s(y)})'
        wrong = [(f'({s(y)}, {s(x)})', 'swapped', 'x comes first, then y.', 'On écrit d’abord x, puis y.'),
                 (f'({s(-x)}, {s(y)})', 'sign_x', '', ''), (f'({s(x)}, {s(-y)})', 'sign_y', '', '')]
        return mc((f'Quelles sont les coordonnées du point {lab} ?', f'What are the coordinates of point {lab}?'), key, wrong,
                  ('x : avance à gauche (−) ou à droite (+) depuis l’origine ; y : monte (+) ou descends (−).',
                   'x: go left (−) or right (+) from the origin; y: go up (+) or down (−).'),
                  (f'{lab} est {abs(x)} {"à gauche" if x < 0 else "à droite"} et {abs(y)} {"en bas" if y < 0 else "en haut"} : {key}.',
                   f'{lab} is {abs(x)} to the {"left" if x < 0 else "right"} and {abs(y)} {"down" if y < 0 else "up"}: {key}.'),
                  shape=plane(pts), pad=lambda: f'({s(random.randint(-5, 5))}, {s(random.randint(-5, 5))})')
    if level == 'medium':
        x, y = _pt(size)
        q = _quadrant(x, y)
        return mc((f'Dans quel quadrant se trouve le point ({s(x)}, {s(y)}) ?', f'Which quadrant is the point ({s(x)}, {s(y)}) in?'),
                  (f'Quadrant {ROMAN[q]}', f'Quadrant {ROMAN[q]}'),
                  [(f'Quadrant {ROMAN[k]}', f'Quadrant {ROMAN[k]}') for k in (1, 2, 3, 4) if k != q]
                  + [('Sur un des axes', 'On one of the axes')],
                  ('I : (+, +) · II : (−, +) · III : (−, −) · IV : (+, −).', 'I: (+, +) · II: (−, +) · III: (−, −) · IV: (+, −).'),
                  (f'x est {"négatif" if x < 0 else "positif"} et y est {"négatif" if y < 0 else "positif"} : quadrant {ROMAN[q]}.',
                   f'x is {"negative" if x < 0 else "positive"} and y is {"negative" if y < 0 else "positive"}: quadrant {ROMAN[q]}.'),
                  shape=plane({}))
    if random.random() < 0.5:
        from ..widgets import place_point
        x, y = _pt(size)
        return place_point((f'Place le point ({s(x)}, {s(y)}) dans le plan cartésien.', f'Place the point ({s(x)}, {s(y)}) on the coordinate plane.'),
                           (x, y),
                           ('Pars de l’origine : x négatif → à gauche, y négatif → en bas.', 'Start at the origin: negative x → left, negative y → down.'),
                           (f'{abs(x)} {"à gauche" if x < 0 else "à droite"}, puis {abs(y)} {"en bas" if y < 0 else "en haut"}.',
                            f'{abs(x)} to the {"left" if x < 0 else "right"}, then {abs(y)} {"down" if y < 0 else "up"}.'),
                           xmin=-size, xmax=size, ymin=-size, ymax=size)
    pts = {}
    for lab in 'ABCDE':
        p = _pt(size)
        while p in pts.values():
            p = _pt(size)
        pts[lab] = p
    lab = random.choice(list(pts))
    x, y = pts[lab]
    return typed((f'Écris les coordonnées du point {lab} sous la forme (x, y).', f'Write the coordinates of point {lab} as (x, y).'),
                 [f'({s(x)}, {s(y)})', f'({x}, {y})'], 'coordinate',
                 ('Lis d’abord sur l’axe horizontal (x), puis sur l’axe vertical (y).', 'Read the horizontal axis (x) first, then the vertical axis (y).'),
                 (f'{lab} = ({s(x)}, {s(y)})', f'{lab} = ({s(x)}, {s(y)})'),
                 shape=plane(pts))
