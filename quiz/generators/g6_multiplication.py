"""
g6_multiplication.py — Grade-6 column multiplication & estimation (content_g6.md §4–5).

Topics:
  g6_multiply_gen          typed (integer) – 826 × 74 (2×2 easy, 3×2 medium, 3×2 with zeros/nines hard)
  g6_partial_products_gen  typed (integer) – one step of the algorithm: 826 × 4, 826 × 70, or their sum
  g6_estimate_product_gen  QCM             – best estimate by rounding: 1 835 × 21 ≈ 2 000 × 20 = 40 000
  g6_rate_problem_gen      typed (integer) – "Une reine abeille pond 1 835 œufs par jour. En 3 semaines ?" (estimate or exact)
"""
import random
from .base import _tagged_shuffle_mc
from . import scenarios as sc


def _factors(level):
    if level == 'easy':
        return random.randint(12, 99), random.randint(12, 99)
    if level == 'medium':
        return random.randint(112, 989), random.randint(12, 99)
    a = random.choice([random.randint(100, 999), int(f'{random.randint(1, 9)}0{random.randint(1, 9)}'), random.randint(890, 999)])
    b = random.choice([random.randint(12, 99), random.randint(90, 99), int(f'{random.randint(1, 9)}0')])
    return a, b


def _steps(a, b):
    u, t = b % 10, b // 10
    return a * u, a * t * 10


def _expl(a, b, lang):
    pu, pt = _steps(a, b)
    if lang == 'fr':
        return (f'Étape 1 : unités → {sc.fmt_n(a)} × {b % 10} = {sc.fmt_n(pu)}\n'
                f'Étape 2 : dizaines → {sc.fmt_n(a)} × {b // 10 * 10} = {sc.fmt_n(pt)} (on place un 0 à droite)\n'
                f'Étape 3 : {sc.fmt_n(pu)} + {sc.fmt_n(pt)} = {sc.fmt_n(a * b)}')
    return (f'Step 1: ones → {sc.fmt_n(a)} × {b % 10} = {sc.fmt_n(pu)}\n'
            f'Step 2: tens → {sc.fmt_n(a)} × {b // 10 * 10} = {sc.fmt_n(pt)} (place a 0 on the right)\n'
            f'Step 3: {sc.fmt_n(pu)} + {sc.fmt_n(pt)} = {sc.fmt_n(a * b)}')


def g6_multiply_gen(level='easy'):
    a, b = _factors(level)
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"Calcule : **{sc.fmt_n(a)} × {b}**",
        'prompt_en': f"Calculate: **{sc.fmt_n(a)} × {b}**",
        'hint_fr': f"Multiplie par {b % 10} (unités), puis par {b // 10 * 10} (dizaines, avec un 0 à droite), et additionne les deux produits partiels.",
        'hint_en': f"Multiply by {b % 10} (ones), then by {b // 10 * 10} (tens, with a 0 on the right), and add the two partial products.",
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': _expl(a, b, 'en'), 'explanation_fr': _expl(a, b, 'fr'),
        'correct_answers': [str(a * b)],
    }


def g6_partial_products_gen(level='easy'):
    a, b = _factors('medium' if level == 'easy' else level)
    pu, pt = _steps(a, b)
    which = random.choice(['units', 'tens', 'sum']) if level != 'easy' else random.choice(['units', 'tens'])
    if which == 'units':
        q_fr = f"Dans la multiplication **{sc.fmt_n(a)} × {b}**, quel est le produit partiel des **unités** ({sc.fmt_n(a)} × {b % 10}) ?"
        q_en = f"In the multiplication **{sc.fmt_n(a)} × {b}**, what is the **ones** partial product ({sc.fmt_n(a)} × {b % 10})?"
        ans = pu
    elif which == 'tens':
        q_fr = f"Dans la multiplication **{sc.fmt_n(a)} × {b}**, quel est le produit partiel des **dizaines** ({sc.fmt_n(a)} × {b // 10 * 10}) ?"
        q_en = f"In the multiplication **{sc.fmt_n(a)} × {b}**, what is the **tens** partial product ({sc.fmt_n(a)} × {b // 10 * 10})?"
        ans = pt
    else:
        q_fr = f"Les produits partiels de **{sc.fmt_n(a)} × {b}** sont {sc.fmt_n(pu)} et {sc.fmt_n(pt)}. Quel est le produit final ?"
        q_en = f"The partial products of **{sc.fmt_n(a)} × {b}** are {sc.fmt_n(pu)} and {sc.fmt_n(pt)}. What is the final product?"
        ans = a * b
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': q_fr, 'prompt_en': q_en,
        'hint_fr': "Le produit des dizaines se termine toujours par 0 : on multiplie par le chiffre des dizaines puis on place un 0.",
        'hint_en': 'The tens product always ends in 0: multiply by the tens digit, then place a 0.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': _expl(a, b, 'en'), 'explanation_fr': _expl(a, b, 'fr'),
        'correct_answers': [str(ans)],
    }


