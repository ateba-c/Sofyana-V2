"""
measurement.py — Grade-3 measurement generators (content2.md Thème 3 §15 + Thème 4 §26).

Topics:
  measure_unit_gen      QCM       – choose the right unit (mm / cm / m / km)
  read_clock_gen        QCM + SVG – read an analog clock (hours & minutes)
  time_convert_gen      QCM       – time facts (60 min = 1 h, 7 days = 1 week…)
  unit_by_quantity_gen  QCM       – choose the unit that fits the quantity (length / mass / capacity)

Difficulty (measure_unit_gen):
  easy   → obvious extremes (mm for a grain of rice, km between two cities)
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

# Each thing sits clearly inside one unit's range (no cat's nose, which is about 2 cm).
_OBJECTS = {
    'mm': [
        ("l'épaisseur d'une pièce de monnaie",   "the thickness of a coin"),
        ("la largeur d'une mine de crayon",       "the width of a pencil lead"),
        ("la longueur d'un grain de riz",         "the length of a grain of rice"),
        ("la longueur d'une fourmi",              "the length of an ant"),
    ],
    'cm': [
        ("la longueur d'un crayon",               "the length of a pencil"),
        ("la largeur d'un livre",                 "the width of a book"),
        ("la taille d'un lapin",                  "the height of a rabbit"),
        ("la longueur d'une gomme à effacer",     "the length of an eraser"),
    ],
    'm': [
        ("la hauteur d'une maison",               "the height of a house"),
        ("la longueur d'une piscine",             "the length of a swimming pool"),
        ("la hauteur d'un grand arbre",           "the height of a tall tree"),
        ("la largeur d'une salle de classe",      "the width of a classroom"),
    ],
    'km': [
        ("la distance parcourue par un oiseau migrateur", "the distance travelled by a migrating bird"),
        ("la distance entre deux villes",                 "the distance between two cities"),
        ("la longueur d'une rivière",                     "the length of a river"),
        ("la distance d'une randonnée en montagne",       "the distance of a mountain hike"),
    ],
}

# Why this unit fits — and why not the neighbouring one.
_UNIT_WHY = {
    'mm': ("C'est plus petit qu'un centimètre : on compte en millimètres.",
           "It is smaller than a centimetre, so we count in millimetres."),
    'cm': ("Ça tient dans la main ou sur une table : plus grand qu'un millimètre, plus petit qu'un mètre. On utilise le centimètre.",
           "It fits in your hand or on a table: bigger than a millimetre, smaller than a metre. We use centimetres."),
    'm':  ("C'est plus grand que toi, mais on peut le parcourir en quelques pas : on utilise le mètre.",
           "It is bigger than you, but you can cross it in a few steps, so we use metres."),
    'km': ("Il faudrait marcher longtemps, ou prendre la voiture : on utilise le kilomètre.",
           "You would have to walk a long time or take a car, so we use kilometres."),
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

    wrong_len = [u for u in _ALL_UNITS if u != unit]
    tagged_candidates = [
        (u, 'wrong_unit',
         "That unit is used for things of a different size.",
         "Cette unité convient à des choses de taille différente.")
        for u in wrong_len
    ]
    # A mass / capacity unit only sometimes, so most questions are about neighbouring length units.
    if level != 'hard' or random.random() < 0.5:
        tagged_candidates.insert(random.randrange(len(tagged_candidates) + 1), (
            random.choice(_MASS_UNITS), 'wrong_quantity',
            "That unit measures mass or capacity, not length.",
            "Cette unité mesure une masse ou une capacité, pas une longueur."))
    why_fr, why_en = _UNIT_WHY[unit]

    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       f"Quelle unité de mesure est la plus appropriée pour mesurer {obj_fr} ?",
        'prompt_en':       f"Which unit of measurement is most appropriate to measure {obj_en}?",
        'hint_fr':         "Imagine ce qu'on mesure : est-ce minuscule, de la taille de ta main, grand comme une pièce, ou très loin ?",
        'hint_en':         "Picture what is being measured: is it tiny, hand-sized, as big as a room, or very far?",
        'show_illustration': True,
        'shape_data':      [],
        'choices':         _tagged_shuffle_mc(unit, tagged_candidates),
        'pairs':           [],
        'explanation_en': (
            f'Step 1: Picture {obj_en}.\n'
            f'Step 2: {why_en}\n'
            f'Answer: the best unit is {unit}.'
        ),
        'explanation_fr': (
            f'Étape 1 : Imagine {obj_fr}.\n'
            f'Étape 2 : {why_fr}\n'
            f'Réponse : l\'unité la plus adaptée est {unit}.'
        ),
        'correct_answers': [unit],
    }


# ─────────────────────────────────────────────────────────────────────────────
# read_clock_gen
# ─────────────────────────────────────────────────────────────────────────────

def _fmt_time(h, m):
    """'9 h 45' in French and '9:45' in English (the face shows no AM/PM)."""
    fr = f"{h} h {m:02d}" if m else f"{h} h"
    en = f"{h}:{m:02d}"
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
            dfr,    # « 9 h 45 » — shown as 9:45 in English by labels.translate_label
            'wrong_time',
            "Look carefully at the position of both hands.",
            "Observe bien la position des deux aiguilles.",
        ))

    choices = _tagged_shuffle_mc(correct_fr, tagged_candidates)

    nxt = h % 12 + 1
    if m == 0:
        hour_fr = f"La petite aiguille (heures) pointe exactement sur le {h} : il est {h} h pile."
        hour_en = f"The short (hour) hand points exactly at {h}: it is {h} o'clock."
    else:
        hour_fr = (f"La petite aiguille (heures) est entre le {h} et le {nxt}"
                   + (f", tout près du {nxt}" if m >= 45 else '') + f" : l'heure est encore {h}.")
        hour_en = (f"The short (hour) hand is between {h} and {nxt}"
                   + (f", very close to {nxt}" if m >= 45 else '') + f": the hour is still {h}.")
    if m == 0:
        min_fr = "La grande aiguille (minutes) pointe sur le 12 : 0 minute."
        min_en = "The long (minute) hand points at 12: 0 minutes."
    else:
        min_fr = f"La grande aiguille (minutes) pointe sur le {m // 5} — chaque chiffre = 5 min, donc {m // 5} × 5 = {m} min."
        min_en = f"The long (minute) hand points at {m // 5} — each number = 5 minutes, so {m // 5} × 5 = {m} minutes."

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
        'explanation_en':  f'Step 1: {hour_en}\nStep 2: {min_en}\nAnswer: {correct_en}',
        'explanation_fr':  f'Étape 1 : {hour_fr}\nÉtape 2 : {min_fr}\nRéponse : {correct_fr}',
        'correct_answers': [correct_fr],
    }


# ─────────────────────────────────────────────────────────────────────────────
# time_convert_gen  (content3.md Bloc C, section C1)
# ─────────────────────────────────────────────────────────────────────────────

# (prompt_fr, prompt_en, answer, distractors, hint (fr, en), explanation step (fr, en))
# The hint never states the very fact that is asked; the explanation shows the calculation.
_TIME_FACTS = {
    'easy': [
        ('Combien de minutes y a-t-il dans 1 heure ?', 'How many minutes are in 1 hour?',
         '60', ['30', '24', '100', '12'],
         ("Pense à la grande aiguille : elle fait un tour complet de l'horloge en 1 heure, et chaque chiffre vaut 5 minutes.",
          'Think of the long hand: it goes all the way around the clock in 1 hour, and each number is worth 5 minutes.'),
         ('12 chiffres × 5 min = 60 min', '12 numbers × 5 min = 60 minutes')),
        ("Combien d'heures y a-t-il dans 1 jour ?", 'How many hours are in 1 day?',
         '24', ['12', '60', '7', '36'],
         ("La petite aiguille fait 2 tours d'horloge en un jour : un tour le matin, un tour l'après-midi et le soir.",
          'The short hand goes around the clock twice in a day: once in the morning, once in the afternoon and evening.'),
         ('2 tours × 12 h = 24 h', '2 turns × 12 hours = 24 hours')),
        ("Combien de jours y a-t-il dans 1 semaine ?", 'How many days are in 1 week?',
         '7', ['5', '10', '12', '6'],
         ('Récite les jours : lundi, mardi, mercredi…', 'Say the days: Monday, Tuesday, Wednesday…'),
         ('lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche : 7 jours',
          'Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: 7 days')),
        ("Combien de mois y a-t-il dans 1 an ?", 'How many months are in 1 year?',
         '12', ['7', '10', '24', '52'],
         ('Récite les mois : janvier, février, mars…', 'Say the months: January, February, March…'),
         ('de janvier à décembre, on compte 12 mois', 'from January to December there are 12 months')),
    ],
    'medium': [
        ('Combien de secondes y a-t-il dans 1 minute ?', 'How many seconds are in 1 minute?',
         '60', ['100', '30', '24', '12'],
         ("Une minute se découpe comme une heure : en autant de petites parties qu'il y a de minutes dans une heure.",
          'A minute splits up like an hour: into as many small parts as there are minutes in an hour.'),
         ('1 min = 60 s (comme 1 h = 60 min)', '1 minute = 60 seconds (just like 1 hour = 60 minutes)')),
        ("Combien de semaines y a-t-il dans 1 an ?", 'How many weeks are in 1 year?',
         '52', ['12', '24', '365', '48'],
         ('Un an a 365 jours, et une semaine a 7 jours.', 'A year has 365 days, and a week has 7 days.'),
         ('365 ÷ 7 = 52 semaines (et 1 jour de plus)', '365 ÷ 7 = 52 weeks (and 1 day left over)')),
        ("1 heure et demie = ___ minutes", '1 and a half hours = ___ minutes',
         '90', ['60', '120', '150', '75'],
         ('Une demi-heure, c\'est la moitié de 60 minutes.', 'Half an hour is half of 60 minutes.'),
         ('1 h = 60 min et une demi-heure = 30 min : 60 + 30 = 90 min',
          '1 hour = 60 minutes and half an hour = 30 minutes: 60 + 30 = 90 minutes')),
        ("2 heures = ___ minutes", '2 hours = ___ minutes',
         '120', ['60', '100', '180', '240'],
         ('1 h = 60 min. Pour 2 h, compte 60 deux fois.', '1 hour = 60 minutes. For 2 hours, count 60 twice.'),
         ('2 × 60 = 120 min', '2 × 60 = 120 minutes')),
    ],
    'hard': [
        ("Combien de secondes y a-t-il dans 1 heure ?", 'How many seconds are in 1 hour?',
         '3600', ['60', '600', '1440', '360'],
         ('1 h = 60 min et 1 min = 60 s.', '1 hour = 60 minutes and 1 minute = 60 seconds.'),
         ('60 min × 60 s = 3600 s', '60 minutes × 60 seconds = 3600 seconds')),
        ("Combien de minutes y a-t-il dans 2 heures 30 minutes ?", 'How many minutes are in 2 hours and 30 minutes?',
         '150', ['130', '230', '120', '160'],
         ('Change les heures en minutes (1 h = 60 min), puis ajoute les 30 minutes.',
          'Change the hours into minutes (1 hour = 60 minutes), then add the 30 minutes.'),
         ('2 × 60 = 120 min, puis 120 + 30 = 150 min', '2 × 60 = 120 minutes, then 120 + 30 = 150 minutes')),
        ("1 jour et demi = ___ heures", '1 and a half days = ___ hours',
         '36', ['24', '48', '30', '12'],
         ('1 jour = 24 h. Un demi-jour, c\'est la moitié de 24 h.', '1 day = 24 hours. Half a day is half of 24 hours.'),
         ('24 h + 12 h = 36 h', '24 hours + 12 hours = 36 hours')),
        ("Combien de jours y a-t-il dans 2 semaines ?", 'How many days are in 2 weeks?',
         '14', ['12', '10', '7', '21'],
         ('1 semaine = 7 jours. Compte 7 deux fois.', '1 week = 7 days. Count 7 twice.'),
         ('7 + 7 = 14 jours', '7 + 7 = 14 days')),
    ],
}


def time_convert_gen(level='easy'):
    prompt_fr, prompt_en, answer, distractors, (hint_fr, hint_en), (calc_fr, calc_en) = random.choice(_TIME_FACTS[level])

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
        'hint_fr':          hint_fr,
        'hint_en':          hint_en,
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(answer, tagged_candidates),
        'pairs':            [],
        'explanation_en':   f'Step 1: {calc_en}.\nAnswer: {answer}',
        'explanation_fr':   f'Étape 1 : {calc_fr}.\nRéponse : {answer}',
        'correct_answers':  [answer],
    }


# ─────────────────────────────────────────────────────────────────────────────
# unit_by_quantity_gen  (content3.md Bloc C, section C2)
# ─────────────────────────────────────────────────────────────────────────────

_UNIT_LABELS = {
    'mm': ('Millimètre (mm)', 'Millimetre (mm)'), 'cm': ('Centimètre (cm)', 'Centimetre (cm)'),
    'm': ('Mètre (m)', 'Metre (m)'), 'km': ('Kilomètre (km)', 'Kilometre (km)'),
    'g': ('Gramme (g)', 'Gram (g)'), 'kg': ('Kilogramme (kg)', 'Kilogram (kg)'),
    'mL': ('Millilitre (mL)', 'Millilitre (mL)'), 'L': ('Litre (L)', 'Litre (L)'),
}
_QTY_UNITS = {'length': ['mm', 'cm', 'm', 'km'], 'mass': ['g', 'kg'], 'volume': ['mL', 'L']}
_QTY_NAMES = {'length': ('une longueur', 'a length'), 'mass': ('une masse', 'a mass'), 'volume': ('une capacité', 'a capacity')}

# (prompt_fr, prompt_en, right unit, why fr, why en) — each context has ONE clearly right unit.
_QUANTITY_CONTEXTS = {
    'volume': {
        'easy': [
            ("Pour mesurer la quantité de jus dans un verre, j'utilise :",
             "To measure the amount of juice in a glass, I use:", 'mL',
             'un verre contient peu de liquide', 'a glass holds only a little liquid'),
            ("Pour mesurer la quantité d'eau dans un grand seau, j'utilise :",
             "To measure the amount of water in a big bucket, I use:", 'L',
             'un grand seau contient beaucoup d\'eau', 'a big bucket holds a lot of water'),
        ],
        'medium': [
            ("Pour mesurer la capacité d'une piscine, j'utilise :",
             "To measure the capacity of a swimming pool, I use:", 'L',
             'une piscine contient énormément d\'eau', 'a pool holds a huge amount of water'),
            ("Pour mesurer la quantité de médicament dans une seringue, j'utilise :",
             "To measure the amount of medicine in a syringe, I use:", 'mL',
             'une seringue contient très peu de liquide', 'a syringe holds very little liquid'),
        ],
        'hard': [
            ("Pour mesurer la quantité d'essence dans le réservoir d'une voiture, j'utilise :",
             "To measure the fuel in a car's tank, I use:", 'L',
             'un réservoir contient des dizaines de litres', 'a tank holds tens of litres'),
            ("Pour mesurer une cuillerée de sirop, j'utilise :",
             "To measure a spoonful of syrup, I use:", 'mL',
             'une cuillère contient quelques millilitres', 'a spoon holds just a few millilitres'),
        ],
    },
    'mass': {
        'easy': [
            ("Pour mesurer la masse d'un chien, j'utilise :",
             "To measure the mass of a dog, I use:", 'kg',
             'un chien est lourd', 'a dog is heavy'),
            ("Pour mesurer la masse d'un sac de farine, j'utilise :",
             "To measure the mass of a bag of flour, I use:", 'kg',
             'un sac de farine est lourd', 'a bag of flour is heavy'),
        ],
        'medium': [
            ("Pour peser des épices dans une recette, j'utilise :",
             "To weigh spices in a recipe, I use:", 'g',
             'quelques épices sont très légères', 'a few spices are very light'),
            ("Pour mesurer la masse d'un élève, j'utilise :",
             "To measure a student's mass, I use:", 'kg',
             'un élève est lourd', 'a student is heavy'),
        ],
        'hard': [
            ("Pour mesurer la masse d'une lettre avant de l'envoyer, j'utilise :",
             "To measure the mass of a letter before mailing it, I use:", 'g',
             'une lettre est très légère', 'a letter is very light'),
            ("Pour peser un éléphant, j'utilise :",
             "To weigh an elephant, I use:", 'kg',
             'un éléphant est très lourd', 'an elephant is very heavy'),
        ],
    },
    'length': {
        'easy': [
            ("Pour mesurer la longueur d'une salle de classe, j'utilise :",
             "To measure the length of a classroom, I use:", 'm',
             'une classe se traverse en quelques pas', 'you cross a classroom in a few steps'),
            ("Pour mesurer la longueur d'un crayon, j'utilise :",
             "To measure the length of a pencil, I use:", 'cm',
             'un crayon tient dans la main', 'a pencil fits in your hand'),
        ],
        'medium': [
            ("Pour mesurer la distance entre deux maisons dans la même rue, j'utilise :",
             "To measure the distance between two houses on the same street, I use:", 'm',
             'deux maisons voisines sont à quelques pas', 'two houses on a street are a few steps apart'),
            ("Pour mesurer la longueur d'un terrain de soccer, j'utilise :",
             "To measure the length of a soccer field, I use:", 'm',
             'un terrain de soccer mesure une centaine de mètres', 'a soccer field is about a hundred metres long'),
        ],
        'hard': [
            ("Pour mesurer la distance entre Montréal et Québec, j'utilise :",
             "To measure the distance between Montreal and Quebec City, I use:", 'km',
             "entre deux villes, c'est très loin", 'two cities are very far apart'),
            ("Pour mesurer l'épaisseur d'une feuille de papier, j'utilise :",
             "To measure the thickness of a sheet of paper, I use:", 'mm',
             'une feuille est plus mince qu\'un centimètre', 'a sheet is thinner than a centimetre'),
        ],
    },
}


def unit_by_quantity_gen(level='easy'):
    qty = random.choice(['volume', 'mass', 'length'])
    prompt_fr, prompt_en, unit, why_fr, why_en = random.choice(_QUANTITY_CONTEXTS[qty][level])
    correct = _UNIT_LABELS[unit]

    same = [u for u in _QTY_UNITS[qty] if u != unit]
    other = [u for q, us in _QTY_UNITS.items() if q != qty for u in us]
    picks = same[:2] + random.sample(other, 4 - len(same[:2]))
    tagged_candidates = [
        (_UNIT_LABELS[u], 'close_unit',
         'That unit measures the same quantity but at a different scale.',
         'Cette unité mesure la même grandeur, mais à une autre échelle.')
        if u in same else
        (_UNIT_LABELS[u], 'wrong_quantity',
         'That unit measures a different quantity.',
         'Cette unité mesure une autre grandeur.')
        for u in picks
    ]
    q_fr, q_en = _QTY_NAMES[qty]
    return {
        'q_type':           'multiple_choice',
        'prompt_fr':        prompt_fr,
        'prompt_en':        prompt_en,
        'hint_fr':          'Longueur : mm, cm, m, km. Masse : g, kg. Capacité : mL, L. Puis choisis la petite ou la grande unité.',
        'hint_en':          'Length: mm, cm, m, km. Mass: g, kg. Capacity: mL, L. Then pick the small or the big unit.',
        'show_illustration': False,
        'shape_data':       [],
        'choices':          _tagged_shuffle_mc(correct, tagged_candidates),
        'pairs':            [],
        'explanation_en': (
            f'Step 1: We measure {q_en}.\n'
            f'Step 2: {why_en[0].upper() + why_en[1:]}, so the right unit is the {correct[1][0].lower() + correct[1][1:]}.\n'
            f'Answer: {correct[1]}'
        ),
        'explanation_fr': (
            f'Étape 1 : On mesure {q_fr}.\n'
            f'Étape 2 : {why_fr[0].upper() + why_fr[1:]}, donc la bonne unité est le {correct[0][0].lower() + correct[0][1:]}.\n'
            f'Réponse : {correct[0]}'
        ),
        'correct_answers':  [correct[0]],
    }
