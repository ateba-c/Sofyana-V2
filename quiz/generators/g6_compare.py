"""
g6_compare.py — Grade-6 comparing & ordering (content_g6.md §3).

Topics:
  g6_compare_gen        typed (symbol)  – 45 671 ⬜ 45 176, 456 131 ⬜ 45 376
  g6_order_gen          ordering        – 5 numbers (5–6 digits) with a scenario, croissant/décroissant
  g6_extreme_gen        QCM             – the largest / smallest of five numbers
  g6_money_compare_gen  typed           – stacks of $100/$50/$20/$5 bills: total (easy) or compare (medium/hard)
"""
import random
from .base import _tagged_shuffle_mc
from . import scenarios as sc


def _num(level):
    return {'easy': random.randint(1_000, 99_999),
            'medium': random.randint(10_000, 999_999),
            'hard': random.randint(100_000, 999_999)}[level]


def _pair(level):
    a = _num(level)
    r = random.random()
    if r < 0.12:
        return a, a
    s = str(a)
    if level == 'easy':
        b = a + random.choice([-1, 1]) * random.randint(1, 900)
    elif level == 'medium':
        if random.random() < 0.5:                      # same digits, different length
            b = int(s[:-1]) if random.random() < 0.5 else int(s + str(random.randint(0, 9)))
        else:                                           # scrambled tail
            d = list(s); i, j = random.sample(range(2, len(d)), 2); d[i], d[j] = d[j], d[i]
            b = int(''.join(d))
    else:
        d = list(s); i, j = random.sample(range(1, len(d)), 2); d[i], d[j] = d[j], d[i]
        b = int(''.join(d)) if d[0] != '0' else a + 1
    if b == a:
        b = a + 1
    return a, max(1, b)


def g6_compare_gen(level='easy'):
    a, b = _pair(level)
    sym = '<' if a < b else '>' if a > b else '='
    return {
        'q_type': 'text_input', 'answer_type': 'symbol',
        'prompt_fr': f"Compare : **{sc.fmt_n(a)}** ⬜ **{sc.fmt_n(b)}**. Écris <, > ou =.",
        'prompt_en': f"Compare: **{sc.fmt_n(a)}** ⬜ **{sc.fmt_n(b)}**. Type <, > or =.",
        'hint_fr': "Un nombre avec plus de chiffres est plus grand. À nombre de chiffres égal, compare position par position depuis la gauche.",
        'hint_en': 'A number with more digits is bigger. With the same number of digits, compare position by position from the left.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': f'{sc.fmt_n(a)} has {len(str(a))} digits, {sc.fmt_n(b)} has {len(str(b))}. → {sc.fmt_n(a)} {sym} {sc.fmt_n(b)}',
        'explanation_fr': f'{sc.fmt_n(a)} a {len(str(a))} chiffres, {sc.fmt_n(b)} en a {len(str(b))}. → {sc.fmt_n(a)} {sym} {sc.fmt_n(b)}',
        'correct_answers': [sym],
    }


