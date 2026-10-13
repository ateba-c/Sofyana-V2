"""
Tests for the curriculum-upgrade skills (quiz/generators/registry_plus.py).

Every skill: wired everywhere, has audit refs, and 40 problems × 3 levels pass the
shared structural check. Below that, one correctness test per skill whose answer
can be recomputed from the prompt.
"""
import re
from fractions import Fraction

from django.test import SimpleTestCase

from .answers import check_answer
from .curriculum import CURRICULUM_REFS
from .generators import GENERATORS, SKILL_MAP, TOPIC_GROUPS
from .generators.registry_plus import PLUS_GENERATORS
from .test_g4_generators import Grade4GeneratorTests

PLUS = list(PLUS_GENERATORS)
LEVELS = ('easy', 'medium', 'hard')
RUNS = 40


def _q(slug, level='medium'):
    return GENERATORS[slug](level)


class PlusRegistryTests(SimpleTestCase):
    def test_wired_everywhere(self):
        in_groups = {t['slug'] for g in TOPIC_GROUPS for t in g['topics']}
        for slug in PLUS:
            self.assertIs(GENERATORS[slug], PLUS_GENERATORS[slug], slug)
            self.assertIn(slug, in_groups, slug)
            self.assertIn(slug, SKILL_MAP, slug)
            for key in ('prereq', 'next', 'mastery_next', 'downgrade'):
                target = SKILL_MAP[slug][key]
                if target:
                    self.assertIn(target, GENERATORS, f'{slug}.{key} → {target}')

    def test_curriculum_refs(self):
        for slug in PLUS:
            self.assertTrue(CURRICULUM_REFS.get(slug), f'{slug} has no QC refs in quiz/curriculum.py')

    def test_slugs_carry_their_grade(self):
        grade_of = {t['slug']: g.get('grade') for g in TOPIC_GROUPS for t in g['topics']}
        for slug in PLUS:
            m = re.match(r'g(\d)-', slug)
            if m:
                self.assertEqual(grade_of[slug], int(m.group(1)), slug)


class PlusGeneratorTests(SimpleTestCase):
    _check = Grade4GeneratorTests._check

    def test_all_generators_all_levels(self):
        for slug in PLUS:
            for level in LEVELS:
                for _ in range(RUNS):
                    q = GENERATORS[slug](level)
                    self._check(slug, q)
                    for c in q.get('choices') or []:
                        self.assertNotRegex(str(c['label']), r'^\d{2,}$' if '/' in q['correct_answers'][0] else r'^$',
                                            f'{slug}: padded with a bare number {c}')


def _frac_in(text):
    return [Fraction(int(a), int(b)) for a, b in re.findall(r'(\d+)/(\d+)', text)]


