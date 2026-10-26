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
# Key symbols unrelated to every survey topic (no 🍎 on a fruit survey, no ⚽ on a sport one).
ICONS = ['⭐', '🙂', '💜']


def _topic(n):
    q_fr, q_en, p_fr, p_en, cats = pick(TOPICS)
    return q_fr, q_en, p_fr, p_en, random.sample(cats, n)


def _distinct_vals(n, choices):
    return random.sample(choices, n)


def _de(word):
    """French « de » with elision: « d’élèves », « de garçons »."""
    return f'd’{word}' if word[0] in 'aeiouéèh' else f'de {word}'


def _symbols(count, lang):
    """count symbols as words: 1 symbole, 2 symboles, 3,5 symboles / 1 symbol, 3.5 symbols."""
    s = f'{count:g}'
    if lang == 'fr':
        return f"{s.replace('.', ',')} symbole{'s' if count >= 2 else ''}"
    return f"{s} symbol{'s' if count != 1 else ''}"


# ── G3 · Pictograph ──────────────────────────────────────────────────────────

def g3_pictograph_gen(level='easy'):
    """Read a pictograph with a key (212, 218)."""
    n = 3 if level == 'easy' else 4
    q_fr, q_en, p_fr, p_en, cats = _topic(n)
    if level == 'easy':
        per, icon = 2, pick(ICONS)
        vals = _distinct_vals(n, list(range(2, 15, 2)))
    elif level == 'medium':
        per, icon = 5, pick(ICONS)
        vals = _distinct_vals(n, list(range(5, 41, 5)))
    else:
        # half symbols are drawn as half discs, so the key symbol is a disc too
        per, icon = pick([4, 10]), '🔵'
        vals = _distinct_vals(n, list(range(per // 2, per * 6 + 1, per // 2)))
    halves = level == 'hard'
    pic = I.pictograph(cats, vals, icon, per, half_ok=halves)
    key = (f'Chaque {icon} vaut {per} {p_fr}' + (' ; un demi-symbole vaut la moitié.' if halves else '.'),
           f'Each {icon} stands for {per} {p_en}' + ('; half a symbol is half of that.' if halves else '.'))
    half_tip = ((f' Un demi-symbole vaut {per // 2}.', f' Half a symbol is worth {per // 2}.') if halves else ('', ''))

    def reading(v):
        """How the number of a row is found: '3,5 symboles × 4 = 14' (fr, en)."""
        k = v / per
        return (f'{_symbols(k, "fr")} × {per} = {v}', f'{_symbols(k, "en")} × {per} = {v}')

    i, j = random.sample(range(n), 2)
    ask = 'one' if level == 'easy' else pick(['one', 'diff', 'total'])
    if ask == 'one':
        r = reading(vals[i])
        return typed((f'Sondage : « {q_fr} » {key[0]} Combien {_de(p_fr)} ont choisi **{cats[i][0]}** ?',
                      f'Survey: “{q_en}” {key[1]} How many {p_en} chose **{cats[i][1]}**?'),
                     [vals[i]], 'integer',
                     (f'Compte les symboles de la ligne, puis multiplie par {per}.{half_tip[0]}',
                      f'Count the symbols in the row, then multiply by {per}.{half_tip[1]}'),
                     ([r[0]], [r[1]]),
                     shape=pic)
    if ask == 'diff':
        a, b = (i, j) if vals[i] > vals[j] else (j, i)
        ra, rb = reading(vals[a]), reading(vals[b])
        return typed((f'Sondage : « {q_fr} » {key[0]} Combien {_de(p_fr)} de plus ont choisi **{cats[a][0]}** plutôt que **{cats[b][0]}** ?',
                      f'Survey: “{q_en}” {key[1]} How many more {p_en} chose **{cats[a][1]}** than **{cats[b][1]}**?'),
                     [vals[a] - vals[b]], 'integer',
                     (f'Trouve le nombre de chaque ligne (symboles × {per}), puis soustrais.{half_tip[0]}',
                      f'Find the number for each row (symbols × {per}), then subtract.{half_tip[1]}'),
                     ([f'{cats[a][0]} : {ra[0]}', f'{cats[b][0]} : {rb[0]}', f'{vals[a]} − {vals[b]} = {vals[a] - vals[b]}'],
                      [f'{cats[a][1]}: {ra[1]}', f'{cats[b][1]}: {rb[1]}', f'{vals[a]} − {vals[b]} = {vals[a] - vals[b]}']),
                     shape=pic)
    total = sum(vals)
    return typed((f'Sondage : « {q_fr} » {key[0]} Combien {_de(p_fr)} ont répondu en tout ?',
                  f'Survey: “{q_en}” {key[1]} How many {p_en} answered in all?'),
                 [total], 'integer',
                 (f'Trouve le nombre de chaque ligne (symboles × {per}), puis additionne.{half_tip[0]}',
                  f'Find the number for each row (symbols × {per}), then add.{half_tip[1]}'),
                 ([f'{c[0]} : {reading(v)[0]}' for c, v in zip(cats, vals)] + [f'{" + ".join(map(str, vals))} = {total}'],
                  [f'{c[1]}: {reading(v)[1]}' for c, v in zip(cats, vals)] + [f'{" + ".join(map(str, vals))} = {total}']),
                 shape=pic)


# ── G4 · Line graph ──────────────────────────────────────────────────────────

DAYS = [('lun', 'Mon'), ('mar', 'Tue'), ('mer', 'Wed'), ('jeu', 'Thu'), ('ven', 'Fri'), ('sam', 'Sat')]
DAYS_FULL = [('lundi', 'Monday'), ('mardi', 'Tuesday'), ('mercredi', 'Wednesday'), ('jeudi', 'Thursday'),
             ('vendredi', 'Friday'), ('samedi', 'Saturday')]


def _series(kind, n):
    """Values that all sit exactly on a gridline of the graph (see g4_line_graph_gen)."""
    while True:
        if kind == 'temp':
            v = [random.randint(2, 14) * 2 for _ in range(n)]          # even: gridline every 2 °C
        elif kind == 'plant':
            v, h = [], random.randint(1, 3)                             # gridline every cm
            for _ in range(n):
                v.append(h)
                h += random.randint(1, 4)
        else:
            v = [random.randint(2, 9) * 10 for _ in range(n)]           # gridline every 10 visitors
        ups = [v[k + 1] - v[k] for k in range(n - 1)]
        if len(set(v)) == n and max(ups) > 0 and ups.count(max(ups)) == 1:
            return v


def g4_line_graph_gen(level='easy'):
    """Read and compare a broken-line graph (213, 219)."""
    n = 5 if level != 'hard' else 6
    kind = pick(['temp', 'plant', 'visits'])
    vals = _series(kind, n)
    # step = one gridline per possible value, so every point sits exactly on a gridline
    if kind == 'temp':
        xs, full, unit, step, every = DAYS[:n], DAYS_FULL[:n], '°C', 2, 4
        what = ('la température à midi', 'the temperature at noon')
        on = [(f'le {d[0]}', f'on {d[1]}') for d in full]
        ask_one = [(f'Quelle température faisait-il à midi {o[0]} ?', f'What was the temperature at noon {o[1]}?') for o in on]
        gap = ('de température', 'in temperature')
        between = ('Entre quels jours', 'Between which two days')
        pair_of = lambda a, b=None: (f'entre le {full[a][0]} et le {full[a + 1 if b is None else b][0]}', f'between {full[a][1]} and {full[a + 1 if b is None else b][1]}')
    elif kind == 'plant':
        xs = [(f'S{k + 1}', f'W{k + 1}') for k in range(n)]
        full = [(f'semaine {k + 1}', f'week {k + 1}') for k in range(n)]
        unit, step, every = 'cm', 1, 5
        what = ('la hauteur d’une plante, semaine après semaine', 'the height of a plant, week by week')
        on = [(f'à la semaine {k + 1}', f'in week {k + 1}') for k in range(n)]
        ask_one = [(f'Quelle était la hauteur de la plante {o[0]} ?', f'How tall was the plant {o[1]}?') for o in on]
        gap = ('de hauteur', 'in height')
        between = ('Entre quelles semaines', 'Between which two weeks')
        pair_of = lambda a, b=None: (f'entre la {full[a][0]} et la {full[a + 1 if b is None else b][0]}', f'between {full[a][1]} and {full[a + 1 if b is None else b][1]}')
    else:
        xs, full, unit, step, every = DAYS[:n], DAYS_FULL[:n], '', 10, 10
        what = ('le nombre de visiteurs à la bibliothèque', 'the number of library visitors')
        on = [(f'le {d[0]}', f'on {d[1]}') for d in full]
        ask_one = [(f'Combien de visiteurs sont venus à la bibliothèque {o[0]} ?', f'How many visitors came to the library {o[1]}?') for o in on]
        gap = ('du nombre de visiteurs', 'in the number of visitors')
        between = ('Entre quels jours', 'Between which two days')
        pair_of = lambda a, b=None: (f'entre le {full[a][0]} et le {full[a + 1 if b is None else b][0]}', f'between {full[a][1]} and {full[a + 1 if b is None else b][1]}')
    pic = I.line_graph(xs, vals, step=step, unit=unit, label_every=every)
    intro = (f'Ce diagramme à ligne brisée montre {what[0]}.', f'This line graph shows {what[1]}.')
    grid = ((f' Chaque ligne de la grille vaut {step} {unit}.'.replace(' .', '.'), f' Each gridline is worth {step} {unit}.'.replace(' .', '.'))
            if every != step else ('', ''))
    u = f' {unit}' if unit else ''
    if level == 'easy':
        i = random.randrange(n)
        x_fr, x_en = xs[i]
        return typed((f'{intro[0]} {ask_one[i][0]}', f'{intro[1]} {ask_one[i][1]}'),
                     [vals[i]], 'integer',
                     (f'Trouve le point au-dessus de « {x_fr} », puis suis la ligne horizontale jusqu’à l’axe vertical.{grid[0]}',
                      f'Find the point above “{x_en}”, then follow the gridline across to the vertical axis.{grid[1]}'),
                     (f'Le point au-dessus de « {x_fr} » est vis-à-vis de {vals[i]}{u} sur l’axe vertical.', f'The point above “{x_en}” is at {vals[i]}{u}.'), shape=pic)
    if level == 'medium':
        i, j = sorted(random.sample(range(n), 2))
        d = abs(vals[j] - vals[i])
        span = pair_of(i, j)
        return typed((f'{intro[0]} Quel est l’écart {gap[0]} {span[0]} ?',
                      f'{intro[1]} What is the difference {gap[1]} {span[1]}?'),
                     [d], 'integer',
                     (f'Lis les deux valeurs, puis soustrais la plus petite de la plus grande.{grid[0]}',
                      f'Read both values, then subtract the smaller from the larger.{grid[1]}'),
                     (f'{on[i][0][0].upper()}{on[i][0][1:]} : {vals[i]}{u} ; {on[j][0]} : {vals[j]}{u}. '
                      f'{max(vals[i], vals[j])} − {min(vals[i], vals[j])} = {d}{u}',
                      f'{on[i][1][0].upper()}{on[i][1][1:]}: {vals[i]}{u}; {on[j][1]}: {vals[j]}{u}. '
                      f'{max(vals[i], vals[j])} − {min(vals[i], vals[j])} = {d}{u}'),
                     shape=pic)
    ups = [vals[k + 1] - vals[k] for k in range(n - 1)]
    k = ups.index(max(ups))
    p = pair_of(k)
    return mc((f'{intro[0]} {between[0]} la hausse est-elle la plus forte ?', f'{intro[1]} {between[1]} is the biggest rise?'),
              p, [pair_of(a) for a in range(n - 1) if a != k],
              ('La plus forte hausse correspond au segment qui monte le plus raide.', 'The biggest rise is the segment that climbs most steeply.'),
              (f'{p[0][0].upper()}{p[0][1:]} : de {vals[k]} à {vals[k + 1]}{u}, soit +{ups[k]}{u}, c’est la plus forte hausse.',
               f'{p[1][0].upper()}{p[1][1:]}: from {vals[k]} to {vals[k + 1]}{u}, that is +{ups[k]}{u}, the biggest rise.'),
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
    return mc(('Quelle ligne de résultats donne le bon nombre de chaque sorte d’objet ?',
               'Which line of results gives the right count for each kind of object?'),
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
    table = {'headers': [('Réponse', 'Answer'), (f'Nombre {_de(p_fr)}', f'Number of {p_en}')],
             'rows': [[c, str(v)] for c, v in zip(cats, vals)]}
    if level == 'hard' or (level == 'medium' and random.random() < 0.5):
        # tap-to-build: the child draws the chart themselves (workplan D7.4)
        from ..widgets import build_bars
        bstep = 1 if level == 'medium' and max(vals) <= 10 else 2
        if bstep == 2:
            vals = [v + v % 2 for v in vals]
            if len(set(vals)) < n:
                vals = random.sample(range(2, 17, 2), n)
            table['rows'] = [[c, str(v)] for c, v in zip(cats, vals)]
        return build_bars((f'Sondage « {q_fr} » — les résultats sont dans le tableau. Construis le diagramme à bandes.',
                           f'Survey “{q_en}” — the results are in the table. Build the bar chart.'),
                          short, vals,
                          (f'Pour chaque réponse, monte la bande jusqu’au nombre du tableau. Une case vaut {bstep}.',
                           f'For each answer, raise the bar up to the number in the table. One square is worth {bstep}.'),
                          ([f'{c[0]} : {v}' for c, v in zip(cats, vals)], [f'{c[1]}: {v}' for c, v in zip(cats, vals)]),
                          top=max(10, max(vals) + bstep) if bstep == 1 else max(16, max(vals) + bstep), step=bstep, table=table)
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
    big = vals.index(max(vals))
    heights = (', '.join(f'{c[0]} {v}' for c, v in zip(cats, vals)), ', '.join(f'{c[1]} {v}' for c, v in zip(cats, vals)))
    return mc((f'Sondage « {q_fr} » — les résultats sont dans le tableau. Quel diagramme à bandes représente ces résultats ?',
               f'Survey “{q_en}” — the results are in the table. Which bar chart shows these results?'),
              L5[i], [x for x in L5 if x != L5[i]],
              (f'Commence par « {cats[big][0]} » : c’est le plus grand nombre, sa bande doit être la plus haute. '
               'Vérifie ensuite chaque bande avec le tableau.',
               f'Start with “{cats[big][1]}”: it is the largest number, so its bar must be the tallest. '
               'Then check every bar against the table.'),
              (f'Le diagramme {L5[i]} : les bandes montent à {heights[0]}, comme dans le tableau. '
               'Dans chacun des autres diagrammes, au moins une bande n’a pas la bonne hauteur.',
               f'Chart {L5[i]}: the bars reach {heights[1]}, as in the table. '
               'In each of the other charts, at least one bar has the wrong height.'),
              shape=c.shape(), table=table)


# ── G4 · Survey questions ────────────────────────────────────────────────────

SURVEYS = [
    (('Tu veux savoir quel sport tes camarades préfèrent.', 'You want to find out which sport your classmates like best.'),
     ('Quel est ton sport préféré : soccer, hockey, natation ou basket ?', 'What is your favourite sport: soccer, hockey, swimming or basketball?'),
     [('Aimes-tu le sport ?', 'Do you like sport?'),
      ('Le hockey est le meilleur sport, n’est-ce pas ?', 'Hockey is the best sport, isn’t it?'),
      ('Combien de sports existe-t-il dans le monde : moins de 100, environ 500 ou plus de 1000 ?', 'How many sports are there in the world: under 100, about 500 or over 1000?'),
      ('Quel est le sport préféré de la directrice : soccer, hockey, natation ou basket ?', 'What is the principal’s favourite sport: soccer, hockey, swimming or basketball?')]),
    (('Tu veux savoir comment les élèves viennent à l’école.', 'You want to find out how students get to school.'),
     ('Comment viens-tu à l’école le plus souvent : à pied, en autobus, en voiture ou à vélo ?', 'How do you usually get to school: walk, bus, car or bike?'),
     [('Est-ce que l’autobus est jaune ?', 'Is the school bus yellow?'),
      ('Marcher, c’est meilleur pour la santé, non ?', 'Walking is healthier, right?'),
      ('À quelle heure commence l’école le matin : 8 h, 8 h 30 ou 9 h ?', 'What time does school start in the morning: 8:00, 8:30 or 9:00?'),
      ('Comment ton voisin vient-il à l’école : à pied, en autobus, en voiture ou à vélo ?', 'How does your neighbour get to school: walk, bus, car or bike?')]),
    (('Tu veux choisir la saveur de crème glacée pour la fête de la classe.', 'You want to choose the ice-cream flavour for the class party.'),
     ('Quelle saveur préfères-tu : vanille, chocolat ou fraise ?', 'Which flavour do you prefer: vanilla, chocolate or strawberry?'),
     [('Aimes-tu la crème glacée ?', 'Do you like ice cream?'),
      ('Le chocolat, c’est délicieux, tu ne trouves pas ?', 'Chocolate is delicious, don’t you think?'),
      ('Combien coûte un cornet à l’épicerie : 1 $, 2 $ ou 3 $ ?', 'How much does a cone cost at the grocery store: $1, $2 or $3?'),
      ('Quelle saveur ton enseignante préfère-t-elle : vanille, chocolat ou fraise ?', 'Which flavour does your teacher prefer: vanilla, chocolate or strawberry?')]),
    (('Tu veux savoir combien de temps les élèves lisent chaque soir.', 'You want to know how long students read each evening.'),
     ('Combien de minutes lis-tu un soir d’école : moins de 10, de 10 à 30, ou plus de 30 ?', 'How many minutes do you read on a school night: under 10, 10 to 30, or over 30?'),
     [('Aimes-tu lire ?', 'Do you like reading?'),
      ('Lire, c’est important, n’est-ce pas ?', 'Reading is important, isn’t it?'),
      ('Quel genre de livre lis-tu : roman, bande dessinée ou documentaire ?', 'What kind of book do you read: novel, comic or information book?'),
      ('Combien de livres y a-t-il à la bibliothèque : moins de 1000 ou plus de 1000 ?', 'How many books are in the library: under 1000 or over 1000?')]),
    (('Tu veux savoir quel animal de compagnie les familles de ta classe ont.', 'You want to know which pets the families in your class have.'),
     ('Quel animal as-tu à la maison : chien, chat, poisson, autre ou aucun ?', 'Which pet do you have at home: dog, cat, fish, other or none?'),
     [('Aimes-tu les animaux ?', 'Do you like animals?'),
      ('Les chats sont plus gentils que les chiens, non ?', 'Cats are nicer than dogs, right?'),
      ('Combien de pattes a un chien : 2, 4 ou 6 ?', 'How many legs does a dog have: 2, 4 or 6?'),
      ('Quel animal ton cousin a-t-il : chien, chat, poisson, autre ou aucun ?', 'Which pet does your cousin have: dog, cat, fish, other or none?')]),
]
WHY_BAD = [('Oui/non ne dit pas lequel ils préfèrent.', 'Yes/no does not tell which one they prefer.'),
           ('Cette question pousse vers une réponse : elle n’est pas neutre.', 'This question pushes towards one answer: it is not neutral.'),
           ('Cette question ne répond pas à ce que tu veux savoir.', 'This question does not find out what you want to know.'),
           ('Elle ne concerne qu’une seule personne.', 'It is only about one person.')]

POPULATIONS = [
    (('Tu veux savoir quel jeu les élèves de 4e année préfèrent à la récréation.', 'You want to know which recess game grade 4 students prefer.'),
     ('les élèves de 4e année', 'the grade 4 students'),
     [('tes parents', 'your parents'), ('les élèves de maternelle seulement', 'kindergarten students only'),
      ('ton meilleur ami seulement', 'only your best friend'), ('les enseignants', 'the teachers')]),
    (('Tu veux savoir quels livres les parents des élèves de l’école aimeraient voir à la bibliothèque.', 'You want to know which library books the parents of the school’s students would like.'),
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
                  ('Interroge toutes les personnes concernées par la question, pas seulement une personne.',
                   'Ask all the people the question is about, not just one person.'),
                  (f'Il faut interroger {right[0]} : ce sont eux que la question concerne.', f'You should ask {right[1]}: the question is about them.'))
    goal, right, wrong = pick(SURVEYS)
    # each wrong question keeps the reason that matches it (yes/no, leading, off-topic, one person)
    tagged = [(w, 'bad_question', WHY_BAD[k][1], WHY_BAD[k][0]) for k, w in enumerate(wrong)]
    if level == 'easy':
        tagged = tagged[:1] + tagged[2:]       # leave out the subtle « leading » distractor
        tagged.append((('Quelle heure est-il en ce moment, à ta montre ?', 'What time is it right now on your watch?'),
                       'bad_question', WHY_BAD[2][1], WHY_BAD[2][0]))
    return mc((f'{goal[0]} Quelle question est la meilleure pour ton sondage ?', f'{goal[1]} Which question is best for your survey?'),
              right, tagged,
              ('Une bonne question de sondage est neutre, s’adresse à chaque personne et propose des réponses faciles à compter.',
               'A good survey question is neutral, is asked to each person, and gives answers that are easy to count.'),
              (f'« {right[0]} » : neutre, et les réponses se comptent facilement.', f'“{right[1]}”: neutral, and the answers are easy to count.'))
