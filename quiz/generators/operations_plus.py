"""
operations_plus.py — WP4 of the curriculum upgrade (docs/curriculum/PLAN.md §4).

  g3_equality_true_gen         G3  which equality is true? (068, 069)
  g4_equivalent_expr_gen       G4  equivalent expressions (013)
  g4_properties_gen            G4  commutativity / associativity without computing (069, 070)
  g6_distributive_gen          G6  7 × 12 = 7 × 10 + 7 × 2 (071)
  g4_missing_factor_gen        G4  a × □ = c, □ ÷ b = c … (100)
  g4_division_remainder_gen    G4  quotient and remainder (099)
  g4_arrays_gen                G4  arrays and multiplication strategies (067, 095, 097)
  g3_story_meaning_gen         G3  join / separate / compare, unknown anywhere (063–065)
  g5_expression_for_story_gen  G5  pick the chain of operations for a story (072)
  g3_estimate_sum_gen          G3  estimate a sum / difference (083)
  g5_estimate_quotient_gen     G5  estimate a quotient with compatible numbers (084)
  g6_divisibility_gen          G6  divisibility by 2, 3, 4, 5, 6, 8, 9, 10 (103)
  g6_prime_factors_gen         G6  prime factorisation, factor trees (101)
  g6_powers_gen                G6  exponents, squares and cubes (022, 025, 102)
  g5_number_patterns_gen       G5  sequences: ×2, squares, triangular, growing steps (016, 107)
  g4_times_tables_gen          G4  multiplication facts 0×0 … 10×10, typed and timed (094, 096)
  g6_write_large_number_gen    G6  write numbers up to 999 999 from words (008)
"""
import random

from quiz import illustrations as ill
from .kit import mc, typed, N
from . import scenarios as sc


def _int_pad(v, spread=10):
    def pad():
        return str(max(1, v + random.choice([i for i in range(-spread, spread + 1) if i])))
    return pad


# ── G3 · Which equality is true? ─────────────────────────────────────────────

