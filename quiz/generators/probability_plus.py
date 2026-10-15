"""
probability_plus.py — curriculum upgrade WP8 (probability), 2026-10.

Equally likely outcomes, comparing likelihoods, independence of trials,
variability, the 0–1 probability line, tree diagrams, experiments vs theory
(simulated in the generator), and listing the outcomes of a simple experiment.
"""
import random
from fractions import Fraction

from quiz import illustrations as I
from .kit import mc, typed, pick

L5 = list('ABCDE')
COLS = {'rouge': ('red', '#EF4444'), 'bleu': ('blue', '#3B82F6'), 'vert': ('green', '#22C55E'), 'jaune': ('yellow', '#FACC15')}
FEM_FR = {'rouge': 'rouge', 'bleu': 'bleue', 'vert': 'verte', 'jaune': 'jaune'}


def hexof(name):
    return COLS[name][1]


def en(name):
    return COLS[name][0]


def _letters(prompt, i, hint, explanation, shape):
    return mc(prompt, L5[i], [x for x in L5 if x != L5[i]], hint, explanation, shape=shape)


# ── G3 · Equally likely ──────────────────────────────────────────────────────

def g3_equally_likely_gen(level='easy'):
    """Recognise equally likely outcomes: spinners, bags, fair objects (222)."""
    a, b = random.sample(list(COLS), 2)
    if level == 'easy':
        good = [a, b] * random.choice([1, 2, 3])
        # wrong spinners are clearly unequal (at least 2 : 1) so the answer is visible at a glance
        bads = [[a, a, a, b], [(a, 3), (b, 1)], [a, b, b], [(a, 1), (b, 2)], [(a, 1), (b, 3)], [a, a, b, a, a, b]]
        spins = [good] + random.sample(bads, 4)
        order = list(range(5))
        random.shuffle(order)
        c, boxes = I.panels(5, 100, 100)
        for j, box in zip(order, boxes):
            I.draw_spinner(c, box, [(hexof(s[0]), s[1]) if isinstance(s, tuple) else hexof(s) for s in spins[j]])
        i = order.index(0)
        return _letters((f'Sur quelle roulette le {a} et le {b} ont-ils **autant de chances** de sortir ?',
                         f'On which spinner do {en(a)} and {en(b)} have **the same chance**?'), i,
                        ('Compare la place occupée par chaque couleur : elles doivent couvrir la même surface.',
                         'Compare how much room each colour takes: they must cover the same amount.'),
                        (f'Roulette {L5[i]} : le {a} et le {b} couvrent chacun la moitié.', f'Spinner {L5[i]}: {en(a)} and {en(b)} each cover half.'),
                        c.shape())
    if level == 'medium':
        n = random.randint(2, 5)
        good = [(hexof(a), n), (hexof(b), n)]
        bads = [[(hexof(a), n + 1), (hexof(b), n)], [(hexof(a), n), (hexof(b), n + 2)], [(hexof(a), 2 * n), (hexof(b), n)],
                [(hexof(a), n - 1 if n > 2 else n + 3), (hexof(b), n + 1)], [(hexof(a), 1), (hexof(b), n + 1)]]
        bags = [good] + random.sample(bads, 4)
        order = list(range(5))
        random.shuffle(order)
        c, boxes = I.panels(5, 100, 100)
        for j, box in zip(order, boxes):
            I.draw_bag(c, box, bags[j])
        i = order.index(0)
        return _letters((f'On tire une bille sans regarder. Dans quel sac a-t-on autant de chances de tirer une bille {FEM_FR[a]} qu’une bille {FEM_FR[b]} ?',
                         f'You pick a marble without looking. Which bag gives the same chance of {en(a)} and {en(b)}?'), i,
                        ('Compte les billes de chaque couleur : il en faut autant.', 'Count the marbles of each colour: there must be the same number.'),
                        (f'Sac {L5[i]} : {n} billes {FEM_FR[a]}s et {n} billes {FEM_FR[b]}s.', f'Bag {L5[i]}: {n} {en(a)} and {n} {en(b)} marbles.'),
                        c.shape())
    correct = pick([('un dé à 6 faces bien équilibré (quel nombre sort)', 'a fair six-sided die (which number comes up)'),
                    ('une pièce de monnaie (pile ou face)', 'a coin (heads or tails)'),
                    ('un cube dont chaque face a une couleur différente', 'a cube with a different colour on each face')])
    wrong = [('une punaise lancée (pointe en haut ou en bas)', 'a thumbtack tossed (point up or down)'),
             ('un prisme rectangulaire très allongé (sur quelle face il tombe)', 'a long rectangular prism (which face it lands on)'),
             ('une roulette dont le rouge occupe les trois quarts', 'a spinner that is three-quarters red'),
             ('un sac avec 5 billes rouges et 1 bleue', 'a bag with 5 red marbles and 1 blue'),
             ('un verre en plastique lancé (debout, à l’envers ou couché)', 'a plastic cup tossed (upright, upside down or on its side)')]
    return mc(('Avec quel objet chaque résultat a-t-il **la même chance** (équiprobabilité) ?',
               'With which object does every result have **the same chance** (equally likely)?'),
              correct, wrong,
              ('Les résultats sont équiprobables quand l’objet est symétrique ou que chaque possibilité occupe la même place.',
               'Outcomes are equally likely when the object is symmetrical or every possibility takes the same room.'),
              (f'{correct[0].capitalize()} : chaque résultat a la même chance, grâce à sa symétrie.',
               f'{correct[1].capitalize()}: every result has the same chance, thanks to its symmetry.'))


