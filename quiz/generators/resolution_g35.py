"""
resolution_g35.py — extra "Résolution" story families for grade 3 and grade 5
(the shared families in resolution.py also serve these grades).

Families:
  sharing            equal groups, sharing, missing parts (grade 3 arithmetic)
  rounding_estimate  round then add / multiply (grade 3 approximation)
  fencing            perimeter of a garden, cost per metre (grade 3 measurement)
  fraction_of        fraction of a collection, the rest, decimal form (grade 3 fractions)
  survey             bar-chart style counts in words: totals, differences (grade 3 statistics)
  decimal_shopping   prices with cents, change, order of operations (grade 5 arithmetic)
  volume_capacity    aquarium volume, litres, mass conversions (grade 5 measurement)
  mean_scores        arithmetic mean, score needed (grade 5 statistics)
  probability_bag    marbles in a bag, outcomes of choices (grade 5 probability)
  temperature_change rises and drops through the day, never below 0 (grade 5)
  solids             faces / vertices / edges of several solids (grade 5 geometry)
"""
import random
from fractions import Fraction
from . import scenarios as sc
from .resolution import _problem, _cap, N, inventory, money, schedule, measurements, pattern, production


def _money_fr(x):
    return f"{x:.2f}".replace('.', ',') + ' $'


def _money_en(x):
    return f"${x:.2f}"


# ─────────────────────────────────────────────────────────────────────────────
# Grade 3
# ─────────────────────────────────────────────────────────────────────────────

def sharing(grade):
    who, g = sc.pick_actor()
    key, thing = sc.pick_thing('object')
    cont = sc.pick_container('object')
    variant = random.choice(['groups_minus', 'share_minus', 'missing_start', 'left_over', 'two_kinds'])
    if variant == 'groups_minus':
        n, per, give = random.randint(3, 9), random.randint(3, 9), random.randint(2, 9)
        total = n * per
        return _problem(
            f"{who} a **{n}** {sc.cont(cont, n, 'fr')} de **{per}** {sc.noun(thing, per, 'fr')}. {_cap(sc.pronoun_fr(g))} en donne **{give}** à un ami. Combien de {sc.noun(thing, 2, 'fr')} lui reste-t-il ?",
            f"{who} has **{n}** {sc.cont(cont, n, 'en')} of **{per}** {sc.noun(thing, per, 'en')}. {_cap(sc.pronoun_en(g))} gives **{give}** to a friend. How many {sc.noun(thing, 2, 'en')} are left?",
            total - give, [f'{n} × {per} = {total}', f'{total} − {give} = {total - give}', f'{total - give} {sc.noun(thing, total - give, "fr")}'],
            [f'{n} × {per} = {total}', f'{total} − {give} = {total - give}', f'{total - give} {sc.noun(thing, total - give, "en")}'],
            "Multiplie pour trouver le total, puis soustrais.", 'Multiply to find the total, then subtract.')
    if variant == 'share_minus':
        friends = random.randint(2, 6)
        each = random.randint(3, 9)
        total = friends * each
        eat = random.randint(1, each - 1)
        return _problem(
            f"{who} partage **{total}** {sc.noun(thing, total, 'fr')} également entre **{friends}** amis. Chaque ami en utilise ensuite **{eat}**. Combien en reste-t-il à chaque ami ?",
            f"{who} shares **{total}** {sc.noun(thing, total, 'en')} equally among **{friends}** friends. Each friend then uses **{eat}**. How many does each friend have left?",
            each - eat, [f'{total} ÷ {friends} = {each}', f'{each} − {eat} = {each - eat}', f'{each - eat} {sc.noun(thing, each - eat, "fr")} chacun'],
            [f'{total} ÷ {friends} = {each}', f'{each} − {eat} = {each - eat}', f'{each - eat} {sc.noun(thing, each - eat, "en")} each'],
            "Partage d'abord (division), puis enlève ce qui est utilisé.", 'Share first (division), then take away what is used.')
    if variant == 'missing_start':
        got, now = random.randint(5, 40), random.randint(50, 99)
        start = now - got
        return _problem(
            f"Après avoir reçu **{got}** {sc.noun(thing, got, 'fr')}, {who} en a maintenant **{now}**. Combien en avait-{sc.pronoun_fr(g)} au départ ?",
            f"After receiving **{got}** {sc.noun(thing, got, 'en')}, {who} now has **{now}**. How many did {sc.pronoun_en(g)} have at the start?",
            start, [f'? + {got} = {now}', f'{now} − {got} = {start}', f'{start} {sc.noun(thing, start, "fr")}'],
            [f'? + {got} = {now}', f'{now} − {got} = {start}', f'{start} {sc.noun(thing, start, "en")}'],
            'Le nombre de départ est le terme manquant : total − ce qui a été reçu.', 'The starting number is the missing term: total − what was received.')
    if variant == 'left_over':
        per = random.randint(3, 9)
        boxes = random.randint(3, 9)
        rest = random.randint(1, per - 1)
        total = boxes * per + rest
        return _problem(
            f"{who} range **{total}** {sc.noun(thing, total, 'fr')} dans des {sc.cont(cont, 2, 'fr')} de **{per}**. Combien de {sc.cont(cont, 2, 'fr')} pleines obtient-{sc.pronoun_fr(g)}, et combien de {sc.noun(thing, 2, 'fr')} restent ? Écris seulement le nombre de {sc.noun(thing, 2, 'fr')} qui restent.",
            f"{who} puts **{total}** {sc.noun(thing, total, 'en')} into {sc.cont(cont, 2, 'en')} of **{per}**. How many full {sc.cont(cont, 2, 'en')}, and how many {sc.noun(thing, 2, 'en')} are left over? Write only the number left over.",
            rest, [f'{total} ÷ {per} = {boxes} reste {rest}', f'{boxes} {sc.cont(cont, boxes, "fr")} pleines', f'{rest} {sc.noun(thing, rest, "fr")} restent'],
            [f'{total} ÷ {per} = {boxes} remainder {rest}', f'{boxes} full {sc.cont(cont, boxes, "en")}', f'{rest} {sc.noun(thing, rest, "en")} left over'],
            'Division avec reste : le reste est ce qui ne remplit pas une boîte.', 'Division with a remainder: the remainder is what does not fill a box.')
    key2, thing2 = sc.pick_thing('object')
    while key2 == key:
        key2, thing2 = sc.pick_thing('object')
    n1, p1, n2, p2 = random.randint(2, 6), random.randint(4, 9), random.randint(2, 6), random.randint(4, 9)
    t1, t2 = n1 * p1, n2 * p2
    return _problem(
        f"{who} achète **{n1}** paquets de **{p1}** {sc.noun(thing, p1, 'fr')} et **{n2}** paquets de **{p2}** {sc.noun(thing2, p2, 'fr')}. Combien d'objets cela fait-il en tout ?",
        f"{who} buys **{n1}** packs of **{p1}** {sc.noun(thing, p1, 'en')} and **{n2}** packs of **{p2}** {sc.noun(thing2, p2, 'en')}. How many objects is that altogether?",
        t1 + t2, [f'{n1} × {p1} = {t1}', f'{n2} × {p2} = {t2}', f'{t1} + {t2} = {t1 + t2}', f'{t1 + t2} objets'],
        [f'{n1} × {p1} = {t1}', f'{n2} × {p2} = {t2}', f'{t1} + {t2} = {t1 + t2}', f'{t1 + t2} objects'],
        'Deux multiplications, puis une addition.', 'Two multiplications, then an addition.')


