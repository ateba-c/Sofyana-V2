"""
g5_stats.py — Grade-5 statistics & probability generators (content_g5.md Ch.5-6).

Topics:
  g5_arithmetic_mean_gen    typed       – calculate arithmetic mean
  g5_probability_forms_gen  mix_match   – fraction ↔ decimal ↔ percentage
  g5_probability_frac_gen   QCM         – calculate P(event) as a fraction
  g5_count_outcomes_gen     QCM         – count combined outcomes (multiplication principle)
  g5_data_table_gen         QCM         – interpret a simple data table
  g5_euler_gen              QCM         – Euler's formula V − E + F = 2
  g5_solid_counts_gen       mix_match   – solid → face/vertex/edge counts
  g5_pie_chart_gen          QCM + SVG   – read a pie chart
"""
import random
from quiz.labels import translate_label as _L
from .base import _tagged_shuffle_mc


# ─────────────────────────────────────────────────────────────────────────────
# g5_arithmetic_mean_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_arithmetic_mean_gen(level='easy'):
    """Typed — calculate the arithmetic mean of a list."""
    # The key is always computed from the values actually shown (sum ÷ count):
    # easy/medium → a whole-number mean, hard → a mean ending in ,5.
    if level == 'easy':
        n, lo, hi = random.randint(3, 4), 1, 20
    elif level == 'medium':
        n, lo, hi = random.randint(4, 5), 1, 35
    else:
        n, lo, hi = random.choice([4, 6]), 2, 40
    while True:
        values = [random.randint(lo, hi) for _ in range(n)]
        s = sum(values)
        if level == 'hard':
            if (2 * s) % n == 0 and s % n != 0:      # mean = k,5
                break
        elif s % n == 0:
            break
    mean2 = 2 * sum(values) // n                     # twice the mean, an integer
    correct_str = str(mean2 // 2) if mean2 % 2 == 0 else f'{mean2 // 2},5'

    random.shuffle(values)
    values_str = ', '.join(str(v) for v in values)

    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Quelle est la moyenne de : **{values_str}** ?",
        'prompt_en':        f"What is the mean of: **{values_str}**?",
        'hint_fr':          f"Additionne toutes les valeurs, puis divise par {len(values)}.",
        'hint_en':          f"Add all values, then divide by {len(values)}.",
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Add all values: {" + ".join(str(v) for v in values)} = {sum(values)}.\n'
            f'Step 2: Divide the total by the count: {sum(values)} ÷ {len(values)} = {correct_str.replace(",", ".")}.\n'
            f'Answer: mean = {correct_str.replace(",", ".")}'
        ),
        'explanation_fr': (
            f'Étape 1 : Additionne toutes les valeurs : {" + ".join(str(v) for v in values)} = {sum(values)}.\n'
            f'Étape 2 : Divise le total par le nombre de valeurs : {sum(values)} ÷ {len(values)} = {correct_str}.\n'
            f'Réponse : moyenne = {correct_str}'
        ),
        'correct_answers':  list(dict.fromkeys([correct_str, correct_str.replace(',', '.')])),
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_probability_forms_gen
# ─────────────────────────────────────────────────────────────────────────────

_PROB_TRIPLES = [
    # (fraction, decimal, percentage)
    ('1/2',  '0,5',  '50 %'),
    ('1/4',  '0,25', '25 %'),
    ('3/4',  '0,75', '75 %'),
    ('1/5',  '0,2',  '20 %'),
    ('2/5',  '0,4',  '40 %'),
    ('3/5',  '0,6',  '60 %'),
    ('4/5',  '0,8',  '80 %'),
    ('1/10', '0,1',  '10 %'),
    ('3/10', '0,3',  '30 %'),
    ('7/10', '0,7',  '70 %'),
]


