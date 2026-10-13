"""
registry_plus.py — wiring of the curriculum-upgrade skills (docs/curriculum/WORKPLAN.md).

Merged into GENERATORS / SKILL_MAP / TOPIC_GROUPS at the end of generators/__init__.py:
  * PLUS_GENERATORS / PLUS_SKILL_MAP entries are added (or replace a legacy generator);
  * each PLUS_GROUPS entry either extends the existing group with the same ``name_en``
    or is inserted right after the last group of its grade.
"""
from .fractions_plus import (
    fraction_shape_gen, g3_fraction_words_gen, g3_numerator_denominator_gen,
    g4_fraction_benchmark_gen, g4_equivalent_fractions_gen, g5_fraction_meanings_gen,
    g5_order_same_numerator_gen, g6_order_related_den_gen, g6_simplify_fraction_gen,
    g6_fraction_add_related_gen, g6_whole_times_fraction_gen,
)

_L3 = ['easy', 'medium', 'hard']


def _sk(prereq, nxt, mastery, down, levels=None):
    return {'prereq': prereq, 'next': nxt, 'mastery_next': mastery, 'downgrade': down, 'level_sequence': levels or _L3}


PLUS_GENERATORS = {
    # WP2 — fractions
    'fraction-shape':                fraction_shape_gen,        # rewrite of the legacy generator
    'g3-fraction-words':             g3_fraction_words_gen,
    'g3-numerator-denominator':      g3_numerator_denominator_gen,
    'g4-fraction-benchmark':         g4_fraction_benchmark_gen,
    'g4-equivalent-fractions':       g4_equivalent_fractions_gen,
    'g5-fraction-meanings':          g5_fraction_meanings_gen,
    'g5-order-same-numerator':       g5_order_same_numerator_gen,
    'g6-order-related-denominators': g6_order_related_den_gen,
    'g6-simplify-fraction':          g6_simplify_fraction_gen,
    'g6-fraction-add-related':       g6_fraction_add_related_gen,
    'g6-whole-times-fraction':       g6_whole_times_fraction_gen,
}

PLUS_SKILL_MAP = {
    'g3-fraction-words':             _sk('fraction-shape', 'g3-numerator-denominator', 'g4-fraction-benchmark', 'fraction-shape'),
    'g3-numerator-denominator':      _sk('fraction-shape', 'fraction-collection', 'g4-equivalent-fractions', 'fraction-shape'),
    'g4-fraction-benchmark':         _sk('g3-numerator-denominator', 'g4-equivalent-fractions', 'compare-fraction', 'fraction-shape'),
    'g4-equivalent-fractions':       _sk('g4-fraction-benchmark', 'compare-fraction', 'g6-simplify-fraction', 'fraction-shape'),
    'g5-fraction-meanings':          _sk('g4-equivalent-fractions', 'g5-order-same-numerator', 'g6-whole-times-fraction', 'fraction-collection'),
    'g5-order-same-numerator':       _sk('g4-fraction-benchmark', 'g6-order-related-denominators', 'g6-fraction-order', 'g4-fraction-benchmark'),
    'g6-order-related-denominators': _sk('g5-order-same-numerator', 'g6-simplify-fraction', 'g6-fraction-add-related', 'g4-equivalent-fractions'),
    'g6-simplify-fraction':          _sk('g4-equivalent-fractions', 'g6-fraction-add-related', 'g6-whole-times-fraction', 'g4-equivalent-fractions'),
    'g6-fraction-add-related':       _sk('g6-simplify-fraction', 'g6-whole-times-fraction', 'fraction-add', 'g4-equivalent-fractions'),
    'g6-whole-times-fraction':       _sk('g6-fraction-add-related', 'g6-fraction-on-line', 'fraction-multiply', 'fraction-collection'),
}

PLUS_GROUPS = [
    {'name_en': 'Grade 3 — Fractions & Decimals', 'grade': 3, 'topics': [
        {'slug': 'g3-fraction-words',        'name_en': 'Read & Write Fractions',      'name_fr': 'Lire et écrire une fraction'},
        {'slug': 'g3-numerator-denominator', 'name_en': 'Numerator & Denominator',     'name_fr': 'Numérateur et dénominateur'},
    ]},
    {'name_en': 'Grade 4 — Fractions & Decimals', 'name_fr': '4e année — Fractions & Décimaux', 'icon': '½', 'grade': 4, 'topics': [
        {'slug': 'g4-fraction-benchmark',    'name_en': 'Compare to 0, ½ and 1',       'name_fr': 'Comparer à 0, à ½ et à 1'},
        {'slug': 'g4-equivalent-fractions',  'name_en': 'Equivalent Fractions',        'name_fr': 'Fractions équivalentes'},
    ]},
    {'name_en': 'Grade 5 — Fractions', 'name_fr': '5e année — Fractions', 'icon': '½', 'grade': 5, 'topics': [
        {'slug': 'g5-fraction-meanings',     'name_en': 'What a Fraction Means',       'name_fr': 'Les sens de la fraction'},
        {'slug': 'g5-order-same-numerator',  'name_en': 'Order: Same Numerator',       'name_fr': 'Ordonner : même numérateur'},
    ]},
    {'name_en': 'Grade 6 — Fractions', 'grade': 6, 'topics': [
        {'slug': 'g6-order-related-denominators', 'name_en': 'Order: Related Denominators', 'name_fr': 'Ordonner : dénominateurs multiples'},
        {'slug': 'g6-simplify-fraction',     'name_en': 'Simplest Form',               'name_fr': 'Fraction irréductible'},
        {'slug': 'g6-fraction-add-related',  'name_en': 'Add & Subtract Fractions',    'name_fr': 'Additionner et soustraire des fractions'},
        {'slug': 'g6-whole-times-fraction',  'name_en': 'Whole Number × Fraction',     'name_fr': 'Nombre entier × fraction'},
    ]},
]


def merge(generators, skill_map, topic_groups):
    generators.update(PLUS_GENERATORS)
    skill_map.update(PLUS_SKILL_MAP)
    for group in PLUS_GROUPS:
        existing = next((g for g in topic_groups if g['name_en'] == group['name_en']), None)
        if existing:
            have = {t['slug'] for t in existing['topics']}
            existing['topics'].extend(t for t in group['topics'] if t['slug'] not in have)
            continue
        new = dict(group, topics=list(group['topics']))
        same_grade = [i for i, g in enumerate(topic_groups) if g.get('grade') == group['grade']]
        later = [i for i, g in enumerate(topic_groups) if (g.get('grade') or 0) > group['grade']]
        pos = same_grade[-1] + 1 if same_grade else (later[0] if later else len(topic_groups))
        topic_groups.insert(pos, new)
