"""
clock.py — Reading a clock and reasoning from it, grades 3 → 6.

Every problem shows an analog clock (``shape_data`` type 'clock') that gives
the *current* time; the child must read it first, then reason:

  g3-clock-later      QCM    – "In 30 minutes, what time will it be?" / "30 minutes ago…"
  g4-clock-back       typed  – "The game started 45 min ago. At what time did it start?"
                                (or: "ends in 45 min → at what time?")
  g5-clock-schedule   typed  – "Started 45 min ago and lasts 120 min. When does it end?"
                                / "How much time is left?"
  g6-clock-planning   typed  – same, plus breaks between two parts, "leave at the
                                latest at…" and answers in 24-hour notation (PM)

Gradation (per grade, per level):
  grade  easy                       medium                        hard
  3      whole/half hours, ±1 h     quarter hours, ±15/30/45 min  5-min, crossing the hour
  4      30-min steps               15-min steps, cross 1 hour    5-min steps, up to 2 h 30
  5      30-min steps, ≤ 2 h        15-min steps, ≤ 2 h 30        5-min steps, ≤ 3 h, crosses hours
  6      15-min, 2 steps            5-min, 3 steps (break)        any minute, 3-4 steps, 24 h notation
"""
import random

from .base import _tagged_shuffle_mc
from . import scenarios as sc


# ── helpers ──────────────────────────────────────────────────────────────────

def _fmt24(mins):
    h, m = divmod(mins, 60)
    return f'{h} h {m:02d}'


def _fmt12(mins):
    h, m = divmod(mins, 60)
    return f'{h % 12 or 12} h {m:02d}'


def _answers_for_time(mins):
    """All typed forms accepted for a clock time (checked as a duration in minutes)."""
    h, m = divmod(mins, 60)
    out = [_fmt24(mins), f'{h}:{m:02d}', f'{h}h{m:02d}']
    if h > 12:
        out += [_fmt12(mins), f'{h % 12}:{m:02d}', f'{h % 12}h{m:02d}']
    if m == 0:
        out += [f'{h} h']
    return out


def _dur(mins):
    h, m = divmod(mins, 60)
    if h and m:
        return f'{h} h {m} min'
    if h:
        return f'{h} h'
    return f'{m} min'


def _dur_answers(mins):
    return [_dur(mins), f'{mins} min']


def _clock_shape(mins):
    h, m = divmod(mins, 60)
    return [{'type': 'clock', 'hours': h % 12 or 12, 'minutes': m}]


def _period_fr(mins):
    return "de l'avant-midi" if mins < 12 * 60 else "de l'après-midi"


def _period_en(mins):
    return 'in the morning' if mins < 12 * 60 else 'in the afternoon'


def _mc_time(correct, wrong_list):
    """Multiple choice on a time; distractors tagged by misconception."""
    tagged = []
    for mins, tag, fb_en, fb_fr in wrong_list:
        if 0 <= mins < 24 * 60:
            tagged.append((_fmt12(mins), tag, fb_en, fb_fr))
    seen, uniq = {correct}, []
    for t in tagged:
        if t[0] not in seen:
            seen.add(t[0])
            uniq.append(t)
    # Always offer 4 distinct wrong times so the choice list never falls back to fillers.
    base = wrong_list[0][0] if wrong_list else 0
    for k in (5, 10, 15, 20, 25, 35, 40, 45, 50, 55):
        if len(uniq) >= 4:
            break
        for cand in (base + k, base - k):
            lab = _fmt12(cand)
            if 0 <= cand < 24 * 60 and lab not in seen:
                seen.add(lab)
                uniq.append((lab, 'wrong_minutes', 'Count the minutes carefully, 5 by 5.',
                             'Compte bien les minutes, 5 par 5.'))
    return _tagged_shuffle_mc(correct, uniq[:4] if len(uniq) > 4 else uniq)


def _pick_now(step, lo=7, hi=20):
    """Current time (minutes) on a `step`-minute grid, between lo h and hi h."""
    h = random.randint(lo, hi)
    m = random.choice(range(0, 60, step)) if step else random.randint(0, 59)
    return h * 60 + m


def _actor_activity():
    who, g = sc.pick_actor()
    act_fr, act_en, act_g = sc.pick_activity()
    act_fr_cap = act_fr[0].upper() + act_fr[1:]
    fr = f'{act_fr_cap} {sc.de(who)}'                 # "Le cours de piano de Léa"
    en = f"{who}'s {act_en.replace('the ', '')}"       # "Léa's piano lesson"
    return fr, en, act_g, who, g