def g5_probability_forms_gen(level='easy'):
    """mix_match — fraction ↔ decimal ↔ percentage for probabilities."""
    count = 3 if level == 'easy' else 4
    pool  = _PROB_TRIPLES[:6] if level == 'easy' else _PROB_TRIPLES
    chosen = random.sample(pool, min(count, len(pool)))

    # Alternate left/right representation type. English uses 0.5 and 50%, French 0,5 and 50 %.
    pairs, steps_fr, steps_en = [], [], []
    for frac, dec, pct in chosen:
        dec_en, pct_en = dec.replace(',', '.'), pct.replace(' %', '%')
        kind = random.choice(['frac_dec', 'frac_pct', 'dec_pct'])
        if kind == 'frac_dec':
            l, r, l_en, r_en = frac, dec, frac, dec_en
        elif kind == 'frac_pct':
            l, r, l_en, r_en = frac, pct, frac, pct_en
        else:
            l, r, l_en, r_en = dec, pct, dec_en, pct_en
        pairs.append({'left': l, 'right': r, 'left_en': l_en, 'right_en': r_en})
        n, d = frac.split('/')
        steps_fr.append(f'{frac} = {n} ÷ {d} = {dec} = {pct}')
        steps_en.append(f'{frac} = {n} ÷ {d} = {dec_en} = {pct_en}')

    return {
        'q_type':           'mix_match',
        'prompt_fr':        'Associe les représentations équivalentes (fraction, décimal, pourcentage).',
        'prompt_en':        'Match the equivalent representations (fraction, decimal, percentage).',
        # procedural hint: no value that could give away one of the pairs
        'hint_fr':          'Fraction → décimal : divise le numérateur par le dénominateur. Décimal → pourcentage : multiplie par 100.',
        'hint_en':          'Fraction → decimal: divide the numerator by the denominator. Decimal → percentage: multiply by 100.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            pairs,
        'explanation_en':   '\n'.join(['Divide the numerator by the denominator, then multiply by 100 for the percentage:'] + steps_en),
        'explanation_fr':   '\n'.join(['Divise le numérateur par le dénominateur, puis multiplie par 100 pour le pourcentage :'] + steps_fr),
        'correct_answers':  [p['right'] for p in pairs],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_probability_frac_gen
# ─────────────────────────────────────────────────────────────────────────────

# (singular, plural, English) — « orange » is invariable in French
_COLORS = [('rouge', 'rouges', 'red'), ('bleue', 'bleues', 'blue'), ('verte', 'vertes', 'green'),
           ('jaune', 'jaunes', 'yellow'), ('orange', 'orange', 'orange'), ('violette', 'violettes', 'purple')]


def g5_probability_frac_gen(level='easy'):
    """QCM — calculate P(event) as fraction, decimal, or percentage."""
    total     = random.randint(4, 10) if level == 'easy' else random.randint(5, 20)
    favorable = random.randint(1, total - 1)
    others    = total - favorable
    color_sg, color_pl, color_en = random.choice(_COLORS)

    from math import gcd
    g = gcd(favorable, total)
    num_r, den_r = favorable // g, total // g
    correct_frac = f"{favorable}/{total}"
    correct_red  = f"{num_r}/{den_r}"

    # Present as fraction QCM. Every candidate comes from a real mistake; when the
    # complement equals the answer (half the marbles), the later ones take its place.
    tagged_candidates = [
        (f"{others}/{total}", 'complement',
         'That is the probability of NOT drawing that colour.',
         "C'est la probabilité de NE PAS piger cette couleur."),
        (f"{favorable}/{others}", 'ratio_not_prob',
         'Probability = favourable ÷ total outcomes, not favourable ÷ the others.',
         'Probabilité = cas favorables ÷ total des cas, pas cas favorables ÷ les autres.'),
        (f"{total}/{favorable}", 'inverted',
         'The numerator is favourable, denominator is total.',
         'Le numérateur est les cas favorables, le dénominateur est le total.'),
        (f"{favorable}/{total + favorable}", 'counted_twice',
         'The total already includes the marbles of that colour.',
         'Le total comprend déjà les billes de cette couleur.'),
        (f"{others}/{favorable}", 'others_over_favourable',
         'Probability = favourable ÷ total outcomes.',
         'Probabilité = cas favorables ÷ total des cas.'),
        (f"1/{total}", 'one_marble',
         'There are several marbles of that colour, not just one.',
         "Il y a plusieurs billes de cette couleur, pas une seule."),
    ]
    from fractions import Fraction
    tagged_candidates = [c for c in tagged_candidates
                         if Fraction(c[0]) != Fraction(favorable, total)]   # never a value-equal « wrong » choice

    fav_fr = f"{favorable} bille{'s' if favorable > 1 else ''} {color_pl if favorable > 1 else color_sg}"
    fav_en = f"{favorable} {color_en} marble{'s' if favorable != 1 else ''}"
    oth_fr = "1 bille d'une autre couleur" if others == 1 else f"{others} billes d'autres couleurs"
    oth_en = "1 marble of another colour" if others == 1 else f"{others} marbles of other colours"

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        (f"Un sac contient {total} billes : {fav_fr} et {oth_fr}. "
                             f"Quelle est la probabilité de piger une bille {color_sg} ?"),
        'prompt_en':        (f"A bag has {total} marbles: {fav_en} and {oth_en}. "
                             f"What is the probability of drawing {'an' if color_en[0] in 'aeiou' else 'a'} {color_en} marble?"),
        'hint_fr':          'Probabilité = nombre de cas favorables / nombre total de cas.',
        'hint_en':          'Probability = number of favourable outcomes / total number of outcomes.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(correct_frac, tagged_candidates),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Count the favourable outcomes: {fav_en}.\n'
            f'Step 2: Count total outcomes: {total} marbles.\n'
            f'Step 3: P(event) = favourable ÷ total = {favorable}/{total}.\n'
            f'Answer: {correct_frac}'
        ),
        'explanation_fr': (
            f'Étape 1 : Compte les cas favorables : {fav_fr}.\n'
            f'Étape 2 : Compte le total des cas : {total} billes.\n'
            f'Étape 3 : P(événement) = cas favorables ÷ total = {favorable}/{total}.\n'
            f'Réponse : {correct_frac}'
        ),
        'correct_answers':  list(dict.fromkeys([correct_frac, correct_red])),
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_count_outcomes_gen
# ─────────────────────────────────────────────────────────────────────────────

