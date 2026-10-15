"""
stats_plus.py — curriculum upgrade WP7 (statistics), 2026-10.

Pictographs with a key, line graphs, tallying raw data, matching a table to its
bar chart, and choosing a good survey question.
"""
import random

from quiz import illustrations as I
from .kit import mc, typed, pick

L5 = list('ABCDE')

TOPICS = [
    # (question fr, question en, people fr, people en, categories)
    ('Quel est ton fruit préféré ?', 'What is your favourite fruit?', 'élèves', 'students',
     [('Pommes', 'Apples'), ('Bananes', 'Bananas'), ('Raisins', 'Grapes'), ('Fraises', 'Strawberries'), ('Poires', 'Pears')]),
    ('Quel est ton sport préféré ?', 'What is your favourite sport?', 'élèves', 'students',
     [('Soccer', 'Soccer'), ('Hockey', 'Hockey'), ('Natation', 'Swimming'), ('Basket', 'Basketball'), ('Vélo', 'Cycling')]),
    ('Quel animal aimerais-tu avoir ?', 'Which pet would you like?', 'enfants', 'children',
     [('Chien', 'Dog'), ('Chat', 'Cat'), ('Lapin', 'Rabbit'), ('Poisson', 'Fish'), ('Oiseau', 'Bird')]),
    ('Comment viens-tu à l’école ?', 'How do you get to school?', 'élèves', 'students',
     [('À pied', 'Walk'), ('Autobus', 'Bus'), ('Voiture', 'Car'), ('Vélo', 'Bike'), ('Métro', 'Subway')]),
]
ICONS = ['⭐', '🙂', '⚽', '🍎', '🐾']


def _topic(n):
    q_fr, q_en, p_fr, p_en, cats = pick(TOPICS)
    return q_fr, q_en, p_fr, p_en, random.sample(cats, n)


def _distinct_vals(n, choices):
    return random.sample(choices, n)


# ── G3 · Pictograph ──────────────────────────────────────────────────────────