# ── Grade 3: "what time will it be in N minutes?" ────────────────────────────

def g3_clock_later_gen(level='easy'):
    if level == 'easy':
        now = _pick_now(30, 1, 11)          # 12-h face, morning-ish hours 1 → 11
        delta = random.choice([60, 120, 180, 30])
    elif level == 'medium':
        now = _pick_now(15, 1, 11)
        delta = random.choice([15, 30, 45, 60, 90])
    else:
        now = _pick_now(5, 1, 11)
        delta = random.choice([5, 10, 20, 25, 35, 40, 50, 55, 65, 70])
        if (now % 60) + (delta % 60) < 60 and random.random() < 0.7:
            delta = 60 - (now % 60) + random.choice([5, 10, 15, 20])   # force crossing the hour
    later = random.random() < 0.65 or now - delta < 60
    target = now + delta if later else now - delta
    correct = _fmt12(target)
    dur = _dur(delta)
    if later:
        prompt_fr = f"Cette horloge indique l'heure qu'il est maintenant. Quelle heure sera-t-il dans **{dur}** ?"
        prompt_en = f"This clock shows the time now. What time will it be in **{dur}**?"
    else:
        prompt_fr = f"Cette horloge indique l'heure qu'il est maintenant. Quelle heure était-il il y a **{dur}** ?"
        prompt_en = f"This clock shows the time now. What time was it **{dur}** ago?"
    sign = 1 if later else -1
    wrong = [
        (now, 'no_change', 'You must add or remove the minutes from the time on the clock.',
         "Il faut ajouter ou enlever les minutes à l'heure de l'horloge."),
        (now - sign * delta, 'wrong_direction', '"In" means later (add); "ago" means earlier (subtract).',
         '« Dans » veut dire plus tard (on ajoute) ; « il y a » veut dire plus tôt (on enlève).'),
        (target + 60, 'hour_plus_one', 'Check the hour again: did you cross a full hour?',
         "Vérifie l'heure : as-tu vraiment passé une heure pleine ?"),
        (target - 60, 'hour_minus_one', 'Check the hour again.', "Vérifie l'heure."),
        (now + sign * (delta % 60 if delta >= 60 else delta + 60), 'wrong_unit',
         'Remember: 60 minutes make 1 hour.', 'Rappelle-toi : 60 minutes font 1 heure.'),
        (target + 30, 'wrong_minutes', 'Count the minutes carefully, 5 by 5.',
         'Compte bien les minutes, 5 par 5.'),
    ]
    op_fr = '+' if later else '−'
    op_en = op_fr
    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         "Lis d'abord l'heure sur l'horloge (petite aiguille = heures, grande = minutes), puis compte les minutes.",
        'hint_en':         'First read the clock (short hand = hours, long hand = minutes), then count the minutes.',
        'show_illustration': True,
        'shape_data':      _clock_shape(now),
        'choices':         _mc_time(correct, wrong),
        'pairs':           [],
        'explanation_en': (
            f'Step 1: The clock shows {_fmt12(now)}.\n'
            f'Step 2: {_fmt12(now)} {op_en} {dur} = {correct}\n'
            f'Answer: {correct}'
        ),
        'explanation_fr': (
            f"Étape 1 : L'horloge indique {_fmt12(now)}.\n"
            f'Étape 2 : {_fmt12(now)} {op_fr} {dur} = {correct}\n'
            f'Réponse : {correct}'
        ),
        'correct_answers': [correct],
    }


# ── Grade 4: start time (or end time) from the clock ─────────────────────────

