"""
measurement.py — Grade-3 measurement generators (content2.md Thème 3 §15 + Thème 4 §26).

Topics:
  measure_unit_gen   QCM       – choose the right unit (mm / cm / m / km)
  read_clock_gen     QCM + SVG – read an analog clock (hours & minutes)

Difficulty (measure_unit_gen):
  easy   → obvious extremes (mm for cat's nose, km for migratory bird)
  medium → middle-range objects (cm / m)
  hard   → any unit, including trickier objects

Difficulty (read_clock_gen):
  easy   → hour and half-hour only (HH:00, HH:30)
  medium → quarter-hours (HH:00, HH:15, HH:30, HH:45)
  hard   → 5-minute intervals
"""
import random
from .base import _tagged_shuffle_mc

# ─────────────────────────────────────────────────────────────────────────────
# measure_unit_gen
# ─────────────────────────────────────────────────────────────────────────────

_OBJECTS = {
    'mm': [
        ("le nez d'un chat",                     "a cat's nose"),
        ("l'épaisseur d'une pièce de monnaie",   "the thickness of a coin"),
        ("la largeur d'un crayon",                "the width of a pencil"),
        ("le diamètre d'un grain de riz",         "the diameter of a grain of rice"),
    ],
    'cm': [
        ("la longueur d'un chien",                "the length of a dog"),
        ("la largeur d'un livre",                 "the width of a book"),
        ("la taille d'un lapin",                  "the height of a rabbit"),
        ("la longueur d'une gomme",               "the length of an eraser"),
    ],
    'm': [
        ("la hauteur d'une écurie",               "the height of a stable"),
        ("la longueur d'une piscine",             "the length of a swimming pool"),
        ("la taille d'un grand arbre",            "the height of a tall tree"),
        ("la largeur d'une salle de classe",      "the width of a classroom"),
    ],
    'km': [
        ("la distance parcourue par un oiseau migrateur", "the distance traveled by a migrating bird"),
        ("la distance entre deux villes",                 "the distance between two cities"),
        ("la longueur d'une rivière",                     "the length of a river"),
        ("la distance d'une randonnée en montagne",       "the distance of a mountain hike"),
    ],
}

_ALL_UNITS = ['mm', 'cm', 'm', 'km']
_MASS_UNITS = ['g', 'kg', 'L', 'mL']


def measure_unit_gen(level='easy'):
    if level == 'easy':
        unit = random.choice(['mm', 'km'])      # most obvious
    elif level == 'medium':
        unit = random.choice(['cm', 'm'])
    else:
        unit = random.choice(_ALL_UNITS)

    obj_fr, obj_en = random.choice(_OBJECTS[unit])

    wrong_len  = [u for u in _ALL_UNITS if u != unit]
    wrong_mass = random.choice(_MASS_UNITS)

    tagged_candidates = [
        (u, 'wrong_unit',
         "That unit is used for objects of a different size.",
         "Cette unité convient à des objets de taille différente.")
        for u in wrong_len
    ] + [
        (wrong_mass, 'wrong_quantity',
         "That unit measures mass (weight), not length.",
         "Cette unité mesure la masse, pas la longueur.")
    ]

    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       f"Quelle unité de mesure est la plus appropriée pour mesurer {obj_fr} ?",
        'prompt_en':       f"Which unit of measurement is most appropriate to measure {obj_en}?",
        'hint_fr':         "Pense à la taille de l'objet — est-il minuscule, moyen ou immense ?",
        'hint_en':         "Think about the size of the object — is it tiny, medium-sized, or huge?",
        'show_illustration': True,
        'shape_data':      [],
        'choices':         _tagged_shuffle_mc(unit, tagged_candidates),
        'pairs':           [],
        'explanation_en': (
            f'Step 1: Think about the size of "{obj_en}".\n'
            f'Step 2: Match the size to the appropriate unit — mm (tiny), cm (hand-sized), m (room-sized), km (city-to-city).\n'
            f'Answer: the best unit is {unit}.'
        ),
        'explanation_fr': (
            f'Étape 1 : Pense à la taille de « {obj_fr} ».\n'
            f'Étape 2 : Associe la taille à l\'unité appropriée — mm (minuscule), cm (à main), m (pièce), km (ville à ville).\n'
            f'Réponse : l\'unité la plus adaptée est {unit}.'
        ),
        'correct_answers': [unit],
    }


