"""
early_numbers.py — curriculum upgrade WP1, grades 1–2: numbers and operations (2026-10).

Counting, counting on, skip counting, estimating, base-ten blocks, the hundred
chart, comparing and ordering, addition and subtraction facts and strategies,
two-digit addition/subtraction on an open number line, story problems, equal
groups, true equalities and missing numbers. Short sentences, small numbers,
a picture whenever it helps (prompts can be read aloud).
"""
import random

from quiz import illustrations as I
from .kit import mc, typed, ordering, pick

L5 = list('ABCDE')
ICONS = [('🍎', 'pommes', 'apples'), ('⭐', 'étoiles', 'stars'), ('🐟', 'poissons', 'fish'), ('🎈', 'ballons', 'balloons'),
         ('🐞', 'coccinelles', 'ladybugs'), ('🌸', 'fleurs', 'flowers'), ('🚗', 'voitures', 'cars'), ('🍪', 'biscuits', 'cookies')]


def _pad_numbers(correct, lo, hi):
    def pad():
        return str(random.randint(lo, hi))
    return pad


# ── E1.1 Count objects ───────────────────────────────────────────────────────

def g1_count_objects_gen(level='easy'):
    """How many? (004, 006, 009)"""
    icon, fr, en = pick(ICONS)
    if level == 'easy':
        n = random.randint(3, 10)
        pic = I.emoji_set(icon, n, per_row=5)
    elif level == 'medium':
        n = random.randint(11, 20)
        pic = I.emoji_set(icon, n, group_tens=True)
    else:
        n = random.randint(21, 60)
        pic = I.emoji_set(icon, n, group_tens=True, size=18)
    hint = ('Touche chaque objet une seule fois en comptant.', 'Touch each object only once as you count.') if level == 'easy' else \
           ('Chaque rangée complète a 10 objets. Compte les dizaines, puis les autres.', 'Each full row has 10. Count the tens, then the rest.')
    expl = (f'Il y a {n} {fr}.', f'There are {n} {en}.') if level == 'easy' else \
           ([f'{n // 10} rangée{"s" if n // 10 > 1 else ""} de 10 = {n // 10 * 10}', f'{n // 10 * 10} + {n % 10} = {n}'],
            [f'{n // 10} row{"s" if n // 10 > 1 else ""} of 10 = {n // 10 * 10}', f'{n // 10 * 10} + {n % 10} = {n}'])
    return typed((f'Combien y a-t-il de {fr} ?', f'How many {en} are there?'), [n], 'integer', hint, expl, shape=pic)


# ── E1.2 Count on ────────────────────────────────────────────────────────────

def g1_count_on_gen(level='easy'):
    """Count on from a number; what comes after / before (001, 005)."""
    hi = {'easy': 20, 'medium': 60, 'hard': 99}[level]
    if level == 'hard':
        a = random.randint(2, 9) * 10 - random.randint(1, 3)          # crosses a ten
    else:
        a = random.randint(1, hi - 5)
    k = random.randint(1, 3) if level != 'easy' else 1
    if random.random() < 0.5 or level == 'easy':
        seq = [a + i for i in range(3)]
        ans = a + 2 + k
        s = ', '.join(map(str, seq)) + (', …' if k > 1 else '')
        if k == 1:
            return typed((f'Continue à compter : {s}, ?', f'Keep counting: {s}, ?'), [ans], 'integer',
                         ('Ajoute 1 au dernier nombre.', 'Add 1 to the last number.'),
                         (f'Après {a + 2} vient {ans}.', f'After {a + 2} comes {ans}.'))
        return typed((f'Quel nombre vient {k} places après {a + 2} ?', f'Which number comes {k} places after {a + 2}?'), [ans], 'integer',
                     ('Compte en avançant de 1 à la fois.', 'Count forward one at a time.'),
                     (f'{", ".join(str(a + 2 + i) for i in range(k + 1))} → {ans}', f'{", ".join(str(a + 2 + i) for i in range(k + 1))} → {ans}'))
    b = a + 3
    return typed((f'Quel nombre vient juste **avant** {b} ?', f'Which number comes just **before** {b}?'), [b - 1], 'integer',
                 ('Recule de 1.', 'Go back 1.'), (f'Avant {b} vient {b - 1}.', f'Before {b} comes {b - 1}.'))


# ── E1.3 Skip count ──────────────────────────────────────────────────────────

