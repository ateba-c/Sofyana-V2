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
    if level == 'easy':
        n = random.randint(3, 4)
        mean = random.randint(4, 15)
        # Build list summing to mean*n
        values = [random.randint(1, mean * 2) for _ in range(n - 1)]
        last   = mean * n - sum(values)
        if last < 1:
            # Retry with smaller values
            values = [random.randint(1, mean) for _ in range(n - 1)]
            last   = mean * n - sum(values)
        values.append(max(1, last))
        correct_str = str(mean)
    elif level == 'medium':
        n    = random.randint(4, 5)
        mean = random.randint(5, 20)
        values = [random.randint(1, mean * 2) for _ in range(n - 1)]
        last   = mean * n - sum(values)
        values.append(max(1, last))
        correct_str = str(mean)
    else:
        # Mean may have 0.5
        n   = random.randint(4, 6)
        # Force mean = x.5
        mean_times_2 = random.randint(10, 40)
        total = mean_times_2 * n
        if total % 2 == 1:
            total += n  # adjust
        values = [random.randint(2, total // n * 2) for _ in range(n - 1)]
        last   = total - sum(values)
        values.append(max(1, last))
        mean_val = total / n
        correct_str = str(mean_val).replace('.', ',').rstrip('0').rstrip(',')

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
            f'Answer: mean = {correct_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Additionne toutes les valeurs : {" + ".join(str(v) for v in values)} = {sum(values)}.\n'
            f'Étape 2 : Divise le total par le nombre de valeurs : {sum(values)} ÷ {len(values)} = {correct_str}.\n'
            f'Réponse : moyenne = {correct_str}'
        ),
        'correct_answers':  [correct_str, correct_str.replace(',', '.')],
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

    # Alternate left/right representation type
    pairs = []
    for frac, dec, pct in chosen:
        kind = random.choice(['frac_dec', 'frac_pct', 'dec_pct'])
        if kind == 'frac_dec':
            pairs.append({'left': frac, 'right': dec})
        elif kind == 'frac_pct':
            pairs.append({'left': frac, 'right': pct})
        else:
            pairs.append({'left': dec, 'right': pct})

    return {
        'q_type':           'mix_match',
        'prompt_fr':        'Associe les représentations équivalentes (fraction, décimal, pourcentage).',
        'prompt_en':        'Match the equivalent representations (fraction, decimal, percentage).',
        'hint_fr':          '1/2 = 0,5 = 50 %. Multiplie la fraction par 100 pour obtenir le pourcentage.',
        'hint_en':          '1/2 = 0.5 = 50%. Multiply the fraction by 100 to get the percentage.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            pairs,
        'explanation_en': (
            'Step 1: Fraction → decimal: divide numerator by denominator.\n'
            'Step 2: Decimal → percentage: multiply by 100 and add %.\n'
            'Step 3: Key equivalences: 1/2=0.5=50%, 1/4=0.25=25%, 1/5=0.2=20%, 1/10=0.1=10%.'
        ),
        'explanation_fr': (
            'Étape 1 : Fraction → décimal : divise le numérateur par le dénominateur.\n'
            'Étape 2 : Décimal → pourcentage : multiplie par 100 et ajoute %.\n'
            'Étape 3 : Équivalences clés : 1/2=0,5=50%, 1/4=0,25=25%, 1/5=0,2=20%, 1/10=0,1=10%.'
        ),
        'correct_answers':  [p['right'] for p in pairs],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_probability_frac_gen
# ─────────────────────────────────────────────────────────────────────────────

_COLORS_FR = ['rouges', 'bleues', 'vertes', 'jaunes', 'oranges', 'violettes']
_COLORS_EN = ['red',    'blue',   'green',  'yellow', 'orange',  'purple']


def g5_probability_frac_gen(level='easy'):
    """QCM — calculate P(event) as fraction, decimal, or percentage."""
    total     = random.randint(4, 10) if level == 'easy' else random.randint(5, 20)
    favorable = random.randint(1, total - 1)
    ci, cj    = random.sample(range(len(_COLORS_FR)), 2)
    color_fr  = _COLORS_FR[ci]
    color_en  = _COLORS_EN[ci]

    from math import gcd
    g = gcd(favorable, total)
    num_r, den_r = favorable // g, total // g
    correct_frac = f"{favorable}/{total}"
    correct_red  = f"{num_r}/{den_r}"

    # Present as fraction QCM
    tagged_candidates = [
        (f"{total - favorable}/{total}", 'complement',
         'That is the probability of NOT drawing that colour.',
         "C'est la probabilité de NE PAS piger cette couleur."),
        (f"{favorable}/{total - favorable}", 'ratio_not_prob',
         'Probability = favourable ÷ total outcomes.',
         'Probabilité = cas favorables ÷ total des cas.'),
        (f"{total}/{favorable}", 'inverted',
         'The numerator is favourable, denominator is total.',
         'Le numérateur est les cas favorables, le dénominateur est le total.'),
        (f"{favorable + 1}/{total}", 'off_by_one',
         'Count carefully.',
         'Compte bien.'),
    ]
    tagged_candidates = [c for c in tagged_candidates if c[0] != correct_frac]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        (f"Un sac contient {total} billes : {favorable} {color_fr} "
                             f"et {total - favorable} d'autres couleurs. "
                             f"Quelle est la probabilité de piger une bille {color_fr} ?"),
        'prompt_en':        (f"A bag has {total} marbles: {favorable} {color_en} "
                             f"and {total - favorable} of other colours. "
                             f"What is the probability of drawing {'an' if color_en[0] in 'aeiou' else 'a'} {color_en} marble?"),
        'hint_fr':          'Probabilité = nombre de cas favorables / nombre total de cas.',
        'hint_en':          'Probability = number of favourable outcomes / total number of outcomes.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(correct_frac, tagged_candidates[:4]),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Count the favourable outcomes: {favorable} {color_en} marble(s).\n'
            f'Step 2: Count total outcomes: {total} marbles.\n'
            f'Step 3: P(event) = favourable ÷ total = {favorable}/{total}.\n'
            f'Answer: {correct_frac}'
        ),
        'explanation_fr': (
            f'Étape 1 : Compte les cas favorables : {favorable} bille(s) {color_fr}.\n'
            f'Étape 2 : Compte le total des cas : {total} billes.\n'
            f'Étape 3 : P(événement) = cas favorables ÷ total = {favorable}/{total}.\n'
            f'Réponse : {correct_frac}'
        ),
        'correct_answers':  [correct_frac, correct_red],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_count_outcomes_gen
# ─────────────────────────────────────────────────────────────────────────────

_SCENARIOS = [
    # (fr, en, choices_a, choices_b)
    ("chemises", "shirts",   3, 4),
    ("pantalons", "pants",    4, 3),
    ("sandwichs", "sandwiches", 3, 3),
    ("pizzas",  "pizzas",    4, 2),
    ("glaces",  "ice creams", 3, 5),
    ("menus",   "menus",     4, 4),
]
_TOPPERS = [
    ("garnitures", "toppings"),
    ("couleurs",   "colours"),
    ("saveurs",    "flavours"),
    ("formats",    "sizes"),
]


def g5_count_outcomes_gen(level='easy'):
    """QCM — count total outcomes using the multiplication principle."""
    if level == 'easy':
        name_fr, name_en, a, b = random.choice(_SCENARIOS[:4])
        c = None
    elif level == 'medium':
        name_fr, name_en, a, b = random.choice(_SCENARIOS)
        c = None
    else:
        # Three independent choices
        name_fr, name_en, a, b = random.choice(_SCENARIOS)
        c = random.randint(2, 4)

    top_fr, top_en = random.choice(_TOPPERS)

    if c is None:
        total   = a * b
        prompt_fr = (f"Tu as {a} choix de {name_fr} et {b} choix de {top_fr}. "
                     f"Combien de combinaisons différentes peux-tu faire ?")
        prompt_en = (f"You have {a} choices of {name_en} and {b} choices of {top_en}. "
                     f"How many different combinations can you make?")
        wrong_sum = a + b
        wrong2    = a * b - a
        wrong3    = a + b + 1
        wrong4    = total + b
    else:
        total   = a * b * c
        prompt_fr = (f"Tu as {a} {name_fr}, {b} {top_fr} et {c} boissons. "
                     f"Combien de repas différents peux-tu composer ?")
        prompt_en = (f"You have {a} {name_en}, {b} {top_en} and {c} drinks. "
                     f"How many different meals can you make?")
        wrong_sum = a + b + c
        wrong2    = a * b
        wrong3    = a * b * c - a
        wrong4    = total + 1

    tagged_candidates = [
        (str(wrong_sum), 'sum_not_product',
         'When combining independent choices, multiply — don\'t add.',
         'Quand on combine des choix indépendants, on multiplie — pas on additionne.'),
        (str(wrong2),    'forgot_category',
         'Did you use all the categories?',
         'As-tu utilisé toutes les catégories ?'),
        (str(wrong3),    'arithmetic_error',
         'Recheck your multiplication.',
         'Revérifie ta multiplication.'),
        (str(wrong4),    'off_by_one',
         'Count carefully.',
         'Compte soigneusement.'),
    ]
    tagged_candidates = [c for c in tagged_candidates if c[0] != str(total)]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Multiplie le nombre de choix de chaque catégorie.',
        'hint_en':          'Multiply the number of choices in each category.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(str(total), tagged_candidates[:4]),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Use the multiplication principle: multiply the number of choices in each category.\n'
            f'Step 2: {" × ".join(str(x) for x in ([a, b] if c is None else [a, b, c]))} = {total}.\n'
            f'Answer: {total} different combinations'
        ),
        'explanation_fr': (
            f'Étape 1 : Utilise le principe multiplicatif : multiplie le nombre de choix de chaque catégorie.\n'
            f'Étape 2 : {" × ".join(str(x) for x in ([a, b] if c is None else [a, b, c]))} = {total}.\n'
            f'Réponse : {total} combinaisons différentes'
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
    # What to find
    unknown = random.choice(['E', 'V', 'F'])

    if unknown == 'E':
        # V − E + F = 2 → E = V + F − 2
        correct = E
        prompt_fr = f"Un **{name_fr}** a {V} sommets et {F} faces. Combien a-t-il d'arêtes ?"
        prompt_en = f"A **{name_en}** has {V} vertices and {F} faces. How many edges does it have?"
        wrong1 = V + F
        wrong2 = V + F - 1
        wrong3 = V * F
    elif unknown == 'V':
        # E = V + F − 2 → V = E − F + 2
        correct = V
        prompt_fr = f"Un **{name_fr}** a {E} arêtes et {F} faces. Combien a-t-il de sommets ?"
        prompt_en = f"A **{name_en}** has {E} edges and {F} faces. How many vertices does it have?"
        wrong1 = E + F
        wrong2 = E - F
        wrong3 = E + F - 2
    else:
        # F = 2 − V + E
        correct = F
        prompt_fr = f"Un **{name_fr}** a {V} sommets et {E} arêtes. Combien a-t-il de faces ?"
        prompt_en = f"A **{name_en}** has {V} vertices and {E} edges. How many faces does it have?"
        wrong1 = E - V
        wrong2 = V + E - 2
        wrong3 = E + V

    tagged_candidates = [
        (str(wrong1), 'wrong_formula',
         'Use Euler\'s formula: V − E + F = 2.',
         'Utilise la relation d\'Euler : S − A + F = 2.'),
        (str(wrong2), 'sign_error',
         'Watch the signs in V − E + F = 2.',
         'Attention aux signes dans S − A + F = 2.'),
        (str(wrong3), 'wrong_operation',
         'Isolate the unknown with Euler\'s formula.',
         'Isole l\'inconnue avec la relation d\'Euler.'),
        (str(correct + 1), 'off_by_one',
         'Recheck your arithmetic.',
         'Recalcule soigneusement.'),
    ]
    tagged_candidates = [c for c in tagged_candidates if c[0] != str(correct)]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Relation d\'Euler pour les polyèdres convexes : Sommets − Arêtes + Faces = 2.',
        'hint_en':          'Euler\'s formula for convex polyhedra: Vertices − Edges + Faces = 2.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(str(correct), tagged_candidates[:4]),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Euler\'s formula: V − E + F = 2, where V = vertices, E = edges, F = faces.\n'
            f'Step 2: For a {name_en}: V={V}, E={E}, F={F}. Check: {V} − {E} + {F} = {V - E + F} ✓\n'
            f'Step 3: Isolate the unknown and calculate.\n'
            f'Answer: {correct}'
        ),
        'explanation_fr': (
            f'Étape 1 : Relation d\'Euler : S − A + F = 2, où S = sommets, A = arêtes, F = faces.\n'
            f'Étape 2 : Pour un {name_fr} : S={V}, A={E}, F={F}. Vérif : {V} − {E} + {F} = {V - E + F} ✓\n'
            f'Étape 3 : Isole l\'inconnue et calcule.\n'
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

    chosen = random.sample(pool, min(count, len(pool)))
    # Vary description: sometimes F/V/E, sometimes just faces
    pairs = []
    for name_fr, name_en, V, E, F in chosen:
        desc_kind = random.choice(['all', 'faces_edges'])
        if desc_kind == 'all':
            desc = f"{F} faces, {V} sommets, {E} arêtes"
            desc_en = f"{F} faces, {V} vertices, {E} edges"
        else:
            desc = f"{F} face{'s' if F > 1 else ''}, {E} arête{'s' if E > 1 else ''}"
            desc_en = f"{F} face{'s' if F > 1 else ''}, {E} edge{'s' if E > 1 else ''}"
        pairs.append({'left': name_fr, 'left_en': name_en, 'right': desc, 'right_en': desc_en})

    return {
        'q_type':           'mix_match',
        'prompt_fr':        'Associe chaque solide à ses caractéristiques (faces, sommets, arêtes).',
        'prompt_en':        'Match each solid to its properties (faces, vertices, edges).',
        'hint_fr':          'Un cube a 6 faces, 8 sommets et 12 arêtes. Vérifie la relation d\'Euler : S − A + F = 2.',
        'hint_en':          'A cube has 6 faces, 8 vertices, and 12 edges. Check Euler: V − E + F = 2.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            pairs,
        'explanation_en': (
            'Step 1: Recall key solids — cube: 6F/8V/12E; tetrahedron: 4F/4V/6E; square pyramid: 5F/5V/8E.\n'
            'Step 2: Use Euler\'s formula (V − E + F = 2) to verify each match.\n'
            'Step 3: Match each solid name to its face/vertex/edge count.'
        ),
        'explanation_fr': (
            'Étape 1 : Rappelle-toi les solides clés — cube : 6F/8S/12A ; tétraèdre : 4F/4S/6A ; pyramide carrée : 5F/5S/8A.\n'
            'Étape 2 : Utilise la relation d\'Euler (S − A + F = 2) pour vérifier chaque association.\n'
            'Étape 3 : Associe chaque nom de solide à ses caractéristiques.'
        ),
        'correct_answers':  [p['right'] for p in pairs],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_pie_chart_gen
# ─────────────────────────────────────────────────────────────────────────────

_PIE_CONTEXTS = [
    (['Chat', 'Chien', 'Oiseau'],            "animaux préférés",  "favourite animals"),
    (['Rouge', 'Bleu', 'Vert', 'Jaune'],     "couleurs préférées","favourite colours"),
    (['Football', 'Basketball', 'Natation'], "sports pratiqués",  "sports"),
    (['Été', 'Automne', 'Hiver', 'Printemps'], "saisons préférées","favourite seasons"),
]


def g5_pie_chart_gen(level='easy'):
    """QCM + SVG — read a pie chart (ask largest, smallest, or percentage)."""
    cats_list, ctx_fr, ctx_en = random.choice(_PIE_CONTEXTS)
    n_cats = 3 if level == 'easy' else len(cats_list)
    cats   = cats_list[:n_cats]

    # Generate proportions that sum to 100 (percentages)
    for _ in range(100):
        props = [random.randint(5, 50) for _ in range(n_cats - 1)]
        last  = 100 - sum(props)
        if 5 <= last <= 50:
            props.append(last)
            break
    else:
        props = [round(100 / n_cats)] * (n_cats - 1)
        props.append(100 - sum(props))

    q_type = random.choice(['largest', 'pct_of'])

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
    else:
        idx     = random.randint(0, n_cats - 1)
        correct = str(props[idx]) + ' %'
        prompt_fr = f"D'après le diagramme circulaire des {ctx_fr}, quel pourcentage représente « {cats[idx]} » ?"
        prompt_en = f"According to the pie chart about {ctx_en}, what percentage does '{_L(cats[idx], 'en')}' represent?"
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
        'hint_fr':          'Lis le pourcentage de chaque secteur et compare-les.',
        'hint_en':          'Read the percentage of each sector and compare them.',
        'show_illustration': True,
        'shape_data':       [{
            'type':        'pie_chart_multi',
            'categories':  cats,
            'proportions': props,
        }],
        'choices':          _tagged_shuffle_mc(str(correct), tagged_candidates[:4]),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Identify each sector in the pie chart and its percentage label.\n'
            f'Step 2: Find the sector for the category asked.\n'
            f'Answer: {_L(correct, 'en')}'
        ),
        'explanation_fr': (
            f'Étape 1 : Identifie chaque secteur du diagramme circulaire et son pourcentage.\n'
            f'Étape 2 : Repère le secteur correspondant à la catégorie demandée.\n'
            f'Réponse : {correct}'
        ),
        'correct_answers':  [str(correct)],
    }
