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
from .decimals_plus import (
    g4_decimal_grid_gen, g4_decimal_equivalence_gen, g4_decimal_number_line_gen,
    g6_decimal_number_line_gen, g4_round_decimal_gen, g5_times_power_of_ten_gen,
    g5_estimate_decimal_gen, g5_decimal_story_gen, g6_percent_gen, g6_choose_notation_gen,
    fraction_to_decimal_gen,
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
    # WP3 — decimals & percentages
    'fraction-to-decimal':           fraction_to_decimal_gen,   # rewrite: tenths + hundredths
    'g4-decimal-grid':               g4_decimal_grid_gen,
    'g4-decimal-equivalence':        g4_decimal_equivalence_gen,
    'g4-decimal-number-line':        g4_decimal_number_line_gen,
    'g4-round-decimal':              g4_round_decimal_gen,
    'g5-times-power-of-ten':         g5_times_power_of_ten_gen,
    'g5-estimate-decimal':           g5_estimate_decimal_gen,
    'g5-decimal-story':              g5_decimal_story_gen,
    'g6-decimal-number-line':        g6_decimal_number_line_gen,
    'g6-percent':                    g6_percent_gen,
    'g6-choose-notation':            g6_choose_notation_gen,
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
    'g4-decimal-grid':               _sk('fraction-to-decimal', 'g4-decimal-equivalence', 'g4-decimal-number-line', 'read-decimal'),
    'g4-decimal-equivalence':        _sk('g4-decimal-grid', 'g4-decimal-number-line', 'compare-decimal', 'g4-decimal-grid'),
    'g4-decimal-number-line':        _sk('g4-decimal-grid', 'g4-round-decimal', 'g6-decimal-number-line', 'g4-decimal-grid'),
    'g4-round-decimal':              _sk('g4-decimal-number-line', 'compare-decimal', 'g5-estimate-decimal', 'g4-decimal-number-line'),
    'g5-times-power-of-ten':         _sk('g5-decimal-write', 'g5-estimate-decimal', 'g5-decimal-mult', 'g5-decimal-write'),
    'g5-estimate-decimal':           _sk('g4-round-decimal', 'g5-decimal-story', 'g5-decimal-mult', 'g4-round-decimal'),
    'g5-decimal-story':              _sk('g5-estimate-decimal', 'g5-decimal-mult', 'g5-decimal-div', 'decimal-add'),
    'g6-decimal-number-line':        _sk('g4-decimal-number-line', 'g6-percent', 'compare-decimal', 'g4-decimal-number-line'),
    'g6-percent':                    _sk('g5-decimal-forms', 'g6-choose-notation', 'g5-probability-forms', 'fraction-to-decimal'),
    'g6-choose-notation':            _sk('g6-percent', 'g6-decimal-number-line', 'compare-mixed', 'g6-percent'),
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
    {'name_en': 'Grade 4 — Fractions & Decimals', 'grade': 4, 'topics': [
        {'slug': 'g4-decimal-grid',          'name_en': 'Decimals on a Grid',          'name_fr': 'Décimaux sur un quadrillage'},
        {'slug': 'g4-decimal-equivalence',   'name_en': 'Equal Decimal Writings',      'name_fr': 'Écritures équivalentes d\'un décimal'},
        {'slug': 'g4-decimal-number-line',   'name_en': 'Decimals on a Number Line',   'name_fr': 'Décimaux sur la droite numérique'},
        {'slug': 'g4-round-decimal',         'name_en': 'Round Decimals',              'name_fr': 'Arrondir un nombre décimal'},
    ]},
    {'name_en': 'Grade 5 — Arithmetic', 'grade': 5, 'topics': [
        {'slug': 'g5-times-power-of-ten',    'name_en': '× and ÷ by 10, 100, 1000',    'name_fr': '× et ÷ par 10, 100, 1000'},
        {'slug': 'g5-estimate-decimal',      'name_en': 'Estimate with Decimals',      'name_fr': 'Estimer avec des décimaux'},
        {'slug': 'g5-decimal-story',         'name_en': 'Decimal Word Problems',       'name_fr': 'Problèmes avec des décimaux'},
    ]},
    {'name_en': 'Grade 6 — Decimals & Percentages', 'name_fr': '6e année — Décimaux et pourcentages', 'icon': '%', 'grade': 6, 'topics': [
        {'slug': 'g6-decimal-number-line',   'name_en': 'Decimals Between Decimals',   'name_fr': 'Décimaux entre deux décimaux'},
        {'slug': 'g6-percent',               'name_en': 'Percentages',                 'name_fr': 'Pourcentages'},
        {'slug': 'g6-choose-notation',       'name_en': 'Fraction, Decimal or %?',     'name_fr': 'Fraction, décimal ou % ?'},
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