# ── G4 · Compare likelihoods ─────────────────────────────────────────────────

def g4_compare_likelihood_gen(level='easy'):
    """More / less / equally likely; compare two bags (226, 231)."""
    if level == 'easy':
        a, b, c3 = random.sample(list(COLS), 3)
        na, nb = random.choice([(3, 1), (1, 3), (2, 2), (4, 2), (2, 4), (3, 3), (5, 1), (1, 2)])
        sectors = [a] * na + [b] * nb + [c3]
        random.shuffle(sectors)
        if na > nb:
            k = 0
        elif na < nb:
            k = 1
        else:
            k = 2
        opts = [(f'Le {a} est plus probable que le {b}.', f'{en(a).capitalize()} is more likely than {en(b)}.'),
                (f'Le {a} est moins probable que le {b}.', f'{en(a).capitalize()} is less likely than {en(b)}.'),
                (f'Le {a} et le {b} sont également probables.', f'{en(a).capitalize()} and {en(b)} are equally likely.'),
                (f'Le {a} est impossible.', f'{en(a).capitalize()} is impossible.'),
                (f'Le {b} est certain.', f'{en(b).capitalize()} is certain.')]
        correct = opts[k]
        return mc(('Les parts de cette roulette sont toutes de la même taille. Que peut-on dire ?',
                   'All the parts of this spinner are the same size. What can we say?'),
                  correct, [o for j, o in enumerate(opts) if j != k],
                  ('Compte les parts de chaque couleur.', 'Count the parts of each colour.'),
                  (f'{na} part{"s" if na > 1 else ""} {a}, {nb} part{"s" if nb > 1 else ""} {b} : {correct[0][0].lower()}{correct[0][1:]}',
                   f'{na} {en(a)} part{"s" if na > 1 else ""}, {nb} {en(b)} part{"s" if nb > 1 else ""}: {correct[1][0].lower()}{correct[1][1:]}'),
                  shape=I.spinner([hexof(s) for s in sectors]))
    if level == 'medium':
        names = random.sample(list(COLS), 3)
        counts = random.sample(range(1, 8), 3)
        best = names[counts.index(max(counts))]
        bag = I.bag([(hexof(n), c) for n, c in zip(names, counts)])
        left = [x for x in COLS if x not in names]
        opts = [(f'une bille {FEM_FR[n]}', f'a {en(n)} marble') for n in names] + \
               [(f'une bille {FEM_FR[left[0]]}', f'a {en(left[0])} marble'), ('toutes les couleurs ont la même chance', 'all colours have the same chance')]
        correct = (f'une bille {FEM_FR[best]}', f'a {en(best)} marble')
        return mc(('On tire une bille sans regarder. Quel résultat est **le plus probable** ?', 'You pick a marble without looking. Which result is **most likely**?'),
                  correct, [o for o in opts if o != correct],
                  ('La couleur qui a le plus de billes a le plus de chances.', 'The colour with the most marbles has the best chance.'),
                  (f'Il y a {max(counts)} billes {FEM_FR[best]}s : c’est la couleur la plus nombreuse.', f'There are {max(counts)} {en(best)} marbles: the largest number.'),
                  shape=bag)
    # hard — which bag gives the better chance of red?
    pairs = [((2, 3), (3, 6)), ((3, 4), (4, 8)), ((1, 4), (2, 4)), ((2, 5), (4, 10)), ((3, 5), (5, 10)), ((1, 3), (2, 6)),
             ((2, 4), (3, 6)), ((4, 5), (6, 10)), ((1, 2), (3, 8))]
    (ra, ta), (rb, tb) = pick(pairs)
    if random.random() < 0.5:
        (ra, ta), (rb, tb) = (rb, tb), (ra, ta)
    pa, pb = Fraction(ra, ta), Fraction(rb, tb)
    k = 0 if pa > pb else 1 if pb > pa else 2
    opts = [('Le sac A', 'Bag A'), ('Le sac B', 'Bag B'), ('Les deux sacs donnent la même chance', 'Both bags give the same chance'),
            ('Aucun : on ne peut jamais tirer de rouge', 'Neither: red can never be picked'), ('Le sac qui a le plus de billes', 'The bag with more marbles')]
    c, boxes = I.panels(2, 140, 130)
    I.draw_bag(c, boxes[0], [(hexof('rouge'), ra), (hexof('bleu'), ta - ra)])
    I.draw_bag(c, boxes[1], [(hexof('rouge'), rb), (hexof('bleu'), tb - rb)])
    return mc(('Dans quel sac a-t-on **la meilleure chance** de tirer une bille rouge ?', 'Which bag gives **the better chance** of picking a red marble?'),
              opts[k], [o for j, o in enumerate(opts) if j != k],
              ('Compare la fraction de billes rouges dans chaque sac, pas seulement leur nombre.', 'Compare the fraction of red marbles in each bag, not just how many.'),
              (f'Sac A : {ra}/{ta} ; sac B : {rb}/{tb}. ' + ('Le sac A l’emporte.' if k == 0 else 'Le sac B l’emporte.' if k == 1 else 'Les deux fractions sont égales.'),
               f'Bag A: {ra}/{ta}; bag B: {rb}/{tb}. ' + ('Bag A wins.' if k == 0 else 'Bag B wins.' if k == 1 else 'Both fractions are equal.')),
              shape=c.shape())