# One closed, coherent scenario each: the categories belong together and are independent.
# (what is built fr/en, [category fr/en ×3])
_OUTCOME_SCENARIOS = [
    (('tenues', 'outfits'),
     [('chandails', 'sweaters'), ('pantalons', 'pairs of pants'), ('paires de chaussures', 'pairs of shoes')]),
    (('repas', 'meals'),
     [('plats principaux', 'main dishes'), ('desserts', 'desserts'), ('boissons', 'drinks')]),
    (('sandwichs', 'sandwiches'),
     [('sortes de pain', 'kinds of bread'), ('garnitures', 'fillings'), ('sauces', 'sauces')]),
    (('cornets de crème glacée', 'ice-cream cones'),
     [('parfums de crème glacée', 'ice-cream flavours'), ('sortes de cornets', 'kinds of cones'), ('garnitures', 'toppings')]),
    (('pizzas', 'pizzas'),
     [('sortes de croûte', 'kinds of crust'), ('garnitures', 'toppings'), ('tailles', 'sizes')]),
]


def g5_count_outcomes_gen(level='easy'):
    """QCM — count total outcomes using the multiplication principle."""
    (what_fr, what_en), cats = random.choice(_OUTCOME_SCENARIOS)
    fem = what_fr in ('tenues', 'pizzas')
    if level == 'easy':
        nums = random.sample(range(2, 5), 2)
    elif level == 'medium':
        nums = random.sample(range(2, 7), 2)
    else:
        nums = random.sample(range(2, 6), 3)
    cats = cats[:len(nums)]
    total = 1
    for n in nums:
        total *= n

    bullets = [(f'{cfr[0].upper()}{cfr[1:]} : {n} choix', f'{cen[0].upper()}{cen[1:]}: {n} choices')
               for (cfr, cen), n in zip(cats, nums)]
    diff_fr = 'différentes' if fem else 'différents'
    prompt_fr = f"Pour composer des {what_fr}, tu choisis un élément de chaque catégorie. Combien de {what_fr} {diff_fr} peux-tu composer ?"
    prompt_en = f"To make {what_en}, you choose one item from each category. How many different {what_en} can you make?"

    # Distractors, each from a named mistake
    a, b = nums[0], nums[1]
    cand = [
        (sum(nums), 'sum_not_product',
         f'You added {" + ".join(map(str, nums))}. Each choice goes with every other one: multiply.',
         f'Tu as additionné {" + ".join(map(str, nums))}. Chaque choix va avec chacun des autres : multiplie.'),
    ]
    if len(nums) == 3:
        c = nums[2]
        cand += [
            (a * b, 'forgot_category', f'{a} × {b} forgets the {cats[2][1]}.', f'{a} × {b} oublie les {cats[2][0]}.'),
            (b * c, 'forgot_category', f'{b} × {c} forgets the {cats[0][1]}.', f'{b} × {c} oublie les {cats[0][0]}.'),
            (a * b + c, 'added_last', f'{a} × {b} + {c}: the last category must be multiplied too.',
             f'{a} × {b} + {c} : la dernière catégorie doit aussi être multipliée.'),
            (a * c, 'forgot_category', f'{a} × {c} forgets the {cats[1][1]}.', f'{a} × {c} oublie les {cats[1][0]}.'),
            (a * b * (c + 1), 'one_too_many', f'{a} × {b} × {c + 1}: there are only {c} {cats[2][1]}.',
             f'{a} × {b} × {c + 1} : il n’y a que {c} {cats[2][0]}.'),
        ]
    else:
        cand += [
            (a * a, 'same_number_twice', f'{a} × {a} uses the number of {cats[0][1]} twice.', f'{a} × {a} utilise deux fois le nombre de {cats[0][0]}.'),
            (b * b, 'same_number_twice', f'{b} × {b} uses the number of {cats[1][1]} twice.', f'{b} × {b} utilise deux fois le nombre de {cats[1][0]}.'),
            (a * (b + 1), 'one_too_many', f'{a} × {b + 1}: there are only {b} {cats[1][1]}.', f'{a} × {b + 1} : il n’y a que {b} {cats[1][0]}.'),
            (a * b + a + b, 'added_and_multiplied', f'{a} × {b} + {a} + {b}: the product alone counts every combination.',
             f'{a} × {b} + {a} + {b} : le produit seul compte toutes les combinaisons.'),
            ((a + 1) * b, 'one_too_many', f'{a + 1} × {b}: there are only {a} {cats[0][1]}.', f'{a + 1} × {b} : il n’y a que {a} {cats[0][0]}.'),
        ]
    tagged_candidates = [(str(v), e, fen, ffr) for v, e, fen, ffr in cand if v != total and v > 0]

    calc = ' × '.join(map(str, nums))
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'bullets':          bullets,
        'hint_fr':          'Chaque choix d’une catégorie va avec chaque choix des autres : multiplie les nombres de choix.',
        'hint_en':          'Each choice in one category goes with every choice in the others: multiply the numbers of choices.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(str(total), tagged_candidates),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Use the multiplication principle: multiply the number of choices in each category.\n'
            f'Step 2: {calc} = {total}.\n'
            f'Answer: {total} different {what_en}'
        ),
        'explanation_fr': (
            f'Étape 1 : Utilise le principe multiplicatif : multiplie le nombre de choix de chaque catégorie.\n'
            f'Étape 2 : {calc} = {total}.\n'
            f'Réponse : {total} {what_fr} {diff_fr}'
        ),
        'correct_answers':  [str(total)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_data_table_gen
# ─────────────────────────────────────────────────────────────────────────────

# One survey per context. Each category: (table label FR, table label EN, phrase FR with article, phrase EN).
_TABLE_CONTEXTS = [
    {
        'cats': [('Chat', 'Cat', 'le chat', 'cats'), ('Chien', 'Dog', 'le chien', 'dogs'),
                 ('Oiseau', 'Bird', "l'oiseau", 'birds'), ('Poisson', 'Fish', 'le poisson', 'fish')],
        'col': ('Animal', 'Pet'),
        'intro': ("On a demandé aux élèves de la classe quel est leur animal de compagnie préféré.",
                  "The students in a class were asked which pet they like best."),
        'which': ('Quel animal', 'Which pet'),
    },
    {
        'cats': [('Pomme', 'Apple', 'la pomme', 'apples'), ('Orange', 'Orange', "l'orange", 'oranges'),
                 ('Raisin', 'Grapes', 'le raisin', 'grapes'), ('Banane', 'Banana', 'la banane', 'bananas')],
        'col': ('Fruit', 'Fruit'),
        'intro': ("On a demandé aux élèves de la classe quel est leur fruit préféré.",
                  "The students in a class were asked which fruit they like best."),
        'which': ('Quel fruit', 'Which fruit'),
    },
    {
        # Quebec French: « soccer » (« football » means American football there)
        'cats': [('Soccer', 'Soccer', 'le soccer', 'soccer'), ('Basketball', 'Basketball', 'le basketball', 'basketball'),
                 ('Natation', 'Swimming', 'la natation', 'swimming'), ('Tennis', 'Tennis', 'le tennis', 'tennis')],
        'col': ('Sport', 'Sport'),
        'intro': ("On a demandé aux élèves de la classe quel est leur sport préféré.",
                  "The students in a class were asked which sport they like best."),
        'which': ('Quel sport', 'Which sport'),
    },
    {
        'cats': [('Rouge', 'Red', 'le rouge', 'red'), ('Bleu', 'Blue', 'le bleu', 'blue'),
                 ('Vert', 'Green', 'le vert', 'green'), ('Jaune', 'Yellow', 'le jaune', 'yellow')],
        'col': ('Couleur', 'Colour'),
        'intro': ("On a demandé aux élèves de la classe quelle est leur couleur préférée.",
                  "The students in a class were asked which colour they like best."),
        'which': ('Quelle couleur', 'Which colour'),
    },
]


def g5_data_table_gen(level='easy'):
    """QCM — interpret a survey table (shown as a real table, not inline text)."""
    ctx     = random.choice(_TABLE_CONTEXTS)
    n_cats  = len(ctx['cats']) if level == 'hard' else random.randint(3, len(ctx['cats']))
    cats    = ctx['cats'][:n_cats]
    while True:                 # a tie on the max/min would make a "wrong" choice correct too
        values = [random.randint(2, 15) for _ in cats]
        if values.count(max(values)) == 1 and values.count(min(values)) == 1:
            break
    labels  = [(c[0], c[1]) for c in cats]
    which_fr, which_en = ctx['which']
    max_v, min_v = max(values), min(values)
    hi, lo  = cats[values.index(max_v)], cats[values.index(min_v)]

    q_type  = random.choice(['largest', 'smallest', 'total', 'difference'])

    if q_type in ('largest', 'smallest'):
        most     = q_type == 'largest'
        pick     = hi if most else lo
        pick_v   = max_v if most else min_v
        correct  = (pick[0], pick[1])
        agree    = 'e' if which_fr.startswith('Quelle') else ''
        q_fr = f"{which_fr} a été choisi{agree} par le {'plus' if most else 'moins'} d'élèves ?"
        q_en = f"{which_en} was chosen by the {'most' if most else 'fewest'} students?"
        fb   = (('Find the largest number in the table.', 'Cherche le plus grand nombre du tableau.') if most else
                ('Find the smallest number in the table.', 'Cherche le plus petit nombre du tableau.'))
        tagged_candidates = [(lb, 'wrong_category', fb[0], fb[1]) for lb in labels if lb != correct]
        hint_fr = f"Compare les nombres de la colonne « Nombre d'élèves » : lequel est le plus {'grand' if most else 'petit'} ?"
        hint_en = f"Compare the numbers in the “Number of students” column: which one is the {'largest' if most else 'smallest'}?"
        expl_fr = [f"Les nombres d'élèves sont : {', '.join(map(str, values))}.",
                   f"Le plus {'grand' if most else 'petit'} est {pick_v}, sur la ligne « {pick[0]} »."]
        expl_en = [f"The numbers of students are: {', '.join(map(str, values))}.",
                   f"The {'largest' if most else 'smallest'} is {pick_v}, on the “{pick[1]}” row."]
        ans_fr, ans_en = pick[0], pick[1]
    elif q_type == 'total':
        total   = sum(values)
        correct = str(total)
        q_fr = "Combien d'élèves ont répondu en tout ?"
        q_en = "How many students answered in all?"
        tagged_candidates = [
            (str(total - values[-1]), 'forgot_last', 'Add ALL the rows of the table.', 'Additionne TOUTES les lignes du tableau.'),
            (str(total + values[0]), 'counted_twice', 'Count each row only once.', 'Compte chaque ligne une seule fois.'),
            (str(max_v), 'max_not_total', 'The question asks for the total, not the largest number.',
             'La question demande le total, pas le plus grand nombre.'),
            (str(total - 1), 'off_by_one', 'Check your addition again.', 'Vérifie ton addition.'),
        ]
        hint_fr = "Additionne les nombres d'élèves de toutes les lignes du tableau."
        hint_en = "Add the numbers of students from every row of the table."
        calc = f"{' + '.join(map(str, values))} = {total}"
        expl_fr = ["Il faut additionner toutes les lignes du tableau.", calc]
        expl_en = ["Add every row of the table.", calc]
        ans_fr, ans_en = f"{total} élèves", f"{total} students"
    else:  # difference
        diff    = max_v - min_v
        correct = str(diff)
        q_fr = f"Combien d'élèves de plus ont choisi {hi[2]} plutôt que {lo[2]} ?"
        q_en = f"How many more students chose {hi[3]} than {lo[3]}?"
        tagged_candidates = [
            (str(max_v), 'max_not_diff', 'Subtract the two numbers.', 'Soustrais les deux nombres.'),
            (str(min_v), 'min_not_diff', 'Subtract the two numbers.', 'Soustrais les deux nombres.'),
            (str(diff + 1), 'off_by_one', 'Check your subtraction again.', 'Vérifie ta soustraction.'),
            (str(max_v + min_v), 'added_not_subtracted', 'Find the difference, not the sum.', 'Cherche la différence, pas la somme.'),
        ]
        hint_fr = f"Trouve les nombres de « {hi[0]} » et de « {lo[0]} », puis soustrais le plus petit du plus grand."
        hint_en = f"Find the numbers for “{hi[1]}” and “{lo[1]}”, then subtract the smaller from the larger."
        calc = f"{max_v} − {min_v} = {diff}"
        expl_fr = [f"{hi[0]} : {max_v} élèves. {lo[0]} : {min_v} élèves.", calc]
        expl_en = [f"{hi[1]}: {max_v} students. {lo[1]}: {min_v} students.", calc]
        ans_fr, ans_en = f"{diff} élèves de plus", f"{diff} more students"

    intro_fr, intro_en = ctx['intro']
    tagged_candidates = [c for c in tagged_candidates if c[0] != correct]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        f"{intro_fr} {q_fr}",
        'prompt_en':        f"{intro_en} {q_en}",
        # Rendered as a real table under the prompt (partials/data_table.html); cells may be (fr, en) pairs.
        'table': {
            'headers': [ctx['col'], ("Nombre d'élèves", 'Number of students')],
            'rows':    [[lb, str(v)] for lb, v in zip(labels, values)],
        },
        'hint_fr':          hint_fr,
        'hint_en':          hint_en,
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(correct, tagged_candidates[:4]),
        'pairs':            [],
        'explanation_fr':   '\n'.join(expl_fr + [f'Réponse : {ans_fr}']),
        'explanation_en':   '\n'.join(expl_en + [f'Answer: {ans_en}']),
        'correct_answers':  [correct[0] if isinstance(correct, tuple) else correct],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_euler_gen
# ─────────────────────────────────────────────────────────────────────────────

# (name_fr, name_en, V, E, F)
_POLYHEDRA = [
    ('Cube',                      'Cube',                     8, 12, 6),
    ('Tétraèdre',                 'Tetrahedron',              4,  6, 4),
    ('Pyramide à base carrée',    'Square pyramid',           5,  8, 5),
    ('Prisme à base triangulaire','Triangular prism',         6,  9, 5),
    ('Prisme à base rectangulaire','Rectangular prism',       8, 12, 6),
    ('Octaèdre',                  'Octahedron',               6, 12, 8),
    ('Pyramide à base pentagonale','Pentagonal pyramid',       6, 10, 6),
    ('Prisme à base pentagonale', 'Pentagonal prism',        10, 15, 7),
]


def g5_euler_gen(level='easy'):
    """QCM — find missing value using Euler's formula V − E + F = 2."""
    if level == 'easy':
        pool = _POLYHEDRA[:4]
    elif level == 'medium':
        pool = _POLYHEDRA[:6]
    else:
        pool = _POLYHEDRA

    name_fr, name_en, V, E, F = random.choice(pool)
    fem = name_fr.startswith('Pyramide')
    sol_fr = f"{'Une' if fem else 'Un'} {name_fr[0].lower()}{name_fr[1:]}"      # « Une pyramide à base carrée »
    sol_en = f"{'An' if name_en[0] in 'AEIOU' else 'A'} {name_en.lower()}"      # « An octahedron »
    il = 'elle' if fem else 'il'
    # What to find
    unknown = random.choice(['E', 'V', 'F'])

    if unknown == 'E':
        correct = E
        prompt_fr = f"{sol_fr} a {V} sommets et {F} faces. Combien a-t-{il} d'arêtes ?"
        prompt_en = f"{sol_en} has {V} vertices and {F} faces. How many edges does it have?"
        iso_fr = f'A = S + F − 2 = {V} + {F} − 2 = {E}'
        iso_en = f'E = V + F − 2 = {V} + {F} − 2 = {E}'
        wrong = [(V + F, 'forgot_minus_2', 'You added V + F but forgot to subtract 2.', 'Tu as fait S + F, mais oublié d’enlever 2.'),
                 (V + F + 2, 'sign_error', 'E = V + F − 2: subtract 2, do not add it.', 'A = S + F − 2 : on enlève 2, on ne l’ajoute pas.'),
                 (V + F - 1, 'off_by_one', 'Subtract 2, not 1.', 'Enlève 2, pas 1.'),
                 (E - 1, 'off_by_one', 'Recheck V + F − 2.', 'Recalcule S + F − 2.')]
    elif unknown == 'V':
        correct = V
        prompt_fr = f"{sol_fr} a {E} arêtes et {F} faces. Combien a-t-{il} de sommets ?"
        prompt_en = f"{sol_en} has {E} edges and {F} faces. How many vertices does it have?"
        iso_fr = f'S = 2 + A − F = 2 + {E} − {F} = {V}'
        iso_en = f'V = 2 + E − F = 2 + {E} − {F} = {V}'
        wrong = [(E - F, 'forgot_plus_2', 'You did E − F but forgot to add 2.', 'Tu as fait A − F, mais oublié d’ajouter 2.'),
                 (E + F - 2, 'sign_error', 'V = 2 + E − F: subtract the faces.', 'S = 2 + A − F : on soustrait les faces.'),
                 (E + F, 'wrong_formula', 'Use V − E + F = 2 to isolate V.', 'Utilise S − A + F = 2 pour isoler S.'),
                 (V + 1, 'off_by_one', 'Recheck 2 + E − F.', 'Recalcule 2 + A − F.')]
    else:
        correct = F
        prompt_fr = f"{sol_fr} a {V} sommets et {E} arêtes. Combien a-t-{il} de faces ?"
        prompt_en = f"{sol_en} has {V} vertices and {E} edges. How many faces does it have?"
        iso_fr = f'F = 2 + A − S = 2 + {E} − {V} = {F}'
        iso_en = f'F = 2 + E − V = 2 + {E} − {V} = {F}'
        wrong = [(E - V, 'forgot_plus_2', 'You did E − V but forgot to add 2.', 'Tu as fait A − S, mais oublié d’ajouter 2.'),
                 (V + E - 2, 'sign_error', 'F = 2 + E − V: subtract the vertices.', 'F = 2 + A − S : on soustrait les sommets.'),
                 (E + V, 'wrong_formula', 'Use V − E + F = 2 to isolate F.', 'Utilise S − A + F = 2 pour isoler F.'),
                 (F + 1, 'off_by_one', 'Recheck 2 + E − V.', 'Recalcule 2 + A − S.')]
    wrong += [(correct + 2, 'off_by_two', 'Recheck the ± 2 in the formula.', 'Revérifie le ± 2 de la relation.'),
              (correct - 1, 'off_by_one', 'Recheck your arithmetic.', 'Recalcule soigneusement.')]
    tagged_candidates = [(str(v), e, fen, ffr) for v, e, fen, ffr in wrong if v != correct and v > 0]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Relation d\'Euler pour les polyèdres convexes : Sommets − Arêtes + Faces = 2.',
        'hint_en':          'Euler\'s formula for convex polyhedra: Vertices − Edges + Faces = 2.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(str(correct), tagged_candidates),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Euler\'s formula: V − E + F = 2, where V = vertices, E = edges, F = faces.\n'
            f'Step 2: Isolate the unknown: {iso_en}.\n'
            f'Step 3: Check: {V} − {E} + {F} = 2 ✓\n'
            f'Answer: {correct}'
        ),
        'explanation_fr': (
            f'Étape 1 : Relation d\'Euler : S − A + F = 2, où S = sommets, A = arêtes, F = faces.\n'
            f'Étape 2 : Isole l\'inconnue : {iso_fr}.\n'
            f'Étape 3 : Vérification : {V} − {E} + {F} = 2 ✓\n'
            f'Réponse : {correct}'
        ),
        'correct_answers':  [str(correct)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_solid_counts_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_solid_counts_gen(level='easy'):
    """mix_match — match solid name to its face/vertex/edge description."""
    if level == 'easy':
        pool  = _POLYHEDRA[:4]
        count = 3
    elif level == 'medium':
        pool  = _POLYHEDRA[:6]
        count = 4
    else:
        pool  = _POLYHEDRA
        count = 4

    # Two solids with the same (faces, vertices, edges) — the cube and the rectangular
    # prism — could swap places, so a set never holds two equal profiles.
    while True:
        chosen = random.sample(pool, min(count, len(pool)))
        if len({(V, E, F) for _, _, V, E, F in chosen}) == len(chosen):
            break
    pairs, lines_fr, lines_en = [], [], []
    for name_fr, name_en, V, E, F in chosen:
        desc = f"{F} faces, {V} sommets, {E} arêtes"
        desc_en = f"{F} faces, {V} vertices, {E} edges"
        pairs.append({'left': name_fr, 'left_en': name_en, 'right': desc, 'right_en': desc_en})
        lines_fr.append(f'{name_fr} : {desc} ({V} − {E} + {F} = 2 ✓)')
        lines_en.append(f'{name_en}: {desc_en} ({V} − {E} + {F} = 2 ✓)')

    return {
        'q_type':           'mix_match',
        'prompt_fr':        'Associe chaque solide à ses caractéristiques (faces, sommets, arêtes).',
        'prompt_en':        'Match each solid to its properties (faces, vertices, edges).',
        'hint_fr':          ('Imagine chaque solide : compte ses faces, puis ses sommets (les coins), puis ses arêtes. '
                             'Vérifie avec la relation d\'Euler : sommets − arêtes + faces = 2.'),
        'hint_en':          ('Picture each solid: count its faces, then its vertices (corners), then its edges. '
                             'Check with Euler: vertices − edges + faces = 2.'),
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            pairs,
        'explanation_en':   '\n'.join(lines_en),
        'explanation_fr':   '\n'.join(lines_fr),
        'correct_answers':  [p['right'] for p in pairs],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_pie_chart_gen
# ─────────────────────────────────────────────────────────────────────────────

_PIE_CONTEXTS = [
    (['Chat', 'Chien', 'Oiseau'],            "animaux préférés",  "favourite animals"),
    (['Rouge', 'Bleu', 'Vert', 'Jaune'],     "couleurs préférées","favourite colours"),
    (['Soccer', 'Basketball', 'Natation'],   "sports pratiqués",  "sports"),   # Québec: « soccer »
    (['Été', 'Automne', 'Hiver', 'Printemps'], "saisons préférées","favourite seasons"),
]


def g5_pie_chart_gen(level='easy'):
    """QCM + SVG — read a pie chart (ask largest, smallest, or percentage)."""
    cats_list, ctx_fr, ctx_en = random.choice(_PIE_CONTEXTS)
    n_cats = 3 if level == 'easy' else len(cats_list)
    cats   = cats_list[:n_cats]

    # Generate proportions that sum to 100 (percentages)
    # All shares different, so « the largest share » has exactly one answer.
    while True:
        props = [random.randint(5, 50) for _ in range(n_cats - 1)]
        last  = 100 - sum(props)
        if 5 <= last <= 50:
            props.append(last)
            if len(set(props)) == n_cats:
                break

    q_type = random.choice(['largest', 'pct_of'])
    shares_fr = ', '.join(f'{c} {p} %' for c, p in zip(cats, props))
    shares_en = ', '.join(f"{_L(c, 'en')} {p}%" for c, p in zip(cats, props))

    if q_type == 'largest':
        max_idx = props.index(max(props))
        correct = cats[max_idx]
        prompt_fr = f"D'après le diagramme circulaire des {ctx_fr}, quelle catégorie représente la plus grande part ?"
        prompt_en = f"According to the pie chart about {ctx_en}, which category has the largest share?"
        tagged_candidates = [
            (c, 'wrong_sector',
             'Compare the size of each sector or its percentage.',
             'Compare la taille de chaque secteur ou son pourcentage.')
            for c in cats if c != correct
        ]
        hint = ('Lis le pourcentage de chaque secteur et trouve le plus grand.',
                'Read the percentage of each sector and find the largest.')
        expl_fr = [f'Les parts sont : {shares_fr}.', f'La plus grande est {props[max_idx]} % : « {correct} ».']
        expl_en = [f'The shares are: {shares_en}.', f"The largest is {props[max_idx]}%: “{_L(correct, 'en')}”."]
    else:
        idx     = random.randint(0, n_cats - 1)
        correct = str(props[idx]) + ' %'
        prompt_fr = f"D'après le diagramme circulaire des {ctx_fr}, quel pourcentage représente « {cats[idx]} » ?"
        prompt_en = f"According to the pie chart about {ctx_en}, what percentage does '{_L(cats[idx], 'en')}' represent?"
        hint = (f'Repère le secteur « {cats[idx]} » et lis le pourcentage écrit dessus.',
                f"Find the “{_L(cats[idx], 'en')}” sector and read the percentage written on it.")
        expl_fr = [f'Le secteur « {cats[idx]} » affiche {props[idx]} %.']
        expl_en = [f"The “{_L(cats[idx], 'en')}” sector shows {props[idx]}%."]
        tagged_candidates = [
            (str(props[i]) + ' %', 'wrong_sector',
             'Find the correct sector for that category.',
             'Repère le bon secteur pour cette catégorie.')
            for i in range(n_cats) if i != idx
        ] + [
            (str(100 - props[idx]) + ' %', 'complement',
             'That is the percentage of all OTHER categories.',
             "C'est le pourcentage de TOUTES les autres catégories."),
        ]

    tagged_candidates = [c for c in tagged_candidates if c[0] != str(correct)]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          hint[0],
        'hint_en':          hint[1],
        'show_illustration': True,
        'shape_data':       [{
            'type':        'pie_chart_multi',
            'categories':  cats,
            'proportions': props,
        }],
        # percentages as (fr, en) labels: « 45 % » in French, “45%” in English
        'choices':          _tagged_shuffle_mc(_pct_label(correct), [(_pct_label(c[0]),) + tuple(c[1:]) for c in tagged_candidates[:4]]),
        'pairs':            [],
        'explanation_en':   '\n'.join(expl_en + [f"Answer: {_L(correct, 'en').replace(' %', '%')}"]),
        'explanation_fr':   '\n'.join(expl_fr + [f'Réponse : {correct}']),
        'correct_answers':  [str(correct)],
    }


def _pct_label(label):
    """'45 %' → ('45 %', '45%'); any other label is returned unchanged."""
    return (label, label.replace(' %', '%')) if label.endswith(' %') else label