def g1_skip_count_gen(level='easy'):
    """Count by 2, 5, 10, forwards and backwards (< 100) (002, 003)."""
    step = pick([10, 5] if level == 'easy' else [2, 5, 10])
    back = level == 'hard' and random.random() < 0.6
    if step == 10:
        start = random.randint(0, 5) * 10 if level == 'easy' else random.randint(1, 49)
    elif step == 5:
        start = random.randint(0, 8) * 5
    else:
        start = random.randint(0, 40) * 2 + (0 if level != 'hard' else random.randint(0, 1))
    seq = [start + i * step for i in range(5)]
    if back:
        seq = seq[::-1]
    hide = random.randint(2, 4) if level != 'easy' else 4
    ans = seq[hide]
    shown = ['?' if i == hide else str(v) for i, v in enumerate(seq)]
    return typed((f'Trouve le nombre qui manque : {", ".join(shown)}', f'Find the missing number: {", ".join(shown)}'), [ans], 'integer',
                 (f'On compte de {step} en {step}' + (' en reculant.' if back else '.'), f'We count by {step}s' + (' going backwards.' if back else '.')),
                 (f'{"−" if back else "+"}{step} chaque fois : le nombre manquant est {ans}.', f'{"−" if back else "+"}{step} each time: the missing number is {ans}.'))


# ── E1.4 Estimate a collection ───────────────────────────────────────────────

def g1_estimate_collection_gen(level='easy'):
    """About how many? (021)"""
    options = {'easy': [5, 10, 20, 40, 80], 'medium': [10, 20, 30, 50, 100], 'hard': [20, 40, 60, 80, 100]}[level]
    target = pick(options[1:4])
    spread = 2 if level == 'easy' else 3
    n = target + random.randint(-spread, spread)
    icon, fr, en = pick(ICONS)
    pic = I.emoji_set(icon, n, scatter=True)
    correct = (f'environ {target}', f'about {target}')
    return mc((f'Sans compter un par un : **environ** combien de {fr} vois-tu ?', f'Without counting one by one: **about** how many {en} do you see?'),
              correct, [(f'environ {o}', f'about {o}') for o in options if o != target],
              ('Imagine un petit groupe de 10, puis vois combien de groupes pareils il y a.', 'Picture a small group of 10, then see how many groups like it there are.'),
              (f'Il y en a {n} : c’est environ {target}.', f'There are {n}: about {target}.'),
              shape=pic, time_limit=30)


# ── E1.5 Tens and ones (base-ten blocks) ─────────────────────────────────────

def g2_tens_ones_picture_gen(level='easy'):
    """Base-ten blocks ↔ number (010, 012)."""
    if level == 'medium':
        n = random.randint(21, 99)
        while n % 10 == 0:
            n = random.randint(21, 99)
        t, o = divmod(n, 10)
        variants = [(t, o), (o, t) if o != t and o > 0 else (t, (o + 2) % 10), (t + 1, o), (t, o + 1 if o < 9 else o - 1), (t - 1, o)]
        seen, specs = set(), []
        for v in variants:
            if v not in seen and v[0] >= 0:
                seen.add(v)
                specs.append(v)
        while len(specs) < 5:
            v = (random.randint(1, 9), random.randint(0, 9))
            if v not in seen:
                seen.add(v)
                specs.append(v)
        order = list(range(5))
        random.shuffle(order)
        c, boxes = I.panels(5, 130, 100, cols=3, css_w='max-w-xl')
        for j, box in zip(order, boxes):
            tt, oo = specs[j]
            x0, y0, w, h = box
            unit = 7
            x = x0 + 4
            for _ in range(tt):
                c.rect(x, y0 + 4, unit, 10 * unit, fill=I.SHADES[I.BLUE][1], stroke=I.INK, sw=1.2)
                x += unit + 3
            x += 6
            for k in range(oo):
                col, row = divmod(k, 5)
                c.rect(x + col * (unit + 3), y0 + 4 + 10 * unit - (row + 1) * (unit + 3) + 3, unit, unit,
                       fill=I.SHADES[I.BLUE][0], stroke=I.INK, sw=1.1)
        i = order.index(0)
        return mc((f'Quelle image montre le nombre **{n}** ?', f'Which picture shows the number **{n}**?'),
                  L5[i], [x for x in L5 if x != L5[i]],
                  ('Une barre = 10. Un petit cube = 1.', 'A rod = 10. A small cube = 1.'),
                  (f'{n} = {t} dizaines et {o} unités : image {L5[i]}.', f'{n} = {t} tens and {o} ones: picture {L5[i]}.'),
                  shape=c.shape())
    hundreds = 0 if level == 'easy' else random.randint(1, 3)
    t, o = random.randint(1, 9), random.randint(0, 9)
    n = hundreds * 100 + t * 10 + o
    return typed(('Quel nombre est représenté ?', 'What number is shown?'), [n], 'integer',
                 ('Grande plaque = 100, barre = 10, petit cube = 1.' if hundreds else 'Une barre = 10. Un petit cube = 1.',
                  'Flat = 100, rod = 10, small cube = 1.' if hundreds else 'A rod = 10. A small cube = 1.'),
                 ((f'{hundreds} centaine{"s" if hundreds > 1 else ""}, ' if hundreds else '') + f'{t} dizaine{"s" if t > 1 else ""} et {o} unité{"s" if o > 1 else ""} = {n}',
                  (f'{hundreds} hundred{"s" if hundreds > 1 else ""}, ' if hundreds else '') + f'{t} ten{"s" if t > 1 else ""} and {o} one{"s" if o != 1 else ""} = {n}'),
                 shape=I.base_ten(hundreds, t, o))


