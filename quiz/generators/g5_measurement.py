"""
g5_measurement.py — Grade-5 measurement generators (content_g5.md Ch.4-5).

Topics:
  g5_volume_gen           typed       – volume of rectangular prism (l×w×h)
  g5_capacity_convert_gen typed       – L ↔ mL
  g5_mass_convert_gen     typed       – g ↔ kg
  g5_elapsed_time_gen     typed       – duration between two clock times
  g5_temperature_gen      QCM         – compare temperatures (0 °C and above)
  g5_thermometer_gen      typed + SVG – read a thermometer
"""
import random
from .base import _tagged_shuffle_mc


# ─────────────────────────────────────────────────────────────────────────────
# g5_volume_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_volume_gen(level='easy'):
    """Typed — volume = l × w × h."""
    if level == 'easy':
        l, w, h = (random.randint(2, 6) for _ in range(3))
    elif level == 'medium':
        l, w, h = (random.randint(3, 10) for _ in range(3))
    else:
        l, w, h = (random.randint(5, 20) for _ in range(3))

    volume = l * w * h
    unit = random.choice(['cm', 'm'])

    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Un pavé droit mesure **{l} {unit}**, **{w} {unit}** et **{h} {unit}**. Quel est son volume en {unit}³ ?",
        'prompt_en':        f"A rectangular prism measures **{l} {unit}**, **{w} {unit}**, and **{h} {unit}**. What is its volume in {unit}³?",
        'hint_fr':          f"Volume = longueur × largeur × hauteur = {l} × {w} × {h}",
        'hint_en':          f"Volume = length × width × height = {l} × {w} × {h}",
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Use the formula: Volume = length × width × height.\n'
            f'Step 2: Substitute: {l} × {w} × {h}.\n'
            f'Step 3: Calculate: {l} × {w} = {l*w}, then {l*w} × {h} = {volume}.\n'
            f'Answer: Volume = {volume} {unit}³'
        ),
        'explanation_fr': (
            f'Étape 1 : Applique la formule : Volume = longueur × largeur × hauteur.\n'
            f'Étape 2 : Substitue : {l} × {w} × {h}.\n'
            f'Étape 3 : Calcule : {l} × {w} = {l*w}, puis {l*w} × {h} = {volume}.\n'
            f'Réponse : Volume = {volume} {unit}³'
        ),
        'correct_answers':  [str(volume), f"{volume} {unit}³"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_capacity_convert_gen / g5_mass_convert_gen
# ─────────────────────────────────────────────────────────────────────────────

def _num(x):
    """(fr, en) text of a number: 0,875 / 0.875 — no trailing zeros, no thousands separator."""
    s = f'{x:.3f}'.rstrip('0').rstrip('.') if isinstance(x, float) else str(x)
    return s.replace('.', ','), s


def _convert_problem(val, from_unit, to_unit, big, small):
    """Typed conversion big ↔ small (factor 1000), with a hint that follows the direction."""
    if from_unit == big:
        answer = round(val * 1000, 3)
        answer = int(answer) if float(answer).is_integer() else answer
    else:
        answer = round(val / 1000, 3)
        answer = int(answer) if float(answer).is_integer() else answer
    v_fr, v_en = _num(val)
    a_fr, a_en = _num(answer)
    if from_unit == big:
        hint_fr = f'1 {big} = 1 000 {small}. Pour passer de {big} à {small}, multiplie par 1 000.'
        hint_en = f'1 {big} = 1000 {small}. To go from {big} to {small}, multiply by 1000.'
        op_fr = f'multiplie par 1 000 : {v_fr} × 1 000 = {a_fr}'
        op_en = f'multiply by 1000: {v_en} × 1000 = {a_en}'
    else:
        hint_fr = f'1 000 {small} = 1 {big}. Pour passer de {small} à {big}, divise par 1 000.'
        hint_en = f'1000 {small} = 1 {big}. To go from {small} to {big}, divide by 1000.'
        op_fr = f'divise par 1 000 : {v_fr} ÷ 1 000 = {a_fr}'
        op_en = f'divide by 1000: {v_en} ÷ 1000 = {a_en}'
    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Convertis **{v_fr} {from_unit}** en **{to_unit}**.",
        'prompt_en':        f"Convert **{v_en} {from_unit}** to **{to_unit}**.",
        'hint_fr':          hint_fr,
        'hint_en':          hint_en,
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Remember: 1 {big} = 1000 {small}.\n'
            f'Step 2: To convert {from_unit} → {to_unit}, {op_en}.\n'
            f'Answer: {v_en} {from_unit} = {a_en} {to_unit}'
        ),
        'explanation_fr': (
            f'Étape 1 : Rappel : 1 {big} = 1 000 {small}.\n'
            f'Étape 2 : Pour convertir {from_unit} → {to_unit}, {op_fr}.\n'
            f'Réponse : {v_fr} {from_unit} = {a_fr} {to_unit}'
        ),
        'correct_answers':  [a_fr] if a_fr == a_en else [a_fr, a_en],
    }


