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
    """Column multiplication a × b (b < 100): the tens row is a × (tens digit), shifted one place."""
    pu, pt = _steps(a, b)
    u, t = b % 10, b // 10
    A, PU, PT, P, T = sc.fmt_n(a), sc.fmt_n(pu), sc.fmt_n(pt), sc.fmt_n(a * b), sc.fmt_n(a * t)
    if b < 10:
        return f'{A} × {b} = {P}'
    if u == 0:                                  # 20, 40, 90…: a single row, no "× 0" step
        if lang == 'fr':
            return f'{A} × {t} = {T}, puis on ajoute un 0 (× 10) : {A} × {b} = {P}'
        return f'{A} × {t} = {T}, then add a 0 (× 10): {A} × {b} = {P}'
    if lang == 'fr':
        return (f'Étape 1 : unités → {A} × {u} = {PU}\n'
                f'Étape 2 : dizaines → {A} × {t} = {T}, décalé d’un rang (un 0 à droite) → {PT}\n'
                f'Étape 3 : {PU} + {PT} = {P}')
    return (f'Step 1: ones → {A} × {u} = {PU}\n'
            f'Step 2: tens → {A} × {t} = {T}, shifted one place (a 0 on the right) → {PT}\n'
            f'Step 3: {PU} + {PT} = {P}')


def g6_multiply_gen(level='easy'):
    a, b = _factors(level)
    u, t = b % 10, b // 10
    if u == 0:
        hint_fr = f"Multiplie {sc.fmt_n(a)} par {t}, puis ajoute un 0 à droite (× 10)."
        hint_en = f"Multiply {sc.fmt_n(a)} by {t}, then add a 0 on the right (× 10)."
    else:
        hint_fr = (f"Multiplie par {u} (unités), puis par le chiffre des dizaines {t} en décalant d’un rang "
                   f"(un 0 à droite), et additionne les deux produits partiels.")
        hint_en = (f"Multiply by {u} (ones), then by the tens digit {t}, shifted one place "
                   f"(a 0 on the right), and add the two partial products.")
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"Calcule : **{sc.fmt_n(a)} × {b}**",
        'prompt_en': f"Calculate: **{sc.fmt_n(a)} × {b}**",
        'hint_fr': hint_fr,
        'hint_en': hint_en,
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': _expl(a, b, 'en'), 'explanation_fr': _expl(a, b, 'fr'),
        'correct_answers': [str(a * b)],
    }


def g6_partial_products_gen(level='easy'):
    a, b = _factors('medium' if level == 'easy' else level)
    while b % 10 == 0:                     # needs two partial products
        b += random.randint(1, 9)
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
    hint = {
        'units': (f"Multiplie {sc.fmt_n(a)} par le chiffre des unités, {b % 10}.",
                  f"Multiply {sc.fmt_n(a)} by the ones digit, {b % 10}."),
        'tens': (f"Multiplie {sc.fmt_n(a)} par le chiffre des dizaines, {b // 10}, puis place un 0 à droite : le produit des dizaines se termine toujours par 0.",
                 f"Multiply {sc.fmt_n(a)} by the tens digit, {b // 10}, then put a 0 on the right: the tens product always ends in 0."),
        'sum': ("Le produit final est la somme des deux produits partiels.",
                'The final product is the sum of the two partial products.'),
    }[which]
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': q_fr, 'prompt_en': q_en,
        'hint_fr': hint[0],
        'hint_en': hint[1],
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': _expl(a, b, 'en'), 'explanation_fr': _expl(a, b, 'fr'),
        'correct_answers': [str(ans)],
    }


