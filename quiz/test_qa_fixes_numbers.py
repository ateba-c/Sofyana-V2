"""
Regression tests for the QA-Studio findings on numeration, decimals, fractions
and comparison generators (group E, 2026-10).

Each test pins one fixed accuracy / ambiguity problem so it cannot come back.
"""
import copy
import re
from fractions import Fraction

from django.test import SimpleTestCase

from .generators import GENERATORS
from .labels import localize_problem

LEVELS = ('easy', 'medium', 'hard')
RUNS = 150


def _samples(slug, levels=LEVELS, runs=RUNS):
    for lv in levels:
        for _ in range(runs):
            yield lv, GENERATORS[slug](lv)


def _num(label):
    """'0,25' / '3/4' / '12' (first token) → Fraction."""
    return Fraction(str(label).split(' ')[0].replace(',', '.'))


class ComparisonExplanationTests(SimpleTestCase):
    def test_g4_compare_different_lengths_not_digit_by_digit(self):
        from .generators.g4_comparison import compare_steps
        fr, en = compare_steps(58, 102)
        self.assertIn('102 a 3 chiffres et 58 en a 2', fr)
        self.assertNotIn('gauche', fr)
        self.assertIn('more digits is larger', en)
        fr, en = compare_steps(473, 424)
        self.assertIn('rang des dizaines, 7 > 2', fr)
        self.assertIn('tens place, 7 > 2', en)

    def test_g4_compare_never_says_n_and_n_digits(self):
        for _, q in _samples('g4-compare'):
            self.assertNotRegex(q['explanation_en'], r'have (\d+) and \1 digits')

    def test_g6_compare_stays_below_one_million(self):
        for _, q in _samples('g6-compare'):
            nums = [int(x.replace(' ', '')) for x in re.findall(r'\*\*([\d ]+)\*\*', q['prompt_fr'])]
            self.assertEqual(len(nums), 2)
            self.assertTrue(all(n < 1_000_000 for n in nums), q['prompt_fr'])

    def test_g4_skip_sequence_has_no_negative_step(self):
        seen_desc = False
        for _, q in _samples('g4-skip-sequence'):
            for text in (q['explanation_fr'], q['explanation_en']):
                self.assertNotRegex(text, r'(?<![\w)])[-−]\d', text)
            self.assertNotIn('Subtract the step to', q['explanation_en'])
            if 'decreases by' in q['explanation_en']:
                seen_desc = True
                self.assertIn('diminue de', q['explanation_fr'])
        self.assertTrue(seen_desc)


class NumberLineTests(SimpleTestCase):
    def test_question_mark_tick_never_labelled(self):
        for slug in ('g4-number-line-point', 'g5-number-line'):
            for _, q in _samples(slug):
                sd = q['shape_data'][0]
                self.assertIsNotNone(sd.get('nl_labels'), slug)
                self.assertNotIn(sd['nl_target'], sd['nl_labels'], slug)

    def test_g6_decimal_line_point_not_on_a_label(self):
        for _, q in _samples('g6-decimal-number-line', levels=('hard',)):
            labels = [lab['text'] for lab in q['shape_data'][0]['labels'] if lab['text'] != '?']
            answer = _num(q['correct_answers'][0])
            self.assertNotIn(answer, [_num(t) for t in labels])

    def test_number_line_explanations_pluralised(self):
        for slug in ('g4-number-line-point', 'g5-number-line', 'g6-fraction-on-line'):
            for _, q in _samples(slug, runs=40):
                self.assertNotIn('(s)', q['explanation_fr'] + q['explanation_en'], slug)


class DecimalTests(SimpleTestCase):
    def test_g5_estimate_key_is_the_closest_choice(self):
        for _, q in _samples('g5-estimate-decimal'):
            m = re.search(r'\*\*([\d,]+) (\+|−|×|÷) ([\d,]+)\*\*', q['prompt_fr'])
            a, op, b = _num(m.group(1)), m.group(2), _num(m.group(3))
            exact = {'+': a + b, '−': a - b, '×': a * b, '÷': a / b if b else 0}[op]
            key = next(_num(c['label']) for c in q['choices'] if c['correct'])
            for c in q['choices']:
                if not c['correct']:
                    self.assertGreater(abs(_num(c['label']) - exact), abs(key - exact), q['prompt_fr'])

    def test_english_never_shows_decimal_commas(self):
        slugs = ['g5-estimate-decimal', 'g5-decimal-forms', 'g6-decimal-number-line', 'g4-decimal-number-line',
                 'fraction-to-decimal', 'g6-choose-notation', 'g4-decimal-equivalence', 'g4-round-decimal']
        for slug in slugs:
            for _, q in _samples(slug, runs=40):
                en = localize_problem(copy.deepcopy(q), 'en')
                text = ' '.join([en['prompt_en'], en['hint_en'], en['explanation_en']]
                                + [c['label'] for c in en.get('choices') or []]
                                + [f"{p['left']} {p['right']}" for p in en.get('pairs') or []])
                self.assertNotRegex(text, r'\d,\d', slug)

    def test_truncation_prompt_is_not_rounding(self):
        seen = False
        for _, q in _samples('g4-round-decimal', levels=('hard',), runs=300):
            if q['prompt_fr'].startswith('Tronque'):
                seen = True
                self.assertNotRegex(q['prompt_fr'], r'(?<!a)près')
                self.assertNotIn('nearest', q['prompt_en'])
                self.assertIn('sans arrondir', q['prompt_fr'])
        self.assertTrue(seen)

    def test_choose_notation_fraction_and_percent_differ(self):
        for _, q in _samples('g6-choose-notation'):
            rights = [p['right'] for p in q['pairs']]
            fr = [Fraction(r) for r in rights if '/' in r]
            pct = [Fraction(int(r.split()[0]), 100) for r in rights if '%' in r]
            for f in fr:
                self.assertNotIn(f, pct, rights)

    def test_fraction_to_decimal_explanation_not_tautological(self):
        for _, q in _samples('fraction-to-decimal'):
            self.assertNotRegex(q['explanation_fr'], r'(\d+/100) = \1')


