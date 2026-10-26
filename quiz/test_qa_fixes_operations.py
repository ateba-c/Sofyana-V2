"""
Regression tests for the QA pre-review fixes, group D (operations, word problems,
money).  Each test pins one accuracy / ambiguity bug found in generated questions.
"""
import re
from fractions import Fraction

from django.test import SimpleTestCase

from .answers import check_answer
from .generators import GENERATORS
from .generators.approximation import _round_to
from .generators.g6_multiplication import _round_lead

LEVELS = ('easy', 'medium', 'hard')
RUNS = 150


def _samples(slug, levels=LEVELS, runs=RUNS):
    for level in levels:
        for _ in range(runs):
            yield level, GENERATORS[slug](level)


def _ints(text):
    return [int(x.replace(' ', '').replace(' ', '')) for x in re.findall(r'\d+(?:[  ]\d{3})*', text)]


def _expr_value(label):
    return eval(label.replace('×', '*').replace('÷', '/').replace('−', '-'))   # trusted generator output


def _num(label):
    return int(label.replace(' ', '').replace(' ', '').replace('\xa0', ''))


def _correct(q):
    return next(c for c in q['choices'] if c['correct'])


class RoundingTests(SimpleTestCase):
    def test_a_half_rounds_up(self):
        # Python's round() is banker's rounding: round(4.5) == 4 → 45 was keyed 40.
        for n, ten in [(45, 50), (55, 60), (65, 70), (85, 90), (95, 100), (44, 40), (995, 1000)]:
            self.assertEqual(_round_to(n, 10), ten, n)
        self.assertEqual(_round_to(250, 100), 300)
        for n, lead in [(250, 300), (2500, 3000), (15, 20), (25, 30), (1499, 1000)]:
            self.assertEqual(_round_lead(n), lead, n)

    def test_round_ten_key_matches_school_rule(self):
        for level, q in _samples('round-ten'):
            n = _ints(q['prompt_fr'])[0]
            self.assertLess(n, 1000)
            self.assertEqual(_correct(q)['label'], str((n + 5) // 10 * 10), q['prompt_fr'])


class Grade3RangeTests(SimpleTestCase):
    def test_grade3_numbers_stay_below_1000(self):
        for slug in ('number-sequence', 'missing-addend', 'missing-subtrahend', 'word-problem', 'g3-estimate-sum'):
            for level, q in _samples(slug):
                values = _ints(q['prompt_fr']) + [int(a) for a in q['correct_answers'] if a.isdigit()]
                self.assertLess(max(values), 1000, (slug, q['prompt_fr']))

    def test_missing_terms_are_not_degenerate(self):
        for level, q in _samples('missing-subtrahend'):
            a, c = _ints(q['prompt_fr'])
            self.assertGreaterEqual(c, 1)
            self.assertGreaterEqual(a - c, 1)

    def test_estimate_sum_is_a_sum(self):
        for level, q in _samples('g3-estimate-sum'):
            self.assertNotIn('−', q['prompt_fr'])


class WordProblemTests(SimpleTestCase):
    def test_count_groups_explanation_has_no_false_equality(self):
        # "4 × 6 = 24 + 4 = 28" claims 24 = 28.
        for level, q in _samples('count-groups'):
            for line in q['explanation_fr'].split('\n') + q['explanation_en'].split('\n'):
                sides = [re.findall(r'\d[\d ×+]*', s)[-1] for s in line.replace('*', '').split('=')]
                self.assertEqual(len({_expr_value(s) for s in sides}), 1, line)

    def test_choose_operation_division_shares_exactly(self):
        for level, q in _samples('choose-operation'):
            m = re.search(r'(\d+) ÷ (\d+) = (\d+)', q['explanation_fr'])
            if m:
                total, groups, each = map(int, m.groups())
                self.assertEqual(total, groups * each)
            self.assertTrue(all(c.get('label_en') for c in q['choices']))

    def test_multiply_context_has_one_right_operation(self):
        for level, q in _samples('multiply-context'):
            key = _correct(q)['label']
            self.assertNotEqual(key, '2 × 2')          # 2 + 2 would be right too
            for c in q['choices']:
                if not c['correct']:
                    self.assertNotEqual(_expr_value(c['label']), _expr_value(key), c['label'])
                    self.assertGreaterEqual(_expr_value(c['label']), 0, c['label'])
            self.assertEqual(len(set(q['correct_answers'])), len(q['correct_answers']))

    def test_fraction_collection_choices_are_distinct_fractions(self):
        for level, q in _samples('fraction-collection'):
            labels = [c['label'] for c in q['choices']]
            self.assertTrue(all('/' in label for label in labels), labels)     # never a raw "44"
            self.assertEqual(len({Fraction(label) for label in labels}), len(labels), labels)

    def test_number_classify_has_exactly_one_true_choice(self):
        for level, q in _samples('number-classify'):
            n = _ints(q['prompt_fr'])[0]
            even = n % 2 == 0
            prime = all(n % k for k in range(2, int(n ** 0.5) + 1))
            for c in q['choices']:
                label = c['label_fr']
                true = ((label.startswith('Pair') and even) or (label.startswith('Impair') and not even)) \
                    and label.endswith('et premier') == prime
                self.assertEqual(true, c['correct'], (n, label))

    def test_repeated_addition_products_are_distinct(self):
        for level, q in _samples('repeated-addition'):
            products = [_expr_value(p['right']) for p in q['pairs']]
            self.assertEqual(len(set(products)), len(products), q['pairs'])

    def test_fact_family_never_shows_the_hidden_fact(self):
        for level, q in _samples('fact-family'):
            asked = re.search(r'\*\*(.+) = ___\*\*', q['prompt_fr']).group(1)
            self.assertFalse(any(b.startswith(asked + ' =') for b in q['bullets']), (asked, q['bullets']))
            self.assertEqual(len(set(q['bullets'])), len(q['bullets']))

    def test_money_choices_are_localized(self):
        for level, q in _samples('money-change'):
            for c in q['choices']:
                self.assertTrue(c['label_en'].startswith('$'), c)
        for level, q in _samples('money-match'):
            for p in q['pairs']:
                self.assertNotIn(',', p['left_en'])
                self.assertNotIn(' $', p['right_en'])


class Grade4To6Tests(SimpleTestCase):
    def test_expression_for_story_choices_differ_and_stay_positive(self):
        for level, q in _samples('g5-expression-for-story'):
            values = []
            for c in q['choices']:
                for inner in re.findall(r'\(([^()]*)\)', c['label']):
                    self.assertGreaterEqual(_expr_value(inner), 0, c['label'])
                values.append(_expr_value(c['label']))
            self.assertTrue(all(v >= 0 for v in values))
            self.assertEqual(len(set(values)), len(values), [c['label'] for c in q['choices']])

    def test_best_estimate_is_the_closest_choice(self):
        for slug in ('g6-estimate-product', 'g6-rate-problem'):
            for level, q in _samples(slug):
                if q['q_type'] != 'multiple_choice':
                    continue
                exact = _num(re.search(r'exact ?: ([\d  ]+)', q['explanation_en']).group(1).strip())
                key = _num(_correct(q)['label'])
                for c in q['choices']:
                    if not c['correct']:
                        self.assertGreater(abs(_num(c['label']) - exact), abs(key - exact), (slug, q['prompt_en']))

    def test_powers_notation_choices_have_distinct_values(self):
        sup = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')

        def value(label):
            m = re.fullmatch(r'(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', label)
            return int(m.group(1)) ** int(m.group(2).translate(sup)) if m else _expr_value(label)
        for level, q in _samples('g6-powers'):
            if q['q_type'] == 'multiple_choice':
                self.assertEqual(len({value(c['label']) for c in q['choices']}), 5)

    def test_number_pattern_rules_are_exclusive(self):
        for level, q in _samples('g5-number-patterns', ('easy', 'medium')):
            labels = [c.get('label_en', c['label']) for c in q.get('choices', [])]
            self.assertFalse(any('then 3, then 4' in l for l in labels) and any('grows by 1' in l for l in labels), labels)

    def test_division_remainder_divisor_has_one_digit(self):
        for level, q in _samples('g4-division-remainder'):
            m = re.search(r'÷ (\d+)\*\*', q['prompt_fr']) or re.search(r'de \*\*(\d+)\*\*', q['prompt_fr'])
            self.assertLessEqual(int(m.group(1)), 9, q['prompt_fr'])

    def test_comparative_unneeded_fact_does_not_contradict(self):
        for level, q in _samples('g6-comparative-phrase', ('hard',)):
            if 'vitesse' in q['prompt_fr']:
                self.assertNotIn('court à', q['prompt_fr'])

    def test_decimal_answers_in_english_use_a_point(self):
        for slug in ('g5-decimal-div', 'g5-div-decimal', 'g5-decimal-mult'):
            for level, q in _samples(slug):
                for key in ('prompt_en', 'explanation_en', 'hint_en'):
                    self.assertIsNone(re.search(r'\d,\d', q[key]), (slug, q[key]))
                self.assertTrue(check_answer(q['correct_answers'][0], q['correct_answers'], 'decimal'))
                if slug != 'g5-decimal-mult':
                    self.assertNotIn('.', q['correct_answers'][0])        # key is fr: '8,75'
                    self.assertIn(',', q['correct_answers'][0])           # a true decimal, never '26,000'
                    self.assertFalse(q['correct_answers'][0].endswith('0'))
