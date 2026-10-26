"""
g4_time.py — Grade-4 time generators (content_g4.md §6).

Topics:
  g4_clock_24h_gen      QCM + SVG        – read an analog clock, answer in 24-h notation (avant-midi / après-midi)
  g4_time_units_gen     typed (integer)  – convert between days, hours, minutes, weeks, months, years (with a scenario)
  g4_elapsed_time_gen   typed (duration) – duration of an activity from start and end time (scenario)
  g4_end_time_gen       typed (duration) – end time from start time and duration (scenario)

Difficulty:
  easy   → whole / half hours, single-unit conversions
  medium → 5-minute precision, crossing one hour, compound conversions (2 h 20 min)
  hard   → any minute, crossing several hours, mixed units (1 day 6 h)
"""
import random
from .base import _tagged_shuffle_mc
from . import scenarios as sc
from .clock import pick_activity_for, _dur_en


def _fmt24(h, m):
    return f"{h} h {m:02d}"


def _fmt12(h, m):
    h12 = h % 12 or 12
    return f"{h12} h {m:02d}"


def _en24(h, m):
    """English 24-hour notation: 18:39 (never the French « 18 h 39 »)."""
    return f"{h}:{m:02d}"


def _en12(h, m):
    return f"{h % 12 or 12}:{m:02d}"


def _period_fr(h):
    return "de l'avant-midi (AM)" if h < 12 else "de l'après-midi (PM)"


def _period_en(h):
    return 'in the morning (AM)' if h < 12 else 'in the afternoon (PM)'


# ─────────────────────────────────────────────────────────────────────────────
# g4_clock_24h_gen
# ─────────────────────────────────────────────────────────────────────────────

def g4_clock_24h_gen(level='easy'):
    if level == 'easy':
        h = random.randint(0, 23)
        m = random.choice([0, 30])
    elif level == 'medium':
        h = random.randint(0, 23)
        m = random.choice(range(0, 60, 5))
    else:
        h = random.randint(0, 23)
        m = random.randint(0, 59)
    # Favour afternoon (the whole point of 24-h notation)
    if h < 12 and random.random() < 0.6:
        h += 12
    h12 = h % 12 or 12
    correct = _fmt24(h, m)
    tagged = [
        (_fmt24((h + 12) % 24, m), 'wrong_period',
         'Afternoon hours are 12 more than the clock shows; morning hours stay the same.',
         "L'après-midi, on ajoute 12 à l'heure de l'horloge ; l'avant-midi, on garde la même heure."),
        (_fmt24(h, (m + 30) % 60), 'wrong_minutes', 'Read the long hand again.', 'Relis la grande aiguille.'),
        (_fmt24((h + 1) % 24, m), 'hour_plus_one', 'The short hand has not reached the next number yet.',
         "La petite aiguille n'a pas encore atteint le chiffre suivant."),
        (_fmt24((m // 5 or 12) if h >= 12 and (m // 5 or 12) + 12 < 24 else (m // 5 or 12), (h12 * 5) % 60), 'swapped_hands',
         'Short hand = hours, long hand = minutes.', 'Petite aiguille = heures, grande aiguille = minutes.'),
        (_fmt24((h + 12) % 24, (m + 15) % 60), 'wrong_period', 'Check AM/PM and the minutes.',
         "Vérifie l'avant-midi / l'après-midi et les minutes."),
    ]
    tagged = [t for t in tagged if t[0] != correct]
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        f"Cette horloge indique l'heure **{_period_fr(h)}**. Écris cette heure en notation 24 h.",
        'prompt_en':        f"This clock shows a time **{_period_en(h)}**. Write this time in 24-hour notation.",
        'hint_fr':          "Lis l'heure sur l'horloge. Si c'est l'après-midi, ajoute 12 aux heures (sauf pour 12 h). À minuit, 12 devient 0 h.",
        'hint_en':          'Read the clock. In the afternoon, add 12 to the hour (except 12 itself). At midnight, 12 becomes 0:00.',
        'show_illustration': True,
        'shape_data':       [{'type': 'clock', 'hours': h12, 'minutes': m}],
        'choices':          _tagged_shuffle_mc(correct, tagged),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: The clock shows {_en12(h, m)}.\n'
            f'Step 2: It is {_period_en(h)}, so {"add 12 to the hour: " + str(h12) + " + 12 = " + str(h) if 12 < h else "the hour stays " + str(h) if h != 0 else "12 at midnight is written 0"}.\n'
            f'Answer: {_en24(h, m)}'
        ),
        'explanation_fr': (
            f'Étape 1 : L\'horloge indique {_fmt12(h, m)}.\n'
            f'Étape 2 : C\'est {_period_fr(h)}, donc {"on ajoute 12 : " + str(h12) + " + 12 = " + str(h) if 12 < h else "l\'heure reste " + str(h) if h != 0 else "minuit s\'écrit 0 h"}.\n'
            f'Réponse : {correct}'
        ),
        'correct_answers':  [correct],
    }