def g4_clock_back_gen(level='easy'):
    if level == 'easy':
        now = _pick_now(30, 8, 20)
        delta = random.choice([30, 60, 90, 120])
    elif level == 'medium':
        now = _pick_now(5, 8, 20)
        delta = random.choice([15, 30, 45, 60, 75, 90, 105])
    else:
        now = _pick_now(5, 8, 20)
        delta = random.choice(range(35, 155, 5))
    fr_act, en_act, act_g, who, who_g = _actor_activity()
    back = random.random() < 0.6
    dur = _dur(delta)
    if back:
        target = now - delta
        prompt_fr = (f"L'horloge indique l'heure qu'il est maintenant. {fr_act} a commencé il y a **{dur}**. "
                     f"À quelle heure a-t-{sc.pronoun_fr(act_g)} commencé ?")
        prompt_en = (f"The clock shows the time now. {en_act} started **{dur}** ago. "
                     f"At what time did it start?")
        op = '−'
    else:
        target = now + delta
        prompt_fr = (f"L'horloge indique l'heure qu'il est maintenant. {fr_act} se termine dans **{dur}**. "
                     f"À quelle heure se termine-t-{sc.pronoun_fr(act_g)} ?")
        prompt_en = (f"The clock shows the time now. {en_act} ends in **{dur}**. "
                     f"At what time does it end?")
        op = '+'
    return {
        'q_type':          'text_input',
        'answer_type':     'duration',
        'prompt_fr':       prompt_fr + " (réponds en heures et minutes, ex. 9 h 15)",
        'prompt_en':       prompt_en + ' (answer in hours and minutes, e.g. 9 h 15)',
        'hint_fr':         "Lis l'heure sur l'horloge, puis enlève (« il y a ») ou ajoute (« dans ») les heures d'abord, les minutes ensuite.",
        'hint_en':         'Read the clock, then subtract ("ago") or add ("in") the hours first, then the minutes.',
        'show_illustration': True,
        'shape_data':      _clock_shape(now),
        'choices':         [],
        'pairs':           [],
        'explanation_en': (
            f'Step 1: The clock shows {_fmt12(now)}.\n'
            f'Step 2: {_fmt12(now)} {op} {delta // 60} h = {_fmt12(now + (delta // 60) * 60 * (-1 if back else 1))}\n'
            f'Step 3: {op} {delta % 60} min = {_fmt12(target)}\n'
            f'Answer: {_fmt12(target)}'
        ),
        'explanation_fr': (
            f"Étape 1 : L'horloge indique {_fmt12(now)}.\n"
            f'Étape 2 : {_fmt12(now)} {op} {delta // 60} h = {_fmt12(now + (delta // 60) * 60 * (-1 if back else 1))}\n'
            f'Étape 3 : {op} {delta % 60} min = {_fmt12(target)}\n'
            f'Réponse : {_fmt12(target)}'
        ),
        'correct_answers': _answers_for_time(target),
    }


# ── Grade 5: started N ago, lasts D → end time / time left ───────────────────

def _schedule_numbers(level):
    if level == 'easy':
        now = _pick_now(30, 9, 19)
        ago = random.choice([30, 60, 90])
        dur = random.choice([60, 90, 120])
    elif level == 'medium':
        now = _pick_now(15, 9, 19)
        ago = random.choice([15, 30, 45, 60, 75])
        dur = random.choice([45, 60, 75, 90, 105, 120, 150])
    else:
        now = _pick_now(5, 9, 19)
        ago = random.choice(range(15, 100, 5))
        dur = random.choice(range(60, 185, 5))
    while dur <= ago:            # the activity must still be running
        dur += 15
    return now, ago, dur


def g5_clock_schedule_gen(level='easy'):
    now, ago, dur = _schedule_numbers(level)
    fr_act, en_act, act_g, who, who_g = _actor_activity()
    start = now - ago
    end = start + dur
    ask_end = random.random() < 0.6
    dur_s, ago_s = _dur(dur), _dur(ago)
    if ask_end:
        prompt_fr = (f"L'horloge indique l'heure qu'il est maintenant. {fr_act} a commencé il y a **{ago_s}** "
                     f"et doit durer **{dur_s}** en tout. À quelle heure se terminera-t-{sc.pronoun_fr(act_g)} ? (ex. 15 h 30)")
        prompt_en = (f"The clock shows the time now. {en_act} started **{ago_s}** ago and must last "
                     f"**{dur_s}** in total. At what time will it end? (e.g. 15 h 30)")
        answers = _answers_for_time(end)
        final = _fmt24(end)
        step3_en = f'Step 3: end = {_fmt24(start)} + {dur_s} = {final}'
        step3_fr = f'Étape 3 : fin = {_fmt24(start)} + {dur_s} = {final}'
    else:
        left = dur - ago
        prompt_fr = (f"L'horloge indique l'heure qu'il est maintenant. {fr_act} a commencé il y a **{ago_s}** "
                     f"et doit durer **{dur_s}** en tout. Combien de temps reste-t-il ? (en h et min, ou en minutes)")
        prompt_en = (f"The clock shows the time now. {en_act} started **{ago_s}** ago and must last "
                     f"**{dur_s}** in total. How much time is left? (in h and min, or in minutes)")
        answers = _dur_answers(left)
        final = _dur(left)
        step3_en = f'Step 3: time left = {dur_s} − {ago_s} = {final} (it ends at {_fmt24(end)})'
        step3_fr = f'Étape 3 : temps restant = {dur_s} − {ago_s} = {final} (fin à {_fmt24(end)})'
    return {
        'q_type':          'text_input',
        'answer_type':     'duration',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         "1) Lis l'heure sur l'horloge. 2) Enlève le temps écoulé pour trouver l'heure de début. 3) Ajoute la durée totale.",
        'hint_en':         '1) Read the clock. 2) Subtract the time already spent to find the start. 3) Add the total duration.',
        'show_illustration': True,
        'shape_data':      _clock_shape(now),
        'choices':         [],
        'pairs':           [],
        'explanation_en': (
            f'Step 1: The clock shows {_fmt24(now)} ({_period_en(now)}).\n'
            f'Step 2: start = {_fmt24(now)} − {ago_s} = {_fmt24(start)}\n'
            f'{step3_en}\n'
            f'Answer: {final}'
        ),
        'explanation_fr': (
            f"Étape 1 : L'horloge indique {_fmt24(now)} ({_period_fr(now)}).\n"
            f'Étape 2 : début = {_fmt24(now)} − {ago_s} = {_fmt24(start)}\n'
            f'{step3_fr}\n'
            f'Réponse : {final}'
        ),
        'correct_answers': answers,
    }


