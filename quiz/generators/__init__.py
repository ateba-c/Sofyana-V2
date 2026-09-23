from .arithmetic import (
    add_gen, subtract_gen, multiply_gen, divide_gen,
    decimal_add_gen, decimal_subtract_gen, decimal_multiply_gen, decimal_divide_gen,
)
from .fractions import (
    fraction_add_gen, fraction_subtract_gen, fraction_multiply_gen, fraction_divide_gen,
    fraction_shape_gen,
)
from .comparisons import (
    compare_int_gen, compare_decimal_gen, compare_fraction_gen, compare_mixed_gen,
)
from .conversions import convert_length_gen, convert_mass_gen, convert_volume_gen
from .geometry import (
    geometry_area_gen, geometry_perimeter_gen,
    identify_angle_gen, parallel_perpendicular_gen,
    name_polygon_gen, count_sides_gen,
)
from .number_properties import squares_gen, primes_gen, even_odd_gen

# ── Grade 3 — Numération ──────────────────────────────────────────────────────
from .numeration import (
    read_number_gen, write_number_gen,
    digit_position_gen, digit_value_gen,
    expanded_form_gen, decomposition_match_gen,
    base10_match_gen, build_number_gen, order_numbers_gen,
)

# ── Grade 3 — Termes manquants ────────────────────────────────────────────────
from .missing_terms import missing_addend_gen, missing_subtrahend_gen

# ── Grade 3 — Approximation ───────────────────────────────────────────────────
from .approximation import round_ten_gen, round_hundred_gen, count_groups_gen

# ── Grade 3 — Problèmes & sens des opérations ─────────────────────────────────
from .word_problems import (
    word_problem_gen, multiply_context_gen, repeated_addition_gen,
    division_sharing_gen, choose_operation_gen, read_decimal_gen,
    fraction_to_decimal_gen, number_classify_gen, fraction_collection_gen,
)

# ── Grade 3 — Monnaie ─────────────────────────────────────────────────────────
from .money import money_change_gen, money_composition_gen

# ── Grade 3 — Mesure & Temps ──────────────────────────────────────────────────
from .measurement import measure_unit_gen, read_clock_gen, time_convert_gen, unit_by_quantity_gen

# ── Grade 3 — Espace (repérage cartésien) ────────────────────────────────────
from .space import cartesian_coord_gen

# ── Grade 3 — Suites & Familles de calculs ────────────────────────────────────
from .patterns import number_sequence_gen, fact_family_gen

# ── Grade 3 — Statistiques & Probabilité ─────────────────────────────────────
from .statistics import read_bar_chart_gen, probability_vocab_gen

# ── Grade 3 — Géométrie (solides + périmètre étiqueté) ───────────────────────
from .geometry import identify_solid_gen, perimeter_labeled_gen

# ── Grade 4 ───────────────────────────────────────────────────────────────────
from .g4_numeration import (
    g4_roman_to_arabic_gen, g4_arabic_to_roman_gen, g4_roman_match_gen,
    g4_digit_position_gen, g4_digit_value_gen, g4_expanded_form_gen,
    g4_count_groups_gen, g4_grouping_problem_gen,
)
from .g4_comparison import (
    g4_before_after_gen, g4_compare_gen, g4_order_numbers_gen,
    g4_skip_sequence_gen, g4_number_line_step_gen, g4_number_line_point_gen,
)
from .g4_geometry import (
    g4_lines_gen, g4_quadrilateral_name_gen, g4_quadrilateral_riddle_gen,
    g4_quadrilateral_match_gen, g4_quadrilateral_count_gen,
)
from .g4_time import (
    g4_clock_24h_gen, g4_time_units_gen, g4_elapsed_time_gen, g4_end_time_gen,
)
from .clock import g3_clock_later_gen, g4_clock_back_gen, g5_clock_schedule_gen, g6_clock_planning_gen

# ── Grade 5 ───────────────────────────────────────────────────────────────────
from .g5_arithmetic import (
    g5_order_ops_gen, g5_div_decimal_gen,
    g5_decimal_mult_gen, g5_decimal_div_gen,
)
from .g5_measurement import (
    g5_volume_gen, g5_capacity_convert_gen, g5_mass_convert_gen,
    g5_elapsed_time_gen, g5_temperature_gen, g5_thermometer_gen,
)
from .g5_numeration import (
    g5_large_integer_gen, g5_decimal_write_gen,
    g5_decimal_forms_gen, g5_number_line_gen,
)
from .g5_stats import (
    g5_arithmetic_mean_gen, g5_probability_forms_gen, g5_probability_frac_gen,
    g5_count_outcomes_gen, g5_data_table_gen,
    g5_euler_gen, g5_solid_counts_gen, g5_pie_chart_gen,
)

# ── Grade 6 ───────────────────────────────────────────────────────────────────
from .g6_numeration import (
    g6_digit_position_gen, g6_digit_value_gen, g6_count_groups_gen,
    g6_place_value_change_gen, g6_additive_form_gen, g6_symbol_form_gen,
    g6_multiplicative_form_gen,
)
from .g6_compare import g6_compare_gen, g6_order_gen, g6_extreme_gen, g6_money_compare_gen
from .g6_multiplication import (
    g6_multiply_gen, g6_partial_products_gen, g6_estimate_product_gen, g6_rate_problem_gen,
)
from .g6_fractions import g6_fraction_on_line_gen, g6_fraction_between_gen, g6_fraction_order_gen
from .g6_strategies import g6_relevant_info_gen, g6_comparative_phrase_gen

from .resolution import RESOLUTION, RESOLUTION_FAMILIES