def rounding_estimate(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['sum_tens', 'sum_hundreds', 'enough'])
    items = random.sample(['un ballon', 'un livre', 'un casse-tête', 'une lampe', 'un sac', 'des écouteurs'], 3)
    items_en = {'un ballon': 'a ball', 'un livre': 'a book', 'un casse-tête': 'a puzzle', 'une lampe': 'a lamp', 'un sac': 'a bag', 'des écouteurs': 'headphones'}
    if variant == 'sum_tens':
        prices = [random.randint(11, 89) for _ in range(3)]
        rnd = [round(p / 10) * 10 for p in prices]
        est = sum(rnd)
        return _problem(
            f"{who} veut acheter {items[0]} à **{prices[0]} $**, {items[1]} à **{prices[1]} $** et {items[2]} à **{prices[2]} $**. Arrondis chaque prix à la dizaine près, puis estime le total.",
            f"{who} wants to buy {items_en[items[0]]} for **${prices[0]}**, {items_en[items[1]]} for **${prices[1]}** and {items_en[items[2]]} for **${prices[2]}**. Round each price to the nearest ten, then estimate the total.",
            est, [', '.join(f'{p} ≈ {r}' for p, r in zip(prices, rnd)), f'{" + ".join(map(str, rnd))} = {est}', f'environ {est} $ (exact : {sum(prices)} $)'],
            [', '.join(f'{p} ≈ {r}' for p, r in zip(prices, rnd)), f'{" + ".join(map(str, rnd))} = {est}', f'about ${est} (exact: ${sum(prices)})'],
            'Regarde le chiffre des unités : 5 ou plus → dizaine supérieure.', 'Look at the ones digit: 5 or more → round up.',
            'money', [f'{est} $', str(est)])
    if variant == 'sum_hundreds':
        prices = [random.randint(110, 890) for _ in range(2)]
        rnd = [round(p / 100) * 100 for p in prices]
        est = sum(rnd)
        return _problem(
            f"Une école achète {items[0]} à **{prices[0]} $** et {items[1]} à **{prices[1]} $**. Arrondis chaque prix à la centaine près, puis estime le total.",
            f"A school buys {items_en[items[0]]} for **${prices[0]}** and {items_en[items[1]]} for **${prices[1]}**. Round each price to the nearest hundred, then estimate the total.",
            est, [', '.join(f'{p} ≈ {r}' for p, r in zip(prices, rnd)), f'{" + ".join(map(str, rnd))} = {est}', f'environ {est} $ (exact : {sum(prices)} $)'],
            [', '.join(f'{p} ≈ {r}' for p, r in zip(prices, rnd)), f'{" + ".join(map(str, rnd))} = {est}', f'about ${est} (exact: ${sum(prices)})'],
            'Regarde le chiffre des dizaines : 5 ou plus → centaine supérieure.', 'Look at the tens digit: 5 or more → round up.',
            'money', [f'{est} $', str(est)])
    prices = [random.randint(11, 49) for _ in range(3)]
    budget = random.choice([100, 120, 150])
    total = sum(prices)
    diff = abs(budget - total)
    return _problem(
        f"{who} a **{budget} $** et veut acheter {items[0]} ({prices[0]} $), {items[1]} ({prices[1]} $) et {items[2]} ({prices[2]} $). Calcule le total exact. Combien d'argent lui {'restera-t-il' if total <= budget else 'manquera-t-il'} ?",
        f"{who} has **${budget}** and wants to buy {items_en[items[0]]} (${prices[0]}), {items_en[items[1]]} (${prices[1]}) and {items_en[items[2]]} (${prices[2]}). Work out the exact total. How much money will {'be left' if total <= budget else 'be missing'}?",
        diff, [f'{" + ".join(map(str, prices))} = {total}', f'{max(budget, total)} − {min(budget, total)} = {diff}', f'{diff} $ {"restent" if total <= budget else "manquent"}'],
        [f'{" + ".join(map(str, prices))} = {total}', f'{max(budget, total)} − {min(budget, total)} = {diff}', f'${diff} {"left" if total <= budget else "missing"}'],
        'Additionne les prix, puis compare au budget.', 'Add the prices, then compare with the budget.',
        'money', [f'{diff} $', str(diff)])


