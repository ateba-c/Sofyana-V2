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


# ── grade 6 additions ────────────────────────────────────────────────────────

# Large quantities for comparing / ordering 5–6 digit numbers.
# (fr_plural_thing, en_plural_thing, unit_suffix, low, high, fr_verb, en_verb)
LARGE_QUANTITIES = [
    ('villes', 'towns', 'habitants', 'inhabitants', 20_000, 900_000, 'compte les habitants de', 'counts the inhabitants of'),
    ('maisons', 'houses', '$', '$', 150_000, 999_000, 'compare les prix de', 'compares the prices of'),
    ('musées', 'museums', 'visiteurs', 'visitors', 12_000, 850_000, 'note le nombre de visiteurs de', 'records the visitors of'),
    ('fleuves', 'rivers', 'km', 'km', 1_000, 7_000, 'mesure la longueur de', 'measures the length of'),
    ('camions', 'trucks', 'kg', 'kg', 5_000, 40_000, 'pèse', 'weighs'),
    ('stades', 'stadiums', 'places', 'seats', 8_000, 110_000, 'compte les places de', 'counts the seats of'),
    ('vidéos', 'videos', 'vues', 'views', 10_000, 999_000, 'compare les vues de', 'compares the views of'),
    ('montagnes', 'mountains', 'm', 'm', 1_000, 8_800, "mesure l'altitude de", 'measures the height of'),
]

# Rate problems: subject does X things per period.  (subject_fr, subject_en,
# verb_fr, verb_en, thing_fr, thing_en, period_key, low, high)
RATES = [
    ('Une reine abeille', 'A queen bee', 'pond', 'lays', 'œufs', 'eggs', 'day', 1_200, 2_500),
    ('Une usine', 'A factory', 'fabrique', 'makes', 'vélos', 'bikes', 'day', 120, 980),
    ('Une boulangerie', 'A bakery', 'cuit', 'bakes', 'pains', 'loaves', 'day', 250, 900),
    ('Un cœur humain', 'A human heart', 'bat', 'beats', 'fois', 'times', 'minute', 60, 95),
    ('Un colibri', 'A hummingbird', 'bat des ailes', 'flaps its wings', 'fois', 'times', 'second', 50, 80),
    ('Un train', 'A train', 'parcourt', 'travels', 'km', 'km', 'hour', 110, 300),
    ('Une imprimerie', 'A print shop', 'imprime', 'prints', 'pages', 'pages', 'minute', 150, 650),
    ('Une ferme', 'A farm', 'récolte', 'harvests', 'pommes', 'apples', 'day', 1_500, 4_800),
    ('Un cinéma', 'A cinema', 'vend', 'sells', 'billets', 'tickets', 'day', 320, 1_900),
    ('Une abeille', 'A bee', 'rapporte', 'brings back', 'mg de nectar', 'mg of nectar', 'trip', 40, 95),
]

# How many small periods in a bigger one, for RATES: period_key → [(n, fr, en, count)]
PERIODS = {
    'day':    [(7, '1 semaine', '1 week', 7), (14, '2 semaines', '2 weeks', 14), (21, '3 semaines', '3 weeks', 21),
               (30, '30 jours', '30 days', 30), (12, '12 jours', '12 days', 12)],
    'minute': [(60, '1 heure', '1 hour', 60), (45, '45 minutes', '45 minutes', 45), (90, '1 h 30 min', '1 h 30 min', 90),
               (25, '25 minutes', '25 minutes', 25)],
    'second': [(60, '1 minute', '1 minute', 60), (30, '30 secondes', '30 seconds', 30), (75, '75 secondes', '75 seconds', 75)],
    'hour':   [(24, '1 jour', '1 day', 24), (12, '12 heures', '12 hours', 12), (36, '36 heures', '36 hours', 36)],
    'trip':   [(40, '40 sorties', '40 trips', 40), (25, '25 sorties', '25 trips', 25), (64, '64 sorties', '64 trips', 64)],
}