# ─────────────────────────────────────────────────────────────────────────────
# g4_time_units_gen
# ─────────────────────────────────────────────────────────────────────────────

# (big_fr, big_en, small_fr, small_en, factor, (lo, hi)) — "N big units" → small units.
# lo ≥ 2: with 1 unit, the hint « 1 an = 12 mois » would already be the answer.
_CONVERSIONS = {
    'easy': [
        ('heures', 'hours', 'minutes', 'minutes', 60, (2, 5)),
        ('jours', 'days', 'heures', 'hours', 24, (2, 4)),
        ('semaines', 'weeks', 'jours', 'days', 7, (2, 6)),
        ('ans', 'years', 'mois', 'months', 12, (2, 5)),
        ('minutes', 'minutes', 'secondes', 'seconds', 60, (2, 5)),
    ],
    'medium': [
        ('heures', 'hours', 'minutes', 'minutes', 60, (2, 9)),
        ('jours', 'days', 'heures', 'hours', 24, (2, 7)),
        ('semaines', 'weeks', 'jours', 'days', 7, (3, 12)),
        ('ans', 'years', 'semaines', 'weeks', 52, (2, 3)),
        ('ans', 'years', 'jours', 'days', 365, (2, 3)),
    ],
    'hard': [
        ('heures', 'hours', 'minutes', 'minutes', 60, (3, 12)),
        ('jours', 'days', 'heures', 'hours', 24, (3, 10)),
        ('semaines', 'weeks', 'heures', 'hours', 168, (2, 3)),
        ('ans', 'years', 'jours', 'days', 365, (2, 3)),
        ('jours', 'days', 'minutes', 'minutes', 1440, (2, 3)),
    ],
}

# Two-step facts, so the hint shows the chain rather than a ready-made total.
_CHAIN = {
    168:  ('1 semaine = 7 jours et 1 jour = 24 heures, donc 1 semaine = 7 × 24 = 168 heures',
           '1 week = 7 days and 1 day = 24 hours, so 1 week = 7 × 24 = 168 hours'),
    1440: ('1 jour = 24 heures et 1 heure = 60 minutes, donc 1 jour = 24 × 60 = 1440 minutes',
           '1 day = 24 hours and 1 hour = 60 minutes, so 1 day = 24 × 60 = 1440 minutes'),
}