GENERATORS = {
    # ── Integer Arithmetic
    'add':                add_gen,
    'subtract':           subtract_gen,
    'multiply':           multiply_gen,
    'divide':             divide_gen,
    # ── Decimal Arithmetic
    'decimal-add':        decimal_add_gen,
    'decimal-subtract':   decimal_subtract_gen,
    'decimal-multiply':   decimal_multiply_gen,
    'decimal-divide':     decimal_divide_gen,
    # ── Fraction Arithmetic
    'fraction-add':       fraction_add_gen,
    'fraction-subtract':  fraction_subtract_gen,
    'fraction-multiply':  fraction_multiply_gen,
    'fraction-divide':    fraction_divide_gen,
    # ── Comparisons
    'compare-int':        compare_int_gen,
    'compare-decimal':    compare_decimal_gen,
    'compare-fraction':   compare_fraction_gen,
    'compare-mixed':      compare_mixed_gen,
    # ── Metric Conversions
    'convert-length':     convert_length_gen,
    'convert-mass':       convert_mass_gen,
    'convert-volume':     convert_volume_gen,
    # ── Geometry (areas / perimeters)
    'geometry-area':      geometry_area_gen,
    'geometry-perimeter': geometry_perimeter_gen,
    # ── Number Properties
    'squares':            squares_gen,
    'primes':             primes_gen,
    'even-odd':           even_odd_gen,

    # ══════════════════ Grade 3 ════════════════════════════════════════════════

    # Numération (sections 1-3)
    'read-number':         read_number_gen,
    'write-number':        write_number_gen,
    'digit-position':      digit_position_gen,
    'digit-value':         digit_value_gen,
    'expanded-form':       expanded_form_gen,
    'decomposition-match': decomposition_match_gen,
    'base10-match':        base10_match_gen,
    'build-number':        build_number_gen,
    'order-numbers':       order_numbers_gen,

    # Termes manquants (section 8)
    'missing-addend':      missing_addend_gen,
    'missing-subtrahend':  missing_subtrahend_gen,

    # Géométrie grade 3 (sections 9-10)
    'identify-angle':      identify_angle_gen,
    'parallel-perp':       parallel_perpendicular_gen,
    'name-polygon':        name_polygon_gen,
    'count-sides':         count_sides_gen,

    # Approximation & dénombrement (section 11)
    'round-ten':           round_ten_gen,
    'round-hundred':       round_hundred_gen,
    'count-groups':        count_groups_gen,

    # Sens des opérations (section 12)
    'word-problem':        word_problem_gen,
    'multiply-context':    multiply_context_gen,
    'repeated-addition':   repeated_addition_gen,
    'division-sharing':    division_sharing_gen,
    'choose-operation':    choose_operation_gen,

    # Fractions (section 13)
    'fraction-shape':      fraction_shape_gen,

    # Décimaux & monnaie (section 14)
    'read-decimal':        read_decimal_gen,
    'money-change':        money_change_gen,
    'money-match':         money_composition_gen,

    # Mesure & Temps (section 15 + 26)
    'measure-unit':        measure_unit_gen,
    'perimeter-labeled':   perimeter_labeled_gen,
    'read-clock':          read_clock_gen,

    # Statistiques & Probabilité (sections 16 + 27)
    'read-bar-chart':      read_bar_chart_gen,
    'probability-vocab':   probability_vocab_gen,

    # Solides & Suites (sections 17 + 18 + 25)
    'identify-solid':      identify_solid_gen,
    'fact-family':         fact_family_gen,
    'number-sequence':     number_sequence_gen,

    # Décimaux notation (section 21)
    'fraction-to-decimal': fraction_to_decimal_gen,

    # Classification des nombres (section 24)
    'number-classify':     number_classify_gen,

    # Espace — Repérage cartésien (Bloc B2)
    'cartesian-coord':     cartesian_coord_gen,

    # Mesure — Conversions de temps (Bloc C1)
    'time-convert':        time_convert_gen,
    'g3-clock-later':      g3_clock_later_gen,

    # Mesure — Choix d'unité (masse / volume / longueur) (Bloc C2)
    'unit-by-quantity':    unit_by_quantity_gen,

    # Fractions — Fraction d'une collection (Bloc E1)
    'fraction-collection': fraction_collection_gen,

    # ══════════════════ Grade 4 ════════════════════════════════════════════════

    # Numération (§1-2) — chiffres romains, numération de position
    'g4-roman-to-arabic':   g4_roman_to_arabic_gen,
    'g4-arabic-to-roman':   g4_arabic_to_roman_gen,
    'g4-roman-match':       g4_roman_match_gen,
    'g4-digit-position':    g4_digit_position_gen,
    'g4-digit-value':       g4_digit_value_gen,
    'g4-expanded-form':     g4_expanded_form_gen,
    'g4-count-groups':      g4_count_groups_gen,
    'g4-grouping-problem':  g4_grouping_problem_gen,

    # Comparaison, ordre & droite numérique (§3-4)
    'g4-before-after':      g4_before_after_gen,
    'g4-compare':           g4_compare_gen,
    'g4-order-numbers':     g4_order_numbers_gen,
    'g4-skip-sequence':     g4_skip_sequence_gen,
    'g4-number-line-step':  g4_number_line_step_gen,
    'g4-number-line-point': g4_number_line_point_gen,

    # Géométrie (§5) — droites & quadrilatères
    'g4-lines':                 g4_lines_gen,
    'g4-quadrilateral-name':    g4_quadrilateral_name_gen,
    'g4-quadrilateral-riddle':  g4_quadrilateral_riddle_gen,
    'g4-quadrilateral-match':   g4_quadrilateral_match_gen,
    'g4-quadrilateral-count':   g4_quadrilateral_count_gen,

    # Mesure du temps (§6)
    'g4-clock-24h':         g4_clock_24h_gen,
    'g4-time-units':        g4_time_units_gen,
    'g4-elapsed-time':      g4_elapsed_time_gen,
    'g4-end-time':          g4_end_time_gen,
    'g4-clock-back':        g4_clock_back_gen,

    # ══════════════════ Grade 5 ════════════════════════════════════════════════

    # Arithmetic
    'g5-order-ops':      g5_order_ops_gen,
    'g5-div-decimal':    g5_div_decimal_gen,
    'g5-decimal-mult':   g5_decimal_mult_gen,
    'g5-decimal-div':    g5_decimal_div_gen,

    # Measurement
    'g5-volume':          g5_volume_gen,
    'g5-capacity-convert': g5_capacity_convert_gen,
    'g5-mass-convert':    g5_mass_convert_gen,
    'g5-elapsed-time':    g5_elapsed_time_gen,
    'g5-clock-schedule':  g5_clock_schedule_gen,
    'g5-temperature':     g5_temperature_gen,
    'g5-thermometer':     g5_thermometer_gen,
    'g6-clock-planning':  g6_clock_planning_gen,

    # Numeration
    'g5-large-integer':   g5_large_integer_gen,
    'g5-decimal-write':   g5_decimal_write_gen,
    'g5-decimal-forms':   g5_decimal_forms_gen,
    'g5-number-line':     g5_number_line_gen,

    # Statistics & Probability
    'g5-arithmetic-mean':    g5_arithmetic_mean_gen,
    'g5-probability-forms':  g5_probability_forms_gen,
    'g5-probability-frac':   g5_probability_frac_gen,
    'g5-count-outcomes':     g5_count_outcomes_gen,
    'g5-data-table':         g5_data_table_gen,
    'g5-euler':              g5_euler_gen,
    'g5-solid-counts':       g5_solid_counts_gen,
    'g5-pie-chart':          g5_pie_chart_gen,

    # ══════════════════ Grade 6 ════════════════════════════════════════════════

    # Numération & décomposition (§1-2)
    'g6-digit-position':      g6_digit_position_gen,
    'g6-digit-value':         g6_digit_value_gen,
    'g6-count-groups':        g6_count_groups_gen,
    'g6-place-value-change':  g6_place_value_change_gen,
    'g6-additive-form':       g6_additive_form_gen,
    'g6-symbol-form':         g6_symbol_form_gen,
    'g6-multiplicative-form': g6_multiplicative_form_gen,

    # Comparer et ordonner (§3)
    'g6-compare':             g6_compare_gen,
    'g6-order':               g6_order_gen,
    'g6-extreme':             g6_extreme_gen,
    'g6-money-compare':       g6_money_compare_gen,

    # Multiplication & estimation (§4-5)
    'g6-multiply':            g6_multiply_gen,
    'g6-partial-products':    g6_partial_products_gen,
    'g6-estimate-product':    g6_estimate_product_gen,
    'g6-rate-problem':        g6_rate_problem_gen,

    # Fractions sur la droite numérique (§6)
    'g6-fraction-on-line':    g6_fraction_on_line_gen,
    'g6-fraction-between':    g6_fraction_between_gen,
    'g6-fraction-order':      g6_fraction_order_gen,

    # Stratégies de résolution (§7)
    'g6-relevant-info':       g6_relevant_info_gen,
    'g6-comparative-phrase':  g6_comparative_phrase_gen,
}