# ── G4 · Independence of trials ──────────────────────────────────────────────

def g4_independence_gen(level='easy'):
    """Each new trial ignores the earlier ones (223)."""
    name = pick(['Léa', 'Samuel', 'Inès', 'Noah', 'Maya', 'Félix'])
    k = random.randint(3, 6)
    setups = [
        ((f'{name} lance une pièce de monnaie {k} fois de suite et obtient **pile** chaque fois. Au lancer suivant…',
          f'{name} tosses a coin {k} times in a row and gets **heads** every time. On the next toss…'),
         ('pile et face ont toujours autant de chances', 'heads and tails still have the same chance'),
         [('face a plus de chances, c’est son tour', 'tails is more likely, it is its turn'),
          ('pile a plus de chances, la pièce est lancée', 'heads is more likely, it is on a streak'),
          ('face est certain', 'tails is certain'), ('pile est impossible', 'heads is impossible')]),
        ((f'{name} lance un dé équilibré {k * 2} fois et n’obtient jamais de 6. Au lancer suivant, le 6…',
          f'{name} rolls a fair die {k * 2} times and never gets a 6. On the next roll, a 6…'),
         ('a toujours 1 chance sur 6', 'still has a 1 in 6 chance'),
         [('est plus probable, il doit bientôt sortir', 'is more likely, it is due'), ('est certain', 'is certain'),
          ('est impossible, le dé ne fait pas de 6', 'is impossible, the die does not roll 6s'), ('a 1 chance sur 2', 'has a 1 in 2 chance')]),
        ((f'Une roulette a 2 parts égales, rouge et bleue. Elle s’arrête {k} fois de suite sur le rouge. Au tour suivant…',
          f'A spinner has 2 equal parts, red and blue. It lands on red {k} times in a row. On the next spin…'),
         ('le rouge et le bleu ont toujours autant de chances', 'red and blue still have the same chance'),
         [('le bleu est plus probable', 'blue is more likely'), ('le rouge est plus probable', 'red is more likely'),
          ('le bleu est certain', 'blue is certain'), ('la roulette est sûrement brisée', 'the spinner must be broken')]),
        ((f'Un sac contient 1 bille rouge et 1 bille bleue. {name} tire une bille, la regarde, puis **la remet** dans le sac. Elle a tiré la rouge {k} fois. Au tirage suivant…',
          f'A bag holds 1 red and 1 blue marble. {name} picks one, looks, then **puts it back**. Red came out {k} times. On the next pick…'),
         ('rouge et bleu ont toujours autant de chances', 'red and blue still have the same chance'),
         [('le bleu est plus probable', 'blue is more likely'), ('le rouge est plus probable', 'red is more likely'),
          ('le bleu est certain', 'blue is certain'), ('le rouge est impossible', 'red is impossible')]),
    ]
    if level == 'hard' and random.random() < 0.5:
        # contrast: without putting back, the chances DO change
        r = random.randint(3, 5)
        return mc((f'Un sac contient {r} billes rouges et {r} billes bleues. {name} tire une bille rouge et **ne la remet pas**. Au tirage suivant…',
                   f'A bag holds {r} red and {r} blue marbles. {name} picks a red marble and **does not put it back**. On the next pick…'),
                  ('le bleu est maintenant un peu plus probable', 'blue is now a little more likely'),
                  [('rouge et bleu ont toujours autant de chances', 'red and blue still have the same chance'),
                   ('le rouge est maintenant plus probable', 'red is now more likely'),
                   ('le bleu est certain', 'blue is certain'), ('le rouge est impossible', 'red is impossible')],
                  ('Sans remise, le contenu du sac change : recompte les billes.', 'Without putting back, the bag changes: count the marbles again.'),
                  (f'Il reste {r - 1} rouges et {r} bleues : le bleu a un peu plus de chances.',
                   f'There are {r - 1} red and {r} blue left: blue has a slightly better chance.'))
    prompt, right, wrong = pick(setups[:2] if level == 'easy' else setups)
    return mc(prompt, right, wrong,
              ('La pièce, le dé ou la roulette ne se souviennent pas des tours précédents.', 'The coin, die or spinner does not remember earlier turns.'),
              (f'Chaque tour est indépendant : {right[0]}.', f'Each turn is independent: {right[1]}.'))