# Stories that fit the size of the duration: {who}, {de_who}, {dur}.
_CTX = {
    'minutes': [
        ("La chanson préférée {de_who} dure {dur}.", "{who}'s favourite song lasts {dur}."),
        ("{who} a fait la planche pendant {dur}.", "{who} held a plank for {dur}."),
        ("Le sablier {de_who} se vide en {dur}.", "{who}'s sand timer empties in {dur}."),
    ],
    'heures': [
        ("Le trajet en train {de_who} dure {dur}.", "{who}'s train ride lasts {dur}."),
        ("{who} a dormi pendant {dur}.", "{who} slept for {dur}."),
        ("La sortie au musée {de_who} a duré {dur}.", "{who}'s museum trip lasted {dur}."),
    ],
    'jours': [
        ("{who} est {parti} en camping pendant {dur}.", "{who} went camping for {dur}."),
        ("{who} a attendu {dur} avant de recevoir son colis.", "{who} waited {dur} to receive a package."),
        ("La plante {de_who} a mis {dur} à fleurir.", "{who}'s plant took {dur} to bloom."),
    ],
    'semaines': [
        ("Les vacances {de_who} durent {dur}.", "{who}'s holidays last {dur}."),
        ("{who} est {parti} en voyage pendant {dur}.", "{who} went on a trip for {dur}."),
        ("Le camp de jour {de_who} dure {dur}.", "{who}'s day camp lasts {dur}."),
    ],
    'ans': [
        ("{who} suit des cours de piano depuis {dur}.", "{who} has been taking piano lessons for {dur}."),
        ("Le chat {de_who} vit avec sa famille depuis {dur}.", "{who}'s cat has lived with the family for {dur}."),
        ("{who} habite dans sa maison depuis {dur}.", "{who} has lived in the same house for {dur}."),
    ],
}


def _sing(word):
    return word[:-1] if word.endswith('s') and word != 'mois' else word


