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
    choices_for_level = angle_types.get(level, angle_types["medium"])
    angle_type, deg_range = random.choice(choices_for_level)
    degrees = 90 if deg_range is None else random.randint(*deg_range)
    names = {"acute": ("aigu", "acute"), "right": ("droit", "right"),
             "obtuse": ("obtus", "obtuse"), "straight": ("plat", "straight")}
    correct = names[angle_type]
    distractors = [(names[t], "wrong_angle_type",
                    "Compare it with a right angle (the corner of a sheet of paper).",
                    "Compare-le à un angle droit (le coin d’une feuille).")
                   for t in ("acute", "right", "obtuse") if t != angle_type]
    distractors.append((names["straight"], "wrong_angle_type",
                        "A straight angle measures 180°: its two sides form a straight line.",
                        "Un angle plat mesure 180° : ses deux côtés forment une ligne droite."))
    mc = _tagged_shuffle_mc(correct, distractors)
    expl = {"acute": ("Un angle aigu mesure plus de 0° et moins de 90°.",
                      "An acute angle is greater than 0° and less than 90°."),
            "right": ("Un angle droit mesure exactement 90°.", "A right angle measures exactly 90°."),
            "obtuse": ("Un angle obtus mesure plus de 90° et moins de 180°.",
                       "An obtuse angle is greater than 90° and less than 180°.")}[angle_type]
    return {
        "q_type": "multiple_choice",
        "prompt_fr": "Quel type d’angle vois-tu ?",
        "prompt_en": "What type of angle is this?",
        "hint_fr": "Droit = 90° (coin parfait). Aigu : moins de 90°. Obtus : entre 90° et 180°. Plat = 180° (une ligne droite).",
        "hint_en": "Right = 90° (a perfect corner). Acute: less than 90°. Obtuse: between 90° and 180°. Straight = 180° (a straight line).",
        "shape_data": [{"type": "angle", "degrees": degrees}],
        "show_illustration": True,
        "choices": mc,
        "correct_answers": list(correct),
        "time_limit": 25, "points": 1,
        "explanation_fr": f"Cet angle mesure {degrees}°. {expl[0]} C’est un angle {correct[0]}.",
        "explanation_en": f"This angle measures {degrees}°. {expl[1]} It is {_a_en(correct[1])} angle.",
    }


# Line relations — mutually exclusive labels: perpendicular lines are also
# intersecting, so the third relation is « sécantes non perpendiculaires ».
LINE_LABELS = {
    'parallel': ('parallèles', 'parallel'),
    'perpendicular': ('perpendiculaires', 'perpendicular'),
    'intersecting': ('sécantes non perpendiculaires', 'intersecting, not perpendicular'),
}


def parallel_perpendicular_gen(level='medium'):
    """QCM + SVG — identify whether lines are parallel, perpendicular or intersecting (not at a right angle)."""
    relations = ['parallel', 'perpendicular', 'intersecting']
    relation = random.choice(['parallel', 'perpendicular'] if level == 'easy' else relations)
    correct = LINE_LABELS[relation]
    distractors = [
        (LINE_LABELS[r], 'wrong_relation',
         'Parallel: they never meet. Perpendicular: they cross at a right angle. '
         'Intersecting, not perpendicular: they cross without a right angle.',
         'Parallèles : elles ne se croisent jamais. Perpendiculaires : elles se croisent à angle droit. '
         'Sécantes non perpendiculaires : elles se croisent sans angle droit.')
        for r in relations if r != relation
    ]
    distractors.append((('courbes', 'curved'), 'irrelevant_property',
                        'These are straight lines.', 'Ce sont des droites, pas des courbes.'))
    choices = _tagged_shuffle_mc(correct, distractors)
    expl_fr = {'parallel': 'Elles ne se croisent jamais et gardent le même écart : elles sont parallèles.',
               'perpendicular': 'Elles se croisent en formant un angle droit (90°) : elles sont perpendiculaires.',
               'intersecting': 'Elles se croisent en un point, sans angle droit : elles sont sécantes non perpendiculaires.'}[relation]
    expl_en = {'parallel': 'They never meet and stay the same distance apart: they are parallel.',
               'perpendicular': 'They cross forming a right angle (90°): they are perpendicular.',
               'intersecting': 'They cross at one point, without a right angle: they are intersecting, not perpendicular.'}[relation]
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': 'Ces deux droites sont-elles parallèles, perpendiculaires ou sécantes non perpendiculaires ?',
        'prompt_en': 'Are these two lines parallel, perpendicular, or intersecting but not perpendicular?',
        'hint_fr': 'Les droites se croisent-elles ? Si oui, cherche un angle droit (petit carré). '
                   'Des droites perpendiculaires sont aussi sécantes : choisis la réponse la plus précise.',
        'hint_en': 'Do the lines cross? If they do, look for a right angle (small square). '
                   'Perpendicular lines also intersect: choose the most precise answer.',
        'shape_data': [{'type': 'line_pair', 'relation': relation}],
        'show_illustration': True,
        'choices': choices,
        'correct_answers': list(correct),
        'time_limit': 25, 'points': 1,
        'explanation_fr': expl_fr,
        'explanation_en': expl_en,
    }