def g5_capacity_convert_gen(level='easy'):
    """Typed — convert L ↔ mL."""
    if level == 'easy':
        val, from_unit, to_unit = random.randint(1, 10), 'L', 'mL'
    elif level == 'medium':
        if random.random() < 0.5:
            val, from_unit, to_unit = random.choice([0.5, 1.5, 2.5, 0.25, 0.75, 1.25]), 'L', 'mL'
        else:
            val, from_unit, to_unit = random.choice([500, 250, 750, 1500, 2000, 3500]), 'mL', 'L'
    else:
        if random.random() < 0.5:
            val = random.randint(1, 5) + random.choice([25, 50, 75, 125, 250, 375]) / 1000
            from_unit, to_unit = 'L', 'mL'
        else:
            val, from_unit, to_unit = random.randint(1, 9) * 100 + random.choice([0, 25, 50, 75]), 'mL', 'L'
    return _convert_problem(val, from_unit, to_unit, 'L', 'mL')


def g5_mass_convert_gen(level='easy'):
    """Typed — convert g ↔ kg."""
    if level == 'easy':
        val, from_unit, to_unit = random.randint(1, 10), 'kg', 'g'
    elif level == 'medium':
        if random.random() < 0.5:
            val, from_unit, to_unit = random.choice([0.5, 1.5, 2.5, 0.25, 0.75]), 'kg', 'g'
        else:
            val, from_unit, to_unit = random.choice([500, 250, 750, 1500, 2500]), 'g', 'kg'
    else:
        if random.random() < 0.5:
            val = random.randint(1, 9) + random.choice([250, 500, 750, 100, 200]) / 1000
            from_unit, to_unit = 'kg', 'g'
        else:
            val, from_unit, to_unit = random.randint(1, 9) * 1000 + random.choice([0, 250, 500, 750]), 'g', 'kg'
    return _convert_problem(val, from_unit, to_unit, 'kg', 'g')


# ─────────────────────────────────────────────────────────────────────────────
# g5_elapsed_time_gen
# ─────────────────────────────────────────────────────────────────────────────

def _hm(mins):
    h, m = divmod(mins, 60)
    return f'{h}:{m:02d}'