# ── G4 · Variability ─────────────────────────────────────────────────────────

def g4_variability_gen(level='easy'):
    """Results of a chance experiment vary (221)."""
    n = random.choice([20, 24, 25, 30])
    t = random.choice([10, 12, 20])
    items = [
        ((f'Les {n} élèves d’une classe lancent chacun un dé {t} fois et comptent leurs 6. Que va-t-il se passer ?',
          f'Each of the {n} students in a class rolls a die {t} times and counts the 6s. What will happen?'),
         ('Les élèves n’auront pas tous le même nombre de 6.', 'Students will not all get the same number of 6s.'),
         [('Tous les élèves auront exactement le même nombre de 6.', 'Every student will get exactly the same number of 6s.'),
          (f'Chaque élève aura exactement {t // 6 if t % 6 == 0 else 2} six.', f'Every student will get exactly {t // 6 if t % 6 == 0 else 2} sixes.'),
          ('Personne n’aura de 6.', 'Nobody will get a 6.'), ('Tout le monde n’aura que des 6.', 'Everyone will get only 6s.')]),
        ((f'Tu lances une pièce {t} fois. Lequel de ces résultats est **possible** ?', f'You toss a coin {t} times. Which of these results is **possible**?'),
         (f'{t // 2 + 2} piles et {t - t // 2 - 2} faces', f'{t // 2 + 2} heads and {t - t // 2 - 2} tails'),
         [(f'{t + 1} piles', f'{t + 1} heads'), (f'{t // 2} piles et {t // 2 + 3} faces', f'{t // 2} heads and {t // 2 + 3} tails'),
          (f'{t} piles et {t} faces', f'{t} heads and {t} tails'), ('0 pile et 0 face', '0 heads and 0 tails')]),
        ((f'Lucas et Zoé tournent chacun la même roulette (moitié rouge, moitié bleue) {t} fois. Lucas obtient {t // 2 + 1} rouges. Zoé…',
          f'Lucas and Zoé each spin the same spinner (half red, half blue) {t} times. Lucas gets {t // 2 + 1} reds. Zoé…'),
         ('peut obtenir un autre nombre de rouges', 'may get a different number of reds'),
         [(f'obtiendra sûrement {t // 2 + 1} rouges aussi', f'will surely get {t // 2 + 1} reds too'),
          (f'obtiendra sûrement exactement {t // 2} rouges', f'will surely get exactly {t // 2} reds'),
          ('ne peut pas obtenir de rouge', 'cannot get any red'), ('obtiendra seulement du bleu', 'will get only blue')]),
    ]
    prompt, right, wrong = pick(items[:2] if level == 'easy' else items)
    return mc(prompt, right, wrong,
              ('Le hasard fait varier les résultats d’une fois à l’autre, mais certains résultats restent impossibles.',
               'Chance makes results vary from one time to the next, but some results stay impossible.'),
              (f'{right[0]} Le hasard fait varier les résultats.', f'{right[1]} Chance makes results vary.'))