def fencing(grade):
    who_fr, who_en, g = sc.pick_role()
    w, h = random.randint(3, 12), random.randint(3, 12)
    unit = 'm'
    per = 2 * (w + h)
    variant = random.choice(['perimeter', 'cost', 'square', 'missing_side'])
    if variant == 'perimeter':
        return _problem(
            f"{_cap(who_fr)} veut clôturer un jardin rectangulaire de **{w} {unit}** de long et **{h} {unit}** de large. Quelle longueur de clôture faut-il ?",
            f"{_cap(who_en)} wants to fence a rectangular garden **{w} {unit}** long and **{h} {unit}** wide. What length of fence is needed?",
            per, [f'Périmètre = {w} + {h} + {w} + {h}', f'= 2 × ({w} + {h}) = {per}', f'{per} {unit}'],
            [f'Perimeter = {w} + {h} + {w} + {h}', f'= 2 × ({w} + {h}) = {per}', f'{per} {unit}'],
            'Le périmètre est la somme des 4 côtés.', 'The perimeter is the sum of the 4 sides.')
    if variant == 'cost':
        price = random.choice([2, 3, 4, 5])
        return _problem(
            f"{_cap(who_fr)} clôture un jardin rectangulaire de **{w} {unit}** sur **{h} {unit}**. La clôture coûte **{price} $** le mètre. Combien coûte toute la clôture ?",
            f"{_cap(who_en)} fences a rectangular garden **{w} {unit}** by **{h} {unit}**. The fence costs **${price}** per metre. How much does the whole fence cost?",
            per * price, [f'Périmètre : 2 × ({w} + {h}) = {per} {unit}', f'{per} × {price} = {per * price}', f'{per * price} $'],
            [f'Perimeter: 2 × ({w} + {h}) = {per} {unit}', f'{per} × {price} = {per * price}', f'${per * price}'],
            "Trouve le périmètre, puis multiplie par le prix du mètre.", 'Find the perimeter, then multiply by the price per metre.',
            'money', [f'{per * price} $', str(per * price)])
    if variant == 'square':
        s = random.randint(4, 15)
        gates = random.randint(1, 3)
        return _problem(
            f"Un enclos carré a des côtés de **{s} {unit}**. On laisse une ouverture de **{gates} {unit}** pour la porte. Quelle longueur de clôture faut-il ?",
            f"A square pen has sides of **{s} {unit}**. A **{gates} {unit}** opening is left for the gate. What length of fence is needed?",
            4 * s - gates, [f'4 × {s} = {4 * s}', f'{4 * s} − {gates} = {4 * s - gates}', f'{4 * s - gates} {unit}'],
            [f'4 × {s} = {4 * s}', f'{4 * s} − {gates} = {4 * s - gates}', f'{4 * s - gates} {unit}'],
            "Périmètre du carré, puis enlève l'ouverture.", 'Perimeter of the square, then take away the opening.')
    return _problem(
        f"Le périmètre d'un terrain rectangulaire est **{per} {unit}**. Sa longueur est **{w} {unit}**. Quelle est sa largeur ?",
        f"The perimeter of a rectangular field is **{per} {unit}**. Its length is **{w} {unit}**. What is its width?",
        h, [f'{per} ÷ 2 = {w + h} (longueur + largeur)', f'{w + h} − {w} = {h}', f'{h} {unit}'],
        [f'{per} ÷ 2 = {w + h} (length + width)', f'{w + h} − {w} = {h}', f'{h} {unit}'],
        'La moitié du périmètre = longueur + largeur.', 'Half the perimeter = length + width.')


def fraction_of(grade):
    who, g = sc.pick_actor()
    key, thing = sc.pick_thing('object')
    d = random.choice([2, 3, 4, 5, 6, 8, 10])
    n = random.randint(1, d - 1)
    total = d * random.randint(2, 6)
    part = total * n // d
    color_fr, color_en = random.choice([('rouges', 'red'), ('bleues', 'blue'), ('vertes', 'green'), ('jaunes', 'yellow')])
    variant = random.choice(['rest', 'part', 'decimal'])
    if variant == 'part':
        return _problem(
            f"{who} a **{total}** {sc.noun(thing, total, 'fr')}. **{n}/{d}** d'entre eux sont {color_fr}. Combien de {sc.noun(thing, 2, 'fr')} sont {color_fr} ?",
            f"{who} has **{total}** {sc.noun(thing, total, 'en')}. **{n}/{d}** of them are {color_en}. How many {sc.noun(thing, 2, 'en')} are {color_en}?",
            part, [f'1/{d} de {total} = {total} ÷ {d} = {total // d}', f'{n}/{d} = {n} × {total // d} = {part}', f'{part} {sc.noun(thing, part, "fr")} {color_fr}'],
            [f'1/{d} of {total} = {total} ÷ {d} = {total // d}', f'{n}/{d} = {n} × {total // d} = {part}', f'{part} {color_en} {sc.noun(thing, part, "en")}'],
            "Trouve d'abord une part (÷ dénominateur), puis multiplie par le numérateur.", 'Find one part first (÷ denominator), then multiply by the numerator.')
    if variant == 'rest':
        return _problem(
            f"{who} a **{total}** {sc.noun(thing, total, 'fr')}. **{n}/{d}** d'entre eux sont {color_fr}. Combien de {sc.noun(thing, 2, 'fr')} ne sont **pas** {color_fr} ?",
            f"{who} has **{total}** {sc.noun(thing, total, 'en')}. **{n}/{d}** of them are {color_en}. How many {sc.noun(thing, 2, 'en')} are **not** {color_en}?",
            total - part, [f'{n}/{d} de {total} = {n} × ({total} ÷ {d}) = {part}', f'{total} − {part} = {total - part}', f'{total - part} {sc.noun(thing, total - part, "fr")}'],
            [f'{n}/{d} of {total} = {n} × ({total} ÷ {d}) = {part}', f'{total} − {part} = {total - part}', f'{total - part} {sc.noun(thing, total - part, "en")}'],
            'Calcule la fraction, puis soustrais du total.', 'Work out the fraction, then subtract from the total.')
    d2 = random.choice([2, 4, 5, 10])
    n2 = random.randint(1, d2 - 1)
    dec = n2 / d2
    dec_fr = f'{dec:.2f}'.rstrip('0').rstrip('.').replace('.', ',')
    dec_en = f'{dec:.2f}'.rstrip('0').rstrip('.')
    return _problem(
        f"{who} a mangé **{n2}/{d2}** d'une tablette de chocolat. Écris cette fraction sous forme de nombre décimal.",
        f"{who} ate **{n2}/{d2}** of a chocolate bar. Write this fraction as a decimal number.",
        dec, [f'{n2}/{d2} = {n2 * (100 // d2)}/100' if d2 != 10 else f'{n2}/10 = {n2} dixième(s)', f'= {dec_fr}', dec_fr],
        [f'{n2}/{d2} = {n2 * (100 // d2)}/100' if d2 != 10 else f'{n2}/10 = {n2} tenth(s)', f'= {dec_en}', dec_en],
        'Transforme en dixièmes ou en centièmes.', 'Turn it into tenths or hundredths.',
        'decimal', [dec_fr, dec_en, f'{n2}/{d2}'])


