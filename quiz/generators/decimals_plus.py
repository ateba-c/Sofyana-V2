"""
decimals_plus.py — WP3 of the curriculum upgrade (docs/curriculum/PLAN.md §4).

  g4_decimal_grid_gen          G4  10×10 grid / tenth strip / money ↔ decimal (041, 042)
  g4_decimal_equivalence_gen   G4  0,5 = 0,50 · 12 dixièmes = 1,2 (044, 046)
  g4_decimal_number_line_gen   G4  decimals between two whole numbers (047)
  g6_decimal_number_line_gen   G6  decimals between two decimals (048)
  g4_round_decimal_gen         G4  round / truncate (050)
  g5_times_power_of_ten_gen    G5  × and ÷ by 10, 100, 1000 (122)
  g5_estimate_decimal_gen      G5  estimate sums, products, quotients (118, 119)
  g5_decimal_story_gen         G5  +, −, ×, ÷ stories with decimals (075–078)
  g6_percent_gen               G6  fraction ↔ decimal ↔ percentage (034, 053, 127–129, 131)
  g6_choose_notation_gen       G6  which notation suits the context (130)
  fraction_to_decimal_gen      G3/4 rewrite: tenths AND hundredths (052)

All decimals are built from integers (value = k / 10**p) so nothing is ever a
float rounding artefact. French labels use a decimal comma, English a point.
"""
import random
from fractions import Fraction

from quiz import illustrations as ill
from .kit import mc, typed, match, frac
from . import scenarios as sc


def D(k, p):
    """k / 10**p as (fr, en) strings with exactly p decimals (p = 0 → integer)."""
    neg = k < 0
    k = abs(k)
    s = str(k) if p == 0 else f'{k // 10 ** p}.{k % 10 ** p:0{p}d}'
    s = ('-' if neg else '') + s
    return s.replace('.', ','), s


def _pad(k, p, spread=9):
    """Plausible nearby decimal (never ≤ 0) for padding a choice list."""
    def pad():
        return D(max(1, k + random.choice([i for i in range(-spread, spread + 1) if i])), p)
    return pad


def Dfr(k, p):
    return D(k, p)[0]


def Dtrim(k, p):
    """Like D but without trailing zeros (0,50 → 0,5)."""
    while p > 0 and k % 10 == 0:
        k //= 10
        p -= 1
    return D(k, p)


# ── G4 · Decimal grid / money ────────────────────────────────────────────────