# ─────────────────────────────────────────────────────────────────────────────
# read_clock_gen
# ─────────────────────────────────────────────────────────────────────────────

def _fmt_time(h, m):
    """Return 'HH h MM' in French and 'H:MM AM/PM' in English."""
    fr = f"{h} h {m:02d}" if m else f"{h} h"
    period = "AM" if h < 12 else "PM"
    en = f"{h}:{m:02d} {period}"
    return fr, en


def _time_distractors(h, m):
    """Generate plausible wrong times."""
    wrong = set()
    # Swap hands
    wrong.add((m % 12 or 12, (h * 5) % 60))
    # ±1 hour
    wrong.add(((h % 12) + 1 or 12, m))
    wrong.add(((h - 2) % 12 or 12, m))
    # ±15 min
    wrong.add((h, (m + 15) % 60))
    wrong.add((h, (m + 30) % 60))
    return [t for t in wrong if t != (h, m)]


def read_clock_gen(level='easy'):
    if level == 'easy':
        h = random.randint(1, 12)
        m = random.choice([0, 30])
    elif level == 'medium':
        h = random.randint(1, 12)
        m = random.choice([0, 15, 30, 45])
    else:
        h = random.randint(1, 12)
        m = random.choice(range(0, 60, 5))

    correct_fr, correct_en = _fmt_time(h, m)
    distractors = _time_distractors(h, m)[:4]

    tagged_candidates = []
    for dh, dm in distractors:
        dfr, den = _fmt_time(dh, dm)
        tagged_candidates.append((
            dfr if True else den,   # we'll handle bilingual in choices below
            'wrong_time',
            "Look carefully at the position of both hands.",
            "Observe bien la position des deux aiguilles.",
        ))

    # Build bilingual choices manually (FR display, but store both)
    choices = _tagged_shuffle_mc(correct_fr, tagged_candidates)

    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       "Quelle heure indique cette horloge ?",
        'prompt_en':       "What time does this clock show?",
        'hint_fr':         "La petite aiguille indique les heures, la grande indique les minutes.",
        'hint_en':         "The short hand shows the hour, the long hand shows the minutes.",
        'show_illustration': True,
        'shape_data':      [{'type': 'clock', 'hours': h, 'minutes': m}],
        'choices':         choices,
        'pairs':           [],
        'explanation_en': (
            f'Step 1: The short (hour) hand points near {h} — it shows the hour.\n'
            f'Step 2: The long (minute) hand points to the {m // 5 if m else 12} — each number = 5 minutes, so {m} minutes.\n'
            f'Answer: {correct_en}'
        ),
        'explanation_fr': (
            f'Étape 1 : La petite aiguille (heures) pointe vers {h} — elle indique l\'heure.\n'
            f'Étape 2 : La grande aiguille (minutes) pointe vers le {m // 5 if m else 12} — chaque chiffre = 5 min, donc {m} min.\n'
            f'Réponse : {correct_fr}'
        ),
        'correct_answers': [correct_fr],
    }


# ─────────────────────────────────────────────────────────────────────────────
# time_convert_gen  (content3.md Bloc C, section C1)
# ─────────────────────────────────────────────────────────────────────────────