def survey(grade):
    cats_fr = ['chat', 'chien', 'poisson', 'lapin', 'oiseau']
    cats_en = {'chat': 'cat', 'chien': 'dog', 'poisson': 'fish', 'lapin': 'rabbit', 'oiseau': 'bird'}
    picked = random.sample(cats_fr, 3)
    vals = [random.randint(3, 15) for _ in picked]
    art = lambda c: "l'" + c if c[0] in 'aeiou' else 'le ' + c
    txt_fr = ', '.join(f'**{v}** élèves préfèrent {art(c)}' for c, v in zip(picked, vals))
    txt_en = ', '.join(f'**{v}** students prefer the {cats_en[c]}' for c, v in zip(picked, vals))
    variant = random.choice(['total', 'diff', 'missing'])
    if variant == 'total':
        return _problem(f"Dans une classe, {txt_fr}. Combien d'élèves ont répondu au sondage ?", f"In a class, {txt_en}. How many students answered the survey?", sum(vals),
                        [f'{" + ".join(map(str, vals))} = {sum(vals)}', f'{sum(vals)} élèves'], [f'{" + ".join(map(str, vals))} = {sum(vals)}', f'{sum(vals)} students'],
                        'Additionne toutes les catégories.', 'Add all the categories.')
    if variant == 'diff':
        hi, lo = max(vals), min(vals)
        return _problem(f"Dans une classe, {txt_fr}. Combien d'élèves de plus ont choisi l'animal le plus populaire par rapport au moins populaire ?",
                        f"In a class, {txt_en}. How many more students chose the most popular animal than the least popular?", hi - lo,
                        [f'Le plus : {hi}, le moins : {lo}', f'{hi} − {lo} = {hi - lo}', f'{hi - lo} élèves de plus'], [f'Most: {hi}, least: {lo}', f'{hi} − {lo} = {hi - lo}', f'{hi - lo} more students'],
                        'Repère le plus grand et le plus petit, puis soustrais.', 'Find the largest and smallest, then subtract.')
    total = sum(vals) + random.randint(2, 9)
    missing = total - sum(vals)
    return _problem(f"**{total}** élèves ont répondu à un sondage : {txt_fr}. Les autres préfèrent le hamster. Combien préfèrent le hamster ?",
                    f"**{total}** students answered a survey: {txt_en}. The others prefer the hamster. How many prefer the hamster?", missing,
                    [f'{" + ".join(map(str, vals))} = {sum(vals)}', f'{total} − {sum(vals)} = {missing}', f'{missing} élèves'], [f'{" + ".join(map(str, vals))} = {sum(vals)}', f'{total} − {sum(vals)} = {missing}', f'{missing} students'],
                    'Additionne ce qui est connu, puis soustrais du total.', 'Add what is known, then subtract from the total.')


# ─────────────────────────────────────────────────────────────────────────────
# Grade 5
# ─────────────────────────────────────────────────────────────────────────────

_SHOP = [('cahier', 'cahiers', 'notebook', 'notebooks'), ('crayon', 'crayons', 'pencil', 'pencils'), ('règle', 'règles', 'ruler', 'rulers'),
         ('gomme', 'gommes', 'eraser', 'erasers'), ('stylo', 'stylos', 'pen', 'pens'), ('carnet', 'carnets', 'notepad', 'notepads')]