def g4_decimal_grid_gen(level='medium'):
    variant = 'tenths' if level == 'easy' else random.choice(['hundredths', 'hundredths', 'money'])
    if variant == 'tenths':
        k = random.randint(1, 9)
        shape = ill.hundred_grid(k, size=1, color=ill.TEAL)
        correct = D(k, 1)
        distr = [(D(k, 2), 'place', 'Each part is one TENTH of the strip.', 'Chaque case est un DIXIÈME de la bande.'),
                 ((str(k), str(k)), 'whole', 'The whole strip is 1: the coloured part is less than 1.', 'La bande entière vaut 1 : la partie coloriée est plus petite que 1.'),
                 (D(10 - k, 1), 'complement', 'Count the coloured parts, not the white ones.', 'Compte les cases coloriées, pas les blanches.'),
                 (D(k + 1, 1) if k < 9 else D(k - 2, 1), 'miscount', 'Count the coloured parts again.', 'Recompte les cases coloriées.')]
        return mc(('La bande entière vaut 1. Quel nombre décimal représente la partie coloriée ?',
                   'The whole strip is 1. Which decimal number shows the coloured part?'),
                  correct, distr,
                  ('La bande a 10 cases : chaque case vaut 0,1.', 'The strip has 10 parts: each part is 0.1.'),
                  ([f'{k} cases sur 10 = {k}/10 = {correct[0]}'], [f'{k} parts out of 10 = {k}/10 = {correct[1]}']),
                  shape=shape, pad=_pad(k, 1, 4))
    if variant == 'hundredths':
        k = random.randint(1, 99)
        if k % 10 == 0:
            k += random.randint(1, 9) if k < 90 else -3
        shape = ill.hundred_grid(k, color=ill.BLUE)
        correct = D(k, 2)
        rev = int(str(k).zfill(2)[::-1])
        distr = [(D(k, 1) if k < 100 and k // 10 else D(k, 3), 'place', 'Each small square is one HUNDREDTH.', 'Chaque petit carré est un CENTIÈME.'),
                 ((str(k), str(k)), 'whole', 'The whole grid is 1.', 'Le quadrillage entier vaut 1.'),
                 (D(100 - k, 2), 'complement', 'Count the coloured squares, not the white ones.', 'Compte les carrés coloriés, pas les blancs.'),
                 (D(rev, 2) if rev != k else D(k + 10, 2), 'swapped', 'Tenths = full rows, hundredths = the extra squares.', 'Dixièmes = lignes complètes, centièmes = les carrés en plus.'),
                 (D(k, 3), 'place', 'Each small square is one HUNDREDTH.', 'Chaque petit carré est un CENTIÈME.')]
        return mc(('Le quadrillage entier vaut 1. Quel nombre décimal représente la partie coloriée ?',
                   'The whole grid is 1. Which decimal number shows the coloured part?'),
                  correct, distr,
                  ('Une ligne = 0,1 (un dixième) ; un petit carré = 0,01 (un centième).', 'One row = 0.1 (a tenth); one small square = 0.01 (a hundredth).'),
                  ([f'{k // 10} lignes = {k // 10} dixièmes, {k % 10} carrés = {k % 10} centièmes', f'= {correct[0]}'],
                   [f'{k // 10} rows = {k // 10} tenths, {k % 10} squares = {k % 10} hundredths', f'= {correct[1]}']),
                  shape=shape, pad=_pad(k, 2))
    dollars = random.randint(1, 20)
    cents = random.choice([5, 10, 25, 35, 50, 75, 90, 95, random.randint(1, 99)])
    k = dollars * 100 + cents
    return typed((f'Écris en nombre décimal : **{dollars} $ et {cents} ¢**', f'Write as a decimal number: **${dollars} and {cents}¢**'),
                 [Dfr(k, 2), D(k, 2)[1], Dtrim(k, 2)[0]], 'money',
                 ('100 ¢ = 1 $ : les cents sont des centièmes de dollar.', '100¢ = $1: cents are hundredths of a dollar.'),
                 ([f'{cents} ¢ = {D(cents, 2)[0]} $', f'{dollars} + {D(cents, 2)[0]} = {Dfr(k, 2)} $'],
                  [f'{cents}¢ = ${D(cents, 2)[1]}', f'{dollars} + {D(cents, 2)[1]} = ${D(k, 2)[1]}']))


# ── G4 · Equivalent decimal writings ─────────────────────────────────────────

def _equiv_pair():
    kind = random.choice(['zeros', 'tenths', 'hundredths', 'mixed'])
    if kind == 'zeros':
        k = random.randint(1, 9)
        w = random.randint(0, 9)
        return (Dfr(w * 10 + k, 1), D(w * 10 + k, 1)[1]), (Dfr(w * 100 + k * 10, 2), D(w * 100 + k * 10, 2)[1])
    if kind == 'tenths':
        t = random.randint(11, 49)
        return (f'{t} dixièmes', f'{t} tenths'), D(t, 1)
    if kind == 'hundredths':
        h = random.randint(101, 499)
        return (f'{h} centièmes', f'{h} hundredths'), D(h, 2)
    u, t, h = random.randint(1, 9), random.randint(0, 9), random.randint(1, 9)
    return (f'{u} unités {h} centièmes' if t == 0 else f'{u} unités {t} dixièmes {h} centièmes',
            f'{u} ones {h} hundredths' if t == 0 else f'{u} ones {t} tenths {h} hundredths'), D(u * 100 + t * 10 + h, 2)


def g4_decimal_equivalence_gen(level='medium'):
    if level == 'easy' or random.random() < 0.4:
        k = random.randint(1, 9)
        w = random.randint(0, 9)
        target = D(w * 10 + k, 1)
        correct = D(w * 100 + k * 10, 2)
        distr = [(D(w * 100 + k, 2), 'zero_inside', f'A zero in the tenths place changes the value: {D(w * 100 + k, 2)[1]} ≠ {target[1]}.', f'Un zéro aux dixièmes change la valeur : {D(w * 100 + k, 2)[0]} ≠ {target[0]}.'),
                 (D(w * 1000 + k, 3), 'zero_inside', 'Only zeros added at the END keep the value.', 'Seuls les zéros ajoutés à la FIN gardent la valeur.'),
                 (D(k * 10 + w, 1) if k != w else D(w * 10 + k + 1, 1), 'swapped', 'Keep each digit in its place.', 'Garde chaque chiffre à sa place.'),
                 ((f'{w}{k}', f'{w}{k}') if w else (f'{k}', f'{k}'), 'no_point', 'Removing the decimal point changes the value.', 'Enlever la virgule change la valeur.'),
                 (D(w * 10 + k, 2), 'shift', 'Compare tenths with tenths.', 'Compare les dixièmes avec les dixièmes.')]
        return mc((f'Quel nombre est égal à **{target[0]}** ?', f'Which number is equal to **{target[1]}**?'),
                  correct, distr,
                  ('Ajouter un zéro à la fin de la partie décimale ne change pas la valeur.', 'Adding a zero at the end of the decimal part does not change the value.'),
                  ([f'{target[0]} = {correct[0]} ({k} dixièmes = {k * 10} centièmes)'], [f'{target[1]} = {correct[1]} ({k} tenths = {k * 10} hundredths)']),
                  pad=_pad(w * 100 + k * 10, 2, 30))
    pairs, seen = [], set()
    while len(pairs) < (3 if level == 'medium' else 4):
        left, right = _equiv_pair()
        if right[0] in seen or left[0] in seen:
            continue
        seen.update({right[0], left[0]})
        pairs.append((left, right))
    return match(('Associe chaque écriture au nombre décimal égal.', 'Match each writing to the equal decimal number.'),
                 pairs,
                 ('10 dixièmes = 1 unité ; 10 centièmes = 1 dixième.', '10 tenths = 1 one; 10 hundredths = 1 tenth.'),
                 ([f'{l[0]} = {r[0]}' for l, r in pairs], [f'{l[1]} = {r[1]}' for l, r in pairs]))


# ── G4 / G6 · Decimals on a number line ──────────────────────────────────────

def g4_decimal_number_line_gen(level='medium'):
    a = random.randint(0, 9)
    t = random.randint(1, 9)
    k = a * 10 + t
    if level == 'hard':
        shape = ill.number_line([D(a, 0), D(a + 1, 0)], minor=10, point=t)
    elif level == 'medium':
        shape = ill.number_line([D(a, 0), D(a + 1, 0), D(a + 2, 0)], minor=10, point=t)
    else:
        shape = ill.number_line([D(a, 0), D(a + 1, 0)], minor=10, point=t)
    correct = D(k, 1)
    distr = [(D(k + 1, 1) if t < 9 else D(k - 2, 1), 'miscount', 'Count the small ticks from the whole number again.', 'Recompte les petites graduations à partir de l’entier.'),
             (D(k - 1, 1) if t > 1 else D(k + 2, 1), 'miscount', 'Count the small ticks from the whole number again.', 'Recompte les petites graduations à partir de l’entier.'),
             (D(a * 100 + t, 2), 'place', 'Each small tick is one tenth (0.1).', 'Chaque petite graduation vaut un dixième (0,1).'),
             (D((a + 1) * 10 - t, 1) if 10 - t != t else D(k + 3, 1), 'from_right', 'Count from the left whole number.', 'Compte à partir de l’entier de gauche.'),
             ((str(t), str(t)), 'whole', f'The point is between {a} and {a + 1}.', f'Le point est entre {a} et {a + 1}.')]
    return mc(('Quel nombre décimal se trouve au point « ? » ?', 'Which decimal number is at the “?” point?'),
              correct, distr,
              ('L’unité est partagée en 10 : chaque petite graduation vaut 0,1.', 'Each unit is split into 10: each small tick is 0.1.'),
              ([f'{a} + {t} × 0,1 = {correct[0]}'], [f'{a} + {t} × 0.1 = {correct[1]}']),
              shape=shape, pad=_pad(k, 1, 4))


def g6_decimal_number_line_gen(level='medium'):
    if level == 'easy':
        start = random.randint(1, 98)            # in tenths: e.g. 23 → 2,3
        h = random.randint(1, 9)
        shape = ill.number_line([D(start, 1), D(start + 1, 1)], minor=10, point=h)
        k, p = start * 10 + h, 2
        step = ('0,01', '0.01')
    else:
        start = random.randint(10, 989)          # in hundredths: 2,35
        h = random.randint(1, 9)
        if level == 'medium':
            shape = ill.number_line([D(start, 2), D(start + 1, 2)], minor=10, point=h)
            k, p = start * 10 + h, 3
            step = ('0,001', '0.001')
        else:
            start = random.randint(1, 98)
            h = random.randint(1, 19)
            shape = ill.number_line([D(start, 1), D(start + 1, 1), D(start + 2, 1)], minor=10, point=h)
            k, p = start * 10 + h, 2
            step = ('0,01', '0.01')
    correct = D(k, p)
    distr = [(D(k + 1, p), 'miscount', 'Count the small ticks again.', 'Recompte les petites graduations.'),
             (D(k - 1, p), 'miscount', 'Count the small ticks again.', 'Recompte les petites graduations.'),
             (D(k, p + 1) if p < 3 else D(k * 10 + 1, p + 1), 'place', f'Each small tick is {step[1]}.', f'Chaque petite graduation vaut {step[0]}.'),
             (D(k // 10 * 10 + 10 - (k % 10), p) if k % 10 != 5 else D(k + 2, p), 'from_right', 'Count from the left mark.', 'Compte à partir du repère de gauche.'),
             (D(k + 10, p), 'big_step', 'A small tick is ten times smaller than the gap between labels.', 'Une petite graduation est dix fois plus petite que l’écart entre les nombres écrits.')]
    return mc(('Quel nombre décimal se trouve au point « ? » ?', 'Which decimal number is at the “?” point?'),
              correct, distr,
              (f'Entre deux nombres écrits, il y a 10 petites graduations : chacune vaut {step[0]}.',
               f'Between two labelled numbers there are 10 small ticks: each is {step[1]}.'),
              ([f'Chaque graduation vaut {step[0]}', f'Réponse : {correct[0]}'], [f'Each tick is {step[1]}', f'Answer: {correct[1]}']),
              shape=shape, pad=_pad(k, p, 5))


# ── G4 · Rounding & truncating ───────────────────────────────────────────────

_PLACE = {0: ("à l'unité près", 'to the nearest whole number'), 1: ('au dixième près', 'to the nearest tenth'),
          2: ('au centième près', 'to the nearest hundredth')}


def g4_round_decimal_gen(level='medium'):
    if level == 'easy':
        p, to = 1, 0
    elif level == 'medium':
        p, to = 2, random.choice([0, 1])
    else:
        p, to = 3, random.choice([1, 2])
    k = random.randint(10 ** p, 99 * 10 ** p)
    if k % 10 == 0:
        k += random.randint(1, 9)
    truncate = level == 'hard' and random.random() < 0.3
    f = 10 ** (p - to)
    down = k // f
    up = down + 1
    res = down if truncate or (k % f) * 2 < f else up
    verb = ('Tronque', 'Truncate') if truncate else ('Arrondis', 'Round')
    ans = D(res, to)
    return typed((f'{verb[0]} **{Dfr(k, p)}** {_PLACE[to][0]}.', f'{verb[1]} **{D(k, p)[1]}** {_PLACE[to][1]}.'),
                 [ans[0], ans[1]], 'decimal',
                 (('Tronquer : on coupe simplement les chiffres après la position demandée.', 'Truncate: just cut off the digits after that place.') if truncate else
                  ('Regarde le chiffre juste à droite de la position : 5 ou plus → on arrondit vers le haut.', 'Look at the digit just to the right: 5 or more → round up.')),
                 ([f'{Dfr(k, p)} est entre {Dfr(down, to)} et {Dfr(up, to)}', f'→ {ans[0]}'],
                  [f'{D(k, p)[1]} is between {D(down, to)[1]} and {D(up, to)[1]}', f'→ {ans[1]}']))


# ── G5 · × and ÷ by 10, 100, 1000 ────────────────────────────────────────────

def g5_times_power_of_ten_gen(level='medium'):
    e = random.choice([1, 2]) if level == 'easy' else random.choice([1, 2, 3])
    p = random.choice([1, 2]) if level != 'hard' else random.choice([1, 2, 3])
    k = random.randint(10 ** p + 1, 99 * 10 ** p)
    if k % 10 == 0:
        k += 3
    times = random.random() < (0.6 if level == 'easy' else 0.5)
    factor = 10 ** e
    if not times and p + e > 3:          # results stay within thousandths (primary limit)
        p = 3 - e
        k = random.randint(10 ** p + 1, 99 * 10 ** p) if p else random.randint(12, 999)
        if k % 10 == 0:
            k += 3
    if times:
        res_k, res_p = k * factor, p
        op = '×'
    else:
        res_k, res_p = k, p + e
        op = '÷'
    ans = Dtrim(res_k, res_p)
    return typed((f'Calcule : **{Dfr(k, p)} {op} {factor}**', f'Calculate: **{D(k, p)[1]} {op} {factor}**'),
                 [ans[0], ans[1]], 'decimal',
                 ((f'× {factor} : chaque chiffre prend une valeur {factor} fois plus grande (la virgule « recule » de {e} rang{"s" if e > 1 else ""}).',
                   f'× {factor}: every digit becomes {factor} times bigger (the point moves {e} place{"s" if e > 1 else ""} right).') if times else
                  (f'÷ {factor} : chaque chiffre prend une valeur {factor} fois plus petite (la virgule avance de {e} rang{"s" if e > 1 else ""} vers la gauche).',
                   f'÷ {factor}: every digit becomes {factor} times smaller (the point moves {e} place{"s" if e > 1 else ""} left).')),
                 ([f'{Dfr(k, p)} {op} {factor} = {ans[0]}'], [f'{D(k, p)[1]} {op} {factor} = {ans[1]}']))


# ── G5 · Estimate decimal results ────────────────────────────────────────────

def g5_estimate_decimal_gen(level='medium'):
    ops = ['+', '−'] if level == 'easy' else ['+', '−', '×'] if level == 'medium' else ['×', '÷', '+']
    op = random.choice(ops)
    if op in '+−':
        a, b = random.randint(110, 980), random.randint(110, 980)      # hundredths: 1,10 … 9,80
        if op == '−' and a < b:
            a, b = b, a
        ra, rb = round(a / 100), round(b / 100)
        est = ra + rb if op == '+' else ra - rb
        if est <= 0:
            a, ra, est = a + 300, round((a + 300) / 100), round((a + 300) / 100) - rb
        prompt_nums = (Dfr(a, 2), Dfr(b, 2), D(a, 2)[1], D(b, 2)[1])
    elif op == '×':
        a, b = random.randint(15, 99), random.randint(2, 9)            # a in tenths: 1,5 … 9,9 × whole
        ra, rb = round(a / 10), b
        est = ra * rb
        prompt_nums = (Dfr(a, 1), str(b), D(a, 1)[1], str(b))
    else:
        q, b = random.randint(2, 12), random.randint(2, 9)
        a = q * b * 10 + random.choice([-3, -2, 2, 3])                  # tenths, close to a multiple of b
        ra, rb = round(a / 10), b
        est = round(ra / rb)
        prompt_nums = (Dfr(a, 1), str(b), D(a, 1)[1], str(b))
    distr = [(str(est * 10), 'decimal_place', 'Check where the decimal point goes: is that a sensible size?', 'Vérifie la place de la virgule : est-ce une grandeur raisonnable ?'),
             (Dfr(est, 1), 'decimal_place', 'Check where the decimal point goes: is that a sensible size?', 'Vérifie la place de la virgule : est-ce une grandeur raisonnable ?'),
             (str(est + 2), 'far', 'Round each number to the nearest whole first.', 'Arrondis d’abord chaque nombre à l’unité.'),
             (str(max(1, est - 2)) if est > 2 else str(est + 3), 'far', 'Round each number to the nearest whole first.', 'Arrondis d’abord chaque nombre à l’unité.'),
             (str(est + 1), 'close', 'Round to the NEAREST whole number.', 'Arrondis à l’unité la PLUS PROCHE.')]
    return mc((f'Sans calculer exactement, quelle est la meilleure **estimation** de **{prompt_nums[0]} {op} {prompt_nums[1]}** ?',
               f'Without calculating exactly, what is the best **estimate** of **{prompt_nums[2]} {op} {prompt_nums[3]}**?'),
              str(est), distr,
              ('Arrondis chaque nombre décimal à l’unité, puis calcule mentalement.', 'Round each decimal to the nearest whole number, then calculate mentally.'),
              ([f'{prompt_nums[0]} ≈ {ra}', f'{prompt_nums[1]} ≈ {rb}', f'{ra} {op} {rb} ≈ {est}'],
               [f'{prompt_nums[2]} ≈ {ra}', f'{prompt_nums[3]} ≈ {rb}', f'{ra} {op} {rb} ≈ {est}']),
              pad=lambda: str(max(1, est + random.choice([-4, -3, 3, 4, 5]))))


# ── G5 · Decimal word problems ───────────────────────────────────────────────

_ITEMS = [('un cahier', 'a notebook'), ('un jus', 'a juice'), ('une règle', 'a ruler'), ('un crayon', 'a pencil'),
          ('une gomme', 'an eraser'), ('un muffin', 'a muffin')]


def g5_decimal_story_gen(level='medium'):
    who, g = random.choice(sc.ACTORS)
    il = sc.pronoun_fr(g).capitalize()
    he = sc.pronoun_en(g).capitalize()
    kind = random.choice(['total', 'change', 'compare'] if level == 'easy' else ['total', 'change', 'unit', 'many', 'compare'])
    if kind == 'total':
        (i1, i2) = random.sample(_ITEMS, 2)
        a, b = random.randint(105, 899), random.randint(105, 899)
        return typed((f'{who} achète {i1[0]} à **{Dfr(a, 2)} $** et {i2[0]} à **{Dfr(b, 2)} $**. Combien paie-t-{"elle" if g == "f" else "il"} en tout ?',
                      f'{who} buys {i1[1]} for **${D(a, 2)[1]}** and {i2[1]} for **${D(b, 2)[1]}**. How much does {sc.pronoun_en(g)} pay in all?'),
                     [Dfr(a + b, 2), D(a + b, 2)[1]], 'money',
                     ('Additionne en alignant les virgules.', 'Add with the decimal points lined up.'),
                     ([f'{Dfr(a, 2)} + {Dfr(b, 2)} = {Dfr(a + b, 2)} $'], [f'{D(a, 2)[1]} + {D(b, 2)[1]} = ${D(a + b, 2)[1]}']))
    if kind == 'change':
        bill = random.choice([500, 1000, 2000])
        a = random.randint(105, bill - 55)
        return typed((f'{who} paie un article de **{Dfr(a, 2)} $** avec un billet de **{bill // 100} $**. Combien d’argent lui rend-on ?',
                      f'{who} pays for an item costing **${D(a, 2)[1]}** with a **${bill // 100}** bill. How much change does {sc.pronoun_en(g)} get?'),
                     [Dfr(bill - a, 2), D(bill - a, 2)[1]], 'money',
                     ('Monnaie = billet − prix.', 'Change = bill − price.'),
                     ([f'{bill // 100},00 − {Dfr(a, 2)} = {Dfr(bill - a, 2)} $'], [f'{bill // 100}.00 − {D(a, 2)[1]} = ${D(bill - a, 2)[1]}']))
    if kind == 'unit':
        n = random.randint(2, 9)
        unit = random.randint(35, 650)
        total = unit * n
        return typed((f'{who} paie **{Dfr(total, 2)} $** pour **{n}** muffins identiques. Combien coûte un muffin ?',
                      f'{who} pays **${D(total, 2)[1]}** for **{n}** identical muffins. How much does one muffin cost?'),
                     [Dfr(unit, 2), D(unit, 2)[1]], 'money',
                     (f'Partage le total en {n} parts égales.', f'Split the total into {n} equal parts.'),
                     ([f'{Dfr(total, 2)} ÷ {n} = {Dfr(unit, 2)} $'], [f'{D(total, 2)[1]} ÷ {n} = ${D(unit, 2)[1]}']))
    if kind == 'many':
        n = random.randint(3, 9)
        l = random.randint(12, 95)                 # tenths of a metre
        return typed((f'{who} coupe **{n}** morceaux de ruban de **{Dfr(l, 1)} m** chacun. Quelle longueur de ruban utilise-t-{"elle" if g == "f" else "il"} ?',
                      f'{who} cuts **{n}** pieces of ribbon, each **{D(l, 1)[1]} m** long. What length of ribbon does {sc.pronoun_en(g)} use?'),
                     [Dtrim(l * n, 1)[0], Dtrim(l * n, 1)[1]], 'decimal',
                     ('Multiplie comme avec des nombres entiers, puis place la virgule.', 'Multiply as with whole numbers, then place the decimal point.'),
                     ([f'{n} × {Dfr(l, 1)} = {Dtrim(l * n, 1)[0]} m'], [f'{n} × {D(l, 1)[1]} = {Dtrim(l * n, 1)[1]} m']))
    a, b = random.randint(120, 480), random.randint(120, 480)
    if a == b:
        b += 7
    other = random.choice([n for n, _ in sc.ACTORS if n != who])
    hi_, lo_ = max(a, b), min(a, b)
    return typed((f'{who} saute **{Dfr(a, 2)} m** et {other} saute **{Dfr(b, 2)} m**. Quelle est la différence entre les deux sauts ?',
                  f'{who} jumps **{D(a, 2)[1]} m** and {other} jumps **{D(b, 2)[1]} m**. What is the difference between the two jumps?'),
                 [Dtrim(hi_ - lo_, 2)[0], Dtrim(hi_ - lo_, 2)[1]], 'decimal',
                 ('Différence = le plus grand − le plus petit.', 'Difference = larger − smaller.'),
                 ([f'{Dfr(hi_, 2)} − {Dfr(lo_, 2)} = {Dtrim(hi_ - lo_, 2)[0]} m'], [f'{D(hi_, 2)[1]} − {D(lo_, 2)[1]} = {Dtrim(hi_ - lo_, 2)[1]} m']))


# ── G6 · Percentages ─────────────────────────────────────────────────────────

_NICE = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10), (9, 10), (1, 20), (1, 25)]


def g6_percent_gen(level='medium'):
    variant = random.choice(['grid', 'from_frac', 'from_dec'] if level == 'easy'
                            else ['from_frac', 'from_dec', 'to_dec', 'to_frac', 'grid'] if level == 'medium'
                            else ['from_frac', 'to_frac', 'of', 'of'])
    if variant == 'grid':
        k = random.randint(1, 99)
        return typed(('Le quadrillage entier représente 100 %. Quel pourcentage est colorié ?', 'The whole grid is 100%. What percentage is coloured?'),
                     [f'{k} %', str(k)], 'integer',
                     ('Pour cent = sur cent : chaque petit carré vaut 1 %.', 'Per cent = out of a hundred: each small square is 1%.'),
                     ([f'{k} carrés sur 100 = {k} %'], [f'{k} squares out of 100 = {k}%']),
                     shape=ill.hundred_grid(k, color=ill.PURPLE))
    if variant in ('from_frac', 'to_frac'):
        n, d = random.choice(_NICE if level != 'easy' else [(1, 2), (1, 4), (3, 4), (1, 10), (7, 10)])
        pct = n * 100 // d
        if variant == 'from_frac':
            return typed((f'Écris **{frac(n, d)}** en pourcentage.', f'Write **{frac(n, d)}** as a percentage.'),
                         [f'{pct} %', str(pct)], 'integer',
                         (f'Trouve la fraction équivalente sur 100 : {frac(n, d)} = ?/100.', f'Find the equivalent fraction over 100: {frac(n, d)} = ?/100.'),
                         ([f'{frac(n, d)} = {frac(pct, 100)} = {pct} %'], [f'{frac(n, d)} = {frac(pct, 100)} = {pct}%']))
        distr = [(frac(pct, 10) if pct % 10 == 0 and frac(pct, 10) != frac(n, d) else frac(n + 1, d) if n + 1 < d else frac(n, d * 2), 'scale', 'Per cent means out of 100.', 'Pour cent veut dire sur 100.'),
                 (frac(1, pct) if pct > 1 else frac(1, 3), 'inverted', f'{pct}% = {pct}/100, then simplify.', f'{pct} % = {pct}/100, puis simplifie.'),
                 (frac(d - n, d) if d - n != n else frac(n, d + 1), 'complement', 'That is the part that is left.', 'C’est la partie qui reste.'),
                 (frac(n, d * 10), 'scale', 'Per cent means out of 100.', 'Pour cent veut dire sur 100.'),
                 (frac(pct, 1000), 'scale', 'Per cent means out of 100.', 'Pour cent veut dire sur 100.')]
        return mc((f'Quelle fraction est égale à **{pct} %** ?', f'Which fraction is equal to **{pct}%**?'),
                  frac(n, d), distr,
                  (f'{pct} % = {pct}/100 : simplifie cette fraction.', f'{pct}% = {pct}/100: simplify this fraction.'),
                  ([f'{pct} % = {frac(pct, 100)} = {frac(n, d)}'], [f'{pct}% = {frac(pct, 100)} = {frac(n, d)}']))
    if variant in ('from_dec', 'to_dec'):
        k = random.choice([random.randint(1, 99), random.choice([5, 25, 50, 75, 10, 20])])
        if variant == 'from_dec':
            return typed((f'Écris **{Dfr(k, 2)}** en pourcentage.', f'Write **{D(k, 2)[1]}** as a percentage.'),
                         [f'{k} %', str(k)], 'integer',
                         ('0,01 = 1 % : le nombre de centièmes donne le pourcentage.', '0.01 = 1%: the number of hundredths is the percentage.'),
                         ([f'{Dfr(k, 2)} = {k} centièmes = {k} %'], [f'{D(k, 2)[1]} = {k} hundredths = {k}%']))
        ans = Dtrim(k, 2)
        return typed((f'Écris **{k} %** en nombre décimal.', f'Write **{k}%** as a decimal number.'),
                     [ans[0], ans[1]], 'decimal',
                     (f'{k} % = {k} centièmes.', f'{k}% = {k} hundredths.'),
                     ([f'{k} % = {k}/100 = {ans[0]}'], [f'{k}% = {k}/100 = {ans[1]}']))
    pct = random.choice([10, 20, 25, 50, 75, 5])
    base = random.choice([b for b in range(20, 401, 20) if b * pct % 100 == 0])
    res = base * pct // 100
    return typed((f'Combien font **{pct} % de {base}** ?', f'What is **{pct}% of {base}**?'),
                 [res], 'integer',
                 (f'{pct} % = {frac(pct, 100)} : trouve cette fraction de {base}.', f'{pct}% = {frac(pct, 100)}: find that fraction of {base}.'),
                 ([f'1 % de {base} = {base} ÷ 100', f'{pct} % de {base} = {base} × {pct} ÷ 100 = {res}'],
                  [f'1% of {base} = {base} ÷ 100', f'{pct}% of {base} = {base} × {pct} ÷ 100 = {res}']))


# ── G6 · Choose the right notation ───────────────────────────────────────────

_CONTEXTS = [
    (('le prix d’un jus', 'the price of a juice'), 'dec'),
    (('la masse d’un colis', 'the mass of a parcel'), 'dec'),
    (('la taille d’un élève en mètres', 'a student’s height in metres'), 'dec'),
    (('la part d’une pizza mangée', 'the part of a pizza eaten'), 'frac'),
    (('la portion d’une recette (tasse)', 'a recipe amount (cup)'), 'frac'),
    (('le rabais dans un magasin', 'a discount in a shop'), 'pct'),
    (('la note d’un examen', 'an exam score'), 'pct'),
    (('la charge d’une batterie de téléphone', 'a phone battery level'), 'pct'),
]


def g6_choose_notation_gen(level='medium'):
    picks = {}
    for ctx, kind in random.sample(_CONTEXTS, len(_CONTEXTS)):
        picks.setdefault(kind, ctx)
    pairs = []
    for kind, ctx in picks.items():
        if kind == 'dec':
            if 'prix' in ctx[0]:
                k = random.randint(105, 950)
                val = (Dfr(k, 2) + ' $', '$' + D(k, 2)[1])
            elif 'masse' in ctx[0]:
                k = random.randint(105, 950)
                val = (Dfr(k, 2) + ' kg', D(k, 2)[1] + ' kg')
            else:
                k = random.randint(110, 175)
                val = (Dfr(k, 2) + ' m', D(k, 2)[1] + ' m')
        elif kind == 'frac':
            n, d = random.choice([(3, 8), (1, 4), (2, 3), (3, 4), (1, 3)])
            val = (frac(n, d), frac(n, d))
        else:
            p = random.choice([15, 20, 25, 30, 40, 75, 85, 90])
            val = (f'{p} %', f'{p}%')
        pairs.append((ctx, val))
    random.shuffle(pairs)
    return match(('Associe chaque situation à l’écriture la plus appropriée.', 'Match each situation with the most suitable way of writing the number.'),
                 pairs,
                 ('Argent et mesures → nombre décimal ; parts d’un tout partagé → fraction ; comparaison sur 100 → pourcentage.',
                  'Money and measures → decimal; parts of a shared whole → fraction; comparing out of 100 → percentage.'),
                 ([f'{c[0]} → {v[0]}' for c, v in pairs], [f'{c[1]} → {v[1]}' for c, v in pairs]))


# ── G3/G4 · Fraction → decimal (rewrite: tenths and hundredths) ─────────────

def fraction_to_decimal_gen(level='easy'):
    if level == 'easy':
        n, d = random.randint(1, 9), 10
    elif level == 'medium':
        n, d = random.choice([(random.randint(1, 9), 10), (random.randint(1, 99), 100), (random.randint(1, 9), 100)])
    else:
        n, d = random.choice([(random.randint(11, 29), 10), (random.randint(101, 299), 100), (1, 2), (1, 4), (3, 4), (2, 5), (3, 5)])
    f = Fraction(n, d)
    if 100 % f.denominator == 0:
        k100 = f.numerator * (100 // f.denominator)
    else:
        k100 = n * 100 // d
    correct = Dtrim(k100, 2)
    distr = [(D(n, 3) if d == 100 else D(n, 2), 'place', 'Tenths: 1 digit after the comma; hundredths: 2 digits.', 'Dixièmes : 1 chiffre après la virgule ; centièmes : 2 chiffres.'),
             (D(n, 1) if d == 100 and n < 100 and n % 10 else D(n * 10 + 1, 2), 'place', 'Tenths: 1 digit after the comma; hundredths: 2 digits.', 'Dixièmes : 1 chiffre après la virgule ; centièmes : 2 chiffres.'),
             ((f'{n},{d}', f'{n}.{d}'), 'concat', 'The fraction bar is not a decimal point.', 'La barre de fraction n’est pas une virgule.'),
             ((f'{d},{n}', f'{d}.{n}'), 'concat', 'The fraction bar is not a decimal point.', 'La barre de fraction n’est pas une virgule.'),
             (Dtrim(k100 + 10, 2), 'close', 'Check the tenths digit.', 'Vérifie le chiffre des dixièmes.')]
    return mc((f'La fraction **{frac(n, d)}** s’écrit aussi :', f'The fraction **{frac(n, d)}** can also be written as:'),
              correct, distr,
              ('Écris la fraction sur 10 ou sur 100, puis lis les dixièmes ou les centièmes.', 'Write the fraction over 10 or 100, then read the tenths or hundredths.'),
              ([f'{frac(n, d)} = {frac(k100, 100)} = {correct[0]}'], [f'{frac(n, d)} = {frac(k100, 100)} = {correct[1]}']),
              pad=_pad(k100, 2, 20))
