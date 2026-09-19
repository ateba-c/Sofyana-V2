"""
g6_numeration.py — Grade-6 place value & decomposition (content_g6.md §1–2).

Topics:
  g6_digit_position_gen     QCM             – position of a digit in a 6-digit number (u, d, c, UM, DM, CM)
  g6_digit_value_gen        typed (integer) – value of a digit
  g6_count_groups_gen       typed (integer) – "combien d'unités de mille / de centaines dans 872 435 ?"
  g6_place_value_change_gen typed (integer) – start from 16 142, add 6 CM and 3 c → 616 442
  g6_additive_form_gen      QCM / typed     – 300 000 + 50 000 + 1 000 + 600 + 40 + 5 ↔ 351 645
  g6_symbol_form_gen        typed (integer) – 5 DM + 15 UM + 9 c + 10 d + 4 u = 66 004 (regrouping)
  g6_multiplicative_form_gen QCM            – (8 × 100 000) + (4 × 10 000) + … ↔ 849 078

Difficulty:
  easy   → 5-digit numbers, no regrouping
  medium → 6-digit numbers
  hard   → 6-digit with zeros, regrouping (15 UM), several changes at once
"""
import random
from .base import _tagged_shuffle_mc
from . import scenarios as sc
from .g4_numeration import _mult_expansion, _wrong_expansions

_POS_FR = ['unités', 'dizaines', 'centaines', 'unités de mille', 'dizaines de mille', 'centaines de mille']
_POS_EN = ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'hundred thousands']
_POS_SYM = ['u', 'd', 'c', 'UM', 'DM', 'CM']
_POS_FR_SING = ['unité', 'dizaine', 'centaine', 'unité de mille', 'dizaine de mille', 'centaine de mille']
_POS_EN_SING = ['one', 'ten', 'hundred', 'thousand', 'ten thousand', 'hundred thousand']


def _pick_number(level, unique_digits=False):
    while True:
        if level == 'easy':
            n = random.randint(10_000, 99_999)
        elif level == 'medium':
            n = random.randint(100_000, 999_999)
        else:
            digits = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(5)]
            digits[random.randint(1, 4)] = 0
            n = int(''.join(map(str, digits)))
        s = str(n)
        if not unique_digits or len(set(s)) == len(s):
            return n


def _pos_of(n):
    """Random (index, digit) with digit ≠ 0 and unique in n."""
    s = str(n)[::-1]
    cands = [i for i, d in enumerate(s) if d != '0' and s.count(d) == 1]
    i = random.choice(cands) if cands else random.choice([i for i, d in enumerate(s) if d != '0'])
    return i, int(s[i])


# ─────────────────────────────────────────────────────────────────────────────

def g6_digit_position_gen(level='easy'):
    n = _pick_number(level)
    i, d = _pos_of(n)
    k = len(str(n))
    correct = f'{_POS_FR[i]} ({_POS_SYM[i]})'
    tagged = [(f'{_POS_FR[j]} ({_POS_SYM[j]})', 'wrong_position',
               'Count from the right: u, d, c, UM, DM, CM.',
               'Compte depuis la droite : u, d, c, UM, DM, CM.') for j in range(6) if j != i]
    random.shuffle(tagged)
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f"Dans **{sc.fmt_n(n)}**, quelle position occupe le chiffre **{d}** ?",
        'prompt_en': f"In **{sc.fmt_n(n)}**, which position does the digit **{d}** occupy?",
        'hint_fr': 'De droite à gauche : unités (u), dizaines (d), centaines (c), unités de mille (UM), dizaines de mille (DM), centaines de mille (CM).',
        'hint_en': 'Right to left: ones (u), tens (d), hundreds (c), thousands (UM), ten thousands (DM), hundred thousands (CM).',
        'show_illustration': False, 'shape_data': [],
        'choices': _tagged_shuffle_mc(correct, tagged[:4]),
        'pairs': [],
        'explanation_en': f'Positions from the right: {", ".join(_POS_EN[:k])}. The digit {d} is in position {i + 1} → {_POS_EN[i]} ({_POS_SYM[i]}).',
        'explanation_fr': f'Positions depuis la droite : {", ".join(_POS_FR[:k])}. Le chiffre {d} est à la position {i + 1} → {correct}.',
        'correct_answers': [correct, _POS_EN[i]],
    }