def decimal_shopping(grade):
    who, g = sc.pick_actor()
    (a_s, a_p, ae_s, ae_p), (b_s, b_p, be_s, be_p) = random.sample(_SHOP, 2)
    qa, qb = random.randint(2, 6), random.randint(1, 4)
    pa = random.randint(105, 495) / 100
    pb = random.randint(80, 350) / 100
    total = round(qa * pa + qb * pb, 2)
    variant = random.choice(['total', 'change', 'each', 'ops'])
    if variant == 'total':
        return _problem(
            f"{who} achète **{qa}** {a_p} à **{_money_fr(pa)}** l'unité et **{qb}** {b_p if qb > 1 else b_s} à **{_money_fr(pb)}**{" l'unité" if qb > 1 else ''}. Combien paie-t-{sc.pronoun_fr(g)} en tout ?",
            f"{who} buys **{qa}** {ae_p} at **{_money_en(pa)}** each and **{qb}** {be_p if qb > 1 else be_s} at **{_money_en(pb)}** {'each' if qb > 1 else ''}. How much does {sc.pronoun_en(g)} pay in total?",
            total, [f'{qa} × {_money_fr(pa)} = {_money_fr(qa * pa)}', f'{qb} × {_money_fr(pb)} = {_money_fr(qb * pb)}', f'{_money_fr(qa * pa)} + {_money_fr(qb * pb)} = {_money_fr(total)}', _money_fr(total)],
            [f'{qa} × {_money_en(pa)} = {_money_en(qa * pa)}', f'{qb} × {_money_en(pb)} = {_money_en(qb * pb)}', f'{_money_en(qa * pa)} + {_money_en(qb * pb)} = {_money_en(total)}', _money_en(total)],
            'Multiplie chaque prix par la quantité, puis additionne.', 'Multiply each price by the quantity, then add.',
            'money', [_money_fr(total), f'{total:.2f}'])
    if variant == 'change':
        paid = 20 if total < 20 else 50
        change = round(paid - total, 2)
        return _problem(
            f"{who} achète **{qa}** {a_p} à **{_money_fr(pa)}** l'unité et **{qb}** {b_p if qb > 1 else b_s} à **{_money_fr(pb)}**{" l'unité" if qb > 1 else ''}. {_cap(sc.pronoun_fr(g))} paie avec un billet de **{paid} $**. Combien de monnaie reçoit-{sc.pronoun_fr(g)} ?",
            f"{who} buys **{qa}** {ae_p} at **{_money_en(pa)}** each and **{qb}** {be_p if qb > 1 else be_s} at **{_money_en(pb)}**{' each' if qb > 1 else ''}. {_cap(sc.pronoun_en(g))} pays with a **${paid}** bill. How much change does {sc.pronoun_en(g)} get?",
            change, [f'{qa} × {_money_fr(pa)} + {qb} × {_money_fr(pb)} = {_money_fr(total)}', f'{paid} $ − {_money_fr(total)} = {_money_fr(change)}', _money_fr(change)],
            [f'{qa} × {_money_en(pa)} + {qb} × {_money_en(pb)} = {_money_en(total)}', f'${paid} − {_money_en(total)} = {_money_en(change)}', _money_en(change)],
            'Total des achats, puis soustrais du billet.', 'Total of the purchases, then subtract from the bill.',
            'money', [_money_fr(change), f'{change:.2f}'])
    if variant == 'each':
        n = random.choice([3, 4, 5, 6, 8])
        each = random.randint(105, 895) / 100
        tot = round(n * each, 2)
        return _problem(
            f"{who} paie **{_money_fr(tot)}** pour **{n}** {a_p} identiques. Combien coûte un {a_s} ?",
            f"{who} pays **{_money_en(tot)}** for **{n}** identical {ae_p}. How much does one {ae_s} cost?",
            each, [f'{_money_fr(tot)} ÷ {n} = {_money_fr(each)}', _money_fr(each)], [f'{_money_en(tot)} ÷ {n} = {_money_en(each)}', _money_en(each)],
            'Divise le total par le nombre d\'objets.', 'Divide the total by the number of items.',
            'money', [_money_fr(each), f'{each:.2f}'])
    boxes, per, extra, give = random.randint(3, 9), random.randint(6, 12), random.randint(2, 9), random.randint(3, 12)
    val = boxes * per + extra - give
    key, thing = sc.pick_thing('object')
    return _problem(
        f"{who} a **{boxes}** boîtes de **{per}** {sc.noun(thing, per, 'fr')} et **{extra}** {sc.noun(thing, extra, 'fr')} en plus, puis en donne **{give}**. Écris le calcul en une seule expression et trouve le résultat : {boxes} × {per} + {extra} − {give} = ?",
        f"{who} has **{boxes}** boxes of **{per}** {sc.noun(thing, per, 'en')} plus **{extra}** more {sc.noun(thing, extra, 'en')}, then gives **{give}** away. Write it as one expression and find the result: {boxes} × {per} + {extra} − {give} = ?",
        val, [f'Priorité : la multiplication d\'abord : {boxes} × {per} = {boxes * per}', f'{boxes * per} + {extra} − {give} = {val}', f'{val} {sc.noun(thing, val, "fr")}'],
        [f'Order of operations: multiply first: {boxes} × {per} = {boxes * per}', f'{boxes * per} + {extra} − {give} = {val}', f'{val} {sc.noun(thing, val, "en")}'],
        'Multiplication avant addition et soustraction.', 'Multiplication before addition and subtraction.')


def volume_capacity(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['aquarium', 'litres', 'bottles', 'mass'])
    if variant == 'aquarium':
        L, W, H = random.randint(20, 60), random.randint(10, 40), random.randint(10, 40)
        v = L * W * H
        return _problem(
            f"L'aquarium de {who} mesure **{L} cm** de long, **{W} cm** de large et **{H} cm** de haut. Quel est son volume en cm³ ?",
            f"{who}'s aquarium is **{L} cm** long, **{W} cm** wide and **{H} cm** high. What is its volume in cm³?",
            v, [f'Volume = longueur × largeur × hauteur', f'{L} × {W} × {H} = {N(v)}', f'{N(v)} cm³'], ['Volume = length × width × height', f'{L} × {W} × {H} = {N(v)}', f'{N(v)} cm³'],
            'Multiplie les trois dimensions.', 'Multiply the three dimensions.')
    if variant == 'litres':
        L, W, H = random.choice([20, 25, 40, 50]), random.choice([10, 20, 25]), random.choice([10, 20, 40])
        v = L * W * H
        litres = v // 1000
        return _problem(
            f"Un bac mesure **{L} cm** × **{W} cm** × **{H} cm**. Sachant que 1 000 cm³ = 1 L, combien de litres d'eau peut-il contenir ?",
            f"A tub measures **{L} cm** × **{W} cm** × **{H} cm**. Knowing that 1 000 cm³ = 1 L, how many litres of water can it hold?",
            litres, [f'{L} × {W} × {H} = {N(v)} cm³', f'{N(v)} ÷ 1 000 = {litres}', f'{litres} L'], [f'{L} × {W} × {H} = {N(v)} cm³', f'{N(v)} ÷ 1 000 = {litres}', f'{litres} L'],
            'Volume en cm³, puis divise par 1 000.', 'Volume in cm³, then divide by 1 000.')
    if variant == 'bottles':
        n = random.randint(3, 9)
        ml = random.choice([250, 330, 500, 750])
        big = random.choice([2, 3, 4])
        total_ml = n * ml
        return _problem(
            f"{who} verse **{n}** bouteilles de **{ml} mL** dans une cruche de **{big} L**. Combien de millilitres manque-t-il pour remplir la cruche ? (si elle déborde, écris 0)",
            f"{who} pours **{n}** bottles of **{ml} mL** into a **{big} L** jug. How many millilitres are missing to fill the jug? (if it overflows, write 0)",
            max(0, big * 1000 - total_ml), [f'{n} × {ml} = {N(total_ml)} mL', f'{big} L = {N(big * 1000)} mL', f'{N(big * 1000)} − {N(total_ml)} = {N(max(0, big * 1000 - total_ml))}', f'{N(max(0, big * 1000 - total_ml))} mL'],
            [f'{n} × {ml} = {N(total_ml)} mL', f'{big} L = {N(big * 1000)} mL', f'{N(big * 1000)} − {N(total_ml)} = {N(max(0, big * 1000 - total_ml))}', f'{N(max(0, big * 1000 - total_ml))} mL'],
            'Mets tout en millilitres, puis soustrais.', 'Put everything in millilitres, then subtract.')
    bags = random.randint(2, 6)
    kg = random.choice([1, 2, 5])
    g_ = random.choice([250, 500, 750])
    total_g = bags * kg * 1000 + g_
    return _problem(
        f"Une recette utilise **{bags}** sacs de **{kg} kg** de farine et **{g_} g** de sucre. Quelle est la masse totale en grammes ?",
        f"A recipe uses **{bags}** bags of **{kg} kg** of flour and **{g_} g** of sugar. What is the total mass in grams?",
        total_g, [f'{bags} × {kg} kg = {bags * kg} kg = {N(bags * kg * 1000)} g', f'{N(bags * kg * 1000)} + {g_} = {N(total_g)}', f'{N(total_g)} g'],
        [f'{bags} × {kg} kg = {bags * kg} kg = {N(bags * kg * 1000)} g', f'{N(bags * kg * 1000)} + {g_} = {N(total_g)}', f'{N(total_g)} g'],
        '1 kg = 1 000 g. Convertis, puis additionne.', '1 kg = 1 000 g. Convert, then add.')


