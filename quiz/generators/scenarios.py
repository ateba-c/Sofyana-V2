"""
scenarios.py — bilingual scenario bank for dynamically generated word problems.

The idea: an exercise keeps the same mathematical structure but the *story*
changes every time — a farmer counting sheep becomes a librarian shelving
books, a piano lesson becomes a soccer practice, a jar of screws becomes a bag
of marbles.  Quantities, names, verbs and objects are all drawn at random so
the child never sees the exact same sentence twice.

Everything here is a plain data table plus a few tiny formatting helpers.
Generators call ``pick_actor()``, ``pick_thing()``, ``qty()``, … and format
their own sentences in both languages.
"""
import random

# ── people ───────────────────────────────────────────────────────────────────
# (name, gender) — names that read naturally in both French and English.
ACTORS = [
    ('Léa', 'f'), ('Noah', 'm'), ('Maya', 'f'), ('Samir', 'm'), ('Zoé', 'f'),
    ('Théo', 'm'), ('Inès', 'f'), ('Malik', 'm'), ('Sofia', 'f'), ('Liam', 'm'),
    ('Emma', 'f'), ('Yara', 'f'), ('Kenji', 'm'), ('Amara', 'f'), ('Hugo', 'm'),
    ('Nadia', 'f'), ('Omar', 'm'), ('Chloé', 'f'), ('Rafael', 'm'), ('Aïcha', 'f'),
]

# Role-based actors (with article) used when a job fits better than a name.
ROLES = [
    # fr (with article), en (with article), gender
    ('le fermier', 'the farmer', 'm'), ('la fermière', 'the farmer', 'f'),
    ('le libraire', 'the bookseller', 'm'), ('la bibliothécaire', 'the librarian', 'f'),
    ('le boulanger', 'the baker', 'm'), ('la fleuriste', 'the florist', 'f'),
    ('le menuisier', 'the carpenter', 'm'), ('la vétérinaire', 'the vet', 'f'),
    ('le berger', 'the shepherd', 'm'),
    ('la jardinière', 'the gardener', 'f'), ('le marchand', 'the merchant', 'm'),
]

# ── things that can be counted ───────────────────────────────────────────────
# key: (fr_singular, fr_plural, fr_gender, en_singular, en_plural, category)
THINGS = {
    # animals
    'chien':   ('chien', 'chiens', 'm', 'dog', 'dogs', 'animal'),
    'mouton':  ('mouton', 'moutons', 'm', 'sheep', 'sheep', 'animal'),
    'vache':   ('vache', 'vaches', 'f', 'cow', 'cows', 'animal'),
    'poule':   ('poule', 'poules', 'f', 'hen', 'hens', 'animal'),
    'chat':    ('chat', 'chats', 'm', 'cat', 'cats', 'animal'),
    'lapin':   ('lapin', 'lapins', 'm', 'rabbit', 'rabbits', 'animal'),
    'cheval':  ('cheval', 'chevaux', 'm', 'horse', 'horses', 'animal'),
    'canard':  ('canard', 'canards', 'm', 'duck', 'ducks', 'animal'),
    'chèvre':  ('chèvre', 'chèvres', 'f', 'goat', 'goats', 'animal'),
    'abeille': ('abeille', 'abeilles', 'f', 'bee', 'bees', 'animal'),
    # small objects
    'bille':   ('bille', 'billes', 'f', 'marble', 'marbles', 'object'),
    'vis':     ('vis', 'vis', 'f', 'screw', 'screws', 'object'),
    'clou':    ('clou', 'clous', 'm', 'nail', 'nails', 'object'),
    'timbre':  ('timbre', 'timbres', 'm', 'stamp', 'stamps', 'object'),
    'crayon':  ('crayon', 'crayons', 'm', 'pencil', 'pencils', 'object'),
    'bouton':  ('bouton', 'boutons', 'm', 'button', 'buttons', 'object'),
    'perle':   ('perle', 'perles', 'f', 'bead', 'beads', 'object'),
    'carte':   ('carte', 'cartes', 'f', 'card', 'cards', 'object'),
    'bonbon':  ('bonbon', 'bonbons', 'm', 'candy', 'candies', 'object'),
    'livre':   ('livre', 'livres', 'm', 'book', 'books', 'object'),
    'pomme':   ('pomme', 'pommes', 'f', 'apple', 'apples', 'food'),
    'œuf':     ('œuf', 'œufs', 'm', 'egg', 'eggs', 'food'),
    'biscuit': ('biscuit', 'biscuits', 'm', 'cookie', 'cookies', 'food'),
    'fleur':   ('fleur', 'fleurs', 'f', 'flower', 'flowers', 'object'),
    'graine':  ('graine', 'graines', 'f', 'seed', 'seeds', 'object'),
}

# Containers that make sense for each category:  (fr_sing, fr_plur, en_sing, en_plur)
CONTAINERS = {
    'animal': [
        ('enclos', 'enclos', 'pen', 'pens'),
        ('troupeau', 'troupeaux', 'herd', 'herds'),
        ('groupe', 'groupes', 'group', 'groups'),
        ('camion', 'camions', 'truck', 'trucks'),
    ],
    'object': [
        ('pot', 'pots', 'jar', 'jars'),
        ('boîte', 'boîtes', 'box', 'boxes'),
        ('sac', 'sacs', 'bag', 'bags'),
        ('paquet', 'paquets', 'pack', 'packs'),
        ('caisse', 'caisses', 'crate', 'crates'),
    ],
    'food': [
        ('panier', 'paniers', 'basket', 'baskets'),
        ('caisse', 'caisses', 'crate', 'crates'),
        ('boîte', 'boîtes', 'box', 'boxes'),
        ('sac', 'sacs', 'bag', 'bags'),
    ],
}