def g6_digit_value_gen(level='easy'):
    n = _pick_number(level)
    i, d = _pos_of(n)
    value = d * 10 ** i
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"Dans **{sc.fmt_n(n)}**, quelle est la valeur du chiffre **{d}** ?",
        'prompt_en': f"In **{sc.fmt_n(n)}**, what is the value of the digit **{d}**?",
        'hint_fr': f'Le chiffre {d} est à la position des {_POS_FR[i]} ({_POS_SYM[i]}) : sa valeur est {d} × {sc.fmt_n(10 ** i)}.',
        'hint_en': f'The digit {d} is in the {_POS_EN[i]} ({_POS_SYM[i]}) position: its value is {d} × {sc.fmt_n(10 ** i)}.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': f'{d} is in the {_POS_EN[i]} position → {d} × {sc.fmt_n(10 ** i)} = {sc.fmt_n(value)}.',
        'explanation_fr': f'{d} est à la position des {_POS_FR[i]} → {d} × {sc.fmt_n(10 ** i)} = {sc.fmt_n(value)}.',
        'correct_answers': [str(value)],
    }


def g6_count_groups_gen(level='easy'):
    n = _pick_number(level)
    i = random.choice({'easy': [2, 3], 'medium': [2, 3, 4], 'hard': [1, 2, 3, 4, 5]}[level])
    i = min(i, len(str(n)) - 1)
    answer = n // 10 ** i
    rest = n - answer * 10 ** i
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"Combien y a-t-il d'**{_POS_FR[i]}** en tout dans **{sc.fmt_n(n)}** ?" if _POS_FR[i][0] == 'u'
                     else f"Combien y a-t-il de **{_POS_FR[i]}** en tout dans **{sc.fmt_n(n)}** ?",
        'prompt_en': f"How many **{_POS_EN[i]}** are there in total in **{sc.fmt_n(n)}**?",
        'hint_fr': f"On veut le NOMBRE d'{_POS_FR[i]} (tous les groupes de {sc.fmt_n(10 ** i)}), pas seulement le chiffre. Cache les {i} chiffres de droite.",
        'hint_en': f'We want the NUMBER of {_POS_EN[i]} (all the groups of {sc.fmt_n(10 ** i)}), not just the digit. Cover the {i} rightmost digits.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': f'{sc.fmt_n(n)} = {sc.fmt_n(answer)} × {sc.fmt_n(10 ** i)} + {rest} → {sc.fmt_n(answer)} {_POS_EN[i]}.',
        'explanation_fr': f'{sc.fmt_n(n)} = {sc.fmt_n(answer)} × {sc.fmt_n(10 ** i)} + {rest} → {sc.fmt_n(answer)} {_POS_FR[i]}.',
        'correct_answers': [str(answer)],
    }


