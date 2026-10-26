"""
fractions_plus.py — WP2 of the curriculum upgrade (docs/curriculum/PLAN.md §4).

  fraction_shape_gen            G3  rewrite: bar / circle / collection, no answer printed (027, 028)
  g3_fraction_words_gen         G3  « trois quarts » ↔ 3/4 (031, 039, 040)
  g3_numerator_denominator_gen  G3  role of numerator and denominator (030, 040)
  g4_fraction_benchmark_gen     G4  compare to 0, ½ and 1 (032)
  g4_equivalent_fractions_gen   G4  equivalent fractions, pictures then numbers (033, 113)
  g5_fraction_meanings_gen      G5  sharing / division / ratio (029)
  g5_order_same_numerator_gen   G5  order fractions with the same numerator (037)
  g6_order_related_den_gen      G6  order fractions, one denominator a multiple of the others (036)
  g6_simplify_fraction_gen      G6  simplest form (114, 117)
  g6_fraction_add_related_gen   G6  + / − with related denominators (115)
  g6_whole_times_fraction_gen   G6  whole number × fraction, fraction of a quantity (116, 082)

Fractions stay "with material or diagrams" in grades 3–4 (pictures everywhere);
calculation (+, −, ×) only in grade 6, with related denominators, per the audit.
"""
import random
from fractions import Fraction

from quiz import illustrations as ill
from .kit import mc, typed, ordering, frac, simplest, frac_words, N
from . import scenarios as sc


def _frac_pad(d_max, avoid=None):
    """Random proper fraction for padding; never equal in value to ``avoid`` (the key, or a list of values)."""
    avoid = set(avoid) if isinstance(avoid, (list, set, tuple)) else {avoid} if avoid is not None else set()

    def pad():
        while True:
            d = random.randint(2, d_max)
            f = (random.randint(1, d - 1), d)
            # irreducible only, so a pad never repeats the value of another choice (1/4 vs 2/8)
            if Fraction(*f).denominator == d and Fraction(*f) not in avoid:
                return frac(*f)
    return pad


def _distinct_values(key, distractors):
    """Drop distractors equal in value to the key or to an earlier distractor (2/4 vs 1/2)."""
    def val(label):
        text = label[0] if isinstance(label, tuple) else label
        return Fraction(text.split(' ')[0])
    seen, out = {val(key)}, []
    for t in distractors:
        if t is None:
            continue
        v = val(t[0])
        if v not in seen:
            seen.add(v)
            out.append(t)
    return out


def _parts(n, fr_adj='', en_adj=''):
    """« 1 part coloriée » / « 3 parts coloriées » and the English twin."""
    pl = n > 1
    fr = f'{n} part{"s" if pl else ""}' + (f' {fr_adj}{"s" if pl else ""}' if fr_adj else '')
    en = f'{n}' + (f' {en_adj}' if en_adj else '') + f' part{"s" if pl else ""}'
    return fr, en


# ── G3 · Fraction of a shape (rewrite) ───────────────────────────────────────

_OBJ = [('ballons', 'balloons'), ('étoiles', 'stars'), ('billes', 'marbles'), ('jetons', 'counters')]