# ── E1.6 Hundred chart ───────────────────────────────────────────────────────

def g2_hundred_chart_gen(level='easy'):
    """Missing number in a piece of the hundred chart (017)."""
    rows, cols = (2, 5) if level == 'easy' else (3, 4) if level == 'medium' else (3, 3)
    r0, c0 = random.randint(0, 10 - rows), random.randint(0, 10 - cols)
    if level == 'hard':
        # only the four corners + centre are guaranteed visible: hide the centre's vertical neighbour
        hide_r, hide_c = random.choice([0, rows - 1]), cols // 2
    else:
        hide_r, hide_c = random.randrange(rows), random.randrange(cols)
    n = (r0 + hide_r) * 10 + c0 + hide_c + 1
    return typed(('Voici un morceau du tableau des nombres de 1 à 100. Quel nombre cache le « ? » ?',
                  'Here is a piece of the 1 to 100 chart. Which number is hiding under the “?”?'),
                 [n], 'integer',
                 ('Vers la droite : +1. Vers le bas : +10.', 'To the right: +1. Down: +10.'),
                 (f'Le nombre caché est {n}.', f'The hidden number is {n}.'),
                 shape=I.hundred_window(r0, c0, rows, cols, n))


# ── E1.7 Compare / E1.8 Order ────────────────────────────────────────────────

def g1_compare_gen(level='easy'):
    """Which number is the greatest / smallest? (014)"""
    hi = {'easy': 20, 'medium': 99, 'hard': 999}[level]
    want_big = random.random() < 0.5
    base = random.randint(12, hi)
    pool = {base}
    while len(pool) < 5:
        s = str(base)
        cand = random.choice([int(s[::-1]) if len(s) > 1 and s[::-1][0] != '0' else base + 1,
                              base + random.choice([-10, -1, 1, 10]), random.randint(10, hi)])
        if 1 <= cand <= hi:
            pool.add(cand)
    nums = sorted(pool)
    correct = str(nums[-1] if want_big else nums[0])
    return mc((f'Quel est le **plus {"grand" if want_big else "petit"}** nombre ?', f'Which number is the **{"greatest" if want_big else "smallest"}**?'),
              correct, [str(x) for x in nums if str(x) != correct],
              ('Compare d’abord les centaines, puis les dizaines, puis les unités.' if hi > 99 else 'Compare d’abord les dizaines, puis les unités.',
               'Compare the hundreds first, then the tens, then the ones.' if hi > 99 else 'Compare the tens first, then the ones.'),
              (f'{correct} est le plus {"grand" if want_big else "petit"}.', f'{correct} is the {"greatest" if want_big else "smallest"}.'))


def g2_order_gen(level='easy'):
    """Order numbers < 100 / < 1000 (015)."""
    hi = {'easy': 50, 'medium': 99, 'hard': 999}[level]
    nums = random.sample(range(1, hi + 1), 4)
    if level == 'hard':
        a = random.randint(100, 899)
        nums = list({a, int(str(a)[::-1]) if str(a)[-1] != '0' else a + 9, a + 10, a - 1, a + 100})[:4]
    desc = level != 'easy' and random.random() < 0.4
    nums = sorted(nums, reverse=desc)
    return ordering((f'Range ces nombres du plus {"grand au plus petit" if desc else "petit au plus grand"}.',
                     f'Order these numbers from {"greatest to smallest" if desc else "smallest to greatest"}.'),
                    [str(x) for x in nums],
                    ('Compare les chiffres de gauche à droite.', 'Compare the digits from left to right.'),
                    (' > '.join(map(str, nums)) if desc else ' < '.join(map(str, nums)),) * 2)