def mean_scores(grade):
    who, g = sc.pick_actor()
    n = random.choice([3, 4, 5])
    mean = random.randint(6, 18)
    scores = [random.randint(mean - 4, mean + 4) for _ in range(n - 1)]
    last = mean * n - sum(scores)
    if last < 0 or last > 25:
        scores = [mean] * (n - 1); last = mean
    all_scores = scores + [last]
    variant = random.choice(['mean', 'needed', 'total'])
    if variant == 'mean':
        return _problem(
            f"{who} a obtenu **{', '.join(map(str, all_scores))}** points sur 20 à ses {n} derniers tests. Quelle est sa moyenne ?",
            f"{who} scored **{', '.join(map(str, all_scores))}** out of 20 on the last {n} tests. What is the mean?",
            mean, [f'{" + ".join(map(str, all_scores))} = {sum(all_scores)}', f'{sum(all_scores)} ÷ {n} = {mean}', f'moyenne {mean}'], [f'{" + ".join(map(str, all_scores))} = {sum(all_scores)}', f'{sum(all_scores)} ÷ {n} = {mean}', f'mean {mean}'],
            'Additionne, puis divise par le nombre de tests.', 'Add, then divide by the number of tests.')
    if variant == 'needed':
        return _problem(
            f"{who} a obtenu **{', '.join(map(str, scores))}** points à ses {n - 1} premiers tests. Combien doit-{sc.pronoun_fr(g)} obtenir au {n}e test pour avoir une moyenne de **{mean}** ?",
            f"{who} scored **{', '.join(map(str, scores))}** on the first {n - 1} tests. What must {sc.pronoun_en(g)} score on test {n} to have a mean of **{mean}**?",
            last, [f'Total visé : {mean} × {n} = {mean * n}', f'Déjà : {" + ".join(map(str, scores))} = {sum(scores)}', f'{mean * n} − {sum(scores)} = {last}', f'{last} points'],
            [f'Target total: {mean} × {n} = {mean * n}', f'So far: {" + ".join(map(str, scores))} = {sum(scores)}', f'{mean * n} − {sum(scores)} = {last}', f'{last} points'],
            'Moyenne × nombre de tests = total visé ; enlève ce qui est déjà obtenu.', 'Mean × number of tests = target total; subtract what was already scored.')
    return _problem(
        f"La moyenne de {who} sur **{n}** tests est **{mean}**. Quel est le total de ses points ?",
        f"{who}'s mean over **{n}** tests is **{mean}**. What is the total of the points?",
        mean * n, [f'moyenne × nombre = total', f'{mean} × {n} = {mean * n}', f'{mean * n} points'], ['mean × number = total', f'{mean} × {n} = {mean * n}', f'{mean * n} points'],
        'Le total est la moyenne multipliée par le nombre de tests.', 'The total is the mean multiplied by the number of tests.')


