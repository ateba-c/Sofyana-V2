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


def _en24(mins):
    """English 24-hour notation: 16:45 (never the French « 16 h 45 »)."""
    h, m = divmod(mins, 60)
    return f'{h}:{m:02d}'


def _en12(mins):
    """English reading of the 12-hour face: 4:45."""
    h, m = divmod(mins, 60)
    return f'{h % 12 or 12}:{m:02d}'


def _uniq(seq):
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out


def _answers_for_time(mins):
    """All typed forms accepted for a clock time (checked as a duration in minutes)."""
    h, m = divmod(mins, 60)
    out = [_fmt24(mins), f'{h}:{m:02d}', f'{h}h{m:02d}']
    if h > 12:
        out += [_fmt12(mins), f'{h % 12}:{m:02d}', f'{h % 12}h{m:02d}']
    if m == 0:
        out += [f'{h} h']
    return out


def _answers_either_half(mins):
    """A time read on a 12-hour face with no AM/PM given: both readings are right (7 h 40 and 19 h 40)."""
    out = _answers_for_time(mins)
    if 60 <= mins < 12 * 60:
        out += _answers_for_time(mins + 12 * 60)
    return _uniq(out)


def _dur(mins):
    h, m = divmod(mins, 60)
    if h and m:
        return f'{h} h {m} min'
    if h:
        return f'{h} h'
    return f'{m} min'


def _dur_en(mins):
    """English duration in words: 1 hour 30 minutes, 2 hours, 45 minutes."""
    h, m = divmod(mins, 60)
    hs = f"{h} hour{'s' if h > 1 else ''}"
    ms = f"{m} minute{'s' if m > 1 else ''}"
    if h and m:
        return f'{hs} {ms}'
    return hs if h else ms


def _dur_answers(mins):
    return _uniq([_dur(mins), f'{mins} min'])


# Activities that only make sense at some times of day or for a short while.
# fr label → (earliest start, latest end, longest duration), in minutes.
_ACT_LIMITS = {
    'la récréation':          (9 * 60, 16 * 60, 30),
    'la lecture du soir':     (18 * 60, 22 * 60, 60),
    'la promenade du chien':  (None, None, 60),
    'le cours de piano':      (None, None, 60),
    'le cours de karaté':     (None, None, 90),
    'le cours de natation':   (None, None, 90),
    'le trajet en autobus':   (None, None, 90),
    "l'entraînement de soccer": (None, None, 120),
    'le match de basketball': (None, None, 150),
    'la partie de hockey':    (None, None, 180),
    'le film':                (None, None, 180),
    'la répétition de théâtre': (None, None, 180),
    "l'atelier de dessin":    (None, None, 180),
    'la fête d’anniversaire': (None, None, 240),
    'la sortie au musée':     (None, None, 300),
}


def pick_activity_for(start=None, dur=None):
    """sc.pick_activity(), but never an evening reading at noon or a four-hour recess."""
    for _ in range(60):
        act = sc.pick_activity()
        lo, hi, longest = _ACT_LIMITS.get(act[0], (None, None, 240))
        if dur is not None and dur > longest:
            continue
        if start is not None and lo is not None and start < lo:
            continue
        if start is not None and hi is not None and start + (dur or 0) > hi:
            continue
        return act
    return ('la sortie au musée', 'the museum trip', 'f')


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