# ── E1.9–E1.11 Facts and strategies ──────────────────────────────────────────

def g1_add_facts_gen(level='easy'):
    """Addition facts to 10 / 20 (085, 087)."""
    hi = 10 if level == 'easy' else 20
    if level == 'hard':                      # facts that cross 10: 8 + 5, 9 + 7…
        a = random.randint(2, 9)
        b = random.randint(11 - a, 9)
    else:
        a = random.randint(0, hi if level == 'easy' else 10)
        b = random.randint(0, hi - a) if level == 'easy' else random.randint(0, min(10, hi - a))
    return typed((f'**{a} + {b} = ?**', f'**{a} + {b} = ?**'), [a + b], 'integer',
                 ('Pars du plus grand nombre et avance.', 'Start from the bigger number and count on.'),
                 (f'{a} + {b} = {a + b}',) * 2, time_limit=15 if level == 'hard' else 30)


def g1_sub_facts_gen(level='easy'):
    """Subtraction facts within 10 / 20 (085, 087)."""
    hi = 10 if level == 'easy' else 20
    if level == 'hard':                      # back through 10: 13 − 5, 16 − 8…
        a = random.randint(11, 18)
        b = random.randint(a - 9, 9)
    else:
        a = random.randint(2, hi)
        b = random.randint(0, a)
    return typed((f'**{a} − {b} = ?**', f'**{a} − {b} = ?**'), [a - b], 'integer',
                 ('Recule à partir du plus grand nombre, ou pense à l’addition : ? + ' + str(b) + ' = ' + str(a),
                  'Count back from the bigger number, or think addition: ? + ' + str(b) + ' = ' + str(a)),
                 (f'{a} − {b} = {a - b}',) * 2, time_limit=15 if level == 'hard' else 30)


def g1_fact_strategies_gen(level='easy'):
    """Doubles, near doubles, making ten (086)."""
    kind = pick(['double'] if level == 'easy' else ['near', 'ten'] if level == 'medium' else ['near', 'ten', 'choose'])
    if kind == 'double':
        a = random.randint(1, 10)
        return typed((f'Un double : **{a} + {a} = ?**', f'A double: **{a} + {a} = ?**'), [2 * a], 'integer',
                     ('Un double, c’est le même nombre deux fois.', 'A double is the same number twice.'),
                     (f'{a} + {a} = {2 * a}',) * 2)
    if kind == 'near':
        a = random.randint(2, 9)
        return typed((f'Tu sais que {a} + {a} = {2 * a}. Alors **{a} + {a + 1} = ?**', f'You know {a} + {a} = {2 * a}. So **{a} + {a + 1} = ?**'),
                     [2 * a + 1], 'integer',
                     ('C’est le double, plus 1.', 'It is the double, plus 1.'),
                     (f'{a} + {a + 1} = {a} + {a} + 1 = {2 * a + 1}',) * 2)
    if kind == 'ten':
        a = random.randint(6, 9)
        b = random.randint(11 - a, 9)
        need = 10 - a
        return typed((f'Pour calculer {a} + {b}, on fait d’abord 10 : {a} + {need} = 10. Combien reste-t-il à ajouter ?',
                      f'To work out {a} + {b}, first make 10: {a} + {need} = 10. How much is left to add?'),
                     [b - need], 'integer',
                     (f'On a pris {need} dans {b}.', f'We took {need} out of {b}.'),
                     (f'{b} − {need} = {b - need}, donc {a} + {b} = 10 + {b - need} = {a + b}',
                      f'{b} − {need} = {b - need}, so {a} + {b} = 10 + {b - need} = {a + b}'))
    a = random.randint(2, 9)
    q = pick([('double', f'{a} + {a}'), ('near', f'{a} + {a + 1}'), ('ten', f'9 + {a}')])
    labels = {'double': ('les doubles', 'doubles'), 'near': ('presque un double', 'near doubles'), 'ten': ('faire 10', 'make ten')}
    return mc((f'Quelle stratégie aide le plus pour calculer **{q[1]}** ?', f'Which strategy helps most with **{q[1]}**?'),
              labels[q[0]], [v for k, v in labels.items() if k != q[0]] + [('compter jusqu’à 100', 'count to 100'), ('soustraire', 'subtract')],
              ('Regarde les nombres : sont-ils pareils, presque pareils, ou proches de 10 ?', 'Look at the numbers: the same, almost the same, or close to 10?'),
              ({'double': f'{q[1]} : le même nombre deux fois → les doubles.', 'near': f'{q[1]} : un double plus 1.', 'ten': f'{q[1]} : 9 est presque 10 → faire 10.'}[q[0]],
               {'double': f'{q[1]}: the same number twice → doubles.', 'near': f'{q[1]}: a double plus 1.', 'ten': f'{q[1]}: 9 is almost 10 → make ten.'}[q[0]]))