def fraction_shape_gen(level='medium'):
    d = random.randint(2, 4) if level == 'easy' else random.randint(3, 8) if level == 'medium' else random.randint(4, 10)
    n = random.randint(1, d - 1)
    kinds = ['bar', 'circle'] if level == 'easy' else ['bar', 'circle', 'collection']
    kind = random.choice(kinds)
    if kind == 'bar':
        shape = ill.fraction_bars([(n, d)], color=random.choice([ill.BLUE, ill.PURPLE, ill.TEAL]))
        what = ('de la bande', 'of the strip')
    elif kind == 'circle':
        shape = ill.fraction_circle(n, d, color=random.choice([ill.GREEN, ill.RED, ill.AMBER]))
        what = ('du disque', 'of the circle')
    else:
        obj = random.choice(_OBJ)
        shape = ill.collection(d, n, icon='star' if obj[0] == 'étoiles' else 'circle')
        what = (f'des {obj[0]}', f'of the {obj[1]}')
    correct = frac(n, d)
    distractors = [
        (frac(d - n, d), 'complement', 'You counted the parts that are NOT coloured.', 'Tu as compté les parts qui ne sont PAS coloriées.'),
        (frac(n, d - n) if d - n != n else frac(n, d + 1), 'part_part', 'The denominator is ALL the parts, coloured or not.', 'Le dénominateur, c’est TOUTES les parts, coloriées ou non.'),
        (frac(d, n), 'swapped', 'Coloured parts on top, total parts below.', 'Parts coloriées en haut, total des parts en bas.'),
        (frac(n + 1, d) if n + 1 < d else frac(n - 1, d) if n > 1 else frac(n, d + 2), 'miscount', 'Count the coloured parts again.', 'Recompte les parts coloriées.'),
        (frac(n, d + 1), 'miscount', 'Count all the parts again.', 'Recompte toutes les parts.'),
    ]
    distractors = _distinct_values(correct, distractors)
    taken = [Fraction(n, d)] + [Fraction(t[0]) for t in distractors]
    return mc((f'Quelle fraction {what[0]} est coloriée ?', f'What fraction {what[1]} is coloured?'),
              correct, distractors,
              ('Compte toutes les parts égales (dénominateur), puis les parts coloriées (numérateur).',
               'Count all the equal parts (denominator), then the coloured parts (numerator).'),
              ([f'{d} parts égales en tout → dénominateur {d}', f'{_parts(n, "coloriée")[0]} → numérateur {n}', f'Réponse : {correct}'],
               [f'{d} equal parts in all → denominator {d}', f'{_parts(n, en_adj="coloured")[1]} → numerator {n}', f'Answer: {correct}']),
              shape=shape, pad=_frac_pad(10, taken))


# ── G3 · Fraction words ──────────────────────────────────────────────────────

def g3_fraction_words_gen(level='medium'):
    dens = [2, 3, 4] if level == 'easy' else [2, 3, 4, 5, 6, 8, 10] if level == 'medium' else [3, 4, 5, 6, 7, 8, 9, 10, 12]
    d = random.choice(dens)
    n = random.randint(1, d - 1)
    words = frac_words(n, d)
    if random.random() < 0.5:
        return typed((f'Écris en chiffres la fraction : **{words[0]}**', f'Write this fraction with digits: **{words[1]}**'),
                     [frac(n, d)], 'fraction',
                     ('Le mot du nombre de parts (tiers, quarts…) donne le dénominateur.',
                      'The part word (thirds, quarters…) gives the denominator.'),
                     ([f'« {words[0]} » : {_parts(n)[0]} sur {d}', f'= {frac(n, d)}'], [f'"{words[1]}": {_parts(n)[1]} out of {d}', f'= {frac(n, d)}']))
    others = []
    for nn, dd in [(d - n, d), (n, d + 1 if d + 1 <= 12 else d - 1), (min(n + 1, 12), d), (d, n)]:
        if 0 < nn < 13 and dd in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) and (nn, dd) != (n, d):
            if nn < dd or dd in (2, 3, 4):
                if nn <= 12:
                    try:
                        others.append(frac_words(nn, dd))
                    except (KeyError, IndexError):
                        pass

    def pad():
        dd = random.choice([2, 3, 4, 5, 6, 8, 10])
        return frac_words(random.randint(1, dd - 1), dd)
    return mc((f'Comment se lit la fraction **{frac(n, d)}** ?', f'How do you read the fraction **{frac(n, d)}**?'),
              words, others,
              ('Le numérateur se lit d’abord, puis le nom des parts donné par le dénominateur.',
               'Read the numerator first, then the name of the parts given by the denominator.'),
              ([f'{frac(n, d)} : {_parts(n)[0]} sur {d} → {words[0]}'], [f'{frac(n, d)}: {_parts(n)[1]} out of {d} → {words[1]}']),
              pad=pad)


# ── G3 · Numerator and denominator ───────────────────────────────────────────

