"""
space.py — Grade-3 spatial reasoning generators (content3.md Bloc B, section B2).

Topics:
  cartesian_coord_gen   typed_input + SVG – read (x, y) coordinates from a grid

Difficulty:
  easy   → grid 0-4, ask only for x-value
  medium → grid 0-6, ask only for y-value
  hard   → grid 0-8, ask for both "(x, y)"
"""
import random


def cartesian_coord_gen(level='easy'):
    if level == 'easy':
        size = 4
        ask = 'x'
    elif level == 'medium':
        size = 6
        ask = 'y'
    else:
        size = 8
        ask = 'both'

    # Avoid the origin and edges for clarity
    px = random.randint(1, size - 1)
    py = random.randint(1, size - 1)

    if ask == 'x':
        correct = [str(px)]
        prompt_fr = f"Quel est l'abscisse (valeur de x) du point A sur ce repère ?"
        prompt_en = f"What is the x-coordinate of point A on this grid?"
        hint_fr   = "Lis la valeur en dessous du point sur l'axe horizontal (axe des x)."
        hint_en   = "Read the value below the point on the horizontal axis (x-axis)."
    elif ask == 'y':
        correct = [str(py)]
        prompt_fr = "Quel est l'ordonnée (valeur de y) du point A sur ce repère ?"
        prompt_en = "What is the y-coordinate of point A on this grid?"
        hint_fr   = "Lis la valeur à gauche du point sur l'axe vertical (axe des y)."
        hint_en   = "Read the value to the left of the point on the vertical axis (y-axis)."
    else:
        correct = [f"({px}, {py})", f"{px}, {py}", f"{px},{py}"]
        prompt_fr = "Quelles sont les coordonnées du point A ? (Écris sous la forme x, y)"
        prompt_en = "What are the coordinates of point A? (Write as x, y)"
        hint_fr   = "L'abscisse (x) se lit en premier, puis l'ordonnée (y)."
        hint_en   = "The x-coordinate comes first, then the y-coordinate."

    return {
        'q_type':          'text_input',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         hint_fr,
        'hint_en':         hint_en,
        'show_illustration': True,
        'shape_data':      [{'type': 'grid_point', 'px': px, 'py': py, 'grid_size': size}],
        'choices':         [],
        'pairs':           [],
        'explanation_en': (
            f'Step 1: Locate point A on the grid.\n'
            f'Step 2: Read the x-coordinate (horizontal axis) = {px}.\n'
            f'Step 3: Read the y-coordinate (vertical axis) = {py}.\n'
            f'Answer: point A is at ({px}, {py})'
        ),
        'explanation_fr': (
            f'Étape 1 : Repère le point A sur le repère.\n'
            f'Étape 2 : Lis l\'abscisse (axe horizontal) = {px}.\n'
            f'Étape 3 : Lis l\'ordonnée (axe vertical) = {py}.\n'
            f'Réponse : le point A est en ({px}, {py})'
        ),
        'correct_answers': correct,
    }