# ── G5 · The 0–1 probability line ────────────────────────────────────────────

def g5_probability_line_gen(level='easy'):
    """A probability lies between 0 and 1: place an event on the line (232, 225)."""
    spots = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)] if level != 'hard' else \
            [Fraction(0), Fraction(1, 5), Fraction(1, 2), Fraction(4, 5), Fraction(1)]
    p = pick(spots)
    total = p.denominator * random.choice([1, 2]) if p not in (0, 1) else random.choice([4, 5, 6])
    red = int(p * total)
    other = pick(['bleu', 'vert', 'jaune'])
    contents = [(hexof('rouge'), red), (hexof(other), total - red)]
    word = {Fraction(0): ('impossible', 'impossible'), Fraction(1): ('certain', 'certain'),
            Fraction(1, 2): ('une chance sur deux', 'an even chance')}.get(p, ('peu probable' if p < Fraction(1, 2) else 'très probable',
                                                                              'unlikely' if p < Fraction(1, 2) else 'very likely'))
    i = spots.index(p)
    pics = [I.bag([c for c in contents if c[1]]), I.prob_line([(float(v), L5[k]) for k, v in enumerate(spots)])]
    return _letters(('On tire une bille sans regarder. Où places-tu l’événement « tirer une bille rouge » sur la droite des probabilités ?',
                     'You pick a marble without looking. Where does the event “picking a red marble” go on the probability line?'), i,
                    ('0 = impossible, 1 = certain, ½ = une chance sur deux. Compare le nombre de billes rouges au nombre total.',
                     '0 = impossible, 1 = certain, ½ = an even chance. Compare the red marbles with the total.'),
                    (f'{red} rouge{"s" if red > 1 else ""} sur {total} : probabilité {red}/{total} → point {L5[i]} ({word[0]}).',
                     f'{red} red out of {total}: probability {red}/{total} → point {L5[i]} ({word[1]}).'),
                    pics)


# ── G5 · Tree diagrams ───────────────────────────────────────────────────────