def _expr_equal_to(v, hi):
    """A random + / − / × expression equal to v (operands within 0..hi)."""
    kind = random.choice(['+', '−', '×'] if v > 3 else ['+', '−'])
    if kind == '+':
        a = random.randint(0, v)
        return f'{a} + {v - a}'
    if kind == '−':
        b = random.randint(1, max(1, hi // 3))
        return f'{v + b} − {b}'
    divs = [d for d in range(2, 10) if v % d == 0 and v // d > 1]
    if not divs:
        a = random.randint(0, v)
        return f'{a} + {v - a}'
    d = random.choice(divs)
    return f'{d} × {v // d}'


def g3_equality_true_gen(level='medium'):
    hi = 20 if level == 'easy' else 100 if level == 'medium' else 500
    v = random.randint(6, hi)
    left = _expr_equal_to(v, hi)
    right = _expr_equal_to(v, hi)
    while right == left:
        right = _expr_equal_to(v, hi)
    correct = f'{left} = {right}'
    wrong = []
    while len(wrong) < 4:
        delta = random.choice([-2, -1, 1, 2, 10, -10] if level != 'easy' else [-2, -1, 1, 2])
        w = v + delta
        if w <= 0:
            continue
        cand = f'{_expr_equal_to(v, hi)} = {_expr_equal_to(w, hi)}'
        if cand not in [x[0] for x in wrong]:
            wrong.append((cand, 'unequal', 'Work out BOTH sides: they must give the same number.',
                          'Calcule les DEUX côtés : ils doivent donner le même nombre.'))
    return mc(('Laquelle de ces égalités est **vraie** ?', 'Which of these equalities is **true**?'),
              correct, wrong,
              ('Le signe = veut dire « a la même valeur que ». Calcule chaque côté.', 'The = sign means "has the same value as". Work out each side.'),
              ([f'{left} = {v}', f'{right} = {v}', f'Les deux côtés valent {v} : {correct}'],
               [f'{left} = {v}', f'{right} = {v}', f'Both sides are {v}: {correct}']))


# ── G4 · Equivalent expressions ──────────────────────────────────────────────

def g4_equivalent_expr_gen(level='medium'):
    a = random.randint(12, 60 if level != 'hard' else 400)
    b = random.randint(11, 60 if level != 'hard' else 400)
    v = a + b
    if random.random() < 0.5:
        # typed: 25 + 27 = 30 + ?
        r = (a // 10 + 1) * 10
        if r - a > b:
            r = a - a % 10
        missing = v - r
        return typed((f'Complète pour que l’égalité soit vraie : **{a} + {b} = {r} + ?**', f'Fill in so the equality is true: **{a} + {b} = {r} + ?**'),
                     [missing], 'integer',
                     (f'Les deux côtés doivent valoir {a} + {b}. {a} est devenu {r} : qu’arrive-t-il à {b} ?',
                      f'Both sides must equal {a} + {b}. {a} became {r}: what happens to {b}?'),
                     ([f'{a} + {b} = {v}', f'{v} − {r} = {missing}'], [f'{a} + {b} = {v}', f'{v} − {r} = {missing}']))
    correct = random.choice([f'{v - 10} + 10', f'{2 * v} ÷ 2', f'{v + 5} − 5', f'{a - a % 10} + {b + a % 10}'])
    wrong = [(f'{a + 1} + {b + 1}', 'both_up', 'Adding to both numbers changes the sum.', 'Ajouter aux deux nombres change la somme.'),
             (f'{a} − {b}' if a > b else f'{b} − {a}', 'wrong_op', 'Keep the same total.', 'Garde le même total.'),
             (f'{v + 10} − 1', 'off', 'Work out the expression.', 'Calcule l’expression.'),
             (f'{v} × 2', 'double', 'That is twice as much.', 'C’est deux fois plus.'),
             (f'{a - 10} + {b - 10}' if a > 10 and b > 10 else f'{a + 10} + {b}', 'both_down', 'Taking from both numbers changes the sum.', 'Enlever aux deux nombres change la somme.')]
    return mc((f'Quelle expression est égale à **{a} + {b}** ?', f'Which expression is equal to **{a} + {b}**?'),
              correct, wrong,
              ('Calcule la valeur de chaque expression et compare.', 'Work out each expression and compare.'),
              ([f'{a} + {b} = {v}', f'{correct} = {v}'], [f'{a} + {b} = {v}', f'{correct} = {v}']))


# ── G4 · Properties without computing ────────────────────────────────────────

def g4_properties_gen(level='medium'):
    hi = 50 if level == 'easy' else 200 if level == 'medium' else 999
    a, b, c = random.randint(11, hi), random.randint(11, hi), random.randint(2, 30)
    kind = random.choice(['comm_add', 'comm_mul'] if level == 'easy' else ['comm_add', 'comm_mul', 'assoc_add', 'assoc_mul', 'inverse'])
    if kind == 'comm_add':
        return typed((f'Complète sans calculer : **{a} + {b} = {b} + ?**', f'Fill in without calculating: **{a} + {b} = {b} + ?**'),
                     [a], 'integer', ('On peut additionner dans n’importe quel ordre.', 'You can add in any order.'),
                     ([f'{a} + {b} = {b} + {a} (commutativité)'], [f'{a} + {b} = {b} + {a} (commutative property)']))
    if kind == 'comm_mul':
        x, y = random.randint(3, 12), random.randint(13, 99)
        return typed((f'Complète sans calculer : **{x} × {y} = {y} × ?**', f'Fill in without calculating: **{x} × {y} = {y} × ?**'),
                     [x], 'integer', ('On peut multiplier dans n’importe quel ordre.', 'You can multiply in any order.'),
                     ([f'{x} × {y} = {y} × {x} (commutativité)'], [f'{x} × {y} = {y} × {x} (commutative property)']))
    if kind == 'assoc_add':
        return typed((f'Complète sans calculer : **({a} + {b}) + {c} = {a} + ({b} + ?)**', f'Fill in without calculating: **({a} + {b}) + {c} = {a} + ({b} + ?)**'),
                     [c], 'integer', ('On peut regrouper les termes d’une addition comme on veut.', 'You can group the terms of a sum any way you like.'),
                     ([f'({a} + {b}) + {c} = {a} + ({b} + {c}) (associativité)'], [f'({a} + {b}) + {c} = {a} + ({b} + {c}) (associative property)']))
    if kind == 'assoc_mul':
        x, y, z = random.randint(2, 9), random.choice([2, 4, 5, 25]), random.randint(2, 9)
        return typed((f'Complète sans calculer : **({x} × {y}) × {z} = {x} × ({y} × ?)**', f'Fill in without calculating: **({x} × {y}) × {z} = {x} × ({y} × ?)**'),
                     [z], 'integer', ('On peut regrouper les facteurs comme on veut.', 'You can group the factors any way you like.'),
                     ([f'({x} × {y}) × {z} = {x} × ({y} × {z}) (associativité)'], [f'({x} × {y}) × {z} = {x} × ({y} × {z}) (associative property)']))
    s = a + b
    return typed((f'Sachant que **{a} + {b} = {s}**, complète sans calculer : **{s} − {b} = ?**', f'Knowing that **{a} + {b} = {s}**, fill in without calculating: **{s} − {b} = ?**'),
                 [a], 'integer', ('La soustraction défait l’addition.', 'Subtraction undoes addition.'),
                 ([f'{a} + {b} = {s} donc {s} − {b} = {a}'], [f'{a} + {b} = {s} so {s} − {b} = {a}']))


# ── G6 · Distributivity ──────────────────────────────────────────────────────

def g6_distributive_gen(level='medium'):
    a = random.randint(3, 9)
    tens = random.choice([10, 20, 30, 40]) if level != 'easy' else 10
    u = random.randint(1, 9)
    b = tens + u
    kind = random.choice(['split', 'picture'] if level == 'easy' else ['split', 'mental', 'mc'])
    if kind == 'picture':
        return typed((f'Le tableau de {a} lignes et {b} colonnes est coupé en deux. Complète : **{a} × {b} = {a} × 10 + {a} × ?**',
                      f'The array of {a} rows and {b} columns is cut in two. Fill in: **{a} × {b} = {a} × 10 + {a} × ?**'),
                     [u], 'integer', ('Compte les colonnes bleues : la partie rouge a 10 colonnes.', 'Count the blue columns: the red part has 10 columns.'),
                     ([f'{b} = 10 + {u}', f'{a} × {b} = {a} × 10 + {a} × {u} = {a * 10} + {a * u} = {a * b}'],
                      [f'{b} = 10 + {u}', f'{a} × {b} = {a} × 10 + {a} × {u} = {a * 10} + {a * u} = {a * b}']),
                     shape=ill.dot_array(a, b, split_col=10))
    if kind == 'split':
        return typed((f'Complète : **{a} × {b} = {a} × {tens} + {a} × ?**', f'Fill in: **{a} × {b} = {a} × {tens} + {a} × ?**'),
                     [u], 'integer', (f'Décompose {b} en {tens} + {u}.', f'Split {b} into {tens} + {u}.'),
                     ([f'{b} = {tens} + {u}', f'{a} × {b} = {a} × {tens} + {a} × {u} = {a * tens} + {a * u} = {a * b}'],
                      [f'{b} = {tens} + {u}', f'{a} × {b} = {a} × {tens} + {a} × {u} = {a * tens} + {a * u} = {a * b}']))
    if kind == 'mental':
        x = random.randint(3, 9)
        p, q = random.choice([(25, 75), (40, 60), (30, 70), (45, 55), (12, 88)])
        return typed((f'Calcule astucieusement : **{x} × {p} + {x} × {q}**', f'Calculate cleverly: **{x} × {p} + {x} × {q}**'),
                     [x * (p + q)], 'integer', ('Mets le facteur commun en évidence.', 'Take out the common factor.'),
                     ([f'{x} × {p} + {x} × {q} = {x} × ({p} + {q}) = {x} × {p + q} = {x * (p + q)}'],
                      [f'{x} × {p} + {x} × {q} = {x} × ({p} + {q}) = {x} × {p + q} = {x * (p + q)}']))
    correct = f'{a} × {tens} + {a} × {u}'
    wrong = [(f'{a} × {tens} + {u}', 'forgot_factor', f'Multiply BOTH parts by {a}.', f'Multiplie LES DEUX parties par {a}.'),
             (f'{a} + {tens} × {u}', 'mixed', 'Keep the factor and split the other number.', 'Garde le facteur et décompose l’autre nombre.'),
             (f'{a} × {tens} × {u}', 'times', 'The parts are added, not multiplied.', 'Les parties s’additionnent, elles ne se multiplient pas.'),
             (f'{a} × {tens} + {a} × {u + 1}', 'split', f'{tens} + {u + 1} is not {b}.', f'{tens} + {u + 1} ne fait pas {b}.'),
             (f'{a + tens} × {u}', 'mixed', 'Keep the factor and split the other number.', 'Garde le facteur et décompose l’autre nombre.')]
    return mc((f'Quelle expression est égale à **{a} × {b}** ?', f'Which expression is equal to **{a} × {b}**?'),
              correct, wrong, (f'{b} = {tens} + {u}', f'{b} = {tens} + {u}'),
              ([f'{a} × {b} = {correct} = {a * b}'], [f'{a} × {b} = {correct} = {a * b}']))


# ── G4 · Missing factor / divisor ────────────────────────────────────────────

def g4_missing_factor_gen(level='medium'):
    a = random.randint(2, 10) if level != 'hard' else random.randint(3, 12)
    b = random.randint(2, 10) if level == 'easy' else random.randint(2, 12) if level == 'medium' else random.randint(11, 25)
    c = a * b
    form = random.choice(['a×?=c', '?×b=c'] if level == 'easy' else ['a×?=c', '?×b=c', 'c÷?=a', '?÷a=b'])
    if form == 'a×?=c':
        p, ans, why = f'{a} × ? = {c}', b, (f'{c} ÷ {a} = {b}', f'{c} ÷ {a} = {b}')
    elif form == '?×b=c':
        p, ans, why = f'? × {b} = {c}', a, (f'{c} ÷ {b} = {a}', f'{c} ÷ {b} = {a}')
    elif form == 'c÷?=a':
        p, ans, why = f'{c} ÷ ? = {a}', b, (f'{a} × ? = {c} → {b}', f'{a} × ? = {c} → {b}')
    else:
        p, ans, why = f'? ÷ {a} = {b}', c, (f'{a} × {b} = {c}', f'{a} × {b} = {c}')
    return typed((f'Trouve le nombre manquant : **{p}**', f'Find the missing number: **{p}**'),
                 [ans], 'integer',
                 ('La multiplication et la division sont des opérations inverses.', 'Multiplication and division undo each other.'),
                 ([why[0], f'{p.replace("?", str(ans))}'], [why[1], f'{p.replace("?", str(ans))}']))


# ── G4 · Division with remainder ─────────────────────────────────────────────

def g4_division_remainder_gen(level='medium'):
    d = random.randint(2, 9) if level != 'hard' else random.randint(11, 25)
    q = random.randint(2, 9) if level == 'easy' else random.randint(10, 99) if level == 'medium' else random.randint(20, 300)
    r = random.randint(1, d - 1)
    n = d * q + r
    ask = random.choice(['q', 'r'])
    if level == 'hard' and random.random() < 0.4:
        who, g = random.choice(sc.ACTORS)
        cap = random.choice([('boîtes', 'boxes'), ('sacs', 'bags'), ('rangées', 'rows')])
        return typed((f'{who} range **{N(n)}** biscuits dans des {cap[0]} de **{d}**. Combien de {cap[0]} complètes peut-{sc.pronoun_fr(g)} remplir ?',
                      f'{who} packs **{N(n)}** cookies into {cap[1]} of **{d}**. How many full {cap[1]} can {sc.pronoun_en(g)} fill?'),
                     [q], 'integer',
                     ('Le reste ne remplit pas une boîte complète.', 'The remainder does not fill a whole box.'),
                     ([f'{n} = {d} × {q} + {r}', f'{q} complètes, il reste {r}'], [f'{n} = {d} × {q} + {r}', f'{q} full, {r} left over']))
    name = ('le **quotient**', 'the **quotient**') if ask == 'q' else ('le **reste**', 'the **remainder**')
    return typed((f'Dans la division **{N(n)} ÷ {d}**, quel est {name[0]} ?', f'In the division **{N(n)} ÷ {d}**, what is {name[1]}?'),
                 [q if ask == 'q' else r], 'integer',
                 (f'Cherche le plus grand multiple de {d} qui ne dépasse pas {n}.', f'Find the largest multiple of {d} that is not more than {n}.'),
                 ([f'{d} × {q} = {d * q}', f'{n} − {d * q} = {r}', f'Quotient {q}, reste {r}'],
                  [f'{d} × {q} = {d * q}', f'{n} − {d * q} = {r}', f'Quotient {q}, remainder {r}']))


# ── G4 · Arrays ──────────────────────────────────────────────────────────────

def g4_arrays_gen(level='medium'):
    r, c = random.randint(2, 6 if level == 'easy' else 9), random.randint(3, 10)
    if r == c:
        c += 1
    kind = random.choice(['which', 'count'] if level == 'easy' else ['which', 'count', 'strategy'])
    shape = ill.dot_array(r, c)
    if kind == 'which':
        wrong = [(f'{r} + {c}', 'added', 'Rows × columns, not rows + columns.', 'Lignes × colonnes, pas lignes + colonnes.'),
                 (f'{r} × {c + 1}', 'miscount', 'Count the columns again.', 'Recompte les colonnes.'),
                 (f'{r + 1} × {c}', 'miscount', 'Count the rows again.', 'Recompte les lignes.'),
                 (f'{r * c} × 2', 'double', 'One multiplication: rows × columns.', 'Une seule multiplication : lignes × colonnes.'),
                 (f'{r - 1} × {c}' if r > 2 else f'{r} × {c - 1}', 'miscount', 'Count the rows again.', 'Recompte les lignes.')]
        return mc(('Quelle multiplication représente ce tableau de points ?', 'Which multiplication matches this array of dots?'),
                  f'{r} × {c}', wrong, ('Compte les lignes, puis les points dans une ligne.', 'Count the rows, then the dots in one row.'),
                  ([f'{r} lignes de {c} points : {r} × {c} = {r * c}'], [f'{r} rows of {c} dots: {r} × {c} = {r * c}']), shape=shape)
    if kind == 'count':
        return typed(('Combien y a-t-il de points en tout ? Utilise une multiplication.', 'How many dots are there in all? Use a multiplication.'),
                     [r * c], 'integer', ('Lignes × points par ligne.', 'Rows × dots in a row.'),
                     ([f'{r} × {c} = {r * c}'], [f'{r} × {c} = {r * c}']), shape=shape)
    a = random.randint(6, 9)
    b = random.randint(3, 9)
    near = 5                      # 6, 7, 8, 9 = 5 + something: start from a known fact
    diff = a - near
    return typed((f'Pour calculer **{a} × {b}**, Léa fait **{near} × {b} + ? × {b}**. Complète.', f'To work out **{a} × {b}**, Léa does **{near} × {b} + ? × {b}**. Fill in.'),
                 [diff], 'integer', (f'{a} = {near} + ?', f'{a} = {near} + ?'),
                 ([f'{a} = {near} + {diff}', f'{a} × {b} = {near * b} + {diff * b} = {a * b}'], [f'{a} = {near} + {diff}', f'{a} × {b} = {near * b} + {diff * b} = {a * b}']))


# ── G3 · Meaning of + and − in stories ───────────────────────────────────────

_OBJ = [('billes', 'marbles'), ('cartes', 'cards'), ('autocollants', 'stickers'), ('timbres', 'stamps'), ('livres', 'books')]


def g3_story_meaning_gen(level='medium'):
    hi = 50 if level == 'easy' else 500 if level == 'medium' else 999
    who, g = random.choice(sc.ACTORS)
    other = random.choice([n for n, _ in sc.ACTORS if n != who])
    obj = random.choice(_OBJ)
    il, he = sc.pronoun_fr(g), sc.pronoun_en(g)
    a = random.randint(5, hi // 2)
    b = random.randint(3, hi // 2)
    kinds = ['join_result', 'separate_result', 'compare_diff'] if level == 'easy' else \
            ['join_change', 'join_start', 'separate_change', 'separate_start', 'compare_diff', 'compare_more', 'compare_less']
    kind = random.choice(kinds)
    if kind == 'join_result':
        p = (f'{who} a {a} {obj[0]}. {other} lui en donne {b}. Combien de {obj[0]} {who} a-t-{il} maintenant ?',
             f'{who} has {a} {obj[1]}. {other} gives {he == "she" and "her" or "him"} {b} more. How many {obj[1]} does {who} have now?')
        ans, st = a + b, (f'{a} + {b} = {a + b}', f'{a} + {b} = {a + b}')
    elif kind == 'separate_result':
        a = a + b
        p = (f'{who} a {a} {obj[0]}. {il.capitalize()} en perd {b}. Combien lui en reste-t-il ?',
             f'{who} has {a} {obj[1]} and loses {b}. How many are left?')
        ans, st = a - b, (f'{a} − {b} = {a - b}', f'{a} − {b} = {a - b}')
    elif kind == 'join_change':
        p = (f'{who} avait {a} {obj[0]}. On lui en donne quelques-uns. Maintenant, {il} en a {a + b}. Combien lui en a-t-on donné ?',
             f'{who} had {a} {obj[1]}. Someone gave {he == "she" and "her" or "him"} some more. Now {he} has {a + b}. How many was {he} given?')
        ans, st = b, (f'{a + b} − {a} = {b}', f'{a + b} − {a} = {b}')
    elif kind == 'join_start':
        p = (f'{who} avait des {obj[0]}. On lui en donne {b}. Maintenant, {il} en a {a + b}. Combien en avait-{il} au départ ?',
             f'{who} had some {obj[1]}. Someone gave {he == "she" and "her" or "him"} {b} more. Now {he} has {a + b}. How many did {he} have at the start?')
        ans, st = a, (f'{a + b} − {b} = {a}', f'{a + b} − {b} = {a}')
    elif kind == 'separate_change':
        p = (f'{who} avait {a + b} {obj[0]}. {il.capitalize()} en a donné. Il lui en reste {a}. Combien en a-t-{il} donné ?',
             f'{who} had {a + b} {obj[1]} and gave some away. {he.capitalize()} has {a} left. How many did {he} give away?')
        ans, st = b, (f'{a + b} − {a} = {b}', f'{a + b} − {a} = {b}')
    elif kind == 'separate_start':
        p = (f'{who} avait des {obj[0]}. {il.capitalize()} en a donné {b}. Il lui en reste {a}. Combien en avait-{il} au départ ?',
             f'{who} had some {obj[1]} and gave {b} away. {he.capitalize()} has {a} left. How many did {he} have at the start?')
        ans, st = a + b, (f'{a} + {b} = {a + b}', f'{a} + {b} = {a + b}')
    elif kind == 'compare_diff':
        p = (f'{who} a {a + b} {obj[0]} et {other} en a {a}. Combien {who} en a-t-{il} de plus que {other} ?',
             f'{who} has {a + b} {obj[1]} and {other} has {a}. How many more does {who} have than {other}?')
        ans, st = b, (f'{a + b} − {a} = {b}', f'{a + b} − {a} = {b}')
    elif kind == 'compare_more':
        p = (f'{other} a {a} {obj[0]}. {who} en a {b} de plus que {other}. Combien {who} en a-t-{il} ?',
             f'{other} has {a} {obj[1]}. {who} has {b} more than {other}. How many does {who} have?')
        ans, st = a + b, (f'{a} + {b} = {a + b}', f'{a} + {b} = {a + b}')
    else:
        p = (f'{who} a {a + b} {obj[0]}. C’est {b} de plus que {other}. Combien de {obj[0]} a {other} ?',
             f'{who} has {a + b} {obj[1]}. That is {b} more than {other}. How many does {other} have?')
        ans, st = a, (f'{a + b} − {b} = {a}', f'{a + b} − {b} = {a}')
    return typed(p, [ans], 'integer',
                 ('Demande-toi : connaît-on le début, le changement ou la fin ? Fais un petit schéma.',
                  'Ask yourself: do we know the start, the change or the end? Draw a quick sketch.'),
                 ([st[0]], [st[1]]))


# ── G5 · Pick the expression for a story ─────────────────────────────────────

def g5_expression_for_story_gen(level='medium'):
    who, g = random.choice(sc.ACTORS)
    a, b, c = random.randint(3, 9), random.randint(4, 12), random.randint(2, 9)
    obj = random.choice([('paquets de crayons', 'packs of pencils', 'crayons', 'pencils'),
                         ('boîtes de biscuits', 'boxes of cookies', 'biscuits', 'cookies'),
                         ('sacs de billes', 'bags of marbles', 'billes', 'marbles')])
    kind = random.choice(['minus', 'plus', 'share'] if level != 'easy' else ['minus', 'plus'])
    if kind == 'minus':
        c = min(c, a * b - 1)
        p = (f'{who} achète **{a}** {obj[0]} de **{b}**, puis en donne **{c}** à un ami.',
             f'{who} buys **{a}** {obj[1]} with **{b}** in each, then gives **{c}** to a friend.')
        correct = f'{a} × {b} − {c}'
        wrong = [f'{a} × ({b} − {c})', f'{a} + {b} − {c}', f'{a} × {b} + {c}', f'({a} − {c}) × {b}', f'{a} × {b} × {c}']
        val = a * b - c
    elif kind == 'plus':
        p = (f'{who} a **{c}** {obj[2]}. {sc.pronoun_fr(g).capitalize()} achète **{a}** {obj[0]} de **{b}**.',
             f'{who} has **{c}** {obj[3]} and buys **{a}** {obj[1]} with **{b}** in each.')
        correct = f'{c} + {a} × {b}'
        wrong = [f'({c} + {a}) × {b}', f'{c} × {a} + {b}', f'{c} + {a} + {b}', f'{c} × {a} × {b}', f'{a} × ({b} + {c})']
        val = c + a * b
    else:
        k = random.randint(2, 6)
        tot_each = a * b + c
        while tot_each % k:
            c += 1
            tot_each = a * b + c
        p = (f'{who} a **{a}** {obj[0]} de **{b}** et **{c}** {obj[2]} en vrac. {sc.pronoun_fr(g).capitalize()} partage tout également entre **{k}** amis.',
             f'{who} has **{a}** {obj[1]} with **{b}** in each and **{c}** loose {obj[3]}, and shares everything equally among **{k}** friends.')
        correct = f'({a} × {b} + {c}) ÷ {k}'
        wrong = [f'{a} × {b} + {c} ÷ {k}', f'{a} × ({b} + {c}) ÷ {k}', f'({a} + {b} + {c}) ÷ {k}', f'{a} × {b} + {c} × {k}', f'({a} × {b} − {c}) ÷ {k}']
        val = (a * b + c) // k
    return mc((p[0] + ' Quelle chaîne d’opérations donne la réponse ?', p[1] + ' Which chain of operations gives the answer?'),
              correct, [(w, 'order', 'Remember: × and ÷ come before + and −, unless there are parentheses.',
                         'Rappel : × et ÷ passent avant + et −, sauf s’il y a des parenthèses.') for w in wrong],
              ('Repère ce qui se fait en premier dans l’histoire ; les parenthèses imposent un ordre.', 'Find what happens first in the story; parentheses force an order.'),
              ([f'{correct} = {val}'], [f'{correct} = {val}']))


# ── Estimation ───────────────────────────────────────────────────────────────

def g3_estimate_sum_gen(level='medium'):
    to = 10 if level == 'easy' else random.choice([10, 100]) if level == 'medium' else 100
    hi = 99 if level == 'easy' else 999 if level == 'medium' else 4999
    a, b = random.randint(to + 1, hi), random.randint(to + 1, hi)
    sub = random.random() < 0.4
    if sub and a < b:
        a, b = b, a
    ra, rb = (a + to // 2) // to * to, (b + to // 2) // to * to
    if sub and ra <= rb:
        a += 3 * to
        ra = (a + to // 2) // to * to
    est = ra - rb if sub else ra + rb
    op = '−' if sub else '+'
    exact = a - b if sub else a + b
    wrong = [(str(exact), 'exact', 'An estimate uses rounded numbers.', 'Une estimation utilise des nombres arrondis.'),
             (str(est + to), 'off', f'Round each number to the nearest {to}.', f'Arrondis chaque nombre à la {"dizaine" if to == 10 else "centaine"} près.'),
             (str(est - to) if est > to else str(est + 2 * to), 'off', f'Round each number to the nearest {to}.', f'Arrondis chaque nombre à la {"dizaine" if to == 10 else "centaine"} près.'),
             (str(est * 10), 'place', 'Check the size of your answer.', 'Vérifie la grandeur de ta réponse.'),
             (str(ra + rb if sub else abs(ra - rb)) if (ra + rb if sub else abs(ra - rb)) > 0 else str(est + 3 * to), 'wrong_op', 'Keep the same operation.', 'Garde la même opération.')]
    word = ('dizaine', 'ten') if to == 10 else ('centaine', 'hundred')
    return mc((f'Arrondis chaque nombre à la {word[0]} près pour **estimer** : **{a} {op} {b}**', f'Round each number to the nearest {word[1]} to **estimate**: **{a} {op} {b}**'),
              str(est), wrong, ('Arrondis d’abord, calcule ensuite.', 'Round first, then calculate.'),
              ([f'{a} ≈ {ra}', f'{b} ≈ {rb}', f'{ra} {op} {rb} = {est}'], [f'{a} ≈ {ra}', f'{b} ≈ {rb}', f'{ra} {op} {rb} = {est}']),
              pad=_int_pad(est, 3 * to))


def g5_estimate_quotient_gen(level='medium'):
    d = random.randint(3, 9) if level != 'hard' else random.choice([12, 15, 21, 25, 31, 42])
    q_est = random.randint(2, 9) * (10 if level == 'easy' else 100)
    compat = d * q_est
    n = compat + random.randint(-d * 3, d * 3)
    wrong = [(str(q_est * 10), 'place', 'Check the size: multiply your estimate back.', 'Vérifie la grandeur : remultiplie ton estimation.'),
             (str(q_est // 10) if q_est >= 100 else str(q_est + 30), 'place', 'Check the size: multiply your estimate back.', 'Vérifie la grandeur : remultiplie ton estimation.'),
             (str(q_est + (10 if level == 'easy' else 100)), 'off', 'Look for a multiple of the divisor close to the number.', 'Cherche un multiple du diviseur proche du nombre.'),
             (str(q_est - (10 if level == 'easy' else 100)), 'off', 'Look for a multiple of the divisor close to the number.', 'Cherche un multiple du diviseur proche du nombre.')]
    return mc((f'Quelle est la meilleure **estimation** de **{N(n)} ÷ {d}** ?', f'What is the best **estimate** of **{N(n)} ÷ {d}**?'),
              str(q_est), wrong,
              (f'Remplace {N(n)} par un nombre proche facile à diviser par {d}.', f'Replace {N(n)} by a nearby number that is easy to divide by {d}.'),
              ([f'{N(n)} ≈ {N(compat)}', f'{N(compat)} ÷ {d} = {q_est}'], [f'{N(n)} ≈ {N(compat)}', f'{N(compat)} ÷ {d} = {q_est}']),
              pad=_int_pad(q_est, q_est // 2))


# ── G6 · Divisibility ────────────────────────────────────────────────────────

_RULES = {2: ('le chiffre des unités est pair', 'the last digit is even'),
          3: ('la somme des chiffres est un multiple de 3', 'the digit sum is a multiple of 3'),
          4: ('les deux derniers chiffres forment un multiple de 4', 'the last two digits make a multiple of 4'),
          5: ('le chiffre des unités est 0 ou 5', 'the last digit is 0 or 5'),
          6: ('il est divisible par 2 ET par 3', 'it is divisible by 2 AND by 3'),
          8: ('les trois derniers chiffres forment un multiple de 8', 'the last three digits make a multiple of 8'),
          9: ('la somme des chiffres est un multiple de 9', 'the digit sum is a multiple of 9'),
          10: ('le chiffre des unités est 0', 'the last digit is 0')}


def g6_divisibility_gen(level='medium'):
    k = random.choice([2, 5, 10] if level == 'easy' else [2, 3, 4, 5, 9, 10] if level == 'medium' else [3, 4, 6, 8, 9])
    hi = 999 if level == 'easy' else 9999
    good = random.randrange(k * (100 // k + 1), hi, k)
    bad = []
    while len(bad) < 4:
        x = random.randint(100, hi)
        if x % k and str(x) not in bad:
            if k in (3, 9) and random.random() < 0.6:
                x = x - x % 3 + (1 if x % 3 == 0 else 0)          # near misses
                if x % k == 0:
                    continue
            bad.append(str(x))
    digits = ' + '.join(str(good))
    return mc((f'Lequel de ces nombres est **divisible par {k}** ?', f'Which of these numbers is **divisible by {k}**?'),
              str(good), [(b, 'rule', f'Divisible by {k}: {_RULES[k][1]}.', f'Divisible par {k} : {_RULES[k][0]}.') for b in bad],
              (f'Un nombre est divisible par {k} si {_RULES[k][0]}.', f'A number is divisible by {k} if {_RULES[k][1]}.'),
              ([f'{good} : {_RULES[k][0]}' + (f' ({digits} = {sum(map(int, str(good)))})' if k in (3, 9) else ''), f'{good} ÷ {k} = {good // k}'],
               [f'{good}: {_RULES[k][1]}' + (f' ({digits} = {sum(map(int, str(good)))})' if k in (3, 9) else ''), f'{good} ÷ {k} = {good // k}']))


# ── G6 · Prime factors ───────────────────────────────────────────────────────

def _factors(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out


def _tree(n):
    """Factor tree splitting n into (small prime) × (rest)."""
    fs = _factors(n)
    if len(fs) == 1:
        return n
    p = fs[0]
    return (n, p, _tree(n // p))


def g6_prime_factors_gen(level='medium'):
    pool = [12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 50] if level == 'easy' else \
           [48, 54, 56, 60, 63, 72, 75, 80, 84, 90, 96, 100] if level == 'medium' else [108, 120, 126, 132, 140, 150, 168, 180, 196, 210]
    n = random.choice(pool)
    fs = _factors(n)
    correct = ' × '.join(map(str, fs))
    if level == 'hard' and random.random() < 0.5:
        tree = _tree(n)
        inner = [t for t in _walk(tree) if not isinstance(t, int)]
        hide_val = random.choice([t[0] for t in inner[1:]] or [fs[-1]])
        return typed((f'Voici l’arbre des facteurs de **{n}**. Quel nombre remplace le « ? » ?', f'Here is the factor tree of **{n}**. Which number replaces the “?”?'),
                      [hide_val], 'integer',
                      ('Chaque nombre est le produit des deux nombres juste en dessous.', 'Each number is the product of the two numbers just below it.'),
                      ([f'{n} = {correct}'], [f'{n} = {correct}']), shape=ill.factor_tree(tree, hide=hide_val))
    a = fs[0]
    wrong = [(f'{a} × {n // a}' if not _is_prime(n // a) else f'{a * a} × {n // (a * a)}' if n % (a * a) == 0 else f'1 × {n}', 'not_prime', 'Every factor must be a prime number.', 'Chaque facteur doit être un nombre premier.'),
             (' × '.join(map(str, fs[1:])), 'missing', f'The product must equal {n}: you lost a factor.', f'Le produit doit donner {n} : il manque un facteur.'),
             (' × '.join(map(str, fs + [fs[0]])), 'extra', f'The product must equal {n}.', f'Le produit doit donner {n}.'),
             (' × '.join(map(str, sorted(fs[:-1] + [fs[-1] + 2]))), 'wrong', f'The product must equal {n}.', f'Le produit doit donner {n}.'),
             (f'{fs[0] * fs[1]} × ' + ' × '.join(map(str, fs[2:])) if len(fs) > 2 else f'{n} × 1', 'not_prime', 'Every factor must be a prime number.', 'Chaque facteur doit être un nombre premier.')]
    return mc((f'Quelle est la décomposition de **{n}** en facteurs premiers ?', f'What is the prime factorisation of **{n}**?'),
              correct, wrong,
              ('Divise par 2 tant que possible, puis par 3, 5, 7…', 'Divide by 2 as long as you can, then by 3, 5, 7…'),
              (_steps(n), _steps(n)))


def _walk(t):
    yield t
    if not isinstance(t, int):
        yield from _walk(t[1])
        yield from _walk(t[2])


def _is_prime(n):
    return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))


def _steps(n):
    out, m = [], n
    for p in _factors(n):
        out.append(f'{m} ÷ {p} = {m // p}')
        m //= p
    return out + [f'{n} = ' + ' × '.join(map(str, _factors(n)))]


# ── G6 · Powers ──────────────────────────────────────────────────────────────

_SUP = {2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶'}


def g6_powers_gen(level='medium'):
    kind = random.choice(['value', 'words'] if level == 'easy' else ['value', 'notation', 'words', 'compare'])
    base = random.randint(2, 10) if level != 'hard' else random.randint(2, 12)
    exp = 2 if level == 'easy' else random.choice([2, 3]) if level == 'medium' else random.choice([3, 4, 5]) if base <= 4 else random.choice([2, 3])
    val = base ** exp
    rep = ' × '.join([str(base)] * exp)
    if kind == 'value':
        return typed((f'Calcule : **{base}{_SUP[exp]}**', f'Calculate: **{base}{_SUP[exp]}**'),
                     [val], 'integer',
                     (f'L’exposant {exp} dit combien de fois on multiplie {base} par lui-même.', f'The exponent {exp} tells how many times {base} is multiplied by itself.'),
                     ([f'{base}{_SUP[exp]} = {rep} = {val}'], [f'{base}{_SUP[exp]} = {rep} = {val}']))
    if kind == 'words':
        word = {2: ('le carré', 'the square'), 3: ('le cube', 'the cube')}.get(exp, ('la puissance ' + str(exp), 'the power ' + str(exp)))
        if exp not in (2, 3):
            exp, val, rep = 2, base * base, f'{base} × {base}'
            word = ('le carré', 'the square')
        return typed((f'Quel est **{word[0]} de {base}** ?', f'What is **{word[1]} of {base}**?'),
                     [val], 'integer', (f'{word[0].capitalize()} de {base} = {rep}', f'{word[1].capitalize()} of {base} = {rep}'),
                     ([f'{rep} = {val}'], [f'{rep} = {val}']))
    if kind == 'notation':
        correct = f'{base}{_SUP[exp]}'
        wrong = [(f'{exp}{_SUP.get(base, "^" + str(base))}' if base in _SUP else f'{exp} × {base}', 'swapped', 'The base is the repeated number; the exponent counts it.', 'La base est le nombre répété ; l’exposant compte les répétitions.'),
                 (f'{base} × {exp}', 'times', 'An exponent is not a multiplication by the exponent.', 'Un exposant n’est pas une multiplication par l’exposant.'),
                 (f'{base}{_SUP[exp + 1 if exp < 6 else exp - 1]}', 'count', 'Count how many times the number appears.', 'Compte combien de fois le nombre apparaît.'),
                 (f'{base * exp}', 'times', 'An exponent is not a multiplication by the exponent.', 'Un exposant n’est pas une multiplication par l’exposant.'),
                 (f'{base}{_SUP[exp - 1]}' if exp > 2 else f'{base + 1}{_SUP[exp]}', 'count', 'Count how many times the number appears.', 'Compte combien de fois le nombre apparaît.')]
        return mc((f'Comment écrit-on **{rep}** avec un exposant ?', f'How do you write **{rep}** with an exponent?'),
                  correct, wrong, ('Base = le nombre répété ; exposant = le nombre de fois.', 'Base = the repeated number; exponent = how many times.'),
                  ([f'{rep} = {correct} = {val}'], [f'{rep} = {correct} = {val}']))
    a, b = random.choice([(2, 3), (3, 2), (2, 4), (4, 2), (2, 5), (5, 2), (3, 4), (4, 3), (3, 5), (2, 6)])
    x, y = a ** b, b ** a
    sym = '<' if x < y else '>' if x > y else '='
    return typed((f'Compare avec <, > ou = : **{a}{_SUP[b]}** ⬜ **{b}{_SUP[a]}**', f'Compare with <, > or =: **{a}{_SUP[b]}** ⬜ **{b}{_SUP[a]}**'),
                 [sym], 'symbol', ('Calcule chaque puissance avant de comparer.', 'Work out each power before comparing.'),
                 ([f'{a}{_SUP[b]} = {x}', f'{b}{_SUP[a]} = {y}', f'{x} {sym} {y}'], [f'{a}{_SUP[b]} = {x}', f'{b}{_SUP[a]} = {y}', f'{x} {sym} {y}']))


# ── G5 · Number patterns ─────────────────────────────────────────────────────

def _sequence(level):
    kind = random.choice(['double', 'square', 'triangular', 'growing'] if level != 'easy' else ['double', 'growing'])
    if kind == 'double':
        s = random.randint(1, 6)
        seq = [s * 2 ** i for i in range(6)]
        rule = ('on multiplie par 2', 'multiply by 2')
    elif kind == 'square':
        s = random.randint(1, 4)
        seq = [(s + i) ** 2 for i in range(6)]
        rule = ('les nombres carrés', 'the square numbers')
    elif kind == 'triangular':
        seq = [n * (n + 1) // 2 for n in range(1, 7)]
        rule = ('on ajoute 2, puis 3, puis 4… (nombres triangulaires)', 'add 2, then 3, then 4… (triangular numbers)')
    else:
        s, step = random.randint(1, 20), random.randint(1, 3)
        seq = [s]
        for i in range(5):
            seq.append(seq[-1] + step + i)
        rule = (f'on ajoute {step}, puis {step + 1}, puis {step + 2}…', f'add {step}, then {step + 1}, then {step + 2}…')
    return kind, seq, rule


def g5_number_patterns_gen(level='medium'):
    kind, seq, rule = _sequence(level)
    shown = seq[:4] if level != 'hard' else seq[:5]
    nxt = seq[len(shown)]
    if level == 'hard' or random.random() < 0.6:
        return typed((f'Quel est le nombre suivant ? **{", ".join(map(str, shown))}, …**', f'What is the next number? **{", ".join(map(str, shown))}, …**'),
                     [nxt], 'integer', ('Regarde comment on passe d’un nombre au suivant : l’écart change-t-il ?', 'Look at how you get from one number to the next: does the gap change?'),
                     ([f'Règle : {rule[0]}', f'Suivant : {nxt}'], [f'Rule: {rule[1]}', f'Next: {nxt}']))
    rules = [('on multiplie par 2', 'multiply by 2'), ('les nombres carrés', 'the square numbers'),
             ('on ajoute 2, puis 3, puis 4… (nombres triangulaires)', 'add 2, then 3, then 4… (triangular numbers)'),
             ('on ajoute toujours le même nombre', 'add the same number each time'), ('on soustrait 1 à chaque fois', 'subtract 1 each time')]
    correct = rule if kind != 'growing' else ('l’écart augmente de 1 à chaque fois', 'the gap grows by 1 each time')
    return mc((f'Quelle est la règle de cette suite ? **{", ".join(map(str, seq[:5]))}, …**', f'What is the rule of this sequence? **{", ".join(map(str, seq[:5]))}, …**'),
              correct, [r for r in rules if r[0] != correct[0]],
              ('Calcule les écarts entre les nombres.', 'Work out the gaps between the numbers.'),
              ([f'Règle : {correct[0]}'], [f'Rule: {correct[1]}']))


# ── G4 · Times tables (fluency) ──────────────────────────────────────────────

def g4_times_tables_gen(level='medium'):
    tables = [2, 5, 10] if level == 'easy' else [3, 4, 6] if level == 'medium' else [6, 7, 8, 9]
    a = random.choice(tables)
    b = random.randint(0, 10)
    if random.random() < 0.5:
        a, b = b, a
    if level == 'hard' and random.random() < 0.4 and a and b:
        p = a * b
        return typed((f'**{p} ÷ {a} = ?**', f'**{p} ÷ {a} = ?**'), [b], 'integer',
                     (f'Pense à la table de {a} : {a} × ? = {p}', f'Think of the {a} times table: {a} × ? = {p}'),
                     ([f'{a} × {b} = {p} donc {p} ÷ {a} = {b}'], [f'{a} × {b} = {p} so {p} ÷ {a} = {b}']), time_limit=12)
    return typed((f'**{a} × {b} = ?**', f'**{a} × {b} = ?**'), [a * b], 'integer',
                 ('Récite la table, ou pars d’un fait que tu connais (× 2, × 5, × 10).', 'Say the table, or start from a fact you know (× 2, × 5, × 10).'),
                 ([f'{a} × {b} = {a * b}'], [f'{a} × {b} = {a * b}']), time_limit=10)


# ── G6 · Write large numbers ─────────────────────────────────────────────────

def g6_write_large_number_gen(level='medium'):
    from .g5_numeration import _to_fr, _to_en
    lo, hi = (10_000, 99_999) if level == 'easy' else (100_000, 999_999)
    n = random.randint(lo, hi)
    if level == 'hard':
        s = list(str(n))
        for i in random.sample(range(1, 6), 2):
            s[i] = '0'
        n = int(''.join(s))
    return typed((f'Écris en chiffres : **{_to_fr(n)}**', f'Write in digits: **{_to_en(n)}**'),
                 [str(n), N(n)], 'integer',
                 ('Repère le mot « mille » : à gauche, les milliers ; à droite, les centaines, dizaines et unités.',
                  'Find the word "thousand": on its left the thousands, on its right the hundreds, tens and ones.'),
                 ([f'{_to_fr(n)} = {N(n)}'], [f'{_to_en(n)} = {N(n)}']))
