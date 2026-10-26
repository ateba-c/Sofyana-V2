"""
statistics.py — Grade-3 statistics & probability generators (content2.md Thème 3 §16 + Thème 4 §27).

Topics:
  read_bar_chart_gen     typed_input + SVG – read a value from a bar chart
  probability_vocab_gen  QCM               – probability vocabulary (certain / probable / peu probable / impossible)

Difficulty (read_bar_chart_gen):
  easy   → 3 bars, values 2–8, a gridline for every unit
  medium → 4 bars, even values up to 16, a gridline every 2
  hard   → 4 bars, even values up to 24: how many MORE chose one pet than another

Every bar ends exactly on a gridline, so a value is read, never estimated.

Difficulty (probability_vocab_gen):
  easy   → certain or impossible
  medium → probable or peu probable
  hard   → any of the four terms, including equally probable
"""
import random

from quiz import illustrations as I

# ─────────────────────────────────────────────────────────────────────────────
# read_bar_chart_gen
# ─────────────────────────────────────────────────────────────────────────────

# All masculine in French (« un chat », « un oiseau »…), so the article is fixed.
_ANIMALS_FR = ["Chat", "Chien", "Hamster", "Oiseau", "Poisson", "Lapin"]
_ANIMALS_EN = ["Cat",  "Dog",   "Hamster", "Bird",   "Fish",    "Rabbit"]