def _round_lead(n):
    """Round to the leading digit: 1 835 → 2 000, 74 → 70, 826 → 800."""
    p = 10 ** (len(str(n)) - 1)
    return round(n / p) * p


def g6_estimate_product_gen(level='easy'):
    if level == 'easy':
        a, b = random.randint(112, 989), random.randint(12, 99)
    elif level == 'medium':
        a, b = random.randint(1_100, 9_899), random.randint(12, 99)
    else:
        a, b = random.randint(1_100, 9_899), random.randint(112, 989)
    ra, rb = _round_lead(a), _round_lead(b)
    est = ra * rb
    correct = sc.fmt_n(est)
    tagged = [
        (sc.fmt_n(est * 10), 'magnitude_x10', 'Count the zeros again.', 'Recompte les zéros.'),
        (sc.fmt_n(max(1, est // 10)), 'magnitude_div10', 'Count the zeros again.', 'Recompte les zéros.'),
        (sc.fmt_n(ra + rb), 'added_instead', 'This is an estimate of a sum, not a product.', "C'est une estimation d'une somme, pas d'un produit."),
        (sc.fmt_n((ra // 10 * 10 if ra >= 100 else ra) * (rb // 10 * 10 if rb >= 100 else rb) if False else _round_lead(a) * (rb + 10 ** (len(str(b)) - 1))), 'rounded_wrong', 'Round each factor to its leading digit.', 'Arrondis chaque facteur à son premier chiffre.'),
        (sc.fmt_n(ra * rb + ra), 'rounded_wrong', 'Round each factor to its leading digit.', 'Arrondis chaque facteur à son premier chiffre.'),
    ]
    tagged = [t for t in tagged if t[0] != correct]
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f"Sans calculer exactement, quelle est la meilleure **estimation** de **{sc.fmt_n(a)} × {sc.fmt_n(b)}** ? (arrondis chaque nombre à son premier chiffre)",
        'prompt_en': f"Without calculating exactly, what is the best **estimate** of **{sc.fmt_n(a)} × {sc.fmt_n(b)}**? (round each number to its leading digit)",
        'hint_fr': f"{sc.fmt_n(a)} ≈ {sc.fmt_n(ra)} et {sc.fmt_n(b)} ≈ {sc.fmt_n(rb)}. Multiplie les chiffres de tête, puis ajoute tous les zéros.",
        'hint_en': f"{sc.fmt_n(a)} ≈ {sc.fmt_n(ra)} and {sc.fmt_n(b)} ≈ {sc.fmt_n(rb)}. Multiply the leading digits, then add all the zeros.",
        'show_illustration': False, 'shape_data': [],
        'choices': _tagged_shuffle_mc(correct, tagged), 'pairs': [],
        'explanation_en': f'{sc.fmt_n(a)} ≈ {sc.fmt_n(ra)}, {sc.fmt_n(b)} ≈ {sc.fmt_n(rb)} → {sc.fmt_n(ra)} × {sc.fmt_n(rb)} = {correct} (exact: {sc.fmt_n(a * b)})',
        'explanation_fr': f'{sc.fmt_n(a)} ≈ {sc.fmt_n(ra)}, {sc.fmt_n(b)} ≈ {sc.fmt_n(rb)} → {sc.fmt_n(ra)} × {sc.fmt_n(rb)} = {correct} (exact : {sc.fmt_n(a * b)})',
        'correct_answers': [correct],
    }


def g6_rate_problem_gen(level='easy'):
    subj_fr, subj_en, v_fr, v_en, th_fr, th_en, pkey, lo, hi = random.choice(sc.RATES)
    rate = random.randint(lo, hi)
    n, per_fr, per_en, count = random.choice(sc.PERIODS[pkey])
    unit_fr = {'day': 'par jour', 'minute': 'par minute', 'second': 'par seconde', 'hour': "par heure", 'trip': 'par sortie'}[pkey]
    unit_en = {'day': 'per day', 'minute': 'per minute', 'second': 'per second', 'hour': 'per hour', 'trip': 'per trip'}[pkey]
    exact = rate * count
    story_fr = f"{subj_fr} {v_fr} **{sc.fmt_n(rate)} {th_fr}** {unit_fr}."
    story_en = f"{subj_en} {v_en} **{sc.fmt_n(rate)} {th_en}** {unit_en}."
    ask_estimate = level == 'easy' or (level == 'medium' and random.random() < 0.3)
    ra, rc = _round_lead(rate), _round_lead(count)
    if ask_estimate:
        est = ra * rc
        tagged = [(sc.fmt_n(est * 10), 'magnitude_x10', 'Count the zeros again.', 'Recompte les zéros.'),
                  (sc.fmt_n(max(1, est // 10)), 'magnitude_div10', 'Count the zeros again.', 'Recompte les zéros.'),
                  (sc.fmt_n(ra + rc), 'added_instead', 'It is a product, not a sum.', "C'est un produit, pas une somme."),
                  (sc.fmt_n(est + ra), 'rounded_wrong', 'Round both numbers first.', "Arrondis d'abord les deux nombres."),
                  (sc.fmt_n(rate * (count + 10)), 'rounded_wrong', 'Round both numbers first.', "Arrondis d'abord les deux nombres.")]
        tagged = [t for t in tagged if t[0] != sc.fmt_n(est)]
        return {
            'q_type': 'multiple_choice',
            'prompt_fr': f"{story_fr} Environ combien de {th_fr} en **{per_fr}** ? Choisis la meilleure estimation.",
            'prompt_en': f"{story_en} About how many {th_en} in **{per_en}**? Choose the best estimate.",
            'hint_fr': f"{per_fr} = {count} {('jours' if pkey == 'day' else 'minutes' if pkey == 'minute' else 'secondes' if pkey == 'second' else 'heures' if pkey == 'hour' else 'sorties')}. Arrondis : {sc.fmt_n(rate)} ≈ {sc.fmt_n(ra)} et {count} ≈ {rc}.",
            'hint_en': f"{per_en} = {count} {('days' if pkey == 'day' else 'minutes' if pkey == 'minute' else 'seconds' if pkey == 'second' else 'hours' if pkey == 'hour' else 'trips')}. Round: {sc.fmt_n(rate)} ≈ {sc.fmt_n(ra)} and {count} ≈ {rc}.",
            'show_illustration': False, 'shape_data': [],
            'choices': _tagged_shuffle_mc(sc.fmt_n(est), tagged), 'pairs': [],
            'explanation_en': f'{per_en} = {count}. Estimate: {sc.fmt_n(ra)} × {rc} = {sc.fmt_n(est)} (exact: {sc.fmt_n(exact)}).',
            'explanation_fr': f'{per_fr} = {count}. Estimation : {sc.fmt_n(ra)} × {rc} = {sc.fmt_n(est)} (exact : {sc.fmt_n(exact)}).',
            'correct_answers': [sc.fmt_n(est)],
        }
    extra_fr = extra_en = ''
    if level == 'hard':
        d_fr, d_en, dlo, dhi = random.choice(sc.DISTRACTOR_FACTS)
        dn = random.randint(dlo, dhi)
        extra_fr = ' ' + d_fr.format(n=sc.fmt_n(dn))
        extra_en = ' ' + d_en.format(n=sc.fmt_n(dn))
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"{story_fr}{extra_fr} Combien de {th_fr} en **{per_fr}** exactement ?",
        'prompt_en': f"{story_en}{extra_en} Exactly how many {th_en} in **{per_en}**?",
        'hint_fr': f"Convertis d'abord la durée ({per_fr} = {count}), estime ({sc.fmt_n(ra)} × {rc} ≈ {sc.fmt_n(ra * rc)}), puis calcule {sc.fmt_n(rate)} × {count}.",
        'hint_en': f"Convert the duration first ({per_en} = {count}), estimate ({sc.fmt_n(ra)} × {rc} ≈ {sc.fmt_n(ra * rc)}), then compute {sc.fmt_n(rate)} × {count}.",
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': f'{per_en} = {count}. Estimate: {sc.fmt_n(ra)} × {rc} = {sc.fmt_n(ra * rc)}.\n' + _expl(rate, count, 'en') if count >= 10 else f'{sc.fmt_n(rate)} × {count} = {sc.fmt_n(exact)}',
        'explanation_fr': f'{per_fr} = {count}. Estimation : {sc.fmt_n(ra)} × {rc} = {sc.fmt_n(ra * rc)}.\n' + _expl(rate, count, 'fr') if count >= 10 else f'{sc.fmt_n(rate)} × {count} = {sc.fmt_n(exact)}',
        'correct_answers': [str(exact)],
    }