_TIME_FACTS = {
    'easy': [
        ('Combien de minutes y a-t-il dans 1 heure ?',
         'How many minutes are in 1 hour?',
         '60', ['30', '24', '100', '12']),
        ("Combien d'heures y a-t-il dans 1 jour ?",
         'How many hours are in 1 day?',
         '24', ['12', '60', '7', '36']),
        ("Combien de jours y a-t-il dans 1 semaine ?",
         'How many days are in 1 week?',
         '7', ['5', '10', '12', '6']),
        ("Combien de mois y a-t-il dans 1 an ?",
         'How many months are in 1 year?',
         '12', ['7', '10', '24', '52']),
    ],
    'medium': [
        ('Combien de secondes y a-t-il dans 1 minute ?',
         'How many seconds are in 1 minute?',
         '60', ['100', '30', '24', '12']),
        ("Combien de semaines y a-t-il dans 1 an ?",
         'How many weeks are in 1 year?',
         '52', ['12', '24', '365', '48']),
        ("1 heure et demie = ___ minutes",
         '1 and a half hours = ___ minutes',
         '90', ['60', '120', '150', '75']),
        ("2 heures = ___ minutes",
         '2 hours = ___ minutes',
         '120', ['60', '100', '180', '240']),
    ],
    'hard': [
        ("Combien de secondes y a-t-il dans 1 heure ?",
         'How many seconds are in 1 hour?',
         '3600', ['60', '600', '1440', '360']),
        ("Combien de minutes y a-t-il dans 2 heures 30 minutes ?",
         'How many minutes are in 2 hours and 30 minutes?',
         '150', ['130', '230', '120', '160']),
        ("1 jour et demi = ___ heures",
         '1 and a half days = ___ hours',
         '36', ['24', '48', '30', '12']),
        ("Combien de jours y a-t-il dans 2 semaines ?",
         'How many days are in 2 weeks?',
         '14', ['12', '10', '7', '21']),
    ],
}


def time_convert_gen(level='easy'):
    import random as _r
    from .base import _tagged_shuffle_mc as _mc

    fact = _r.choice(_TIME_FACTS[level])
    prompt_fr, prompt_en, answer, distractors = fact

    tagged_candidates = [
        (d, 'wrong_conversion',
         'Check the time facts.',
         'Vérifie les équivalences de temps.')
        for d in distractors
    ]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          '60 s = 1 min | 60 min = 1 h | 24 h = 1 jour | 7 jours = 1 semaine',
        'hint_en':          '60 s = 1 min | 60 min = 1 h | 24 h = 1 day | 7 days = 1 week',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _mc(answer, tagged_candidates),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Recall the time facts: 60 s = 1 min | 60 min = 1 h | 24 h = 1 day | 7 days = 1 week.\n'
            f'Step 2: Apply the correct conversion to the question.\n'
            f'Answer: {answer}'
        ),
        'explanation_fr': (
            f'Étape 1 : Rappelle-toi les équivalences : 60 s = 1 min | 60 min = 1 h | 24 h = 1 jour | 7 jours = 1 semaine.\n'
            f'Étape 2 : Applique la bonne conversion à la question.\n'
            f'Réponse : {answer}'
        ),
        'correct_answers':  [answer],
    }


# ─────────────────────────────────────────────────────────────────────────────
# unit_by_quantity_gen  (content3.md Bloc C, section C2)
# ─────────────────────────────────────────────────────────────────────────────

