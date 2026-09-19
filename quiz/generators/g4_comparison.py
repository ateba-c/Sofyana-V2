"""
g4_comparison.py — Grade-4 comparing, ordering and number-line generators
(content_g4.md §3–4).

Topics:
  g4_before_after_gen      typed (integer) – predecessor / successor
  g4_compare_gen           typed (symbol)  – <, > or =
  g4_order_numbers_gen     ordering        – ascending / descending with a scenario and units
  g4_skip_sequence_gen     typed (integer) – missing term of a skip-counting sequence
  g4_number_line_step_gen  QCM + SVG       – find the graduation step of a number line
  g4_number_line_point_gen typed + SVG     – value of a point when only some ticks are labelled

Difficulty:
  easy   → numbers < 1 000, small steps
  medium → numbers < 10 000, boundary crossings (…999 → …000)
  hard   → numbers < 100 000, descending sequences, close numbers
"""
import random
from .base import _tagged_shuffle_mc
from . import scenarios as sc


def _bounds(level):
    return {'easy': (10, 999), 'medium': (100, 9_999), 'hard': (1_000, 99_999)}[level]


# ─────────────────────────────────────────────────────────────────────────────
# g4_before_after_gen
# ─────────────────────────────────────────────────────────────────────────────

_BEFORE_AFTER_CTX = [
    # (fr, en) — {n} number, {rel} "avant"/"après" is inserted by the caller
    ("{who} lit la page **{n}** d'un livre. Quel est le numéro de la page juste {rel_fr} ?",
     "{who} is reading page **{n}** of a book. What is the number of the page right {rel_en}?"),
    ("Le compteur d'une voiture affiche **{n}** km. Quel nombre affichait-il juste {rel_fr} ?",
     "A car's odometer shows **{n}** km. What number did it show right {rel_en}?"),
    ("{who} porte le dossard **{n}** à la course. Quel est le dossard juste {rel_fr} le sien ?",
     "{who} wears bib number **{n}** in the race. Which bib number comes right {rel_en} theirs?"),
    ("Dans la file d'attente, {who} a le billet **{n}**. Quel billet vient juste {rel_fr} ?",
     "In the waiting line, {who} holds ticket **{n}**. Which ticket comes right {rel_en}?"),
]