def g3_numerator_denominator_gen(level='medium'):
    d = random.randint(3, 6) if level == 'easy' else random.randint(4, 10)
    n = random.randint(1, d - 1)
    variant = random.choice(['concept', 'picture_den', 'picture_num'] if level != 'hard' else ['concept', 'build'])
    if variant == 'concept':
        role = random.choice(['den', 'num'])
        right = (('le nombre de parts égales dans le tout', 'the number of equal parts in the whole') if role == 'den'
                 else ('le nombre de parts que l’on prend (coloriées)', 'the number of parts we take (coloured)'))
        wrong = [(('le nombre de parts que l’on prend (coloriées)', 'the number of parts we take (coloured)') if role == 'den'
                  else ('le nombre de parts égales dans le tout', 'the number of equal parts in the whole')),
                 ('le nombre de parts qui ne sont pas coloriées', 'the number of parts that are not coloured'),
                 ('la taille d’une part en centimètres', 'the size of one part in centimetres'),
                 ('la grandeur du tout', 'how big the whole is')]
        name = ('le dénominateur', 'the denominator') if role == 'den' else ('le numérateur', 'the numerator')
        return mc((f'Dans la fraction **{frac(n, d)}**, que représente {name[0]} **{d if role == "den" else n}** ?',
                   f'In the fraction **{frac(n, d)}**, what does {name[1]} **{d if role == "den" else n}** tell us?'),
                  right, wrong,
                  ('Le dénominateur est en bas, le numérateur en haut.', 'The denominator is at the bottom, the numerator on top.'),
                  ([f'{frac(n, d)} : le tout est partagé en {d} parts égales, on en prend {n}.'],
                   [f'{frac(n, d)}: the whole is split into {d} equal parts, we take {n}.']))
    if variant == 'build':
        return typed((f'Une fraction a pour numérateur **{n}** et pour dénominateur **{d}**. Écris-la.',
                      f'A fraction has numerator **{n}** and denominator **{d}**. Write it.'),
                     [frac(n, d)], 'fraction',
                     ('Numérateur en haut (avant la barre), dénominateur en bas.', 'Numerator on top (before the bar), denominator below.'),
                     ([f'{n} / {d} = {frac(n, d)}'], [f'{n} / {d} = {frac(n, d)}']))
    shape = ill.fraction_bars([(n, d)], color=ill.PURPLE)
    if variant == 'picture_den':
        return typed(('Quel est le **dénominateur** de la fraction coloriée ?', 'What is the **denominator** of the coloured fraction?'),
                     [d], 'integer',
                     ('Le dénominateur = le nombre total de parts égales.', 'The denominator = the total number of equal parts.'),
                     ([f'La bande a {d} parts égales → dénominateur {d}.'], [f'The strip has {d} equal parts → denominator {d}.']),
                     shape=shape)
    return typed(('Quel est le **numérateur** de la fraction coloriée ?', 'What is the **numerator** of the coloured fraction?'),
                 [n], 'integer',
                 ('Le numérateur = le nombre de parts coloriées.', 'The numerator = the number of coloured parts.'),
                 ([f'{_parts(n)[0]} {"sont coloriées" if n > 1 else "est coloriée"} → numérateur {n}.'],
                  [f'{_parts(n)[1]} {"are" if n > 1 else "is"} coloured → numerator {n}.']),
                 shape=shape)


# ── G4 · Compare to 0, ½ and 1 ───────────────────────────────────────────────

_BENCH = [('égale à 0', 'equal to 0'), ('entre 0 et ½', 'between 0 and ½'), ('égale à ½', 'equal to ½'),
          ('entre ½ et 1', 'between ½ and 1'), ('égale à 1', 'equal to 1'), ('plus grande que 1', 'greater than 1')]


def g4_fraction_benchmark_gen(level='medium'):
    if level == 'easy':
        d = random.choice([2, 4, 6, 8, 10])
        n = random.randint(1, d)
    elif level == 'medium':
        d = random.randint(3, 12)
        n = random.randint(1, d)
    else:
        d = random.randint(3, 12)
        n = random.randint(1, 2 * d)
    if level != 'hard' and random.random() < 0.1:
        n = 0
    f = Fraction(n, d)
    idx = 0 if n == 0 else 1 if f < Fraction(1, 2) else 2 if f == Fraction(1, 2) else 3 if f < 1 else 4 if f == 1 else 5
    shape = ill.fraction_bars([(n, d)]) if level == 'easy' and n <= d else None

    def cmp(x, y):
        return '<' if x < y else '=' if x == y else '>'
    if n == 0:
        steps_fr = [f'Le numérateur est 0 : on ne prend aucune part, donc {frac(n, d)} = 0.']
        steps_en = [f'The numerator is 0: no part is taken, so {frac(n, d)} = 0.']
    else:
        # ½ test without decimals: compare 2 × numerator with the denominator
        steps_fr = [f'Comparer à ½ : 2 × {n} = {2 * n} et {2 * n} {cmp(2 * n, d)} {d}, donc {frac(n, d)} {cmp(2 * n, d)} ½.',
                    f'Comparer à 1 : {n} {cmp(n, d)} {d}, donc {frac(n, d)} {cmp(n, d)} 1.']
        steps_en = [f'Compare with ½: 2 × {n} = {2 * n} and {2 * n} {cmp(2 * n, d)} {d}, so {frac(n, d)} {cmp(2 * n, d)} ½.',
                    f'Compare with 1: {n} {cmp(n, d)} {d}, so {frac(n, d)} {cmp(n, d)} 1.']
    steps_fr.append(f'{frac(n, d)} est {_BENCH[idx][0]}.')
    steps_en.append(f'{frac(n, d)} is {_BENCH[idx][1]}.')
    return mc((f'La fraction **{frac(n, d)}** est…', f'The fraction **{frac(n, d)}** is…'),
              _BENCH[idx], random.sample([b for i, b in enumerate(_BENCH) if i != idx], len(_BENCH) - 1),
              ('Compare le double du numérateur au dénominateur (pour ½), puis le numérateur au dénominateur (pour 1).',
               'Compare twice the numerator with the denominator (for ½), then the numerator with the denominator (for 1).'),
              (steps_fr, steps_en), shape=shape)


