"""
g5_measurement.py — Grade-5 measurement generators (content_g5.md Ch.4-5).

Topics:
  g5_volume_gen           typed       – volume of rectangular prism (l×w×h)
  g5_capacity_convert_gen typed       – L ↔ mL
  g5_mass_convert_gen     typed       – g ↔ kg
  g5_elapsed_time_gen     typed       – duration between two clock times
  g5_temperature_gen      QCM         – compare temperatures (incl. negatives)
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
# g5_capacity_convert_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_capacity_convert_gen(level='easy'):
    """Typed — convert L ↔ mL."""
    if level == 'easy':
        # Whole litres → mL
        val = random.randint(1, 10)
        from_unit, to_unit = 'L', 'mL'
        answer = val * 1000
        answer_str = str(answer)
    elif level == 'medium':
        direction = random.choice(['L_to_mL', 'mL_to_L'])
        if direction == 'L_to_mL':
            val = random.choice([0.5, 1.5, 2.5, 0.25, 0.75, 1.25])
            from_unit, to_unit = 'L', 'mL'
            answer = int(val * 1000)
            val_str = str(val).replace('.', ',')
            answer_str = str(answer)
        else:
            val = random.choice([500, 250, 750, 1500, 2000, 3500])
            from_unit, to_unit = 'mL', 'L'
            answer = val / 1000
            answer_str = str(answer).replace('.', ',')
            val_str = str(val)
    else:
        direction = random.choice(['L_to_mL', 'mL_to_L'])
        if direction == 'L_to_mL':
            whole = random.randint(1, 5)
            dec   = random.choice([25, 50, 75, 125, 250, 375])
            val   = whole + dec / 1000
            from_unit, to_unit = 'L', 'mL'
            answer = int(val * 1000)
            val_str = f"{whole},{dec:03d}".replace(',000', '')
            answer_str = str(answer)
        else:
            val = random.randint(1, 9) * 100 + random.choice([0, 25, 50, 75])
            from_unit, to_unit = 'mL', 'L'
            answer = val / 1000
            answer_str = str(answer).replace('.', ',')
            val_str = str(val)

    # For easy, val_str wasn't set
    if level == 'easy':
        val_str = str(val)

    correct_dot = answer_str.replace(',', '.')
    if from_unit == 'L':
        op_en = f'multiply by 1,000: {val_str} × 1,000 = {answer_str}'
        op_fr = f'multiplie par 1 000 : {val_str} × 1 000 = {answer_str}'
    else:
        op_en = f'divide by 1,000: {val_str} ÷ 1,000 = {answer_str}'
        op_fr = f'divise par 1 000 : {val_str} ÷ 1 000 = {answer_str}'
    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Convertis **{val_str} {from_unit}** en **{to_unit}**.",
        'prompt_en':        f"Convert **{val_str} {from_unit}** to **{to_unit}**.",
        'hint_fr':          '1 L = 1 000 mL. Pour convertir L → mL, multiplie par 1 000.',
        'hint_en':          '1 L = 1,000 mL. To convert L → mL, multiply by 1,000.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Remember: 1 L = 1,000 mL.\n'
            f'Step 2: To convert {from_unit} → {to_unit}, {op_en}.\n'
            f'Answer: {val_str} {from_unit} = {answer_str} {to_unit}'
        ),
        'explanation_fr': (
            f'Étape 1 : Rappel : 1 L = 1 000 mL.\n'
            f'Étape 2 : Pour convertir {from_unit} → {to_unit}, {op_fr}.\n'
            f'Réponse : {val_str} {from_unit} = {answer_str} {to_unit}'
        ),
        'correct_answers':  [answer_str, correct_dot, answer_str.replace(',', '.')],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_mass_convert_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_mass_convert_gen(level='easy'):
    """Typed — convert g ↔ kg."""
    if level == 'easy':
        val = random.randint(1, 10)
        from_unit, to_unit = 'kg', 'g'
        answer_str = str(val * 1000)
        val_str    = str(val)
    elif level == 'medium':
        direction = random.choice(['kg_to_g', 'g_to_kg'])
        if direction == 'kg_to_g':
            val = random.choice([0.5, 1.5, 2.5, 0.25, 0.75])
            from_unit, to_unit = 'kg', 'g'
            answer_str = str(int(val * 1000))
            val_str    = str(val).replace('.', ',')
        else:
            val = random.choice([500, 250, 750, 1500, 2500])
            from_unit, to_unit = 'g', 'kg'
            answer_str = str(val / 1000).replace('.', ',')
            val_str    = str(val)
    else:
        direction = random.choice(['kg_to_g', 'g_to_kg'])
        if direction == 'kg_to_g':
            whole = random.randint(1, 9)
            dec   = random.choice([250, 500, 750, 100, 200])
            val   = whole + dec / 1000
            from_unit, to_unit = 'kg', 'g'
            answer_str = str(int(val * 1000))
            val_str    = f"{whole},{dec:03d}".rstrip('0').rstrip(',')
        else:
            val = random.randint(1, 9) * 1000 + random.choice([0, 250, 500, 750])
            from_unit, to_unit = 'g', 'kg'
            answer_str = str(val / 1000).replace('.', ',')
            val_str    = str(val)

    correct_dot = answer_str.replace(',', '.')
    if from_unit == 'kg':
        mass_op_en = f'multiply by 1,000: {val_str} × 1,000 = {answer_str}'
        mass_op_fr = f'multiplie par 1 000 : {val_str} × 1 000 = {answer_str}'
    else:
        mass_op_en = f'divide by 1,000: {val_str} ÷ 1,000 = {answer_str}'
        mass_op_fr = f'divise par 1 000 : {val_str} ÷ 1 000 = {answer_str}'
    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Convertis **{val_str} {from_unit}** en **{to_unit}**.",
        'prompt_en':        f"Convert **{val_str} {from_unit}** to **{to_unit}**.",
        'hint_fr':          '1 kg = 1 000 g. Pour convertir kg → g, multiplie par 1 000.',
        'hint_en':          '1 kg = 1,000 g. To convert kg → g, multiply by 1,000.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Remember: 1 kg = 1,000 g.\n'
            f'Step 2: To convert {from_unit} → {to_unit}, {mass_op_en}.\n'
            f'Answer: {val_str} {from_unit} = {answer_str} {to_unit}'
        ),
        'explanation_fr': (
            f'Étape 1 : Rappel : 1 kg = 1 000 g.\n'
            f'Étape 2 : Pour convertir {from_unit} → {to_unit}, {mass_op_fr}.\n'
            f'Réponse : {val_str} {from_unit} = {answer_str} {to_unit}'
        ),
        'correct_answers':  [answer_str, correct_dot],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_elapsed_time_gen
# ─────────────────────────────────────────────────────────────────────────────

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
        if dur_h == 0 and dur_m == 0:
            dur_m = 30

    end_total_m = start_h * 60 + start_m + dur_h * 60 + dur_m
    end_h = (end_total_m // 60) % 24
    end_m = end_total_m % 60

    start_str = f"{start_h}:{start_m:02d}"
    end_str   = f"{end_h}:{end_m:02d}"

    if dur_h == 0:
        answer_fr = f"{dur_m} min"
        answer_en = f"{dur_m} min"
    elif dur_m == 0:
        answer_fr = f"{dur_h} h"
        answer_en = f"{dur_h} h"
    else:
        answer_fr = f"{dur_h} h {dur_m} min"
        answer_en = f"{dur_h} h {dur_m} min"

    # Accept several formats
    correct_answers = [answer_fr]
    if dur_h > 0 and dur_m > 0:
        total_min = dur_h * 60 + dur_m
        correct_answers.append(f"{total_min} min")
    elif dur_h > 0:
        correct_answers.append(f"{dur_h * 60} min")

    return {
        'q_type':           'text_input',
        'prompt_fr':        f"Une activité commence à **{start_str}** et se termine à **{end_str}**. Quelle est sa durée ?",
        'prompt_en':        f"An activity starts at **{start_str}** and ends at **{end_str}**. How long does it last?",
        'hint_fr':          'Compte les heures puis les minutes séparément.',
        'hint_en':          'Count the hours first, then the minutes.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: From {start_str} to the next full hour: count up to {start_h + 1 if start_m else start_h}:00.\n'
            f'Step 2: Count full hours from there to {end_str}.\n'
            f'Step 3: Count remaining minutes.\n'
            f'Answer: the duration is {answer_en}'
        ),
        'explanation_fr': (
            f'Étape 1 : De {start_str} à la prochaine heure pleine : compte jusqu\'à {start_h + 1 if start_m else start_h}:00.\n'
            f'Étape 2 : Compte les heures entières jusqu\'à {end_str}.\n'
            f'Étape 3 : Compte les minutes restantes.\n'
            f'Réponse : la durée est {answer_fr}'
        ),
        'correct_answers':  correct_answers,
    }


# ─────────────────────────────────────────────────────────────────────────────
# g5_temperature_gen
# ─────────────────────────────────────────────────────────────────────────────

def g5_temperature_gen(level='easy'):
    """QCM — compare temperatures; includes negatives at medium/hard."""
    if level == 'easy':
        temps = random.sample(range(0, 41), 5)
        question = random.choice(['coldest', 'warmest'])
    elif level == 'medium':
        temps = [random.randint(-15, 30) for _ in range(5)]
        # ensure distinct
        temps = list(set(temps))
        while len(temps) < 5:
            temps.append(random.randint(-15, 30))
        temps = list(set(temps))[:5]
        question = random.choice(['coldest', 'warmest'])
    else:
        temps = [random.randint(-25, 35) for _ in range(5)]
        temps = list(set(temps))
        while len(temps) < 5:
            temps.append(random.randint(-25, 35))
        temps = list(set(temps))[:5]
        question = 'coldest'  # always coldest for hard (more common error with negatives)

    if question == 'coldest':
        correct = min(temps)
        prompt_fr = f"Quelle est la température la plus froide parmi : {', '.join(str(t) + ' °C' for t in temps)} ?"
        prompt_en = f"Which is the coldest temperature among: {', '.join(str(t) + ' °C' for t in temps)}?"
    else:
        correct = max(temps)
        prompt_fr = f"Quelle est la température la plus chaude parmi : {', '.join(str(t) + ' °C' for t in temps)} ?"
        prompt_en = f"Which is the warmest temperature among: {', '.join(str(t) + ' °C' for t in temps)}?"

    others = [t for t in temps if t != correct]
    tagged_candidates = [
        (str(t) + ' °C', 'wrong_temperature',
         'Remember: lower numbers mean colder temperatures, even when negative.',
         'Plus le nombre est petit, plus la température est froide — même en négatif.')
        for t in others
    ]
    correct_str = str(correct) + ' °C'

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Sur un thermomètre, la température monte vers le haut. −10 °C est plus froid que −5 °C.',
        'hint_en':          'On a thermometer, temperature rises upward. −10 °C is colder than −5 °C.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(correct_str, tagged_candidates[:4]),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: List all temperatures: {", ".join(str(t) + " °C" for t in temps)}.\n'
            f'Step 2: Remember — more negative = colder, more positive = warmer.\n'
            f'Step 3: The {"coldest" if question == "coldest" else "warmest"} is {correct_str}.\n'
            f'Answer: {correct_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Liste toutes les températures : {", ".join(str(t) + " °C" for t in temps)}.\n'
            f'Étape 2 : Plus le nombre est négatif = plus froid ; plus il est positif = plus chaud.\n'
            f'Étape 3 : La plus {"froide" if question == "coldest" else "chaude"} est {correct_str}.\n'
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
        min_t, max_t, step = 0, 40, 5
        temp = random.choice(range(0, 41, 5))
    elif level == 'medium':
        min_t, max_t, step = -10, 40, 5
        temp = random.choice(range(-10, 41, 5))
    else:
        min_t, max_t, step = -20, 40, 10
        temp = random.choice(range(-20, 41, 10))

    temp_str = f"{temp} °C"

    return {
        'q_type':           'text_input',
        'prompt_fr':        "Quelle température indique ce thermomètre ?",
        'prompt_en':        "What temperature does this thermometer show?",
        'hint_fr':          'Lis la graduation atteinte par la colonne de liquide.',
        'hint_en':          'Read the graduation reached by the liquid column.',
        'show_illustration': True,
        'shape_data':       [{
            'type':     'thermometer',
            'temp':     temp,
            'min_temp': min_t,
            'max_temp': max_t,
            'step':     step,
        }],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Look at the liquid column in the thermometer.\n'
            f'Step 2: Find the graduation line it reaches.\n'
            f'Step 3: Read the number on the scale at that line.\n'
            f'Answer: {temp_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Observe la colonne de liquide dans le thermomètre.\n'
            f'Étape 2 : Trouve la graduation qu\'elle atteint.\n'
            f'Étape 3 : Lis le nombre sur l\'échelle à cette graduation.\n'
            f'Réponse : {temp_str}'
        ),
        'correct_answers':  [temp_str, str(temp)],
    }