def g6_place_value_change_gen(level='easy'):
    n = _pick_number('easy' if level == 'easy' else 'medium')
    n_changes = 1 if level == 'easy' else 2
    changes = []
    positions = random.sample(range(1, 6), n_changes)
    for i in positions:
        d = (n // 10 ** i) % 10
        if level == 'hard':
            k = random.randint(1, 9)                 # may regroup
        else:
            k = random.randint(1, max(1, 9 - d))     # never regroups
        if len(str(n + k * 10 ** i)) > 6:
            k = 1
        changes.append((k, i))
    result = n + sum(k * 10 ** i for k, i in changes)
    if result > 999_999:
        changes = changes[:1]
        result = n + changes[0][0] * 10 ** changes[0][1]

    def part(k, i, lang):
        name = _POS_FR[i] if lang == 'fr' else _POS_EN[i]
        if k == 1:
            name = {'fr': _POS_FR_SING, 'en': _POS_EN_SING}[lang][i]
        return f"**{k} {name}**"
    fr = ' et '.join(part(k, i, 'fr') for k, i in changes)
    en = ' and '.join(part(k, i, 'en') for k, i in changes)
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"Pars du nombre **{sc.fmt_n(n)}** et ajoute {fr}. Quel nombre obtiens-tu ?",
        'prompt_en': f"Start from **{sc.fmt_n(n)}** and add {en}. What number do you get?",
        'hint_fr': 'Transforme chaque ajout en valeur (ex. 6 centaines de mille = 600 000), puis additionne.',
        'hint_en': 'Turn each addition into a value (e.g. 6 hundred thousands = 600 000), then add.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': f'{sc.fmt_n(n)} + ' + ' + '.join(sc.fmt_n(k * 10 ** i) for k, i in changes) + f' = {sc.fmt_n(result)}',
        'explanation_fr': f'{sc.fmt_n(n)} + ' + ' + '.join(sc.fmt_n(k * 10 ** i) for k, i in changes) + f' = {sc.fmt_n(result)}',
        'correct_answers': [str(result)],
    }


def _additive(n):
    return ' + '.join(sc.fmt_n(int(ch) * 10 ** (len(str(n)) - 1 - idx))
                      for idx, ch in enumerate(str(n)) if ch != '0')


def g6_additive_form_gen(level='easy'):
    n = _pick_number(level)
    if random.random() < 0.5:
        return {
            'q_type': 'text_input', 'answer_type': 'integer',
            'prompt_fr': f"Quel nombre est représenté par **{_additive(n)}** ?",
            'prompt_en': f"Which number is represented by **{_additive(n)}**?",
            'hint_fr': 'Place chaque valeur à sa position ; mets un 0 dans les positions absentes.',
            'hint_en': 'Put each value in its position; write 0 in the missing positions.',
            'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
            'explanation_en': f'{_additive(n)} = {sc.fmt_n(n)}',
            'explanation_fr': f'{_additive(n)} = {sc.fmt_n(n)}',
            'correct_answers': [str(n)],
        }
    correct = _additive(n)
    s = str(n)
    wrong = set()
    for _ in range(8):
        d = list(s); i, j = random.sample(range(len(d)), 2); d[i], d[j] = d[j], d[i]
        v = int(''.join(d))
        if v != n and len(str(v)) == len(s):
            wrong.add(_additive(v))
    terms = correct.split(' + ')
    if len(terms) > 2:
        wrong.add(' + '.join(terms[:-1]))
    wrong.add(' + '.join(sc.fmt_n(int(ch) * 10 ** (len(s) - 2 - idx)) for idx, ch in enumerate(s) if ch != '0' and len(s) - 2 - idx >= 0))
    wrong.discard(correct)
    tagged = [(w, 'wrong_decomposition', 'Check each digit against its place value.', 'Vérifie chaque chiffre avec la valeur de sa position.') for w in wrong if w]
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f"Quelle est la forme additive de **{sc.fmt_n(n)}** ?",
        'prompt_en': f"What is the additive form of **{sc.fmt_n(n)}**?",
        'hint_fr': 'Chaque chiffre non nul devient sa valeur de position, et on additionne.',
        'hint_en': 'Each non-zero digit becomes its place value, then add them.',
        'show_illustration': False, 'shape_data': [],
        'choices': _tagged_shuffle_mc(correct, tagged), 'pairs': [],
        'explanation_en': f'{sc.fmt_n(n)} = {correct}', 'explanation_fr': f'{sc.fmt_n(n)} = {correct}',
        'correct_answers': [correct],
    }