TREES = [
    ((('pile', 'heads'), ('face', 'tails')), [(str(k), str(k)) for k in range(1, 7)],
     ('On lance une pièce, puis un dé.', 'You toss a coin, then roll a die.')),
    ((('chandail rouge', 'red top'), ('chandail bleu', 'blue top'), ('chandail vert', 'green top')),
     [('jupe', 'skirt'), ('short', 'shorts'), ('pantalon', 'trousers')],
     ('Mia choisit un chandail, puis un bas.', 'Mia picks a top, then a bottom.')),
    ((('pâtes', 'pasta'), ('pizza', 'pizza')), [('pomme', 'apple'), ('yogourt', 'yogurt'), ('biscuit', 'cookie'), ('raisins', 'grapes')],
     ('Au dîner, on choisit un plat, puis un dessert.', 'At lunch you pick a main, then a dessert.')),
    ((('rouge', 'red'), ('bleu', 'blue')), [('A', 'A'), ('B', 'B'), ('C', 'C')],
     ('On tourne une roulette rouge/bleu, puis on tire une carte A, B ou C.', 'You spin a red/blue spinner, then draw card A, B or C.')),
]


def g5_tree_diagram_gen(level='easy'):
    """Count outcomes with a tree diagram (230)."""
    first, second, story = pick(TREES)
    if level == 'easy':
        n = len(first) * len(second)
        return typed((f'{story[0]} Combien de résultats possibles y a-t-il en tout ?', f'{story[1]} How many possible outcomes are there in all?'),
                     [n], 'integer',
                     ('Compte les bouts de branches à droite de l’arbre.', 'Count the branch ends on the right of the tree.'),
                     (f'{len(first)} × {len(second)} = {n} résultats', f'{len(first)} × {len(second)} = {n} outcomes'),
                     shape=I.tree_diagram(first, second))
    if level == 'medium':
        i, j = random.randrange(len(first)), random.randrange(len(second))
        return mc((f'{story[0]} Une étiquette de l’arbre est cachée. Laquelle manque ?', f'{story[1]} One label of the tree is hidden. Which one is missing?'),
                  second[j], [s for s in second if s != second[j]] + [first[0], first[-1]] + [('rien', 'nothing')],
                  ('Chaque branche du premier choix porte les mêmes possibilités au deuxième choix.', 'Every first-choice branch carries the same second-choice options.'),
                  (f'Les autres branches montrent {", ".join(s[0] for s in second)} : il manque « {second[j][0]} ».',
                   f'The other branches show {", ".join(s[1] for s in second)}: “{second[j][1]}” is missing.'),
                  shape=I.tree_diagram(first, second, hide=(i, j)))
    a, b, c = random.randint(2, 4), random.randint(2, 5), random.randint(2, 3)
    if random.random() < 0.5:
        return typed((f'Un restaurant propose {a} entrées, {b} plats et {c} desserts. Combien de repas différents (une entrée, un plat, un dessert) peut-on composer ?',
                      f'A restaurant offers {a} starters, {b} mains and {c} desserts. How many different meals (one of each) can you make?'),
                     [a * b * c], 'integer',
                     ('Imagine un arbre à trois étages : multiplie le nombre de choix à chaque étage.', 'Picture a three-level tree: multiply the number of choices at each level.'),
                     (f'{a} × {b} × {c} = {a * b * c}', f'{a} × {b} × {c} = {a * b * c}'))
    return typed((f'On lance une pièce, puis on tire une carte parmi {b + 2} cartes numérotées. Combien de résultats possibles ?',
                  f'You toss a coin, then draw one of {b + 2} numbered cards. How many possible outcomes?'),
                 [2 * (b + 2)], 'integer',
                 ('Chaque côté de la pièce peut aller avec chaque carte.', 'Each side of the coin can go with each card.'),
                 (f'2 × {b + 2} = {2 * (b + 2)}', f'2 × {b + 2} = {2 * (b + 2)}'))


# ── G5 · Experiments, predictions and theory (simulated here) ────────────────

def _spin(weights, n):
    names = list(weights)
    return [random.choices(names, weights=[weights[k] for k in names])[0] for _ in range(n)]


