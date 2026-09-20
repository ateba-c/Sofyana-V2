"""
Language of a practice session — one language, end to end.

Two mechanisms:

1. ``resolve_lang(request)``: the language is sticky.  ``?lang=`` (or a posted
   ``lang`` field) sets it and stores it in the session; every later request
   without an explicit ``lang`` reuses the session value.  So a child who chose
   French keeps French even through links that forget the parameter.

2. ``localize_problem(q, lang)``: answer choices, matching pairs and ordering
   items are shown in the session language.  Generators may supply explicit
   ``label_en`` / ``label_fr`` (or ``left_en`` / ``right_en``); when they only
   give one label, a curated vocabulary translates the school words it contains
   (place-value names, shapes, units, solids, seasons…).  Numbers, symbols and
   units pass through untouched.
"""
import re

DEFAULT_LANG = 'fr'
SESSION_KEY = 'ui_lang'
LANGS = ('fr', 'en')


def resolve_lang(request):
    """Sticky UI language: explicit param wins and is remembered; else session; else default."""
    raw = request.POST.get('lang') if request.method == 'POST' else None
    if raw is None:
        raw = request.GET.get('lang')
    if raw in LANGS:
        if hasattr(request, 'session') and request.session.get(SESSION_KEY) != raw:
            request.session[SESSION_KEY] = raw
        return raw
    if hasattr(request, 'session'):
        stored = request.session.get(SESSION_KEY)
        if stored in LANGS:
            return stored
    return DEFAULT_LANG


# ── vocabulary (French → English); longest phrases first so they win ─────────
_FR_EN = [
    # place value
    ('centaines de mille', 'hundred thousands'), ('centaine de mille', 'hundred thousand'),
    ('dizaines de mille', 'ten thousands'), ('dizaine de mille', 'ten thousand'),
    ('dizaine de milliers', 'ten thousands'), ('dizaines de milliers', 'ten thousands'),
    ('unités de mille', 'thousands'), ('unité de mille', 'thousand'),
    ('milliers', 'thousands'), ('millier', 'thousand'),
    ('centaines', 'hundreds'), ('centaine', 'hundred'),
    ('dizaines', 'tens'), ('dizaine', 'ten'),
    ('unités', 'ones'), ('unité', 'one'),
    ('dixièmes', 'tenths'), ('dixième', 'tenth'),
    ('centièmes', 'hundredths'), ('centième', 'hundredth'),
    ('millièmes', 'thousandths'), ('millième', 'thousandth'),
    # lines & shapes
    ('ni parallel ni perp', 'neither parallel nor perpendicular'),
    ('parallèles', 'parallel'), ('paralleles', 'parallel'),
    ('perpendiculaires', 'perpendicular'), ('sécantes', 'intersecting'), ('secantes', 'intersecting'),
    ('horizontales', 'horizontal'), ('verticales', 'vertical'), ('courbes', 'curved'),
    ('parallélogramme', 'parallelogram'), ('losange', 'rhombus'), ('trapèze', 'trapezoid'),
    ('carré', 'square'), ('rectangle', 'rectangle'),
    ('quadrilatère', 'quadrilateral'), ('quadrilatere', 'quadrilateral'),
    ('triangle', 'triangle'), ('pentagone', 'pentagon'), ('hexagone', 'hexagon'),
    ('heptagone', 'heptagon'), ('octogone', 'octagon'),
    ('aigu', 'acute'), ('obtus', 'obtuse'), ('droit', 'right'), ('plat', 'straight'),
    # solids
    ('bases circulaires', 'circular bases'), ('base circulaire', 'circular base'),
    ('faces carrées', 'square faces'), ('faces plates', 'flat faces'), ('face plate', 'flat face'),
    ('face courbe', 'curved face'), ('arêtes droites', 'straight edges'), ('arête droite', 'straight edge'),
    ('sommets', 'vertices'), ('sommet', 'vertex'), ('arêtes', 'edges'), ('arête', 'edge'), ('faces', 'faces'), ('face', 'face'),
    ('Prisme à base triangulaire', 'Triangular prism'), ('Pyramide à base carrée', 'Square pyramid'),
    ('Cylindre', 'Cylinder'), ('Sphère', 'Sphere'), ('Cône', 'Cone'), ('Cube', 'Cube'),
    # operations
    ('soustraction', 'subtraction'), ('addition', 'addition'), ('multiplication', 'multiplication'), ('division', 'division'),
    # units (long form)
    ('Millimètre', 'Millimetre'), ('Centimètre', 'Centimetre'), ('Kilomètre', 'Kilometre'), ('Mètre', 'Metre'),
    ('Kilogramme', 'Kilogram'), ('Gramme', 'Gram'), ('Millilitre', 'Millilitre'), ('Litre', 'Litre'),
    # quantities used in ordering / comparing
    ('habitants', 'inhabitants'), ('visiteurs', 'visitors'), ('places', 'seats'), ('vues', 'views'),
    # categories (tables / pie charts)
    ('Printemps', 'Spring'), ('Été', 'Summer'), ('Automne', 'Fall'), ('Hiver', 'Winter'),
    ('Rouge', 'Red'), ('Bleu', 'Blue'), ('Vert', 'Green'), ('Jaune', 'Yellow'),
    ('Chat', 'Cat'), ('Chien', 'Dog'), ('Oiseau', 'Bird'), ('Poisson', 'Fish'),
    ('Pomme', 'Apple'), ('Raisin', 'Grapes'), ('Banane', 'Banana'), ('Orange', 'Orange'),
    ('Football', 'Soccer'), ('Natation', 'Swimming'),
    # probability words
    ('impossible', 'impossible'), ('certain', 'certain'), ('probable', 'likely'), ('peu probable', 'unlikely'),
    ('également probable', 'equally likely'),
    # sentences used as choices
    ('Toutes les informations sont utiles.', 'All the information is useful.'),
    ("Aucune information n'est utile.", 'No information is useful.'),
    # connectors
    ('et', 'and'), ('ou', 'or'),
]
_FR_EN.sort(key=lambda p: -len(p[0]))