# ── Skill progression map ─────────────────────────────────────────────────────
SKILL_MAP = {
    # ── Integer Arithmetic
    'add':      {'prereq': None,       'next': 'subtract',       'mastery_next': 'multiply',       'downgrade': None,          'level_sequence': ['easy', 'medium', 'hard']},
    'subtract': {'prereq': 'add',      'next': 'multiply',       'mastery_next': 'decimal-add',    'downgrade': 'add',         'level_sequence': ['easy', 'medium', 'hard']},
    'multiply': {'prereq': 'add',      'next': 'divide',         'mastery_next': 'decimal-multiply','downgrade': 'add',         'level_sequence': ['easy', 'medium', 'hard']},
    'divide':   {'prereq': 'multiply', 'next': 'fraction-add',   'mastery_next': 'decimal-divide',  'downgrade': 'multiply',    'level_sequence': ['easy', 'medium', 'hard']},
    # ── Decimal Arithmetic
    'decimal-add':      {'prereq': 'add',           'next': 'decimal-subtract',    'mastery_next': 'decimal-multiply',  'downgrade': 'add',           'level_sequence': ['easy', 'medium', 'hard']},
    'decimal-subtract': {'prereq': 'subtract',       'next': 'decimal-multiply',    'mastery_next': 'decimal-divide',    'downgrade': 'subtract',      'level_sequence': ['easy', 'medium', 'hard']},
    'decimal-multiply': {'prereq': 'multiply',       'next': 'decimal-divide',      'mastery_next': 'fraction-multiply', 'downgrade': 'multiply',      'level_sequence': ['easy', 'medium', 'hard']},
    'decimal-divide':   {'prereq': 'divide',         'next': 'fraction-add',        'mastery_next': 'fraction-divide',   'downgrade': 'divide',        'level_sequence': ['easy', 'medium', 'hard']},
    # ── Fraction Arithmetic
    'fraction-add':      {'prereq': 'add',            'next': 'fraction-subtract',   'mastery_next': 'fraction-multiply', 'downgrade': 'add',           'level_sequence': ['easy', 'medium', 'hard']},
    'fraction-subtract': {'prereq': 'fraction-add',   'next': 'fraction-multiply',   'mastery_next': 'compare-fraction',  'downgrade': 'fraction-add',  'level_sequence': ['easy', 'medium', 'hard']},
    'fraction-multiply': {'prereq': 'multiply',        'next': 'fraction-divide',     'mastery_next': 'compare-fraction',  'downgrade': 'multiply',      'level_sequence': ['easy', 'medium', 'hard']},
    'fraction-divide':   {'prereq': 'fraction-multiply','next': 'compare-fraction',   'mastery_next': 'compare-mixed',    'downgrade': 'fraction-multiply','level_sequence': ['easy', 'medium', 'hard']},
    # ── Comparisons
    'compare-int':      {'prereq': 'add',            'next': 'compare-decimal',    'mastery_next': 'compare-fraction', 'downgrade': 'add',           'level_sequence': ['easy', 'medium', 'hard']},
    'compare-decimal':  {'prereq': 'decimal-add',    'next': 'compare-fraction',   'mastery_next': 'compare-mixed',    'downgrade': 'decimal-add',   'level_sequence': ['easy', 'medium', 'hard']},
    'compare-fraction': {'prereq': 'fraction-add',   'next': 'compare-mixed',      'mastery_next': 'convert-length',   'downgrade': 'fraction-add',  'level_sequence': ['easy', 'medium', 'hard']},
    'compare-mixed':    {'prereq': 'compare-fraction','next': 'convert-length',     'mastery_next': 'geometry-area',    'downgrade': 'compare-fraction','level_sequence': ['easy', 'medium', 'hard']},
    # ── Metric Conversions
    'convert-length': {'prereq': 'multiply',   'next': 'convert-mass',   'mastery_next': 'convert-volume',   'downgrade': 'multiply',   'level_sequence': ['easy', 'medium', 'hard']},
    'convert-mass':   {'prereq': 'multiply',   'next': 'convert-volume', 'mastery_next': 'geometry-area',    'downgrade': 'multiply',   'level_sequence': ['easy', 'medium', 'hard']},
    'convert-volume': {'prereq': 'multiply',   'next': 'geometry-area',  'mastery_next': 'geometry-perimeter','downgrade': 'multiply',  'level_sequence': ['easy', 'medium', 'hard']},
    # ── Geometry (area/perimeter)
    'geometry-area':      {'prereq': 'multiply',        'next': 'geometry-perimeter', 'mastery_next': 'compare-mixed',   'downgrade': 'multiply',       'level_sequence': ['easy', 'medium', 'hard']},
    'geometry-perimeter': {'prereq': 'add',              'next': 'geometry-area',      'mastery_next': 'fraction-add',    'downgrade': 'add',             'level_sequence': ['easy', 'medium', 'hard']},
    # ── Number Properties
    'squares':  {'prereq': 'multiply', 'next': 'primes',    'mastery_next': 'even-odd',  'downgrade': 'multiply', 'level_sequence': ['easy', 'medium', 'hard']},
    'primes':   {'prereq': 'divide',   'next': 'even-odd',  'mastery_next': 'squares',   'downgrade': 'divide',   'level_sequence': ['easy', 'medium', 'hard']},
    'even-odd': {'prereq': 'add',      'next': 'primes',    'mastery_next': 'squares',   'downgrade': 'add',      'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Numération ────────────────────────────────────────────────────
    'read-number':         {'prereq': None,             'next': 'write-number',        'mastery_next': 'digit-position',    'downgrade': None,             'level_sequence': ['easy', 'medium', 'hard']},
    'write-number':        {'prereq': 'read-number',    'next': 'digit-position',      'mastery_next': 'expanded-form',     'downgrade': 'read-number',    'level_sequence': ['easy', 'medium', 'hard']},
    'digit-position':      {'prereq': 'read-number',    'next': 'digit-value',         'mastery_next': 'expanded-form',     'downgrade': 'read-number',    'level_sequence': ['easy', 'medium', 'hard']},
    'digit-value':         {'prereq': 'digit-position', 'next': 'expanded-form',       'mastery_next': 'decomposition-match','downgrade': 'digit-position', 'level_sequence': ['easy', 'medium', 'hard']},
    'expanded-form':       {'prereq': 'digit-value',    'next': 'decomposition-match', 'mastery_next': 'order-numbers',     'downgrade': 'digit-value',    'level_sequence': ['easy', 'medium', 'hard']},
    'decomposition-match': {'prereq': 'expanded-form',  'next': 'base10-match',        'mastery_next': 'order-numbers',     'downgrade': 'expanded-form',  'level_sequence': ['easy', 'medium', 'hard']},
    'base10-match':        {'prereq': 'digit-position', 'next': 'order-numbers',       'mastery_next': 'compare-int',       'downgrade': 'digit-position', 'level_sequence': ['easy', 'medium', 'hard']},
    'build-number':        {'prereq': 'digit-value',    'next': 'order-numbers',       'mastery_next': 'compare-int',       'downgrade': 'digit-value',    'level_sequence': ['easy', 'medium', 'hard']},
    'order-numbers':       {'prereq': 'compare-int',    'next': 'missing-addend',      'mastery_next': 'round-ten',         'downgrade': 'compare-int',    'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Termes manquants ─────────────────────────────────────────────
    'missing-addend':      {'prereq': 'add',             'next': 'missing-subtrahend',  'mastery_next': 'word-problem',     'downgrade': 'add',            'level_sequence': ['easy', 'medium', 'hard']},
    'missing-subtrahend':  {'prereq': 'missing-addend',  'next': 'word-problem',        'mastery_next': 'multiply-context', 'downgrade': 'missing-addend', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Géométrie ────────────────────────────────────────────────────
    'identify-angle':      {'prereq': None,              'next': 'parallel-perp',       'mastery_next': 'name-polygon',     'downgrade': None,             'level_sequence': ['easy', 'medium', 'hard']},
    'parallel-perp':       {'prereq': 'identify-angle',  'next': 'name-polygon',        'mastery_next': 'count-sides',      'downgrade': 'identify-angle', 'level_sequence': ['easy', 'medium', 'hard']},
    'name-polygon':        {'prereq': 'identify-angle',  'next': 'count-sides',         'mastery_next': 'geometry-area',    'downgrade': 'identify-angle', 'level_sequence': ['easy', 'medium', 'hard']},
    'count-sides':         {'prereq': 'name-polygon',    'next': 'geometry-area',       'mastery_next': 'geometry-perimeter','downgrade': 'name-polygon',   'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Approximation ────────────────────────────────────────────────
    'round-ten':           {'prereq': 'compare-int',     'next': 'round-hundred',       'mastery_next': 'count-groups',     'downgrade': 'compare-int',    'level_sequence': ['easy', 'medium', 'hard']},
    'round-hundred':       {'prereq': 'round-ten',       'next': 'count-groups',        'mastery_next': 'word-problem',     'downgrade': 'round-ten',      'level_sequence': ['easy', 'medium', 'hard']},
    'count-groups':        {'prereq': 'multiply',        'next': 'multiply-context',    'mastery_next': 'division-sharing', 'downgrade': 'multiply',       'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Sens des opérations ─────────────────────────────────────────
    'word-problem':        {'prereq': 'add',             'next': 'multiply-context',    'mastery_next': 'choose-operation', 'downgrade': 'add',            'level_sequence': ['easy', 'medium', 'hard']},
    'multiply-context':    {'prereq': 'multiply',        'next': 'repeated-addition',   'mastery_next': 'division-sharing', 'downgrade': 'multiply',       'level_sequence': ['easy', 'medium', 'hard']},
    'repeated-addition':   {'prereq': 'multiply-context','next': 'division-sharing',    'mastery_next': 'choose-operation', 'downgrade': 'multiply-context','level_sequence': ['easy', 'medium', 'hard']},
    'division-sharing':    {'prereq': 'divide',          'next': 'choose-operation',    'mastery_next': 'fraction-shape',   'downgrade': 'divide',         'level_sequence': ['easy', 'medium', 'hard']},
    'choose-operation':    {'prereq': 'word-problem',    'next': 'fraction-shape',      'mastery_next': 'read-decimal',     'downgrade': 'word-problem',   'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Fractions ────────────────────────────────────────────────────
    'fraction-shape':      {'prereq': 'divide',          'next': 'compare-fraction',    'mastery_next': 'fraction-add',     'downgrade': 'divide',         'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Décimaux & Monnaie ───────────────────────────────────────────
    'read-decimal':        {'prereq': 'read-number',     'next': 'compare-decimal',     'mastery_next': 'money-change',        'downgrade': 'read-number',      'level_sequence': ['easy', 'medium', 'hard']},
    'money-change':        {'prereq': 'decimal-add',     'next': 'money-match',         'mastery_next': 'compare-decimal',     'downgrade': 'decimal-add',      'level_sequence': ['easy', 'medium', 'hard']},
    'money-match':         {'prereq': 'money-change',    'next': 'compare-decimal',     'mastery_next': 'decimal-add',         'downgrade': 'money-change',     'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Mesure & Temps ───────────────────────────────────────────────
    'measure-unit':        {'prereq': None,              'next': 'perimeter-labeled',   'mastery_next': 'read-clock',          'downgrade': None,               'level_sequence': ['easy', 'medium', 'hard']},
    'perimeter-labeled':   {'prereq': 'add',             'next': 'read-clock',          'mastery_next': 'geometry-perimeter',  'downgrade': 'add',              'level_sequence': ['easy', 'medium', 'hard']},
    'read-clock':          {'prereq': None,              'next': 'number-sequence',     'mastery_next': 'measure-unit',        'downgrade': None,               'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Statistiques & Probabilité ──────────────────────────────────
    'read-bar-chart':      {'prereq': None,              'next': 'probability-vocab',   'mastery_next': 'number-classify',     'downgrade': None,               'level_sequence': ['easy', 'medium', 'hard']},
    'probability-vocab':   {'prereq': None,              'next': 'read-bar-chart',      'mastery_next': 'number-classify',     'downgrade': None,               'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Solides & Suites ─────────────────────────────────────────────
    'identify-solid':      {'prereq': 'name-polygon',   'next': 'fact-family',         'mastery_next': 'number-sequence',     'downgrade': 'name-polygon',     'level_sequence': ['easy', 'medium', 'hard']},
    'fact-family':         {'prereq': 'multiply',        'next': 'number-sequence',     'mastery_next': 'divide',              'downgrade': 'multiply',         'level_sequence': ['easy', 'medium', 'hard']},
    'number-sequence':     {'prereq': 'add',             'next': 'fact-family',         'mastery_next': 'round-ten',           'downgrade': 'add',              'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Décimaux notation & Classification ───────────────────────────
    'fraction-to-decimal': {'prereq': 'read-decimal',   'next': 'compare-decimal',     'mastery_next': 'decimal-add',         'downgrade': 'read-decimal',     'level_sequence': ['easy', 'medium', 'hard']},
    'number-classify':     {'prereq': 'even-odd',        'next': 'primes',              'mastery_next': 'squares',             'downgrade': 'even-odd',         'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Espace ───────────────────────────────────────────────────────
    'cartesian-coord':     {'prereq': None,              'next': 'read-bar-chart',      'mastery_next': 'compare-int',         'downgrade': None,               'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Mesure étendue ───────────────────────────────────────────────
    'time-convert':        {'prereq': 'read-clock',      'next': 'measure-unit',        'mastery_next': 'unit-by-quantity',    'downgrade': 'read-clock',       'level_sequence': ['easy', 'medium', 'hard']},
    'g3-clock-later':      {'prereq': 'read-clock',      'next': 'time-convert',        'mastery_next': 'g4-clock-back',       'downgrade': 'read-clock',       'level_sequence': ['easy', 'medium', 'hard']},
    'unit-by-quantity':    {'prereq': 'measure-unit',    'next': 'time-convert',        'mastery_next': 'convert-length',      'downgrade': 'measure-unit',     'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 3: Fraction d'une collection ───────────────────────────────────
    'fraction-collection': {'prereq': 'fraction-shape',  'next': 'compare-fraction',    'mastery_next': 'fraction-add',        'downgrade': 'fraction-shape',   'level_sequence': ['easy', 'medium', 'hard']},

    # ══════════════════ Grade 4 ═══════════════════════════════════════════════

    # ── Grade 4: Numération ───────────────────────────────────────────────────
    'g4-roman-to-arabic': {'prereq': None, 'next': 'g4-arabic-to-roman', 'mastery_next': 'g4-roman-match', 'downgrade': None, 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-arabic-to-roman': {'prereq': 'g4-roman-to-arabic', 'next': 'g4-roman-match', 'mastery_next': 'g4-digit-position', 'downgrade': 'g4-roman-to-arabic', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-roman-match': {'prereq': 'g4-roman-to-arabic', 'next': 'g4-digit-position', 'mastery_next': 'g4-digit-value', 'downgrade': 'g4-arabic-to-roman', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-digit-position': {'prereq': None, 'next': 'g4-digit-value', 'mastery_next': 'g4-expanded-form', 'downgrade': 'digit-position', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-digit-value': {'prereq': 'g4-digit-position', 'next': 'g4-expanded-form', 'mastery_next': 'g4-count-groups', 'downgrade': 'g4-digit-position', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-expanded-form': {'prereq': 'g4-digit-value', 'next': 'g4-count-groups', 'mastery_next': 'g4-grouping-problem', 'downgrade': 'g4-digit-value', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-count-groups': {'prereq': 'g4-expanded-form', 'next': 'g4-grouping-problem', 'mastery_next': 'g4-before-after', 'downgrade': 'g4-expanded-form', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-grouping-problem': {'prereq': 'g4-count-groups', 'next': 'g4-before-after', 'mastery_next': 'g4-compare', 'downgrade': 'g4-count-groups', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 4: Comparaison, ordre & droite numérique ────────────────────────
    'g4-before-after': {'prereq': None, 'next': 'g4-compare', 'mastery_next': 'g4-order-numbers', 'downgrade': 'g4-digit-position', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-compare': {'prereq': 'g4-before-after', 'next': 'g4-order-numbers', 'mastery_next': 'g4-skip-sequence', 'downgrade': 'g4-before-after', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-order-numbers': {'prereq': 'g4-compare', 'next': 'g4-skip-sequence', 'mastery_next': 'g4-number-line-step', 'downgrade': 'g4-compare', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-skip-sequence': {'prereq': 'g4-order-numbers', 'next': 'g4-number-line-step', 'mastery_next': 'g4-number-line-point', 'downgrade': 'g4-order-numbers', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-number-line-step': {'prereq': 'g4-skip-sequence', 'next': 'g4-number-line-point', 'mastery_next': 'g4-lines', 'downgrade': 'g4-skip-sequence', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-number-line-point': {'prereq': 'g4-number-line-step', 'next': 'g4-lines', 'mastery_next': 'g4-quadrilateral-name', 'downgrade': 'g4-number-line-step', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 4: Géométrie ────────────────────────────────────────────────────
    'g4-lines': {'prereq': None, 'next': 'g4-quadrilateral-name', 'mastery_next': 'g4-quadrilateral-riddle', 'downgrade': 'parallel-perp', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-quadrilateral-name': {'prereq': 'g4-lines', 'next': 'g4-quadrilateral-riddle', 'mastery_next': 'g4-quadrilateral-match', 'downgrade': 'g4-lines', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-quadrilateral-riddle': {'prereq': 'g4-quadrilateral-name', 'next': 'g4-quadrilateral-match', 'mastery_next': 'g4-quadrilateral-count', 'downgrade': 'g4-quadrilateral-name', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-quadrilateral-match': {'prereq': 'g4-quadrilateral-riddle', 'next': 'g4-quadrilateral-count', 'mastery_next': 'g4-clock-24h', 'downgrade': 'g4-quadrilateral-riddle', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-quadrilateral-count': {'prereq': 'g4-quadrilateral-match', 'next': 'g4-clock-24h', 'mastery_next': 'g4-time-units', 'downgrade': 'g4-quadrilateral-match', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 4: Mesure du temps ──────────────────────────────────────────────
    'g4-clock-24h': {'prereq': None, 'next': 'g4-time-units', 'mastery_next': 'g4-elapsed-time', 'downgrade': 'read-clock', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-time-units': {'prereq': 'g4-clock-24h', 'next': 'g4-elapsed-time', 'mastery_next': 'g4-end-time', 'downgrade': 'g4-clock-24h', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-elapsed-time': {'prereq': 'g4-time-units', 'next': 'g4-end-time', 'mastery_next': 'g5-elapsed-time', 'downgrade': 'g4-time-units', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-end-time': {'prereq': 'g4-elapsed-time', 'next': 'g4-clock-back', 'mastery_next': 'g5-elapsed-time', 'downgrade': 'g4-elapsed-time', 'level_sequence': ['easy', 'medium', 'hard']},
    'g4-clock-back': {'prereq': 'g4-end-time', 'next': 'g5-clock-schedule', 'mastery_next': 'g5-clock-schedule', 'downgrade': 'g3-clock-later', 'level_sequence': ['easy', 'medium', 'hard']},

    # ══════════════════ Grade 5 ═══════════════════════════════════════════════

    # ── Grade 5: Arithmetic ───────────────────────────────────────────────────
    'g5-order-ops':    {'prereq': None,              'next': 'g5-decimal-mult',   'mastery_next': 'g5-div-decimal',    'downgrade': None,              'level_sequence': ['easy', 'medium', 'hard']},
    'g5-div-decimal':  {'prereq': 'g5-order-ops',    'next': 'g5-decimal-div',    'mastery_next': 'g5-decimal-mult',   'downgrade': 'g5-order-ops',    'level_sequence': ['easy', 'medium', 'hard']},
    'g5-decimal-mult': {'prereq': 'g5-order-ops',    'next': 'g5-div-decimal',    'mastery_next': 'g5-decimal-div',    'downgrade': 'g5-order-ops',    'level_sequence': ['easy', 'medium', 'hard']},
    'g5-decimal-div':  {'prereq': 'g5-decimal-mult', 'next': 'g5-order-ops',      'mastery_next': 'g5-volume',         'downgrade': 'g5-decimal-mult', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 5: Measurement ──────────────────────────────────────────────────
    'g5-volume':           {'prereq': None,                'next': 'g5-capacity-convert', 'mastery_next': 'g5-mass-convert',   'downgrade': None,                'level_sequence': ['easy', 'medium', 'hard']},
    'g5-capacity-convert': {'prereq': 'g5-volume',         'next': 'g5-mass-convert',     'mastery_next': 'g5-elapsed-time',   'downgrade': 'g5-volume',         'level_sequence': ['easy', 'medium', 'hard']},
    'g5-mass-convert':     {'prereq': 'g5-volume',         'next': 'g5-elapsed-time',     'mastery_next': 'g5-temperature',    'downgrade': 'g5-volume',         'level_sequence': ['easy', 'medium', 'hard']},
    'g5-elapsed-time':     {'prereq': 'g5-mass-convert',   'next': 'g5-clock-schedule',   'mastery_next': 'g5-temperature',    'downgrade': 'g5-mass-convert',   'level_sequence': ['easy', 'medium', 'hard']},
    'g5-clock-schedule':   {'prereq': 'g5-elapsed-time',   'next': 'g5-temperature',      'mastery_next': 'g6-clock-planning', 'downgrade': 'g4-clock-back',     'level_sequence': ['easy', 'medium', 'hard']},
    'g5-temperature':      {'prereq': 'g5-elapsed-time',   'next': 'g5-thermometer',      'mastery_next': 'g5-large-integer',  'downgrade': 'g5-elapsed-time',   'level_sequence': ['easy', 'medium', 'hard']},
    'g5-thermometer':      {'prereq': 'g5-temperature',    'next': 'g5-large-integer',    'mastery_next': 'g5-decimal-write',  'downgrade': 'g5-temperature',    'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 5: Numeration ───────────────────────────────────────────────────
    'g5-large-integer': {'prereq': None,               'next': 'g5-decimal-write', 'mastery_next': 'g5-decimal-forms',  'downgrade': None,               'level_sequence': ['easy', 'medium', 'hard']},
    'g5-decimal-write': {'prereq': 'g5-large-integer', 'next': 'g5-decimal-forms', 'mastery_next': 'g5-number-line',    'downgrade': 'g5-large-integer', 'level_sequence': ['easy', 'medium', 'hard']},
    'g5-decimal-forms': {'prereq': 'g5-decimal-write', 'next': 'g5-number-line',   'mastery_next': 'g5-arithmetic-mean','downgrade': 'g5-decimal-write', 'level_sequence': ['easy', 'medium', 'hard']},
    'g5-number-line':   {'prereq': 'g5-decimal-forms', 'next': 'g5-decimal-write', 'mastery_next': 'g5-large-integer',  'downgrade': 'g5-decimal-forms', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 5: Statistics & Probability ────────────────────────────────────
    'g5-arithmetic-mean':   {'prereq': None,                  'next': 'g5-data-table',       'mastery_next': 'g5-pie-chart',      'downgrade': None,                  'level_sequence': ['easy', 'medium', 'hard']},
    'g5-data-table':        {'prereq': 'g5-arithmetic-mean',  'next': 'g5-pie-chart',        'mastery_next': 'g5-probability-frac','downgrade': 'g5-arithmetic-mean', 'level_sequence': ['easy', 'medium', 'hard']},
    'g5-pie-chart':         {'prereq': 'g5-data-table',       'next': 'g5-probability-frac', 'mastery_next': 'g5-probability-forms','downgrade': 'g5-data-table',     'level_sequence': ['easy', 'medium', 'hard']},
    'g5-probability-frac':  {'prereq': None,                  'next': 'g5-probability-forms','mastery_next': 'g5-count-outcomes',  'downgrade': None,                  'level_sequence': ['easy', 'medium', 'hard']},
    'g5-probability-forms': {'prereq': 'g5-probability-frac', 'next': 'g5-count-outcomes',   'mastery_next': 'g5-pie-chart',      'downgrade': 'g5-probability-frac', 'level_sequence': ['easy', 'medium', 'hard']},
    'g5-count-outcomes':    {'prereq': 'g5-probability-frac', 'next': 'g5-euler',            'mastery_next': 'g5-solid-counts',   'downgrade': 'g5-probability-frac', 'level_sequence': ['easy', 'medium', 'hard']},
    'g5-euler':             {'prereq': None,                  'next': 'g5-solid-counts',     'mastery_next': 'g5-count-outcomes', 'downgrade': None,                  'level_sequence': ['easy', 'medium', 'hard']},
    'g5-solid-counts':      {'prereq': 'g5-euler',            'next': 'g5-euler',            'mastery_next': 'g5-count-outcomes', 'downgrade': 'g5-euler',            'level_sequence': ['easy', 'medium', 'hard']},

    # ══════════════════ Grade 6 ═══════════════════════════════════════════════

    # ── Grade 6: Numération ───────────────────────────────────────────────────
    'g6-digit-position': {'prereq': None, 'next': 'g6-digit-value', 'mastery_next': 'g6-count-groups', 'downgrade': 'g4-digit-position', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-digit-value': {'prereq': 'g6-digit-position', 'next': 'g6-count-groups', 'mastery_next': 'g6-place-value-change', 'downgrade': 'g6-digit-position', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-count-groups': {'prereq': 'g6-digit-value', 'next': 'g6-place-value-change', 'mastery_next': 'g6-additive-form', 'downgrade': 'g6-digit-value', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-place-value-change': {'prereq': 'g6-count-groups', 'next': 'g6-additive-form', 'mastery_next': 'g6-symbol-form', 'downgrade': 'g6-count-groups', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-additive-form': {'prereq': 'g6-digit-value', 'next': 'g6-symbol-form', 'mastery_next': 'g6-multiplicative-form', 'downgrade': 'g6-digit-value', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-symbol-form': {'prereq': 'g6-additive-form', 'next': 'g6-multiplicative-form', 'mastery_next': 'g6-compare', 'downgrade': 'g6-additive-form', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-multiplicative-form': {'prereq': 'g6-additive-form', 'next': 'g6-compare', 'mastery_next': 'g6-order', 'downgrade': 'g6-additive-form', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 6: Comparer et ordonner ─────────────────────────────────────────
    'g6-compare': {'prereq': None, 'next': 'g6-order', 'mastery_next': 'g6-extreme', 'downgrade': 'g4-compare', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-order': {'prereq': 'g6-compare', 'next': 'g6-extreme', 'mastery_next': 'g6-money-compare', 'downgrade': 'g6-compare', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-extreme': {'prereq': 'g6-order', 'next': 'g6-money-compare', 'mastery_next': 'g6-multiply', 'downgrade': 'g6-order', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-money-compare': {'prereq': 'g6-compare', 'next': 'g6-multiply', 'mastery_next': 'g6-estimate-product', 'downgrade': 'g6-compare', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 6: Multiplication & estimation ──────────────────────────────────
    'g6-multiply': {'prereq': None, 'next': 'g6-partial-products', 'mastery_next': 'g6-estimate-product', 'downgrade': 'multiply', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-partial-products': {'prereq': 'g6-multiply', 'next': 'g6-estimate-product', 'mastery_next': 'g6-rate-problem', 'downgrade': 'g6-multiply', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-estimate-product': {'prereq': 'g6-multiply', 'next': 'g6-rate-problem', 'mastery_next': 'g6-comparative-phrase', 'downgrade': 'g6-multiply', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-rate-problem': {'prereq': 'g6-estimate-product', 'next': 'g6-comparative-phrase', 'mastery_next': 'g6-relevant-info', 'downgrade': 'g6-estimate-product', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 6: Fractions ────────────────────────────────────────────────────
    'g6-fraction-on-line': {'prereq': None, 'next': 'g6-fraction-between', 'mastery_next': 'g6-fraction-order', 'downgrade': 'fraction-shape', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-fraction-between': {'prereq': 'g6-fraction-on-line', 'next': 'g6-fraction-order', 'mastery_next': 'compare-fraction', 'downgrade': 'g6-fraction-on-line', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-fraction-order': {'prereq': 'g6-fraction-between', 'next': 'g6-fraction-on-line', 'mastery_next': 'compare-fraction', 'downgrade': 'g6-fraction-between', 'level_sequence': ['easy', 'medium', 'hard']},

    # ── Grade 6: Stratégies ───────────────────────────────────────────────────
    'g6-relevant-info': {'prereq': None, 'next': 'g6-comparative-phrase', 'mastery_next': 'g6-rate-problem', 'downgrade': 'word-problem', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-comparative-phrase': {'prereq': 'g6-relevant-info', 'next': 'g6-rate-problem', 'mastery_next': 'g6-multiply', 'downgrade': 'g6-relevant-info', 'level_sequence': ['easy', 'medium', 'hard']},
    'g6-clock-planning': {'prereq': 'g5-clock-schedule', 'next': 'g6-relevant-info', 'mastery_next': 'g6-rate-problem', 'downgrade': 'g5-clock-schedule', 'level_sequence': ['easy', 'medium', 'hard']},
}

# ── 4th level "Résolution": qualifying skills get a longer level sequence ─────
LEVEL_NAMES = {
    'easy':       ('Easy', 'Facile'),
    'medium':     ('Medium', 'Moyen'),
    'hard':       ('Hard', 'Difficile'),
    'resolution': ('Problem solving', 'Résolution'),
}
for _slug in RESOLUTION_FAMILIES:
    if _slug in SKILL_MAP and 'resolution' not in SKILL_MAP[_slug]['level_sequence']:
        SKILL_MAP[_slug]['level_sequence'] = SKILL_MAP[_slug]['level_sequence'] + ['resolution']


def generator_for(slug, level):
    """The callable that produces a problem for (slug, level); the 4th level has its own generators."""
    if level == 'resolution' and slug in RESOLUTION:
        return RESOLUTION[slug]
    return GENERATORS.get(slug)

TOPIC_GROUPS = [
    # ── Existing advanced groups (not grade-specific) ──────────────────────────
    {'name_en': 'Integer Arithmetic', 'name_fr': 'Arithmétique entière', 'icon': '🔢', 'grade': None, 'topics': [
        {'slug': 'add',      'name_en': 'Addition',       'name_fr': 'Addition'},
        {'slug': 'subtract', 'name_en': 'Subtraction',    'name_fr': 'Soustraction'},
        {'slug': 'multiply', 'name_en': 'Multiplication', 'name_fr': 'Multiplication'},
        {'slug': 'divide',   'name_en': 'Division',       'name_fr': 'Division'},
    ]},
    {'name_en': 'Decimal Arithmetic', 'name_fr': 'Arithmétique décimale', 'icon': '🔡', 'grade': None, 'topics': [
        {'slug': 'decimal-add',      'name_en': 'Decimal Addition',       'name_fr': 'Addition décimale'},
        {'slug': 'decimal-subtract', 'name_en': 'Decimal Subtraction',    'name_fr': 'Soustraction décimale'},
        {'slug': 'decimal-multiply', 'name_en': 'Decimal Multiplication', 'name_fr': 'Multiplication décimale'},
        {'slug': 'decimal-divide',   'name_en': 'Decimal Division',       'name_fr': 'Division décimale'},
    ]},
    {'name_en': 'Fraction Arithmetic', 'name_fr': 'Arithmétique des fractions', 'icon': '½', 'grade': None, 'topics': [
        {'slug': 'fraction-add',      'name_en': 'Fraction Addition',       'name_fr': 'Addition de fractions'},
        {'slug': 'fraction-subtract', 'name_en': 'Fraction Subtraction',    'name_fr': 'Soustraction de fractions'},
        {'slug': 'fraction-multiply', 'name_en': 'Fraction Multiplication', 'name_fr': 'Multiplication de fractions'},
        {'slug': 'fraction-divide',   'name_en': 'Fraction Division',       'name_fr': 'Division de fractions'},
    ]},
    {'name_en': 'Comparisons', 'name_fr': 'Comparaisons', 'icon': '⚖️', 'grade': None, 'topics': [
        {'slug': 'compare-int',      'name_en': 'Compare Integers',  'name_fr': 'Comparer des entiers'},
        {'slug': 'compare-decimal',  'name_en': 'Compare Decimals',  'name_fr': 'Comparer des décimaux'},
        {'slug': 'compare-fraction', 'name_en': 'Compare Fractions', 'name_fr': 'Comparer des fractions'},
        {'slug': 'compare-mixed',    'name_en': 'Compare Mixed',     'name_fr': 'Comparer (mixte)'},
    ]},
    {'name_en': 'Metric Conversions', 'name_fr': 'Conversions métriques', 'icon': '📏', 'grade': None, 'topics': [
        {'slug': 'convert-length', 'name_en': 'Length',  'name_fr': 'Longueur'},
        {'slug': 'convert-mass',   'name_en': 'Mass',    'name_fr': 'Masse'},
        {'slug': 'convert-volume', 'name_en': 'Volume',  'name_fr': 'Volume'},
    ]},
    {'name_en': 'Geometry', 'name_fr': 'Géométrie', 'icon': '📐', 'grade': None, 'topics': [
        {'slug': 'geometry-area',      'name_en': 'Area',      'name_fr': 'Aire'},
        {'slug': 'geometry-perimeter', 'name_en': 'Perimeter', 'name_fr': 'Périmètre'},
    ]},
    {'name_en': 'Number Properties', 'name_fr': 'Propriétés des nombres', 'icon': '🔍', 'grade': None, 'topics': [
        {'slug': 'squares',  'name_en': 'Square Numbers', 'name_fr': 'Carrés parfaits'},
        {'slug': 'primes',   'name_en': 'Prime Numbers',  'name_fr': 'Nombres premiers'},
        {'slug': 'even-odd', 'name_en': 'Even & Odd',     'name_fr': 'Pairs & Impairs'},
    ]},

    # ── Grade 3 groups ─────────────────────────────────────────────────────────
    {'name_en': 'Grade 3 — Number Sense', 'name_fr': '3e année — Numération', 'icon': '🔢', 'grade': 3, 'topics': [
        {'slug': 'read-number',         'name_en': 'Read a Number',         'name_fr': 'Lire un nombre'},
        {'slug': 'write-number',        'name_en': 'Write a Number',        'name_fr': 'Écrire un nombre'},
        {'slug': 'digit-position',      'name_en': 'Digit Position',        'name_fr': 'Position d\'un chiffre'},
        {'slug': 'digit-value',         'name_en': 'Digit Value',           'name_fr': 'Valeur d\'un chiffre'},
        {'slug': 'expanded-form',       'name_en': 'Expanded Form',         'name_fr': 'Forme développée'},
        {'slug': 'decomposition-match', 'name_en': 'Decomposition Match',   'name_fr': 'Décomposition (match)'},
        {'slug': 'base10-match',        'name_en': 'Base-10 Match',         'name_fr': 'Base 10 (match)'},
        {'slug': 'build-number',        'name_en': 'Build a Number',        'name_fr': 'Construire un nombre'},
        {'slug': 'order-numbers',       'name_en': 'Order Numbers',         'name_fr': 'Ranger des nombres'},
    ]},
    {'name_en': 'Grade 3 — Arithmetic', 'name_fr': '3e année — Calcul', 'icon': '➕', 'grade': 3, 'topics': [
        {'slug': 'missing-addend',     'name_en': 'Missing Addend',         'name_fr': 'Terme manquant (addition)'},
        {'slug': 'missing-subtrahend', 'name_en': 'Missing Subtrahend',     'name_fr': 'Terme manquant (soustraction)'},
        {'slug': 'word-problem',       'name_en': 'Word Problem',           'name_fr': 'Problème en contexte'},
        {'slug': 'multiply-context',   'name_en': 'Multiplication Context', 'name_fr': 'Sens de la multiplication'},
        {'slug': 'repeated-addition',  'name_en': 'Repeated Addition',      'name_fr': 'Addition répétée ↔ ×'},
        {'slug': 'division-sharing',   'name_en': 'Division as Sharing',    'name_fr': 'Division comme partage'},
        {'slug': 'choose-operation',   'name_en': 'Choose the Operation',   'name_fr': 'Choisir l\'opération'},
        {'slug': 'fact-family',        'name_en': 'Fact Family',            'name_fr': 'Famille de calculs'},
        {'slug': 'number-sequence',    'name_en': 'Number Sequence',        'name_fr': 'Suite numérique'},
        {'slug': 'number-classify',    'name_en': 'Classify a Number',      'name_fr': 'Classifier un nombre'},
    ]},
    {'name_en': 'Grade 3 — Geometry', 'name_fr': '3e année — Géométrie', 'icon': '📐', 'grade': 3, 'topics': [
        {'slug': 'identify-angle',    'name_en': 'Identify Angle',         'name_fr': 'Identifier un angle'},
        {'slug': 'parallel-perp',     'name_en': 'Parallel / Perp.',       'name_fr': 'Parallèles / Perpendiculaires'},
        {'slug': 'name-polygon',      'name_en': 'Name a Polygon',         'name_fr': 'Nommer un polygone'},
        {'slug': 'count-sides',       'name_en': 'Count Sides',            'name_fr': 'Compter les côtés'},
        {'slug': 'identify-solid',    'name_en': 'Identify a Solid',       'name_fr': 'Identifier un solide'},
        {'slug': 'perimeter-labeled', 'name_en': 'Labeled Perimeter',      'name_fr': 'Périmètre (côtés étiquetés)'},
    ]},
    {'name_en': 'Grade 3 — Approximation', 'name_fr': '3e année — Approximation', 'icon': '≈', 'grade': 3, 'topics': [
        {'slug': 'round-ten',     'name_en': 'Round to 10',   'name_fr': 'Arrondir à la dizaine'},
        {'slug': 'round-hundred', 'name_en': 'Round to 100',  'name_fr': 'Arrondir à la centaine'},
        {'slug': 'count-groups',  'name_en': 'Count Groups',  'name_fr': 'Dénombrement par groupes'},
    ]},
    {'name_en': 'Grade 3 — Fractions & Decimals', 'name_fr': '3e année — Fractions & Décimaux', 'icon': '½', 'grade': 3, 'topics': [
        {'slug': 'fraction-shape',      'name_en': 'Fraction of a Shape',      'name_fr': 'Fraction d\'une figure'},
        {'slug': 'fraction-collection', 'name_en': 'Fraction of a Collection', 'name_fr': 'Fraction d\'une collection'},
        {'slug': 'read-decimal',        'name_en': 'Read a Decimal',           'name_fr': 'Lire un décimal'},
        {'slug': 'fraction-to-decimal', 'name_en': 'Fraction → Decimal',       'name_fr': 'Fraction → Décimal'},
    ]},
    {'name_en': 'Grade 3 — Money', 'name_fr': '3e année — Monnaie', 'icon': '💰', 'grade': 3, 'topics': [
        {'slug': 'money-change', 'name_en': 'Calculate Change',    'name_fr': 'Calculer la monnaie'},
        {'slug': 'money-match',  'name_en': 'Money Composition',   'name_fr': 'Composer une somme'},
    ]},
    {'name_en': 'Grade 3 — Measurement & Time', 'name_fr': '3e année — Mesure & Temps', 'icon': '📏', 'grade': 3, 'topics': [
        {'slug': 'measure-unit',      'name_en': 'Choose a Unit',            'name_fr': 'Choisir une unité (longueur)'},
        {'slug': 'unit-by-quantity',  'name_en': 'Unit by Quantity Type',    'name_fr': 'Unité selon la grandeur'},
        {'slug': 'read-clock',        'name_en': 'Read a Clock',             'name_fr': 'Lire l\'heure'},
        {'slug': 'time-convert',      'name_en': 'Convert Time Units',       'name_fr': 'Convertir des unités de temps'},
        {'slug': 'g3-clock-later',    'name_en': 'Clock: In / Ago',          'name_fr': 'Horloge : dans… / il y a…'},
    ]},
    {'name_en': 'Grade 3 — Statistics & Probability', 'name_fr': '3e année — Statistiques & Probabilité', 'icon': '📊', 'grade': 3, 'topics': [
        {'slug': 'read-bar-chart',    'name_en': 'Read a Bar Chart',         'name_fr': 'Lire un diagramme à bandes'},
        {'slug': 'probability-vocab', 'name_en': 'Probability Vocab',        'name_fr': 'Vocabulaire des probabilités'},
        {'slug': 'cartesian-coord',   'name_en': 'Cartesian Coordinates',    'name_fr': 'Repérage cartésien'},
    ]},

    # ── Grade 4 groups ─────────────────────────────────────────────────────────
    {'name_en': 'Grade 4 — Number Sense', 'name_fr': '4e année — Numération', 'icon': '🔢', 'grade': 4, 'topics': [
        {'slug': 'g4-roman-to-arabic',  'name_en': 'Read Roman Numerals',        'name_fr': 'Lire des chiffres romains'},
        {'slug': 'g4-arabic-to-roman',  'name_en': 'Write Roman Numerals',       'name_fr': 'Écrire en chiffres romains'},
        {'slug': 'g4-roman-match',      'name_en': 'Roman Numerals Match',       'name_fr': 'Chiffres romains (associer)'},
        {'slug': 'g4-digit-position',   'name_en': 'Digit Position (to 10 000s)', 'name_fr': 'Position d\'un chiffre (jusqu\'aux dizaines de mille)'},
        {'slug': 'g4-digit-value',      'name_en': 'Digit Value',                'name_fr': 'Valeur d\'un chiffre'},
        {'slug': 'g4-expanded-form',    'name_en': 'Expanded Form (× place value)', 'name_fr': 'Décomposition multiplicative'},
        {'slug': 'g4-count-groups',     'name_en': 'How Many Tens / Hundreds?',  'name_fr': 'Combien de dizaines / centaines ?'},
        {'slug': 'g4-grouping-problem', 'name_en': 'Grouping Word Problems',     'name_fr': 'Problèmes de groupements'},
    ]},
    {'name_en': 'Grade 4 — Compare, Order & Number Line', 'name_fr': '4e année — Comparer, ordonner & droite numérique', 'icon': '⚖️', 'grade': 4, 'topics': [
        {'slug': 'g4-before-after',      'name_en': 'Before & After',            'name_fr': 'Le nombre avant / après'},
        {'slug': 'g4-compare',           'name_en': 'Compare with <, >, =',      'name_fr': 'Comparer avec <, >, ='},
        {'slug': 'g4-order-numbers',     'name_en': 'Ascending / Descending Order', 'name_fr': 'Ordre croissant / décroissant'},
        {'slug': 'g4-skip-sequence',     'name_en': 'Skip-Counting Sequences',   'name_fr': 'Suites de nombres (pas)'},
        {'slug': 'g4-number-line-step',  'name_en': 'Number Line: Find the Step', 'name_fr': 'Droite numérique : le pas'},
        {'slug': 'g4-number-line-point', 'name_en': 'Number Line: Find the Point', 'name_fr': 'Droite numérique : situer un nombre'},
    ]},
    {'name_en': 'Grade 4 — Geometry', 'name_fr': '4e année — Géométrie', 'icon': '📐', 'grade': 4, 'topics': [
        {'slug': 'g4-lines',                'name_en': 'Parallel & Perpendicular Lines', 'name_fr': 'Droites parallèles & perpendiculaires'},
        {'slug': 'g4-quadrilateral-name',   'name_en': 'Name the Quadrilateral',  'name_fr': 'Nommer le quadrilatère'},
        {'slug': 'g4-quadrilateral-riddle', 'name_en': 'Quadrilateral Riddles',   'name_fr': 'Devinettes : quadrilatères'},
        {'slug': 'g4-quadrilateral-match',  'name_en': 'Quadrilateral Definitions', 'name_fr': 'Définitions des quadrilatères'},
        {'slug': 'g4-quadrilateral-count',  'name_en': 'Quadrilateral Properties', 'name_fr': 'Propriétés des quadrilatères'},
    ]},
    {'name_en': 'Grade 4 — Time', 'name_fr': '4e année — Mesure du temps', 'icon': '🕓', 'grade': 4, 'topics': [
        {'slug': 'g4-clock-24h',    'name_en': 'Clock in 24-hour Notation',  'name_fr': 'Horloge en notation 24 h'},
        {'slug': 'g4-time-units',   'name_en': 'Convert Time Units',         'name_fr': 'Convertir des unités de temps'},
        {'slug': 'g4-elapsed-time', 'name_en': 'Elapsed Time',               'name_fr': 'Durée écoulée'},
        {'slug': 'g4-end-time',     'name_en': 'Find the End Time',          'name_fr': 'Trouver l\'heure de fin'},
        {'slug': 'g4-clock-back',   'name_en': 'Clock: Started … Ago',       'name_fr': 'Horloge : commencé il y a…'},
    ]},

    # ── Grade 5 groups ─────────────────────────────────────────────────────────
    {'name_en': 'Grade 5 — Arithmetic', 'name_fr': '5e année — Arithmétique', 'icon': '➗', 'grade': 5, 'topics': [
        {'slug': 'g5-order-ops',    'name_en': 'Order of Operations',    'name_fr': 'Priorité des opérations'},
        {'slug': 'g5-decimal-mult', 'name_en': 'Decimal × Natural',      'name_fr': 'Décimal × entier'},
        {'slug': 'g5-div-decimal',  'name_en': 'Natural ÷ → Decimal',    'name_fr': 'Entier ÷ → décimal'},
        {'slug': 'g5-decimal-div',  'name_en': 'Decimal ÷ Natural',      'name_fr': 'Décimal ÷ entier'},
    ]},
    {'name_en': 'Grade 5 — Measurement', 'name_fr': '5e année — Mesure', 'icon': '📏', 'grade': 5, 'topics': [
        {'slug': 'g5-volume',           'name_en': 'Volume of a Prism',      'name_fr': 'Volume d\'un pavé droit'},
        {'slug': 'g5-capacity-convert', 'name_en': 'L ↔ mL',                'name_fr': 'L ↔ mL'},
        {'slug': 'g5-mass-convert',     'name_en': 'g ↔ kg',                 'name_fr': 'g ↔ kg'},
        {'slug': 'g5-elapsed-time',     'name_en': 'Elapsed Time',           'name_fr': 'Durée écoulée'},
        {'slug': 'g5-clock-schedule',   'name_en': 'Clock: When Does It End?', 'name_fr': 'Horloge : à quelle heure finit-il ?'},
        {'slug': 'g5-temperature',      'name_en': 'Compare Temperatures',   'name_fr': 'Comparer des températures'},
        {'slug': 'g5-thermometer',      'name_en': 'Read a Thermometer',     'name_fr': 'Lire un thermomètre'},
    ]},
    {'name_en': 'Grade 5 — Number Sense', 'name_fr': '5e année — Numération', 'icon': '🔢', 'grade': 5, 'topics': [
        {'slug': 'g5-large-integer',  'name_en': 'Read Large Integers',     'name_fr': 'Lire de grands nombres'},
        {'slug': 'g5-decimal-write',  'name_en': 'Write Decimals',          'name_fr': 'Écrire un décimal'},
        {'slug': 'g5-decimal-forms',  'name_en': 'Decimal Forms',           'name_fr': 'Formes d\'un décimal'},
        {'slug': 'g5-number-line',    'name_en': 'Number Line',             'name_fr': 'Droite numérique'},
    ]},
    {'name_en': 'Grade 5 — Statistics & Probability', 'name_fr': '5e année — Statistiques & Probabilité', 'icon': '📊', 'grade': 5, 'topics': [
        {'slug': 'g5-arithmetic-mean',   'name_en': 'Arithmetic Mean',        'name_fr': 'Moyenne arithmétique'},
        {'slug': 'g5-data-table',        'name_en': 'Data Table',             'name_fr': 'Tableau de données'},
        {'slug': 'g5-pie-chart',         'name_en': 'Pie Chart',              'name_fr': 'Diagramme circulaire'},
        {'slug': 'g5-probability-frac',  'name_en': 'Probability as Fraction','name_fr': 'Probabilité (fraction)'},
        {'slug': 'g5-probability-forms', 'name_en': 'Probability Forms',      'name_fr': 'Formes d\'une probabilité'},
        {'slug': 'g5-count-outcomes',    'name_en': 'Count Outcomes',         'name_fr': 'Dénombrement des résultats'},
        {'slug': 'g5-euler',             'name_en': "Euler's Formula",        'name_fr': 'Formule d\'Euler'},
        {'slug': 'g5-solid-counts',      'name_en': 'Solid Face/Vertex/Edge', 'name_fr': 'Faces, sommets, arêtes'},
    ]},

    # ── Grade 6 groups ─────────────────────────────────────────────────────────
    {'name_en': 'Grade 6 — Number Sense', 'name_fr': '6e année — Numération', 'icon': '🔢', 'grade': 6, 'topics': [
        {'slug': 'g6-digit-position',      'name_en': 'Digit Position (to 100 000s)', 'name_fr': 'Position d\'un chiffre (u, d, c, UM, DM, CM)'},
        {'slug': 'g6-digit-value',         'name_en': 'Digit Value',                  'name_fr': 'Valeur d\'un chiffre'},
        {'slug': 'g6-count-groups',        'name_en': 'How Many Thousands / Hundreds?', 'name_fr': 'Combien d\'unités de mille / de centaines ?'},
        {'slug': 'g6-place-value-change',  'name_en': 'Add Place-Value Units',        'name_fr': 'Ajouter des unités de position'},
        {'slug': 'g6-additive-form',       'name_en': 'Additive Form',                'name_fr': 'Forme additive'},
        {'slug': 'g6-symbol-form',         'name_en': 'Place-Value Symbols (with regrouping)', 'name_fr': 'Notation u, d, c, UM, DM (avec regroupement)'},
        {'slug': 'g6-multiplicative-form', 'name_en': 'Multiplicative Form',          'name_fr': 'Forme multiplicative'},
    ]},
    {'name_en': 'Grade 6 — Compare & Order', 'name_fr': '6e année — Comparer et ordonner', 'icon': '⚖️', 'grade': 6, 'topics': [
        {'slug': 'g6-compare',        'name_en': 'Compare with <, >, =',        'name_fr': 'Comparer avec <, >, ='},
        {'slug': 'g6-order',          'name_en': 'Ascending / Descending Order', 'name_fr': 'Ordre croissant / décroissant'},
        {'slug': 'g6-extreme',        'name_en': 'Largest & Smallest',          'name_fr': 'Le plus grand, le plus petit'},
        {'slug': 'g6-money-compare',  'name_en': 'Banknotes: Total & Compare',  'name_fr': 'Billets : total et comparaison'},
    ]},
    {'name_en': 'Grade 6 — Multiplication & Estimation', 'name_fr': '6e année — Multiplication et estimation', 'icon': '✖️', 'grade': 6, 'topics': [
        {'slug': 'g6-multiply',         'name_en': 'Column Multiplication (× 2 digits)', 'name_fr': 'Multiplication posée à 2 chiffres'},
        {'slug': 'g6-partial-products', 'name_en': 'Partial Products',             'name_fr': 'Produits partiels'},
        {'slug': 'g6-estimate-product', 'name_en': 'Estimate a Product',           'name_fr': 'Estimer un produit'},
        {'slug': 'g6-rate-problem',     'name_en': 'Rate Word Problems',           'name_fr': 'Problèmes : estimation et calcul réel'},
    ]},
    {'name_en': 'Grade 6 — Fractions', 'name_fr': '6e année — Fractions', 'icon': '½', 'grade': 6, 'topics': [
        {'slug': 'g6-fraction-on-line', 'name_en': 'Fractions on a Number Line',   'name_fr': 'Fractions sur la droite numérique'},
        {'slug': 'g6-fraction-between', 'name_en': 'Improper Fractions: Between Which Integers?', 'name_fr': 'Fractions impropres : entre quels entiers ?'},
        {'slug': 'g6-fraction-order',   'name_en': 'Order Fractions',              'name_fr': 'Ordonner des fractions'},
    ]},
    {'name_en': 'Grade 6 — Problem Solving', 'name_fr': '6e année — Stratégies de résolution', 'icon': '🧠', 'grade': 6, 'topics': [
        {'slug': 'g6-relevant-info',      'name_en': 'Spot the Useless Information', 'name_fr': 'Repérer l\'information inutile'},
        {'slug': 'g6-comparative-phrase', 'name_en': 'Translate "more than / less than"', 'name_fr': 'Traduire « plus que / moins que »'},
    ]},
    {'name_en': 'Grade 6 — Time', 'name_fr': '6e année — Mesure du temps', 'icon': '🕓', 'grade': 6, 'topics': [
        {'slug': 'g6-clock-planning', 'name_en': 'Clock: Plan the Schedule', 'name_fr': 'Horloge : planifier l\'horaire'},
    ]},
]