POLYGON_NAMES = {3: ('triangle', 'triangle'), 4: ('quadrilatère', 'quadrilateral'),
                 5: ('pentagone', 'pentagon'), 6: ('hexagone', 'hexagon'),
                 7: ('heptagone', 'heptagon'), 8: ('octogone', 'octagon')}


def _a_en(word):
    """English indefinite article: « an octagon », « a hexagon »."""
    return ('an ' if word[0] in 'aeiou' else 'a ') + word


def _count_steps(n):
    return ', '.join(str(k) for k in range(1, n + 1))


def name_polygon_gen(level='medium'):
    """QCM + SVG — see a regular polygon, choose its name."""
    mapping = {'easy': [3, 4], 'medium': [3, 4, 5, 6], 'hard': [5, 6, 7, 8]}
    sides = random.choice(mapping.get(level, [3, 4, 5, 6]))
    correct = POLYGON_NAMES[sides]
    distract_sides = [s for s in POLYGON_NAMES if s != sides]
    random.shuffle(distract_sides)
    distractors = [
        (POLYGON_NAMES[s], 'wrong_name',
         f'Count the sides: this shape has {sides}.',
         f'Compte les côtés : cette figure en a {sides}.')
        for s in distract_sides[:4]
    ]
    choices = _tagged_shuffle_mc(correct, distractors)
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': 'Comment s’appelle cette figure ?',
        'prompt_en': 'What is this shape called?',
        'hint_fr': 'Compte le nombre de côtés.',
        'hint_en': 'Count the number of sides.',
        'shape_data': [{'type': 'polygon', 'sides': sides}],
        'show_illustration': True,
        'choices': choices,
        'correct_answers': list(correct),
        'time_limit': 25, 'points': 1,
        'explanation_fr': f'Cette figure a {sides} côtés, donc c’est un {correct[0]}.',
        'explanation_en': f'This shape has {sides} sides, so it is {_a_en(correct[1])}.',
    }