def g4_before_after_gen(level='easy'):
    lo, hi = _bounds(level)
    # Half the time force a boundary crossing (…99 → …00), the classic trap.
    if random.random() < 0.5:
        digits = len(str(hi))
        p = random.randint(1, digits - 1)
        base = random.randint(1, (hi // 10 ** p) - 1) * 10 ** p     # e.g. 600, 4000
        n = base if random.random() < 0.5 else base - 1              # 600 or 599
    else:
        n = random.randint(lo + 1, hi - 1)
    n = max(lo, min(hi, n))
    before = random.random() < 0.5
    answer = n - 1 if before else n + 1
    rel_fr = 'avant' if before else 'après'
    rel_en = 'before' if before else 'after'

    if random.random() < 0.5:
        who, _ = sc.pick_actor()
        ctx_fr, ctx_en = random.choice(_BEFORE_AFTER_CTX)
        prompt_fr = ctx_fr.format(who=who, n=sc.fmt_n(n), rel_fr=rel_fr)
        prompt_en = ctx_en.format(who=who, n=sc.fmt_n(n), rel_en=rel_en)
    else:
        prompt_fr = f"Quel nombre vient juste **{rel_fr}** {sc.fmt_n(n)} ?"
        prompt_en = f"Which number comes right **{rel_en}** {sc.fmt_n(n)}?"

    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          f"« Juste {rel_fr} » veut dire {'−' if before else '+'} 1. Attention quand le nombre finit par 0 ou par 9 !",
        'hint_en':          f"“Right {rel_en}” means {'−' if before else '+'} 1. Watch out when the number ends in 0 or 9!",
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: The number right {rel_en} is found by {"subtracting" if before else "adding"} 1.\n'
            f'Step 2: {sc.fmt_n(n)} {"−" if before else "+"} 1 = {sc.fmt_n(answer)}\n'
            f'Answer: {sc.fmt_n(answer)}'
        ),
        'explanation_fr': (
            f'Étape 1 : Le nombre juste {rel_fr} s\'obtient en {"soustrayant" if before else "ajoutant"} 1.\n'
            f'Étape 2 : {sc.fmt_n(n)} {"−" if before else "+"} 1 = {sc.fmt_n(answer)}\n'
            f'Réponse : {sc.fmt_n(answer)}'
        ),
        'correct_answers':  [str(answer)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_compare_gen — type <, > or =
# ─────────────────────────────────────────────────────────────────────────────

def _close_pair(level):
    lo, hi = _bounds(level)
    a = random.randint(lo, hi)
    r = random.random()
    if r < 0.15:
        return a, a
    if level == 'easy':
        b = a + random.choice([-1, 1]) * random.randint(1, 50)
    elif level == 'medium':
        # Same digits scrambled (1784 vs 1847) or a small difference
        if random.random() < 0.5:
            d = list(str(a))
            random.shuffle(d)
            b = int(''.join(d)) if d[0] != '0' else a + 9
        else:
            b = a + random.choice([-1, 1]) * random.randint(1, 30)
    else:
        d = list(str(a))
        i, j = random.sample(range(len(d)), 2)
        d[i], d[j] = d[j], d[i]
        b = int(''.join(d)) if d[0] != '0' else a + 100
    if b == a:
        b = a + 1
    b = max(1, b)
    return a, b


def g4_compare_gen(level='easy'):
    a, b = _close_pair(level)
    sym = '<' if a < b else '>' if a > b else '='
    word_fr = {'<': 'plus petit que', '>': 'plus grand que', '=': 'égal à'}[sym]
    word_en = {'<': 'less than', '>': 'greater than', '=': 'equal to'}[sym]
    return {
        'q_type':           'text_input',
        'answer_type':      'symbol',
        'prompt_fr':        f"Compare : **{sc.fmt_n(a)}** ⬜ **{sc.fmt_n(b)}**. Écris <, > ou =.",
        'prompt_en':        f"Compare: **{sc.fmt_n(a)}** ⬜ **{sc.fmt_n(b)}**. Type <, > or =.",
        'hint_fr':          'Compare d\'abord le nombre de chiffres, puis les chiffres de gauche à droite. La pointe du symbole vise le plus petit nombre.',
        'hint_en':          'Compare the number of digits first, then the digits from left to right. The small end of the symbol points to the smaller number.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Both numbers have {len(str(a))} and {len(str(b))} digits — compare from the left.\n'
            f'Step 2: {sc.fmt_n(a)} is {word_en} {sc.fmt_n(b)}.\n'
            f'Answer: {sc.fmt_n(a)} {sym} {sc.fmt_n(b)}'
        ),
        'explanation_fr': (
            f'Étape 1 : Les nombres ont {len(str(a))} et {len(str(b))} chiffres — compare à partir de la gauche.\n'
            f'Étape 2 : {sc.fmt_n(a)} est {word_fr} {sc.fmt_n(b)}.\n'
            f'Réponse : {sc.fmt_n(a)} {sym} {sc.fmt_n(b)}'
        ),
        'correct_answers':  [sym],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_order_numbers_gen — ordering with scenario & units
# ─────────────────────────────────────────────────────────────────────────────

def g4_order_numbers_gen(level='easy'):
    count = 4 if level == 'easy' else 5
    descending = level == 'hard' and random.random() < 0.5 or (level == 'medium' and random.random() < 0.25)
    things_fr, things_en, unit, lo, hi = sc.pick_measured()

    if level == 'easy':
        nums = sorted(random.sample(range(lo, hi + 1), count))
    else:
        # Close values that share leading digits: 6279, 6377, 6907 …
        base = random.randint(lo, max(lo, hi - 1000))
        spread = 999 if level == 'medium' else 300
        nums = sorted(random.sample(range(base, min(hi, base + spread) + 1), count))
    if len(set(nums)) < count:
        nums = sorted(set(nums))
        count = len(nums)

    ordered = nums[::-1] if descending else nums
    items = [{'label': f'{sc.fmt_n(n)} {unit}', 'order': i + 1} for i, n in enumerate(ordered)]
    who, _ = sc.pick_actor()
    order_fr = 'décroissant (du plus grand au plus petit)' if descending else 'croissant (du plus petit au plus grand)'
    order_en = 'descending order (largest to smallest)' if descending else 'ascending order (smallest to largest)'
    sep = ' > ' if descending else ' < '

    return {
        'q_type':           'ordering',
        'prompt_fr':        f"{who} mesure {count} {things_fr}. Range les mesures en ordre **{order_fr}**.",
        'prompt_en':        f"{who} measures {count} {things_en}. Sort the measurements in **{order_en}**.",
        'hint_fr':          'Compare d\'abord les chiffres de gauche (les plus grandes positions), puis avance vers la droite.',
        'hint_en':          'Compare the leftmost digits first (biggest place values), then move right.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'items':            items,
        'correct_answers':  [it['label'] for it in items],
        'time_limit':       40,
        'points':           1,
        'explanation_en':   f'{order_en.capitalize()}: ' + sep.join(f'{sc.fmt_n(n)} {unit}' for n in ordered),
        'explanation_fr':   f'Ordre {order_fr} : ' + sep.join(f'{sc.fmt_n(n)} {unit}' for n in ordered),
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_skip_sequence_gen — missing term in a skip-counting sequence
# ─────────────────────────────────────────────────────────────────────────────

def g4_skip_sequence_gen(level='easy'):
    if level == 'easy':
        step = random.choice([2, 3, 4, 5, 10])
        start = random.randint(10, 500)
        ascending = True
        n_shown = 5
    elif level == 'medium':
        step = random.choice([4, 6, 7, 8, 9, 25, 50])
        start = random.randint(100, 3000)
        ascending = random.random() < 0.8
        n_shown = 5
    else:
        step = random.choice([3, 6, 9, 12, 15, 25, 125, 250])
        start = random.randint(1000, 20000)
        ascending = random.random() < 0.5
        n_shown = 6
    if not ascending:
        start += step * (n_shown + 1)

    terms = [start + (i * step if ascending else -i * step) for i in range(n_shown)]
    # Hide one term: the last one (easy) or any interior one (medium/hard)
    hide = n_shown - 1 if level == 'easy' else random.randint(1, n_shown - 1)
    answer = terms[hide]
    shown = ['?' if i == hide else sc.fmt_n(t) for i, t in enumerate(terms)]
    seq = ', '.join(shown) + ', …'
    # Two consecutive visible terms to explain the step
    j = 0 if hide != 0 and hide != 1 else 2
    prev_vis = terms[hide - 1] if hide > 0 else terms[hide + 1]
    op = '+' if ascending else '−'

    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        f"Complète la suite : **{seq}**  Quel nombre remplace le « ? » ?",
        'prompt_en':        f"Complete the sequence: **{seq}**  Which number replaces the “?”?",
        'hint_fr':          'Trouve le pas : soustrais deux nombres voisins connus. La suite ' + ('augmente' if ascending else 'diminue') + ' toujours du même pas.',
        'hint_en':          'Find the step: subtract two known neighbours. The sequence always ' + ('increases' if ascending else 'decreases') + ' by the same step.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Two neighbours differ by {sc.fmt_n(terms[j + 1])} − {sc.fmt_n(terms[j])} = {"" if ascending else "−"}{step}, so the step is {op}{step}.\n'
            f'Step 2: {"Add" if (ascending and hide > 0) or (not ascending and hide == 0) else "Subtract"} the step to the neighbour: '
            f'{sc.fmt_n(prev_vis)} {op if hide > 0 else ("−" if ascending else "+")} {step} = {sc.fmt_n(answer)}\n'
            f'Answer: {sc.fmt_n(answer)}'
        ),
        'explanation_fr': (
            f'Étape 1 : Deux voisins diffèrent de {sc.fmt_n(terms[j + 1])} − {sc.fmt_n(terms[j])} = {"" if ascending else "−"}{step}, donc le pas est {op}{step}.\n'
            f'Étape 2 : Applique le pas au voisin : '
            f'{sc.fmt_n(prev_vis)} {op if hide > 0 else ("−" if ascending else "+")} {step} = {sc.fmt_n(answer)}\n'
            f'Réponse : {sc.fmt_n(answer)}'
        ),
        'correct_answers':  [str(answer)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Number-line helpers
# ─────────────────────────────────────────────────────────────────────────────

def _number_line(level):
    """(start, step, n_ticks) for a graduated line."""
    if level == 'easy':
        start = random.choice([0, 10, 20, 50, 100])
        step = random.choice([2, 5, 10])
        n_ticks = random.randint(5, 7)
    elif level == 'medium':
        start = random.choice([0, 100, 200, 500, 1000])
        step = random.choice([4, 5, 20, 25, 50, 100])
        n_ticks = random.randint(5, 8)
    else:
        start = random.randint(0, 40) * 250
        step = random.choice([3, 6, 15, 25, 125, 250, 500])
        n_ticks = random.randint(6, 9)
    return start, step, n_ticks


# ─────────────────────────────────────────────────────────────────────────────
# g4_number_line_step_gen — QCM + SVG
# ─────────────────────────────────────────────────────────────────────────────

def g4_number_line_step_gen(level='easy'):
    start, step, n_ticks = _number_line(level)
    end = start + step * (n_ticks - 1)
    # Label only two ticks: the first and one k intervals later (k ≥ 2)
    k = random.randint(2, n_ticks - 1)
    labels = [start, start + k * step]
    span = k * step
    correct = str(step)
    tagged = [
        (str(span), 'span_not_step',
         'That is the distance between the two labels, not one graduation.',
         "C'est l'écart entre les deux étiquettes, pas une seule graduation."),
        (str(k), 'counted_ticks',
         'You counted the intervals; the step is the value of ONE interval.',
         "Tu as compté les intervalles ; le pas est la valeur d'UN intervalle."),
        (str(step * 2), 'double_step', 'Divide the span by the number of intervals.', "Divise l'écart par le nombre d'intervalles."),
        (str(max(1, step // 2)), 'half_step', 'Divide the span by the number of intervals.', "Divise l'écart par le nombre d'intervalles."),
        (str(step + 1), 'off_by_one', 'Check the division.', 'Vérifie la division.'),
        (str(n_ticks - 1), 'counted_ticks', 'You counted the intervals of the whole line.', 'Tu as compté les intervalles de toute la droite.'),
        (str(step * 5), 'wrong_step', 'Divide the span by the number of intervals.', "Divise l'écart par le nombre d'intervalles."),
        (str(span - 1), 'wrong_step', 'Divide the span by the number of intervals.', "Divise l'écart par le nombre d'intervalles."),
        (str(step * 10), 'wrong_step', 'Divide the span by the number of intervals.', "Divise l'écart par le nombre d'intervalles."),
    ]
    seen = {correct}
    tagged = [t for t in tagged if t[0] not in seen and not seen.add(t[0])]
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        "Quel est le pas de graduation de cette droite numérique ?",
        'prompt_en':        "What is the step between two graduations on this number line?",
        'hint_fr':          f"Entre {sc.fmt_n(labels[0])} et {sc.fmt_n(labels[1])}, compte le nombre d'intervalles, puis divise l'écart par ce nombre.",
        'hint_en':          f"Between {sc.fmt_n(labels[0])} and {sc.fmt_n(labels[1])}, count the intervals, then divide the span by that count.",
        'show_illustration': True,
        'shape_data':       [{
            'type': 'number_line_svg', 'nl_start': start, 'nl_end': end,
            'nl_step': step, 'nl_target': None, 'nl_labels': labels,
        }],
        'choices':          _tagged_shuffle_mc(correct, tagged),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: The labels {sc.fmt_n(labels[0])} and {sc.fmt_n(labels[1])} are {k} intervals apart.\n'
            f'Step 2: Span = {sc.fmt_n(labels[1])} − {sc.fmt_n(labels[0])} = {sc.fmt_n(span)}.\n'
            f'Step 3: Step = {sc.fmt_n(span)} ÷ {k} = {step}.\n'
            f'Answer: {step}'
        ),
        'explanation_fr': (
            f'Étape 1 : Les étiquettes {sc.fmt_n(labels[0])} et {sc.fmt_n(labels[1])} sont séparées par {k} intervalles.\n'
            f'Étape 2 : Écart = {sc.fmt_n(labels[1])} − {sc.fmt_n(labels[0])} = {sc.fmt_n(span)}.\n'
            f'Étape 3 : Pas = {sc.fmt_n(span)} ÷ {k} = {step}.\n'
            f'Réponse : {step}'
        ),
        'correct_answers':  [correct],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_number_line_point_gen — typed + SVG (only first & last ticks labelled)
# ─────────────────────────────────────────────────────────────────────────────

def g4_number_line_point_gen(level='easy'):
    start, step, n_ticks = _number_line(level)
    end = start + step * (n_ticks - 1)
    idx = random.randint(1, n_ticks - 2)
    target = start + idx * step
    if level == 'easy':
        labels = [start + i * step for i in range(n_ticks)]     # everything labelled
    elif level == 'medium':
        labels = [start, start + step, end]                      # first two + last
    else:
        labels = [start, end]                                    # only the ends
    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        "Quel nombre se trouve au point « ? » sur cette droite numérique ?",
        'prompt_en':        "Which number is at the “?” point on this number line?",
        'hint_fr':          "Trouve d'abord le pas (écart entre deux étiquettes ÷ nombre d'intervalles), puis compte les graduations depuis le début.",
        'hint_en':          'Find the step first (span between two labels ÷ number of intervals), then count graduations from the start.',
        'show_illustration': True,
        'shape_data':       [{
            'type': 'number_line_svg', 'nl_start': start, 'nl_end': end,
            'nl_step': step, 'nl_target': target, 'nl_labels': labels,
        }],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: From {sc.fmt_n(start)} to {sc.fmt_n(end)} there are {n_ticks - 1} intervals, so the step is '
            f'({sc.fmt_n(end)} − {sc.fmt_n(start)}) ÷ {n_ticks - 1} = {step}.\n'
            f'Step 2: The point is {idx} graduation(s) after {sc.fmt_n(start)}: {sc.fmt_n(start)} + {idx} × {step} = {sc.fmt_n(target)}.\n'
            f'Answer: {sc.fmt_n(target)}'
        ),
        'explanation_fr': (
            f'Étape 1 : De {sc.fmt_n(start)} à {sc.fmt_n(end)} il y a {n_ticks - 1} intervalles, donc le pas est '
            f'({sc.fmt_n(end)} − {sc.fmt_n(start)}) ÷ {n_ticks - 1} = {step}.\n'
            f'Étape 2 : Le point est {idx} graduation(s) après {sc.fmt_n(start)} : {sc.fmt_n(start)} + {idx} × {step} = {sc.fmt_n(target)}.\n'
            f'Réponse : {sc.fmt_n(target)}'
        ),
        'correct_answers':  [str(target)],
    }