def _elapsed_jumps(start, end):
    """The jumps really used: (from, to, label_fr, label_en) — no empty or impossible steps."""
    nxt = (start // 60 + 1) * 60 if start % 60 else start
    if nxt > end:                                  # 11:40 → 11:50: minutes only
        return [(start, end, f'{end - start} min', f'{end - start} min')]
    jumps = []
    if nxt != start:
        jumps.append((start, nxt, f'{nxt - start} min', f'{nxt - start} min'))
    full = (end - nxt) // 60
    if full:
        jumps.append((nxt, nxt + full * 60, f'{full} h', f"{full} hour{'s' if full > 1 else ''}"))
    rest = end - nxt - full * 60
    if rest:
        jumps.append((nxt + full * 60, end, f'{rest} min', f'{rest} min'))
    return jumps


def g5_elapsed_time_gen(level='easy'):
    """Typed — calculate elapsed time between two clock times (end > start)."""
    if level == 'easy':
        # Whole hours only
        start_h = random.randint(7, 18)
        dur_h   = random.randint(1, 5)
        start_m = 0
        dur_m   = 0
    elif level == 'medium':
        # Hours + half-hours
        start_h = random.randint(7, 17)
        start_m = random.choice([0, 30])
        dur_h   = random.randint(1, 4)
        dur_m   = random.choice([0, 30])
    else:
        # Any 5-minute interval
        start_h = random.randint(7, 17)
        start_m = random.choice(range(0, 60, 5))
        dur_h   = random.randint(0, 4)
        dur_m   = random.choice(range(5, 60, 5))

    start = start_h * 60 + start_m
    total_min = dur_h * 60 + dur_m
    end = start + total_min
    start_str, end_str = _hm(start), _hm(end)

    if dur_h == 0:
        answer_fr, answer_en = f"{dur_m} min", f"{dur_m} minutes"
    elif dur_m == 0:
        answer_fr, answer_en = f"{dur_h} h", f"{dur_h} hour{'s' if dur_h > 1 else ''}"
    else:
        answer_fr = f"{dur_h} h {dur_m} min"
        answer_en = f"{dur_h} hour{'s' if dur_h > 1 else ''} {dur_m} minutes"

    # Accept several formats (the check is by value: 1 h 30 min == 90 min == 1:30)
    correct_answers = [answer_fr] + ([f"{total_min} min"] if dur_h else [])

    jumps = _elapsed_jumps(start, end)
    steps_fr = [f'De {_hm(a)} à {_hm(b)} : {lf}' for a, b, lf, _ in jumps]
    steps_en = [f'From {_hm(a)} to {_hm(b)}: {le}' for a, b, _, le in jumps]
    if len(jumps) > 1:
        steps_fr.append('Additionne : ' + ' + '.join(lf for *_, lf, _ in jumps) + f' = {answer_fr}')
        steps_en.append('Add them up: ' + ' + '.join(le for *_, le in jumps) + f' = {answer_en}')
    if start_m == 0 and dur_m == 0:
        hint_fr, hint_en = "Compte les heures entières de l'heure de début à l'heure de fin.", 'Count the whole hours from the start to the end.'
    elif len(jumps) == 1:
        hint_fr, hint_en = "Compte les minutes de l'heure de début à l'heure de fin.", 'Count the minutes from the start to the end.'
    else:
        hint_fr = "Fais des bonds : jusqu'à l'heure pleine, puis les heures entières, puis les minutes qui restent."
        hint_en = 'Make jumps: up to the next full hour, then whole hours, then the minutes left.'

    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Une activité commence à **{start_str}** et se termine à **{end_str}**. Quelle est sa durée ?",
        'prompt_en':        f"An activity starts at **{start_str}** and ends at **{end_str}**. How long does it last?",
        'hint_fr':          hint_fr,
        'hint_en':          hint_en,
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en':   ''.join(f'Step {i + 1}: {s}\n' for i, s in enumerate(steps_en)) + f'Answer: the duration is {answer_en}',
        'explanation_fr':   ''.join(f'Étape {i + 1} : {s}\n' for i, s in enumerate(steps_fr)) + f'Réponse : la durée est {answer_fr}',
        'correct_answers':  correct_answers,
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_temperature_gen
# ─────────────────────────────────────────────────────────────────────────────

def _distinct_temps(lo, hi, k=5):
    return random.sample(range(lo, hi + 1), k)


def g5_temperature_gen(level='easy'):
    """QCM — compare temperatures. Hard: winter temperatures below zero (decision D2, 2026-10-26)."""
    if level == 'easy':
        temps = _distinct_temps(0, 40)
        question = random.choice(['coldest', 'warmest'])
    elif level == 'medium':
        temps = _distinct_temps(0, 30)
        question = random.choice(['coldest', 'warmest'])
    else:
        temps = random.sample([t for t in range(-25, 16) if t], 5)
        if sum(t < 0 for t in temps) < 2:                 # at least two below zero: compare negatives
            temps[:2] = random.sample(range(-25, 0), 2)
            temps = list(dict.fromkeys(temps))
            while len(temps) < 5:
                t = random.randint(-25, 15)
                if t and t not in temps:
                    temps.append(t)
        question = random.choice(['coldest', 'warmest'])

    # The temperatures are the answer choices; the prompt does not repeat them.
    if question == 'coldest':
        correct = min(temps)
        prompt_fr = "Quelle est la température la plus froide ?"
        prompt_en = "Which is the coldest temperature?"
    else:
        correct = max(temps)
        prompt_fr = "Quelle est la température la plus chaude ?"
        prompt_en = "Which is the warmest temperature?"

    others = [t for t in temps if t != correct]
    T = lambda t: (f'−{abs(t)}' if t < 0 else str(t)) + ' °C'
    tagged_candidates = [
        (T(t), 'wrong_temperature',
         'Remember: the smaller the number, the colder it is.',
         'Plus le nombre est petit, plus la température est froide.')
        for t in others
    ]
    correct_str = T(correct)
    in_order = ', '.join(T(t) for t in sorted(temps))

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Sur un thermomètre, la température monte vers le haut : plus le nombre est petit, plus il fait froid.'
                            + (' Sous zéro, −20 °C est plus froid que −5 °C.' if level == 'hard' else ''),
        'hint_en':          'On a thermometer, temperature rises upward: the smaller the number, the colder.'
                            + (' Below zero, −20 °C is colder than −5 °C.' if level == 'hard' else ''),
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(correct_str, tagged_candidates[:4]),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Put the temperatures in order, from coldest to warmest: {in_order}.\n'
            f'Step 2: The {"coldest is the smallest number" if question == "coldest" else "warmest is the biggest number"}: {correct_str}.\n'
            f'Answer: {correct_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Range les températures de la plus froide à la plus chaude : {in_order}.\n'
            f'Étape 2 : La plus {"froide est le plus petit nombre" if question == "coldest" else "chaude est le plus grand nombre"} : {correct_str}.\n'
            f'Réponse : {correct_str}'
        ),
        'correct_answers':  [correct_str],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_thermometer_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_thermometer_gen(level='easy'):
    """Typed + SVG — read the temperature shown on a thermometer."""
    if level == 'easy':
        # every mark is numbered (5 by 5)
        min_t, max_t, step, minor = 0, 40, 5, None
        temp = random.choice(range(0, 41, 5))
    elif level == 'medium':
        # numbered every 10, one small mark in between: the reading falls on that small mark
        min_t, max_t, step, minor = 0, 50, 10, 5
        temp = random.choice(range(5, 50, 10))
    elif random.random() < 0.5:
        # winter scale, below zero (decision D2): numbered every 10, small marks every 2
        min_t, max_t, step, minor = -30, 20, 10, 2
        temp = random.choice([t for t in range(-28, 0, 2) if t % 10])
    else:
        # numbered every 10, small marks every 2: count the small marks
        min_t, max_t, step, minor = 0, 50, 10, 2
        temp = random.choice([t for t in range(2, 50, 2) if t % 10])

    temp_str = (f'−{abs(temp)}' if temp < 0 else str(temp)) + ' °C'
    # As drawn: numbers every 10 °C; the small marks in between are worth `small` °C.
    small = minor or step
    below = temp - temp % 10                  # the numbered mark just under the liquid (−14 → −20)
    k = (temp - below) // small
    S = lambda t: f'−{abs(t)}' if t < 0 else str(t)
    hint_fr = f'Les nombres vont de 10 en 10. Chaque petit trait vaut {small} °C.'
    hint_en = f'The numbers go up by 10. Each small mark is worth {small} °C.'
    if k == 0:
        mid_fr = f'Le liquide s’arrête juste au nombre {S(temp)}.'
        mid_en = f'The liquid stops right at the number {S(temp)}.'
    else:
        pl = 's' if k > 1 else ''
        mid_fr = f'Le liquide dépasse le {S(below)} de {k} petit{pl} trait{pl} de {small} °C : {S(below)} + {k * small} = {S(temp)}.'
        mid_en = f'The liquid goes {k} small mark{pl} of {small} °C above {S(below)}: {S(below)} + {k * small} = {S(temp)}.'

    return {
        'q_type':           'text_input',
        'prompt_fr':        "Quelle température indique ce thermomètre ?",
        'prompt_en':        "What temperature does this thermometer show?",
        'hint_fr':          hint_fr,
        'hint_en':          hint_en,
        'show_illustration': True,
        'shape_data':       [{
            'type':     'thermometer',
            'temp':     temp,
            'min_temp': min_t,
            'max_temp': max_t,
            'step':     step,
            'minor':    minor,
        }],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Find the top of the liquid column.\n'
            f'Step 2: {mid_en}\n'
            f'Answer: {temp_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Repère le haut de la colonne de liquide.\n'
            f'Étape 2 : {mid_fr}\n'
            f'Réponse : {temp_str}'
        ),
        'correct_answers':  list(dict.fromkeys([temp_str, str(temp), temp_str.replace(' °C', '')])),
        'answer_type':      'signed' if temp < 0 else 'integer',
    }