def count_sides_gen(level='medium'):
    """Typed + SVG — count the number of sides of a polygon."""
    mapping = {'easy': [3, 4, 5], 'medium': [3, 4, 5, 6], 'hard': [5, 6, 7, 8]}
    sides = random.choice(mapping.get(level, [3, 4, 5, 6]))
    name_fr, name_en = POLYGON_NAMES[sides]
    return {
        'q_type': 'text_input',
        'answer_type': 'integer',
        'prompt_fr': 'Combien de côtés a cette figure ?',
        'prompt_en': 'How many sides does this shape have?',
        'hint_fr': 'Compte chaque segment du contour une seule fois.',
        'hint_en': 'Count each edge of the outline once.',
        'shape_data': [{'type': 'polygon', 'sides': sides}],
        'show_illustration': True,
        'choices': [],
        'correct_answers': [str(sides)],
        'time_limit': 20, 'points': 1,
        'explanation_fr': (f'Je compte les segments du contour : {_count_steps(sides)}. '
                           f'Cette figure a {sides} côtés : c’est un {name_fr}.'),
        'explanation_en': (f'Count the segments of the outline: {_count_steps(sides)}. '
                           f'This shape has {sides} sides: it is {_a_en(name_en)}.'),
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

# English descriptions (plural after 0 and after numbers above 1)
_SOLIDS_DESC_EN = {
    'Cône':                       '1 circular base, 1 vertex, 0 straight edges',
    'Cube':                       '6 square faces, 8 vertices, 12 edges',
    'Cylindre':                   '2 circular bases, 0 vertices, 0 straight edges',
    'Sphère':                     '0 flat faces, 0 edges, 0 vertices',
    'Prisme à base triangulaire': '5 faces, 6 vertices, 9 edges',
    'Pyramide à base carrée':     '5 faces, 5 vertices, 8 edges',
}

# Why each description fits: (fr, en)
_SOLIDS_WHY = {
    'Cône':      ('le cône a une seule base ronde et une pointe (1 sommet)',
                  'the cone has one round base and a tip (1 vertex)'),
    'Cube':      ('le cube a 6 faces carrées', 'the cube has 6 square faces'),
    'Cylindre':  ('le cylindre a 2 bases rondes et aucun sommet', 'the cylinder has 2 round bases and no vertex'),
    'Sphère':    ('la sphère est toute ronde : aucune face plate, aucune arête, aucun sommet',
                  'the sphere is completely round: no flat face, no edge, no vertex'),
    'Prisme à base triangulaire': ('le prisme à base triangulaire a 2 triangles et 3 rectangles : 5 faces et 6 sommets',
                                   'the triangular prism has 2 triangles and 3 rectangles: 5 faces and 6 vertices'),
    'Pyramide à base carrée': ('la pyramide à base carrée a 1 carré et 4 triangles : 5 faces et 5 sommets',
                               'the square pyramid has 1 square and 4 triangles: 5 faces and 5 vertices'),
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
        pairs.append({'left': name_fr, 'left_en': _SOLIDS_EN.get(name_fr, name_fr),
                      'right': desc_fr, 'right_en': _SOLIDS_DESC_EN[name_fr]})

    return {
        'q_type':          'mix_match',
        'prompt_fr':       'Associe chaque solide à sa description (faces, sommets, arêtes).',
        'prompt_en':       'Match each solid to its description (faces, vertices, edges).',
        'hint_fr':         'Imagine chaque solide : a-t-il des surfaces courbes ? Compte ses faces plates, puis ses sommets (les pointes).',
        'hint_en':         'Picture each solid: does it have curved surfaces? Count its flat faces, then its vertices (the corners and tips).',
        'show_illustration': False,
        'shape_data':      [],
        'choices':         [],
        'pairs':           pairs,
        'explanation_en':  '\n'.join(f'{_SOLIDS_EN[n]} → {_SOLIDS_DESC_EN[n]}: {_SOLIDS_WHY[n][1]}.' for n in chosen),
        'explanation_fr':  '\n'.join(f'{n} → {_SOLIDS_FR[n][0]} : {_SOLIDS_WHY[n][0]}.' for n in chosen),
        'correct_answers': [p['right'] for p in pairs],
    }


# ─────────────────────────────────────────────────────────────────────────────
# perimeter_labeled_gen  (content2.md Thème 3, section 15)
# ─────────────────────────────────────────────────────────────────────────────

_PERIM_HINTS = {
    'rectangle': ('Un rectangle a 4 côtés et ses côtés opposés ont la même longueur. Additionne les 4 côtés.',
                  'A rectangle has 4 sides and its opposite sides are the same length. Add all 4 sides.'),
    'square': ('Un carré a 4 côtés de même longueur. Additionne les 4 côtés.',
               'A square has 4 sides of the same length. Add all 4 sides.'),
    'equilateral': ('Un triangle équilatéral a 3 côtés de même longueur. Additionne les 3 côtés.',
                    'An equilateral triangle has 3 sides of the same length. Add all 3 sides.'),
    'isosceles': ('Ce triangle a 3 côtés, dont 2 de même longueur. Additionne les 3 côtés.',
                  'This triangle has 3 sides, 2 of them the same length. Add all 3 sides.'),
}


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
            while leg == base or base >= 2 * leg:   # triangle inequality
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
            while leg == base or base >= 2 * leg:   # triangle inequality
                leg = random.randint(5, 50)
            sides = [leg, base, leg]
            svg = [{'type': 'labeled_triangle', 'sides': sides, 'unit': unit}]
            perimeter = 2 * leg + base

    sides_str = ' + '.join(str(s) for s in sides)

    return {
        'q_type':          'text_input',
        'prompt_fr':       "Quel est le périmètre de cet enclos (en cm) ?",
        'prompt_en':       "What is the perimeter of this enclosure (in cm)?",
        'hint_fr':         _PERIM_HINTS[shape_type][0],
        'hint_en':         _PERIM_HINTS[shape_type][1],
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
