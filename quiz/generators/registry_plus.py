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
from .operations_plus import (
    g3_equality_true_gen, g4_equivalent_expr_gen, g4_properties_gen, g6_distributive_gen,
    g4_missing_factor_gen, g4_division_remainder_gen, g4_arrays_gen, g3_story_meaning_gen,
    g5_expression_for_story_gen, g3_estimate_sum_gen, g5_estimate_quotient_gen,
    g6_divisibility_gen, g6_prime_factors_gen, g6_powers_gen, g5_number_patterns_gen,
    g4_times_tables_gen, g6_write_large_number_gen,
)
from .geometry_plus import (
    g3_solid_picture_gen, g3_prism_or_pyramid_gen, g3_net_match_gen, g4_net_pyramid_gen,
    g6_polyhedron_net_gen, g3_convex_gen, g6_triangle_type_gen, g6_circle_parts_gen,
    g3_symmetry_axis_gen, g6_translation_gen, g3_frieze_gen, g3_congruent_gen,
    g3_grid_map_gen, cartesian_place_point_gen,
)
from .measurement_plus import (
    g3_ruler_mm_gen, g5_estimate_length_gen, g3_area_count_squares_gen, g5_area_units_gen,
    g3_volume_count_cubes_gen, g6_volume_units_gen, g4_compare_angles_gen, g6_protractor_gen,
    g3_balance_scale_gen, g3_capacity_estimate_gen, g3_thermometer_gen,
)
from .stats_plus import (
    g3_pictograph_gen, g4_line_graph_gen, g3_tally_table_gen, g3_build_chart_gen, g4_survey_question_gen,
)
from .probability_plus import (
    g3_equally_likely_gen, g4_compare_likelihood_gen, g4_independence_gen, g4_variability_gen,
    g5_probability_line_gen, g5_tree_diagram_gen, g5_simulation_gen, g3_list_outcomes_gen,
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
    # WP4 — operations & calculation
    'g3-equality-true':              g3_equality_true_gen,
    'g3-story-meaning':              g3_story_meaning_gen,
    'g3-estimate-sum':               g3_estimate_sum_gen,
    'g4-equivalent-expressions':     g4_equivalent_expr_gen,
    'g4-properties':                 g4_properties_gen,
    'g4-missing-factor':             g4_missing_factor_gen,
    'g4-division-remainder':         g4_division_remainder_gen,
    'g4-arrays':                     g4_arrays_gen,
    'g4-times-tables':               g4_times_tables_gen,
    'g5-expression-for-story':       g5_expression_for_story_gen,
    'g5-estimate-quotient':          g5_estimate_quotient_gen,
    'g5-number-patterns':            g5_number_patterns_gen,
    'g6-distributive':               g6_distributive_gen,
    'g6-divisibility':               g6_divisibility_gen,
    'g6-prime-factors':              g6_prime_factors_gen,
    'g6-powers':                     g6_powers_gen,
    'g6-write-large-number':         g6_write_large_number_gen,
    # WP5 — geometry
    'g3-solid-picture':              g3_solid_picture_gen,
    'g3-prism-or-pyramid':           g3_prism_or_pyramid_gen,
    'g3-net-match':                  g3_net_match_gen,
    'g4-net-pyramid':                g4_net_pyramid_gen,
    'g6-polyhedron-net':             g6_polyhedron_net_gen,
    'g3-convex':                     g3_convex_gen,
    'g6-triangle-type':              g6_triangle_type_gen,
    'g6-circle-parts':               g6_circle_parts_gen,
    'g3-symmetry-axis':              g3_symmetry_axis_gen,
    'g6-translation':                g6_translation_gen,
    'g3-frieze':                     g3_frieze_gen,
    'g3-congruent':                  g3_congruent_gen,
    'g3-grid-map':                   g3_grid_map_gen,
    'cartesian-place-point':         cartesian_place_point_gen,
    # WP6 — measurement
    'g3-ruler-mm':                   g3_ruler_mm_gen,
    'g5-estimate-length':            g5_estimate_length_gen,
    'g3-area-count-squares':         g3_area_count_squares_gen,
    'g5-area-units':                 g5_area_units_gen,
    'g3-volume-count-cubes':         g3_volume_count_cubes_gen,
    'g6-volume-units':               g6_volume_units_gen,
    'g4-compare-angles':             g4_compare_angles_gen,
    'g6-protractor':                 g6_protractor_gen,
    'g3-balance-scale':              g3_balance_scale_gen,
    'g3-capacity-estimate':          g3_capacity_estimate_gen,
    'g3-thermometer':                g3_thermometer_gen,
    # WP7 — statistics
    'g3-pictograph':                 g3_pictograph_gen,
    'g4-line-graph':                 g4_line_graph_gen,
    'g3-tally-table':                g3_tally_table_gen,
    'g3-build-chart':                g3_build_chart_gen,
    'g4-survey-question':            g4_survey_question_gen,
    # WP8 — probability
    'g3-equally-likely':             g3_equally_likely_gen,
    'g4-compare-likelihood':         g4_compare_likelihood_gen,
    'g4-independence':               g4_independence_gen,
    'g4-variability':                g4_variability_gen,
    'g5-probability-line':           g5_probability_line_gen,
    'g5-tree-diagram':               g5_tree_diagram_gen,
    'g5-simulation':                 g5_simulation_gen,
    'g3-list-outcomes':              g3_list_outcomes_gen,
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
    'g3-equality-true':              _sk('missing-addend', 'g3-story-meaning', 'g4-equivalent-expressions', 'add'),
    'g3-story-meaning':              _sk('word-problem', 'g3-estimate-sum', 'choose-operation', 'missing-addend'),
    'g3-estimate-sum':               _sk('round-ten', 'word-problem', 'g5-estimate-quotient', 'round-ten'),
    'g4-equivalent-expressions':     _sk('g3-equality-true', 'g4-properties', 'g6-distributive', 'g3-equality-true'),
    'g4-properties':                 _sk('g4-equivalent-expressions', 'g4-missing-factor', 'g6-distributive', 'fact-family'),
    'g4-missing-factor':             _sk('g4-times-tables', 'g4-division-remainder', 'g5-estimate-quotient', 'fact-family'),
    'g4-division-remainder':         _sk('g4-missing-factor', 'g4-arrays', 'divide', 'division-sharing'),
    'g4-arrays':                     _sk('repeated-addition', 'g4-times-tables', 'g6-distributive', 'repeated-addition'),
    'g4-times-tables':               _sk('g4-arrays', 'g4-missing-factor', 'multiply', 'repeated-addition'),
    'g5-expression-for-story':       _sk('g5-order-ops', 'g5-estimate-quotient', 'g5-decimal-story', 'choose-operation'),
    'g5-estimate-quotient':          _sk('g3-estimate-sum', 'g5-expression-for-story', 'g6-estimate-product', 'g4-division-remainder'),
    'g5-number-patterns':            _sk('number-sequence', 'g6-powers', 'squares', 'number-sequence'),
    'g6-distributive':               _sk('g4-properties', 'g6-divisibility', 'g6-partial-products', 'g4-arrays'),
    'g6-divisibility':               _sk('g4-times-tables', 'g6-prime-factors', 'primes', 'even-odd'),
    'g6-prime-factors':              _sk('g6-divisibility', 'g6-powers', 'g6-simplify-fraction', 'primes'),
    'g6-powers':                     _sk('squares', 'g6-prime-factors', 'g5-number-patterns', 'squares'),
    'g3-solid-picture':              _sk('identify-solid', 'g3-prism-or-pyramid', 'g3-net-match', 'identify-solid'),
    'g3-prism-or-pyramid':           _sk('g3-solid-picture', 'g3-net-match', 'g5-solid-counts', 'g3-solid-picture'),
    'g3-net-match':                  _sk('g3-prism-or-pyramid', 'g4-net-pyramid', 'g6-polyhedron-net', 'g3-solid-picture'),
    'g4-net-pyramid':                _sk('g3-net-match', 'g5-solid-counts', 'g6-polyhedron-net', 'g3-prism-or-pyramid'),
    'g6-polyhedron-net':             _sk('g4-net-pyramid', 'g5-euler', 'g5-euler', 'g3-net-match'),
    'g3-convex':                     _sk('name-polygon', 'g4-quadrilateral-name', 'g6-triangle-type', 'name-polygon'),
    'g6-triangle-type':              _sk('identify-angle', 'g6-circle-parts', 'g4-quadrilateral-riddle', 'identify-angle'),
    'g6-circle-parts':               _sk('g6-triangle-type', 'g6-translation', 'geometry-perimeter', 'name-polygon'),
    'g3-symmetry-axis':              _sk('g3-congruent', 'g3-frieze', 'g6-translation', 'g3-congruent'),
    'g6-translation':                _sk('g3-symmetry-axis', 'g3-frieze', 'cartesian-coord', 'g3-symmetry-axis'),
    'g3-frieze':                     _sk('g3-symmetry-axis', 'g6-translation', 'g6-translation', 'g3-congruent'),
    'g3-congruent':                  _sk('name-polygon', 'g3-symmetry-axis', 'g3-frieze', 'name-polygon'),
    'g3-grid-map':                   _sk('cartesian-coord', 'cartesian-place-point', 'cartesian-coord', 'cartesian-coord'),
    'cartesian-place-point':         _sk('g3-grid-map', 'cartesian-coord', 'g6-translation', 'g3-grid-map'),
    'g3-ruler-mm':                   _sk('measure-unit', 'g5-estimate-length', 'convert-length', 'measure-unit'),
    'g5-estimate-length':            _sk('g3-ruler-mm', 'convert-length', 'perimeter-labeled', 'measure-unit'),
    'g3-area-count-squares':         _sk('perimeter-labeled', 'g5-area-units', 'geometry-area', 'perimeter-labeled'),
    'g5-area-units':                 _sk('g3-area-count-squares', 'geometry-area', 'g6-volume-units', 'g3-area-count-squares'),
    'g3-volume-count-cubes':         _sk('g3-area-count-squares', 'g5-volume', 'g6-volume-units', 'g3-area-count-squares'),
    'g6-volume-units':               _sk('g5-volume', 'g5-capacity-convert', 'convert-volume', 'g3-volume-count-cubes'),
    'g4-compare-angles':             _sk('identify-angle', 'g6-protractor', 'g6-triangle-type', 'identify-angle'),
    'g6-protractor':                 _sk('g4-compare-angles', 'g6-triangle-type', 'g6-circle-parts', 'g4-compare-angles'),
    'g3-balance-scale':              _sk('unit-by-quantity', 'g5-mass-convert', 'convert-mass', 'unit-by-quantity'),
    'g3-capacity-estimate':          _sk('unit-by-quantity', 'g5-capacity-convert', 'g6-volume-units', 'unit-by-quantity'),
    'g3-thermometer':                _sk('g4-number-line-point', 'g5-thermometer', 'g5-temperature', 'g4-number-line-point'),
    'g3-pictograph':                 _sk('read-bar-chart', 'g3-tally-table', 'g4-line-graph', 'read-bar-chart'),
    'g3-tally-table':                _sk('g3-pictograph', 'g3-build-chart', 'g5-data-table', 'g3-pictograph'),
    'g3-build-chart':                _sk('g3-tally-table', 'g4-line-graph', 'g5-pie-chart', 'read-bar-chart'),
    'g4-line-graph':                 _sk('g3-build-chart', 'g4-survey-question', 'g5-data-table', 'read-bar-chart'),
    'g4-survey-question':            _sk('g3-tally-table', 'g4-line-graph', 'g5-arithmetic-mean', 'g3-tally-table'),
    'g3-list-outcomes':              _sk('probability-vocab', 'g3-equally-likely', 'g5-count-outcomes', 'probability-vocab'),
    'g3-equally-likely':             _sk('g3-list-outcomes', 'g4-compare-likelihood', 'g5-probability-frac', 'probability-vocab'),
    'g4-compare-likelihood':         _sk('g3-equally-likely', 'g4-independence', 'g5-probability-line', 'g3-equally-likely'),
    'g4-independence':               _sk('g4-compare-likelihood', 'g4-variability', 'g5-simulation', 'g3-equally-likely'),
    'g4-variability':                _sk('g4-independence', 'g5-simulation', 'g5-simulation', 'probability-vocab'),
    'g5-probability-line':           _sk('g4-compare-likelihood', 'g5-probability-frac', 'g5-probability-forms', 'probability-vocab'),
    'g5-tree-diagram':               _sk('g3-list-outcomes', 'g5-count-outcomes', 'g5-probability-frac', 'g3-list-outcomes'),
    'g5-simulation':                 _sk('g4-variability', 'g5-probability-frac', 'g5-probability-forms', 'g4-compare-likelihood'),
    'g6-write-large-number':         _sk('g5-large-integer', 'g6-digit-value', 'g6-compare', 'write-number'),
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
    {'name_en': 'Grade 3 — Arithmetic', 'grade': 3, 'topics': [
        {'slug': 'g3-equality-true',         'name_en': 'True Equalities',             'name_fr': 'Égalités vraies'},
        {'slug': 'g3-story-meaning',         'name_en': 'Story Problems: + and −',     'name_fr': 'Problèmes : sens de + et −'},
        {'slug': 'g3-estimate-sum',          'name_en': 'Estimate a Sum',              'name_fr': 'Estimer une somme'},
    ]},
    {'name_en': 'Grade 4 — Operations', 'name_fr': '4e année — Opérations', 'icon': '✖️', 'grade': 4, 'topics': [
        {'slug': 'g4-times-tables',          'name_en': 'Times Tables',                'name_fr': 'Tables de multiplication'},
        {'slug': 'g4-arrays',                'name_en': 'Arrays & Strategies',         'name_fr': 'Tableaux de points et stratégies'},
        {'slug': 'g4-missing-factor',        'name_en': 'Missing Factor',              'name_fr': 'Facteur manquant'},
        {'slug': 'g4-division-remainder',    'name_en': 'Division with Remainder',     'name_fr': 'Division avec reste'},
        {'slug': 'g4-equivalent-expressions','name_en': 'Equivalent Expressions',      'name_fr': 'Expressions équivalentes'},
        {'slug': 'g4-properties',            'name_en': 'Properties of Operations',    'name_fr': 'Propriétés des opérations'},
    ]},
    {'name_en': 'Grade 5 — Arithmetic', 'grade': 5, 'topics': [
        {'slug': 'g5-expression-for-story',  'name_en': 'Expression for a Story',      'name_fr': 'Chaîne d’opérations d’un problème'},
        {'slug': 'g5-estimate-quotient',     'name_en': 'Estimate a Quotient',         'name_fr': 'Estimer un quotient'},
        {'slug': 'g5-number-patterns',       'name_en': 'Number Patterns',             'name_fr': 'Suites de nombres'},
    ]},
    {'name_en': 'Grade 6 — Number Theory', 'name_fr': '6e année — Propriétés des nombres', 'icon': '🔍', 'grade': 6, 'topics': [
        {'slug': 'g6-divisibility',          'name_en': 'Divisibility Rules',          'name_fr': 'Critères de divisibilité'},
        {'slug': 'g6-prime-factors',         'name_en': 'Prime Factorisation',         'name_fr': 'Facteurs premiers'},
        {'slug': 'g6-powers',                'name_en': 'Powers & Exponents',          'name_fr': 'Puissances et exposants'},
        {'slug': 'g6-distributive',          'name_en': 'Distributive Property',       'name_fr': 'Distributivité'},
    ]},
    {'name_en': 'Grade 6 — Number Sense', 'grade': 6, 'topics': [
        {'slug': 'g6-write-large-number',    'name_en': 'Write Large Numbers',         'name_fr': 'Écrire de grands nombres'},
    ]},
    {'name_en': 'Grade 3 — Geometry', 'grade': 3, 'topics': [
        {'slug': 'g3-solid-picture',         'name_en': 'Name the Solid',              'name_fr': 'Nommer le solide'},
        {'slug': 'g3-prism-or-pyramid',      'name_en': 'Prisms & Pyramids',           'name_fr': 'Prismes et pyramides'},
        {'slug': 'g3-net-match',             'name_en': 'Nets of Prisms',              'name_fr': 'Développements de prismes'},
        {'slug': 'g3-convex',                'name_en': 'Convex Polygons',             'name_fr': 'Polygones convexes'},
        {'slug': 'g3-congruent',             'name_en': 'Congruent Shapes',            'name_fr': 'Figures isométriques'},
        {'slug': 'g3-symmetry-axis',         'name_en': 'Lines of Symmetry',           'name_fr': 'Axes de symétrie'},
        {'slug': 'g3-frieze',                'name_en': 'Friezes & Patterns',          'name_fr': 'Frises et régularités'},
        {'slug': 'g3-grid-map',              'name_en': 'Grid Map',                    'name_fr': 'Se repérer sur un plan'},
        {'slug': 'cartesian-place-point',    'name_en': 'Find a Point (x, y)',         'name_fr': 'Repérer un point (x, y)'},
    ]},
    {'name_en': 'Grade 4 — Geometry', 'grade': 4, 'topics': [
        {'slug': 'g4-net-pyramid',           'name_en': 'Nets of Pyramids',            'name_fr': 'Développements de pyramides'},
    ]},
    {'name_en': 'Grade 6 — Geometry', 'name_fr': '6e année — Géométrie', 'icon': '📐', 'grade': 6, 'topics': [
        {'slug': 'g6-triangle-type',         'name_en': 'Types of Triangles',          'name_fr': 'Sortes de triangles'},
        {'slug': 'g6-circle-parts',          'name_en': 'Parts of a Circle',           'name_fr': 'Le cercle'},
        {'slug': 'g6-translation',           'name_en': 'Translations',                'name_fr': 'Translations'},
        {'slug': 'g6-polyhedron-net',        'name_en': 'Polyhedra & Nets',            'name_fr': 'Polyèdres et développements'},
    ]},
    {'name_en': 'Grade 3 — Measurement & Time', 'grade': 3, 'topics': [
        {'slug': 'g3-ruler-mm',              'name_en': 'Read a Ruler (cm, mm)',       'name_fr': 'Lire une règle (cm, mm)'},
        {'slug': 'g3-area-count-squares',    'name_en': 'Area: Count the Squares',     'name_fr': 'Aire : compter les carrés'},
        {'slug': 'g3-volume-count-cubes',    'name_en': 'Volume: Count the Cubes',     'name_fr': 'Volume : compter les cubes'},
        {'slug': 'g3-balance-scale',         'name_en': 'Balance & Mass',              'name_fr': 'Balance et masse'},
        {'slug': 'g3-capacity-estimate',     'name_en': 'Capacity',                    'name_fr': 'Capacité'},
        {'slug': 'g3-thermometer',           'name_en': 'Thermometer',                 'name_fr': 'Le thermomètre'},
    ]},
    {'name_en': 'Grade 4 — Geometry', 'grade': 4, 'topics': [
        {'slug': 'g4-compare-angles',        'name_en': 'Compare Angles',              'name_fr': 'Comparer des angles'},
    ]},
    {'name_en': 'Grade 5 — Measurement', 'grade': 5, 'topics': [
        {'slug': 'g5-estimate-length',       'name_en': 'Estimate Lengths',            'name_fr': 'Estimer des longueurs'},
        {'slug': 'g5-area-units',            'name_en': 'Area Units (cm², m²)',        'name_fr': 'Unités d’aire (cm², m²)'},
    ]},
    {'name_en': 'Grade 6 — Measurement', 'name_fr': '6e année — Mesure', 'icon': '📏', 'grade': 6, 'topics': [
        {'slug': 'g6-protractor',            'name_en': 'Protractor & Degrees',        'name_fr': 'Rapporteur et degrés'},
        {'slug': 'g6-volume-units',          'name_en': 'Volume Units (cm³, L)',       'name_fr': 'Unités de volume (cm³, L)'},
    ]},
    {'name_en': 'Grade 3 — Statistics & Probability', 'grade': 3, 'topics': [
        {'slug': 'g3-pictograph',            'name_en': 'Pictographs',                 'name_fr': 'Diagrammes à pictogrammes'},
        {'slug': 'g3-tally-table',           'name_en': 'Count & Organise Data',       'name_fr': 'Dépouiller des données'},
        {'slug': 'g3-build-chart',           'name_en': 'Which Chart Shows the Data?', 'name_fr': 'Quel diagramme ?'},
        {'slug': 'g3-list-outcomes',         'name_en': 'List the Outcomes',           'name_fr': 'Résultats possibles'},
        {'slug': 'g3-equally-likely',        'name_en': 'Equally Likely',              'name_fr': 'Autant de chances'},
    ]},
    {'name_en': 'Grade 4 — Statistics & Probability', 'name_fr': '4e année — Statistique et probabilité', 'icon': '🎲', 'grade': 4, 'topics': [
        {'slug': 'g4-line-graph',            'name_en': 'Line Graphs',                 'name_fr': 'Diagrammes à ligne brisée'},
        {'slug': 'g4-survey-question',       'name_en': 'Survey Questions',            'name_fr': 'Questions d’enquête'},
        {'slug': 'g4-compare-likelihood',    'name_en': 'More or Less Likely',         'name_fr': 'Plus ou moins probable'},
        {'slug': 'g4-independence',          'name_en': 'Does Chance Remember?',       'name_fr': 'Le hasard a-t-il une mémoire ?'},
        {'slug': 'g4-variability',           'name_en': 'Results Vary',                'name_fr': 'Des résultats qui varient'},
    ]},
    {'name_en': 'Grade 5 — Statistics & Probability', 'grade': 5, 'topics': [
        {'slug': 'g5-probability-line',      'name_en': 'Probability Line (0 to 1)',   'name_fr': 'Droite des probabilités'},
        {'slug': 'g5-tree-diagram',          'name_en': 'Tree Diagrams',               'name_fr': 'Diagrammes en arbre'},
        {'slug': 'g5-simulation',            'name_en': 'Experiments vs Theory',       'name_fr': 'Expérience et théorie'},
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