# Comparative statements: two named things with a measurable attribute.
# Verb-based so no adjective agreement is needed.  {S} subject, {n} number.
# keys: attr_fr, attr_en, art_fr ('le'/'la'), unit, lo, hi, subjects, fact_fr, fact_en,
#       more_fr, more_en, less_fr, less_en, times_fr, times_en, q_fr, q_en
COMPARATIVES = [
    dict(attr_fr='vitesse', attr_en='speed', unit='m/h', lo=20_000, hi=250_000,
         subjects=[('la voiture de course', 'the race car'), ('le guépard', 'the cheetah'), ('le service de Serena', "Serena's serve"),
                   ('le faucon', 'the falcon'), ('le train', 'the train'), ('la moto', 'the motorcycle')],
         fact_fr='{S} atteint {n} m/h.', fact_en='{S} reaches {n} m/h.',
         more_fr='{S} va {n} m/h plus vite que {T}.', more_en='{S} goes {n} m/h faster than {T}.',
         less_fr='{S} va {n} m/h moins vite que {T}.', less_en='{S} goes {n} m/h slower than {T}.',
         times_fr='{S} va {n} fois plus vite que {T}.', times_en='{S} goes {n} times faster than {T}.',
         q_fr='Quelle vitesse atteint {S} ?', q_en='What speed does {S} reach?'),
    dict(attr_fr='population', attr_en='population', unit='habitants', lo=15_000, hi=800_000,
         subjects=[('Rivière-Bleue', 'Rivière-Bleue'), ('Saint-Marc', 'Saint-Marc'), ('Val-des-Pins', 'Val-des-Pins'),
                   ('Lac-Doré', 'Lac-Doré'), ('Mont-Clair', 'Mont-Clair')],
         fact_fr='{S} compte {n} habitants.', fact_en='{S} has {n} inhabitants.',
         more_fr='{S} compte {n} habitants de plus que {T}.', more_en='{S} has {n} more inhabitants than {T}.',
         less_fr='{S} compte {n} habitants de moins que {T}.', less_en='{S} has {n} fewer inhabitants than {T}.',
         times_fr="{S} compte {n} fois plus d'habitants que {T}.", times_en='{S} has {n} times as many inhabitants as {T}.',
         q_fr="Combien d'habitants compte {S} ?", q_en='How many inhabitants does {S} have?'),
    dict(attr_fr='prix', attr_en='price', unit='$', lo=8_000, hi=95_000,
         subjects=[('la voiture rouge', 'the red car'), ('le bateau', 'the boat'), ('le camion', 'the truck'),
                   ('la roulotte', 'the trailer'), ('le tracteur', 'the tractor')],
         fact_fr='{S} coûte {n} $.', fact_en='{S} costs ${n}.',
         more_fr='{S} coûte {n} $ de plus que {T}.', more_en='{S} costs ${n} more than {T}.',
         less_fr='{S} coûte {n} $ de moins que {T}.', less_en='{S} costs ${n} less than {T}.',
         times_fr='{S} coûte {n} fois plus que {T}.', times_en='{S} costs {n} times as much as {T}.',
         q_fr='Combien coûte {S} ?', q_en='How much does {S} cost?'),
    dict(attr_fr='masse', attr_en='mass', unit='kg', lo=900, hi=90_000,
         subjects=[("l'éléphant", 'the elephant'), ('la baleine', 'the whale'), ("l'hippopotame", 'the hippo'),
                   ('le camion', 'the truck'), ('le rhinocéros', 'the rhinoceros')],
         fact_fr='{S} pèse {n} kg.', fact_en='{S} weighs {n} kg.',
         more_fr='{S} pèse {n} kg de plus que {T}.', more_en='{S} weighs {n} kg more than {T}.',
         less_fr='{S} pèse {n} kg de moins que {T}.', less_en='{S} weighs {n} kg less than {T}.',
         times_fr='{S} pèse {n} fois plus que {T}.', times_en='{S} weighs {n} times as much as {T}.',
         q_fr='Combien pèse {S} ?', q_en='How much does {S} weigh?'),
    dict(attr_fr='distance', attr_en='distance', unit='km', lo=1_200, hi=40_000,
         subjects=[('le cargo', 'the cargo ship'), ("l'avion", 'the plane'), ('le camionneur', 'the trucker'),
                   ('la cycliste', 'the cyclist'), ('le voilier', 'the sailboat')],
         fact_fr='{S} a parcouru {n} km.', fact_en='{S} covered {n} km.',
         more_fr='{S} a parcouru {n} km de plus que {T}.', more_en='{S} covered {n} km more than {T}.',
         less_fr='{S} a parcouru {n} km de moins que {T}.', less_en='{S} covered {n} km less than {T}.',
         times_fr='{S} a parcouru {n} fois plus de kilomètres que {T}.', times_en='{S} covered {n} times as many km as {T}.',
         q_fr='Quelle distance a parcourue {S} ?', q_en='What distance did {S} cover?'),
]

# Unrelated facts to sprinkle into word problems as "informations inutiles".
DISTRACTOR_FACTS = [
    ('Le guépard court à {n} m/h.', 'The cheetah runs at {n} m/h.', 90_000, 120_000),
    ("L'école compte {n} élèves.", 'The school has {n} students.', 300, 900),
    ('Le stade a {n} places.', 'The stadium has {n} seats.', 8_000, 60_000),
    ('La bibliothèque possède {n} livres.', 'The library owns {n} books.', 5_000, 80_000),
    ('Le film dure {n} minutes.', 'The movie lasts {n} minutes.', 85, 160),
    ('La piscine contient {n} litres.', 'The pool holds {n} litres.', 20_000, 90_000),
]