def g3_pictograph_gen(level='easy'):
    """Read a pictograph with a key (212, 218)."""
    n = 3 if level == 'easy' else 4
    q_fr, q_en, p_fr, p_en, cats = _topic(n)
    icon = pick(ICONS)
    if level == 'easy':
        per = 2
        vals = _distinct_vals(n, list(range(2, 15, 2)))
    elif level == 'medium':
        per = 5
        vals = _distinct_vals(n, list(range(5, 41, 5)))
    else:
        per = pick([4, 10])
        vals = _distinct_vals(n, list(range(per // 2, per * 6 + 1, per // 2)))
    pic = I.pictograph(cats, vals, icon, per)
    key = (f'Chaque {icon} vaut {per} {p_fr}' + (' ; un demi-symbole vaut la moitié.' if level == 'hard' else '.'),
           f'Each {icon} stands for {per} {p_en}' + ('; half a symbol is half of that.' if level == 'hard' else '.'))
    i, j = random.sample(range(n), 2)
    ask = 'one' if level == 'easy' else pick(['one', 'diff', 'total'])
    if ask == 'one':
        return typed((f'Sondage : « {q_fr} » {key[0]} Combien de {p_fr} ont choisi **{cats[i][0]}** ?',
                      f'Survey: “{q_en}” {key[1]} How many {p_en} chose **{cats[i][1]}**?'),
                     [vals[i]], 'integer',
                     (f'Compte les symboles de la ligne, puis multiplie par {per}.', f'Count the symbols in the row, then multiply by {per}.'),
                     ([f'{vals[i] / per:g} symboles × {per} = {vals[i]}'.replace('.', ',')], [f'{vals[i] / per:g} symbols × {per} = {vals[i]}']),
                     shape=pic)
    if ask == 'diff':
        a, b = (i, j) if vals[i] > vals[j] else (j, i)
        return typed((f'Sondage : « {q_fr} » {key[0]} Combien de {p_fr} de plus ont choisi **{cats[a][0]}** plutôt que **{cats[b][0]}** ?',
                      f'Survey: “{q_en}” {key[1]} How many more {p_en} chose **{cats[a][1]}** than **{cats[b][1]}**?'),
                     [vals[a] - vals[b]], 'integer',
                     ('Trouve les deux nombres, puis soustrais.', 'Find both numbers, then subtract.'),
                     (f'{vals[a]} − {vals[b]} = {vals[a] - vals[b]}', f'{vals[a]} − {vals[b]} = {vals[a] - vals[b]}'),
                     shape=pic)
    total = sum(vals)
    return typed((f'Sondage : « {q_fr} » {key[0]} Combien de {p_fr} ont répondu en tout ?',
                  f'Survey: “{q_en}” {key[1]} How many {p_en} answered in all?'),
                 [total], 'integer',
                 ('Trouve le nombre de chaque ligne, puis additionne.', 'Find the number for each row, then add.'),
                 (f'{" + ".join(map(str, vals))} = {total}', f'{" + ".join(map(str, vals))} = {total}'),
                 shape=pic)


# ── G4 · Line graph ──────────────────────────────────────────────────────────

DAYS = [('lun', 'Mon'), ('mar', 'Tue'), ('mer', 'Wed'), ('jeu', 'Thu'), ('ven', 'Fri'), ('sam', 'Sat')]
DAYS_FULL = [('lundi', 'Monday'), ('mardi', 'Tuesday'), ('mercredi', 'Wednesday'), ('jeudi', 'Thursday'),
             ('vendredi', 'Friday'), ('samedi', 'Saturday')]


def _series(kind, n):
    if kind == 'temp':
        while True:
            v = [random.randint(4, 28) for _ in range(n)]
            ups = [v[k + 1] - v[k] for k in range(n - 1)]
            if len(set(v)) == n and max(ups) > 0 and ups.count(max(ups)) == 1:
                return v
    if kind == 'plant':
        v, h = [], random.randint(1, 4)
        for _ in range(n):
            v.append(h)
            h += random.randint(1, 5)
        ups = [v[k + 1] - v[k] for k in range(n - 1)]
        return v if ups.count(max(ups)) == 1 else _series(kind, n)
    while True:
        v = [random.randint(2, 18) * 5 for _ in range(n)]
        ups = [v[k + 1] - v[k] for k in range(n - 1)]
        if len(set(v)) == n and max(ups) > 0 and ups.count(max(ups)) == 1:
            return v


def g4_line_graph_gen(level='easy'):
    """Read and compare a broken-line graph (213, 219)."""
    n = 5 if level != 'hard' else 6
    kind = pick(['temp', 'plant', 'visits'])
    vals = _series(kind, n)
    if kind == 'temp':
        xs, full, what, unit, step = DAYS[:n], DAYS_FULL[:n], ('la température à midi', 'the temperature at noon'), '°C', 5
        where = [(f'le {d[0]}', f'on {d[1]}') for d in full]
    elif kind == 'plant':
        xs = [(f'S{k + 1}', f'W{k + 1}') for k in range(n)]
        full = [(f'semaine {k + 1}', f'week {k + 1}') for k in range(n)]
        what, unit, step = ('la hauteur d’une plante', 'the height of a plant'), 'cm', 5 if max(vals) > 20 else 2
        where = [(f'à la semaine {k + 1}', f'in week {k + 1}') for k in range(n)]
    else:
        xs, full, what, unit, step = DAYS[:n], DAYS_FULL[:n], ('le nombre de visiteurs à la bibliothèque', 'the number of library visitors'), '', 10
        where = [(f'le {d[0]}', f'on {d[1]}') for d in full]
    pic = I.line_graph(xs, vals, step=step, unit=unit)
    intro = (f'Ce diagramme à ligne brisée montre {what[0]}.', f'This line graph shows {what[1]}.')
    u = f' {unit}' if unit else ''
    if level == 'easy':
        i = random.randrange(n)
        return typed((f'{intro[0]} Quelle est la valeur {where[i][0]} ?', f'{intro[1]} What is the value {where[i][1]}?'),
                     [vals[i]], 'integer',
                     ('Trouve le point au-dessus du jour, puis suis la ligne horizontale jusqu’à l’axe.', 'Find the point above the day, then follow across to the axis.'),
                     (f'Le point {where[i][0]} est à {vals[i]}{u}.', f'The point {where[i][1]} is at {vals[i]}{u}.'), shape=pic)
    if level == 'medium':
        i, j = sorted(random.sample(range(n), 2))
        d = abs(vals[j] - vals[i])
        return typed((f'{intro[0]} Quel est l’écart entre {where[i][0]} et {where[j][0]} ?',
                      f'{intro[1]} What is the difference between {where[i][1]} and {where[j][1]}?'),
                     [d], 'integer',
                     ('Lis les deux valeurs, puis soustrais la plus petite de la plus grande.', 'Read both values, then subtract the smaller from the larger.'),
                     (f'{max(vals[i], vals[j])} − {min(vals[i], vals[j])} = {d}{u}', f'{max(vals[i], vals[j])} − {min(vals[i], vals[j])} = {d}{u}'),
                     shape=pic)
    ups = [vals[k + 1] - vals[k] for k in range(n - 1)]
    k = ups.index(max(ups))
    pair = lambda a: (f'entre {full[a][0]} et {full[a + 1][0]}', f'between {full[a][1]} and {full[a + 1][1]}')
    return mc((f'{intro[0]} Entre quels moments la hausse est-elle la plus forte ?', f'{intro[1]} When is the biggest rise?'),
              pair(k), [pair(a) for a in range(n - 1) if a != k],
              ('La plus forte hausse correspond au segment qui monte le plus raide.', 'The biggest rise is the segment that climbs most steeply.'),
              (f'De {vals[k]} à {vals[k + 1]} : +{ups[k]}{u}, c’est la plus forte hausse.', f'From {vals[k]} to {vals[k + 1]}: +{ups[k]}{u}, the biggest rise.'),
              shape=pic)


# ── G3 · Tally and organise data ─────────────────────────────────────────────

EMOJI_SETS = [
    [('🍎', 'pommes', 'apples'), ('🍌', 'bananes', 'bananas'), ('🍇', 'raisins', 'grapes'), ('🍓', 'fraises', 'strawberries')],
    [('🐶', 'chiens', 'dogs'), ('🐱', 'chats', 'cats'), ('🐰', 'lapins', 'rabbits'), ('🐟', 'poissons', 'fish')],
    [('⚽', 'ballons de soccer', 'soccer balls'), ('🏀', 'ballons de basket', 'basketballs'), ('🎾', 'balles de tennis', 'tennis balls'), ('🏈', 'ballons de football', 'footballs')],
]


def _raw_data_pic(items, per_row=8):
    rows = -(-len(items) // per_row)
    c = I.Canvas(per_row * 30 + 12, rows * 32 + 10, max_h=rows * 36 + 20, css_w='max-w-sm')
    for k, e in enumerate(items):
        c.text(20 + (k % per_row) * 30, 28 + (k // per_row) * 32, e, size=22)
    return c.shape()


def _tally_pic(rows):
    """rows: [(label (fr, en), count)] drawn with tally marks in bundles of five."""
    c = I.Canvas(300, len(rows) * 34 + 12, max_h=len(rows) * 38 + 20, css_w='max-w-sm')
    for r, (lab, n) in enumerate(rows):
        y = 8 + r * 34
        c.rect(4, y, 292, 30, fill='#F8FAFC', stroke=I.SOFT, sw=1)
        c.text(14, y + 20, lab[0], size=13, bold=True, anchor='start', text_en=lab[1])
        x = 120
        for b in range(n // 5 + (1 if n % 5 else 0)):
            k = min(5, n - b * 5)
            for t in range(min(k, 4)):
                c.line(x + t * 7, y + 5, x + t * 7, y + 25, color=I.INK, sw=2)
            if k == 5:
                c.line(x - 4, y + 22, x + 25, y + 8, color=I.INK, sw=2)
            x += 40
    return c.shape()


def g3_tally_table_gen(level='easy'):
    """Collect, count and organise data in a table (211)."""
    kinds = random.sample(pick(EMOJI_SETS), 3)
    if level == 'medium':
        rows = [((k[1].capitalize(), k[2].capitalize()), random.randint(3, 17)) for k in kinds]
        i = random.randrange(3)
        n = rows[i][1]
        return typed((f'Ce tableau de dépouillement compte des votes. Combien de votes pour **{rows[i][0][0]}** ?',
                      f'This tally chart counts votes. How many votes for **{rows[i][0][1]}**?'),
                     [n], 'integer',
                     ('Chaque paquet barré vaut 5. Compte les paquets de 5, puis les traits qui restent.', 'Each crossed bundle is 5. Count the fives, then the extra marks.'),
                     ([f'{n // 5} paquets de 5 = {n // 5 * 5}, plus {n % 5} → {n}'], [f'{n // 5} bundles of 5 = {n // 5 * 5}, plus {n % 5} → {n}']),
                     shape=_tally_pic(rows))
    counts = random.sample(range(2, 8 if level == 'easy' else 10), 3)
    items = [k[0] for k, c in zip(kinds, counts) for _ in range(c)]
    random.shuffle(items)
    pic = _raw_data_pic(items)
    if level == 'easy':
        i = random.randrange(3)
        return typed((f'Combien y a-t-il de {kinds[i][1]} {kinds[i][0]} ?', f'How many {kinds[i][2]} {kinds[i][0]} are there?'),
                     [counts[i]], 'integer',
                     ('Pointe chaque objet avec ton doigt et barre-le dans ta tête pour ne pas le compter deux fois.',
                      'Touch each object and cross it off in your head so you do not count it twice.'),
                     (f'Il y a {counts[i]} {kinds[i][0]}.', f'There are {counts[i]} {kinds[i][0]}.'), shape=pic)
    label = lambda cs: (' · '.join(f'{k[0]} {c}' for k, c in zip(kinds, cs)),) * 2
    correct = label(counts)
    wrong = []
    for d in ([1, 0, 0], [0, -1, 0], [0, 0, 1], [-1, 1, 0], [0, 1, -1], [1, -1, 0]):
        cs = [c + x for c, x in zip(counts, d)]
        wrong.append(label(cs))
    wrong.append(label([counts[1], counts[0], counts[2]]))
    return mc(('Quel tableau organise correctement ces données ?', 'Which table organises this data correctly?'),
              correct, wrong,
              ('Compte une sorte d’objet à la fois.', 'Count one kind of object at a time.'),
              (f'On compte : {correct[0]}.', f'Counting gives: {correct[1]}.'), shape=pic)


# ── G3 · Which chart shows this table? ───────────────────────────────────────

def g3_build_chart_gen(level='easy'):
    """Represent data: pick the bar chart that matches a table (215, 216)."""
    n = 3 if level == 'easy' else 4
    q_fr, q_en, p_fr, p_en, cats = _topic(n)
    step = 1 if level == 'easy' else 2
    vals = random.sample(range(1, 9) if level == 'easy' else range(2, 17), n)
    short = [(c[0][:4] + '.' if len(c[0]) > 5 else c[0], c[1][:4] + '.' if len(c[1]) > 5 else c[1]) for c in cats]
    table = ' · '.join(f'{c[0]} : {v}' for c, v in zip(cats, vals)), ' · '.join(f'{c[1]}: {v}' for c, v in zip(cats, vals))
    variants = [vals]
    tries = 0
    while len(variants) < 5 and tries < 200:
        tries += 1
        v = list(vals)
        how = random.randrange(3)
        if how == 0:
            a, b = random.sample(range(n), 2)
            v[a], v[b] = v[b], v[a]
        elif how == 1:
            a = random.randrange(n)
            v[a] += random.choice([-step, step]) if v[a] > step else step
        else:
            a = random.randrange(n)
            v[a] += random.choice([-1, 1]) * (2 if level == 'easy' else 3)
            v[a] = max(1, v[a])
        if v not in variants:
            variants.append(v)
    order = list(range(5))
    random.shuffle(order)
    top = max(max(v) for v in variants)
    c, boxes = I.panels(5, 150, 120, cols=3, css_w='max-w-xl')
    for j, box in zip(order, boxes):
        I.draw_bar_chart(c, box, short, variants[j], color=I.BLUE, step=step if level == 'easy' else 2, top=top, small=True)
    i = order.index(0)
    return mc((f'Sondage « {q_fr} » — résultats : {table[0]}. Quel diagramme à bandes représente ces résultats ?',
               f'Survey “{q_en}” — results: {table[1]}. Which bar chart shows these results?'),
              L5[i], [x for x in L5 if x != L5[i]],
              ('Vérifie chaque bande : sa hauteur doit correspondre au nombre du tableau.', 'Check each bar: its height must match the number in the table.'),
              (f'Le diagramme {L5[i]} : chaque bande a la bonne hauteur.', f'Chart {L5[i]}: every bar has the right height.'),
              shape=c.shape())


# ── G4 · Survey questions ────────────────────────────────────────────────────

SURVEYS = [
    (('Tu veux savoir quel sport tes camarades préfèrent.', 'You want to find out which sport your classmates like best.'),
     ('Quel est ton sport préféré : soccer, hockey, natation ou basket ?', 'What is your favourite sport: soccer, hockey, swimming or basketball?'),
     [('Aimes-tu le sport ?', 'Do you like sport?'),
      ('Le hockey est le meilleur sport, n’est-ce pas ?', 'Hockey is the best sport, isn’t it?'),
      ('Combien de sports existe-t-il dans le monde ?', 'How many sports are there in the world?'),
      ('Quel est le sport préféré de la directrice ?', 'What is the principal’s favourite sport?')]),
    (('Tu veux savoir comment les élèves viennent à l’école.', 'You want to find out how students get to school.'),
     ('Comment viens-tu à l’école le plus souvent : à pied, en autobus, en voiture ou à vélo ?', 'How do you usually get to school: walk, bus, car or bike?'),
     [('Est-ce que l’autobus est jaune ?', 'Is the school bus yellow?'),
      ('Marcher, c’est meilleur pour la santé, non ?', 'Walking is healthier, right?'),
      ('À quelle heure commence l’école ?', 'What time does school start?'),
      ('Ton voisin vient-il en voiture ?', 'Does your neighbour come by car?')]),
    (('Tu veux choisir la saveur de crème glacée pour la fête de la classe.', 'You want to choose the ice-cream flavour for the class party.'),
     ('Quelle saveur préfères-tu : vanille, chocolat ou fraise ?', 'Which flavour do you prefer: vanilla, chocolate or strawberry?'),
     [('Aimes-tu la crème glacée ?', 'Do you like ice cream?'),
      ('Le chocolat, c’est délicieux, tu ne trouves pas ?', 'Chocolate is delicious, don’t you think?'),
      ('Combien coûte un cornet ?', 'How much does a cone cost?'),
      ('Quelle saveur préfère ton enseignante ?', 'Which flavour does your teacher prefer?')]),
    (('Tu veux savoir combien de temps les élèves lisent chaque soir.', 'You want to know how long students read each evening.'),
     ('Combien de minutes lis-tu un soir d’école : moins de 10, de 10 à 30, ou plus de 30 ?', 'How many minutes do you read on a school night: under 10, 10 to 30, or over 30?'),
     [('Aimes-tu lire ?', 'Do you like reading?'),
      ('Lire, c’est important, n’est-ce pas ?', 'Reading is important, isn’t it?'),
      ('Quel est le titre de ton livre ?', 'What is the title of your book?'),
      ('Combien de livres y a-t-il à la bibliothèque ?', 'How many books are in the library?')]),
    (('Tu veux savoir quel animal de compagnie les familles de ta classe ont.', 'You want to know which pets the families in your class have.'),
     ('Quel animal as-tu à la maison : chien, chat, poisson, autre ou aucun ?', 'Which pet do you have at home: dog, cat, fish, other or none?'),
     [('Aimes-tu les animaux ?', 'Do you like animals?'),
      ('Les chats sont plus gentils que les chiens, non ?', 'Cats are nicer than dogs, right?'),
      ('Combien de pattes a un chien ?', 'How many legs does a dog have?'),
      ('Quel animal a ton cousin ?', 'Which pet does your cousin have?')]),
]
WHY_BAD = [('Oui/non ne dit pas lequel ils préfèrent.', 'Yes/no does not tell which one they prefer.'),
           ('Cette question pousse vers une réponse : elle n’est pas neutre.', 'This question pushes towards one answer: it is not neutral.'),
           ('Cette question ne porte pas sur les élèves interrogés.', 'This question is not about the people asked.'),
           ('Elle ne concerne qu’une seule personne.', 'It is only about one person.')]

POPULATIONS = [
    (('Tu veux savoir quel jeu les élèves de 4e année préfèrent à la récréation.', 'You want to know which recess game grade 4 students prefer.'),
     ('les élèves de 4e année', 'the grade 4 students'),
     [('tes parents', 'your parents'), ('les élèves de maternelle seulement', 'kindergarten students only'),
      ('ton meilleur ami seulement', 'only your best friend'), ('les enseignants', 'the teachers')]),
    (('Tu veux savoir quels livres les parents de l’école aimeraient voir à la bibliothèque.', 'You want to know which library books the school’s parents would like.'),
     ('des parents d’élèves de l’école', 'parents of students at the school'),
     [('les élèves de ta classe', 'the students in your class'), ('la bibliothécaire seulement', 'only the librarian'),
      ('tes voisins', 'your neighbours'), ('les joueurs de hockey de la ville', 'the town’s hockey players')]),
]


def g4_survey_question_gen(level='easy'):
    """Formulate survey questions: a fair, countable question; who to ask (210)."""
    if level == 'hard' and random.random() < 0.5:
        goal, right, wrong = pick(POPULATIONS)
        return mc((f'{goal[0]} À qui dois-tu poser ta question ?', f'{goal[1]} Who should you ask?'),
                  right, wrong,
                  ('On interroge les personnes concernées par la question, et pas une seule.', 'Ask the people the question is about, and not just one person.'),
                  (f'Il faut demander à {right[0]}.', f'You should ask {right[1]}.'))
    goal, right, wrong = pick(SURVEYS)
    if level == 'easy':
        wrong = wrong[:1] + wrong[2:]          # leave out the subtle « leading » distractor
        wrong.append(('Quelle heure est-il ?', 'What time is it?'))
    return mc((f'{goal[0]} Quelle question est la meilleure pour ton sondage ?', f'{goal[1]} Which question is best for your survey?'),
              right, [(w, 'bad_question', WHY_BAD[k % 4][1], WHY_BAD[k % 4][0]) for k, w in enumerate(wrong)],
              ('Une bonne question de sondage est neutre, s’adresse à chaque personne et propose des réponses faciles à compter.',
               'A good survey question is neutral, is asked to each person, and gives answers that are easy to count.'),
              (f'« {right[0]} » : neutre, et les réponses se comptent facilement.', f'“{right[1]}”: neutral, and the answers are easy to count.'))