# ── E1.12 Two-digit + / − on an open number line ─────────────────────────────

def g2_add_sub_2digit_gen(level='easy'):
    """Add/subtract with an open number line (088, 090)."""
    sub = level == 'hard' and random.random() < 0.6 or level == 'medium' and random.random() < 0.4
    a = random.randint(21, 69)
    tens, ones = random.randint(1, 3), random.randint(1, 8) if level != 'easy' else 0
    if sub:
        a = random.randint(45, 98)
        tens, ones = random.randint(1, 3), random.randint(1, 8)
    b = tens * 10 + ones
    jumps = [10] * tens + ([ones] if ones else [])
    if sub:
        jumps = [-j for j in jumps]
    ans = a - b if sub else a + b
    op = '−' if sub else '+'
    return typed((f'Utilise les bonds sur la droite : **{a} {op} {b} = ?**', f'Use the jumps on the line: **{a} {op} {b} = ?**'), [ans], 'integer',
                 ('Fais d’abord les bonds de 10, puis le petit bond.', 'Do the jumps of 10 first, then the small jump.'),
                 (f'{a} {op} {b} = {ans}',) * 2, shape=I.number_jumps(a, jumps))


# ── E1.13 Story problems ─────────────────────────────────────────────────────

NAMES = ['Léo', 'Emma', 'Nathan', 'Lily', 'Adam', 'Zoé', 'Malik', 'Rose']


def g1_story_add_sub_gen(level='easy'):
    """Join, separate and compare stories (062, 063)."""
    icon, fr, en = pick(ICONS)
    who, other = random.sample(NAMES, 2)
    hi = 10 if level == 'easy' else 20
    kind = pick(['join', 'separate'] if level == 'easy' else ['join', 'separate', 'compare'])
    if kind == 'join':
        a, b = random.randint(1, hi - 2), random.randint(1, 5)
        b = min(b, hi - a)
        return typed((f'{who} a {a} {fr}. On lui en donne {b} de plus. Combien de {fr} a {who} maintenant ?',
                      f'{who} has {a} {en}. {who} gets {b} more. How many {en} does {who} have now?'),
                     [a + b], 'integer', ('On en ajoute : addition.', 'Some are added: addition.'), (f'{a} + {b} = {a + b}',) * 2,
                     shape=I.emoji_set(icon, a + b, per_row=10) if level == 'easy' else None)
    if kind == 'separate':
        a = random.randint(4, hi)
        b = random.randint(1, a - 1)
        return typed((f'{who} a {a} {fr}. {who} en donne {b} à {other}. Combien lui en reste-t-il ?',
                      f'{who} has {a} {en}. {who} gives {b} to {other}. How many are left?'),
                     [a - b], 'integer', ('On en enlève : soustraction.', 'Some are taken away: subtraction.'), (f'{a} − {b} = {a - b}',) * 2,
                     shape=I.emoji_set(icon, a, per_row=10) if level == 'easy' else None)
    a = random.randint(6, hi)
    b = random.randint(1, a - 1)
    return typed((f'{who} a {a} {fr}. {other} en a {b}. Combien de {fr} {who} a-t-il de plus que {other} ?',
                  f'{who} has {a} {en}. {other} has {b}. How many more {en} does {who} have than {other}?'),
                 [a - b], 'integer', ('Combien de plus : on cherche l’écart.', 'How many more: find the difference.'), (f'{a} − {b} = {a - b}',) * 2)


# ── E1.14 Equal groups ───────────────────────────────────────────────────────