def _round_lead(n):
    """Round to the leading digit: 1 835 → 2 000, 74 → 70, 826 → 800."""
    p = 10 ** (len(str(n)) - 1)
    return (n + p // 2) // p * p          # a half rounds up (250 → 300); round() would give 200


def _closest_only(key, exact, tagged):
    """Drop distractors at least as close to the exact product as the keyed estimate,
    so "the best estimate" has exactly one defensible answer."""
    gap = abs(key - exact)
    return [t for t in tagged if abs(int(t[0].replace(' ', '').replace(' ', '')) - exact) > gap]


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
    pa, pb = 10 ** (len(str(a)) - 1), 10 ** (len(str(b)) - 1)
    ta, tb = a // pa * pa, b // pb * pb            # truncated instead of rounded
    tagged = [
        (sc.fmt_n(est * 10), 'magnitude_x10', 'Count the zeros again.', 'Recompte les zéros.'),
        (sc.fmt_n(max(1, est // 10)), 'magnitude_div10', 'Count the zeros again.', 'Recompte les zéros.'),
        (sc.fmt_n(ra + rb), 'added_instead', 'This is an estimate of a sum, not a product.', "C'est une estimation d'une somme, pas d'un produit."),
        (sc.fmt_n(ta * rb), 'truncated', f'{sc.fmt_n(a)} rounds to {sc.fmt_n(ra)}: look at the second digit.', f'{sc.fmt_n(a)} s’arrondit à {sc.fmt_n(ra)} : regarde le deuxième chiffre.'),
        (sc.fmt_n(ra * tb), 'truncated', f'{sc.fmt_n(b)} rounds to {sc.fmt_n(rb)}: look at the second digit.', f'{sc.fmt_n(b)} s’arrondit à {sc.fmt_n(rb)} : regarde le deuxième chiffre.'),
        (sc.fmt_n(est * 100), 'magnitude_x100', 'Count the zeros again.', 'Recompte les zéros.'),
        (sc.fmt_n(ra * rb * 2), 'doubled', 'Multiply the rounded numbers only once.', 'Multiplie les nombres arrondis une seule fois.'),
    ]
    tagged = _closest_only(est, a * b, [t for t in tagged if t[0] != correct])
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f"Sans calculer exactement, quelle est la meilleure **estimation** de **{sc.fmt_n(a)} × {sc.fmt_n(b)}** ? (arrondis chaque nombre au rang de son premier chiffre)",
        'prompt_en': f"Without calculating exactly, what is the best **estimate** of **{sc.fmt_n(a)} × {sc.fmt_n(b)}**? (round each number to the place value of its leading digit)",
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
    # "combien de œufs" → "combien d'œufs"
    de_th = ("d’" if th_fr[:1].lower() in 'aeiouyhéèêàâîôûœ' else 'de ') + th_fr
    unit_pl_fr = {'day': 'jours', 'minute': 'minutes', 'second': 'secondes', 'hour': 'heures', 'trip': 'sorties'}[pkey]
    unit_pl_en = {'day': 'days', 'minute': 'minutes', 'second': 'seconds', 'hour': 'hours', 'trip': 'trips'}[pkey]
    # A conversion is needed only when the duration is not already in the rate's unit
    # ("3 semaines" → 21 jours, but "30 jours" is already 30 days).
    converts = per_fr != f'{count} {unit_pl_fr}'
    conv_fr = f'{per_fr} = {count} {unit_pl_fr}' if converts else ''
    conv_en = f'{per_en} = {count} {unit_pl_en}' if converts else ''
    if ask_estimate:
        est = ra * rc
        pc = 10 ** (len(str(count)) - 1)
        tagged = [(sc.fmt_n(est * 10), 'magnitude_x10', 'Count the zeros again.', 'Recompte les zéros.'),
                  (sc.fmt_n(max(1, est // 10)), 'magnitude_div10', 'Count the zeros again.', 'Recompte les zéros.'),
                  (sc.fmt_n(ra + rc), 'added_instead', 'It is a product, not a sum.', "C'est un produit, pas une somme."),
                  (sc.fmt_n(ra * (count // pc * pc)), 'truncated', f'{count} rounds to {rc}.', f'{count} s’arrondit à {rc}.'),
                  (sc.fmt_n(est * 100), 'magnitude_x100', 'Count the zeros again.', 'Recompte les zéros.'),
                  (sc.fmt_n(ra), 'forgot_duration', f'Multiply by the number of {unit_pl_en}.', f'Multiplie par le nombre de {unit_pl_fr}.')]
        # The keyed estimate must be the closest choice to the exact answer.
        tagged = _closest_only(est, exact, [t for t in tagged if t[0] != sc.fmt_n(est)])
        lead_fr = f"{conv_fr}. " if converts else ''
        lead_en = f"{conv_en}. " if converts else ''
        return {
            'q_type': 'multiple_choice',
            'prompt_fr': f"{story_fr} Environ combien {de_th} en **{per_fr}** ? Choisis la meilleure estimation.",
            'prompt_en': f"{story_en} About how many {th_en} in **{per_en}**? Choose the best estimate.",
            'hint_fr': f"{lead_fr}Arrondis : {sc.fmt_n(rate)} ≈ {sc.fmt_n(ra)} et {count} ≈ {rc}.",
            'hint_en': f"{lead_en}Round: {sc.fmt_n(rate)} ≈ {sc.fmt_n(ra)} and {count} ≈ {rc}.",
            'show_illustration': False, 'shape_data': [],
            'choices': _tagged_shuffle_mc(sc.fmt_n(est), tagged), 'pairs': [],
            'explanation_en': f'{lead_en}Estimate: {sc.fmt_n(ra)} × {rc} = {sc.fmt_n(est)} (exact: {sc.fmt_n(exact)}).',
            'explanation_fr': f'{lead_fr}Estimation : {sc.fmt_n(ra)} × {rc} = {sc.fmt_n(est)} (exact : {sc.fmt_n(exact)}).',
            'correct_answers': [sc.fmt_n(est)],
        }
    extra_fr = extra_en = ''
    if level == 'hard':
        # Deliberate unneeded fact: the hard level trains picking the useful data.
        d_fr, d_en, dlo, dhi = random.choice(sc.DISTRACTOR_FACTS)
        dn = random.randint(dlo, dhi)
        extra_fr = ' ' + d_fr.format(n=sc.fmt_n(dn))
        extra_en = ' ' + d_en.format(n=sc.fmt_n(dn))
    first_fr = f"Convertis d'abord la durée ({conv_fr}), puis estime" if converts else 'Estime'
    first_en = f"Convert the duration first ({conv_en}), then estimate" if converts else 'Estimate'
    head_fr = f'{conv_fr}. ' if converts else ''
    head_en = f'{conv_en}. ' if converts else ''
    if count >= 10:
        expl_fr = f'{head_fr}Estimation : {sc.fmt_n(ra)} × {rc} = {sc.fmt_n(ra * rc)}.\n' + _expl(rate, count, 'fr')
        expl_en = f'{head_en}Estimate: {sc.fmt_n(ra)} × {rc} = {sc.fmt_n(ra * rc)}.\n' + _expl(rate, count, 'en')
    else:
        expl_fr = f'{head_fr}{sc.fmt_n(rate)} × {count} = {sc.fmt_n(exact)}'
        expl_en = f'{head_en}{sc.fmt_n(rate)} × {count} = {sc.fmt_n(exact)}'
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"{story_fr}{extra_fr} Combien {de_th} en **{per_fr}** exactement ?",
        'prompt_en': f"{story_en}{extra_en} Exactly how many {th_en} in **{per_en}**?",
        'hint_fr': f"{first_fr} ({sc.fmt_n(ra)} × {rc} ≈ {sc.fmt_n(ra * rc)}), puis calcule {sc.fmt_n(rate)} × {count}.",
        'hint_en': f"{first_en} ({sc.fmt_n(ra)} × {rc} ≈ {sc.fmt_n(ra * rc)}), then compute {sc.fmt_n(rate)} × {count}.",
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': expl_en,
        'explanation_fr': expl_fr,
        'correct_answers': [str(exact)],
    }