def _sample_numbers(level, count):
    things_fr, things_en, unit_fr, unit_en, lo, hi, verb_fr, verb_en = random.choice(sc.LARGE_QUANTITIES)
    if level == 'easy':
        nums = random.sample(range(lo, hi + 1), count)
    else:
        # cluster: some share leading digits (99 001 vs 98 890), some differ in length
        base = random.randint(lo, hi)
        nums = {base}
        while len(nums) < count:
            r = random.random()
            if r < 0.4:
                nums.add(max(1, base + random.randint(-2_000, 2_000)))
            elif r < 0.7:
                nums.add(max(1, base // 10 + random.randint(0, 99)))
            else:
                nums.add(random.randint(lo, hi))
        nums = list(nums)
    return sorted(set(nums)), things_fr, things_en, unit_fr, unit_en, verb_fr, verb_en


def _lab(n, unit):
    return f'{sc.fmt_n(n)} {unit}' if unit != '$' else f'{sc.fmt_n(n)} $'


def g6_order_gen(level='easy'):
    count = 4 if level == 'easy' else 5
    nums, things_fr, things_en, unit_fr, unit_en, verb_fr, verb_en = _sample_numbers(level, count)
    desc = level != 'easy' and random.random() < 0.5
    ordered = nums[::-1] if desc else nums
    who, _ = sc.pick_actor()
    items = [{'label': _lab(n, unit_fr), 'order': i + 1} for i, n in enumerate(ordered)]
    o_fr = 'décroissant' if desc else 'croissant'
    o_en = 'descending' if desc else 'ascending'
    sep = ' > ' if desc else ' < '
    return {
        'q_type': 'ordering',
        'prompt_fr': f"{who} {verb_fr} {len(nums)} {things_fr}. Range les nombres en ordre **{o_fr}**.",
        'prompt_en': f"{who} {verb_en} {len(nums)} {things_en}. Sort the numbers in **{o_en}** order.",
        'hint_fr': "Compare d'abord le nombre de chiffres, puis les chiffres de gauche à droite.",
        'hint_en': 'Compare the number of digits first, then the digits from left to right.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'items': items, 'correct_answers': [i['label'] for i in items],
        'time_limit': 45, 'points': 1,
        'explanation_en': f'{o_en.capitalize()}: ' + sep.join(sc.fmt_n(n) for n in ordered),
        'explanation_fr': f'Ordre {o_fr} : ' + sep.join(sc.fmt_n(n) for n in ordered),
    }


def g6_extreme_gen(level='easy'):
    nums, things_fr, things_en, unit_fr, unit_en, verb_fr, verb_en = _sample_numbers(level, 5)
    biggest = random.random() < 0.5
    target = max(nums) if biggest else min(nums)
    tagged = [(_lab(n, unit_fr), 'not_extreme', 'Compare digit counts, then leading digits.',
               'Compare le nombre de chiffres, puis les premiers chiffres.') for n in nums if n != target]
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f"Voici {len(nums)} {things_fr} : {', '.join(_lab(n, unit_fr) for n in random.sample(nums, len(nums)))}. Lequel est le **{'plus grand' if biggest else 'plus petit'}** nombre ?",
        'prompt_en': f"Here are {len(nums)} {things_en}: {', '.join(_lab(n, unit_fr) for n in random.sample(nums, len(nums)))}. Which is the **{'largest' if biggest else 'smallest'}** number?",
        'hint_fr': 'Le nombre avec le plus de chiffres est le plus grand ; sinon compare les chiffres de gauche.',
        'hint_en': 'The number with the most digits is the largest; otherwise compare the leftmost digits.',
        'show_illustration': False, 'shape_data': [],
        'choices': _tagged_shuffle_mc(_lab(target, unit_fr), tagged), 'pairs': [],
        'explanation_en': f'Sorted: {" < ".join(sc.fmt_n(n) for n in sorted(nums))} → {"largest" if biggest else "smallest"} = {sc.fmt_n(target)}',
        'explanation_fr': f'Rangés : {" < ".join(sc.fmt_n(n) for n in sorted(nums))} → le {"plus grand" if biggest else "plus petit"} = {sc.fmt_n(target)}',
        'correct_answers': [_lab(target, unit_fr)],
    }


_BILLS = [100, 50, 20, 5]


def _stack(level):
    hi = {'easy': 4, 'medium': 7, 'hard': 12}[level]
    counts = {b: random.randint(0, hi) for b in _BILLS}
    if sum(counts.values()) == 0:
        counts[20] = 1
    return counts


def _stack_fr(c):
    parts = [f"{n} billet{'s' if n > 1 else ''} de {b} $" for b, n in c.items() if n]
    return ', '.join(parts[:-1]) + (' et ' if len(parts) > 1 else '') + parts[-1]


def _stack_en(c):
    parts = [f"{n} ${b} bill{'s' if n > 1 else ''}" for b, n in c.items() if n]
    return ', '.join(parts[:-1]) + (' and ' if len(parts) > 1 else '') + parts[-1]


def _total(c):
    return sum(b * n for b, n in c.items())


def _calc(c):
    return ' + '.join(f'{n} × {b}' for b, n in c.items() if n) + f' = {sc.fmt_n(_total(c))} $'


def g6_money_compare_gen(level='easy'):
    a = _stack(level)
    who_a, _ = sc.pick_actor()
    if level == 'easy':
        return {
            'q_type': 'text_input', 'answer_type': 'money',
            'prompt_fr': f"{who_a} a {_stack_fr(a)}. Quelle somme d'argent cela fait-il ?",
            'prompt_en': f"{who_a} has {_stack_en(a)}. How much money is that?",
            'hint_fr': 'Multiplie chaque sorte de billet par son nombre, puis additionne.',
            'hint_en': 'Multiply each kind of bill by how many there are, then add.',
            'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
            'explanation_en': _calc(a), 'explanation_fr': _calc(a),
            'correct_answers': [f'{_total(a)} $', str(_total(a))],
        }
    b = _stack(level)
    while _total(b) == _total(a) and random.random() < 0.8:
        b = _stack(level)
    who_b, _ = sc.pick_actor()
    while who_b == who_a:
        who_b, _ = sc.pick_actor()
    ta, tb = _total(a), _total(b)
    sym = '<' if ta < tb else '>' if ta > tb else '='
    return {
        'q_type': 'text_input', 'answer_type': 'symbol',
        'prompt_fr': f"{who_a} a {_stack_fr(a)}. {who_b} a {_stack_fr(b)}. Compare les deux sommes : **argent {sc.de(who_a)}** ⬜ **argent {sc.de(who_b)}**. Écris <, > ou =.",
        'prompt_en': f"{who_a} has {_stack_en(a)}. {who_b} has {_stack_en(b)}. Compare the two amounts: **{who_a}'s money** ⬜ **{who_b}'s money**. Type <, > or =.",
        'hint_fr': "Calcule d'abord chaque somme (nombre de billets × valeur), puis compare les totaux.",
        'hint_en': 'Work out each total first (number of bills × value), then compare.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': f'{who_a}: {_calc(a)}\n{who_b}: {_calc(b)}\n{sc.fmt_n(ta)} {sym} {sc.fmt_n(tb)}',
        'explanation_fr': f'{who_a} : {_calc(a)}\n{who_b} : {_calc(b)}\n{sc.fmt_n(ta)} {sym} {sc.fmt_n(tb)}',
        'correct_answers': [sym],
    }