class FractionTests(SimpleTestCase):
    def test_equivalent_strip_no_distractor_equal_to_key(self):
        for _, q in _samples('g4-equivalent-fractions', levels=('easy',)):
            key = next(_num(c['label']) for c in q['choices'] if c['correct'])
            for c in q['choices']:
                if not c['correct']:
                    self.assertNotEqual(_num(c['label']), key, [c['label'] for c in q['choices']])

    def test_fraction_between_choices_are_consecutive_and_unique(self):
        for _, q in _samples('g6-fraction-between'):
            self.assertIn('consécutifs', q['prompt_fr'])
            self.assertIn('consecutive', q['prompt_en'])
            n, d = map(int, re.search(r'\*\*(\d+)/(\d+)\*\*', q['prompt_fr']).groups())
            containing = 0
            for c in q['choices']:
                lo, hi = map(int, re.findall(r'\d+', c['label']))
                self.assertEqual(hi, lo + 1)
                containing += lo < Fraction(n, d) < hi
            self.assertEqual(containing, 1)

    def test_value_distinct_choices(self):
        for slug in ('g6-fraction-on-line', 'fraction-shape'):
            for _, q in _samples(slug):
                vals = [_num(c['label']) for c in q['choices']]
                self.assertEqual(len(vals), len(set(vals)), (slug, [c['label'] for c in q['choices']]))
        for _, q in _samples('g5-fraction-meanings'):
            if ' de ' in q['choices'][0]['label']:
                vals = [_num(c['label']) for c in q['choices']]
                self.assertEqual(len(vals), len(set(vals)))
                self.assertFalse(any(c['label'].endswith('chocola') for c in q['choices']))

    def test_benchmark_explanation_compares_with_one_without_decimals(self):
        for _, q in _samples('g4-fraction-benchmark'):
            self.assertNotRegex(q['explanation_fr'], r'\d\.\d')
            if not re.search(r'\*\*0/', q['prompt_fr']):
                self.assertIn('Comparer à 1', q['explanation_fr'])

    def test_irreducible_question_not_all_multiples_of_key(self):
        seen = False
        for _, q in _samples('g6-simplify-fraction', levels=('hard',), runs=300):
            if 'irréductible' in q['prompt_fr']:
                seen = True
                key = next(_num(c['label']) for c in q['choices'] if c['correct'])
                others = {_num(c['label']) for c in q['choices'] if not c['correct']}
                self.assertNotIn(key, others)
                self.assertGreater(len(others), 1)
        self.assertTrue(seen)


class WordingTests(SimpleTestCase):
    def test_g4_expanded_form_explanation_builds_the_number(self):
        seen = False
        for _, q in _samples('g4-expanded-form'):
            if q['prompt_fr'].startswith('Quel nombre'):
                seen = True
                self.assertIn('Calcule chaque produit', q['explanation_fr'])
                self.assertIn('Work out each product', q['explanation_en'])
        self.assertTrue(seen)

    def test_count_groups_elision_and_plural(self):
        for slug in ('g4-count-groups', 'g6-count-groups'):
            for _, q in _samples(slug):
                text = q['prompt_fr'] + q['hint_fr'] + q['explanation_fr']
                self.assertNotIn('de unités', text)
                self.assertNotIn('de **unités', text)
                self.assertNotRegex(text, r"d'(centaines|dizaines)")
                self.assertNotIn('les 1 chiffres', text)
                self.assertNotIn('(s)', text + q['explanation_en'])

    def test_g6_extreme_english_units(self):
        for _, q in _samples('g6-extreme'):
            en = localize_problem(copy.deepcopy(q), 'en')
            text = en['prompt_en'] + ' '.join(c['label'] for c in en['choices'])
            for word in ('habitants', 'visiteurs', 'vues', 'places'):
                self.assertNotRegex(text, r'' + word + r'')

    def test_grade3_hints_name_only_present_places(self):
        for slug in ('read-number', 'write-number', 'digit-position', 'base10-match', 'decomposition-match',
                     'build-number', 'order-numbers'):
            for _, q in _samples(slug, levels=('easy',), runs=40):
                self.assertNotIn('milliers', q['hint_fr'], slug)
                self.assertNotIn('units', q['hint_en'] + q.get('explanation_en', ''), slug)

    def test_digit_position_english_has_no_french_abbreviations(self):
        for _, q in _samples('g6-digit-position', runs=40):
            en = localize_problem(copy.deepcopy(q), 'en')
            text = en['hint_en'] + ' '.join(c['label'] for c in en['choices'])
            self.assertNotRegex(text, r'\((u|d|c|UM|DM|CM)\)')