def g2_equal_groups_gen(level='easy'):
    """Equal groups and sharing: meaning of × and ÷ (066)."""
    icon = pick(['🍪', '🍓', '⚽', '🌸', '🐟'])
    g, e = random.randint(2, 4 if level == 'easy' else 5), random.randint(2, 5)
    pic = I.equal_groups(g, e, icon)
    if level == 'easy':
        return typed((f'Il y a {g} assiettes avec {e} {icon} dans chacune. Combien de {icon} en tout ?',
                      f'There are {g} plates with {e} {icon} on each. How many {icon} in all?'),
                     [g * e], 'integer', ('Compte par bonds : ' + ', '.join(str(e * k) for k in range(1, g + 1)), 'Skip count: ' + ', '.join(str(e * k) for k in range(1, g + 1))),
                     (f'{g} groupes de {e} = {g * e}', f'{g} groups of {e} = {g * e}'), shape=pic)
    if level == 'medium':
        correct = (f'{g} groupes de {e}', f'{g} groups of {e}')
        wrong = [(f'{e} groupes de {g}', f'{e} groups of {g}') if e != g else (f'{g} groupes de {e + 1}', f'{g} groups of {e + 1}'),
                 (f'{g} groupes de {e + 1}', f'{g} groups of {e + 1}'), (f'{g + 1} groupes de {e}', f'{g + 1} groups of {e}'),
                 (f'1 groupe de {g * e}', f'1 group of {g * e}'), (f'{g} groupes de {max(1, e - 1)}', f'{g} groups of {max(1, e - 1)}')]
        return mc(('Que montre cette image ?', 'What does this picture show?'), correct, wrong,
                  ('Compte les assiettes, puis les objets dans une assiette.', 'Count the plates, then the objects on one plate.'),
                  (f'{g} assiettes, {e} dans chacune : {g} groupes de {e} ({g} × {e} = {g * e}).', f'{g} plates, {e} on each: {g} groups of {e} ({g} × {e} = {g * e}).'),
                  shape=pic)
    total = g * e
    return typed((f'On partage {total} {icon} également dans {g} assiettes. Combien de {icon} dans chaque assiette ?',
                  f'{total} {icon} are shared equally on {g} plates. How many {icon} on each plate?'),
                 [e], 'integer', ('Distribue un objet à la fois dans chaque assiette.', 'Deal out one object at a time to each plate.'),
                 (f'{total} ÷ {g} = {e}', f'{total} ÷ {g} = {e}'))


# ── E1.15 True equality / E1.16 Missing number ───────────────────────────────

def _expr(v, hi):
    if random.random() < 0.5 and v > 0:
        a = random.randint(0, v)
        return f'{a} + {v - a}'
    b = random.randint(0, hi - v)
    return f'{v + b} − {b}'


def g1_true_equality_gen(level='easy'):
    """Is 3 + 2 = 6 − 1 true? (068, 069)"""
    hi = 10 if level == 'easy' else 20
    v = random.randint(2, hi - 2)
    left, right = _expr(v, hi), _expr(v, hi)
    while right == left:
        right = _expr(v, hi)
    correct = f'{left} = {right}'
    wrong = set()
    while len(wrong) < 4:
        w = v + random.choice([-2, -1, 1, 2])
        if 0 <= w <= hi:
            wrong.add(f'{_expr(v, hi)} = {_expr(w, hi)}')
    return mc(('Quelle égalité est **vraie** ?', 'Which equality is **true**?'), correct, sorted(wrong),
              ('Calcule les deux côtés du signe =. Ils doivent être pareils.', 'Work out both sides of the = sign. They must be the same.'),
              (f'{left} = {v} et {right} = {v}.', f'{left} = {v} and {right} = {v}.'))


def g1_missing_number_gen(level='easy'):
    """□ + 4 = 9 and the other forms (093)."""
    hi = 10 if level == 'easy' else 20
    a = random.randint(1, hi - 1)
    b = random.randint(1, hi - a)
    c = a + b
    forms = [(f'? + {b} = {c}', a), (f'{a} + ? = {c}', b), (f'{c} − ? = {a}', b), (f'? − {b} = {a}', c),
             (f'{c} = ? + {b}', a), (f'{a} = {c} − ?', b)]
    pool = forms[:2] if level == 'easy' else forms[:4] if level == 'medium' else forms
    expr, ans = pick(pool)
    return typed((f'Quel nombre cache le « ? » : **{expr}**', f'Which number is hiding under the “?”: **{expr}**'), [ans], 'integer',
                 ('Pense aux familles de nombres : ' + f'{a} + {b} = {c}, {c} − {b} = {a}.', 'Think of number families: ' + f'{a} + {b} = {c}, {c} − {b} = {a}.'),
                 (f'{expr.replace("?", str(ans))}',) * 2)