# ── G4 · Equivalent fractions ────────────────────────────────────────────────

def g4_equivalent_fractions_gen(level='medium'):
    d = random.choice([2, 3, 4, 5]) if level != 'hard' else random.choice([2, 3, 4, 5, 6, 8])
    n = random.choice([x for x in range(1, d) if Fraction(x, d).denominator == d])   # start irreducible
    k = random.randint(2, 3) if level == 'easy' else random.randint(2, 5)
    n2, d2 = n * k, d * k
    if level == 'easy':
        shape = ill.fraction_bars([(n, d), (n2, d2)], labels=['A', 'B'])
        distractors = [(frac(n + k, d + k), 'additive', 'Equivalent means multiplying top AND bottom by the same number.', 'Équivalent : on multiplie en haut ET en bas par le même nombre.'),
                       (frac(n2 + 1, d2), 'miscount', 'Count the coloured parts of strip B again.', 'Recompte les parts coloriées de la bande B.'),
                       (frac(n2 - 1, d2) if n2 > 1 else frac(n2 + 2, d2), 'miscount', 'Count the coloured parts of strip B again.', 'Recompte les parts coloriées de la bande B.'),
                       (frac(d2 - n2, d2), 'complement', 'Count the coloured parts, not the white ones.', 'Compte les parts coloriées, pas les blanches.')]
        return mc((f'La bande A montre **{frac(n, d)}**. Quelle fraction la bande B montre-t-elle ? Elles sont équivalentes.',
                   f'Strip A shows **{frac(n, d)}**. What fraction does strip B show? They are equivalent.'),
                  frac(n2, d2), _distinct_values(frac(n2, d2), distractors),
                  ('Compte les parts de la bande B : toutes, puis les coloriées.', 'Count the parts of strip B: all of them, then the coloured ones.'),
                  ([f'B : {n2} parts coloriées sur {d2}', f'{frac(n, d)} = {frac(n2, d2)} (× {k} en haut et en bas)'],
                   [f'B: {n2} coloured parts out of {d2}', f'{frac(n, d)} = {frac(n2, d2)} (× {k} top and bottom)']),
                  shape=shape, pad=_frac_pad(12, Fraction(n, d)))
    if level == 'medium' or random.random() < 0.5:
        missing_top = random.random() < 0.6
        prompt = ((f'Complète : **{frac(n, d)} = ?/{d2}**', f'Fill in: **{frac(n, d)} = ?/{d2}**') if missing_top
                  else (f'Complète : **{frac(n, d)} = {n2}/?**', f'Fill in: **{frac(n, d)} = {n2}/?**'))
        ans = n2 if missing_top else d2
        return typed(prompt, [ans], 'integer',
                     (f'Par combien multiplie-t-on {d if missing_top else n} pour obtenir {d2 if missing_top else n2} ?',
                      f'What do you multiply {d if missing_top else n} by to get {d2 if missing_top else n2}?'),
                     ([f'{d if missing_top else n} × {k} = {d2 if missing_top else n2}', f'{n if missing_top else d} × {k} = {ans}', f'{frac(n, d)} = {frac(n2, d2)}'],
                      [f'{d if missing_top else n} × {k} = {d2 if missing_top else n2}', f'{n if missing_top else d} × {k} = {ans}', f'{frac(n, d)} = {frac(n2, d2)}']))
    # hard: which is NOT equivalent
    eqs = [frac(n * j, d * j) for j in (2, 3, 4, 5)]
    odd = random.choice([frac(n * 2 + 1, d * 2), frac(n + 2, d + 2), frac(n * 3, d * 2)])
    if Fraction(odd) == Fraction(n, d):
        odd = frac(n * 2 + 1, d * 2)
    return mc((f'Laquelle de ces fractions n’est **pas** équivalente à **{frac(n, d)}** ?',
               f'Which of these fractions is **not** equivalent to **{frac(n, d)}**?'),
              odd, eqs,
              ('Simplifie chaque fraction, ou vérifie si le haut et le bas sont multipliés par le même nombre.',
               'Simplify each fraction, or check that top and bottom are multiplied by the same number.'),
              ([f'{e} = {frac(n, d)}' for e in eqs] + [f'{odd} ≠ {frac(n, d)}'],
               [f'{e} = {frac(n, d)}' for e in eqs] + [f'{odd} ≠ {frac(n, d)}']))


