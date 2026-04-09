"""
statistics.py — Grade-3 statistics & probability generators (content2.md Thème 3 §16 + Thème 4 §27).

Topics:
  read_bar_chart_gen     typed_input + SVG – read a value from a bar chart
  probability_vocab_gen  QCM               – probability vocabulary (certain / probable / peu probable / impossible)

Difficulty (read_bar_chart_gen):
  easy   → 3 bars, max value ≤ 8
  medium → 4 bars, max value ≤ 15
  hard   → 4 bars, max value ≤ 25; non-even max on y-axis

Difficulty (probability_vocab_gen):
  easy   → certain or impossible
  medium → probable or peu probable
  hard   → any of the four terms, including equally probable
"""
import random
from .base import _tagged_shuffle_mc

# ─────────────────────────────────────────────────────────────────────────────
# read_bar_chart_gen
# ─────────────────────────────────────────────────────────────────────────────

_ANIMALS_FR = ["Chat", "Chien", "Hamster", "Oiseau", "Poisson", "Lapin"]
_ANIMALS_EN = ["Cat",  "Dog",   "Hamster", "Bird",   "Fish",    "Rabbit"]


def read_bar_chart_gen(level='easy'):
    if level == 'easy':
        n_bars  = 3
        max_val = 8
    elif level == 'medium':
        n_bars  = 4
        max_val = 15
    else:
        n_bars  = 4
        max_val = 25

    # Shuffle animals and pick n_bars
    idxs = list(range(len(_ANIMALS_FR)))
    random.shuffle(idxs)
    selected = idxs[:n_bars]

    labels_fr = [_ANIMALS_FR[i] for i in selected]
    labels_en = [_ANIMALS_EN[i] for i in selected]
    values    = [random.randint(2, max_val) for _ in range(n_bars)]

    # Ask about a random bar
    ask_idx   = random.randint(0, n_bars - 1)
    ask_lbl_fr = labels_fr[ask_idx]
    ask_lbl_en = labels_en[ask_idx]
    correct    = values[ask_idx]

    return {
        'q_type':          'text_input',
        'prompt_fr':       f"Selon ce diagramme, combien d'élèves ont un(e) {ask_lbl_fr} comme animal de compagnie ?",
        'prompt_en':       f"According to this chart, how many students have a {ask_lbl_en} as a pet?",
        'hint_fr':         "Repère la barre correspondant à l'animal et lis sa hauteur sur l'axe vertical.",
        'hint_en':         "Find the bar for that animal and read its height on the vertical axis.",
        'show_illustration': True,
        'shape_data':      [{
            'type':         'bar_chart',
            'chart_labels': labels_fr,
            'chart_values': values,
            'highlight':    ask_lbl_fr,
        }],
        'choices':         [],
        'pairs':           [],
        'explanation_en': (
            f'Step 1: Find the bar labelled "{ask_lbl_en}" in the chart.\n'
            f'Step 2: Read the height of that bar on the vertical axis.\n'
            f'Answer: {correct} student{"s" if correct != 1 else ""} have a {ask_lbl_en} as a pet.'
        ),
        'explanation_fr': (
            f'Étape 1 : Repère la barre « {ask_lbl_fr} » dans le diagramme.\n'
            f'Étape 2 : Lis la hauteur de cette barre sur l\'axe vertical.\n'
            f'Réponse : {correct} élève{"s" if correct != 1 else ""} {"ont" if correct != 1 else "a"} un(e) {ask_lbl_fr} comme animal de compagnie.'
        ),
        'correct_answers': [str(correct)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# probability_vocab_gen
# ─────────────────────────────────────────────────────────────────────────────

_COLORS_FR = ["rouge", "bleue", "verte", "jaune", "orange", "violette"]
_COLORS_EN = ["red",   "blue",  "green", "yellow","orange", "purple"]


_PROB_CHOICES_FR = ["Certain", "Probable", "Peu probable", "Impossible", "Également probable"]
_PROB_CHOICES_EN = ["Certain", "Likely",   "Unlikely",     "Impossible", "Equally likely"]

# Each scenario: (total, target_count) → (fr_answer, en_answer, fr_prompt_extra, en_prompt_extra)
def _build_scenario(level):
    """Return (total_balls, color1_count, color2_count, answer_fr, answer_en)."""
    if level == 'easy':
        # All same color (certain) or 0 of target (impossible)
        scenario = random.choice(['certain', 'impossible'])
        total = random.randint(5, 10)
        if scenario == 'certain':
            return total, total, 0, "Certain", "Certain"
        else:
            return total, total, 0, "Impossible", "Impossible"
    elif level == 'medium':
        scenario = random.choice(['probable', 'peu_probable'])
        total = random.randint(8, 12)
        if scenario == 'probable':
            c2 = random.randint(total // 2 + 1, total - 1)   # majority
            return total, total - c2, c2, "Probable", "Likely"
        else:
            c2 = random.randint(1, total // 4)                # small minority
            return total, total - c2, c2, "Peu probable", "Unlikely"
    else:
        scenario = random.choice(['certain', 'impossible', 'probable', 'peu_probable', 'egal'])
        total = random.randint(8, 16)
        if scenario == 'certain':
            return total, total, 0, "Certain", "Certain"
        elif scenario == 'impossible':
            return total, total, 0, "Impossible", "Impossible"
        elif scenario == 'probable':
            c2 = random.randint(total // 2 + 1, total - 1)
            return total, total - c2, c2, "Probable", "Likely"
        elif scenario == 'peu_probable':
            c2 = random.randint(1, total // 4)
            return total, total - c2, c2, "Peu probable", "Unlikely"
        else:  # egal
            half = total // 2
            return total, half, total - half, "Également probable", "Equally likely"


def probability_vocab_gen(level='easy'):
    ci, cj = random.sample(range(len(_COLORS_FR)), 2)
    color1_fr, color1_en = _COLORS_FR[ci], _COLORS_EN[ci]
    color2_fr, color2_en = _COLORS_FR[cj], _COLORS_EN[cj]

    total, c1, c2, ans_fr, ans_en = _build_scenario(level)

    if level == 'easy' and ans_fr == 'Certain':
        c1, c2 = total, 0
    elif level == 'easy' and ans_fr == 'Impossible':
        c1, c2 = total, 0    # bag has only color1, ask about color2

    container_fr = "Dans un sac"
    container_en = "In a bag"

    if c2 == 0:
        # No color2 balls at all
        bag_desc_fr = f"il y a {c1} billes {color1_fr} et aucune bille {color2_fr}"
        bag_desc_en = f"there are {c1} {color1_en} balls and no {color2_en} balls"
    else:
        bag_desc_fr = f"il y a {c1} billes {color1_fr} et {c2} bille{'s' if c2 > 1 else ''} {color2_fr}"
        bag_desc_en = f"there are {c1} {color1_en} ball{'s' if c1 > 1 else ''} and {c2} {color2_en} ball{'s' if c2 > 1 else ''}"

    prompt_fr = f"{container_fr}, {bag_desc_fr}. Piger une bille {color2_fr} est un événement :"
    prompt_en = f"{container_en}, {bag_desc_en}. Drawing a {color2_en} ball is an event that is:"

    # Fixed 5-choice list (same order always)
    choices_fixed = list(zip(_PROB_CHOICES_FR, _PROB_CHOICES_EN))
    random.shuffle(choices_fixed)

    choices = []
    for fr, en in choices_fixed:
        choices.append({
            'value':    fr,
            'label_fr': fr,
            'label_en': en,
            'correct':  (fr == ans_fr),
            'error_type':     '' if fr == ans_fr else 'wrong_probability',
            'feedback_en': '' if fr == ans_fr else 'Think about how many of that colour are in the bag.',
            'feedback_fr': '' if fr == ans_fr else 'Pense au nombre de billes de cette couleur dans le sac.',
        })

    if ans_fr == 'Certain':
        explanation_en = (f'Step 1: Count the {color2_en} balls: all {total} balls are {color2_en}.\n'
                          f'Step 2: Since every ball is {color2_en}, drawing one is guaranteed.\nAnswer: Certain')
        explanation_fr = (f'Étape 1 : Compte les billes {color2_fr} : toutes les {total} billes sont {color2_fr}.\n'
                          f'Étape 2 : Puisque toutes les billes sont {color2_fr}, piger l\'une d\'elles est garanti.\nRéponse : Certain')
    elif ans_fr == 'Impossible':
        explanation_en = (f'Step 1: Count the {color2_en} balls: there are 0 {color2_en} balls out of {total}.\n'
                          f'Step 2: There are no {color2_en} balls at all, so drawing one cannot happen.\nAnswer: Impossible')
        explanation_fr = (f'Étape 1 : Compte les billes {color2_fr} : il y a 0 bille {color2_fr} sur {total}.\n'
                          f'Étape 2 : Il n\'y a aucune bille {color2_fr}, donc piger est impossible.\nRéponse : Impossible')
    elif ans_fr == 'Probable':
        explanation_en = (f'Step 1: Count the {color2_en} balls: {c2} out of {total}.\n'
                          f'Step 2: {c2}/{total} is more than half, so drawing one is likely.\nAnswer: Likely')
        explanation_fr = (f'Étape 1 : Compte les billes {color2_fr} : {c2} sur {total}.\n'
                          f'Étape 2 : {c2}/{total} dépasse la moitié, donc piger est probable.\nRéponse : Probable')
    elif ans_fr == 'Peu probable':
        explanation_en = (f'Step 1: Count the {color2_en} balls: {c2} out of {total}.\n'
                          f'Step 2: {c2}/{total} is less than half, so drawing one is unlikely.\nAnswer: Unlikely')
        explanation_fr = (f'Étape 1 : Compte les billes {color2_fr} : {c2} sur {total}.\n'
                          f'Étape 2 : {c2}/{total} est inférieur à la moitié, donc piger est peu probable.\nRéponse : Peu probable')
    else:
        explanation_en = (f'Step 1: Count the {color2_en} balls: {c2} out of {total}.\n'
                          f'Step 2: Exactly half the balls are {color2_en}, so it is equally likely to draw one or not.\nAnswer: Equally likely')
        explanation_fr = (f'Étape 1 : Compte les billes {color2_fr} : {c2} sur {total}.\n'
                          f'Étape 2 : Exactement la moitié des billes sont {color2_fr}, donc c\'est également probable.\nRéponse : Également probable')

    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         "Si toutes les billes sont de cette couleur → certain. Si aucune → impossible. Entre les deux → probable ou peu probable.",
        'hint_en':         "If all balls are that colour → certain. If none → impossible. In between → likely or unlikely.",
        'show_illustration': False,
        'shape_data':      [],
        'choices':         choices,
        'pairs':           [],
        'explanation_en':  explanation_en,
        'explanation_fr':  explanation_fr,
        'correct_answers': [ans_fr],
    }