# ── Grade 6: planning with breaks, departure times, 24-h notation ────────────

def g6_clock_planning_gen(level='easy'):
    if level == 'easy':
        step, now = 15, _pick_now(15, 12, 17)
        flavors = ['end', 'left']
    elif level == 'medium':
        step, now = 5, _pick_now(5, 12, 17)
        flavors = ['end', 'break', 'left']
    else:
        step, now = 1, _pick_now(0, 12, 17)
        flavors = ['break', 'depart', 'end']
    flavor = random.choice(flavors)
    fr_act, en_act, act_g, who, who_g = _actor_activity()
    r = lambda lo, hi: random.choice(range(lo, hi + 1, step)) if step > 1 else random.randint(lo, hi)
    period_fr, period_en = _period_fr(now), _period_en(now)
    lead_fr = f"L'horloge indique l'heure qu'il est maintenant, {period_fr}."
    lead_en = f'The clock shows the time now, {period_en}.'
    tail_fr = ' Réponds en notation 24 h (ex. 16 h 45).'
    tail_en = ' Answer in 24-hour notation (e.g. 16 h 45).'

    if flavor == 'end':
        ago, dur = r(15, 90), r(60, 180)
        while dur <= ago:
            dur += 15
        start, end = now - ago, now - ago + dur
        prompt_fr = (f"{lead_fr} {fr_act} a commencé il y a **{_dur(ago)}** et dure **{_dur(dur)}** en tout. "
                     f"À quelle heure se termine-t-{sc.pronoun_fr(act_g)} ?{tail_fr}")
        prompt_en = (f"{lead_en} {en_act} started **{_dur(ago)}** ago and lasts **{_dur(dur)}** in total. "
                     f"At what time does it end?{tail_en}")
        steps_en = [f'start = {_fmt24(now)} − {_dur(ago)} = {_fmt24(start)}',
                    f'end = {_fmt24(start)} + {_dur(dur)} = {_fmt24(end)}']
        steps_fr = [f'début = {_fmt24(now)} − {_dur(ago)} = {_fmt24(start)}',
                    f'fin = {_fmt24(start)} + {_dur(dur)} = {_fmt24(end)}']
        answers, final = _answers_for_time(end), _fmt24(end)

    elif flavor == 'left':
        ago, dur = r(15, 90), r(60, 180)
        while dur <= ago:
            dur += 15
        left = dur - ago
        end = now - ago + dur
        prompt_fr = (f"{lead_fr} {fr_act} a commencé il y a **{_dur(ago)}** et dure **{_dur(dur)}** en tout. "
                     f"Combien de temps reste-t-il ? (en h et min, ou en minutes)")
        prompt_en = (f"{lead_en} {en_act} started **{_dur(ago)}** ago and lasts **{_dur(dur)}** in total. "
                     f"How much time is left? (in h and min, or in minutes)")
        steps_en = [f'time left = {_dur(dur)} − {_dur(ago)} = {_dur(left)}',
                    f'check: it ends at {_fmt24(now)} + {_dur(left)} = {_fmt24(end)}']
        steps_fr = [f'temps restant = {_dur(dur)} − {_dur(ago)} = {_dur(left)}',
                    f'vérification : fin à {_fmt24(now)} + {_dur(left)} = {_fmt24(end)}']
        answers, final = _dur_answers(left), _dur(left)

    elif flavor == 'break':
        ago = r(10, 60)
        part1 = r(30, 90)
        while part1 <= ago:
            part1 += 10
        brk, part2 = r(10, 30), r(30, 90)
        start = now - ago
        end = start + part1 + brk + part2
        prompt_fr = (f"{lead_fr} {fr_act} a commencé il y a **{_dur(ago)}**. La première partie dure **{_dur(part1)}**, "
                     f"puis il y a une pause de **{_dur(brk)}**, puis une deuxième partie de **{_dur(part2)}**. "
                     f"À quelle heure tout sera-t-il fini ?{tail_fr}")
        prompt_en = (f"{lead_en} {en_act} started **{_dur(ago)}** ago. The first part lasts **{_dur(part1)}**, "
                     f"then there is a **{_dur(brk)}** break, then a second part of **{_dur(part2)}**. "
                     f"At what time will everything be over?{tail_en}")
        total = part1 + brk + part2
        steps_en = [f'start = {_fmt24(now)} − {_dur(ago)} = {_fmt24(start)}',
                    f'total = {_dur(part1)} + {_dur(brk)} + {_dur(part2)} = {_dur(total)}',
                    f'end = {_fmt24(start)} + {_dur(total)} = {_fmt24(end)}']
        steps_fr = [f'début = {_fmt24(now)} − {_dur(ago)} = {_fmt24(start)}',
                    f'total = {_dur(part1)} + {_dur(brk)} + {_dur(part2)} = {_dur(total)}',
                    f'fin = {_fmt24(start)} + {_dur(total)} = {_fmt24(end)}']
        answers, final = _answers_for_time(end), _fmt24(end)

    else:  # depart
        in_min, trip, early = r(60, 180), r(15, 55), r(5, 20)
        event = now + in_min
        leave = event - early - trip
        prompt_fr = (f"{lead_fr} {fr_act} commence dans **{_dur(in_min)}**. Le trajet prend **{_dur(trip)}** et "
                     f"{who} veut arriver **{_dur(early)}** à l'avance. À quelle heure, au plus tard, doit-{sc.pronoun_fr(who_g)} partir ?{tail_fr}")
        prompt_en = (f"{lead_en} {en_act} starts in **{_dur(in_min)}**. The trip takes **{_dur(trip)}** and "
                     f"{who} wants to arrive **{_dur(early)}** early. At the latest, at what time must {who} leave?{tail_en}")
        steps_en = [f'event = {_fmt24(now)} + {_dur(in_min)} = {_fmt24(event)}',
                    f'arrive by = {_fmt24(event)} − {_dur(early)} = {_fmt24(event - early)}',
                    f'leave by = {_fmt24(event - early)} − {_dur(trip)} = {_fmt24(leave)}']
        steps_fr = [f'événement = {_fmt24(now)} + {_dur(in_min)} = {_fmt24(event)}',
                    f'arrivée = {_fmt24(event)} − {_dur(early)} = {_fmt24(event - early)}',
                    f'départ = {_fmt24(event - early)} − {_dur(trip)} = {_fmt24(leave)}']
        answers, final = _answers_for_time(leave), _fmt24(leave)

    return {
        'q_type':          'text_input',
        'answer_type':     'duration',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         "Lis l'heure sur l'horloge et écris-la en notation 24 h (après-midi : + 12). Puis fais chaque étape dans l'ordre : enlever le temps écoulé, ajouter les durées.",
        'hint_en':         'Read the clock and write it in 24-hour notation (afternoon: + 12). Then do each step in order: subtract what has passed, add the durations.',
        'show_illustration': True,
        'shape_data':      _clock_shape(now),
        'choices':         [],
        'pairs':           [],
        'explanation_en': (f'Step 1: The clock shows {_fmt12(now)} {period_en} → {_fmt24(now)}.\n'
                           + '\n'.join(f'Step {i + 2}: {s}' for i, s in enumerate(steps_en))
                           + f'\nAnswer: {final}'),
        'explanation_fr': (f"Étape 1 : L'horloge indique {_fmt12(now)} {period_fr} → {_fmt24(now)}.\n"
                           + '\n'.join(f'Étape {i + 2} : {s}' for i, s in enumerate(steps_fr))
                           + f'\nRéponse : {final}'),
        'correct_answers': answers,
    }
