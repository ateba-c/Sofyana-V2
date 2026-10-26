"""
resolution_plus.py — "Résolution" (problem-solving) families for the skills added by
the 2026-10 curriculum upgrade (task F3).  Same contract as resolution.py: each
family is ``family(grade) -> problem`` built with ``_problem`` (typed answer, step
explanation, FR + EN), and ``FAMILIES_PLUS`` maps a skill slug to
``(grade, [families])``.  Skills that are about naming, sorting or reasoning
(vocabulary, « who is right? », shape recognition…) deliberately get no 4th level.

Families:
  early_story       two-step add / subtract stories ≤ 20 (grade 1) or ≤ 100 (grade 2)
  rows_groups       chairs in rows, stickers per page, missing factor (grade 4)
  remainder_trips   buses (round up), full boxes (round down), what is left (grade 4)
  plant_growth      weekly heights read like a line graph (grade 4)
  ribbon            cm / mm (grade 3) or m / cm (grade 5) lengths cut and joined
  tiling            floors covered with squares (grade 3) or cm² / m² areas and costs (grade 5)
  cube_boxes        boxes filled with unit cubes (grade 3) or cm³ and litres (grade 6)
  balance           identical objects on a balance, jugs poured into cups (grade 3)
  angles            missing angle in a triangle, on a straight line, clock hands (grade 6)
  circles           radius / diameter of wheels, coins in a row (grade 6)
  decimal_measures  race times and jumps with decimals: gaps, totals, rounding, × 10/100/1000
  fair_share        sharing pizzas → a fraction each, fraction of a set (grade 5)
  recipe_fractions  related-denominator sums, whole × fraction, simplest fraction (grade 6)
  percent_shop      discounts, percent of a class, fraction ↔ percent (grade 6)
  teams             equal teams with no one left out, common multiples (grade 6)
  powers_story      messages passed on, cubes built from small cubes (grade 6)
  outfits           counting combinations (grade 3 two kinds, grade 5 three kinds)
  expected_count    how many times a spinner / die result is expected (grade 5)
  grid_walk         moving on a grid: blocks walked, where you end up
  signed_story      temperatures below zero, elevator floors, divers (grade 6 integers — the only family with
                    negative answers, decision D2)
"""
import random
from fractions import Fraction
from . import scenarios as sc
from .resolution import _problem, _cap, N, inventory, money, pattern, production
from .resolution_g35 import (
    sharing, rounding_estimate, fraction_of, survey, decimal_shopping, volume_capacity,
    probability_bag, temperature_change, _money_fr, _money_en,
)


def _d(x, places, lang):
    """Decimal display from a float already rounded: _d(2.5, 1, 'fr') → '2,5'."""
    s = f'{x:.{places}f}'
    return s.replace('.', ',') if lang == 'fr' else s


def _dec_answers(x, places):
    s = f'{x:.{places}f}'
    trimmed = s.rstrip('0').rstrip('.') if '.' in s else s
    return list(dict.fromkeys([trimmed.replace('.', ','), trimmed, s.replace('.', ','), s]))


