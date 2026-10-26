"""
decimal_equivalences_plus.py — numerical equivalences with decimals (audit QC-079 grade 4, QC-080 grades 5–6).

The whole-number versions are g4-equivalent-expressions / g4-properties / g6-distributive; these skills reuse the
same ideas with tenths and hundredths:

    g4-decimal-equivalences   addition ↔ subtraction, commutativity, associativity, compensation (QC-079)
    g5-decimal-properties     the four operations: × ↔ ÷, distributivity, commutativity of ×, halving / doubling (QC-080)

All arithmetic is done in whole hundredths so no float rounding can creep into a key.
"""
import random

from .kit import mc, typed


def d(h, lang):
    """Hundredths → displayed decimal: d(275, 'fr') → '2,75', d(250, 'en') → '2.5', d(300, 'fr') → '3'."""
    neg, h = h < 0, abs(h)
    s = f'{h // 100}.{h % 100:02d}'.rstrip('0').rstrip('.')
    return ('−' if neg else '') + (s.replace('.', ',') if lang == 'fr' else s)


def dd(h):
    """(fr, en) label."""
    return d(h, 'fr'), d(h, 'en')


def answers(h):
    return list(dict.fromkeys([d(h, 'fr'), d(h, 'en')]))


def _expr(fmt, *vals):
    """fmt with {} slots filled by hundredths values, as an (fr, en) label."""
    return fmt.format(*[d(v, 'fr') for v in vals]), fmt.format(*[d(v, 'en') for v in vals])


def _tenths(lo, hi):
    """A value with exactly one decimal (non-zero tenth), in hundredths."""
    while True:
        v = random.randint(lo, hi) * 10
        if v % 100:
            return v


def _hundredths(lo, hi):
    while True:
        v = random.randint(lo, hi)
        if v % 10:
            return v