# Verbs (3rd person singular present) — (fr, en, allowed categories)
VERBS = [
    ('compte', 'counts', ('animal', 'object', 'food')),
    ('range', 'puts away', ('object', 'food')),
    ('achète', 'buys', ('object', 'food', 'animal')),
    ('ramasse', 'gathers', ('object', 'food')),
    ('transporte', 'carries', ('object', 'food', 'animal')),
    ('vend', 'sells', ('object', 'food', 'animal')),
    ('nourrit', 'feeds', ('animal',)),
    ('rassemble', 'rounds up', ('animal',)),
    ('possède', 'owns', ('animal', 'object', 'food')),
    ('reçoit', 'receives', ('object', 'food')),
    ('emballe', 'packs', ('object', 'food')),
]

# Activities for time problems — (fr, en, gender_fr)
ACTIVITIES = [
    ('le cours de piano', 'the piano lesson', 'm'),
    ("l'entraînement de soccer", 'the soccer practice', 'm'),
    ('le film', 'the movie', 'm'),
    ('le trajet en autobus', 'the bus ride', 'm'),
    ('la partie de hockey', 'the hockey game', 'f'),
    ("l'atelier de dessin", 'the drawing workshop', 'm'),
    ('la sortie au musée', 'the museum trip', 'f'),
    ('la récréation', 'recess', 'f'),
    ('le cours de natation', 'the swimming lesson', 'm'),
    ('la répétition de théâtre', 'the theatre rehearsal', 'f'),
    ('la promenade du chien', 'the dog walk', 'f'),
    ('le cours de karaté', 'the karate class', 'm'),
    ('la fête d’anniversaire', 'the birthday party', 'f'),
    ('le match de basketball', 'the basketball game', 'm'),
    ('la lecture du soir', 'the evening reading', 'f'),
]

# Measured objects for ordering / comparing lengths, masses, capacities.
# (fr_plural, en_plural, unit, low, high)
MEASURED = [
    ('rubans', 'ribbons', 'mm', 500, 9999),
    ('cordes', 'ropes', 'cm', 100, 9999),
    ('routes', 'roads', 'km', 10, 999),
    ('sacs de farine', 'bags of flour', 'g', 500, 9999),
    ('bouteilles', 'bottles', 'mL', 100, 2000),
    ('tours', 'towers', 'm', 20, 999),
    ('sentiers', 'trails', 'm', 100, 9999),
    ('valises', 'suitcases', 'kg', 5, 40),
    ('rivières', 'rivers', 'km', 50, 9999),
    ('planches', 'planks', 'cm', 30, 400),
]


# ── helpers ──────────────────────────────────────────────────────────────────

def fmt_n(n):
    """French-style digit grouping with a narrow no-break space: 49526 → '49 526'."""
    s = str(abs(int(n)))
    groups = []
    while s:
        groups.append(s[-3:])
        s = s[:-3]
    out = ' '.join(reversed(groups))
    return ('-' + out) if n < 0 else out


def pick_actor():
    """('Léa', 'f') — a child's first name and its gender."""
    return random.choice(ACTORS)


def pick_role():
    """('le fermier', 'the farmer', 'm')"""
    return random.choice(ROLES)


def pick_thing(category=None):
    """Return (key, info) for a random countable thing, optionally by category."""
    keys = [k for k, v in THINGS.items() if category is None or v[5] == category]
    k = random.choice(keys)
    return k, THINGS[k]


def pick_container(category):
    return random.choice(CONTAINERS.get(category, CONTAINERS['object']))


def pick_verb(category):
    return random.choice([v for v in VERBS if category in v[2]])


def pick_activity():
    return random.choice(ACTIVITIES)


def pick_measured():
    return random.choice(MEASURED)


def noun(info, n, lang):
    """The noun alone, pluralised for quantity n: noun(THINGS['chien'], 3, 'fr') → 'chiens'."""
    if lang == 'fr':
        return info[1] if n != 1 else info[0]
    return info[4] if n != 1 else info[3]


def qty(n, info, lang):
    """'3 chiens' / '3 dogs' / '1 chien' / '1 dog' with grouped digits."""
    return f"{fmt_n(n)} {noun(info, n, lang)}"


def cont(cinfo, n, lang):
    """Container noun pluralised: cont(('pot','pots','jar','jars'), 3, 'en') → 'jars'."""
    if lang == 'fr':
        return cinfo[1] if n != 1 else cinfo[0]
    return cinfo[3] if n != 1 else cinfo[2]


def pronoun_fr(gender):
    return 'elle' if gender == 'f' else 'il'


def pronoun_en(gender):
    return 'she' if gender == 'f' else 'he'


def possessive_fr(gender_of_noun, plural=False):
    """'son' / 'sa' / 'ses'."""
    if plural:
        return 'ses'
    return 'sa' if gender_of_noun == 'f' else 'son'


def possessive_en(gender_of_owner):
    return 'her' if gender_of_owner == 'f' else 'his'


def de(name):
    """French 'de' + name with elision: de('Inès') → "d'Inès", de('Léa') → 'de Léa'."""
    return ("d'" if name[:1].lower() in 'aeiouhéèêàâîôû' else 'de ') + name