_SUP = {2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶'}


def _que(name):
    """French 'que' + name with elision: _que('Aïcha') → "qu'Aïcha"."""
    return ("qu'" if name[:1].lower() in 'aeiouhéèêàâîôûï' else 'que ') + name


def _frac(fr):
    return str(fr.numerator) if fr.denominator == 1 else f'{fr.numerator}/{fr.denominator}'


def _frac_answers(fr, *extra):
    out = [_frac(fr)]
    if fr > 1 and fr.denominator != 1:
        w = fr.numerator // fr.denominator
        out.append(f'{w} {fr.numerator - w * fr.denominator}/{fr.denominator}')
    return out + [e for e in extra if e not in out]


# ─────────────────────────────────────────────────────────────────────────────
# Grades 1–2
# ─────────────────────────────────────────────────────────────────────────────

def early_story(grade):
    who, g = sc.pick_actor()
    top = 20 if grade <= 1 else 100
    key, thing = sc.pick_thing('object')
    n_fr, n_en = sc.noun(thing, 2, 'fr'), sc.noun(thing, 2, 'en')
    variant = random.choice(['get_give', 'give_get', 'missing_start', 'compare'])
    if variant == 'compare':
        a = random.randint(top // 4, top // 2)
        b = random.randint(1, a - 1)
        friend = random.choice([x for x in sc.ACTORS if x[0] != who])[0]
        return _problem(
            f"{who} a **{a}** {n_fr}. {friend} en a **{b}**. Combien {who} en a-t-{sc.pronoun_fr(g)} de plus {_que(friend)} ?",
            f"{who} has **{a}** {n_en}. {friend} has **{b}**. How many more does {who} have than {friend}?",
            a - b, [f'{a} − {b} = {a - b}', f'{a - b} de plus'], [f'{a} − {b} = {a - b}', f'{a - b} more'],
            'Combien faut-il ajouter au plus petit nombre pour arriver au plus grand ?', 'How many must you add to the smaller number to reach the bigger one?')
    start = random.randint(top // 5, top // 2)
    plus = random.randint(1, top - start - 1) if grade <= 1 else random.randint(5, top - start - 1)
    minus = random.randint(1, start + plus - 1)
    end = start + plus - minus
    if variant == 'missing_start':
        return _problem(
            f"{who} avait des {n_fr}. {_cap(sc.pronoun_fr(g))} en reçoit **{plus}**. Maintenant, {sc.pronoun_fr(g)} en a **{start + plus}**. Combien en avait-{sc.pronoun_fr(g)} au début ?",
            f"{who} had some {n_en}. {_cap(sc.pronoun_en(g))} gets **{plus}** more. Now {sc.pronoun_en(g)} has **{start + plus}**. How many did {sc.pronoun_en(g)} have at the start?",
            start, [f'{start + plus} − {plus} = {start}', f'{start} {n_fr}'], [f'{start + plus} − {plus} = {start}', f'{start} {n_en}'],
            'Recule : enlève ce qui a été reçu.', 'Go backwards: take away what was received.')
    order = variant == 'get_give'
    s_fr = (f"{_cap(sc.pronoun_fr(g))} en reçoit **{plus}**, puis en donne **{minus}**." if order
            else f"{_cap(sc.pronoun_fr(g))} en donne **{minus}**, puis en reçoit **{plus}**.")
    s_en = (f"{_cap(sc.pronoun_en(g))} gets **{plus}** more, then gives away **{minus}**." if order
            else f"{_cap(sc.pronoun_en(g))} gives away **{minus}**, then gets **{plus}** more.")
    if not order and minus > start:
        minus = random.randint(1, start)
        end = start + plus - minus
        s_fr = f"{_cap(sc.pronoun_fr(g))} en donne **{minus}**, puis en reçoit **{plus}**."
        s_en = f"{_cap(sc.pronoun_en(g))} gives away **{minus}**, then gets **{plus}** more."
    mid = start + plus if order else start - minus
    st = [f'{start} + {plus} = {mid}', f'{mid} − {minus} = {end}'] if order else [f'{start} − {minus} = {mid}', f'{mid} + {plus} = {end}']
    return _problem(
        f"{who} a **{start}** {n_fr}. {s_fr} Combien en a-t-{sc.pronoun_fr(g)} maintenant ?",
        f"{who} has **{start}** {n_en}. {s_en} How many does {sc.pronoun_en(g)} have now?",
        end, st + [f'{end} {n_fr}'], st + [f'{end} {n_en}'],
        'Fais une étape à la fois, dans l’ordre de l’histoire.', 'Do one step at a time, in the order of the story.')


# ─────────────────────────────────────────────────────────────────────────────
# Grade 4 operations
# ─────────────────────────────────────────────────────────────────────────────

def rows_groups(grade):
    who, g = sc.pick_actor()
    rows, per = random.randint(3, 9), random.randint(4, 12)
    total = rows * per
    variant = random.choice(['chairs', 'missing_rows', 'stickers'])
    if variant == 'chairs':
        empty = random.randint(1, total // 3)
        return _problem(
            f"Pour le spectacle, on installe **{rows}** rangées de **{per}** chaises. **{empty}** chaises restent vides. Combien de personnes sont assises ?",
            f"For the show, **{rows}** rows of **{per}** chairs are set up. **{empty}** chairs stay empty. How many people are sitting?",
            total - empty, [f'{rows} × {per} = {total} chaises', f'{total} − {empty} = {total - empty}', f'{total - empty} personnes'],
            [f'{rows} × {per} = {total} chairs', f'{total} − {empty} = {total - empty}', f'{total - empty} people'],
            'Trouve d’abord le nombre de chaises (rangées × chaises par rangée).', 'First find the number of chairs (rows × chairs per row).')
    if variant == 'missing_rows':
        return _problem(
            f"{who} plante **{total}** fleurs en rangées de **{per}**. Combien de rangées obtient-{sc.pronoun_fr(g)} ?",
            f"{who} plants **{total}** flowers in rows of **{per}**. How many rows does {sc.pronoun_en(g)} get?",
            rows, [f'? × {per} = {total}', f'{total} ÷ {per} = {rows}', f'{rows} rangées'], [f'? × {per} = {total}', f'{total} ÷ {per} = {rows}', f'{rows} rows'],
            'Quel nombre multiplié par la taille d’une rangée donne le total ?', 'Which number times the size of a row gives the total?')
    give = random.randint(1, per)
    return _problem(
        f"L’album {sc.de(who)} a **{rows}** pages de **{per}** autocollants. {_cap(sc.pronoun_fr(g))} en donne **{give}** à son frère. Combien lui en reste-t-il ?",
        f"{who}'s album has **{rows}** pages of **{per}** stickers. {_cap(sc.pronoun_en(g))} gives **{give}** to {sc.possessive_en(g)} brother. How many are left?",
        total - give, [f'{rows} × {per} = {total}', f'{total} − {give} = {total - give}', f'{total - give} autocollants'],
        [f'{rows} × {per} = {total}', f'{total} − {give} = {total - give}', f'{total - give} stickers'],
        'Multiplie, puis soustrais ce qui est donné.', 'Multiply, then subtract what is given away.')


def remainder_trips(grade):
    size = random.choice([6, 8, 9, 12, 15])
    q = random.randint(3, 9)
    r = random.randint(1, size - 1)
    total = q * size + r
    variant = random.choice(['round_up', 'round_down', 'left'])
    if variant == 'round_up':
        return _problem(
            f"**{total}** élèves partent en sortie. Chaque minibus transporte **{size}** élèves. Combien de minibus faut-il pour que tout le monde parte ?",
            f"**{total}** students go on a field trip. Each minibus carries **{size}** students. How many minibuses are needed so everyone can go?",
            q + 1, [f'{total} ÷ {size} = {q} reste {r}', f'Les {r} élèves qui restent ont besoin d’un minibus de plus : {q} + 1 = {q + 1}', f'{q + 1} minibus'],
            [f'{total} ÷ {size} = {q} remainder {r}', f'The {r} students left over need one more minibus: {q} + 1 = {q + 1}', f'{q + 1} minibuses'],
            'Divise. S’il y a un reste, il faut un véhicule de plus.', 'Divide. If there is a remainder, you need one more vehicle.')
    if variant == 'round_down':
        return _problem(
            f"Une boulangère a **{total}** muffins. Elle remplit des boîtes de **{size}**. Combien de boîtes **pleines** peut-elle faire ?",
            f"A baker has **{total}** muffins. She fills boxes of **{size}**. How many **full** boxes can she make?",
            q, [f'{total} ÷ {size} = {q} reste {r}', f'Le reste ({r}) ne remplit pas une boîte', f'{q} boîtes pleines'],
            [f'{total} ÷ {size} = {q} remainder {r}', f'The remainder ({r}) does not fill a box', f'{q} full boxes'],
            'Seules les boîtes complètes comptent : on ignore le reste.', 'Only complete boxes count: ignore the remainder.')
    return _problem(
        f"On partage **{total}** cartes également entre **{size}** amis. Chacun en reçoit le plus possible. Combien de cartes reste-t-il ?",
        f"**{total}** cards are shared equally among **{size}** friends. Each gets as many as possible. How many cards are left over?",
        r, [f'{size} × {q} = {size * q}', f'{total} − {size * q} = {r}', f'{r} carte{"s" if r > 1 else ""}'], [f'{size} × {q} = {size * q}', f'{total} − {size * q} = {r}', f'{r} card{"s" if r > 1 else ""}'],
        'Le reste est ce qui ne peut pas être partagé également.', 'The remainder is what cannot be shared equally.')


def plant_growth(grade):
    who, g = sc.pick_actor()
    h = [random.randint(2, 6)]
    for _ in range(4):
        h.append(h[-1] + random.randint(1, 7))
    weeks = ', '.join(f'sem. {i + 1} : **{v} cm**' for i, v in enumerate(h))
    weeks_en = ', '.join(f'week {i + 1}: **{v} cm**' for i, v in enumerate(h))
    story_fr = f"{who} mesure son plant de haricot chaque semaine ({weeks})."
    story_en = f"{who} measures {sc.possessive_en(g)} bean plant every week ({weeks_en})."
    variant = random.choice(['total', 'best_week', 'predict'])
    if variant == 'total':
        return _problem(
            f"{story_fr} De combien de centimètres a-t-il grandi entre la semaine 1 et la semaine 5 ?",
            f"{story_en} How many centimetres did it grow between week 1 and week 5?",
            h[4] - h[0], [f'{h[4]} − {h[0]} = {h[4] - h[0]}', f'{h[4] - h[0]} cm'], [f'{h[4]} − {h[0]} = {h[4] - h[0]}', f'{h[4] - h[0]} cm'],
            'Soustrais la première mesure de la dernière.', 'Subtract the first measurement from the last.')
    if variant == 'best_week':
        gains = [h[i + 1] - h[i] for i in range(4)]
        best = max(gains)
        return _problem(
            f"{story_fr} Quelle est la plus forte hausse en une seule semaine (en cm) ?",
            f"{story_en} What is the biggest increase in a single week (in cm)?",
            best, ['Hausses : ' + ', '.join(map(str, gains)), f'La plus grande : {best}', f'{best} cm'],
            ['Increases: ' + ', '.join(map(str, gains)), f'The biggest: {best}', f'{best} cm'],
            'Calcule la hausse d’une semaine à l’autre : c’est la partie la plus raide du diagramme à ligne brisée.',
            'Work out the increase from one week to the next: it is the steepest part of the line graph.')
    step = random.randint(2, 6)
    base = random.randint(2, 8)
    h = [base + step * i for i in range(4)]
    return _problem(
        f"Le plant {sc.de(who)} mesure **{h[0]} cm**, **{h[1]} cm**, **{h[2]} cm** puis **{h[3]} cm** au fil des semaines. S’il continue de grandir de la même façon, combien mesurera-t-il à la semaine 6 ?",
        f"{who}'s plant measures **{h[0]} cm**, **{h[1]} cm**, **{h[2]} cm** then **{h[3]} cm** over the weeks. If it keeps growing the same way, how tall will it be in week 6?",
        h[3] + 2 * step, [f'Il grandit de {step} cm par semaine', f'{h[3]} + {step} + {step} = {h[3] + 2 * step}', f'{h[3] + 2 * step} cm'],
        [f'It grows {step} cm per week', f'{h[3]} + {step} + {step} = {h[3] + 2 * step}', f'{h[3] + 2 * step} cm'],
        'Trouve la hausse régulière, puis prolonge la ligne de deux semaines.', 'Find the steady increase, then extend the line by two weeks.')


# ─────────────────────────────────────────────────────────────────────────────
# Measurement
# ─────────────────────────────────────────────────────────────────────────────

def ribbon(grade):
    who, g = sc.pick_actor()
    if grade <= 3:
        variant = random.choice(['cut', 'mm_total', 'join'])
        if variant == 'cut':
            piece = random.choice([5, 10, 12, 15, 20, 25])
            n = random.randint(2, 100 // piece - 1)
            return _problem(
                f"{who} a un ruban de **1 m**. {_cap(sc.pronoun_fr(g))} coupe **{n}** morceaux de **{piece} cm**. Combien de centimètres de ruban reste-t-il ?",
                f"{who} has a ribbon **1 m** long. {_cap(sc.pronoun_en(g))} cuts **{n}** pieces of **{piece} cm**. How many centimetres of ribbon are left?",
                100 - n * piece, ['1 m = 100 cm', f'{n} × {piece} = {n * piece} cm', f'100 − {n * piece} = {100 - n * piece}', f'{100 - n * piece} cm'],
                ['1 m = 100 cm', f'{n} × {piece} = {n * piece} cm', f'100 − {n * piece} = {100 - n * piece}', f'{100 - n * piece} cm'],
                'Commence par écrire 1 m en centimètres.', 'Start by writing 1 m in centimetres.')
        if variant == 'mm_total':
            cm, mm = random.randint(6, 18), random.randint(1, 9)
            return _problem(
                f"Le crayon {sc.de(who)} mesure **{cm} cm {mm} mm**. Combien de millimètres cela fait-il ?",
                f"{who}'s pencil is **{cm} cm {mm} mm** long. How many millimetres is that?",
                cm * 10 + mm, ['1 cm = 10 mm', f'{cm} × 10 = {cm * 10} mm', f'{cm * 10} + {mm} = {cm * 10 + mm}', f'{cm * 10 + mm} mm'],
                ['1 cm = 10 mm', f'{cm} × 10 = {cm * 10} mm', f'{cm * 10} + {mm} = {cm * 10 + mm}', f'{cm * 10 + mm} mm'],
                'Chaque centimètre contient 10 millimètres.', 'Each centimetre holds 10 millimetres.')
        a, b = random.randint(15, 45), random.randint(15, 45)
        lap = random.choice([2, 3, 5])
        return _problem(
            f"{who} colle deux bandes de papier de **{a} cm** et **{b} cm** en les faisant chevaucher de **{lap} cm**. Quelle est la longueur de la grande bande ?",
            f"{who} glues two paper strips of **{a} cm** and **{b} cm**, overlapping them by **{lap} cm**. How long is the big strip?",
            a + b - lap, [f'{a} + {b} = {a + b}', f'{a + b} − {lap} = {a + b - lap} (le chevauchement compte une seule fois)', f'{a + b - lap} cm'],
            [f'{a} + {b} = {a + b}', f'{a + b} − {lap} = {a + b - lap} (the overlap only counts once)', f'{a + b - lap} cm'],
            'Additionne, puis enlève la partie qui se chevauche.', 'Add, then take away the part that overlaps.')
    variant = random.choice(['laps', 'pieces', 'diff'])
    if variant == 'laps':
        lap = random.choice([250, 400, 500, 800])
        n = random.randint(3, 9)
        m = n * lap
        return _problem(
            f"{who} court **{n}** tours d’une piste de **{lap} m**. Combien de kilomètres et de mètres a-t-{sc.pronoun_fr(g)} parcourus ? Donne la réponse en mètres.",
            f"{who} runs **{n}** laps of a **{lap} m** track. How far did {sc.pronoun_en(g)} run? Give the answer in metres.",
            m, [f'{n} × {lap} = {N(m)} m', f'= {m // 1000} km {m % 1000} m', f'{N(m)} m'], [f'{n} × {lap} = {N(m)} m', f'= {m // 1000} km {m % 1000} m', f'{N(m)} m'],
            'Multiplie la longueur d’un tour par le nombre de tours.', 'Multiply the length of one lap by the number of laps.')
    if variant == 'pieces':
        total_m = random.randint(3, 9)
        piece = random.choice([20, 25, 40, 50])
        return _problem(
            f"Une couturière a **{total_m} m** de tissu. Elle coupe des bandes de **{piece} cm**. Combien de bandes obtient-elle ?",
            f"A dressmaker has **{total_m} m** of fabric. She cuts strips **{piece} cm** long. How many strips does she get?",
            total_m * 100 // piece, [f'{total_m} m = {total_m * 100} cm', f'{total_m * 100} ÷ {piece} = {total_m * 100 // piece}', f'{total_m * 100 // piece} bandes'],
            [f'{total_m} m = {total_m * 100} cm', f'{total_m * 100} ÷ {piece} = {total_m * 100 // piece}', f'{total_m * 100 // piece} strips'],
            'Mets les deux longueurs dans la même unité avant de diviser.', 'Put both lengths in the same unit before dividing.')
    a_m, a_cm = random.randint(1, 2), random.randint(5, 95)
    b_cm = random.randint(80, 99)
    a = a_m * 100 + a_cm
    return _problem(
        f"{who} saute **{a_m} m {a_cm} cm** en longueur. Son ami saute **{b_cm} cm**. Combien de centimètres de plus {who} a-t-{sc.pronoun_fr(g)} sautés ?",
        f"{who} jumps **{a_m} m {a_cm} cm** in the long jump. A friend jumps **{b_cm} cm**. How many more centimetres did {who} jump?",
        a - b_cm, [f'{a_m} m {a_cm} cm = {a} cm', f'{a} − {b_cm} = {a - b_cm}', f'{a - b_cm} cm'], [f'{a_m} m {a_cm} cm = {a} cm', f'{a} − {b_cm} = {a - b_cm}', f'{a - b_cm} cm'],
        'Convertis tout en centimètres, puis soustrais.', 'Convert everything to centimetres, then subtract.')


def tiling(grade):
    who, g = sc.pick_actor()
    w, h = random.randint(3, 9), random.randint(3, 8)
    if grade <= 3:
        variant = random.choice(['left', 'two_rooms'])
        if variant == 'left':
            done = random.randint(1, w * h - 1)
            return _problem(
                f"Le plancher d’une cabane est un rectangle de **{w}** tuiles sur **{h}** tuiles. {who} a déjà posé **{done}** tuiles. Combien de tuiles reste-t-il à poser ?",
                f"A shed floor is a rectangle **{w}** tiles by **{h}** tiles. {who} has already laid **{done}** tiles. How many tiles are left to lay?",
                w * h - done, [f'{w} × {h} = {w * h} tuiles en tout', f'{w * h} − {done} = {w * h - done}', f'{w * h - done} tuiles'],
                [f'{w} × {h} = {w * h} tiles in all', f'{w * h} − {done} = {w * h - done}', f'{w * h - done} tiles'],
                'Compte les carrés d’une rangée, multiplie par le nombre de rangées.', 'Count the squares in one row, multiply by the number of rows.')
        w2, h2 = random.randint(2, 6), random.randint(2, 6)
        return _problem(
            f"Deux tapis carrelés : l’un fait **{w} × {h}** carreaux, l’autre **{w2} × {h2}** carreaux. Combien de carreaux y a-t-il en tout ?",
            f"Two tiled mats: one is **{w} × {h}** squares, the other **{w2} × {h2}** squares. How many squares are there in all?",
            w * h + w2 * h2, [f'{w} × {h} = {w * h}', f'{w2} × {h2} = {w2 * h2}', f'{w * h} + {w2 * h2} = {w * h + w2 * h2}', f'{w * h + w2 * h2} carreaux'],
            [f'{w} × {h} = {w * h}', f'{w2} × {h2} = {w2 * h2}', f'{w * h} + {w2 * h2} = {w * h + w2 * h2}', f'{w * h + w2 * h2} squares'],
            'Calcule l’aire de chaque tapis, puis additionne.', 'Find the area of each mat, then add.')
    variant = random.choice(['cost', 'missing_side', 'garden_path'])
    if variant == 'cost':
        price = random.choice([8, 12, 15, 20, 25])
        return _problem(
            f"Une chambre rectangulaire mesure **{w} m** sur **{h} m**. Le tapis coûte **{price} $ le m²**. Combien coûte le tapis pour toute la chambre ?",
            f"A rectangular bedroom measures **{w} m** by **{h} m**. Carpet costs **${price} per m²**. How much does carpet for the whole room cost?",
            w * h * price, [f'Aire : {w} × {h} = {w * h} m²', f'{w * h} × {price} = {w * h * price}', f'{w * h * price} $'],
            [f'Area: {w} × {h} = {w * h} m²', f'{w * h} × {price} = {w * h * price}', f'${w * h * price}'],
            'Aire du rectangle, puis multiplie par le prix d’un mètre carré.', 'Area of the rectangle, then multiply by the price of one square metre.',
            'money', [f'{w * h * price} $', str(w * h * price)])
    if variant == 'missing_side':
        return _problem(
            f"Une affiche rectangulaire a une aire de **{N(w * h * 100)} cm²**. Sa largeur est **{w * 10} cm**. Quelle est sa longueur ?",
            f"A rectangular poster has an area of **{N(w * h * 100)} cm²**. Its width is **{w * 10} cm**. What is its length?",
            h * 10, [f'longueur × {w * 10} = {w * h * 100}', f'{w * h * 100} ÷ {w * 10} = {h * 10}', f'{h * 10} cm'],
            [f'length × {w * 10} = {w * h * 100}', f'{w * h * 100} ÷ {w * 10} = {h * 10}', f'{h * 10} cm'],
            'Aire = longueur × largeur, donc longueur = aire ÷ largeur.', 'Area = length × width, so length = area ÷ width.')
    W, H = w + 4, h + 4
    return _problem(
        f"Un jardin rectangulaire de **{W} m** sur **{H} m** contient un bassin rectangulaire de **{w} m** sur **{h} m**. Quelle est l’aire du jardin sans le bassin ?",
        f"A rectangular garden **{W} m** by **{H} m** contains a rectangular pond **{w} m** by **{h} m**. What is the area of the garden without the pond?",
        W * H - w * h, [f'Jardin : {W} × {H} = {W * H} m²', f'Bassin : {w} × {h} = {w * h} m²', f'{W * H} − {w * h} = {W * H - w * h}', f'{W * H - w * h} m²'],
        [f'Garden: {W} × {H} = {W * H} m²', f'Pond: {w} × {h} = {w * h} m²', f'{W * H} − {w * h} = {W * H - w * h}', f'{W * H - w * h} m²'],
        'Aire du grand rectangle moins aire du petit.', 'Area of the big rectangle minus area of the small one.')


def cube_boxes(grade):
    who, g = sc.pick_actor()
    l, w, h = random.randint(2, 5), random.randint(2, 4), random.randint(2, 4)
    if grade <= 3:
        variant = random.choice(['count', 'layers_done'])
        if variant == 'count':
            return _problem(
                f"{who} remplit une boîte avec des petits cubes. Une couche contient **{l}** rangées de **{w}** cubes. La boîte a **{h}** couches. Combien de cubes faut-il ?",
                f"{who} fills a box with small cubes. One layer has **{l}** rows of **{w}** cubes. The box has **{h}** layers. How many cubes are needed?",
                l * w * h, [f'Une couche : {l} × {w} = {l * w}', f'{l * w} × {h} = {l * w * h}', f'{l * w * h} cubes'],
                [f'One layer: {l} × {w} = {l * w}', f'{l * w} × {h} = {l * w * h}', f'{l * w * h} cubes'],
                'Compte les cubes d’une couche, puis multiplie par le nombre de couches.', 'Count the cubes in one layer, then multiply by the number of layers.')
        done = random.randint(1, h - 1)
        return _problem(
            f"Une boîte contient **{h}** couches de **{l} × {w}** cubes une fois pleine. {who} a déjà rempli **{done}** couche{'s' if done > 1 else ''}. Combien de cubes manque-t-il ?",
            f"A box holds **{h}** layers of **{l} × {w}** cubes when full. {who} has already filled **{done}** layer{'s' if done > 1 else ''}. How many cubes are missing?",
            l * w * (h - done), [f'Une couche : {l} × {w} = {l * w}', f'Couches manquantes : {h} − {done} = {h - done}', f'{l * w} × {h - done} = {l * w * (h - done)}', f'{l * w * (h - done)} cubes'],
            [f'One layer: {l} × {w} = {l * w}', f'Layers missing: {h} − {done} = {h - done}', f'{l * w} × {h - done} = {l * w * (h - done)}', f'{l * w * (h - done)} cubes'],
            'Combien de couches manque-t-il ? Combien de cubes par couche ?', 'How many layers are missing? How many cubes per layer?')
    variant = random.choice(['litres', 'small_boxes', 'height'])
    L, W, H = random.choice([10, 20, 25, 30, 40]), random.choice([10, 20, 25]), random.choice([10, 20, 30])
    v = L * W * H
    if variant == 'litres' and v % 1000 == 0:
        return _problem(
            f"Un aquarium mesure **{L} cm** × **{W} cm** × **{H} cm**. Combien de litres d’eau faut-il pour le remplir ? (1 L = 1 000 cm³)",
            f"A fish tank measures **{L} cm** × **{W} cm** × **{H} cm**. How many litres of water fill it? (1 L = 1,000 cm³)",
            v // 1000, [f'{L} × {W} × {H} = {N(v)} cm³', f'{N(v)} ÷ 1 000 = {v // 1000}', f'{v // 1000} L'],
            [f'{L} × {W} × {H} = {N(v)} cm³', f'{N(v)} ÷ 1,000 = {v // 1000}', f'{v // 1000} L'],
            'Calcule le volume en cm³, puis convertis : 1 000 cm³ = 1 L.', 'Find the volume in cm³, then convert: 1,000 cm³ = 1 L.')
    if variant in ('litres', 'small_boxes'):
        a, b, c = random.randint(2, 5), random.randint(2, 4), random.randint(2, 4)
        s = random.choice([5, 10])
        return _problem(
            f"Un carton mesure **{a * s} cm** × **{b * s} cm** × **{c * s} cm**. Combien de cubes de **{s} cm** de côté peut-on y ranger ?",
            f"A carton measures **{a * s} cm** × **{b * s} cm** × **{c * s} cm**. How many cubes with **{s} cm** sides fit inside?",
            a * b * c, [f'Sur la longueur : {a * s} ÷ {s} = {a}, la largeur : {b}, la hauteur : {c}', f'{a} × {b} × {c} = {a * b * c}', f'{a * b * c} cubes'],
            [f'Along the length: {a * s} ÷ {s} = {a}, the width: {b}, the height: {c}', f'{a} × {b} × {c} = {a * b * c}', f'{a * b * c} cubes'],
            'Combien de cubes tiennent dans chaque direction ?', 'How many cubes fit in each direction?')
    return _problem(
        f"Une boîte a un volume de **{N(v)} cm³**. Sa base mesure **{L} cm** × **{W} cm**. Quelle est sa hauteur ?",
        f"A box has a volume of **{N(v)} cm³**. Its base measures **{L} cm** × **{W} cm**. What is its height?",
        H, [f'Aire de la base : {L} × {W} = {L * W} cm²', f'{N(v)} ÷ {L * W} = {H}', f'{H} cm'],
        [f'Base area: {L} × {W} = {L * W} cm²', f'{N(v)} ÷ {L * W} = {H}', f'{H} cm'],
        'Volume = aire de la base × hauteur.', 'Volume = base area × height.')


def balance(grade):
    variant = random.choice(['same_objects', 'two_sides', 'cups'])
    if variant == 'same_objects':
        n = random.randint(2, 5)
        one = random.choice([50, 100, 150, 200, 250])
        return _problem(
            f"Sur une balance, **{n}** pommes identiques font l’équilibre avec un melon de **{N(n * one)} g**. Quelle est la masse d’une pomme ?",
            f"On a balance, **{n}** identical apples balance a melon of **{N(n * one)} g**. What is the mass of one apple?",
            one, [f'{n} pommes = {N(n * one)} g', f'{N(n * one)} ÷ {n} = {one}', f'{one} g'], [f'{n} apples = {n * one} g', f'{n * one} ÷ {n} = {one}', f'{one} g'],
            'Les deux plateaux ont la même masse : partage-la entre les pommes.', 'Both pans have the same mass: share it among the apples.')
    if variant == 'two_sides':
        a, b = random.choice([100, 200, 500]), random.choice([50, 100, 200])
        extra = random.randint(1, (a + b) // 50 - 1) * 50
        return _problem(
            f"Sur le plateau de gauche : une masse de **{a} g** et une de **{b} g**. Sur le plateau de droite : un sac de farine de **{a + b - extra} g**. Combien de grammes faut-il ajouter à droite pour l’équilibre ?",
            f"On the left pan: a **{a} g** mass and a **{b} g** mass. On the right pan: a bag of flour of **{a + b - extra} g**. How many grams must be added on the right to balance?",
            extra, [f'Gauche : {a} + {b} = {a + b} g', f'{a + b} − {a + b - extra} = {extra}', f'{extra} g'],
            [f'Left: {a} + {b} = {a + b} g', f'{a + b} − {a + b - extra} = {extra}', f'{extra} g'],
            'Calcule la masse de chaque plateau, puis la différence.', 'Find the mass on each pan, then the difference.')
    jug = random.choice([1, 2, 3])
    cup = random.choice([100, 200, 250, 500])
    return _problem(
        f"Un pichet contient **{jug} L** de jus. On le verse dans des verres de **{cup} mL**. Combien de verres peut-on remplir ?",
        f"A jug holds **{jug} L** of juice. It is poured into **{cup} mL** glasses. How many glasses can be filled?",
        jug * 1000 // cup, [f'{jug} L = {N(jug * 1000)} mL', f'{N(jug * 1000)} ÷ {cup} = {jug * 1000 // cup}', f'{jug * 1000 // cup} verres'],
        [f'{jug} L = {N(jug * 1000)} mL', f'{N(jug * 1000)} ÷ {cup} = {jug * 1000 // cup}', f'{jug * 1000 // cup} glasses'],
        '1 L = 1 000 mL. Convertis avant de diviser.', '1 L = 1,000 mL. Convert before dividing.')


# ─────────────────────────────────────────────────────────────────────────────
# Grade 6 geometry
# ─────────────────────────────────────────────────────────────────────────────

def angles(grade):
    variant = random.choice(['triangle', 'isosceles', 'straight', 'clock'])
    if variant == 'triangle':
        a = random.randint(25, 100)
        b = random.randint(20, 150 - a)
        c = 180 - a - b
        return _problem(
            f"Dans un triangle, deux angles mesurent **{a}°** et **{b}°**. Combien mesure le troisième angle ?",
            f"In a triangle, two angles measure **{a}°** and **{b}°**. What does the third angle measure?",
            c, ['La somme des angles d’un triangle est 180°', f'{a} + {b} = {a + b}', f'180 − {a + b} = {c}', f'{c}°'],
            ['The angles of a triangle add up to 180°', f'{a} + {b} = {a + b}', f'180 − {a + b} = {c}', f'{c}°'],
            'Les trois angles d’un triangle font toujours 180° ensemble.', 'The three angles of a triangle always add up to 180°.')
    if variant == 'isosceles':
        top = random.choice([20, 30, 40, 50, 60, 70, 80, 90, 100, 120])
        base = (180 - top) // 2
        return _problem(
            f"Un triangle isocèle a un angle au sommet de **{top}°**. Les deux autres angles sont égaux. Combien mesure chacun d’eux ?",
            f"An isosceles triangle has a top angle of **{top}°**. The other two angles are equal. What does each of them measure?",
            base, [f'180 − {top} = {180 - top}', f'{180 - top} ÷ 2 = {base}', f'{base}°'], [f'180 − {top} = {180 - top}', f'{180 - top} ÷ 2 = {base}', f'{base}°'],
            'Enlève l’angle connu de 180°, puis partage en deux.', 'Take the known angle away from 180°, then split in two.')
    if variant == 'straight':
        a = random.randint(15, 165)
        return _problem(
            f"Deux angles côte à côte forment une ligne droite. L’un mesure **{a}°**. Combien mesure l’autre ?",
            f"Two angles side by side make a straight line. One measures **{a}°**. What does the other measure?",
            180 - a, ['Un angle plat mesure 180°', f'180 − {a} = {180 - a}', f'{180 - a}°'], ['A straight angle measures 180°', f'180 − {a} = {180 - a}', f'{180 - a}°'],
            'Une ligne droite forme un angle de 180°.', 'A straight line makes an angle of 180°.')
    hr = random.choice([1, 2, 3, 4, 5])
    return _problem(
        f"Il est **{hr} h** pile. Quel angle forment les aiguilles de l’horloge ?",
        f"It is exactly **{hr} o’clock**. What angle do the clock hands make?",
        hr * 30, ['Le tour complet (360°) est partagé en 12 heures : 360 ÷ 12 = 30° par heure', f'{hr} × 30 = {hr * 30}', f'{hr * 30}°'],
        ['The full turn (360°) is shared among 12 hours: 360 ÷ 12 = 30° per hour', f'{hr} × 30 = {hr * 30}', f'{hr * 30}°'],
        'Combien de degrés entre deux nombres voisins de l’horloge ?', 'How many degrees between two neighbouring numbers on the clock?')


def circles(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['wheel', 'coins', 'square_box', 'radius_from'])
    if variant == 'wheel':
        r = random.randint(8, 35)
        return _problem(
            f"Le rayon de la roue du vélo {sc.de(who)} est **{r} cm**. Quel est son diamètre ?",
            f"The radius of {who}'s bike wheel is **{r} cm**. What is its diameter?",
            2 * r, ['Diamètre = 2 × rayon', f'2 × {r} = {2 * r}', f'{2 * r} cm'], ['Diameter = 2 × radius', f'2 × {r} = {2 * r}', f'{2 * r} cm'],
            'Le diamètre traverse le cercle en passant par le centre : il vaut deux rayons.', 'The diameter crosses the circle through the centre: it is two radii.')
    if variant == 'coins':
        r, n = random.randint(1, 4), random.randint(3, 8)
        return _problem(
            f"{who} aligne **{n}** jetons ronds de **{r} cm** de rayon, bord contre bord. Quelle est la longueur de la rangée ?",
            f"{who} lines up **{n}** round tokens with a **{r} cm** radius, edge to edge. How long is the row?",
            2 * r * n, [f'Diamètre d’un jeton : 2 × {r} = {2 * r} cm', f'{n} × {2 * r} = {2 * r * n}', f'{2 * r * n} cm'],
            [f'Diameter of one token: 2 × {r} = {2 * r} cm', f'{n} × {2 * r} = {2 * r * n}', f'{2 * r * n} cm'],
            'Chaque jeton occupe la longueur de son diamètre.', 'Each token takes up the length of its diameter.')
    if variant == 'square_box':
        r = random.randint(5, 20)
        return _problem(
            f"Une pizza ronde de **{r} cm** de rayon tient tout juste dans une boîte carrée. Quel est le périmètre du fond de la boîte ?",
            f"A round pizza with a **{r} cm** radius fits exactly in a square box. What is the perimeter of the bottom of the box?",
            8 * r, [f'Côté de la boîte = diamètre = 2 × {r} = {2 * r} cm', f'4 × {2 * r} = {8 * r}', f'{8 * r} cm'],
            [f'Side of the box = diameter = 2 × {r} = {2 * r} cm', f'4 × {2 * r} = {8 * r}', f'{8 * r} cm'],
            'Le côté du carré est égal au diamètre de la pizza.', 'The side of the square equals the pizza’s diameter.')
    d = 2 * random.randint(5, 40)
    return _problem(
        f"Une table ronde a un diamètre de **{d} cm**. On place un vase au centre. À quelle distance du bord se trouve-t-il ?",
        f"A round table has a diameter of **{d} cm**. A vase is placed at the centre. How far is it from the edge?",
        d // 2, ['La distance du centre au bord est le rayon', f'{d} ÷ 2 = {d // 2}', f'{d // 2} cm'], ['The distance from the centre to the edge is the radius', f'{d} ÷ 2 = {d // 2}', f'{d // 2} cm'],
        'Rayon = diamètre ÷ 2.', 'Radius = diameter ÷ 2.')


# ─────────────────────────────────────────────────────────────────────────────
# Decimals, fractions, percent
# ─────────────────────────────────────────────────────────────────────────────

def decimal_measures(grade):
    who, g = sc.pick_actor()
    friend = random.choice([x for x in sc.ACTORS if x[0] != who])[0]
    variants = ['gap', 'total', 'round'] + (['packs'] if grade >= 5 else [])
    variant = random.choice(variants)
    if variant == 'gap':
        a = random.randint(105, 199)          # tenths of a second
        b = a + random.randint(3, 40)
        fa, fb, d = a / 10, b / 10, (b - a) / 10
        return _problem(
            f"Au 50 m, {who} fait **{_d(fa, 1, 'fr')} s** et {friend} **{_d(fb, 1, 'fr')} s**. Combien de secondes {who} a-t-{sc.pronoun_fr(g)} d’avance ?",
            f"In the 50 m race, {who} runs **{_d(fa, 1, 'en')} s** and {friend} **{_d(fb, 1, 'en')} s**. By how many seconds is {who} ahead?",
            _d(d, 1, 'fr'), [f'{_d(fb, 1, "fr")} − {_d(fa, 1, "fr")} = {_d(d, 1, "fr")}', f'{_d(d, 1, "fr")} s'], [f'{_d(fb, 1, "en")} − {_d(fa, 1, "en")} = {_d(d, 1, "en")}', f'{_d(d, 1, "en")} s'],
            'Aligne les virgules, puis soustrais.', 'Line up the decimal points, then subtract.', 'decimal', _dec_answers(d, 1))
    if variant == 'total':
        jumps = [random.randint(150, 320) for _ in range(3)]       # centimetres → metres with 2 decimals
        tot = sum(jumps)
        fs = [j / 100 for j in jumps]
        return _problem(
            f"{who} fait trois sauts de **{_d(fs[0], 2, 'fr')} m**, **{_d(fs[1], 2, 'fr')} m** et **{_d(fs[2], 2, 'fr')} m**. Quelle distance totale a-t-{sc.pronoun_fr(g)} sautée ?",
            f"{who} makes three jumps of **{_d(fs[0], 2, 'en')} m**, **{_d(fs[1], 2, 'en')} m** and **{_d(fs[2], 2, 'en')} m**. What total distance did {sc.pronoun_en(g)} jump?",
            _d(tot / 100, 2, 'fr'), [' + '.join(_d(f, 2, 'fr') for f in fs) + f' = {_d(tot / 100, 2, "fr")}', f'{_d(tot / 100, 2, "fr")} m'],
            [' + '.join(_d(f, 2, 'en') for f in fs) + f' = {_d(tot / 100, 2, "en")}', f'{_d(tot / 100, 2, "en")} m'],
            'Aligne les virgules et additionne les centièmes, puis les dixièmes, puis les unités.', 'Line up the decimal points; add hundredths, then tenths, then ones.',
            'decimal', _dec_answers(tot / 100, 2))
    if variant == 'round':
        c = random.randint(101, 999)
        while c % 10 == 5:
            c = random.randint(101, 999)
        x = c / 100
        r = round(c / 10) / 10
        return _problem(
            f"La gourde {sc.de(who)} contient **{_d(x, 2, 'fr')} L** d’eau. Arrondis cette quantité au dixième de litre près.",
            f"{who}'s water bottle holds **{_d(x, 2, 'en')} L** of water. Round this amount to the nearest tenth of a litre.",
            _d(r, 1, 'fr'), [f'Chiffre des centièmes : {c % 10}', f'{"5 ou plus → on arrondit vers le haut" if c % 10 >= 5 else "moins de 5 → on garde le dixième"}', f'{_d(r, 1, "fr")} L'],
            [f'Hundredths digit: {c % 10}', f'{"5 or more → round up" if c % 10 >= 5 else "less than 5 → keep the tenth"}', f'{_d(r, 1, "en")} L'],
            'Regarde le chiffre juste après les dixièmes.', 'Look at the digit just after the tenths.', 'decimal', _dec_answers(r, 1))
    k = random.choice([10, 100, 1000])
    p = random.randint(105, 950)
    price = p / 100
    cents = p * k
    tot = cents / 100
    tot_s = N(cents // 100) if cents % 100 == 0 else _d(tot, 2, 'fr').rstrip('0')
    return _problem(
        f"Une gomme coûte **{_money_fr(price)}**. L’école en commande **{N(k)}**. Combien paie-t-elle ?",
        f"An eraser costs **{_money_en(price)}**. The school orders **{k:,}**. How much does it pay?",
        f'{cents / 100:.2f}', [f'{_d(price, 2, "fr")} × {N(k)} : la virgule se déplace de {len(str(k)) - 1} rang{"s" if k > 10 else ""} vers la droite', f'= {tot_s}', f'{_money_fr(tot)}'],
        [f'{_d(price, 2, "en")} × {k:,}: the decimal point moves {len(str(k)) - 1} place{"s" if k > 10 else ""} to the right', f'= {_d(tot, 2, "en").rstrip("0").rstrip(".")}', f'{_money_en(tot)}'],
        'Multiplier par 10, 100 ou 1 000 déplace la virgule de 1, 2 ou 3 rangs.', 'Multiplying by 10, 100 or 1,000 moves the decimal point 1, 2 or 3 places.',
        'money', _dec_answers(tot, 2) + [f'{_money_fr(tot)}'])


def fair_share(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['pizzas', 'set', 'which_more'])
    if variant == 'pizzas':
        kids = random.choice([3, 4, 5, 6, 8])
        piz = random.randint(1, kids - 1)
        fr = Fraction(piz, kids)
        return _problem(
            f"**{kids}** amis partagent également **{piz}** pizza{'s' if piz > 1 else ''}. Quelle fraction de pizza chacun reçoit-il ?",
            f"**{kids}** friends share **{piz}** pizza{'s' if piz > 1 else ''} equally. What fraction of a pizza does each one get?",
            _frac(fr), [f'{piz} ÷ {kids} = {piz}/{kids}', f'Chacun reçoit {_frac(fr)} de pizza'], [f'{piz} ÷ {kids} = {piz}/{kids}', f'Each one gets {_frac(fr)} of a pizza'],
            'Partager a objets entre b personnes donne a/b à chacun.', 'Sharing a things among b people gives a/b to each.', 'fraction', _frac_answers(fr, f'{piz}/{kids}'))
    if variant == 'set':
        d = random.choice([3, 4, 5, 6])
        n = random.randint(1, d - 1)
        tot = d * random.randint(3, 8)
        return _problem(
            f"Une classe compte **{tot}** élèves. **{n}/{d}** de la classe vient à l’école à vélo. Combien d’élèves ne viennent **pas** à vélo ?",
            f"A class has **{tot}** students. **{n}/{d}** of the class bikes to school. How many students do **not** bike?",
            tot - tot * n // d, [f'{tot} ÷ {d} = {tot // d}', f'{n} × {tot // d} = {tot * n // d} à vélo', f'{tot} − {tot * n // d} = {tot - tot * n // d}', f'{tot - tot * n // d} élèves'],
            [f'{tot} ÷ {d} = {tot // d}', f'{n} × {tot // d} = {tot * n // d} bike', f'{tot} − {tot * n // d} = {tot - tot * n // d}', f'{tot - tot * n // d} students'],
            'Trouve 1/d de la classe, puis n/d, puis le reste.', 'Find 1/d of the class, then n/d, then the rest.')
    a, b = random.sample([3, 4, 5, 6, 8], 2)
    p = random.randint(1, min(a, b) - 1)
    more = min(a, b)
    return _problem(
        f"Groupe A : **{a}** enfants se partagent **{p}** tarte{'s' if p > 1 else ''}. Groupe B : **{b}** enfants se partagent **{p}** tarte{'s' if p > 1 else ''}. Dans quel groupe chaque enfant mange-t-il le plus ? Donne le nombre d’enfants de ce groupe.",
        f"Group A: **{a}** children share **{p}** pie{'s' if p > 1 else ''}. Group B: **{b}** children share **{p}** pie{'s' if p > 1 else ''}. In which group does each child eat more? Give the number of children in that group.",
        more, [f'A : {p}/{a} chacun, B : {p}/{b} chacun', f'Même numérateur : le plus petit dénominateur donne la plus grande part', f'Le groupe de {more} enfants'],
        [f'A: {p}/{a} each, B: {p}/{b} each', 'Same numerator: the smaller denominator gives the bigger share', f'The group of {more} children'],
        'Moins il y a de personnes pour la même quantité, plus la part est grande.', 'The fewer people for the same amount, the bigger each share.')


def recipe_fractions(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['add_related', 'whole_times', 'eaten_simplest', 'left_related'])
    if variant in ('add_related', 'left_related'):
        d1 = random.choice([2, 3, 4, 5])
        k = random.choice([2, 3]) if d1 <= 4 else 2
        d2 = d1 * k
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        a, b = Fraction(n1, d1), Fraction(n2, d2)
        if variant == 'add_related':
            s = a + b
            return _problem(
                f"Pour une recette, {who} met **{n1}/{d1}** tasse de farine, puis **{n2}/{d2}** tasse de plus. Combien de tasses de farine en tout ?",
                f"For a recipe, {who} puts in **{n1}/{d1}** cup of flour, then **{n2}/{d2}** cup more. How many cups of flour in all?",
                _frac(s), [f'{n1}/{d1} = {n1 * k}/{d2}', f'{n1 * k}/{d2} + {n2}/{d2} = {n1 * k + n2}/{d2}', f'{_frac(s)} tasse(s)'],
                [f'{n1}/{d1} = {n1 * k}/{d2}', f'{n1 * k}/{d2} + {n2}/{d2} = {n1 * k + n2}/{d2}', f'{_frac(s)} cup(s)'],
                'Écris les deux fractions avec le même dénominateur, puis additionne les numérateurs.', 'Write both fractions with the same denominator, then add the numerators.',
                'fraction', _frac_answers(s, f'{n1 * k + n2}/{d2}'))
        if a <= b:                         # start from a whole litre so something is left
            a, have_fr, have_en = Fraction(1), '**1** litre', '**1** litre'
        else:
            have_fr = have_en = f'**{n1}/{d1}** litre'
        a_k = int(a * d2)
        left = a - b
        first = '1' if a == 1 else f'{n1}/{d1}'
        return _problem(
            f"{who} a {have_fr} de lait. {_cap(sc.pronoun_fr(g))} en utilise **{n2}/{d2}** litre pour des crêpes. Quelle fraction de litre reste-t-il ?",
            f"{who} has {have_en} of milk. {_cap(sc.pronoun_en(g))} uses **{n2}/{d2}** litre for pancakes. What fraction of a litre is left?",
            _frac(left), [f'{first} = {a_k}/{d2}', f'{a_k}/{d2} − {n2}/{d2} = {a_k - n2}/{d2}', f'{_frac(left)} L'],
            [f'{first} = {a_k}/{d2}', f'{a_k}/{d2} − {n2}/{d2} = {a_k - n2}/{d2}', f'{_frac(left)} L'],
            'Même dénominateur d’abord, puis soustrais les numérateurs.', 'Same denominator first, then subtract the numerators.',
            'fraction', _frac_answers(left, f'{a_k - n2}/{d2}'))
    if variant == 'whole_times':
        d = random.choice([2, 3, 4, 5, 8])
        n = random.randint(1, d - 1)
        times = random.randint(2, 9)
        p = Fraction(n * times, d)
        return _problem(
            f"Chaque jour, {who} boit **{n}/{d}** litre de lait. Combien de litres boit-{sc.pronoun_fr(g)} en **{times}** jours ?",
            f"Every day, {who} drinks **{n}/{d}** litre of milk. How many litres does {sc.pronoun_en(g)} drink in **{times}** days?",
            _frac(p), [f'{times} × {n}/{d} = {n * times}/{d}', f'= {_frac_answers(p)[-1] if len(_frac_answers(p)) > 1 else _frac(p)}', f'{_frac(p)} L'],
            [f'{times} × {n}/{d} = {n * times}/{d}', f'= {_frac_answers(p)[-1] if len(_frac_answers(p)) > 1 else _frac(p)}', f'{_frac(p)} L'],
            'Multiplie le numérateur par le nombre de jours ; le dénominateur ne change pas.', 'Multiply the numerator by the number of days; the denominator stays the same.',
            'fraction', _frac_answers(p, f'{n * times}/{d}'))
    d = random.choice([6, 8, 10, 12, 16])
    n = random.choice([x for x in range(2, d) if Fraction(x, d).denominator != d])
    fr = Fraction(n, d)
    return _problem(
        f"Une pizza est coupée en **{d}** parts égales. {who} et ses amis en mangent **{n}**. Quelle fraction de la pizza ont-ils mangée ? (fraction la plus simple)",
        f"A pizza is cut into **{d}** equal slices. {who} and friends eat **{n}** of them. What fraction of the pizza did they eat? (simplest fraction)",
        _frac(fr), [f'{n}/{d}', f'On divise en haut et en bas par {n // fr.numerator} : {_frac(fr)}', _frac(fr)],
        [f'{n}/{d}', f'Divide top and bottom by {n // fr.numerator}: {_frac(fr)}', _frac(fr)],
        'Écris parts mangées / parts en tout, puis simplifie.', 'Write slices eaten / total slices, then simplify.', 'fraction', _frac_answers(fr))


def percent_shop(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['discount', 'sale_price', 'class', 'to_percent'])
    pct = random.choice([10, 20, 25, 50, 75])
    price = random.choice([20, 40, 60, 80, 100, 120, 200])
    off = price * pct // 100
    if variant == 'discount':
        return _problem(
            f"Un jeu coûte **{price} $**. Il est en solde à **{pct} %** de rabais. De combien le prix baisse-t-il ?",
            f"A game costs **${price}**. It is on sale at **{pct}%** off. By how much does the price drop?",
            off, [f'{pct} % = {pct}/100', f'{pct}/100 × {price} = {off}', f'{off} $'], [f'{pct}% = {pct}/100', f'{pct}/100 × {price} = {off}', f'${off}'],
            '10 % est un dixième ; 25 % est un quart ; 50 % est la moitié.', '10% is one tenth; 25% is one quarter; 50% is one half.', 'money', [f'{off} $', str(off)])
    if variant == 'sale_price':
        return _problem(
            f"Un manteau coûte **{price} $**. {who} profite d’un rabais de **{pct} %**. Combien paie-t-{sc.pronoun_fr(g)} ?",
            f"A coat costs **${price}**. {who} gets a **{pct}%** discount. How much does {sc.pronoun_en(g)} pay?",
            price - off, [f'Rabais : {pct} % de {price} = {off} $', f'{price} − {off} = {price - off}', f'{price - off} $'],
            [f'Discount: {pct}% of {price} = ${off}', f'{price} − {off} = {price - off}', f'${price - off}'],
            'Calcule le rabais, puis enlève-le du prix.', 'Work out the discount, then take it off the price.', 'money', [f'{price - off} $', str(price - off)])
    if variant == 'class':
        tot = random.choice([20, 25, 40, 50, 100])
        pct = random.choice([p for p in (10, 20, 25, 40, 50, 60, 75, 80) if tot * p % 100 == 0])
        part = tot * pct // 100
        return _problem(
            f"Dans une école de **{tot}** élèves, **{pct} %** font partie d’une équipe sportive. Combien d’élèves **ne font pas** partie d’une équipe ?",
            f"In a school of **{tot}** students, **{pct}%** are on a sports team. How many students are **not** on a team?",
            tot - part, [f'{pct} % de {tot} = {part}', f'{tot} − {part} = {tot - part}', f'{tot - part} élèves'],
            [f'{pct}% of {tot} = {part}', f'{tot} − {part} = {tot - part}', f'{tot - part} students'],
            'Trouve d’abord combien font partie d’une équipe.', 'First find how many are on a team.')
    tot = random.choice([20, 25, 50])
    got = random.randint(1, tot - 1)
    p = got * 100 // tot
    return _problem(
        f"{who} réussit **{got}** questions sur **{tot}** à un test. Quel pourcentage de bonnes réponses a-t-{sc.pronoun_fr(g)} ?",
        f"{who} gets **{got}** questions out of **{tot}** right on a test. What percentage of correct answers is that?",
        p, [f'{got}/{tot} = {got * (100 // tot)}/100', f'= {p} %', f'{p} %'], [f'{got}/{tot} = {got * (100 // tot)}/100', f'= {p}%', f'{p}%'],
        'Écris la fraction sur 100 : le numérateur est le pourcentage.', 'Write the fraction out of 100: the numerator is the percentage.')


def teams(grade):
    variant = random.choice(['team_size', 'common_multiple', 'no_leftover_count'])
    if variant == 'team_size':
        size = random.choice([4, 5, 6, 7, 8, 9])
        total = size * random.randint(4, 12)
        options = [k for k in (4, 5, 6, 7, 8, 9) if k != size and total % k]
        wrong = random.choice(options) if options else None
        if wrong:
            return _problem(
                f"**{total}** élèves participent à un tournoi. Les équipes doivent être complètes. Peut-on faire des équipes de **{wrong}** ? Sinon, combien d’équipes de **{size}** obtient-on ?",
                f"**{total}** students join a tournament. Teams must be complete. Can teams of **{wrong}** be made? If not, how many teams of **{size}** do we get?",
                total // size, [f'{total} ÷ {wrong} = {total // wrong} reste {total % wrong} → impossible', f'{total} ÷ {size} = {total // size} reste 0', f'{total // size} équipes'],
                [f'{total} ÷ {wrong} = {total // wrong} remainder {total % wrong} → impossible', f'{total} ÷ {size} = {total // size} remainder 0', f'{total // size} teams'],
                'Un nombre est divisible si la division ne laisse aucun reste.', 'A number is divisible when the division leaves no remainder.')
        return _problem(
            f"**{total}** élèves forment des équipes complètes de **{size}**. Combien d’équipes y a-t-il ?",
            f"**{total}** students form complete teams of **{size}**. How many teams are there?",
            total // size, [f'{total} ÷ {size} = {total // size}', f'{total // size} équipes'], [f'{total} ÷ {size} = {total // size}', f'{total // size} teams'],
            'Divise le nombre d’élèves par la taille d’une équipe.', 'Divide the number of students by the size of a team.')
    if variant == 'common_multiple':
        a, b = random.choice([(2, 3), (3, 4), (4, 6), (6, 8), (4, 5), (3, 5), (6, 9), (2, 5)])
        from math import gcd
        l = a * b // gcd(a, b)
        return _problem(
            f"Des petits pains sont vendus par paquets de **{a}** et des saucisses par paquets de **{b}**. Quel est le plus petit nombre de hot-dogs qu’on peut faire sans qu’il reste rien ?",
            f"Buns come in packs of **{a}** and sausages in packs of **{b}**. What is the smallest number of hot dogs you can make with nothing left over?",
            l, [f'Multiples de {a} : ' + ', '.join(str(a * i) for i in range(1, l // a + 1)), f'Multiples de {b} : ' + ', '.join(str(b * i) for i in range(1, l // b + 1)), f'Le premier multiple commun est {l}', f'{l} hot-dogs'],
            [f'Multiples of {a}: ' + ', '.join(str(a * i) for i in range(1, l // a + 1)), f'Multiples of {b}: ' + ', '.join(str(b * i) for i in range(1, l // b + 1)), f'The first common multiple is {l}', f'{l} hot dogs'],
            'Écris les multiples de chaque nombre et cherche le premier en commun.', 'List the multiples of each number and look for the first one they share.')
    total = random.choice([12, 18, 20, 24, 30, 36])
    divs = [k for k in range(2, total) if total % k == 0]
    return _problem(
        f"Un enseignant veut ranger **{total}** pupitres en rangées égales, avec au moins 2 pupitres par rangée et au moins 2 rangées. Combien de façons différentes y a-t-il de choisir le nombre de rangées ?",
        f"A teacher wants to set **{total}** desks in equal rows, with at least 2 desks per row and at least 2 rows. How many different choices are there for the number of rows?",
        len(divs), [f'On cherche les diviseurs de {total} entre 2 et {total // 2}', ', '.join(f'{k} × {total // k}' for k in divs), f'{len(divs)} façons'],
        [f'Look for the divisors of {total} between 2 and {total // 2}', ', '.join(f'{k} × {total // k}' for k in divs), f'{len(divs)} ways'],
        'Chaque diviseur de ce nombre donne un nombre possible de rangées.', 'Each divisor of the number gives a possible number of rows.')


def powers_story(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['message', 'cube', 'square_garden'])
    if variant == 'message':
        b = random.choice([2, 3])
        days = random.randint(3, 5 if b == 3 else 6)
        val = b ** days
        return _problem(
            f"Le jour 1, {who} envoie un message à **{b}** amis. Le lendemain, chacun d’eux l’envoie à **{b}** nouveaux amis, et ainsi de suite. Combien de personnes reçoivent le message le jour **{days}** ?",
            f"On day 1, {who} sends a message to **{b}** friends. The next day, each of them sends it to **{b}** new friends, and so on. How many people get the message on day **{days}**?",
            val, [' → '.join(str(b ** i) for i in range(1, days + 1)), f'{b}{_SUP[days]} = ' + ' × '.join([str(b)] * days) + f' = {val}', f'{val} personnes'],
            [' → '.join(str(b ** i) for i in range(1, days + 1)), f'{b}{_SUP[days]} = ' + ' × '.join([str(b)] * days) + f' = {val}', f'{val} people'],
            f'Chaque jour, on multiplie par {b} : c’est une puissance de {b}.', f'Each day you multiply by {b}: it is a power of {b}.')
    if variant == 'cube':
        s = random.randint(2, 6)
        return _problem(
            f"{who} construit un grand cube avec des petits cubes. Chaque arête du grand cube compte **{s}** petits cubes. Combien de petits cubes lui faut-il ?",
            f"{who} builds a big cube from small cubes. Each edge of the big cube is **{s}** small cubes long. How many small cubes are needed?",
            s ** 3, [f'{s}³ = {s} × {s} × {s}', f'{s * s} × {s} = {s ** 3}', f'{s ** 3} petits cubes'], [f'{s}³ = {s} × {s} × {s}', f'{s * s} × {s} = {s ** 3}', f'{s ** 3} small cubes'],
            'Longueur × largeur × hauteur, toutes égales : c’est le cube du nombre.', 'Length × width × height, all equal: it is the number cubed.')
    s = random.randint(4, 15)
    border = random.randint(1, min(3, (s - 2) // 2))
    return _problem(
        f"Un potager carré a des côtés de **{s} m**. On garde une bande de **{border} m** de large tout autour pour marcher. Quelle est l’aire de la partie cultivée au centre ?",
        f"A square vegetable garden has **{s} m** sides. A **{border} m** strip is kept all around for walking. What is the area of the planted part in the middle?",
        (s - 2 * border) ** 2, [f'Côté du centre : {s} − 2 × {border} = {s - 2 * border} m', f'{s - 2 * border}² = {(s - 2 * border) ** 2}', f'{(s - 2 * border) ** 2} m²'],
        [f'Side of the middle: {s} − 2 × {border} = {s - 2 * border} m', f'{s - 2 * border}² = {(s - 2 * border) ** 2}', f'{(s - 2 * border) ** 2} m²'],
        'La bande enlève de la longueur des deux côtés.', 'The strip takes length off both sides.')


# ─────────────────────────────────────────────────────────────────────────────
# Probability and space
# ─────────────────────────────────────────────────────────────────────────────

def outfits(grade):
    who, g = sc.pick_actor()
    if grade <= 3 or random.random() < 0.4:
        a, b = random.randint(2, 5), random.randint(2, 4)
        variant = random.choice(['ice_cream', 'missing'])
        if variant == 'ice_cream':
            return _problem(
                f"Au comptoir, on choisit **1** saveur parmi **{a}** et **1** garniture parmi **{b}**. Combien de cornets différents peut-on commander ?",
                f"At the counter, you pick **1** flavour out of **{a}** and **1** topping out of **{b}**. How many different cones can you order?",
                a * b, [f'Pour chaque saveur, {b} garnitures possibles', f'{a} × {b} = {a * b}', f'{a * b} cornets'],
                [f'For each flavour, {b} possible toppings', f'{a} × {b} = {a * b}', f'{a * b} cones'],
                'Fais une liste ou un tableau : chaque saveur avec chaque garniture.', 'Make a list or a table: each flavour with each topping.')
        return _problem(
            f"{who} a **{a}** chandails et quelques casquettes. {_cap(sc.pronoun_fr(g))} peut faire **{a * b}** combinaisons chandail-casquette. Combien de casquettes a-t-{sc.pronoun_fr(g)} ?",
            f"{who} has **{a}** sweaters and some caps. {_cap(sc.pronoun_en(g))} can make **{a * b}** sweater-cap combinations. How many caps does {sc.pronoun_en(g)} have?",
            b, [f'{a} × ? = {a * b}', f'{a * b} ÷ {a} = {b}', f'{b} casquettes'], [f'{a} × ? = {a * b}', f'{a * b} ÷ {a} = {b}', f'{b} caps'],
            'Nombre de combinaisons = choix de chandails × choix de casquettes.', 'Number of combinations = sweater choices × cap choices.')
    if random.random() < 0.5:
        return probability_bag(grade)
    n = random.choice([2, 3])
    digits = random.randint(3, 5)
    return _problem(
        f"Un cadenas a **{n}** roulettes. Chaque roulette porte les chiffres de 1 à **{digits}**. Combien de codes différents sont possibles ?",
        f"A lock has **{n}** wheels. Each wheel shows the digits 1 to **{digits}**. How many different codes are possible?",
        digits ** n, [f'{digits} choix pour chaque roulette', ' × '.join([str(digits)] * n) + f' = {digits ** n}', f'{digits ** n} codes'],
        [f'{digits} choices for each wheel', ' × '.join([str(digits)] * n) + f' = {digits ** n}', f'{digits ** n} codes'],
        'Dans un arbre, chaque branche se divise de nouveau à chaque roulette.', 'In a tree diagram, each branch splits again at every wheel.')


def expected_count(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['spinner', 'die', 'compare'])
    if variant == 'spinner':
        d = random.choice([2, 4, 5, 8, 10])
        n = random.randint(1, d - 1)
        spins = d * random.randint(4, 12)
        return _problem(
            f"Une roulette est divisée en **{d}** secteurs égaux ; **{n}** sont rouges. {who} la fait tourner **{spins}** fois. Environ combien de fois devrait-elle s’arrêter sur le rouge ?",
            f"A spinner has **{d}** equal sections; **{n}** are red. {who} spins it **{spins}** times. About how many times should it land on red?",
            spins * n // d, [f'Probabilité du rouge : {n}/{d}', f'{n}/{d} de {spins} = {spins} ÷ {d} × {n} = {spins * n // d}', f'environ {spins * n // d} fois'],
            [f'Probability of red: {n}/{d}', f'{n}/{d} of {spins} = {spins} ÷ {d} × {n} = {spins * n // d}', f'about {spins * n // d} times'],
            'Nombre prévu = probabilité × nombre d’essais.', 'Expected number = probability × number of tries.')
    if variant == 'die':
        rolls = 6 * random.randint(5, 20)
        k = random.choice([1, 2, 3])
        what_fr = {1: 'un 6', 2: 'un 5 ou un 6', 3: 'un nombre pair'}[k]
        what_en = {1: 'a 6', 2: 'a 5 or a 6', 3: 'an even number'}[k]
        return _problem(
            f"{who} lance un dé à 6 faces **{rolls}** fois. Environ combien de fois devrait-{sc.pronoun_fr(g)} obtenir {what_fr} ?",
            f"{who} rolls a 6-sided die **{rolls}** times. About how many times should {sc.pronoun_en(g)} get {what_en}?",
            rolls * k // 6, [f'Probabilité : {k}/6', f'{rolls} ÷ 6 × {k} = {rolls * k // 6}', f'environ {rolls * k // 6} fois'],
            [f'Probability: {k}/6', f'{rolls} ÷ 6 × {k} = {rolls * k // 6}', f'about {rolls * k // 6} times'],
            'Compte les faces favorables sur 6, puis applique cette fraction au nombre de lancers.', 'Count the favourable faces out of 6, then apply that fraction to the number of rolls.')
    tries = random.choice([20, 40, 50, 100])
    got = random.randint(tries // 5, tries // 2)
    more = tries * 2
    exp = got * 2
    return _problem(
        f"En **{tries}** tirages, {who} a obtenu une bille bleue **{got}** fois. {'Si elle' if g == 'f' else 'S’il'} recommence l’expérience avec **{more}** tirages, environ combien de billes bleues peut-{sc.pronoun_fr(g)} prévoir ?",
        f"In **{tries}** draws, {who} got a blue marble **{got}** times. If {sc.pronoun_en(g)} repeats the experiment with **{more}** draws, about how many blue marbles can {sc.pronoun_en(g)} expect?",
        exp, [f'{more} = 2 × {tries}', f'2 × {got} = {exp}', f'environ {exp} billes bleues'], [f'{more} = 2 × {tries}', f'2 × {got} = {exp}', f'about {exp} blue marbles'],
        'Deux fois plus de tirages → environ deux fois plus de résultats.', 'Twice as many draws → about twice as many results.')


def grid_walk(grade):
    who, g = sc.pick_actor()
    x, y = random.randint(1, 4), random.randint(1, 4)
    r, u = random.randint(2, 6), random.randint(2, 6)
    l = random.randint(1, x + r - 1)
    variant = random.choice(['blocks', 'end_x', 'back_home'])
    path_fr = f"**{r}** cases vers la droite, **{u}** vers le haut, puis **{l}** vers la gauche"
    path_en = f"**{r}** squares right, **{u}** up, then **{l}** left"
    if variant == 'blocks':
        return _problem(
            f"Sur un plan quadrillé, {who} part de l’école et se déplace de {path_fr}. Combien de cases a-t-{sc.pronoun_fr(g)} parcourues en tout ?",
            f"On a grid map, {who} leaves school and moves {path_en}. How many squares did {sc.pronoun_en(g)} travel in all?",
            r + u + l, [f'{r} + {u} + {l} = {r + u + l}', f'{r + u + l} cases'], [f'{r} + {u} + {l} = {r + u + l}', f'{r + u + l} squares'],
            'Additionne chaque déplacement, peu importe la direction.', 'Add every move, whatever its direction.')
    if variant == 'end_x':
        ex, ey = x + r - l, y + u
        return _problem(
            f"Un robot est au point **({x}, {y})**. Il avance de {path_fr}. À quel point arrive-t-il ? Écris (x, y).",
            f"A robot is at point **({x}, {y})**. It moves {path_en}. Which point does it reach? Write (x, y).",
            f'({ex}, {ey})', [f'x : {x} + {r} − {l} = {ex}', f'y : {y} + {u} = {ey}', f'({ex}, {ey})'], [f'x: {x} + {r} − {l} = {ex}', f'y: {y} + {u} = {ey}', f'({ex}, {ey})'],
            'Droite/gauche change x ; haut/bas change y.', 'Right/left changes x; up/down changes y.', 'coordinate', [f'({ex}, {ey})'])
    dx, dy = random.randint(2, 8), random.randint(2, 8)
    return _problem(
        f"La maison {sc.de(who)} est **{dx}** rues à l’est et **{dy}** rues au nord de la bibliothèque. {_cap(sc.pronoun_fr(g))} va à la bibliothèque et revient par le chemin le plus court. Combien de rues parcourt-{sc.pronoun_fr(g)} ?",
        f"{who}'s house is **{dx}** blocks east and **{dy}** blocks north of the library. {_cap(sc.pronoun_en(g))} goes to the library and back by the shortest route. How many blocks does {sc.pronoun_en(g)} walk?",
        2 * (dx + dy), [f'Aller : {dx} + {dy} = {dx + dy}', f'Aller-retour : 2 × {dx + dy} = {2 * (dx + dy)}', f'{2 * (dx + dy)} rues'],
        [f'One way: {dx} + {dy} = {dx + dy}', f'There and back: 2 × {dx + dy} = {2 * (dx + dy)}', f'{2 * (dx + dy)} blocks'],
        'Le trajet le plus court suit les rues : est + nord, puis double pour le retour.', 'The shortest route follows the streets: east + north, then double it for the way back.')


# ─────────────────────────────────────────────────────────────────────────────
# Grade 6 integers (D2: negatives only where they are natural)
# ─────────────────────────────────────────────────────────────────────────────

def _sg(n):
    return f'−{abs(n)}' if n < 0 else str(n)


def _signed(n, unit=''):
    out = [_sg(n), str(n)] + ([f'{_sg(n)} {unit}'] if unit else [])
    return list(dict.fromkeys(out))


def signed_story(grade):
    who, g = sc.pick_actor()
    variant = random.choice(['temp_day', 'elevator', 'diver', 'gap'])
    if variant == 'temp_day':
        a = random.randint(-15, -2)
        up = random.randint(3, 18)
        down = random.randint(4, 16)
        b, c = a + up, a + up - down
        return _problem(
            f"À Chibougamau, il fait **{_sg(a)} °C** à 6 h. À midi, la température a monté de **{up} degrés**. Le soir, elle baisse de **{down} degrés**. Quelle température fait-il le soir ?",
            f"In Chibougamau it is **{_sg(a)} °C** at 6 a.m. By noon the temperature has risen by **{up} degrees**. In the evening it drops by **{down} degrees**. What is the evening temperature?",
            _sg(c), [f'Midi : {_sg(a)} + {up} = {_sg(b)} °C', f'Soir : {_sg(b)} − {down} = {_sg(c)} °C', f'{_sg(c)} °C'],
            [f'Noon: {_sg(a)} + {up} = {_sg(b)} °C', f'Evening: {_sg(b)} − {down} = {_sg(c)} °C', f'{_sg(c)} °C'],
            'Avance sur le thermomètre : vers le haut quand ça monte, vers le bas quand ça baisse. Passe par 0.',
            'Move along the thermometer: up when it rises, down when it drops. Go through 0.', 'signed', _signed(c, '°C'))
    if variant == 'elevator':
        start = random.randint(1, 9)
        down = random.randint(start + 1, start + 4)
        up = random.randint(1, 6)
        mid, end = start - down, start - down + up
        return _problem(
            f"{who} est au **{start}e étage**. {_cap(sc.pronoun_fr(g))} descend de **{down} étages** pour aller au stationnement, puis remonte de **{up} étage{'s' if up > 1 else ''}**. Le rez-de-chaussée est l’étage 0 et les sous-sols sont négatifs. À quel étage est-{sc.pronoun_fr(g)} ?",
            f"{who} is on **floor {start}**. {_cap(sc.pronoun_en(g))} goes down **{down} floors** to the car park, then up **{up} floor{'s' if up > 1 else ''}**. The ground floor is floor 0 and basement floors are negative. Which floor is {sc.pronoun_en(g)} on?",
            _sg(end), [f'{start} − {down} = {_sg(mid)}', f'{_sg(mid)} + {up} = {_sg(end)}', f'Étage {_sg(end)}'],
            [f'{start} − {down} = {_sg(mid)}', f'{_sg(mid)} + {up} = {_sg(end)}', f'Floor {_sg(end)}'],
            'Imagine les boutons de l’ascenseur : 0 au rez-de-chaussée, −1, −2… dessous.', 'Picture the elevator buttons: 0 on the ground floor, −1, −2… below it.',
            'signed', _signed(end))
    if variant == 'diver':
        depth = random.randint(8, 30)
        up = random.randint(2, depth + 6)
        end = -depth + up
        return _problem(
            f"Un plongeur est à **{_sg(-depth)} m** (0 m = niveau de la mer). Il remonte de **{up} m**. À quelle altitude est-il maintenant ?",
            f"A diver is at **{_sg(-depth)} m** (0 m = sea level). He rises **{up} m**. What is his altitude now?",
            _sg(end), [f'{_sg(-depth)} + {up} = {_sg(end)}', f'{_sg(end)} m' + (' (il est sorti de l’eau)' if end > 0 else '')],
            [f'{_sg(-depth)} + {up} = {_sg(end)}', f'{_sg(end)} m' + (' (he is out of the water)' if end > 0 else '')],
            'Remonter rapproche de 0 (ou le dépasse).', 'Rising brings you closer to 0 (or past it).', 'signed', _signed(end, 'm'))
    hi = random.choice(range(50, 400, 10))
    lo = -random.choice(range(10, 120, 5))
    return _problem(
        f"Un goéland vole à **{hi} m** au-dessus du niveau de la mer. Juste en dessous, un sous-marin est à **{_sg(lo)} m**. Quelle distance verticale les sépare ?",
        f"A gull flies **{hi} m** above sea level. Right below it, a submarine is at **{_sg(lo)} m**. What vertical distance separates them?",
        hi - lo, [f'Du sous-marin au niveau de la mer : {-lo} m', f'Du niveau de la mer au goéland : {hi} m', f'{-lo} + {hi} = {hi - lo} m'],
        [f'From the submarine to sea level: {-lo} m', f'From sea level to the gull: {hi} m', f'{-lo} + {hi} = {hi - lo} m'],
        'Passe par le niveau de la mer (0 m) : additionne les deux distances.', 'Go through sea level (0 m): add the two distances.')


def plane_walk(grade):
    """A robot moving across the four quadrants: where does it end up?"""
    x, y = random.randint(-4, 4), random.randint(-4, 4)
    moves, ex, ey, st_fr, st_en = [], x, y, [], []
    for _ in range(random.randint(2, 3)):
        d = random.choice(['g', 'd', 'h', 'b'])
        k = random.randint(2, 7)
        moves.append((d, k))
        if d in 'gd':
            nx = ex - k if d == 'g' else ex + k
            st_fr.append(f"x : {_sg(ex)} {'−' if d == 'g' else '+'} {k} = {_sg(nx)}")
            st_en.append(f"x: {_sg(ex)} {'−' if d == 'g' else '+'} {k} = {_sg(nx)}")
            ex = nx
        else:
            ny = ey + k if d == 'h' else ey - k
            st_fr.append(f"y : {_sg(ey)} {'+' if d == 'h' else '−'} {k} = {_sg(ny)}")
            st_en.append(f"y: {_sg(ey)} {'+' if d == 'h' else '−'} {k} = {_sg(ny)}")
            ey = ny
    fr = {'g': 'vers la gauche', 'd': 'vers la droite', 'h': 'vers le haut', 'b': 'vers le bas'}
    en = {'g': 'left', 'd': 'right', 'h': 'up', 'b': 'down'}
    key = f'({_sg(ex)}, {_sg(ey)})'
    return _problem(
        f"Un robot part du point **({_sg(x)}, {_sg(y)})** du plan cartésien. Il se déplace de " + ', puis '.join(f'**{k}** {fr[d]}' for d, k in moves) + ". Quelles sont ses coordonnées d’arrivée ? Écris (x, y).",
        f"A robot starts at point **({_sg(x)}, {_sg(y)})** on the coordinate plane. It moves " + ', then '.join(f'**{k}** {en[d]}' for d, k in moves) + ". What are its final coordinates? Write (x, y).",
        key, st_fr + [key], st_en + [key],
        'Gauche/droite change x ; haut/bas change y. Passe par 0 si besoin.', 'Left/right changes x; up/down changes y. Go through 0 if needed.',
        'coordinate', [key, f'({ex}, {ey})'])


# ─────────────────────────────────────────────────────────────────────────────
# registry: new skills → (grade, families)
# ─────────────────────────────────────────────────────────────────────────────

FAMILIES_PLUS = {
    # grades 1–2
    'g1-story-add-sub':        (1, [early_story]),
    'g1-missing-number':       (1, [early_story]),
    'g2-add-sub-2digit':       (2, [early_story]),
    'g2-equal-groups':         (3, [sharing]),
    # grade 3
    'g3-story-meaning':        (3, [sharing, money]),
    'g3-estimate-sum':         (3, [rounding_estimate]),
    'g3-fraction-words':       (3, [fraction_of]),
    'g3-numerator-denominator': (3, [fraction_of]),
    'g3-pictograph':           (3, [survey]),
    'g3-tally-table':          (3, [survey]),
    'g3-build-chart':          (3, [survey]),
    'g3-ruler-mm':             (3, [ribbon]),
    'g3-area-count-squares':   (3, [tiling]),
    'g3-volume-count-cubes':   (3, [cube_boxes]),
    'g3-balance-scale':        (3, [balance]),
    'g3-capacity-estimate':    (3, [balance]),
    'g3-thermometer':          (3, [temperature_change]),
    'g3-list-outcomes':        (3, [outfits]),
    'g3-grid-map':             (3, [grid_walk]),
    # grade 4
    'g4-arrays':               (4, [rows_groups]),
    'g4-missing-factor':       (4, [rows_groups]),
    'g4-times-tables':         (4, [rows_groups]),
    'g4-division-remainder':   (4, [remainder_trips]),
    'g4-line-graph':           (4, [plant_growth]),
    'g4-equivalent-fractions': (3, [fraction_of]),
    'g4-fraction-benchmark':   (3, [fraction_of]),
    'g4-decimal-grid':         (4, [decimal_measures]),
    'g4-decimal-equivalence':  (4, [decimal_measures]),
    'g4-decimal-number-line':  (4, [decimal_measures]),
    'g4-round-decimal':        (4, [decimal_measures]),
    # grade 5
    'g5-decimal-story':        (5, [decimal_shopping, decimal_measures]),
    'g5-decimal-properties':   (5, [decimal_shopping]),
    'g4-decimal-equivalences': (4, [decimal_measures]),
    'g5-estimate-decimal':     (5, [decimal_measures, decimal_shopping]),
    'g5-times-power-of-ten':   (5, [decimal_measures]),
    'g5-expression-for-story': (5, [decimal_shopping]),
    'g5-estimate-quotient':    (6, [production]),
    'g5-fraction-meanings':    (5, [fair_share]),
    'g5-order-same-numerator': (5, [fair_share]),
    'g5-number-patterns':      (6, [pattern]),
    'g5-area-units':           (5, [tiling]),
    'g5-estimate-length':      (5, [ribbon]),
    'g5-tree-diagram':         (5, [outfits]),
    'g5-simulation':           (5, [expected_count]),
    'g5-probability-line':     (5, [expected_count, probability_bag]),
    # grade 6
    'g6-percent':              (6, [percent_shop]),
    'g6-choose-notation':      (6, [percent_shop]),
    'g6-fraction-add-related': (6, [recipe_fractions]),
    'g6-whole-times-fraction': (6, [recipe_fractions]),
    'g6-simplify-fraction':    (6, [recipe_fractions]),
    'g6-order-related-denominators': (6, [recipe_fractions]),
    'g6-decimal-number-line':  (6, [decimal_measures]),
    'g6-divisibility':         (6, [teams]),
    'g6-prime-factors':        (6, [teams]),
    'g6-powers':               (6, [powers_story]),
    'g6-distributive':         (6, [production]),
    'g6-write-large-number':   (6, [inventory]),
    'g6-volume-units':         (6, [cube_boxes, volume_capacity]),
    'g6-protractor':           (6, [angles]),
    'g6-triangle-type':        (6, [angles]),
    'g6-circle-parts':         (6, [circles]),
    'cartesian-place-point':   (6, [grid_walk]),
    # grade 6 integers (negative answers allowed, decision D2)
    'g6-integer-thermometer':  (6, [signed_story]),
    'g6-integer-number-line':  (6, [signed_story]),
    'g6-integer-compare':      (6, [signed_story]),
    'g6-cartesian-4q':         (6, [plane_walk]),
}

# Skills whose answers may be negative (decision D2, 2026-10-26). Tests exempt exactly these from the
# "no negative numbers" rule; every other generator must stay ≥ 0.
SIGNED_SKILLS = {'g6-integer-read', 'g6-integer-thermometer', 'g6-integer-number-line', 'g6-integer-compare',
                 'g6-integer-order', 'g6-cartesian-4q'}
