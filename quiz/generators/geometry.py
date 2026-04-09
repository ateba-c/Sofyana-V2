import random
from .base import _tagged_shuffle_mc

# ── Pythagorean triples ───────────────────────────────────────────────────────

_PYTH_TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17)]

# ── helpers ───────────────────────────────────────────────────────────────────

def _pi_str(coeff):
    """Return e.g. '9\u03c0' for a circle formula."""
    return f'{coeff}\u03c0'


# ── area generator ────────────────────────────────────────────────────────────

def geometry_area_gen(level='medium'):
    shapes = ['rectangle', 'square', 'right_triangle', 'circle']
    shape = random.choice(shapes)

    if shape == 'rectangle':
        if level == 'easy':
            w, h = random.randint(2, 10), random.randint(2, 10)
        elif level == 'medium':
            w, h = random.randint(3, 20), random.randint(3, 20)
        else:
            w, h = random.randint(5, 50), random.randint(5, 50)
        result = w * h
        result_s = str(result)
        tagged_candidates = [
            (
                str(2 * (w + h)),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                str(w * h + w),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(max(0, w * h - h)),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str((w + 1) * h),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(w * (h + 1)),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(w + h),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
        ]
        choices = _tagged_shuffle_mc(result_s, tagged_candidates)
        prompt_en = f'Find the area of a rectangle with width {w} and height {h}.'
        prompt_fr = f"Trouvez l\u2019aire d\u2019un rectangle de largeur {w} et de hauteur {h}."
        hint_en = 'Area of a rectangle = width \u00d7 height'
        hint_fr = "Aire d\u2019un rectangle = largeur \u00d7 hauteur"
        expl_en = (f'Step 1: Use the formula: Area = width \u00d7 height.\n'
                   f'Step 2: Substitute: {w} \u00d7 {h}.\n'
                   f'Answer: Area = {result}')
        expl_fr = (f'\u00c9tape 1 : Utilise la formule : Aire = largeur \u00d7 hauteur.\n'
                   f'\u00c9tape 2 : Remplace : {w} \u00d7 {h}.\n'
                   f'R\u00e9ponse : Aire = {result}')
        shape_data = [{'type': 'rectangle', 'width': w, 'height': h,
                       'labels': {'inner': 'A = ?'}}]

    elif shape == 'square':
        if level == 'easy':
            s = random.randint(2, 10)
        elif level == 'medium':
            s = random.randint(3, 20)
        else:
            s = random.randint(5, 40)
        result = s * s
        result_s = str(result)
        tagged_candidates = [
            (
                str(4 * s),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                str(s * s + s),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(max(0, s * s - s)),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str((s + 1) ** 2),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(max(0, (s - 1) ** 2)),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(s * 2),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
        ]
        choices = _tagged_shuffle_mc(result_s, tagged_candidates)
        prompt_en = f'Find the area of a square with side length {s}.'
        prompt_fr = f"Trouvez l\u2019aire d\u2019un carr\u00e9 de c\u00f4t\u00e9 {s}."
        hint_en = 'Area of a square = side\u00b2'
        hint_fr = "Aire d\u2019un carr\u00e9 = c\u00f4t\u00e9\u00b2"
        expl_en = (f'Step 1: Use the formula: Area = side\u00b2.\n'
                   f'Step 2: Calculate: {s} \u00d7 {s}.\n'
                   f'Answer: Area = {result}')
        expl_fr = (f'\u00c9tape 1 : Utilise la formule : Aire = c\u00f4t\u00e9\u00b2.\n'
                   f'\u00c9tape 2 : Calcule : {s} \u00d7 {s}.\n'
                   f'R\u00e9ponse : Aire = {result}')
        shape_data = [{'type': 'square', 'side': s,
                       'labels': {'inner': 'A = ?'}}]

    elif shape == 'right_triangle':
        base_triple = random.choice(_PYTH_TRIPLES)
        k = random.choice([1, 2, 3]) if level != 'easy' else 1
        a, b, c = base_triple[0] * k, base_triple[1] * k, base_triple[2] * k
        actual_area_num = a * b
        # Area = a*b/2; if product is even, result is integer
        if actual_area_num % 2 == 0:
            result = actual_area_num // 2
            result_s = str(result)
        else:
            result = actual_area_num / 2
            result_s = f'{result:g}'
        tagged_candidates = [
            (
                str(a * b),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                str((a + b) // 2) if (a + b) % 2 == 0 else str(a + b),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                str(actual_area_num // 2 + 1),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(max(0, actual_area_num // 2 - 1)),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(a + b),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                str(c * c // 2),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
        ]
        choices = _tagged_shuffle_mc(result_s, tagged_candidates)
        prompt_en = f'Find the area of a right triangle with legs {a} and {b}.'
        prompt_fr = f"Trouvez l\u2019aire d\u2019un triangle rectangle de c\u00f4t\u00e9s {a} et {b}."
        hint_en = 'Area of a triangle = \u00bd \u00d7 base \u00d7 height'
        hint_fr = "Aire d\u2019un triangle = \u00bd \u00d7 base \u00d7 hauteur"
        expl_en = (f'Step 1: Use the formula: Area = \u00bd \u00d7 base \u00d7 height.\n'
                   f'Step 2: Multiply the legs: {a} \u00d7 {b} = {a*b}.\n'
                   f'Step 3: Divide by 2: {a*b} \u00f7 2.\n'
                   f'Answer: Area = {result_s}')
        expl_fr = (f'\u00c9tape 1 : Utilise la formule : Aire = \u00bd \u00d7 base \u00d7 hauteur.\n'
                   f'\u00c9tape 2 : Multiplie les c\u00f4t\u00e9s : {a} \u00d7 {b} = {a*b}.\n'
                   f'\u00c9tape 3 : Divise par 2 : {a*b} \u00f7 2.\n'
                   f'R\u00e9ponse : Aire = {result_s}')
        shape_data = [{'type': 'right_triangle', 'a': a, 'b': b,
                       'labels': {'inner': 'A = ?'}}]

    else:  # circle
        r = random.choice([2, 3, 4, 5, 6, 7, 8])
        area_coeff = r * r          # A = r\u00b2\u03c0
        result_s = _pi_str(area_coeff)
        tagged_candidates = [
            (
                _pi_str(2 * r),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                _pi_str(r),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                _pi_str(area_coeff + r),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                _pi_str(max(1, area_coeff - 1)),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                _pi_str(area_coeff + 1),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
        ]
        choices = _tagged_shuffle_mc(result_s, tagged_candidates)
        prompt_en = f'Find the area of a circle with radius {r}. Express in terms of \u03c0.'
        prompt_fr = f"Trouvez l\u2019aire d\u2019un cercle de rayon {r}. Exprimez en termes de \u03c0."
        hint_en = 'Area of a circle = \u03c0r\u00b2'
        hint_fr = "Aire d\u2019un cercle = \u03c0r\u00b2"
        expl_en = (f'Step 1: Use the formula: Area = \u03c0 \u00d7 r\u00b2.\n'
                   f'Step 2: Square the radius: {r}\u00b2 = {r*r}.\n'
                   f'Answer: Area = {result_s}')
        expl_fr = (f'\u00c9tape 1 : Utilise la formule : Aire = \u03c0 \u00d7 r\u00b2.\n'
                   f'\u00c9tape 2 : \u00c9l\u00e8ve le rayon au carr\u00e9 : {r}\u00b2 = {r*r}.\n'
                   f'R\u00e9ponse : Aire = {result_s}')
        shape_data = [{'type': 'circle', 'radius': r,
                       'labels': {'inner': 'A = ?'}}]

    return {
        'q_type':         'multiple_choice',
        'prompt_en':      prompt_en,
        'prompt_fr':      prompt_fr,
        'hint_en':        hint_en,
        'hint_fr':        hint_fr,
        'shape_data':     shape_data,
        'choices':        choices,
        'correct_answers': [result_s],
        'time_limit':     60,
        'points':         3,
        'explanation_en': expl_en,
        'explanation_fr': expl_fr,
    }


# ── perimeter generator ───────────────────────────────────────────────────────

def geometry_perimeter_gen(level='medium'):
    shapes = ['rectangle', 'square', 'equilateral_triangle', 'circle_circumference']
    shape = random.choice(shapes)

    if shape == 'rectangle':
        if level == 'easy':
            w, h = random.randint(2, 10), random.randint(2, 10)
        elif level == 'medium':
            w, h = random.randint(3, 25), random.randint(3, 25)
        else:
            w, h = random.randint(5, 60), random.randint(5, 60)
        result = 2 * (w + h)
        result_s = str(result)
        tagged_candidates = [
            (
                str(w * h),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                str(w + h),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                str(2 * w * h),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                str(2 * (w + h) + 1),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(2 * (w + h) - 1),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(w + w + h),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
        ]
        choices = _tagged_shuffle_mc(result_s, tagged_candidates)
        prompt_en = f'Find the perimeter of a rectangle with width {w} and height {h}.'
        prompt_fr = f"Trouvez le p\u00e9rim\u00e8tre d\u2019un rectangle de largeur {w} et de hauteur {h}."
        hint_en = 'Perimeter of a rectangle = 2 \u00d7 (width + height)'
        hint_fr = "P\u00e9rim\u00e8tre d\u2019un rectangle = 2 \u00d7 (largeur + hauteur)"
        expl_en = (f'Step 1: Use the formula: Perimeter = 2 \u00d7 (width + height).\n'
                   f'Step 2: Add the sides: {w} + {h} = {w+h}.\n'
                   f'Step 3: Multiply by 2: 2 \u00d7 {w+h}.\n'
                   f'Answer: Perimeter = {result}')
        expl_fr = (f'\u00c9tape 1 : Utilise la formule : P\u00e9rim\u00e8tre = 2 \u00d7 (largeur + hauteur).\n'
                   f'\u00c9tape 2 : Additionne les c\u00f4t\u00e9s : {w} + {h} = {w+h}.\n'
                   f'\u00c9tape 3 : Multiplie par 2 : 2 \u00d7 {w+h}.\n'
                   f'R\u00e9ponse : P\u00e9rim\u00e8tre = {result}')
        shape_data = [{'type': 'rectangle', 'width': w, 'height': h,
                       'labels': {'inner': 'P = ?'}}]

    elif shape == 'square':
        if level == 'easy':
            s = random.randint(2, 12)
        elif level == 'medium':
            s = random.randint(3, 25)
        else:
            s = random.randint(5, 50)
        result = 4 * s
        result_s = str(result)
        tagged_candidates = [
            (
                str(s * s),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                str(s * 2),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                str(4 * s + 1),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(3 * s),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                str(4 * s - 1),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(s * 5),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
        ]
        choices = _tagged_shuffle_mc(result_s, tagged_candidates)
        prompt_en = f'Find the perimeter of a square with side length {s}.'
        prompt_fr = f"Trouvez le p\u00e9rim\u00e8tre d\u2019un carr\u00e9 de c\u00f4t\u00e9 {s}."
        hint_en = 'Perimeter of a square = 4 \u00d7 side'
        hint_fr = "P\u00e9rim\u00e8tre d\u2019un carr\u00e9 = 4 \u00d7 c\u00f4t\u00e9"
        expl_en = (f'Step 1: Use the formula: Perimeter = 4 \u00d7 side.\n'
                   f'Step 2: Multiply: 4 \u00d7 {s}.\n'
                   f'Answer: Perimeter = {result}')
        expl_fr = (f'\u00c9tape 1 : Utilise la formule : P\u00e9rim\u00e8tre = 4 \u00d7 c\u00f4t\u00e9.\n'
                   f'\u00c9tape 2 : Multiplie : 4 \u00d7 {s}.\n'
                   f'R\u00e9ponse : P\u00e9rim\u00e8tre = {result}')
        shape_data = [{'type': 'square', 'side': s,
                       'labels': {'inner': 'P = ?'}}]

    elif shape == 'equilateral_triangle':
        if level == 'easy':
            s = random.randint(2, 12)
        elif level == 'medium':
            s = random.randint(3, 25)
        else:
            s = random.randint(5, 50)
        result = 3 * s
        result_s = str(result)
        tagged_candidates = [
            (
                str(s * s),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                str(s * 2),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                str(3 * s + 1),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(s * 4),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                str(3 * s - 1),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                str(s + 3),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
        ]
        choices = _tagged_shuffle_mc(result_s, tagged_candidates)
        prompt_en = f'Find the perimeter of an equilateral triangle with side length {s}.'
        prompt_fr = f"Trouvez le p\u00e9rim\u00e8tre d\u2019un triangle \u00e9quilat\u00e9ral de c\u00f4t\u00e9 {s}."
        hint_en = 'An equilateral triangle has 3 equal sides. Perimeter = 3 \u00d7 side'
        hint_fr = "Un triangle \u00e9quilat\u00e9ral a 3 c\u00f4t\u00e9s \u00e9gaux. P\u00e9rim\u00e8tre = 3 \u00d7 c\u00f4t\u00e9"
        expl_en = (f'Step 1: An equilateral triangle has 3 equal sides of length {s}.\n'
                   f'Step 2: Add all sides: {s} + {s} + {s}.\n'
                   f'Answer: Perimeter = {result}')
        expl_fr = (f'\u00c9tape 1 : Un triangle \u00e9quilat\u00e9ral a 3 c\u00f4t\u00e9s \u00e9gaux de longueur {s}.\n'
                   f'\u00c9tape 2 : Additionne tous les c\u00f4t\u00e9s : {s} + {s} + {s}.\n'
                   f'R\u00e9ponse : P\u00e9rim\u00e8tre = {result}')
        shape_data = [{'type': 'equilateral_triangle', 'side': s,
                       'labels': {'inner': 'P = ?'}}]

    else:  # circle circumference
        r = random.choice([2, 3, 4, 5, 6, 7, 8])
        circ_coeff = 2 * r          # C = 2\u03c0r
        result_s = _pi_str(circ_coeff)
        tagged_candidates = [
            (
                _pi_str(r),
                'wrong_formula',
                "Don't forget to add all sides for the perimeter.",
                "N'oublie pas d'additionner tous les côtés pour le périmètre.",
            ),
            (
                _pi_str(r * r),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                _pi_str(2 * r + 2),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                _pi_str(r * r * 2),
                'wrong_formula',
                "You used the area formula instead of perimeter (or vice versa).",
                "Tu as utilisé la formule d'aire au lieu du périmètre (ou vice versa).",
            ),
            (
                _pi_str(circ_coeff + 2),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
            (
                _pi_str(max(1, circ_coeff - 2)),
                'off_by_one',
                "Check your dimensions — you may have used the wrong one.",
                "Vérifie tes dimensions — tu as peut-être utilisé la mauvaise.",
            ),
        ]
        choices = _tagged_shuffle_mc(result_s, tagged_candidates)
        prompt_en = f'Find the circumference of a circle with radius {r}. Express in terms of \u03c0.'
        prompt_fr = f"Trouvez la circonf\u00e9rence d\u2019un cercle de rayon {r}. Exprimez en termes de \u03c0."
        hint_en = 'Circumference = 2\u03c0r'
        hint_fr = 'Circonf\u00e9rence = 2\u03c0r'
        expl_en = (f'Step 1: Use the formula: Circumference = 2\u03c0r.\n'
                   f'Step 2: Substitute: 2 \u00d7 \u03c0 \u00d7 {r}.\n'
                   f'Answer: Circumference = {result_s}')
        expl_fr = (f'\u00c9tape 1 : Utilise la formule : Circonf\u00e9rence = 2\u03c0r.\n'
                   f'\u00c9tape 2 : Remplace : 2 \u00d7 \u03c0 \u00d7 {r}.\n'
                   f'R\u00e9ponse : Circonf\u00e9rence = {result_s}')
        shape_data = [{'type': 'circle', 'radius': r,
                       'labels': {'inner': 'C = ?'}}]

    return {
        'q_type':         'multiple_choice',
        'prompt_en':      prompt_en,
        'prompt_fr':      prompt_fr,
        'hint_en':        hint_en,
        'hint_fr':        hint_fr,
        'shape_data':     shape_data,
        'choices':        choices,
        'correct_answers': [result_s],
        'time_limit':     60,
        'points':         3,
        'explanation_en': expl_en,
        'explanation_fr': expl_fr,
    }


# Grade-3 geometry generators

def identify_angle_gen(level="medium"):
    angle_types = {
        "easy": [("acute", (20, 70)), ("right", None), ("obtuse", (110, 160))],
        "medium": [("acute", (15, 85)), ("right", None), ("obtuse", (95, 165))],
        "hard": [("acute", (75, 88)), ("obtuse", (92, 110))],
    }
    import random
    choices_for_level = angle_types.get(level, angle_types["medium"])
    angle_type, deg_range = random.choice(choices_for_level)
    degrees = 90 if deg_range is None else random.randint(*deg_range)
    correct_fr = {"acute": "aigu", "right": "droit", "obtuse": "obtus"}[angle_type]
    correct_en = {"acute": "acute", "right": "right", "obtuse": "obtuse"}[angle_type]
    distractors = [(t, "wrong_angle_type",
                   "Compare to a right angle (corner of paper).",
                   "Compare a un angle droit.")
                  for t in ["aigu", "droit", "obtus"] if t != correct_fr]
    distractors.append(("plat", "wrong_angle_type", "Flat angle = 180 degrees.", "Angle plat = 180."))
    from quiz.generators.base import _tagged_shuffle_mc
    mc = _tagged_shuffle_mc(correct_fr, distractors)
    expl = {"acute": ("Aigu: 0<angle<90.", "Acute: 0<90."),
            "right": ("Droit: exactement 90.", "Right: exactly 90."),
            "obtuse": ("Obtus: 90<angle<180.", "Obtuse: 90<180.")}[angle_type]
    return {
        "q_type": "multiple_choice",
        "prompt_fr": "Quel type d angle vois-tu ?",
        "prompt_en": "What type of angle is this?",
        "hint_fr": "Droit = coin parfait. Aigu < droit. Obtus > droit.",
        "hint_en": "Right = perfect corner. Acute < right < obtuse.",
        "shape_data": [{"type": "angle", "degrees": degrees}],
        "show_illustration": True,
        "choices": mc,
        "correct_answers": [correct_fr, correct_en],
        "time_limit": 25, "points": 1,
        "explanation_fr": f"Cet angle mesure {degrees}. {expl[0]}",
        "explanation_en": f"This angle is {degrees}. {expl[1]}",
    }


def parallel_perpendicular_gen(level='medium'):
    """QCM + SVG — identify whether lines are parallel, perpendicular or intersecting."""
    import random
    from quiz.generators.base import _tagged_shuffle_mc
    relations = ['parallel', 'perpendicular', 'intersecting']
    relation = random.choice(['parallel', 'perpendicular'] if level == 'easy' else relations)
    labels_fr = {'parallel': 'paralleles', 'perpendicular': 'perpendiculaires',
                 'intersecting': 'secantes'}
    labels_en = {'parallel': 'parallel', 'perpendicular': 'perpendicular',
                 'intersecting': 'intersecting'}
    correct_fr, correct_en = labels_fr[relation], labels_en[relation]
    distractors = [
        (labels_fr[r], 'wrong_relation',
         'Parallel: never meet. Perpendicular: 90 degree crossing.',
         'Paralleles: ne se croisent pas. Perpendiculaires: angle droit.')
        for r in relations if r != relation
    ]
    distractors.append(('ni parallel ni perp', 'wrong_relation',
                        'One of the three must apply.', "L'une des trois s'applique."))
    choices = _tagged_shuffle_mc(correct_fr, distractors)
    expl_fr = {'parallel': 'Paralleles: ne se croisent pas.',
               'perpendicular': 'Perpendiculaires: angle droit (90).',
               'intersecting': 'Secantes: se croisent en un point.'}[relation]
    expl_en = {'parallel': 'Parallel: they never meet.',
               'perpendicular': 'Perpendicular: they cross at 90 degrees.',
               'intersecting': 'Intersecting: they cross at a point.'}[relation]
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': 'Ces droites sont-elles paralleles, perpendiculaires ou secantes ?',
        'prompt_en': 'Are these lines parallel, perpendicular, or intersecting?',
        'hint_fr': 'Paralleles = jamais en contact. Perpendiculaires = angle droit.',
        'hint_en': 'Parallel = never meet. Perpendicular = right angle.',
        'shape_data': [{'type': 'line_pair', 'relation': relation}],
        'show_illustration': True,
        'choices': choices,
        'correct_answers': [correct_fr, correct_en],
        'time_limit': 25, 'points': 1,
        'explanation_fr': expl_fr,
        'explanation_en': expl_en,
    }


_POLYGON_NAMES_FR = {3: 'triangle', 4: 'quadrilatere', 5: 'pentagone',
                     6: 'hexagone', 7: 'heptagone', 8: 'octogone'}
_POLYGON_NAMES_EN = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon',
                     6: 'hexagon', 7: 'heptagon', 8: 'octagon'}


def name_polygon_gen(level='medium'):
    """QCM + SVG -- see a regular polygon, choose its name."""
    import random
    from quiz.generators.base import _tagged_shuffle_mc
    mapping = {'easy': [3, 4], 'medium': [3, 4, 5, 6], 'hard': [3, 4, 5, 6, 7, 8]}
    sides = random.choice(mapping.get(level, [3, 4, 5, 6]))
    correct_fr = _POLYGON_NAMES_FR[sides]
    correct_en = _POLYGON_NAMES_EN[sides]
    distract_sides = [s for s in _POLYGON_NAMES_FR if s != sides]
    random.shuffle(distract_sides)
    distractors = [
        (_POLYGON_NAMES_FR[s], 'wrong_name',
         f'Count the sides -- this shape has {sides}.',
         f'Compte les cotes -- cette figure en a {sides}.')
        for s in distract_sides[:4]
    ]
    choices = _tagged_shuffle_mc(correct_fr, distractors)
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': 'Comment s\'appelle cette figure ?',
        'prompt_en': 'What is this shape called?',
        'hint_fr': 'Compte le nombre de cotes.',
        'hint_en': 'Count the number of sides.',
        'shape_data': [{'type': 'polygon', 'sides': sides}],
        'show_illustration': True,
        'choices': choices,
        'correct_answers': [correct_fr, correct_en],
        'time_limit': 25, 'points': 1,
        'explanation_fr': f'Cette figure a {sides} cotes -> {correct_fr}.',
        'explanation_en': f'This shape has {sides} sides -> {correct_en}.',
    }


def count_sides_gen(level='medium'):
    """Typed + SVG -- count the number of sides of a polygon."""
    import random
    mapping = {'easy': [3, 4, 5], 'medium': [3, 4, 5, 6], 'hard': [3, 4, 5, 6, 7, 8]}
    sides = random.choice(mapping.get(level, [3, 4, 5, 6]))
    name_fr = _POLYGON_NAMES_FR[sides]
    name_en = _POLYGON_NAMES_EN[sides]
    return {
        'q_type': 'text_input',
        'prompt_fr': 'Combien de cotes a cette figure ?',
        'prompt_en': 'How many sides does this shape have?',
        'hint_fr': 'Compte chaque segment du contour une seule fois.',
        'hint_en': 'Count each edge of the outline once.',
        'shape_data': [{'type': 'polygon', 'sides': sides}],
        'show_illustration': True,
        'choices': [],
        'correct_answers': [str(sides)],
        'time_limit': 20, 'points': 1,
        'explanation_fr': f'Cette figure a {sides} cotes -- c\'est un {name_fr}.',
        'explanation_en': f'This shape has {sides} sides -- it is a {name_en}.',
    }


# ─────────────────────────────────────────────────────────────────────────────
# identify_solid_gen  (content2.md Thème 3, section 17)
# ─────────────────────────────────────────────────────────────────────────────

_SOLIDS_FR = {
    'Cône':                      ('1 base circulaire, 1 sommet, 0 arête droite', 'cone'),
    'Cube':                      ('6 faces carrées, 8 sommets, 12 arêtes',        'cube'),
    'Cylindre':                  ('2 bases circulaires, 0 sommet, 0 arête droite', 'cylinder'),
    'Sphère':                    ('0 face plate, 0 arête, 0 sommet',               'sphere'),
    'Prisme à base triangulaire':('5 faces, 6 sommets, 9 arêtes',                 'triangular prism'),
    'Pyramide à base carrée':    ('5 faces, 5 sommets, 8 arêtes',                 'square pyramid'),
}

_SOLIDS_EN = {
    'Cône':                       'Cone',
    'Cube':                       'Cube',
    'Cylindre':                   'Cylinder',
    'Sphère':                     'Sphere',
    'Prisme à base triangulaire': 'Triangular Prism',
    'Pyramide à base carrée':     'Square Pyramid',
}


def identify_solid_gen(level='easy'):
    """mix_match — match solid name to its face/vertex/edge description."""
    if level == 'easy':
        pool = ['Cube', 'Cône', 'Sphère']
    elif level == 'medium':
        pool = ['Cube', 'Cône', 'Cylindre', 'Pyramide à base carrée']
    else:
        pool = list(_SOLIDS_FR.keys())

    count = 3 if level == 'easy' else 4
    chosen = random.sample(pool, min(count, len(pool)))

    pairs = []
    for name_fr in chosen:
        desc_fr, _ = _SOLIDS_FR[name_fr]
        pairs.append({'left': name_fr, 'right': desc_fr})

    return {
        'q_type':          'mix_match',
        'prompt_fr':       'Associe chaque solide à sa description (faces, sommets, arêtes).',
        'prompt_en':       'Match each solid to its description (faces, vertices, edges).',
        'hint_fr':         'Un cube a 6 faces carrées. Un cône a 1 sommet et 1 base circulaire.',
        'hint_en':         'A cube has 6 square faces. A cone has 1 apex and 1 circular base.',
        'show_illustration': False,
        'shape_data':      [],
        'choices':         [],
        'pairs':           pairs,
        'explanation_en': (
            'Step 1: Recall key solids — cube: 6 faces; cone: 1 apex + 1 circular base; cylinder: 2 circular bases.\n'
            'Step 2: Match each solid name to its correct description.\n'
            'Step 3: Use elimination if unsure — rule out the descriptions that don\'t fit.'
        ),
        'explanation_fr': (
            'Étape 1 : Rappelle-toi les solides clés — cube : 6 faces carrées ; cône : 1 sommet + 1 base circulaire ; cylindre : 2 bases circulaires.\n'
            'Étape 2 : Associe chaque nom de solide à sa description correcte.\n'
            'Étape 3 : Utilise l\'élimination si besoin — écarte les descriptions qui ne correspondent pas.'
        ),
        'correct_answers': [p['right'] for p in pairs],
    }


# ─────────────────────────────────────────────────────────────────────────────
# perimeter_labeled_gen  (content2.md Thème 3, section 15)
# ─────────────────────────────────────────────────────────────────────────────

def perimeter_labeled_gen(level='easy'):
    """
    Typed input + SVG — add labeled sides, compute perimeter.
    Shapes: rectangle, square, equilateral triangle, or isosceles triangle.
    easy   → small sides ≤ 10 cm, rectangle or square
    medium → sides ≤ 20 cm, any shape
    hard   → sides ≤ 50 cm, any shape; may mix units (dm)
    """
    unit = 'cm'
    if level == 'easy':
        shape_type = random.choice(['rectangle', 'square'])
        if shape_type == 'square':
            s = random.randint(2, 10)
            sides = [s, s, s, s]
            svg = [{'type': 'labeled_rect', 'w_val': s, 'h_val': s, 'unit': unit}]
            perimeter = 4 * s
        else:
            w = random.randint(2, 10)
            h = random.randint(2, 10)
            while h == w:
                h = random.randint(2, 10)
            sides = [w, h, w, h]
            svg = [{'type': 'labeled_rect', 'w_val': w, 'h_val': h, 'unit': unit}]
            perimeter = 2 * (w + h)
    elif level == 'medium':
        shape_type = random.choice(['rectangle', 'square', 'equilateral', 'isosceles'])
        if shape_type == 'square':
            s = random.randint(3, 20)
            sides = [s, s, s, s]
            svg = [{'type': 'labeled_rect', 'w_val': s, 'h_val': s, 'unit': unit}]
            perimeter = 4 * s
        elif shape_type == 'rectangle':
            w = random.randint(3, 20)
            h = random.randint(3, 20)
            while h == w:
                h = random.randint(3, 20)
            sides = [w, h, w, h]
            svg = [{'type': 'labeled_rect', 'w_val': w, 'h_val': h, 'unit': unit}]
            perimeter = 2 * (w + h)
        elif shape_type == 'equilateral':
            s = random.randint(3, 20)
            sides = [s, s, s]
            svg = [{'type': 'labeled_triangle', 'sides': sides, 'unit': unit}]
            perimeter = 3 * s
        else:  # isosceles
            base = random.randint(3, 20)
            leg  = random.randint(3, 20)
            while leg == base:
                leg = random.randint(3, 20)
            sides = [leg, base, leg]
            svg = [{'type': 'labeled_triangle', 'sides': sides, 'unit': unit}]
            perimeter = 2 * leg + base
    else:
        shape_type = random.choice(['rectangle', 'equilateral', 'isosceles', 'pentagon'])
        if shape_type == 'pentagon':
            sides = [random.randint(4, 15) for _ in range(5)]
            # For pentagon, use the text-based description (no SVG shape type yet)
            sides_str = ' + '.join(str(s) for s in sides)
            perimeter = sum(sides)
            return {
                'q_type':          'text_input',
                'prompt_fr':       f"Un pentagone a des côtés de {', '.join(str(s) for s in sides)} cm. Quel est son périmètre ?",
                'prompt_en':       f"A pentagon has sides of {', '.join(str(s) for s in sides)} cm. What is its perimeter?",
                'hint_fr':         'Le périmètre = somme de tous les côtés.',
                'hint_en':         'Perimeter = sum of all sides.',
                'show_illustration': False,
                'shape_data':      [],
                'choices':         [],
                'pairs':           [],
                'explanation_en': (
                    f'Step 1: A pentagon has 5 sides: {", ".join(str(s) for s in sides)} cm.\n'
                    f'Step 2: Add all 5 sides: {" + ".join(str(s) for s in sides)} = {perimeter}.\n'
                    f'Answer: perimeter = {perimeter} cm'
                ),
                'explanation_fr': (
                    f'Étape 1 : Un pentagone a 5 côtés : {", ".join(str(s) for s in sides)} cm.\n'
                    f'Étape 2 : Additionne les 5 côtés : {" + ".join(str(s) for s in sides)} = {perimeter}.\n'
                    f'Réponse : périmètre = {perimeter} cm'
                ),
                'correct_answers': [str(perimeter), f'{perimeter} cm'],
            }
        elif shape_type == 'rectangle':
            w = random.randint(5, 50)
            h = random.randint(5, 50)
            while h == w:
                h = random.randint(5, 50)
            sides = [w, h, w, h]
            svg = [{'type': 'labeled_rect', 'w_val': w, 'h_val': h, 'unit': unit}]
            perimeter = 2 * (w + h)
        elif shape_type == 'equilateral':
            s = random.randint(5, 50)
            sides = [s, s, s]
            svg = [{'type': 'labeled_triangle', 'sides': sides, 'unit': unit}]
            perimeter = 3 * s
        else:  # isosceles
            base = random.randint(5, 50)
            leg  = random.randint(5, 50)
            while leg == base:
                leg = random.randint(5, 50)
            sides = [leg, base, leg]
            svg = [{'type': 'labeled_triangle', 'sides': sides, 'unit': unit}]
            perimeter = 2 * leg + base

    sides_str = ' + '.join(str(s) for s in sides)

    return {
        'q_type':          'text_input',
        'prompt_fr':       "Quel est le périmètre de cet enclos (en cm) ?",
        'prompt_en':       "What is the perimeter of this enclosure (in cm)?",
        'hint_fr':         f"Additionne tous les côtés : {sides_str} = ?",
        'hint_en':         f"Add all sides: {sides_str} = ?",
        'show_illustration': True,
        'shape_data':      svg,
        'choices':         [],
        'pairs':           [],
        'explanation_en': (
            f'Step 1: Identify all sides of the shape: {sides_str} cm.\n'
            f'Step 2: Perimeter = sum of all sides = {sides_str} = {perimeter}.\n'
            f'Answer: perimeter = {perimeter} cm'
        ),
        'explanation_fr': (
            f'Étape 1 : Identifie tous les côtés de la figure : {sides_str} cm.\n'
            f'Étape 2 : Périmètre = somme de tous les côtés = {sides_str} = {perimeter}.\n'
            f'Réponse : périmètre = {perimeter} cm'
        ),
        'correct_answers': [str(perimeter), f'{perimeter} cm'],
    }