def g4_time_units_gen(level='easy'):
    big_fr, big_en, small_fr, small_en, factor, (lo, hi) = random.choice(_CONVERSIONS[level])
    n = random.randint(lo, hi)
    extra = 0
    # Compound durations: 2 h 20 min, 3 days 6 h, 2 weeks 3 days (never "1 day and 12 minutes")
    if level != 'easy' and factor <= 60 and random.random() < 0.5:
        extra = random.randint(1, factor - 1)
    total = n * factor + extra
    small_fr_x = _sing(small_fr) if extra == 1 else small_fr
    small_en_x = _sing(small_en) if extra == 1 else small_en
    dur_fr = f"**{n} {big_fr}**" + (f" et **{extra} {small_fr_x}**" if extra else '')
    dur_en = f"**{n} {big_en}**" + (f" and **{extra} {small_en_x}**" if extra else '')

    who, g = sc.pick_actor()
    ctx_fr, ctx_en = random.choice(_CTX[big_fr])
    story_fr = ctx_fr.format(who=who, de_who=sc.de(who), dur=dur_fr, parti='partie' if g == 'f' else 'parti')
    story_en = ctx_en.format(who=who, dur=dur_en)
    one_fr = _CHAIN[factor][0] if factor in _CHAIN else f"1 {_sing(big_fr)} = {factor} {small_fr}"
    one_en = _CHAIN[factor][1] if factor in _CHAIN else f"1 {_sing(big_en)} = {factor} {small_en}"
    tail_fr = " Multiplie, puis ajoute le reste." if extra else " Multiplie."
    tail_en = ' Multiply, then add the leftover.' if extra else ' Multiply.'

    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        f"{story_fr} Combien {'d’' if small_fr[0] in 'aeiouh' else 'de '}**{small_fr}** cela fait-il ?",
        'prompt_en':        f"{story_en} How many **{small_en}** is that?",
        'hint_fr':          one_fr + '.' + tail_fr,
        'hint_en':          one_en + '.' + tail_en,
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: {one_en}.\n'
            f'Step 2: {n} × {factor} = {sc.fmt_n(n * factor)}' + (f', then + {extra} = {sc.fmt_n(total)}' if extra else '') + '\n'
            f'Answer: {sc.fmt_n(total)} {small_en}'
        ),
        'explanation_fr': (
            f'Étape 1 : {one_fr}.\n'
            f'Étape 2 : {n} × {factor} = {sc.fmt_n(n * factor)}' + (f', puis + {extra} = {sc.fmt_n(total)}' if extra else '') + '\n'
            f'Réponse : {sc.fmt_n(total)} {small_fr}'
        ),
        'correct_answers':  [str(total)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Elapsed / end time
# ─────────────────────────────────────────────────────────────────────────────

def _times(level):
    """(start_minutes, duration_minutes) within a single day, end before 22 h."""
    if level == 'easy':
        sh = random.randint(7, 19)
        sm = random.choice([0, 30])
        dur = random.choice([30, 60, 90, 120, 150, 180])
    elif level == 'medium':
        sh = random.randint(7, 19)
        sm = random.choice(range(0, 60, 5))
        dur = random.choice([15, 20, 25, 35, 40, 45, 50, 55, 70, 75, 80, 90, 100, 105, 110])
    else:
        sh = random.randint(6, 19)
        sm = random.randint(0, 59)
        dur = random.randint(35, 260)
    start = sh * 60 + sm
    if start + dur > 22 * 60:
        start = 22 * 60 - dur - random.randint(0, 60)
    return start, dur


def _dur_str(mins):
    h, m = divmod(mins, 60)
    if h and m:
        return f'{h} h {m} min'
    if h:
        return f'{h} h'
    return f'{m} min'


def _clock_str(mins):
    h, m = divmod(mins, 60)
    return _fmt24(h, m)


def _clock_en(mins):
    h, m = divmod(mins, 60)
    return _en24(h, m)


def _elapsed_parts(start, end, clock, h_word, sep):
    """Bridge-through-the-hour steps, only the jumps really used."""
    next_hour = (start // 60 + 1) * 60 if start % 60 else start
    if next_hour > end:
        return None
    parts = []
    if next_hour != start:
        parts.append(f'{clock(start)} → {clock(next_hour)}{sep}{next_hour - start} min')
    full_h = (end - next_hour) // 60
    if full_h:
        parts.append(f'{clock(next_hour)} → {clock(next_hour + full_h * 60)}{sep}{h_word(full_h)}')
    rest = end - next_hour - full_h * 60
    if rest:
        parts.append(f'{clock(next_hour + full_h * 60)} → {clock(end)}{sep}{rest} min')
    return parts


def _elapsed_steps_en(start, end):
    parts = _elapsed_parts(start, end, _clock_en, lambda h: f"{h} hour{'s' if h > 1 else ''}", ': ')
    return f'From {_clock_en(start)} to {_clock_en(end)} is {end - start} min.' if parts is None else ' ; '.join(parts)


def _elapsed_steps_fr(start, end):
    parts = _elapsed_parts(start, end, _clock_str, lambda h: f'{h} h', ' : ')
    return f'De {_clock_str(start)} à {_clock_str(end)}, il y a {end - start} min.' if parts is None else ' ; '.join(parts)


def g4_elapsed_time_gen(level='easy'):
    start, dur = _times(level)
    end = start + dur
    who, g = sc.pick_actor()
    act_fr, act_en, act_g = pick_activity_for(start, dur)
    act_fr_cap = act_fr[0].upper() + act_fr[1:]
    answers = [_dur_str(dur)] + ([f'{dur} min'] if dur >= 60 else [])
    if dur < 60 or (start // 60 == end // 60):
        hint_fr = 'Compte les minutes de l’heure de début jusqu’à l’heure de fin.'
        hint_en = 'Count the minutes from the start time to the end time.'
    elif start % 60 == 0:
        hint_fr = "Le début est à l'heure pile : compte d'abord les heures entières, puis les minutes restantes."
        hint_en = 'The start is on the hour: count the whole hours first, then the leftover minutes.'
    else:
        hint_fr = "Compte d'abord jusqu'à l'heure pleine suivante, puis les heures entières, puis les minutes restantes."
        hint_en = 'Count up to the next full hour first, then the whole hours, then the leftover minutes.'
    steps_fr = [_elapsed_steps_fr(start, end)]
    steps_en = [_elapsed_steps_en(start, end)]
    if dur >= 60:
        steps_fr.append(f'Total = {dur} min = {_dur_str(dur)}')
        steps_en.append(f'Total = {dur} min = {_dur_en(dur)}')
    return {
        'q_type':           'text_input',
        'answer_type':      'duration',
        'prompt_fr':        f"{act_fr_cap} {sc.de(who)} commence à **{_clock_str(start)}** et se termine à **{_clock_str(end)}**. Combien de temps dure-t-{sc.pronoun_fr(act_g)} ? (réponds en h et min, ou en minutes)",
        'prompt_en':        f"{who}'s {act_en.replace('the ', '')} starts at **{_clock_en(start)}** and ends at **{_clock_en(end)}**. How long does it last? (answer in hours and minutes, or in minutes)",
        'hint_fr':          hint_fr,
        'hint_en':          hint_en,
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en':   ''.join(f'Step {i + 1}: {s}\n' for i, s in enumerate(steps_en)) + f'Answer: {_dur_en(dur)}',
        'explanation_fr':   ''.join(f'Étape {i + 1} : {s}\n' for i, s in enumerate(steps_fr)) + f'Réponse : {_dur_str(dur)}',
        'correct_answers':  answers,
    }


def g4_end_time_gen(level='easy'):
    start, dur = _times(level)
    end = start + dur
    who, g = sc.pick_actor()
    act_fr, act_en, act_g = pick_activity_for(start, dur)
    act_fr_cap = act_fr[0].upper() + act_fr[1:]
    eh, em = divmod(end, 60)
    # The start is given in 24-hour notation, so only the 24-hour end time is right
    # (no bare « 4 h 00 » for 16 h 00).
    answers = [_fmt24(eh, em), f'{eh}:{em:02d}']
    dh, dm = divmod(dur, 60)
    sh, sm = divmod(start, 60)
    mid = start + dh * 60
    steps_fr, steps_en = [], []
    if dh:
        steps_fr.append(f'{_clock_str(start)} + {dh} h = {_clock_str(mid)}')
        steps_en.append(f"{_clock_en(start)} + {dh} hour{'s' if dh > 1 else ''} = {_clock_en(mid)}")
    if dm:
        if sm + dm >= 60:
            over = sm + dm - 60
            steps_fr.append(f'Minutes : {sm} + {dm} = {sm + dm} min = 1 h' + (f' {over} min' if over else '')
                            + f', donc {_clock_str(mid)} + {dm} min = {_clock_str(end)}')
            steps_en.append(f'Minutes: {sm} + {dm} = {sm + dm} min = 1 hour' + (f' {over} min' if over else '')
                            + f', so {_clock_en(mid)} + {_dur_en(dm)} = {_clock_en(end)}')
        else:
            steps_fr.append(f'{_clock_str(mid)} + {dm} min = {_clock_str(end)}')
            steps_en.append(f'{_clock_en(mid)} + {_dur_en(dm)} = {_clock_en(end)}')
    return {
        'q_type':           'text_input',
        'answer_type':      'duration',
        'prompt_fr':        f"{act_fr_cap} {sc.de(who)} commence à **{_clock_str(start)}** et dure **{_dur_str(dur)}**. À quelle heure se termine-t-{sc.pronoun_fr(act_g)} ? (ex. 16 h 05)",
        'prompt_en':        f"{who}'s {act_en.replace('the ', '')} starts at **{_clock_en(start)}** and lasts **{_dur_en(dur)}**. At what time does it end? (e.g. 16:05)",
        'hint_fr':          "Ajoute d'abord les heures, puis les minutes. Si les minutes dépassent 60, passe à l'heure suivante.",
        'hint_en':          'Add the hours first, then the minutes. If the minutes go past 60, move to the next hour.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en':   ''.join(f'Step {i + 1}: {s}\n' for i, s in enumerate(steps_en)) + f'Answer: {_clock_en(end)}',
        'explanation_fr':   ''.join(f'Étape {i + 1} : {s}\n' for i, s in enumerate(steps_fr)) + f'Réponse : {_clock_str(end)}',
        'correct_answers':  answers,
    }
