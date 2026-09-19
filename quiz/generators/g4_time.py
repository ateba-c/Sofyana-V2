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


def _fmt24(h, m):
    return f"{h} h {m:02d}"


def _fmt12(h, m):
    h12 = h % 12 or 12
    return f"{h12} h {m:02d}"


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
        'hint_en':          'Read the clock. In the afternoon, add 12 to the hour (except 12 itself). At midnight, 12 becomes 0 h.',
        'show_illustration': True,
        'shape_data':       [{'type': 'clock', 'hours': h12, 'minutes': m}],
        'choices':          _tagged_shuffle_mc(correct, tagged),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: The clock shows {_fmt12(h, m)}.\n'
            f'Step 2: It is {_period_en(h)}, so {"add 12 to the hour: " + str(h12) + " + 12 = " + str(h) if 12 < h else "the hour stays " + str(h) if h != 0 else "12 at midnight is written 0"}.\n'
            f'Answer: {correct}'
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

# (fr_template, en_template, factor, unit_fr, unit_en)
# Each converts "N big units" → small units; the scenario wraps it.
_CONVERSIONS = {
    'easy': [
        ('heures', 'hours', 'minutes', 'minutes', 60, (1, 5)),
        ('jours', 'days', 'heures', 'hours', 24, (1, 4)),
        ('semaines', 'weeks', 'jours', 'days', 7, (1, 6)),
        ('ans', 'years', 'mois', 'months', 12, (1, 5)),
        ('minutes', 'minutes', 'secondes', 'seconds', 60, (1, 5)),
    ],
    'medium': [
        ('heures', 'hours', 'minutes', 'minutes', 60, (2, 9)),
        ('jours', 'days', 'heures', 'hours', 24, (2, 7)),
        ('semaines', 'weeks', 'jours', 'days', 7, (3, 12)),
        ('ans', 'years', 'semaines', 'weeks', 52, (1, 3)),
        ('ans', 'years', 'jours', 'days', 365, (1, 2)),
    ],
    'hard': [
        ('heures', 'hours', 'minutes', 'minutes', 60, (3, 12)),
        ('jours', 'days', 'heures', 'hours', 24, (3, 10)),
        ('semaines', 'weeks', 'heures', 'hours', 168, (1, 2)),
        ('ans', 'years', 'jours', 'days', 365, (1, 3)),
        ('jours', 'days', 'minutes', 'minutes', 1440, (1, 2)),
    ],
}

_CTX = [
    # (fr, en): {who}, {act}, {dur}
    ("{act} {de_who} dure {dur}.", "{who}'s {act} lasts {dur}."),
    ("{who} est parti·e en voyage pendant {dur}.", "{who} went on a trip for {dur}."),
    ("{who} a attendu {dur} avant de recevoir son colis.", "{who} waited {dur} to receive a package."),
    ("Les vacances {de_who} durent {dur}.", "{who}'s holidays last {dur}."),
    ("La plante {de_who} a mis {dur} à fleurir.", "{who}'s plant took {dur} to bloom."),
]