# ── G5 · Meanings of a fraction ──────────────────────────────────────────────

def g5_fraction_meanings_gen(level='medium'):
    variant = random.choice(['share', 'division', 'ratio'] if level != 'easy' else ['share', 'division'])
    who = random.choice(sc.ACTORS)[0]
    if variant == 'share':
        d = random.randint(3, 8)
        n = random.randint(2, d - 1) if level == 'easy' else random.randint(2, d + 3)
        if n == d:
            n += 1
        # (plural fr, plural en, « de … » after a fraction, "of a …")
        item = random.choice([('pizzas', 'pizzas', 'pizza', 'pizza'), ('tartes', 'pies', 'tarte', 'pie'),
                              ('tablettes de chocolat', 'chocolate bars', 'tablette de chocolat', 'chocolate bar')])

        def lab(a, b):
            return f'{frac(a, b)} de {item[2]}', f'{frac(a, b)} of a {item[3]}'

        def pad():
            while True:
                a, b = random.randint(1, 9), random.randint(2, 9)
                if Fraction(a, b) != Fraction(n, d):
                    return lab(a, b)
        distr = [(lab(d, n), 'swapped', 'The number shared goes on top.', 'Ce qu’on partage va en haut.'),
                 (lab(1, d), 'one_item', f'There are {n} items to share, not one.', f'Il y a {n} objets à partager, pas un seul.'),
                 (lab(1, n), 'swapped', 'Divide by the number of friends.', 'Divise par le nombre d’amis.'),
                 (lab(n, d + 1), 'off_by_one', 'Count the friends again.', 'Recompte les amis.'),
                 (lab(n, d - 1) if d - 1 > 1 else None, 'off_by_one', 'Count the friends again.', 'Recompte les amis.')]
        return mc((f'{who} partage **{n}** {item[0]} également entre **{d}** amis. Quelle part reçoit chaque ami ?',
                   f'{who} shares **{n}** {item[1]} equally among **{d}** friends. How much does each friend get?'),
                  lab(n, d), _distinct_values(lab(n, d), distr),
                  ('Partager n objets entre d personnes donne n/d à chacun.', 'Sharing n things among d people gives n/d each.'),
                  ([f'{n} ÷ {d} = {frac(n, d)}'], [f'{n} ÷ {d} = {frac(n, d)}']),
                  pad=pad)
    if variant == 'division':
        d = random.randint(2, 9)
        n = random.randint(1, 12)
        if n == d:
            n += 1
        return mc((f'Quelle division donne la fraction **{frac(n, d)}** ?', f'Which division gives the fraction **{frac(n, d)}**?'),
                  f'{n} ÷ {d}',
                  [(f'{d} ÷ {n}', 'swapped', 'The numerator is divided by the denominator.', 'On divise le numérateur par le dénominateur.'),
                   (f'{n} × {d}', 'wrong_operation', 'A fraction bar means "divided by".', 'La barre de fraction veut dire « divisé par ».'),
                   (f'{n} − {d}' if n > d else f'{d} − {n}', 'wrong_operation', 'A fraction bar means "divided by".', 'La barre de fraction veut dire « divisé par ».'),
                   (f'{n} + {d}', 'wrong_operation', 'A fraction bar means "divided by".', 'La barre de fraction veut dire « divisé par ».')],
                  ('La barre de fraction est un signe de division.', 'The fraction bar is a division sign.'),
                  ([f'{frac(n, d)} = {n} ÷ {d}'], [f'{frac(n, d)} = {n} ÷ {d}']))
    a, b = random.randint(1, 5), random.randint(1, 6)
    if a == b:
        b += 1
    kinds = random.choice([(('garçons', 'boys'), ('filles', 'girls'), ('élèves', 'students')),
                           (('billes rouges', 'red marbles'), ('billes bleues', 'blue marbles'), ('billes', 'marbles'))])
    return mc((f'Dans un groupe, il y a **{a}** {kinds[0][0]} pour **{b}** {kinds[1][0]}. Quelle fraction des {kinds[2][0]} sont des {kinds[0][0]} ?',
               f'In a group there are **{a}** {kinds[0][1]} for every **{b}** {kinds[1][1]}. What fraction of the {kinds[2][1]} are {kinds[0][1]}?'),
              frac(a, a + b),
              [(frac(a, b), 'part_part', 'Divide by the WHOLE group, not by the other part.', 'Divise par le groupe ENTIER, pas par l’autre partie.'),
               (frac(b, a + b), 'other_part', f'The question is about the {kinds[0][1]}.', f'La question porte sur les {kinds[0][0]}.'),
               (frac(b, a), 'swapped', 'Divide by the whole group.', 'Divise par le groupe entier.'),
               (frac(a + b, a), 'swapped', 'The part goes on top, the whole below.', 'La partie en haut, le tout en bas.')],
              ('Un groupe complet contient les deux sortes : additionne-les pour le dénominateur.',
               'One full group holds both kinds: add them for the denominator.'),
              ([f'Groupe : {a} + {b} = {a + b}', f'{kinds[0][0]} : {a} sur {a + b} = {frac(a, a + b)}'],
               [f'Group: {a} + {b} = {a + b}', f'{kinds[0][1]}: {a} out of {a + b} = {frac(a, a + b)}']))


