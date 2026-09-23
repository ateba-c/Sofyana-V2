"""
resolution.py — the 4th level, "Résolution" (problem solving), for qualifying skills.

Pedagogy: after easy → medium → hard (mechanics), the child gets real-world
problems where they must pick the data, choose the operation, and often chain
two or three calculations.  Every problem is generated from the scenario bank
so the story changes each time; the explanation shows every stage.

Each *family* below builds problems for a given grade (4 or 6) and mixes
one-step and multi-step variants.  ``RESOLUTION_FAMILIES`` maps a skill slug to
the families it draws from; ``resolution_gen(slug)`` returns a generator
callable with the usual ``gen(level)`` signature.
"""
import random
from . import scenarios as sc

# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

def _problem(prompt_fr, prompt_en, answer, steps_fr, steps_en, hint_fr, hint_en, answer_type='integer', answers=None):
    return {
        'q_type': 'text_input',
        'answer_type': answer_type,
        'level': 'resolution',
        'prompt_fr': prompt_fr,
        'prompt_en': prompt_en,
        'hint_fr': hint_fr,
        'hint_en': hint_en,
        'show_illustration': False,
        'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_fr': '\n'.join(f'Étape {i + 1} : {s}' for i, s in enumerate(steps_fr[:-1])) + f'\nRéponse : {steps_fr[-1]}',
        'explanation_en': '\n'.join(f'Step {i + 1}: {s}' for i, s in enumerate(steps_en[:-1])) + f'\nAnswer: {steps_en[-1]}',
        'correct_answers': answers or [str(answer)],
        'points': 3,
        'time_limit': 90,
    }


def _clock(mins):
    h, m = divmod(mins, 60)
    return f'{h} h {m:02d}'


def _dur(mins):
    h, m = divmod(mins, 60)
    if h and m:
        return f'{h} h {m} min'
    return f'{h} h' if h else f'{m} min'


def _cap(s):
    return s[0].upper() + s[1:]


N = sc.fmt_n


# ─────────────────────────────────────────────────────────────────────────────
# Family 1 — inventory: groups of 1000/100/10 + loose, then sold / added
# ─────────────────────────────────────────────────────────────────────────────