def g4_decimal_equivalences_gen(level='easy'):
    """Equivalences with + and − on decimals (QC-079)."""
    pick = (lambda: _tenths(5, 95)) if level != 'hard' else (lambda: _hundredths(105, 995))
    kind = random.choice({'easy': ['inverse', 'commute'], 'medium': ['inverse', 'compensate', 'which'],
                          'hard': ['compensate', 'which', 'associate']}[level])
    a, b = pick(), pick()
    s = a + b
    if kind == 'inverse':
        f = _expr('{} + {} = {}', a, b, s)
        return typed((f'On sait que **{f[0]}**. Sans calculer, combien fait **{d(s, "fr")} − {d(b, "fr")}** ?',
                      f'We know that **{f[1]}**. Without calculating, what is **{d(s, "en")} − {d(b, "en")}**?'),
                     answers(a), 'decimal',
                     ('L’addition et la soustraction se défont l’une l’autre.', 'Addition and subtraction undo each other.'),
                     (f'{d(a, "fr")} + {d(b, "fr")} = {d(s, "fr")}, donc {d(s, "fr")} − {d(b, "fr")} = {d(a, "fr")}.',
                      f'{d(a, "en")} + {d(b, "en")} = {d(s, "en")}, so {d(s, "en")} − {d(b, "en")} = {d(a, "en")}.'))
    if kind == 'commute':
        return typed((f'Complète : **{d(a, "fr")} + {d(b, "fr")} = {d(b, "fr")} + ?**', f'Fill in: **{d(a, "en")} + {d(b, "en")} = {d(b, "en")} + ?**'),
                     answers(a), 'decimal',
                     ('On peut additionner dans n’importe quel ordre.', 'You can add in any order.'),
                     (f'L’addition est commutative : {d(a, "fr")} + {d(b, "fr")} = {d(b, "fr")} + {d(a, "fr")}.',
                      f'Addition is commutative: {d(a, "en")} + {d(b, "en")} = {d(b, "en")} + {d(a, "en")}.'))
    if kind == 'compensate':
        r = (a // 100 + 1) * 100                      # round a up to the next whole number
        give = r - a
        if give >= b:
            a, b = b, a
            r = (a // 100 + 1) * 100
            give = r - a
        if give >= b:                                 # both too small to round: start again
            return g4_decimal_equivalences_gen(level)
        miss = b - give
        return typed((f'Complète pour que l’égalité soit vraie : **{d(a, "fr")} + {d(b, "fr")} = {d(r, "fr")} + ?**',
                      f'Fill in so the equality is true: **{d(a, "en")} + {d(b, "en")} = {d(r, "en")} + ?**'),
                     answers(miss), 'decimal',
                     (f'{d(a, "fr")} a reçu {d(give, "fr")} pour devenir {d(r, "fr")} : l’autre nombre doit perdre autant.',
                      f'{d(a, "en")} got {d(give, "en")} to become {d(r, "en")}: the other number must lose the same amount.'),
                     ([f'{d(a, "fr")} + {d(give, "fr")} = {d(r, "fr")}', f'{d(b, "fr")} − {d(give, "fr")} = {d(miss, "fr")}'],
                      [f'{d(a, "en")} + {d(give, "en")} = {d(r, "en")}', f'{d(b, "en")} − {d(give, "en")} = {d(miss, "en")}']))
    if kind == 'associate':
        c = 100 - (b % 100) if b % 100 else 50        # c completes b to a whole number
        total = a + b + c
        return typed((f'Calcule astucieusement : **{d(a, "fr")} + {d(b, "fr")} + {d(c, "fr")}**',
                      f'Calculate cleverly: **{d(a, "en")} + {d(b, "en")} + {d(c, "en")}**'),
                     answers(total), 'decimal',
                     ('Regroupe d’abord les deux nombres qui font un nombre entier.', 'First group the two numbers that make a whole number.'),
                     ([f'{d(b, "fr")} + {d(c, "fr")} = {d(b + c, "fr")}', f'{d(a, "fr")} + {d(b + c, "fr")} = {d(total, "fr")}'],
                      [f'{d(b, "en")} + {d(c, "en")} = {d(b + c, "en")}', f'{d(a, "en")} + {d(b + c, "en")} = {d(total, "en")}']))
    # which: pick the expression equal to a + b
    k = random.choice([10, 20, 50, 100])
    options = [_expr('{} + {}', b, a), _expr('{} − {}', s + k, k)]
    if b > k:
        options.append(_expr('{} + {}', a + k, b - k))
    elif a > k:
        options.append(_expr('{} + {}', a - k, b + k))
    right = random.choice(options)
    wrong = [(_expr('{} + {}', a + k, b + k), 'both_up', 'Adding to both numbers changes the sum.', 'Ajouter aux deux nombres change la somme.'),
             (_expr('{} − {}', max(a, b), min(a, b)), 'wrong_op', 'Keep the same total.', 'Garde le même total.'),
             (_expr('{} + {}', s, k), 'extra', 'That is more than the sum.', 'C’est plus que la somme.'),
             (_expr('{} − {}', s - k, k) if s > 2 * k else _expr('{} + {}', s, 2 * k), 'off', 'Work out the expression.', 'Calcule l’expression.')]
    return mc((f'Quelle expression est égale à **{d(a, "fr")} + {d(b, "fr")}** ?', f'Which expression is equal to **{d(a, "en")} + {d(b, "en")}**?'),
              right, wrong,
              ('Calcule la valeur de chaque expression, ou cherche ce qu’on a ajouté et enlevé.', 'Work out each expression, or look at what was added and taken away.'),
              ([f'{d(a, "fr")} + {d(b, "fr")} = {d(s, "fr")}', f'{right[0]} = {d(s, "fr")}'], [f'{d(a, "en")} + {d(b, "en")} = {d(s, "en")}', f'{right[1]} = {d(s, "en")}']),
              pad=lambda: _expr('{} + {}', a + random.choice([10, 20, 30, 100]), b))


def g5_decimal_properties_gen(level='easy'):
    """Equivalences with the four operations on decimals (QC-080)."""
    kind = random.choice({'easy': ['mult_div', 'commute_x'], 'medium': ['mult_div', 'distribute', 'halve'],
                          'hard': ['distribute', 'halve', 'which']}[level])
    if kind == 'mult_div':
        a = _tenths(2, 95)
        n = random.randint(3, 9)
        p = a * n
        return typed((f'On sait que **{d(a, "fr")} × {n} = {d(p, "fr")}**. Sans calculer, combien fait **{d(p, "fr")} ÷ {n}** ?',
                      f'We know that **{d(a, "en")} × {n} = {d(p, "en")}**. Without calculating, what is **{d(p, "en")} ÷ {n}**?'),
                     answers(a), 'decimal',
                     ('La division défait la multiplication.', 'Division undoes multiplication.'),
                     (f'{d(a, "fr")} × {n} = {d(p, "fr")}, donc {d(p, "fr")} ÷ {n} = {d(a, "fr")}.', f'{d(a, "en")} × {n} = {d(p, "en")}, so {d(p, "en")} ÷ {n} = {d(a, "en")}.'))
    if kind == 'commute_x':
        a = _tenths(2, 95)
        n = random.randint(2, 9)
        return typed((f'Complète : **{d(a, "fr")} × {n} = {n} × ?**', f'Fill in: **{d(a, "en")} × {n} = {n} × ?**'),
                     answers(a), 'decimal',
                     ('On peut multiplier dans n’importe quel ordre.', 'You can multiply in any order.'),
                     (f'La multiplication est commutative : {d(a, "fr")} × {n} = {n} × {d(a, "fr")}.', f'Multiplication is commutative: {d(a, "en")} × {n} = {n} × {d(a, "en")}.'))
    if kind == 'distribute':
        n = random.randint(3, 9)
        w = random.randint(2, 12)
        f = _tenths(1, 9) if level != 'hard' else _hundredths(1, 99)
        a = w * 100 + f
        p = n * a
        if random.random() < 0.5:
            return typed((f'Complète : **{n} × {d(a, "fr")} = {n} × {w} + {n} × ?**', f'Fill in: **{n} × {d(a, "en")} = {n} × {w} + {n} × ?**'),
                         answers(f), 'decimal',
                         (f'Sépare {d(a, "fr")} en partie entière et partie décimale.', f'Split {d(a, "en")} into its whole part and its decimal part.'),
                         (f'{d(a, "fr")} = {w} + {d(f, "fr")}, donc {n} × {d(a, "fr")} = {n} × {w} + {n} × {d(f, "fr")}.',
                          f'{d(a, "en")} = {w} + {d(f, "en")}, so {n} × {d(a, "en")} = {n} × {w} + {n} × {d(f, "en")}.'))
        return typed((f'Calcule en séparant le nombre décimal : **{n} × {d(a, "fr")}**', f'Calculate by splitting the decimal: **{n} × {d(a, "en")}**'),
                     answers(p), 'decimal',
                     (f'{n} × {w}, puis {n} × {d(f, "fr")}, puis additionne.', f'{n} × {w}, then {n} × {d(f, "en")}, then add.'),
                     ([f'{n} × {w} = {n * w}', f'{n} × {d(f, "fr")} = {d(n * f, "fr")}', f'{n * w} + {d(n * f, "fr")} = {d(p, "fr")}'],
                      [f'{n} × {w} = {n * w}', f'{n} × {d(f, "en")} = {d(n * f, "en")}', f'{n * w} + {d(n * f, "en")} = {d(p, "en")}']))
    if kind == 'halve':
        a = random.choice([x for x in range(4, 60, 2)]) * 100
        k = random.choice([50, 25])
        p = a * k // 100
        what = '÷ 2' if k == 50 else '÷ 4'
        return typed((f'Multiplier par **{d(k, "fr")}**, c’est diviser par {2 if k == 50 else 4}. Calcule **{d(a, "fr")} × {d(k, "fr")}**.',
                      f'Multiplying by **{d(k, "en")}** is the same as dividing by {2 if k == 50 else 4}. Calculate **{d(a, "en")} × {d(k, "en")}**.'),
                     answers(p), 'decimal',
                     (f'{d(k, "fr")} = {"la moitié" if k == 50 else "le quart"} de 1.', f'{d(k, "en")} is {"half" if k == 50 else "a quarter"} of 1.'),
                     (f'{d(a, "fr")} × {d(k, "fr")} = {d(a, "fr")} {what} = {d(p, "fr")}', f'{d(a, "en")} × {d(k, "en")} = {d(a, "en")} {what} = {d(p, "en")}'))
    n = random.randint(3, 9)
    w = random.randint(2, 9)
    f = _tenths(1, 9)
    a = w * 100 + f
    right = _expr(f'{n} × {{}} + {n} × {{}}', w * 100, f)
    wrong = [(_expr(f'{n} × {{}} + {{}}', w * 100, f), 'forgot', 'Both parts must be multiplied.', 'Il faut multiplier les deux parties.'),
             (_expr(f'{n} + {{}} × {{}}', w * 100, f), 'order', 'Multiply each part by the same number.', 'Multiplie chaque partie par le même nombre.'),
             (_expr(f'{n} × {{}} × {{}}', w * 100, f), 'times', 'The parts are added, not multiplied.', 'Les parties s’additionnent, elles ne se multiplient pas.'),
             (_expr(f'{n + 1} × {{}}', a), 'factor', 'The factor changed.', 'Le facteur a changé.')]
    return mc((f'Quelle expression est égale à **{n} × {d(a, "fr")}** ?', f'Which expression is equal to **{n} × {d(a, "en")}**?'),
              right, wrong,
              ('Distributivité : multiplie chaque partie du nombre, puis additionne.', 'Distributive property: multiply each part of the number, then add.'),
              ([f'{d(a, "fr")} = {w} + {d(f, "fr")}', f'{n} × {d(a, "fr")} = {right[0]} = {d(n * a, "fr")}'],
               [f'{d(a, "en")} = {w} + {d(f, "en")}', f'{n} × {d(a, "en")} = {right[1]} = {d(n * a, "en")}']))