def _actor_activity(start=None, dur=None):
    who, g = sc.pick_actor()
    act_fr, act_en, act_g = pick_activity_for(start, dur)
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
    dur, dur_en = _dur(delta), _dur_en(delta)
    if later:
        prompt_fr = f"Cette horloge indique l'heure qu'il est maintenant. Quelle heure sera-t-il dans **{dur}** ?"
        prompt_en = f"This clock shows the time now. What time will it be in **{dur_en}**?"
    else:
        prompt_fr = f"Cette horloge indique l'heure qu'il est maintenant. Quelle heure était-il il y a **{dur}** ?"
        prompt_en = f"This clock shows the time now. What time was it **{dur_en}** ago?"
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
    if delta % 60 == 0:
        what_fr, what_en = 'les heures', 'the hours'
    elif delta < 60:
        what_fr, what_en = 'les minutes', 'the minutes'
    else:
        what_fr, what_en = 'les heures, puis les minutes', 'the hours, then the minutes'
    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         ("Lis d'abord l'heure sur l'horloge (petite aiguille = heures, grande = minutes), puis "
                            f"{'ajoute' if later else 'enlève'} {what_fr}."),
        'hint_en':         ('First read the clock (short hand = hours, long hand = minutes), then '
                            f"{'add' if later else 'subtract'} {what_en}."),
        'show_illustration': True,
        'shape_data':      _clock_shape(now),
        'choices':         _mc_time(correct, wrong),
        'pairs':           [],
        'explanation_en': (
            f'Step 1: The clock shows {_en12(now)}.\n'
            f'Step 2: {_en12(now)} {op_en} {dur_en} = {_en12(target)}\n'
            f'Answer: {_en12(target)}'
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
    back = random.random() < 0.6
    target = now - delta if back else now + delta
    fr_act, en_act, act_g, who, who_g = _actor_activity(min(now, target), delta)
    dur, dur_en = _dur(delta), _dur_en(delta)
    if back:
        prompt_fr = (f"L'horloge indique l'heure qu'il est maintenant. {fr_act} a commencé il y a **{dur}**. "
                     f"À quelle heure a-t-{sc.pronoun_fr(act_g)} commencé ?")
        prompt_en = (f"The clock shows the time now. {en_act} started **{dur_en}** ago. "
                     f"At what time did it start?")
        op = '−'
    else:
        prompt_fr = (f"L'horloge indique l'heure qu'il est maintenant. {fr_act} se termine dans **{dur}**. "
                     f"À quelle heure se termine-t-{sc.pronoun_fr(act_g)} ?")
        prompt_en = (f"The clock shows the time now. {en_act} ends in **{dur_en}**. "
                     f"At what time does it end?")
        op = '+'
    sign = -1 if back else 1
    hours, mins = divmod(delta, 60)
    mid = now + sign * hours * 60
    steps_fr, steps_en = [], []
    if hours:
        steps_fr.append(f'{_fmt12(now)} {op} {hours} h = {_fmt12(mid)}')
        steps_en.append(f"{_en12(now)} {op} {_dur_en(hours * 60)} = {_en12(mid)}")
    if mins:
        steps_fr.append((f'{_fmt12(mid)} ' if not hours else '') + f'{op} {mins} min = {_fmt12(target)}')
        steps_en.append((f'{_en12(mid)} ' if not hours else '') + f'{op} {_dur_en(mins)} = {_en12(target)}')
    # The face shows no AM/PM: give (and accept) both readings, e.g. 7 h 40 or 19 h 40.
    h12 = (target // 60) % 12
    other = (target % (12 * 60)) + 12 * 60 if h12 else None
    final_fr = _fmt12(target) + (f' (ou {_fmt24(other)})' if other else '')
    final_en = _en12(target) + (f' (or {_en24(other)})' if other else '')
    carry_fr = " Si les minutes dépassent 60, échange 60 min contre 1 h ; s'il en manque, emprunte 1 h = 60 min."
    carry_en = ' If the minutes go past 60, trade 60 min for 1 hour; if there are not enough, borrow 1 hour = 60 min.'
    return {
        'q_type':          'text_input',
        'answer_type':     'duration',
        'prompt_fr':       prompt_fr + " (réponds en heures et minutes, ex. 9 h 15)",
        'prompt_en':       prompt_en + ' (answer in hours and minutes, e.g. 9:15)',
        'hint_fr':         ("Lis l'heure sur l'horloge, puis " + ('enlève' if back else 'ajoute')
                            + " les heures d'abord, les minutes ensuite." + carry_fr),
        'hint_en':         ('Read the clock, then ' + ('subtract' if back else 'add')
                            + ' the hours first, then the minutes.' + carry_en),
        'show_illustration': True,
        'shape_data':      _clock_shape(now),
        'choices':         [],
        'pairs':           [],
        'explanation_en': (f'Step 1: The clock shows {_en12(now)}.\n'
                           + ''.join(f'Step {i + 2}: {t}\n' for i, t in enumerate(steps_en))
                           + f'Answer: {final_en}'),
        'explanation_fr': (f"Étape 1 : L'horloge indique {_fmt12(now)}.\n"
                           + ''.join(f'Étape {i + 2} : {t}\n' for i, t in enumerate(steps_fr))
                           + f'Réponse : {final_fr}'),
        'correct_answers': _answers_either_half(target),
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
    start = now - ago
    end = start + dur
    fr_act, en_act, act_g, who, who_g = _actor_activity(start, dur)
    ask_end = random.random() < 0.6
    dur_s, ago_s = _dur(dur), _dur(ago)
    dur_e, ago_e = _dur_en(dur), _dur_en(ago)
    if ask_end:
        prompt_fr = (f"L'horloge indique l'heure qu'il est maintenant. {fr_act} a commencé il y a **{ago_s}** "
                     f"et doit durer **{dur_s}** en tout. À quelle heure se terminera-t-{sc.pronoun_fr(act_g)} ? (ex. 15 h 30)")
        prompt_en = (f"The clock shows the time now. {en_act} started **{ago_e}** ago and must last "
                     f"**{dur_e}** in total. At what time will it end? (e.g. 15:30)")
        # the face shows no AM/PM, so the 12-hour reading is accepted too
        answers = _answers_for_time(end)
        final, final_en = _fmt24(end), _en24(end)
        step3_en = f'Step 3: end = {_en24(start)} + {dur_e} = {final_en}'
        step3_fr = f'Étape 3 : fin = {_fmt24(start)} + {dur_s} = {final}'
        hint_fr = "1) Lis l'heure sur l'horloge. 2) Enlève le temps écoulé pour trouver l'heure de début. 3) Ajoute la durée totale."
        hint_en = '1) Read the clock. 2) Subtract the time already spent to find the start. 3) Add the total duration.'
    else:
        left = dur - ago
        prompt_fr = (f"L'horloge indique l'heure qu'il est maintenant. {fr_act} a commencé il y a **{ago_s}** "
                     f"et doit durer **{dur_s}** en tout. Combien de temps reste-t-il ? (en h et min, ou en minutes)")
        prompt_en = (f"The clock shows the time now. {en_act} started **{ago_e}** ago and must last "
                     f"**{dur_e}** in total. How much time is left? (in hours and minutes, or in minutes)")
        answers = _dur_answers(left)
        final, final_en = _dur(left), _dur_en(left)
        step3_en = f'Step 3: time left = {dur_e} − {ago_e} = {final_en} (it ends at {_en24(end)})'
        step3_fr = f'Étape 3 : temps restant = {dur_s} − {ago_s} = {final} (fin à {_fmt24(end)})'
        hint_fr = "Le temps qui reste = la durée totale − le temps déjà écoulé. (Tu peux vérifier avec l'heure de fin.)"
        hint_en = 'Time left = total duration − time already spent. (You can check with the end time.)'
    return {
        'q_type':          'text_input',
        'answer_type':     'duration',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         hint_fr,
        'hint_en':         hint_en,
        'show_illustration': True,
        'shape_data':      _clock_shape(now),
        'choices':         [],
        'pairs':           [],
        'explanation_en': (
            f'Step 1: The clock shows {_en24(now)} ({_period_en(now)}).\n'
            f'Step 2: start = {_en24(now)} − {ago_e} = {_en24(start)}\n'
            f'{step3_en}\n'
            f'Answer: {final_en}'
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
    r = lambda lo, hi: random.choice(range(lo, hi + 1, step)) if step > 1 else random.randint(lo, hi)
    period_fr, period_en = _period_fr(now), _period_en(now)
    lead_fr = f"L'horloge indique l'heure qu'il est maintenant, {period_fr}."
    lead_en = f'The clock shows the time now, {period_en}.'
    tail_fr = ' Réponds en notation 24 h (ex. 16 h 45).'
    tail_en = ' Answer in 24-hour notation (e.g. 16:45).'
    D, E, T = _dur, _dur_en, _en24
    # 12 h xx in the afternoon stays 12 h xx: only 1 h → 11 h get + 12.
    read_fr = ("Lis l'heure sur l'horloge et écris-la en notation 24 h (l'après-midi, ajoute 12 aux heures de 1 à 11 ; "
               "12 h reste 12 h).")
    read_en = ('Read the clock and write it in 24-hour notation (in the afternoon, add 12 to hours 1 to 11; '
               '12 stays 12).')

    if flavor in ('end', 'left'):
        ago, dur = r(15, 90), r(60, 180)
        while dur <= ago:
            dur += 15
        start, end = now - ago, now - ago + dur
        fr_act, en_act, act_g, who, who_g = _actor_activity(start, dur)
        if flavor == 'end':
            prompt_fr = (f"{lead_fr} {fr_act} a commencé il y a **{D(ago)}** et dure **{D(dur)}** en tout. "
                         f"À quelle heure se termine-t-{sc.pronoun_fr(act_g)} ?{tail_fr}")
            prompt_en = (f"{lead_en} {en_act} started **{E(ago)}** ago and lasts **{E(dur)}** in total. "
                         f"At what time does it end?{tail_en}")
            steps_en = [f'start = {T(now)} − {E(ago)} = {T(start)}',
                        f'end = {T(start)} + {E(dur)} = {T(end)}']
            steps_fr = [f'début = {_fmt24(now)} − {D(ago)} = {_fmt24(start)}',
                        f'fin = {_fmt24(start)} + {D(dur)} = {_fmt24(end)}']
            answers, final, final_en = _answers_for_time(end), _fmt24(end), T(end)
            hint_fr = read_fr + " Puis enlève le temps écoulé pour trouver le début, et ajoute la durée totale."
            hint_en = read_en + ' Then subtract the time already spent to find the start, and add the total duration.'
        else:
            left = dur - ago
            prompt_fr = (f"{lead_fr} {fr_act} a commencé il y a **{D(ago)}** et dure **{D(dur)}** en tout. "
                         f"Combien de temps reste-t-il ? (en h et min, ou en minutes)")
            prompt_en = (f"{lead_en} {en_act} started **{E(ago)}** ago and lasts **{E(dur)}** in total. "
                         f"How much time is left? (in hours and minutes, or in minutes)")
            steps_en = [f'time left = {E(dur)} − {E(ago)} = {E(left)}',
                        f'check: it ends at {T(now)} + {E(left)} = {T(end)}']
            steps_fr = [f'temps restant = {D(dur)} − {D(ago)} = {D(left)}',
                        f'vérification : fin à {_fmt24(now)} + {D(left)} = {_fmt24(end)}']
            answers, final, final_en = _dur_answers(left), D(left), E(left)
            hint_fr = "Le temps qui reste = la durée totale − le temps déjà écoulé."
            hint_en = 'Time left = total duration − time already spent.'

    elif flavor == 'break':
        ago = r(10, 60)
        part1 = r(30, 90)
        while part1 <= ago:
            part1 += 10
        brk, part2 = r(10, 30), r(30, 90)
        start = now - ago
        total = part1 + brk + part2
        end = start + total
        fr_act, en_act, act_g, who, who_g = _actor_activity(start, total)
        prompt_fr = (f"{lead_fr} {fr_act} a commencé il y a **{D(ago)}**. La première partie dure **{D(part1)}**, "
                     f"puis il y a une pause de **{D(brk)}**, puis une deuxième partie de **{D(part2)}**. "
                     f"À quelle heure tout sera-t-il fini ?{tail_fr}")
        prompt_en = (f"{lead_en} {en_act} started **{E(ago)}** ago. The first part lasts **{E(part1)}**, "
                     f"then there is a **{E(brk)}** break, then a second part of **{E(part2)}**. "
                     f"At what time will everything be over?{tail_en}")
        steps_en = [f'start = {T(now)} − {E(ago)} = {T(start)}',
                    f'total = {E(part1)} + {E(brk)} + {E(part2)} = {E(total)}',
                    f'end = {T(start)} + {E(total)} = {T(end)}']
        steps_fr = [f'début = {_fmt24(now)} − {D(ago)} = {_fmt24(start)}',
                    f'total = {D(part1)} + {D(brk)} + {D(part2)} = {D(total)}',
                    f'fin = {_fmt24(start)} + {D(total)} = {_fmt24(end)}']
        answers, final, final_en = _answers_for_time(end), _fmt24(end), T(end)
        hint_fr = read_fr + (" Enlève le temps écoulé pour trouver le début, additionne les deux parties et la pause, "
                             "puis ajoute ce total au début.")
        hint_en = read_en + (' Subtract the time already spent to find the start, add up both parts and the break, '
                             'then add that total to the start.')

    else:  # depart
        in_min, trip, early = r(60, 180), r(15, 55), r(5, 20)
        event = now + in_min
        leave = event - early - trip
        fr_act, en_act, act_g, who, who_g = _actor_activity(event, 60)
        prompt_fr = (f"{lead_fr} {fr_act} commence dans **{D(in_min)}**. Le trajet prend **{D(trip)}** et "
                     f"{who} veut arriver **{D(early)}** à l'avance. À quelle heure, au plus tard, "
                     f"doit-{sc.pronoun_fr(who_g)} partir ?{tail_fr}")
        prompt_en = (f"{lead_en} {en_act} starts in **{E(in_min)}**. The trip takes **{E(trip)}** and "
                     f"{who} wants to arrive **{E(early)}** early. At the latest, at what time must {who} leave?{tail_en}")
        steps_en = [f'event = {T(now)} + {E(in_min)} = {T(event)}',
                    f'arrive by = {T(event)} − {E(early)} = {T(event - early)}',
                    f'leave by = {T(event - early)} − {E(trip)} = {T(leave)}']
        steps_fr = [f'événement = {_fmt24(now)} + {D(in_min)} = {_fmt24(event)}',
                    f'arrivée = {_fmt24(event)} − {D(early)} = {_fmt24(event - early)}',
                    f'départ = {_fmt24(event - early)} − {D(trip)} = {_fmt24(leave)}']
        answers, final, final_en = _answers_for_time(leave), _fmt24(leave), T(leave)
        hint_fr = read_fr + " Ajoute le temps d'attente pour trouver le début de l'événement, puis enlève l'avance et le trajet."
        hint_en = read_en + ' Add the waiting time to find when the event starts, then subtract the early arrival and the trip.'

    return {
        'q_type':          'text_input',
        'answer_type':     'duration',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         hint_fr,
        'hint_en':         hint_en,
        'show_illustration': True,
        'shape_data':      _clock_shape(now),
        'choices':         [],
        'pairs':           [],
        'explanation_en': (f'Step 1: The clock shows {_en12(now)} {period_en} → {T(now)}.\n'
                           + '\n'.join(f'Step {i + 2}: {s}' for i, s in enumerate(steps_en))
                           + f'\nAnswer: {final_en}'),
        'explanation_fr': (f"Étape 1 : L'horloge indique {_fmt12(now)} {period_fr} → {_fmt24(now)}.\n"
                           + '\n'.join(f'Étape {i + 2} : {s}' for i, s in enumerate(steps_fr))
                           + f'\nRéponse : {final}'),
        'correct_answers': answers,
    }