def g5_simulation_gen(level='easy'):
    """Prediction vs result, record results, experimental vs theoretical (224, 227, 228, 234, 235)."""
    if level == 'easy':
        t = random.choice([10, 20])
        got = random.choice([x for x in range(t // 2 - 3, t // 2 + 4) if x != t // 2])
        return mc((f'Avant de lancer une pièce {t} fois, Jade prédit {t // 2} piles. Elle obtient {got} piles. Que peut-on dire ?',
                   f'Before tossing a coin {t} times, Jade predicts {t // 2} heads. She gets {got} heads. What can we say?'),
                  ('Un résultat peut être différent de la prédiction : c’est le hasard.', 'A result can differ from the prediction: that is chance.'),
                  [('La pièce est sûrement truquée.', 'The coin must be rigged.'), ('Jade a sûrement mal compté.', 'Jade must have counted wrong.'),
                   (f'Il fallait obtenir exactement {t // 2} piles.', f'She had to get exactly {t // 2} heads.'),
                   ('Sa prédiction était impossible.', 'Her prediction was impossible.')],
                  ('Une prédiction dit ce qui est le plus probable, pas ce qui arrivera à coup sûr.', 'A prediction says what is most likely, not what will surely happen.'),
                  (f'{got} piles au lieu de {t // 2} : un petit écart est normal avec le hasard.', f'{got} heads instead of {t // 2}: a small gap is normal with chance.'))
    if level == 'medium':
        colors = random.sample(list(COLS), 3)
        weights = dict(zip(colors, random.choice([(2, 1, 1), (1, 1, 1), (3, 2, 1)])))
        n = random.choice([20, 30, 40])
        res = _spin(weights, n)
        counts = [res.count(k) for k in colors]
        cats = [(k, en(k)) for k in colors]
        chart = I.bar_chart(cats, counts, color=[hexof(k) for k in colors], step=2 if max(counts) <= 16 else 5)
        i = random.randrange(3)
        if random.random() < 0.5:
            return typed((f'On a fait tourner une roulette {n} fois et noté les résultats dans ce diagramme. Combien de fois est sorti le {colors[i]} ?',
                          f'A spinner was spun {n} times and the results recorded in this chart. How many times did {en(colors[i])} come up?'),
                         [counts[i]], 'integer',
                         ('Lis la hauteur de la bande sur l’axe.', 'Read the height of the bar on the axis.'),
                         (f'La bande {colors[i]} monte jusqu’à {counts[i]}.', f'The {en(colors[i])} bar reaches {counts[i]}.'), shape=chart)
        f = Fraction(counts[i], n)
        return typed((f'On a fait tourner une roulette {n} fois (voir le diagramme). Quelle fraction des tours a donné le {colors[i]} ? (Écris a/b)',
                      f'A spinner was spun {n} times (see the chart). What fraction of the spins gave {en(colors[i])}? (Write a/b)'),
                     [f'{counts[i]}/{n}', f'{f.numerator}/{f.denominator}'], 'fraction',
                     ('Probabilité fréquentielle = nombre de fois / nombre total de tours.', 'Experimental probability = number of times ÷ total spins.'),
                     (f'{counts[i]} fois sur {n} : {counts[i]}/{n}', f'{counts[i]} times out of {n}: {counts[i]}/{n}'), shape=chart)
    if random.random() < 0.5:
        t = random.choice([12, 18, 24, 30, 60, 120])
        face = random.randint(1, 6)
        return typed((f'On lance un dé équilibré {t} fois. Combien de fois peut-on **s’attendre** à obtenir un {face} ?',
                      f'A fair die is rolled {t} times. How many times can you **expect** to roll a {face}?'),
                     [t // 6], 'integer',
                     ('Probabilité théorique d’une face : 1 sur 6.', 'Theoretical probability of one face: 1 in 6.'),
                     (f'{t} ÷ 6 = {t // 6} fois (environ ; le résultat réel peut varier).', f'{t} ÷ 6 = {t // 6} times (about; the real result can vary).'))
    small, big = 10, 500
    a = _spin({'P': 1, 'F': 1}, small).count('P')
    b = _spin({'P': 1, 'F': 1}, big).count('P')
    return mc((f'Expérience 1 : {small} lancers d’une pièce, {a} piles. Expérience 2 : {big} lancers, {b} piles. Quelle expérience donne une fréquence de piles **plus proche** de ½, en général ?',
               f'Experiment 1: {small} coin tosses, {a} heads. Experiment 2: {big} tosses, {b} heads. Which experiment usually gives a share of heads **closer** to ½?'),
              (f'L’expérience 2 ({big} lancers)', f'Experiment 2 ({big} tosses)'),
              [(f'L’expérience 1 ({small} lancers)', f'Experiment 1 ({small} tosses)'),
               ('Les deux, toujours exactement ½', 'Both, always exactly ½'), ('Aucune des deux', 'Neither'),
               ('On ne peut jamais comparer avec ½', 'You can never compare with ½')],
              ('Plus on fait d’essais, plus la fréquence se rapproche de la probabilité théorique.', 'The more trials you do, the closer the share gets to the theoretical probability.'),
              (f'{a}/{small} et {b}/{big} : avec beaucoup de lancers, on s’approche de ½.', f'{a}/{small} and {b}/{big}: with many tosses you get closer to ½.'))


# ── G3 · List the outcomes ───────────────────────────────────────────────────

def g3_list_outcomes_gen(level='easy'):
    """Count/list the possible outcomes of a simple experiment (229)."""
    if level == 'easy':
        names = random.sample(list(COLS), random.randint(2, 4))
        sectors = names + random.sample(names, random.randint(0, 2))
        random.shuffle(sectors)
        return typed(('Combien de résultats différents peut donner cette roulette ? (Compte les couleurs différentes.)',
                      'How many different results can this spinner give? (Count the different colours.)'),
                     [len(names)], 'integer',
                     ('Deux parts de la même couleur donnent le même résultat.', 'Two parts of the same colour give the same result.'),
                     (f'Couleurs possibles : {", ".join(names)} → {len(names)} résultats.', f'Possible colours: {", ".join(en(n) for n in names)} → {len(names)} results.'),
                     shape=I.spinner([hexof(s) for s in sectors]))
    if level == 'medium':
        sides = random.choice([4, 6, 8])
        correct = (', '.join(str(k) for k in range(1, sides + 1)),) * 2
        wrong = [(', '.join(str(k) for k in range(1, sides)),) * 2, (', '.join(str(k) for k in range(0, sides + 1)),) * 2,
                 (', '.join(str(k) for k in range(2, sides + 1, 2)),) * 2, (', '.join(str(k) for k in range(1, sides + 2)),) * 2]
        return mc((f'On lance un dé à {sides} faces numérotées de 1 à {sides}. Quelle liste donne **tous** les résultats possibles ?',
                   f'You roll a {sides}-sided die numbered 1 to {sides}. Which list gives **all** the possible results?'),
                  correct, wrong,
                  ('Chaque face donne un résultat : n’en oublie aucune et n’en ajoute pas.', 'Each face gives one result: do not miss any or add extra.'),
                  (f'Les {sides} faces : {correct[0]}.', f'The {sides} faces: {correct[1]}.'))
    k = random.choice([2, 3])
    if k == 2:
        correct = ('PP, PF, FP, FF', 'HH, HT, TH, TT')
        wrong = [('PP, PF, FF', 'HH, HT, TT'), ('P, F', 'H, T'), ('PP, FF', 'HH, TT'), ('PF, FP', 'HT, TH')]
        return mc(('On lance deux pièces (une pièce de 1 $ puis une pièce de 2 $). Quelle liste donne tous les résultats ? (P = pile, F = face)',
                   'You toss two coins (a $1 coin then a $2 coin). Which list gives all the results? (H = heads, T = tails)'),
                  correct, wrong,
                  ('PF et FP sont différents : la pièce de 1 $ n’est pas la même que celle de 2 $.', 'HT and TH are different: the $1 coin is not the $2 coin.'),
                  ('2 × 2 = 4 résultats : PP, PF, FP, FF.', '2 × 2 = 4 results: HH, HT, TH, TT.'))
    return typed(('On lance trois pièces l’une après l’autre. Combien de résultats possibles (comme PFP) y a-t-il ?',
                  'You toss three coins one after another. How many possible results (like HTH) are there?'),
                 [8], 'integer',
                 ('Chaque pièce double le nombre de résultats.', 'Each coin doubles the number of results.'),
                 ('2 × 2 × 2 = 8', '2 × 2 × 2 = 8'))