def g6_symbol_form_gen(level='easy'):
    """5 DM + 15 UM + 9 c + 10 d + 4 u → 66 004."""
    k = 5 if level == 'easy' else 6
    coeffs = {}
    for i in range(k):
        coeffs[i] = random.randint(0, 9)
    if level != 'easy':
        # one or two coefficients ≥ 10 force regrouping
        for i in random.sample(range(k - 1), 1 if level == 'medium' else 2):
            coeffs[i] = random.randint(10, 19)
    coeffs[k - 1] = max(1, coeffs[k - 1])
    total = sum(c * 10 ** i for i, c in coeffs.items())
    if total > 999_999:
        coeffs[k - 1] -= 1
        total = sum(c * 10 ** i for i, c in coeffs.items())
    order = list(range(k - 1, -1, -1))
    if level == 'hard':
        random.shuffle(order)
    expr = ' + '.join(f'{coeffs[i]} {_POS_SYM[i]}' for i in order if coeffs[i])
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"Quel nombre est représenté par **{expr}** ? (u = unités, d = dizaines, c = centaines, UM = unités de mille, DM = dizaines de mille, CM = centaines de mille)",
        'prompt_en': f"Which number is represented by **{expr}**? (u = ones, d = tens, c = hundreds, UM = thousands, DM = ten thousands, CM = hundred thousands)",
        'hint_fr': 'Convertis chaque terme en valeur (15 UM = 15 000) puis additionne tout. Un coefficient de 10 ou plus se regroupe dans la position supérieure.',
        'hint_en': 'Turn each term into a value (15 UM = 15 000) then add everything. A coefficient of 10 or more regroups into the next position.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': ' + '.join(sc.fmt_n(coeffs[i] * 10 ** i) for i in order if coeffs[i]) + f' = {sc.fmt_n(total)}',
        'explanation_fr': ' + '.join(sc.fmt_n(coeffs[i] * 10 ** i) for i in order if coeffs[i]) + f' = {sc.fmt_n(total)}',
        'correct_answers': [str(total)],
    }


def g6_multiplicative_form_gen(level='easy'):
    n = _pick_number(level)
    if random.random() < 0.5:
        correct = _mult_expansion(n)
        tagged = [t for t in _wrong_expansions(n) if t[0] and t[0] != correct]
        prompt_fr = f"Quelle est la forme multiplicative de **{sc.fmt_n(n)}** ?"
        prompt_en = f"What is the multiplicative form of **{sc.fmt_n(n)}**?"
        answers = [correct]
    else:
        correct = sc.fmt_n(n)
        s = str(n); wrong = set()
        for _ in range(8):
            d = list(s); i, j = random.sample(range(len(d)), 2); d[i], d[j] = d[j], d[i]
            v = int(''.join(d))
            if v != n and len(str(v)) == len(s):
                wrong.add(v)
        wrong.add(n // 10); wrong.add(n + 10 ** (len(s) - 2))
        tagged = [(sc.fmt_n(w), 'wrong_recompose', 'Add the value of every term.', 'Additionne la valeur de chaque terme.') for w in wrong if w != n]
        prompt_fr = f"Quel nombre s'écrit **{_mult_expansion(n)}** ?"
        prompt_en = f"Which number is written **{_mult_expansion(n)}**?"
        answers = [str(n)]
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': prompt_fr, 'prompt_en': prompt_en,
        'hint_fr': 'Chaque chiffre est multiplié par la valeur de sa position (1, 10, 100, 1 000, 10 000, 100 000).',
        'hint_en': 'Each digit is multiplied by its place value (1, 10, 100, 1 000, 10 000, 100 000).',
        'show_illustration': False, 'shape_data': [],
        'choices': _tagged_shuffle_mc(correct, tagged), 'pairs': [],
        'explanation_en': f'{sc.fmt_n(n)} = {_mult_expansion(n)}', 'explanation_fr': f'{sc.fmt_n(n)} = {_mult_expansion(n)}',
        'correct_answers': answers,
    }