_EN_FR = [
    ('Composite', 'Composé'), ('Prime', 'Premier'), ('Neither', 'Ni l’un ni l’autre'),
    ('Even', 'Pair'), ('Odd', 'Impair'), ('Yes', 'Oui'), ('No', 'Non'),
    ('True', 'Vrai'), ('False', 'Faux'),
]
_EN_FR.sort(key=lambda p: -len(p[0]))


def _compile(pairs):
    out = []
    for src, dst in pairs:
        # whole-word match, case-insensitive; accented letters count as word chars
        pat = re.compile(r'(?<![\wÀ-ÿ])' + re.escape(src) + r'(?![\wÀ-ÿ])', re.IGNORECASE)
        out.append((pat, dst))
    return out


_FR_EN_RE = _compile(_FR_EN)
_EN_FR_RE = _compile(_EN_FR)
_TIME_HM = re.compile(r'^(\d{1,2}) h (\d{2})$')
_TIME_H = re.compile(r'^(\d{1,2}) h$')


def _sub_keep_case(pat, dst, text):
    def repl(m):
        src = m.group(0)
        if src[:1].isupper() and not dst[:1].isupper():
            return dst[:1].upper() + dst[1:]
        return dst
    return pat.sub(repl, text)


def translate_label(label, lang):
    """Translate the school vocabulary inside a choice label into ``lang``."""
    text = str(label)
    if lang == 'en':
        if _TIME_HM.match(text):
            return _TIME_HM.sub(r'\1:\2', text)
        if _TIME_H.match(text):
            return _TIME_H.sub(r'\1:00', text)
        for pat, dst in _FR_EN_RE:
            text = _sub_keep_case(pat, dst, text)
        return text
    for pat, dst in _EN_FR_RE:
        text = _sub_keep_case(pat, dst, text)
    return text


def _pick(d, base, lang):
    """d[base_<lang>] if provided, else translate d[base]."""
    explicit = d.get(f'{base}_{lang}')
    if explicit:
        return str(explicit)
    other = d.get(f'{base}_{"fr" if lang == "en" else "en"}')
    src = d.get(base)
    if src is None and other is not None:
        src = other
    return translate_label(src, lang) if src is not None else ''


def localize_problem(q, lang):
    """Rewrite choices / pairs / items of a generated problem into ``lang`` (in place)."""
    for c in q.get('choices') or []:
        c['label'] = _pick(c, 'label', lang)
    for p in q.get('pairs') or []:
        p['left'] = _pick(p, 'left', lang)
        p['right'] = _pick(p, 'right', lang)
    for it in q.get('items') or []:
        it['label'] = _pick(it, 'label', lang)
    if q.get('q_type') == 'mix_match' and q.get('pairs'):
        q['correct_answers'] = [p['right'] for p in q['pairs']]
    elif q.get('q_type') in ('ordering', 'sorting') and q.get('items'):
        q['correct_answers'] = [it['label'] for it in sorted(q['items'], key=lambda x: x['order'])]
    return q