class FractionsPlusTests(SimpleTestCase):
    def test_fraction_shape_never_prints_the_answer(self):
        for level in LEVELS:
            for _ in range(60):
                q = _q('fraction-shape', level)
                texts = [l['text'] for s in q['shape_data'] for l in s.get('labels', [])]
                self.assertNotIn(q['correct_answers'][0], texts)
                n, d = map(int, q['correct_answers'][0].split('/'))
                self.assertTrue(0 < n < d)

    def test_benchmark_is_right(self):
        names = ['plus petite que ½', 'égale à ½', 'entre ½ et 1', 'égale à 1', 'plus grande que 1']
        for level in LEVELS:
            for _ in range(60):
                q = _q('g4-fraction-benchmark', level)
                f = _frac_in(q['prompt_fr'])[0]
                want = 0 if f < Fraction(1, 2) else 1 if f == Fraction(1, 2) else 2 if f < 1 else 3 if f == 1 else 4
                self.assertEqual(q['correct_answers'][0], names[want])

    def test_equivalent_missing_term(self):
        for _ in range(80):
            q = _q('g4-equivalent-fractions', 'medium')
            if q['q_type'] != 'text_input':
                continue
            m = re.search(r'(\d+)/(\d+) = (\?|\d+)/(\?|\d+)', q['prompt_fr'])
            a, b, c, d = m.groups()
            ans = int(q['correct_answers'][0])
            c, d = (ans, int(d)) if c == '?' else (int(c), ans)
            self.assertEqual(Fraction(int(a), int(b)), Fraction(c, d))

    def test_not_equivalent_is_the_odd_one(self):
        for _ in range(40):
            q = GENERATORS['g4-equivalent-fractions']('hard')
            if 'pas' not in q['prompt_fr']:
                continue
            target = _frac_in(q['prompt_fr'])[0]
            for c in q['choices']:
                self.assertEqual(Fraction(c['label']) != target, c['correct'], c)

    def test_orderings_are_sorted(self):
        for slug in ('g5-order-same-numerator', 'g6-order-related-denominators'):
            for level in LEVELS:
                for _ in range(30):
                    q = _q(slug, level)
                    vals = [Fraction(it['label']) for it in sorted(q['items'], key=lambda i: i['order'])]
                    desc = 'décroissant' in q['prompt_fr']
                    self.assertEqual(vals, sorted(vals, reverse=desc), slug)
                    self.assertEqual(len(set(vals)), len(vals))

    def test_related_denominators_really_related(self):
        for _ in range(40):
            q = _q('g6-order-related-denominators', 'hard')
            dens = [Fraction(it['label']).denominator * 0 + int(it['label'].split('/')[1]) for it in q['items']]
            big = max(dens)
            self.assertTrue(all(big % d == 0 for d in dens), dens)

    def test_simplify_answer_is_irreducible_and_equal(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-simplify-fraction', level)
                ans = q['correct_answers'][0]
                n, d = map(int, ans.split('/'))
                self.assertEqual(Fraction(n, d).denominator, d)
                if 'Réduis' in q['prompt_fr']:
                    self.assertEqual(_frac_in(q['prompt_fr'])[0], Fraction(n, d))

    def test_add_related_value(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-fraction-add-related', level)
                a, b = _frac_in(q['prompt_fr'])[:2]
                want = a - b if '−' in q['prompt_fr'] else a + b
                self.assertGreater(want, 0)
                self.assertTrue(check_answer(str(want), q['correct_answers'], 'fraction'), q['prompt_fr'])

    def test_whole_times_fraction_value(self):
        for _ in range(60):
            q = _q('g6-whole-times-fraction', 'medium')
            if '×' in q['prompt_fr']:
                w = int(re.search(r'\*\*(\d+) ×', q['prompt_fr']).group(1))
                f = _frac_in(q['prompt_fr'])[0]
                self.assertEqual(Fraction(q['correct_answers'][0]), w * f)
            else:
                f = _frac_in(q['prompt_fr'])[0]
                total = int(re.search(r'de (\d+)\*\*', q['prompt_fr']).group(1))
                self.assertEqual(int(q['correct_answers'][0]), f * total)

    def test_fraction_words_typed_answer(self):
        for _ in range(40):
            q = _q('g3-fraction-words', 'hard')
            if q['q_type'] == 'text_input':
                self.assertTrue(check_answer(q['correct_answers'][0], q['correct_answers'], 'fraction'))


def _dec_in(text):
    return [Fraction(x.replace(',', '.')) for x in re.findall(r'\*\*(\d+(?:,\d+)?)', text)]


class DecimalsPlusTests(SimpleTestCase):
    def test_round_and_truncate(self):
        from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
        places = {"à l'unité près": 0, 'au dixième près': 1, 'au centième près': 2}
        for level in LEVELS:
            for _ in range(60):
                q = _q('g4-round-decimal', level)
                x = Decimal(re.search(r'\*\*([\d,]+)\*\*', q['prompt_fr']).group(1).replace(',', '.'))
                to = next(v for k, v in places.items() if k in q['prompt_fr'])
                mode = ROUND_DOWN if q['prompt_fr'].startswith('Tronque') else ROUND_HALF_UP
                want = x.quantize(Decimal(1).scaleb(-to), rounding=mode)
                self.assertTrue(check_answer(str(want), q['correct_answers'], 'decimal'), (q['prompt_fr'], q['correct_answers']))

    def test_power_of_ten(self):
        for level in LEVELS:
            for _ in range(60):
                q = _q('g5-times-power-of-ten', level)
                m = re.search(r'\*\*([\d,]+) (×|÷) (\d+)\*\*', q['prompt_fr'])
                x, op, f = Fraction(m.group(1).replace(',', '.')), m.group(2), int(m.group(3))
                want = x * f if op == '×' else x / f
                self.assertEqual(Fraction(q['correct_answers'][1]), want)

    def test_percent_values(self):
        for level in LEVELS:
            for _ in range(60):
                q = _q('g6-percent', level)
                p = q['prompt_fr']
                if 'de ' in p and p.startswith('Combien font'):
                    pct, base = map(int, re.search(r'\*\*(\d+) % de (\d+)\*\*', p).groups())
                    self.assertEqual(int(q['correct_answers'][0]), pct * base // 100)
                elif p.startswith('Écris **') and 'pourcentage' in p:
                    val = _frac_in(p)[0] if '/' in p else _dec_in(p)[0]
                    self.assertTrue(check_answer(str(val * 100), q['correct_answers'], 'integer'), p)

    def test_decimal_grid_counts_squares(self):
        for _ in range(60):
            q = _q('g4-decimal-grid', 'medium')
            if not q['shape_data']:
                continue
            filled = sum(1 for m in q['shape_data'][0]['marks'] if m['type'] == 'rect' and m['fill'] not in ('#FFFFFF', 'none'))
            cells = sum(1 for m in q['shape_data'][0]['marks'] if m['type'] == 'rect' and m['fill'] != 'none')
            self.assertEqual(Fraction(q['correct_answers'][1]), Fraction(filled, cells))

    def test_story_answers_accept_both_notations(self):
        for _ in range(60):
            q = _q('g5-decimal-story', 'hard')
            for a in q['correct_answers']:
                self.assertTrue(check_answer(a.replace(',', '.'), q['correct_answers'], q['answer_type']))

    def test_percent_sign_is_accepted(self):
        self.assertTrue(check_answer('25 %', ['25 %', '25'], 'integer'))
        self.assertTrue(check_answer('25%', ['25'], 'integer'))
        self.assertIsNone(__import__('quiz.answers', fromlist=['parse_duration']).parse_duration('25 %'))


class PrimaryLimitsTests(SimpleTestCase):
    def test_decimals_stop_at_thousandths(self):
        dec = re.compile(r'\d[.,](\d+)')
        for slug in PLUS:
            for level in LEVELS:
                for _ in range(25):
                    for a in GENERATORS[slug](level).get('correct_answers') or []:
                        for m in dec.finditer(str(a)):
                            self.assertLessEqual(len(m.group(1)), 3, f'{slug}/{level}: {a}')


def _eval(expr):
    return eval(expr.replace('×', '*').replace('÷', '//').replace('−', '-'), {'__builtins__': {}})


class OperationsPlusTests(SimpleTestCase):
    def test_exactly_one_true_equality(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g3-equality-true', level)
                for c in q['choices']:
                    left, right = c['label'].split(' = ')
                    self.assertEqual(_eval(left) == _eval(right), c['correct'], c['label'])

    def test_equivalent_expression_choices(self):
        for _ in range(60):
            q = _q('g4-equivalent-expressions', 'medium')
            a, b = map(int, re.findall(r'\*\*(\d+) \+ (\d+)', q['prompt_fr'])[0])
            if q['q_type'] == 'text_input':
                r = int(re.search(r'= (\d+) \+ \?', q['prompt_fr']).group(1))
                self.assertEqual(r + int(q['correct_answers'][0]), a + b)
            else:
                for c in q['choices']:
                    self.assertEqual(_eval(c['label']) == a + b, c['correct'], c['label'])

    def test_missing_factor(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g4-missing-factor', level)
                expr = re.search(r'\*\*(.+)\*\*', q['prompt_fr']).group(1).replace('?', q['correct_answers'][0])
                left, right = expr.split(' = ')
                self.assertEqual(_eval(left), int(right), expr)

    def test_division_remainder(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g4-division-remainder', level)
                m = re.search(r'\*\*([\d ]+) ÷ (\d+)\*\*', q['prompt_fr'])
                if not m:
                    continue
                n, d = int(m.group(1).replace(' ', '')), int(m.group(2))
                want = n // d if 'quotient' in q['prompt_fr'] else n % d
                self.assertEqual(int(q['correct_answers'][0]), want)

    def test_expression_for_story_single_right_value(self):
        for level in LEVELS:
            for _ in range(30):
                q = _q('g5-expression-for-story', level)
                right = next(c for c in q['choices'] if c['correct'])['label']
                for c in q['choices']:
                    if not c['correct']:
                        self.assertNotEqual(c['label'], right)

    def test_divisibility_single_answer(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-divisibility', level)
                k = int(re.search(r'par (\d+)', q['prompt_fr']).group(1))
                for c in q['choices']:
                    self.assertEqual(int(c['label']) % k == 0, c['correct'], (k, c['label']))

    def test_prime_factorisation(self):
        from math import prod
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-prime-factors', level)
                n = int(re.search(r'\*\*(\d+)\*\*', q['prompt_fr']).group(1))
                if q['q_type'] == 'multiple_choice':
                    fs = [int(x) for x in q['correct_answers'][0].split(' × ')]
                    self.assertEqual(prod(fs), n)
                    self.assertTrue(all(all(f % k for k in range(2, f)) for f in fs))

    def test_powers_values(self):
        sup = {'²': 2, '³': 3, '⁴': 4, '⁵': 5}
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-powers', level)
                m = re.match(r'Calcule : \*\*(\d+)([²³⁴⁵])\*\*', q['prompt_fr'])
                if m:
                    self.assertEqual(int(q['correct_answers'][0]), int(m.group(1)) ** sup[m.group(2)])

    def test_times_tables_within_10(self):
        for level in LEVELS:
            for _ in range(60):
                q = _q('g4-times-tables', level)
                nums = list(map(int, re.findall(r'\d+', q['prompt_fr'])))
                if '×' in q['prompt_fr']:
                    self.assertTrue(all(x <= 10 for x in nums), nums)
                    self.assertEqual(int(q['correct_answers'][0]), nums[0] * nums[1])

    def test_write_large_number_accepts_grouping(self):
        for _ in range(30):
            q = _q('g6-write-large-number', 'hard')
            n = q['correct_answers'][0]
            self.assertTrue(check_answer(f'{int(n):,}'.replace(',', ' '), q['correct_answers'], 'integer'))