def probability_bag(grade):
    who, g = sc.pick_actor()
    colors = random.sample([('rouges', 'red'), ('bleues', 'blue'), ('vertes', 'green'), ('jaunes', 'yellow')], 3)
    counts = [random.randint(2, 9) for _ in colors]
    total = sum(counts)
    variant = random.choice(['after_removal', 'not_color', 'outcomes'])
    if variant == 'outcomes':
        a, b, c = random.randint(2, 5), random.randint(2, 4), random.randint(2, 3)
        return _problem(
            f"{who} choisit un chandail parmi **{a}**, un pantalon parmi **{b}** et une paire de chaussures parmi **{c}**. Combien de tenues différentes peut-{sc.pronoun_fr(g)} composer ?",
            f"{who} picks a shirt from **{a}**, pants from **{b}** and shoes from **{c}** pairs. How many different outfits can {sc.pronoun_en(g)} make?",
            a * b * c, [f'{a} × {b} = {a * b}', f'{a * b} × {c} = {a * b * c}', f'{a * b * c} tenues'], [f'{a} × {b} = {a * b}', f'{a * b} × {c} = {a * b * c}', f'{a * b * c} outfits'],
            'Multiplie le nombre de choix de chaque sorte.', 'Multiply the number of choices of each kind.')
    i = random.randrange(3)
    if variant == 'not_color':
        fav = total - counts[i]
        fr = Fraction(fav, total)
        return _problem(
            f"Un sac contient {', '.join(f'**{n}** billes {c[0]}' for n, c in zip(counts, colors))}. {who} pige une bille sans regarder. Quelle est la probabilité qu'elle ne soit **pas** {colors[i][0][:-1]} ? (fraction)",
            f"A bag holds {', '.join(f'**{n}** {c[1]} marbles' for n, c in zip(counts, colors))}. {who} picks one without looking. What is the probability it is **not** {colors[i][1]}? (fraction)",
            f'{fr.numerator}/{fr.denominator}', [f'Total : {" + ".join(map(str, counts))} = {total}', f'Pas {colors[i][0]} : {total} − {counts[i]} = {fav}', f'{fav}/{total} = {fr.numerator}/{fr.denominator}'],
            [f'Total: {" + ".join(map(str, counts))} = {total}', f'Not {colors[i][1]}: {total} − {counts[i]} = {fav}', f'{fav}/{total} = {fr.numerator}/{fr.denominator}'],
            'Cas favorables (toutes les autres couleurs) sur le total.', 'Favourable cases (all the other colours) over the total.',
            'fraction', [f'{fr.numerator}/{fr.denominator}', f'{fav}/{total}'])
    removed = random.randint(1, counts[i])
    new_total = total - removed
    fav = counts[i] - removed
    fr = Fraction(fav, new_total) if new_total else Fraction(0)
    return _problem(
        f"Un sac contient {', '.join(f'**{n}** billes {c[0]}' for n, c in zip(counts, colors))}. {who} retire **{removed}** bille{'s' if removed > 1 else ''} {colors[i][0] if removed > 1 else colors[i][0][:-1]}, puis pige au hasard. Quelle est la probabilité de piger une bille {colors[i][0][:-1]} ? (fraction)",
        f"A bag holds {', '.join(f'**{n}** {c[1]} marbles' for n, c in zip(counts, colors))}. {who} removes **{removed}** {colors[i][1]} marble{'s' if removed > 1 else ''}, then picks at random. What is the probability of picking a {colors[i][1]} marble? (fraction)",
        f'{fr.numerator}/{fr.denominator}', [f'Il reste {counts[i]} − {removed} = {fav} {colors[i][0]}', f'Total : {total} − {removed} = {new_total}', f'{fav}/{new_total} = {fr.numerator}/{fr.denominator}'],
        [f'{counts[i]} − {removed} = {fav} {colors[i][1]} left', f'Total: {total} − {removed} = {new_total}', f'{fav}/{new_total} = {fr.numerator}/{fr.denominator}'],
        'Mets à jour le nombre de billes de la couleur ET le total.', 'Update both the number of that colour AND the total.',
        'fraction', [f'{fr.numerator}/{fr.denominator}', f'{fav}/{new_total}'])


def temperature_change(grade):
    city = random.choice(['Québec', 'Gaspé', 'Sherbrooke', 'Rimouski', 'Val-d’Or', 'Trois-Rivières'])
    start = random.randint(2, 12)
    up = random.randint(4, 14)
    down = random.randint(1, start + up - 1)
    end = start + up - down
    variant = random.choice(['end', 'range', 'drop'])
    if variant == 'end':
        return _problem(
            f"À {city}, il fait **{start} °C** le matin. La température monte de **{up} °C** à midi, puis baisse de **{down} °C** le soir. Quelle est la température le soir ?",
            f"In {city}, it is **{start} °C** in the morning. The temperature rises by **{up} °C** at noon, then drops by **{down} °C** in the evening. What is the evening temperature?",
            end, [f'{start} + {up} = {start + up} °C à midi', f'{start + up} − {down} = {end} °C', f'{end} °C'], [f'{start} + {up} = {start + up} °C at noon', f'{start + up} − {down} = {end} °C', f'{end} °C'],
            'Avance sur le thermomètre pour une hausse, recule pour une baisse.', 'Move up the thermometer for a rise, down for a drop.')
    if variant == 'range':
        temps = [random.randint(0, 30) for _ in range(5)]
        return _problem(
            f"Températures relevées à {city} cette semaine : **{', '.join(f'{t} °C' for t in temps)}**. Quel est l'écart entre la plus chaude et la plus froide ?",
            f"Temperatures recorded in {city} this week: **{', '.join(f'{t} °C' for t in temps)}**. What is the gap between the warmest and the coldest?",
            max(temps) - min(temps), [f'Plus chaude : {max(temps)} °C, plus froide : {min(temps)} °C', f'{max(temps)} − {min(temps)} = {max(temps) - min(temps)}', f'{max(temps) - min(temps)} °C'],
            [f'Warmest: {max(temps)} °C, coldest: {min(temps)} °C', f'{max(temps)} − {min(temps)} = {max(temps) - min(temps)}', f'{max(temps) - min(temps)} °C'],
            'Repère le maximum et le minimum, puis soustrais.', 'Find the maximum and the minimum, then subtract.')
    return _problem(
        f"À {city}, il faisait **{start + up} °C** à midi et **{end} °C** le soir. De combien de degrés la température a-t-elle baissé ?",
        f"In {city}, it was **{start + up} °C** at noon and **{end} °C** in the evening. By how many degrees did the temperature drop?",
        down, [f'{start + up} − {end} = {down}', f'{down} °C'], [f'{start + up} − {end} = {down}', f'{down} °C'],
        'La baisse est la différence entre les deux températures.', 'The drop is the difference between the two temperatures.')


_SOLIDS = [('cube', 'cube', 6, 8, 12), ('prisme à base triangulaire', 'triangular prism', 5, 6, 9),
           ('pyramide à base carrée', 'square pyramid', 5, 5, 8), ('prisme à base rectangulaire', 'rectangular prism', 6, 8, 12),
           ('pyramide à base triangulaire', 'triangular pyramid', 4, 4, 6), ('prisme à base pentagonale', 'pentagonal prism', 7, 10, 15)]