def inventory(grade):
    key, thing = sc.pick_thing('object' if grade >= 5 else None)
    cat = thing[5]
    cont = sc.pick_container(cat)
    who_fr, who_en, g = sc.pick_role()
    who_fr, who_en = _cap(who_fr), _cap(who_en)
    verb_fr, verb_en, _ = sc.pick_verb(cat)
    if grade <= 4:
        groups = [(random.randint(2, 9), 100), (random.randint(1, 9), 10)]
        loose = random.randint(0, 9)
    else:
        groups = [(random.randint(2, 9), 1000), (random.randint(3, 15), 100), (random.randint(1, 20), 10)]
        loose = random.randint(0, 99)
    total = sum(c * s for c, s in groups) + loose
    parts_fr = [f"**{c}** {sc.cont(cont, c, 'fr')} de **{N(s)}** {sc.noun(thing, s, 'fr')}" for c, s in groups]
    parts_en = [f"**{c}** {sc.cont(cont, c, 'en')} of **{N(s)}** {sc.noun(thing, s, 'en')}" for c, s in groups]
    if loose:
        parts_fr.append(f"**{loose}** {sc.noun(thing, loose, 'fr')} en vrac")
        parts_en.append(f"**{loose}** loose {sc.noun(thing, loose, 'en')}")
    story_fr = f"{who_fr} {verb_fr} {', '.join(parts_fr[:-1])} et {parts_fr[-1]}."
    story_en = f"{who_en} {verb_en} {', '.join(parts_en[:-1])} and {parts_en[-1]}."
    calc = ' + '.join(f'{c} × {N(s)}' for c, s in groups) + (f' + {loose}' if loose else '')
    vals = ' + '.join(N(c * s) for c, s in groups) + (f' + {loose}' if loose else '')

    variant = random.choice(['total', 'sold', 'sold_boxes', 'need'])
    if variant == 'total':
        return _problem(
            f"{story_fr} Combien de {sc.noun(thing, 2, 'fr')} cela fait-il en tout ?",
            f"{story_en} How many {sc.noun(thing, 2, 'en')} is that in total?",
            total,
            [f'{calc} = {vals}', f'{vals} = {N(total)}', f'{N(total)} {sc.noun(thing, total, "fr")}'],
            [f'{calc} = {vals}', f'{vals} = {N(total)}', f'{N(total)} {sc.noun(thing, total, "en")}'],
            'Calcule chaque groupe (contenants × quantité), puis additionne tout.',
            'Work out each group (containers × amount), then add everything.')
    if variant == 'sold':
        sold = random.randint(total // 10, total // 2)
        left = total - sold
        return _problem(
            f"{story_fr} Ensuite, {sc.pronoun_fr(g)} en vend **{N(sold)}**. Combien de {sc.noun(thing, 2, 'fr')} reste-t-il ?",
            f"{story_en} Then {sc.pronoun_en(g)} sells **{N(sold)}** of them. How many {sc.noun(thing, 2, 'en')} are left?",
            left,
            [f'Total : {calc} = {N(total)}', f'{N(total)} − {N(sold)} = {N(left)}', f'{N(left)} {sc.noun(thing, left, "fr")}'],
            [f'Total: {calc} = {N(total)}', f'{N(total)} − {N(sold)} = {N(left)}', f'{N(left)} {sc.noun(thing, left, "en")}'],
            "Trouve d'abord le total, puis enlève ce qui est vendu.",
            'Find the total first, then take away what was sold.')
    if variant == 'sold_boxes':
        c0, s0 = groups[-1]
        k = random.randint(1, max(1, c0 - 1))
        left = total - k * s0
        return _problem(
            f"{story_fr} {_cap(sc.pronoun_fr(g))} donne ensuite **{k}** {sc.cont(cont, k, 'fr')} de {N(s0)}. Combien de {sc.noun(thing, 2, 'fr')} reste-t-il ?",
            f"{story_en} {_cap(sc.pronoun_en(g))} then gives away **{k}** {sc.cont(cont, k, 'en')} of {N(s0)}. How many {sc.noun(thing, 2, 'en')} are left?",
            left,
            [f'Total : {calc} = {N(total)}', f'Donné : {k} × {N(s0)} = {N(k * s0)}', f'{N(total)} − {N(k * s0)} = {N(left)}', f'{N(left)} {sc.noun(thing, left, "fr")}'],
            [f'Total: {calc} = {N(total)}', f'Given away: {k} × {N(s0)} = {N(k * s0)}', f'{N(total)} − {N(k * s0)} = {N(left)}', f'{N(left)} {sc.noun(thing, left, "en")}'],
            'Total, puis la quantité donnée (contenants × quantité), puis soustrais.',
            'Total, then the amount given away (containers × amount), then subtract.')
    # need: how many more to reach a round target
    target = (total // 1000 + 1) * 1000 if grade >= 5 else (total // 100 + 1) * 100
    need = target - total
    return _problem(
        f"{story_fr} {_cap(sc.pronoun_fr(g))} veut en avoir **{N(target)}**. Combien de {sc.noun(thing, 2, 'fr')} manque-t-il ?",
        f"{story_en} {_cap(sc.pronoun_en(g))} wants **{N(target)}** of them. How many {sc.noun(thing, 2, 'en')} are missing?",
        need,
        [f'Total : {calc} = {N(total)}', f'{N(target)} − {N(total)} = {N(need)}', f'{N(need)} {sc.noun(thing, need, "fr")}'],
        [f'Total: {calc} = {N(total)}', f'{N(target)} − {N(total)} = {N(need)}', f'{N(need)} {sc.noun(thing, need, "en")}'],
        "Trouve le total, puis la différence avec l'objectif.",
        'Find the total, then the difference with the goal.')


# ─────────────────────────────────────────────────────────────────────────────
# Family 2 — money: bills, two people, purchase and change
# ─────────────────────────────────────────────────────────────────────────────

_BILLS = [100, 50, 20, 10, 5]


def _stack(grade):
    hi = {3: 3, 4: 4}.get(grade, 9)
    bills = [20, 10, 5] if grade == 3 else _BILLS[1:] if grade == 4 else _BILLS
    c = {b: random.randint(0, hi) for b in bills}
    if sum(c.values()) == 0:
        c[20] = 2
    return c


def _stack_txt(c, lang):
    parts = [f"{n} billet{'s' if n > 1 else ''} de {b} $" if lang == 'fr' else f"{n} ${b} bill{'s' if n > 1 else ''}"
             for b, n in c.items() if n]
    return ', '.join(parts[:-1]) + ((' et ' if lang == 'fr' else ' and ') if len(parts) > 1 else '') + parts[-1]


def _total(c):
    return sum(b * n for b, n in c.items())


def _calc(c):
    return ' + '.join(f'{n} × {b}' for b, n in c.items() if n) + f' = {N(_total(c))} $'


_ITEMS = [('un vélo', 'a bike'), ('une console de jeux', 'a game console'), ('une tente', 'a tent'),
          ('un télescope', 'a telescope'), ('des patins', 'skates'), ('une guitare', 'a guitar'),
          ('un aquarium', 'an aquarium'), ('un drone', 'a drone')]


def money(grade):
    a_name, ga = sc.pick_actor()
    b_name, gb = sc.pick_actor()
    while b_name == a_name:
        b_name, gb = sc.pick_actor()
    a, b = _stack(grade), _stack(grade)
    ta, tb = _total(a), _total(b)
    variant = random.choice(['together', 'difference', 'change', 'save'])
    if variant == 'together':
        return _problem(
            f"{a_name} a {_stack_txt(a, 'fr')}. {b_name} a {_stack_txt(b, 'fr')}. Combien d'argent ont-{'elles' if ga == gb == 'f' else 'ils'} ensemble ?",
            f"{a_name} has {_stack_txt(a, 'en')}. {b_name} has {_stack_txt(b, 'en')}. How much money do they have together?",
            ta + tb,
            [f'{a_name} : {_calc(a)}', f'{b_name} : {_calc(b)}', f'{N(ta)} + {N(tb)} = {N(ta + tb)}', f'{N(ta + tb)} $'],
            [f'{a_name}: {_calc(a)}', f'{b_name}: {_calc(b)}', f'{N(ta)} + {N(tb)} = {N(ta + tb)}', f'${N(ta + tb)}'],
            "Calcule chaque somme (billets × valeur), puis additionne.", 'Work out each amount (bills × value), then add.',
            'money', [f'{ta + tb} $', str(ta + tb)])
    if variant == 'difference':
        rich, poor = (a_name, b_name) if ta >= tb else (b_name, a_name)
        d = abs(ta - tb)
        return _problem(
            f"{a_name} a {_stack_txt(a, 'fr')}. {b_name} a {_stack_txt(b, 'fr')}. Qui a le plus d'argent, et combien de plus ? (écris seulement le montant)",
            f"{a_name} has {_stack_txt(a, 'en')}. {b_name} has {_stack_txt(b, 'en')}. Who has more money, and how much more? (write only the amount)",
            d,
            [f'{a_name} : {_calc(a)}', f'{b_name} : {_calc(b)}', f'{rich} a plus : {N(max(ta, tb))} − {N(min(ta, tb))} = {N(d)}', f'{N(d)} $ de plus pour {rich}'],
            [f'{a_name}: {_calc(a)}', f'{b_name}: {_calc(b)}', f'{rich} has more: {N(max(ta, tb))} − {N(min(ta, tb))} = {N(d)}', f'${N(d)} more for {rich}'],
            'Calcule les deux sommes, compare, puis soustrais la plus petite de la plus grande.',
            'Work out both amounts, compare, then subtract the smaller from the larger.',
            'money', [f'{d} $', str(d)])
    if variant == 'change':
        item_fr, item_en = random.choice(_ITEMS)
        price = random.randint(max(5, ta // 3), max(6, ta - 1)) if ta > 6 else 5
        price = price // 5 * 5 or 5
        change = ta - price
        return _problem(
            f"{a_name} a {_stack_txt(a, 'fr')}. {_cap(sc.pronoun_fr(ga))} achète {item_fr} à **{N(price)} $**. Combien d'argent lui reste-t-il ?",
            f"{a_name} has {_stack_txt(a, 'en')}. {_cap(sc.pronoun_en(ga))} buys {item_en} for **${N(price)}**. How much money is left?",
            change,
            [f'{a_name} : {_calc(a)}', f'{N(ta)} − {N(price)} = {N(change)}', f'{N(change)} $'],
            [f'{a_name}: {_calc(a)}', f'{N(ta)} − {N(price)} = {N(change)}', f'${N(change)}'],
            "Calcule la somme, puis enlève le prix.", 'Work out the amount, then take away the price.',
            'money', [f'{change} $', str(change)])
    # save: weekly saving to reach an item
    item_fr, item_en = random.choice(_ITEMS)
    weekly = random.choice([5, 10, 15, 20, 25]) if grade <= 4 else random.choice([15, 20, 25, 30, 40, 45])
    weeks = random.randint(3, 12)
    price = ta + weekly * weeks
    return _problem(
        f"{a_name} a {_stack_txt(a, 'fr')} et économise **{weekly} $** par semaine pendant **{weeks} semaines** pour acheter {item_fr}. Combien d'argent aura-t-{sc.pronoun_fr(ga)} alors ?",
        f"{a_name} has {_stack_txt(a, 'en')} and saves **${weekly}** a week for **{weeks} weeks** to buy {item_en}. How much money will {sc.pronoun_en(ga)} have then?",
        price,
        [f'{a_name} : {_calc(a)}', f'Économies : {weekly} × {weeks} = {N(weekly * weeks)}', f'{N(ta)} + {N(weekly * weeks)} = {N(price)}', f'{N(price)} $'],
        [f'{a_name}: {_calc(a)}', f'Savings: {weekly} × {weeks} = {N(weekly * weeks)}', f'{N(ta)} + {N(weekly * weeks)} = {N(price)}', f'${N(price)}'],
        "Somme actuelle, plus les économies (montant × semaines).", 'Current amount, plus the savings (amount × weeks).',
        'money', [f'{price} $', str(price)])


# ─────────────────────────────────────────────────────────────────────────────
# Family 3 — schedule: chained activities, end time / total / waiting time
# ─────────────────────────────────────────────────────────────────────────────

def schedule(grade):
    who, g = sc.pick_actor()
    acts = random.sample(sc.ACTIVITIES, 3)
    start = random.randint(7, 15) * 60 + random.choice([0, 15, 30, 45] if grade <= 4 else range(0, 60, 5))
    step = [15, 30, 45, 60] if grade <= 4 else list(range(10, 125, 5))
    durs = [random.choice(step) for _ in range(3)]
    breaks = [random.choice([0, 10, 15, 20]) for _ in range(2)]
    variant = random.choice(['end2', 'end3', 'total', 'wait'])
    a1, a2, a3 = [x[0] for x in acts]
    e1, e2, e3 = [x[1].replace('the ', '') for x in acts]
    if variant == 'end2':
        end = start + durs[0] + breaks[0] + durs[1]
        pause = f", puis attend **{breaks[0]} min**" if breaks[0] else ''
        pause_en = f", then waits **{breaks[0]} min**" if breaks[0] else ''
        return _problem(
            f"À **{_clock(start)}**, {who} commence {a1} qui dure **{_dur(durs[0])}**{pause}. Ensuite {sc.pronoun_fr(g)} fait {a2} pendant **{_dur(durs[1])}**. À quelle heure {sc.pronoun_fr(g)} termine-t-{sc.pronoun_fr(g)} ?",
            f"At **{_clock(start)}**, {who} starts {e1}, which lasts **{_dur(durs[0])}**{pause_en}. Then {sc.pronoun_en(g)} does {e2} for **{_dur(durs[1])}**. At what time does {sc.pronoun_en(g)} finish?",
            end,
            [f'{_clock(start)} + {_dur(durs[0])} = {_clock(start + durs[0])}'] + ([f'+ {breaks[0]} min = {_clock(start + durs[0] + breaks[0])}'] if breaks[0] else []) + [f'+ {_dur(durs[1])} = {_clock(end)}', _clock(end)],
            [f'{_clock(start)} + {_dur(durs[0])} = {_clock(start + durs[0])}'] + ([f'+ {breaks[0]} min = {_clock(start + durs[0] + breaks[0])}'] if breaks[0] else []) + [f'+ {_dur(durs[1])} = {_clock(end)}', _clock(end)],
            "Avance l'heure étape par étape : chaque activité, chaque pause.", 'Move the clock forward step by step: each activity, each break.',
            'duration', [_clock(end), f'{end // 60}:{end % 60:02d}'])
    if variant == 'end3':
        total = sum(durs) + sum(breaks)
        end = start + total
        return _problem(
            f"{who} enchaîne trois activités à partir de **{_clock(start)}** : {a1} (**{_dur(durs[0])}**), {a2} (**{_dur(durs[1])}**) et {a3} (**{_dur(durs[2])}**), avec une pause de **{breaks[0]} min** puis une autre de **{breaks[1]} min** entre elles. À quelle heure tout est-il fini ?",
            f"{who} does three activities in a row starting at **{_clock(start)}**: {e1} (**{_dur(durs[0])}**), {e2} (**{_dur(durs[1])}**) and {e3} (**{_dur(durs[2])}**), with a **{breaks[0]} min** break and then a **{breaks[1]} min** break between them. At what time is everything over?",
            end,
            [f'Durée totale : {durs[0]} + {breaks[0]} + {durs[1]} + {breaks[1]} + {durs[2]} = {total} min = {_dur(total)}', f'{_clock(start)} + {_dur(total)} = {_clock(end)}', _clock(end)],
            [f'Total time: {durs[0]} + {breaks[0]} + {durs[1]} + {breaks[1]} + {durs[2]} = {total} min = {_dur(total)}', f'{_clock(start)} + {_dur(total)} = {_clock(end)}', _clock(end)],
            'Additionne toutes les durées en minutes, convertis en h et min, puis ajoute au départ.',
            'Add all the durations in minutes, convert to h and min, then add to the start.',
            'duration', [_clock(end), f'{end // 60}:{end % 60:02d}'])
    if variant == 'total':
        total = sum(durs)
        return _problem(
            f"Aujourd'hui, {who} a fait {a1} pendant **{_dur(durs[0])}**, {a2} pendant **{_dur(durs[1])}** et {a3} pendant **{_dur(durs[2])}**. Combien de temps cela fait-il en tout ? (réponds en h et min)",
            f"Today {who} did {e1} for **{_dur(durs[0])}**, {e2} for **{_dur(durs[1])}** and {e3} for **{_dur(durs[2])}**. How long is that altogether? (answer in h and min)",
            total,
            [f'{durs[0]} + {durs[1]} + {durs[2]} = {total} min', f'{total} min = {_dur(total)}', _dur(total)],
            [f'{durs[0]} + {durs[1]} + {durs[2]} = {total} min', f'{total} min = {_dur(total)}', _dur(total)],
            'Additionne en minutes, puis convertis (60 min = 1 h).', 'Add in minutes, then convert (60 min = 1 h).',
            'duration', [_dur(total), f'{total} min'])
    # wait: activity ends, event later → waiting time
    end = start + durs[0]
    event = end + random.choice([25, 35, 40, 50, 70, 85, 95, 110])
    wait = event - end
    return _problem(
        f"{a1.capitalize()} de {who} commence à **{_clock(start)}** et dure **{_dur(durs[0])}**. {a2.capitalize()} commence à **{_clock(event)}**. Combien de temps {sc.pronoun_fr(g)} doit-{sc.pronoun_fr(g)} attendre entre les deux ?",
        f"{who}'s {e1} starts at **{_clock(start)}** and lasts **{_dur(durs[0])}**. {e2.capitalize()} starts at **{_clock(event)}**. How long does {sc.pronoun_en(g)} wait between the two?",
        wait,
        [f'Fin : {_clock(start)} + {_dur(durs[0])} = {_clock(end)}', f'De {_clock(end)} à {_clock(event)} : {wait} min', _dur(wait)],
        [f'End: {_clock(start)} + {_dur(durs[0])} = {_clock(end)}', f'From {_clock(end)} to {_clock(event)}: {wait} min', _dur(wait)],
        "Trouve d'abord l'heure de fin, puis la durée jusqu'au prochain événement.", 'Find the end time first, then the time until the next event.',
        'duration', [_dur(wait), f'{wait} min'])


# ─────────────────────────────────────────────────────────────────────────────
# Family 4 — measurements with relations: longest / shortest / order
# ─────────────────────────────────────────────────────────────────────────────

def measurements(grade):
    things_fr, things_en, unit, lo, hi = sc.pick_measured()
    if grade >= 5:
        lo, hi = lo * 10, hi * 10
    elif grade == 3:
        lo, hi = max(1, lo // 10), max(20, hi // 10)
    names = random.sample([n for n, _ in sc.ACTORS], 3)
    base = random.randint(lo, hi)
    d1 = random.randint(1, max(2, base // 3))
    k = random.choice([2, 3])
    vals = {names[0]: base, names[1]: base + d1, names[2]: (base + d1) * k if grade == 6 else base - d1 if base > d1 else base + 2 * d1}
    thing_fr = things_fr.split(' ')[0]
    if grade >= 5:
        rel3_fr = f"{names[2]} en a une **{k} fois** plus longue que celle {sc.de(names[1])}"
        rel3_en = f"{names[2]}'s is **{k} times** as long as {names[1]}'s"
        st3 = f'{N(vals[names[1]])} × {k} = {N(vals[names[2]])}'
    else:
        rel3_fr = f"celle de {names[2]} mesure **{N(abs(vals[names[2]] - base))} {unit}** de {'moins' if vals[names[2]] < base else 'plus'} que celle {sc.de(names[0])}"
        rel3_en = f"{names[2]}'s is **{N(abs(vals[names[2]] - base))} {unit}** {'shorter' if vals[names[2]] < base else 'longer'} than {names[0]}'s"
        st3 = f'{N(base)} {"−" if vals[names[2]] < base else "+"} {N(abs(vals[names[2]] - base))} = {N(vals[names[2]])}'
    story_fr = (f"Trois amis comparent leurs {things_fr}. Celle {sc.de(names[0])} mesure **{N(base)} {unit}**, "
                f"celle {sc.de(names[1])} mesure **{N(d1)} {unit}** de plus, et {rel3_fr}.")
    story_en = (f"Three friends compare their {things_en}. {names[0]}'s measures **{N(base)} {unit}**, "
                f"{names[1]}'s is **{N(d1)} {unit}** more, and {rel3_en}.")
    variant = random.choice(['longest', 'sum', 'gap'])
    steps_fr = [f'{names[1]} : {N(base)} + {N(d1)} = {N(vals[names[1]])}', f'{names[2]} : {st3}']
    steps_en = [f'{names[1]}: {N(base)} + {N(d1)} = {N(vals[names[1]])}', f'{names[2]}: {st3}']
    if variant == 'longest':
        big = max(vals.values())
        return _problem(f"{story_fr} Quelle est la mesure de la plus longue ? (en {unit})", f"{story_en} What is the measure of the longest one? (in {unit})", big,
                        steps_fr + [f'La plus longue : {N(big)} {unit}'], steps_en + [f'Longest: {N(big)} {unit}'],
                        'Calcule chaque mesure, puis compare.', 'Work out each measure, then compare.')
    if variant == 'sum':
        tot = sum(vals.values())
        return _problem(f"{story_fr} Quelle est la longueur totale des trois ? (en {unit})", f"{story_en} What is the total length of all three? (in {unit})", tot,
                        steps_fr + [' + '.join(N(v) for v in vals.values()) + f' = {N(tot)}', f'{N(tot)} {unit}'],
                        steps_en + [' + '.join(N(v) for v in vals.values()) + f' = {N(tot)}', f'{N(tot)} {unit}'],
                        'Calcule chaque mesure, puis additionne les trois.', 'Work out each measure, then add all three.')
    gap = max(vals.values()) - min(vals.values())
    return _problem(f"{story_fr} Quel écart y a-t-il entre la plus longue et la plus courte ? (en {unit})", f"{story_en} What is the gap between the longest and the shortest? (in {unit})", gap,
                    steps_fr + [f'{N(max(vals.values()))} − {N(min(vals.values()))} = {N(gap)}', f'{N(gap)} {unit}'],
                    steps_en + [f'{N(max(vals.values()))} − {N(min(vals.values()))} = {N(gap)}', f'{N(gap)} {unit}'],
                    'Calcule chaque mesure, trouve la plus grande et la plus petite, puis soustrais.',
                    'Work out each measure, find the largest and smallest, then subtract.')


# ─────────────────────────────────────────────────────────────────────────────
# Family 5 — savings / patterns: constant step over time
# ─────────────────────────────────────────────────────────────────────────────

def pattern(grade):
    who, g = sc.pick_actor()
    key, thing = sc.pick_thing('object')
    start = random.randint(10, 90) if grade <= 4 else random.randint(120, 900)
    step = random.choice([2, 3, 4, 5, 10, 25]) if grade <= 4 else random.choice([12, 15, 25, 35, 50, 75, 125])
    n = random.randint(4, 9)
    variant = random.choice(['after', 'weeks', 'gift'])
    total = start + step * n
    if variant == 'after':
        return _problem(
            f"{who} a **{start}** {sc.noun(thing, start, 'fr')} et en reçoit **{step}** de plus chaque semaine. Combien en aura-t-{sc.pronoun_fr(g)} après **{n} semaines** ?",
            f"{who} has **{start}** {sc.noun(thing, start, 'en')} and gets **{step}** more each week. How many will {sc.pronoun_en(g)} have after **{n} weeks**?",
            total, [f'{step} × {n} = {step * n}', f'{start} + {step * n} = {total}', f'{total} {sc.noun(thing, total, "fr")}'],
            [f'{step} × {n} = {step * n}', f'{start} + {step * n} = {total}', f'{total} {sc.noun(thing, total, "en")}'],
            'Ajout par semaine × nombre de semaines, puis ajoute au départ.', 'Amount per week × number of weeks, then add to the start.')
    if variant == 'weeks':
        target = start + step * n
        return _problem(
            f"{who} a **{start}** {sc.noun(thing, start, 'fr')} et en reçoit **{step}** de plus chaque semaine. Dans combien de semaines en aura-t-{sc.pronoun_fr(g)} **{target}** ?",
            f"{who} has **{start}** {sc.noun(thing, start, 'en')} and gets **{step}** more each week. In how many weeks will {sc.pronoun_en(g)} have **{target}**?",
            n, [f'{target} − {start} = {target - start}', f'{target - start} ÷ {step} = {n}', f'{n} semaines'],
            [f'{target} − {start} = {target - start}', f'{target - start} ÷ {step} = {n}', f'{n} weeks'],
            "Trouve combien il en manque, puis divise par l'ajout hebdomadaire.", 'Find how many are missing, then divide by the weekly amount.')
    give = random.randint(1, min(step * n // 2, 30))
    return _problem(
        f"{who} a **{start}** {sc.noun(thing, start, 'fr')}, en reçoit **{step}** chaque semaine pendant **{n} semaines**, puis en donne **{give}** à un ami. Combien lui en reste-t-il ?",
        f"{who} has **{start}** {sc.noun(thing, start, 'en')}, gets **{step}** each week for **{n} weeks**, then gives **{give}** to a friend. How many are left?",
        total - give, [f'{step} × {n} = {step * n}', f'{start} + {step * n} = {total}', f'{total} − {give} = {total - give}', f'{total - give} {sc.noun(thing, total - give, "fr")}'],
        [f'{step} × {n} = {step * n}', f'{start} + {step * n} = {total}', f'{total} − {give} = {total - give}', f'{total - give} {sc.noun(thing, total - give, "en")}'],
        'Trois étapes : multiplication, addition, soustraction.', 'Three steps: multiply, add, subtract.')


# ─────────────────────────────────────────────────────────────────────────────
# Family 6 — production rates (grade 6): rate × period, two producers, leftovers
# ─────────────────────────────────────────────────────────────────────────────

def production(grade):
    subj_fr, subj_en, v_fr, v_en, th_fr, th_en, pkey, lo, hi = random.choice([r for r in sc.RATES if r[6] in ('day', 'hour')])
    rate = random.randint(lo, hi)
    n, per_fr, per_en, count = random.choice(sc.PERIODS[pkey])
    unit_fr = 'par jour' if pkey == 'day' else 'par heure'
    unit_en = 'per day' if pkey == 'day' else 'per hour'
    total = rate * count
    story_fr = f"{subj_fr} {v_fr} **{N(rate)} {th_fr}** {unit_fr}."
    story_en = f"{subj_en} {v_en} **{N(rate)} {th_en}** {unit_en}."
    variant = random.choice(['exact', 'two', 'leftover', 'estimate'])
    if variant == 'exact':
        return _problem(f"{story_fr} Combien de {th_fr} en **{per_fr}** ?", f"{story_en} How many {th_en} in **{per_en}**?", total,
                        [f'{per_fr} = {count} {"jours" if pkey == "day" else "heures"}', f'{N(rate)} × {count} = {N(total)}', f'{N(total)} {th_fr}'],
                        [f'{per_en} = {count} {"days" if pkey == "day" else "hours"}', f'{N(rate)} × {count} = {N(total)}', f'{N(total)} {th_en}'],
                        "Convertis la période, estime, puis multiplie exactement.", 'Convert the period, estimate, then multiply exactly.')
    if variant == 'two':
        rate2 = max(lo, rate + random.choice([-1, 1]) * random.randint(lo // 10 + 1, lo // 2 + 1))
        t2 = rate2 * count
        big = 'premier' if total > t2 else 'second'
        big_en = 'first' if total > t2 else 'second'
        return _problem(
            f"{story_fr} Un second {subj_fr.split(' ', 1)[1]} {v_fr} **{N(rate2)} {th_fr}** {unit_fr}. Quelle différence y a-t-il entre les deux en **{per_fr}** ?",
            f"{story_en} A second {subj_en.split(' ', 1)[1]} {v_en} **{N(rate2)} {th_en}** {unit_en}. What is the difference between the two in **{per_en}**?",
            abs(total - t2),
            [f'Premier : {N(rate)} × {count} = {N(total)}', f'Second : {N(rate2)} × {count} = {N(t2)}', f'{N(max(total, t2))} − {N(min(total, t2))} = {N(abs(total - t2))}', f'{N(abs(total - t2))} {th_fr} (le {big} en fait plus)'],
            [f'First: {N(rate)} × {count} = {N(total)}', f'Second: {N(rate2)} × {count} = {N(t2)}', f'{N(max(total, t2))} − {N(min(total, t2))} = {N(abs(total - t2))}', f'{N(abs(total - t2))} {th_en} (the {big_en} makes more)'],
            'Calcule chaque total, puis soustrais.', 'Work out each total, then subtract.')
    if variant == 'leftover':
        used = random.randint(total // 5, total // 2)
        return _problem(
            f"{story_fr} En **{per_fr}**, on en utilise **{N(used)}**. Combien en reste-t-il ?",
            f"{story_en} In **{per_en}**, **{N(used)}** of them are used. How many are left?",
            total - used,
            [f'{N(rate)} × {count} = {N(total)}', f'{N(total)} − {N(used)} = {N(total - used)}', f'{N(total - used)} {th_fr}'],
            [f'{N(rate)} × {count} = {N(total)}', f'{N(total)} − {N(used)} = {N(total - used)}', f'{N(total - used)} {th_en}'],
            'Total produit, moins ce qui est utilisé.', 'Total produced, minus what is used.')
    # estimate: round both
    p = 10 ** (len(str(rate)) - 1)
    ra = round(rate / p) * p
    rc = round(count / 10) * 10 or count
    est = ra * rc
    return _problem(
        f"{story_fr} **Sans calculer exactement**, environ combien de {th_fr} en **{per_fr}** ? Arrondis {N(rate)} et {count} à leur premier chiffre.",
        f"{story_en} **Without calculating exactly**, about how many {th_en} in **{per_en}**? Round {N(rate)} and {count} to their leading digit.",
        est,
        [f'{N(rate)} ≈ {N(ra)} et {count} ≈ {rc}', f'{N(ra)} × {rc} = {N(est)}', f'environ {N(est)} {th_fr} (exact : {N(total)})'],
        [f'{N(rate)} ≈ {N(ra)} and {count} ≈ {rc}', f'{N(ra)} × {rc} = {N(est)}', f'about {N(est)} {th_en} (exact: {N(total)})'],
        'Arrondis chaque nombre, puis multiplie les chiffres de tête et ajoute les zéros.', 'Round each number, multiply the leading digits and add the zeros.')


# ─────────────────────────────────────────────────────────────────────────────
# Family 7 — comparison chains with a useless fact (grade 6)
# ─────────────────────────────────────────────────────────────────────────────

def chain(grade):
    c = random.choice(sc.COMPARATIVES)
    (a_fr, a_en), (b_fr, b_en), (c_fr, c_en) = random.sample(c['subjects'], 3)
    base = random.randint(c['lo'], c['hi'] // 2)
    d = random.randint(1, 9) * 10 ** (len(str(base)) - 2)
    k = random.choice([2, 3])
    vb = base + d
    vc = vb * k
    dist_fr, dist_en, dlo, dhi = random.choice(sc.DISTRACTOR_FACTS)
    dn = N(random.randint(dlo, dhi))
    facts_fr = [c['fact_fr'].format(S=_cap(a_fr), n=N(base)), c['more_fr'].format(S=_cap(b_fr), T=a_fr, n=N(d)),
                c['times_fr'].format(S=_cap(c_fr), T=b_fr, n=k), dist_fr.format(n=dn)]
    facts_en = [c['fact_en'].format(S=_cap(a_en), n=N(base)), c['more_en'].format(S=_cap(b_en), T=a_en, n=N(d)),
                c['times_en'].format(S=_cap(c_en), T=b_en, n=k), dist_en.format(n=dn)]
    order = list(range(4)); random.shuffle(order)
    story_fr = ' '.join(facts_fr[i] for i in order)
    story_en = ' '.join(facts_en[i] for i in order)
    variant = random.choice(['third', 'total', 'gap'])
    steps_fr = [f'{_cap(b_fr)} : {N(base)} + {N(d)} = {N(vb)}', f'{_cap(c_fr)} : {N(vb)} × {k} = {N(vc)}']
    steps_en = [f'{_cap(b_en)}: {N(base)} + {N(d)} = {N(vb)}', f'{_cap(c_en)}: {N(vb)} × {k} = {N(vc)}']
    if variant == 'third':
        return _problem(f"{story_fr} **{_cap(c['q_fr'].format(S=c_fr))}**", f"{story_en} **{c['q_en'].format(S=c_en)}**", vc,
                        steps_fr + [f'{N(vc)} {c["unit"]}'], steps_en + [f'{N(vc)} {c["unit"]}'],
                        "Barre l'information inutile, puis avance d'une comparaison à l'autre.", 'Cross out the useless fact, then work through one comparison after the other.')
    if variant == 'total':
        tot = base + vb + vc
        return _problem(f"{story_fr} **Quel est le total pour {a_fr}, {b_fr} et {c_fr} ?**", f"{story_en} **What is the total for {a_en}, {b_en} and {c_en}?**", tot,
                        steps_fr + [f'{N(base)} + {N(vb)} + {N(vc)} = {N(tot)}', f'{N(tot)} {c["unit"]}'], steps_en + [f'{N(base)} + {N(vb)} + {N(vc)} = {N(tot)}', f'{N(tot)} {c["unit"]}'],
                        'Trouve chaque valeur, puis additionne les trois.', 'Find each value, then add all three.')
    return _problem(f"{story_fr} **Quelle est la différence entre {c_fr} et {a_fr} ?**", f"{story_en} **What is the difference between {c_en} and {a_en}?**", vc - base,
                    steps_fr + [f'{N(vc)} − {N(base)} = {N(vc - base)}', f'{N(vc - base)} {c["unit"]}'], steps_en + [f'{N(vc)} − {N(base)} = {N(vc - base)}', f'{N(vc - base)} {c["unit"]}'],
                    'Trouve les deux valeurs demandées, puis soustrais.', 'Find the two values asked for, then subtract.')


# ─────────────────────────────────────────────────────────────────────────────
# Family 8 — fractions of a distance (grade 6)
# ─────────────────────────────────────────────────────────────────────────────

_NTH_FR = {3: 'tiers', 4: 'quarts', 5: 'cinquièmes', 6: 'sixièmes', 8: 'huitièmes'}
_NTH_EN = {3: 'thirds', 4: 'quarters', 5: 'fifths', 6: 'sixths', 8: 'eighths'}


def fraction_distance(grade):
    who, g = sc.pick_actor()
    d = random.choice([3, 4, 5, 6, 8])
    nth_fr, nth_en = _NTH_FR[d], _NTH_EN[d]
    total_km = random.randint(3, 6)
    num = random.randint(d + 1, total_km * d - 1)
    lo = num // d
    variant = random.choice(['marker', 'remaining', 'segments'])
    if variant == 'marker':
        return _problem(
            f"Un sentier de **{total_km} km** a une borne à chaque kilomètre. {who} a déjà parcouru **{num}/{d} km**. Entre quelles bornes se trouve-t-{sc.pronoun_fr(g)} ? Écris le numéro de la borne qu'{sc.pronoun_fr(g)} vient de dépasser.",
            f"A **{total_km} km** trail has a marker every kilometre. {who} has already walked **{num}/{d} km**. Between which markers is {sc.pronoun_en(g)}? Write the number of the marker just passed.",
            lo, [f'{num} ÷ {d} = {lo} reste {num - lo * d}', f'{num}/{d} = {lo} + {num - lo * d}/{d}, entre les bornes {lo} et {lo + 1}', f'borne {lo}'],
            [f'{num} ÷ {d} = {lo} remainder {num - lo * d}', f'{num}/{d} = {lo} + {num - lo * d}/{d}, between markers {lo} and {lo + 1}', f'marker {lo}'],
            'Combien de fois le dénominateur entre dans le numérateur ?', 'How many times does the denominator go into the numerator?')
    if variant == 'remaining':
        rem = total_km * d - num
        return _problem(
            f"Un sentier mesure **{total_km} km**. {who} a parcouru **{num}/{d} km**. Combien de **{nth_fr} de km** lui reste-t-il à parcourir ?",
            f"A trail is **{total_km} km** long. {who} has walked **{num}/{d} km**. How many **{nth_en} of a km** are left to walk?",
            rem, [f'{total_km} km = {total_km} × {d} = {total_km * d} {nth_fr}', f'{total_km * d} − {num} = {rem}', f'{rem} {nth_fr} de km ({rem}/{d} km)'],
            [f'{total_km} km = {total_km} × {d} = {total_km * d} {nth_en}', f'{total_km * d} − {num} = {rem}', f'{rem} {nth_en} of a km ({rem}/{d} km)'],
            f'Exprime la longueur totale en {nth_fr}, puis soustrais.', f'Write the whole length in {nth_en}, then subtract.')
    nxt = lo + 1
    to_next = nxt * d - num
    return _problem(
        f"Sur une piste graduée en **{nth_fr} de km**, {who} est à **{num}/{d} km**. Combien de graduations lui reste-t-il avant la borne du **{nxt}e km** ?",
        f"On a track marked in **{nth_en} of a km**, {who} is at **{num}/{d} km**. How many marks are left before the **{nxt} km** marker?",
        to_next, [f'{nxt} km = {nxt} × {d} = {nxt * d} {nth_fr}', f'{nxt * d} − {num} = {to_next}', f'{to_next} graduations'],
        [f'{nxt} km = {nxt} × {d} = {nxt * d} {nth_en}', f'{nxt * d} − {num} = {to_next}', f'{to_next} marks'],
        'Convertis la borne en graduations, puis soustrais la position.', 'Convert the marker into marks, then subtract the position.')


# ─────────────────────────────────────────────────────────────────────────────
# registry
# ─────────────────────────────────────────────────────────────────────────────

RESOLUTION_FAMILIES = {
    # grade 4
    'g4-grouping-problem':  (4, [inventory]),
    'g4-count-groups':      (4, [inventory]),
    'g4-before-after':      (4, [pattern, measurements]),
    'g4-compare':           (4, [money, measurements]),
    'g4-order-numbers':     (4, [measurements]),
    'g4-skip-sequence':     (4, [pattern]),
    'g4-time-units':        (4, [schedule]),
    'g4-elapsed-time':      (4, [schedule]),
    'g4-end-time':          (4, [schedule]),
    'g4-clock-24h':         (4, [schedule]),
    # grade 6
    'g6-place-value-change': (6, [inventory]),
    'g6-count-groups':       (6, [inventory]),
    'g6-compare':            (6, [money, measurements]),
    'g6-order':              (6, [measurements]),
    'g6-extreme':            (6, [measurements, chain]),
    'g6-money-compare':      (6, [money]),
    'g6-multiply':           (6, [production, pattern]),
    'g6-estimate-product':   (6, [production]),
    'g6-rate-problem':       (6, [production]),
    'g6-fraction-between':   (6, [fraction_distance]),
    'g6-fraction-order':     (6, [fraction_distance]),
    'g6-comparative-phrase': (6, [chain]),
    'g6-relevant-info':      (6, [chain]),
}


def resolution_gen(slug):
    """Return gen(level) for the 4th level of ``slug`` (None if the skill has no resolution stage)."""
    entry = RESOLUTION_FAMILIES.get(slug)
    if not entry:
        return None
    grade, families = entry

    def gen(level='resolution'):
        return random.choice(families)(grade)
    gen.__name__ = f'{slug}_resolution'
    return gen


from .resolution_g35 import FAMILIES_G35  # noqa: E402  (grade 3 / 5 families reuse the helpers above)
RESOLUTION_FAMILIES.update(FAMILIES_G35)

RESOLUTION = {slug: resolution_gen(slug) for slug in RESOLUTION_FAMILIES}