_QUANTITY_CONTEXTS = {
    'volume': {
        'easy': [
            ("Pour mesurer la quantité de jus dans un verre, j'utilise :",
             "To measure the amount of juice in a glass, I use:"),
            ("Pour mesurer le volume d'eau dans une bouteille, j'utilise :",
             "To measure the volume of water in a bottle, I use:"),
        ],
        'medium': [
            ("Pour mesurer la capacité d'une piscine, j'utilise :",
             "To measure the capacity of a swimming pool, I use:"),
            ("Pour mesurer la quantité de médicament dans une seringue, j'utilise :",
             "To measure the amount of medicine in a syringe, I use:"),
        ],
        'hard': [
            ("Pour mesurer la quantité d'essence dans le réservoir d'une voiture, j'utilise :",
             "To measure the fuel in a car's tank, I use:"),
            ("Pour remplir une baignoire, je mesure l'eau en :",
             "To fill a bathtub, I measure the water in:"),
        ],
        'answer': 'Litre (L)',
        'alt':    'Millilitre (mL)',
        'wrong':  ['Gramme (g)', 'Kilogramme (kg)', 'Mètre (m)', 'Kilomètre (km)'],
    },
    'mass': {
        'easy': [
            ("Pour mesurer le poids d'un chien, j'utilise :",
             "To measure the weight of a dog, I use:"),
            ("Pour mesurer la masse d'un sac de farine, j'utilise :",
             "To measure the mass of a bag of flour, I use:"),
        ],
        'medium': [
            ("Pour peser des épices dans une recette, j'utilise :",
             "To weigh spices in a recipe, I use:"),
            ("Pour mesurer la masse d'un élève, j'utilise :",
             "To measure a student's mass, I use:"),
        ],
        'hard': [
            ("Pour mesurer la masse d'une lettre avant de l'envoyer, j'utilise :",
             "To measure the mass of a letter before mailing it, I use:"),
            ("Pour peser un éléphant, j'utilise :",
             "To weigh an elephant, I use:"),
        ],
        'answer': 'Kilogramme (kg)',
        'alt':    'Gramme (g)',
        'wrong':  ['Litre (L)', 'Millilitre (mL)', 'Mètre (m)', 'Kilomètre (km)'],
    },
    'length': {
        'easy': [
            ("Pour mesurer la longueur d'une salle de classe, j'utilise :",
             "To measure the length of a classroom, I use:"),
            ("Pour mesurer la taille d'un enfant, j'utilise :",
             "To measure a child's height, I use:"),
        ],
        'medium': [
            ("Pour mesurer la distance entre deux maisons dans la même rue, j'utilise :",
             "To measure the distance between two houses on the same street, I use:"),
            ("Pour mesurer la longueur d'un terrain de soccer, j'utilise :",
             "To measure the length of a soccer field, I use:"),
        ],
        'hard': [
            ("Pour mesurer la distance entre Montréal et Québec, j'utilise :",
             "To measure the distance between Montreal and Quebec City, I use:"),
            ("Pour mesurer l'épaisseur d'une feuille de papier, j'utilise :",
             "To measure the thickness of a sheet of paper, I use:"),
        ],
        'answer': 'Mètre (m)',
        'alt':    'Centimètre (cm)',
        'wrong':  ['Gramme (g)', 'Kilogramme (kg)', 'Litre (L)', 'Millilitre (mL)'],
    },
}


def unit_by_quantity_gen(level='easy'):
    import random as _r
    from .base import _tagged_shuffle_mc as _mc

    qty = _r.choice(['volume', 'mass', 'length'])
    ctx = _QUANTITY_CONTEXTS[qty]
    prompt_fr, prompt_en = _r.choice(ctx[level])

    correct = ctx['answer']
    alt     = ctx['alt']

    tagged_candidates = [
        (alt, 'close_unit',
         'That unit measures the same quantity but at a different scale.',
         'Cette unité mesure la même grandeur mais à une autre échelle.'),
    ] + [
        (w, 'wrong_quantity',
         'That unit measures a different physical quantity.',
         'Cette unité mesure une grandeur physique différente.')
        for w in _r.sample(ctx['wrong'], 3)
    ]

    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Longueur → m/cm/mm/km | Masse → kg/g | Volume → L/mL',
        'hint_en':          'Length → m/cm/mm/km | Mass → kg/g | Volume → L/mL',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _mc(correct, tagged_candidates),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: Identify what is being measured (length, mass, or volume).\n'
            f'Step 2: Match to the standard unit — length: m/cm | mass: kg/g | volume: L/mL.\n'
            f'Answer: {correct}'
        ),
        'explanation_fr': (
            f'Étape 1 : Identifie ce qu\'on mesure (longueur, masse ou volume).\n'
            f'Étape 2 : Associe à l\'unité standard — longueur : m/cm | masse : kg/g | volume : L/mL.\n'
            f'Réponse : {correct}'
        ),
        'correct_answers':  [correct],
    }