def g4_time_units_gen(level='easy'):
    big_fr, big_en, small_fr, small_en, factor, (lo, hi) = random.choice(_CONVERSIONS[level])
    n = random.randint(lo, hi)
    extra = 0
    # Compound durations: 2 h 20 min, 1 day 6 h, 2 weeks 3 days
    if level != 'easy' and random.random() < 0.5:
        extra = random.randint(1, factor - 1) if factor <= 60 else random.randint(1, 23)
        if factor > 60 and factor != 1440:
            extra = 0
    total = n * factor + extra
    big_fr_s = big_fr[:-1] if n == 1 and big_fr.endswith('s') else big_fr
    big_en_s = big_en[:-1] if n == 1 and big_en.endswith('s') else big_en
    dur_fr = f"**{n} {big_fr_s}**" + (f" **{extra} {small_fr}**" if extra else '')
    dur_en = f"**{n} {big_en_s}**" + (f" **{extra} {small_en}**" if extra else '')

    who, g = sc.pick_actor()
    act_fr, act_en, _ = sc.pick_activity()
    ctx_fr, ctx_en = random.choice(_CTX)
    story_fr = ctx_fr.format(who=who, de_who=sc.de(who), act=act_fr[0].upper() + act_fr[1:], dur=dur_fr)
    story_en = ctx_en.format(who=who, act=act_en.replace('the ', ''), dur=dur_en)
    story_fr = story_fr.replace('parti·e', 'partie' if g == 'f' else 'parti')

    return {
        'q_type':           'text_input',
        'answer_type':      'integer',
        'prompt_fr':        f"{story_fr} Combien {'d’' if small_fr[0] in 'aeiouh' else 'de '}**{small_fr}** cela fait-il ?",
        'prompt_en':        f"{story_en} How many **{small_en}** is that?",
        'hint_fr':          f"1 {big_fr_s if n == 1 else big_fr[:-1] if big_fr.endswith('s') else big_fr} = {factor} {small_fr}. Multiplie, puis ajoute le reste s'il y en a un.",
        'hint_en':          f"1 {big_en[:-1] if big_en.endswith('s') else big_en} = {factor} {small_en}. Multiply, then add the leftover if there is one.",
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: 1 {big_en[:-1] if big_en.endswith("s") else big_en} = {factor} {small_en}.\n'
            f'Step 2: {n} × {factor} = {sc.fmt_n(n * factor)}' + (f', then + {extra} = {sc.fmt_n(total)}' if extra else '') + '\n'
            f'Answer: {sc.fmt_n(total)} {small_en}'
        ),
        'explanation_fr': (
            f'Étape 1 : 1 {big_fr[:-1] if big_fr.endswith("s") else big_fr} = {factor} {small_fr}.\n'
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


def _elapsed_steps_en(start, end):
    """Bridge-through-the-hour explanation."""
    next_hour = (start // 60 + 1) * 60 if start % 60 else start
    if next_hour > end:
        return f'From {_clock_str(start)} to {_clock_str(end)} is {end - start} min.'
    parts = []
    if next_hour != start:
        parts.append(f'{_clock_str(start)} → {_clock_str(next_hour)}: {next_hour - start} min')
    full_h = (end - next_hour) // 60
    if full_h:
        parts.append(f'{_clock_str(next_hour)} → {_clock_str(next_hour + full_h * 60)}: {full_h} h')
    rest = end - next_hour - full_h * 60
    if rest:
        parts.append(f'{_clock_str(next_hour + full_h * 60)} → {_clock_str(end)}: {rest} min')
    return ' ; '.join(parts)


def _elapsed_steps_fr(start, end):
    next_hour = (start // 60 + 1) * 60 if start % 60 else start
    if next_hour > end:
        return f'De {_clock_str(start)} à {_clock_str(end)}, il y a {end - start} min.'
    parts = []
    if next_hour != start:
        parts.append(f'{_clock_str(start)} → {_clock_str(next_hour)} : {next_hour - start} min')
    full_h = (end - next_hour) // 60
    if full_h:
        parts.append(f'{_clock_str(next_hour)} → {_clock_str(next_hour + full_h * 60)} : {full_h} h')
    rest = end - next_hour - full_h * 60
    if rest:
        parts.append(f'{_clock_str(next_hour + full_h * 60)} → {_clock_str(end)} : {rest} min')
    return ' ; '.join(parts)


def g4_elapsed_time_gen(level='easy'):
    start, dur = _times(level)
    end = start + dur
    who, g = sc.pick_actor()
    act_fr, act_en, act_g = sc.pick_activity()
    act_fr_cap = act_fr[0].upper() + act_fr[1:]
    answers = [_dur_str(dur), f'{dur} min']
    return {
        'q_type':           'text_input',
        'answer_type':      'duration',
        'prompt_fr':        f"{act_fr_cap} {sc.de(who)} commence à **{_clock_str(start)}** et se termine à **{_clock_str(end)}**. Combien de temps dure-t-{sc.pronoun_fr(act_g)} ? (réponds en h et min, ou en minutes)",
        'prompt_en':        f"{who}'s {act_en.replace('the ', '')} starts at **{_clock_str(start)}** and ends at **{_clock_str(end)}**. How long does it last? (answer in h and min, or in minutes)",
        'hint_fr':          "Compte d'abord jusqu'à l'heure pleine suivante, puis les heures entières, puis les minutes restantes.",
        'hint_en':          'Count up to the next full hour first, then the whole hours, then the leftover minutes.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: {_elapsed_steps_en(start, end)}\n'
            f'Step 2: Total = {dur} min = {_dur_str(dur)}\n'
            f'Answer: {_dur_str(dur)}'
        ),
        'explanation_fr': (
            f'Étape 1 : {_elapsed_steps_fr(start, end)}\n'
            f'Étape 2 : Total = {dur} min = {_dur_str(dur)}\n'
            f'Réponse : {_dur_str(dur)}'
        ),
        'correct_answers':  answers,
    }


def g4_end_time_gen(level='easy'):
    start, dur = _times(level)
    end = start + dur
    who, g = sc.pick_actor()
    act_fr, act_en, act_g = sc.pick_activity()
    act_fr_cap = act_fr[0].upper() + act_fr[1:]
    eh, em = divmod(end, 60)
    answers = [_fmt24(eh, em), f'{eh}:{em:02d}']
    if eh > 12:
        answers += [_fmt12(eh, em), f'{eh % 12}:{em:02d}']
    return {
        'q_type':           'text_input',
        'answer_type':      'duration',
        'prompt_fr':        f"{act_fr_cap} {sc.de(who)} commence à **{_clock_str(start)}** et dure **{_dur_str(dur)}**. À quelle heure se termine-t-{sc.pronoun_fr(act_g)} ?",
        'prompt_en':        f"{who}'s {act_en.replace('the ', '')} starts at **{_clock_str(start)}** and lasts **{_dur_str(dur)}**. At what time does it end?",
        'hint_fr':          "Ajoute d'abord les heures, puis les minutes. Si les minutes dépassent 60, passe à l'heure suivante.",
        'hint_en':          'Add the hours first, then the minutes. If the minutes go past 60, move to the next hour.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          [],
        'pairs':            [],
        'explanation_en': (
            f'Step 1: {_clock_str(start)} + {dur // 60} h = {_clock_str(start + (dur // 60) * 60)}\n'
            f'Step 2: + {dur % 60} min = {_clock_str(end)}\n'
            f'Answer: {_clock_str(end)}'
        ),
        'explanation_fr': (
            f'Étape 1 : {_clock_str(start)} + {dur // 60} h = {_clock_str(start + (dur // 60) * 60)}\n'
            f'Étape 2 : + {dur % 60} min = {_clock_str(end)}\n'
            f'Réponse : {_clock_str(end)}'
        ),
        'correct_answers':  answers,
    }