# ── G5 · Order fractions with the same numerator ─────────────────────────────

def g5_order_same_numerator_gen(level='medium'):
    n = 1 if level == 'easy' else random.randint(2, 5)
    count = 4 if level == 'easy' else 5
    dens = sorted(random.sample([d for d in range(2, 13) if d != n], count))
    desc = level != 'easy' and random.random() < 0.5
    vals = sorted(dens, reverse=not desc)          # bigger denominator → smaller fraction
    labels = [frac(n, d) for d in vals]
    return ordering((f'Range ces fractions en ordre **{"décroissant" if desc else "croissant"}**.',
                     f'Sort these fractions in **{"descending" if desc else "ascending"}** order.'),
                    labels,
                    (f'Même numérateur ({n}) : plus il y a de parts, plus chaque part est petite.',
                     f'Same numerator ({n}): the more parts, the smaller each part.'),
                    ([(' > ' if desc else ' < ').join(labels)], [(' > ' if desc else ' < ').join(labels)]))


# ── G6 · Order fractions with related denominators ───────────────────────────

def g6_order_related_den_gen(level='medium'):
    # every denominator divides the largest one (audit: « le dénominateur de l'une étant un multiple de l'autre »)
    base = random.choice([2, 3, 4, 5])
    mults = random.choice([[1, 2, 4], [1, 3]] if base <= 3 else [[1, 2], [1, 3]] if level == 'hard' else [[1, 2]])
    big = base * max(mults)
    count = 4 if level == 'easy' else 5
    seen, fracs = set(), []
    while len(fracs) < count:
        d = base * random.choice(mults)
        n = random.randint(1, d - 1 if level != 'hard' else d + d // 2)
        v = Fraction(n, d)
        if v not in seen:
            seen.add(v)
            fracs.append((n, d))
    desc = random.random() < 0.4
    fracs.sort(key=lambda t: Fraction(*t), reverse=desc)
    labels = [frac(*t) for t in fracs]
    conv = [f'{frac(n, d)} = {frac(n * big // d, big)}' for n, d in fracs]
    return ordering((f'Range ces fractions en ordre **{"décroissant" if desc else "croissant"}**.',
                     f'Sort these fractions in **{"descending" if desc else "ascending"}** order.'),
                    labels,
                    (f'Écris-les toutes avec le dénominateur {big}, puis compare les numérateurs.',
                     f'Rewrite them all with denominator {big}, then compare the numerators.'),
                    (conv + [(' > ' if desc else ' < ').join(labels)], conv + [(' > ' if desc else ' < ').join(labels)]))


# ── G6 · Simplest form ───────────────────────────────────────────────────────

def g6_simplify_fraction_gen(level='medium'):
    while True:
        d0 = random.randint(2, 9 if level == 'easy' else 12)
        n0 = random.randint(1, d0 - 1)
        if Fraction(n0, d0).denominator == d0:
            break
    k = random.choice([2, 3, 5]) if level == 'easy' else random.choice([2, 3, 4, 6]) if level == 'medium' else random.choice([4, 6, 8, 9, 12])
    n, d = n0 * k, d0 * k
    if level == 'hard' and random.random() < 0.35:
        # Reducible fractions of DIFFERENT values and factors, so the key is not just « the one with numerator 1 ».
        wrong, why_fr, why_en, vals = [], [], [], {Fraction(n0, d0)}
        while len(wrong) < 4:
            b = random.randint(3, 12)
            a = random.randint(1, b - 1)
            j = random.choice([2, 3, 5])
            if Fraction(a, b).denominator != b or Fraction(a, b) in vals or a * j >= 100:
                continue
            vals.add(Fraction(a, b))
            wrong.append(frac(a * j, b * j))
            why_fr.append(f'{frac(a * j, b * j)} : {a * j} et {b * j} se divisent par {j}.')
            why_en.append(f'{frac(a * j, b * j)}: {a * j} and {b * j} are both divisible by {j}.')
        return mc(('Laquelle de ces fractions est **irréductible** (déjà à sa plus simple expression) ?',
                   'Which of these fractions is in **simplest form**?'),
                  frac(n0, d0), wrong,
                  ('Irréductible : le numérateur et le dénominateur n’ont aucun diviseur commun sauf 1.',
                   'Simplest form: top and bottom share no factor except 1.'),
                  (why_fr + [f'{frac(n0, d0)} : seul diviseur commun 1'], why_en + [f'{frac(n0, d0)}: only common factor is 1']))
    half_k = next((j for j in (2, 3, 5) if k % j == 0 and j < k), None)
    distractors = [
        (frac(n // half_k, d // half_k), 'not_finished', 'You can still simplify: keep dividing.', 'Tu peux encore simplifier : continue de diviser.') if half_k else None,
        (frac(n0, d), 'one_term', 'Divide the top AND the bottom by the same number.', 'Divise le haut ET le bas par le même nombre.'),
        (frac(n, d0), 'one_term', 'Divide the top AND the bottom by the same number.', 'Divise le haut ET le bas par le même nombre.'),
        (frac(n - k, d - k), 'subtracted', 'Simplifying means dividing, not subtracting.', 'Simplifier, c’est diviser, pas soustraire.') if n > k else None,
        (frac(d0, n0) if n0 > 0 else None, 'swapped', 'Keep the numerator on top.', 'Garde le numérateur en haut.'),
        (frac(n0 * 2, d0 * 2), 'not_finished', 'You can still simplify: keep dividing.', 'Tu peux encore simplifier : continue de diviser.') if k > 2 else None,
    ]
    return mc((f'Réduis **{frac(n, d)}** à sa plus simple expression.', f'Write **{frac(n, d)}** in simplest form.'),
              frac(n0, d0), distractors,
              (f'Cherche le plus grand nombre qui divise {n} et {d}.', f'Find the greatest number that divides both {n} and {d}.'),
              ([f'{n} ÷ {k} = {n0} et {d} ÷ {k} = {d0}', f'{frac(n, d)} = {frac(n0, d0)}'],
               [f'{n} ÷ {k} = {n0} and {d} ÷ {k} = {d0}', f'{frac(n, d)} = {frac(n0, d0)}']),
              pad=lambda: random.choice([frac(n0 + 1, d0), frac(n0, d0 + 1), frac(n0 + 1, d0 + 1), frac(n0 * 2, d0),
                                         frac(n // 2, d) if n % 2 == 0 else frac(n, d // 2 + 1)]))


# ── G6 · Add / subtract with related denominators ────────────────────────────

def g6_fraction_add_related_gen(level='medium'):
    d1 = random.choice([2, 3, 4, 5]) if level != 'hard' else random.choice([3, 4, 5, 6])
    k = random.choice([2, 3]) if level == 'easy' else random.choice([2, 3, 4])
    d2 = d1 * k
    a = random.randint(1, d1 - 1)
    b = random.randint(1, d2 - 1)
    sub = level != 'easy' and random.random() < 0.5
    if sub and Fraction(a, d1) == Fraction(b, d2):
        sub = False
    big_first = Fraction(a, d1) > Fraction(b, d2)
    if sub and not big_first:
        left, right = (b, d2), (a, d1)
    else:
        left, right = (a, d1), (b, d2)
    if random.random() < 0.5 and not sub:
        left, right = right, left
    op = '−' if sub else '+'
    res = Fraction(*left) - Fraction(*right) if sub else Fraction(*left) + Fraction(*right)
    ln, ld = left[0] * (d2 // left[1]), d2
    rn = right[0] * (d2 // right[1])
    raw = frac(ln - rn if sub else ln + rn, d2)
    answers = list(dict.fromkeys([simplest(res.numerator, res.denominator), raw]))
    return typed((f'Calcule : **{frac(*left)} {op} {frac(*right)}**', f'Calculate: **{frac(*left)} {op} {frac(*right)}**'),
                 answers, 'fraction',
                 (f'{d2} est un multiple de {d1} : écris les deux fractions en {d2}es.',
                  f'{d2} is a multiple of {d1}: write both fractions in {d2}ths.'),
                 ([f'{frac(*left)} = {frac(ln, ld)}', f'{frac(*right)} = {frac(rn, d2)}', f'{frac(ln, ld)} {op} {frac(rn, d2)} = {raw}']
                  + ([f'{raw} = {answers[0]} (simplifiée)'] if answers[0] != raw else []) + [f'Réponse : {answers[0]}'],
                  [f'{frac(*left)} = {frac(ln, ld)}', f'{frac(*right)} = {frac(rn, d2)}', f'{frac(ln, ld)} {op} {frac(rn, d2)} = {raw}']
                  + ([f'{raw} = {answers[0]} (simplified)'] if answers[0] != raw else []) + [f'Answer: {answers[0]}']))


# ── G6 · Whole number × fraction ─────────────────────────────────────────────

def g6_whole_times_fraction_gen(level='medium'):
    variant = random.choice(['times', 'of'] if level != 'hard' else ['of', 'story'])
    d = random.randint(2, 8)
    n = random.randint(1, d - 1)
    if variant == 'times':
        w = random.randint(2, 6)
        res = Fraction(w * n, d)
        simp = simplest(res.numerator, res.denominator)
        tail = [f'{frac(w * n, d)} = {simp}'] if simp != frac(w * n, d) else []
        return typed((f'Calcule : **{w} × {frac(n, d)}**', f'Calculate: **{w} × {frac(n, d)}**'),
                     list(dict.fromkeys([frac(w * n, d), simp])), 'fraction',
                     (f'{w} × {frac(n, d)} = {frac(n, d)} + {frac(n, d)} + … ({w} fois) : multiplie seulement le numérateur.',
                      f'{w} × {frac(n, d)} = {frac(n, d)} + {frac(n, d)} + … ({w} times): multiply only the numerator.'),
                     ([f'{w} × {n} = {w * n}', f'{w} × {frac(n, d)} = {frac(w * n, d)}'] + tail,
                      [f'{w} × {n} = {w * n}', f'{w} × {frac(n, d)} = {frac(w * n, d)}'] + tail))
    k = random.randint(2, 6 if level == 'easy' else 9)
    total = d * k
    part = n * k
    if variant == 'of':
        return typed((f'Combien font **{frac(n, d)} de {total}** ?', f'What is **{frac(n, d)} of {total}**?'),
                     [part], 'integer',
                     (f'Trouve d’abord {frac(1, d)} de {total} ({total} ÷ {d}), puis multiplie par {n}.',
                      f'First find {frac(1, d)} of {total} ({total} ÷ {d}), then multiply by {n}.'),
                     ([f'{total} ÷ {d} = {k}', f'{k} × {n} = {part}'], [f'{total} ÷ {d} = {k}', f'{k} × {n} = {part}']))
    who, g = random.choice(sc.ACTORS)
    obj = random.choice([('autocollants', 'stickers'), ('billes', 'marbles'), ('cartes', 'cards'), ('images', 'pictures')])
    return typed((f'{who} a **{total}** {obj[0]}. {sc.pronoun_fr(g).capitalize()} en donne **{frac(n, d)}** à un ami. Combien lui en reste-t-il ?',
                  f'{who} has **{total}** {obj[1]} and gives **{frac(n, d)}** of them to a friend. How many are left?'),
                 [total - part], 'integer',
                 ('Calcule la fraction de la quantité, puis lis bien la question.', 'Work out the fraction of the amount, then read the question carefully.'),
                 ([f'{total} ÷ {d} = {k}', f'{k} × {n} = {part}', f'{total} − {part} = {total - part}'],
                  [f'{total} ÷ {d} = {k}', f'{k} × {n} = {part}', f'{total} − {part} = {total - part}']))
