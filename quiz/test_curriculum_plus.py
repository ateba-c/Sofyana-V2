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