def solids(grade):
    who, g = sc.pick_actor()
    (a_fr, a_en, Fa, Va, Ea), (b_fr, b_en, Fb, Vb, Eb) = random.sample(_SOLIDS, 2)
    na, nb = random.randint(2, 6), random.randint(2, 6)
    variant = random.choice(['edges_total', 'euler', 'sticks'])
    if variant == 'edges_total':
        return _problem(
            f"{who} construit **{na}** {a_fr}s et **{nb}** {b_fr}s avec des pailles (une paille par arête). Combien de pailles utilise-t-{sc.pronoun_fr(g)} en tout ?",
            f"{who} builds **{na}** {a_en}s and **{nb}** {b_en}s with straws (one straw per edge). How many straws does {sc.pronoun_en(g)} use in total?",
            na * Ea + nb * Eb, [f'{a_fr} : {Ea} arêtes → {na} × {Ea} = {na * Ea}', f'{b_fr} : {Eb} arêtes → {nb} × {Eb} = {nb * Eb}', f'{na * Ea} + {nb * Eb} = {na * Ea + nb * Eb}', f'{na * Ea + nb * Eb} pailles'],
            [f'{a_en}: {Ea} edges → {na} × {Ea} = {na * Ea}', f'{b_en}: {Eb} edges → {nb} × {Eb} = {nb * Eb}', f'{na * Ea} + {nb * Eb} = {na * Ea + nb * Eb}', f'{na * Ea + nb * Eb} straws'],
            'Arêtes de chaque solide × nombre de solides, puis additionne.', 'Edges of each solid × number of solids, then add.')
    if variant == 'euler':
        return _problem(
            f"Un solide a **{Fa} faces** et **{Va} sommets**. Avec la relation d'Euler (sommets − arêtes + faces = 2), combien a-t-il d'arêtes ? Puis, combien d'arêtes ont **{na}** solides identiques ?",
            f"A solid has **{Fa} faces** and **{Va} vertices**. Using Euler's relation (vertices − edges + faces = 2), how many edges does it have? Then, how many edges do **{na}** identical solids have?",
            na * Ea, [f'{Va} − A + {Fa} = 2 → A = {Va + Fa - 2}', f'{na} × {Ea} = {na * Ea}', f'{na * Ea} arêtes'], [f'{Va} − E + {Fa} = 2 → E = {Va + Fa - 2}', f'{na} × {Ea} = {na * Ea}', f'{na * Ea} edges'],
            'Trouve les arêtes avec Euler, puis multiplie.', 'Find the edges with Euler, then multiply.')
    sticks = random.choice([30, 40, 50, 60])
    made = sticks // Ea
    left = sticks - made * Ea
    return _problem(
        f"{who} a **{sticks}** cure-dents. Chaque {a_fr} demande une cure-dent par arête ({Ea} arêtes). Combien de {a_fr}s complets peut-{sc.pronoun_fr(g)} faire, et combien de cure-dents restent ? Écris seulement le nombre de cure-dents qui restent.",
        f"{who} has **{sticks}** toothpicks. Each {a_en} needs one toothpick per edge ({Ea} edges). How many complete {a_en}s can {sc.pronoun_en(g)} make, and how many toothpicks are left? Write only the number of toothpicks left.",
        left, [f'{sticks} ÷ {Ea} = {made} reste {left}', f'{made} {a_fr}s complets', f'{left} cure-dents restent'], [f'{sticks} ÷ {Ea} = {made} remainder {left}', f'{made} complete {a_en}s', f'{left} toothpicks left'],
        'Division avec reste.', 'Division with a remainder.')


# ─────────────────────────────────────────────────────────────────────────────
# registry for grades 3 and 5 (+ the general arithmetic skills, sized like grade 3)
# ─────────────────────────────────────────────────────────────────────────────

FAMILIES_G35 = {
    # general arithmetic (any grade) — small numbers
    'add':                 (3, [sharing, money, survey]),
    'subtract':            (3, [sharing, money, survey]),
    'multiply':            (3, [sharing, pattern]),
    'divide':              (3, [sharing]),
    # grade 3
    'order-numbers':       (3, [measurements]),
    'missing-addend':      (3, [sharing]),
    'missing-subtrahend':  (3, [sharing]),
    'word-problem':        (3, [sharing, money, survey]),
    'multiply-context':    (3, [sharing, pattern]),
    'repeated-addition':   (3, [sharing, pattern]),
    'division-sharing':    (3, [sharing]),
    'choose-operation':    (3, [sharing, money, survey]),
    'fact-family':         (3, [sharing]),
    'number-sequence':     (3, [pattern]),
    'perimeter-labeled':   (3, [fencing]),
    'round-ten':           (3, [rounding_estimate]),
    'round-hundred':       (3, [rounding_estimate]),
    'count-groups':        (3, [inventory, sharing]),
    'fraction-shape':      (3, [fraction_of]),
    'fraction-collection': (3, [fraction_of]),
    'fraction-to-decimal': (3, [fraction_of]),
    'money-change':        (3, [money, rounding_estimate]),
    'money-match':         (3, [money]),
    'read-clock':          (3, [schedule]),
    'time-convert':        (3, [schedule]),
    'read-bar-chart':      (3, [survey]),
    # grade 5
    'g5-order-ops':        (5, [decimal_shopping]),
    'g5-decimal-mult':     (5, [decimal_shopping]),
    'g5-div-decimal':      (5, [decimal_shopping]),
    'g5-decimal-div':      (5, [decimal_shopping]),
    'g5-volume':           (5, [volume_capacity]),
    'g5-capacity-convert': (5, [volume_capacity]),
    'g5-mass-convert':     (5, [volume_capacity]),
    'g5-elapsed-time':     (5, [schedule]),
    'g5-temperature':      (5, [temperature_change]),
    'g5-thermometer':      (5, [temperature_change]),
    'g5-large-integer':    (5, [inventory, measurements]),
    'g5-number-line':      (5, [measurements]),
    'g5-arithmetic-mean':  (5, [mean_scores]),
    'g5-data-table':       (5, [mean_scores, survey]),
    'g5-pie-chart':        (5, [survey]),
    'g5-probability-frac': (5, [probability_bag]),
    'g5-probability-forms': (5, [probability_bag]),
    'g5-count-outcomes':   (5, [probability_bag]),
    'g5-euler':            (5, [solids]),
    'g5-solid-counts':     (5, [solids]),
}