def read_bar_chart_gen(level='easy'):
    if level == 'easy':
        n_bars, step = 3, 1
        values = random.sample(range(2, 9), n_bars)
    elif level == 'medium':
        n_bars, step = 4, 2
        values = random.sample(range(2, 17, 2), n_bars)
    else:
        n_bars, step = 4, 2
        values = random.sample(range(2, 25, 2), n_bars)

    selected = random.sample(range(len(_ANIMALS_FR)), n_bars)
    labels_fr = [_ANIMALS_FR[i] for i in selected]
    labels_en = [_ANIMALS_EN[i] for i in selected]
    chart = I.bar_chart(list(zip(labels_fr, labels_en)), values, color='multi', step=step)

    ask = random.randrange(n_bars)
    a_fr, a_en, a_val = labels_fr[ask].lower(), labels_en[ask].lower(), values[ask]

    if level == 'hard':
        # a reasoning step on top of the reading: compare two bars
        j = random.choice([k for k in range(n_bars) if k != ask])
        hi, lo = (ask, j) if values[ask] > values[j] else (j, ask)
        diff = values[hi] - values[lo]
        return {
            'q_type':          'text_input',
            'prompt_fr':       (f"Selon ce diagramme, combien d'élèves de plus ont un {labels_fr[hi].lower()} "
                                f"plutôt qu'un {labels_fr[lo].lower()} comme animal de compagnie ?"),
            'prompt_en':       (f"According to this chart, how many more students have a {labels_en[hi].lower()} "
                                f"than a {labels_en[lo].lower()} as a pet?"),
            'hint_fr':         "Lis la hauteur des deux barres sur l'axe vertical, puis soustrais la plus petite de la plus grande.",
            'hint_en':         "Read the height of both bars on the vertical axis, then subtract the smaller from the larger.",
            'show_illustration': True,
            'shape_data':      [chart],
            'choices':         [],
            'pairs':           [],
            'explanation_en': (
                f'Step 1: The "{labels_en[hi]}" bar reaches {values[hi]} and the "{labels_en[lo]}" bar reaches {values[lo]}.\n'
                f'Step 2: {values[hi]} − {values[lo]} = {diff}.\n'
                f'Answer: {diff} more student{"s" if diff != 1 else ""}.'
            ),
            'explanation_fr': (
                f'Étape 1 : La barre « {labels_fr[hi]} » monte à {values[hi]} et la barre « {labels_fr[lo]} » à {values[lo]}.\n'
                f'Étape 2 : {values[hi]} − {values[lo]} = {diff}.\n'
                f'Réponse : {diff} élève{"s" if diff != 1 else ""} de plus.'
            ),
            'correct_answers': [str(diff)],
        }

    return {
        'q_type':          'text_input',
        'prompt_fr':       f"Selon ce diagramme, combien d'élèves ont un {a_fr} comme animal de compagnie ?",
        'prompt_en':       f"According to this chart, how many students have a {a_en} as a pet?",
        'hint_fr':         "Repère la barre correspondant à l'animal et lis sa hauteur sur l'axe vertical.",
        'hint_en':         "Find the bar for that animal and read its height on the vertical axis.",
        'show_illustration': True,
        'shape_data':      [chart],
        'choices':         [],
        'pairs':           [],
        'explanation_en': (
            f'Step 1: Find the bar labelled "{labels_en[ask]}" in the chart.\n'
            f'Step 2: Read the height of that bar on the vertical axis.\n'
            f'Answer: {a_val} student{"s" if a_val != 1 else ""} {"have" if a_val != 1 else "has"} a {a_en} as a pet.'
        ),
        'explanation_fr': (
            f'Étape 1 : Repère la barre « {labels_fr[ask]} » dans le diagramme.\n'
            f'Étape 2 : Lis la hauteur de cette barre sur l\'axe vertical.\n'
            f'Réponse : {a_val} élève{"s" if a_val != 1 else ""} {"ont" if a_val != 1 else "a"} un {a_fr} comme animal de compagnie.'
        ),
        'correct_answers': [str(a_val)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# probability_vocab_gen
# ─────────────────────────────────────────────────────────────────────────────

# (singular feminine, plural feminine, English) — « orange » is invariable
_COLORS = [
    ("rouge",    "rouges",    "red"),
    ("bleue",    "bleues",    "blue"),
    ("verte",    "vertes",    "green"),
    ("jaune",    "jaunes",    "yellow"),
    ("orange",   "orange",    "orange"),
    ("violette", "violettes", "purple"),
]

_PROB_CHOICES_FR = ["Certain", "Probable", "Peu probable", "Impossible", "Également probable"]
_PROB_CHOICES_EN = ["Certain", "Likely",   "Unlikely",     "Impossible", "Equally likely"]

_ANSWERS = {
    'certain':      ("Certain", "Certain"),
    'impossible':   ("Impossible", "Impossible"),
    'probable':     ("Probable", "Likely"),
    'peu_probable': ("Peu probable", "Unlikely"),
    'egal':         ("Également probable", "Equally likely"),
}


def _article_en(word):
    return 'an' if word[0] in 'aeiou' else 'a'


def _build_scenario(level):
    """Return (scenario, total, other_count, target_count). The question is always about the target colour."""
    if level == 'easy':
        scenario = random.choice(['certain', 'impossible'])
        total = random.randint(5, 10)
    elif level == 'medium':
        scenario = random.choice(['probable', 'peu_probable'])
        total = random.randint(8, 12)
    else:
        scenario = random.choice(['certain', 'impossible', 'probable', 'peu_probable', 'egal'])
        total = random.randint(8, 16)
    if scenario == 'certain':
        return scenario, total, 0, total                  # every marble is the target colour
    if scenario == 'impossible':
        return scenario, total, total, 0                  # no marble of the target colour
    if scenario == 'probable':
        t = random.randint(total // 2 + 1, total - 1)     # more than half
        return scenario, total, total - t, t
    if scenario == 'peu_probable':
        t = random.randint(1, total // 4)                 # a small minority
        return scenario, total, total - t, t
    total += total % 2                                    # exactly half needs an even total
    return scenario, total, total // 2, total // 2


def _count_fr(n, col):
    sg, pl, _ = col
    return f"{n} bille{'s' if n > 1 else ''} {pl if n > 1 else sg}"


def _count_en(n, col):
    return f"{n} {col[2]} ball{'s' if n != 1 else ''}"


def probability_vocab_gen(level='easy'):
    other, target = random.sample(_COLORS, 2)
    scenario, total, n_other, n_target = _build_scenario(level)
    ans_fr, ans_en = _ANSWERS[scenario]
    t_sg, t_pl, t_en = target

    if n_target == 0:
        bag_fr = f"il y a {_count_fr(n_other, other)} et aucune bille {t_sg}"
        bag_en = f"there are {_count_en(n_other, other)} and no {t_en} balls"
    elif n_other == 0:
        bag_fr = f"il y a {_count_fr(n_target, target)} et rien d'autre"
        bag_en = f"there are {_count_en(n_target, target)} and nothing else"
    else:
        bag_fr = f"il y a {_count_fr(n_other, other)} et {_count_fr(n_target, target)}"
        bag_en = f"there are {_count_en(n_other, other)} and {_count_en(n_target, target)}"

    prompt_fr = f"Dans un sac, {bag_fr}. Piger une bille {t_sg} est un événement :"
    prompt_en = f"In a bag, {bag_en}. Drawing {_article_en(t_en)} {t_en} ball is an event that is:"

    choices_fixed = list(zip(_PROB_CHOICES_FR, _PROB_CHOICES_EN))
    random.shuffle(choices_fixed)
    choices = []
    for fr, en in choices_fixed:
        choices.append({
            'value':    fr,
            'label':    fr,
            'label_fr': fr,
            'label_en': en,
            'correct':  (fr == ans_fr),
            'error_type':     '' if fr == ans_fr else 'wrong_probability',
            'feedback_en': '' if fr == ans_fr else 'Think about how many of that colour are in the bag.',
            'feedback_fr': '' if fr == ans_fr else 'Pense au nombre de billes de cette couleur dans le sac.',
        })

    step1_en = f'Step 1: Count the {t_en} balls: {n_target} out of {total}.'
    step1_fr = f'Étape 1 : Compte les billes {t_pl} : {n_target} sur {total}.'
    if scenario == 'certain':
        step2_en = f'Step 2: Every ball in the bag is {t_en}, so drawing one is guaranteed.'
        step2_fr = f'Étape 2 : Toutes les billes du sac sont {t_pl}, donc on est sûr d\'en piger une.'
    elif scenario == 'impossible':
        step2_en = f'Step 2: There are no {t_en} balls at all, so drawing one cannot happen.'
        step2_fr = f'Étape 2 : Il n\'y a aucune bille {t_sg}, donc c\'est impossible d\'en piger une.'
    elif scenario == 'probable':
        step2_en = f'Step 2: {n_target} is more than half of {total}, so drawing one is likely.'
        step2_fr = f'Étape 2 : {n_target}, c\'est plus que la moitié de {total}, donc c\'est probable.'
    elif scenario == 'peu_probable':
        step2_en = f'Step 2: {n_target} is much less than half of {total}, so drawing one is unlikely.'
        step2_fr = f'Étape 2 : {n_target}, c\'est bien moins que la moitié de {total}, donc c\'est peu probable.'
    else:
        step2_en = f'Step 2: {n_target} is exactly half of {total}, so drawing one is as likely as not.'
        step2_fr = f'Étape 2 : {n_target}, c\'est exactement la moitié de {total}, donc c\'est également probable.'

    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       prompt_fr,
        'prompt_en':       prompt_en,
        'hint_fr':         ("Toutes les billes de cette couleur → certain. Aucune → impossible. "
                            "Plus de la moitié → probable. Exactement la moitié → également probable. "
                            "Moins de la moitié → peu probable."),
        'hint_en':         ("All balls that colour → certain. None → impossible. More than half → likely. "
                            "Exactly half → equally likely. Less than half → unlikely."),
        'show_illustration': False,
        'shape_data':      [],
        'choices':         choices,
        'pairs':           [],
        'explanation_en':  f'{step1_en}\n{step2_en}\nAnswer: {ans_en}',
        'explanation_fr':  f'{step1_fr}\n{step2_fr}\nRéponse : {ans_fr}',
        'correct_answers': [ans_fr],
    }
