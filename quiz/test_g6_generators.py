"""
Smoke + correctness tests for the Grade-6 generators (same checks as grade 4).
"""
import re

from django.test import SimpleTestCase

from .answers import check_answer
from .generators import GENERATORS, SKILL_MAP, TOPIC_GROUPS
from .test_g4_generators import Grade4GeneratorTests

G6_SLUGS = [s for s in GENERATORS if s.startswith('g6-')]
LEVELS = ('easy', 'medium', 'hard')
RUNS = 40


class Grade6RegistryTests(SimpleTestCase):
    def test_every_skill_is_wired(self):
        group_slugs = {t['slug'] for g in TOPIC_GROUPS if g.get('grade') == 6 for t in g['topics']}
        self.assertEqual(set(G6_SLUGS), group_slugs)
        for slug in G6_SLUGS:
            self.assertIn(slug, SKILL_MAP, slug)
            for key in ('prereq', 'next', 'mastery_next', 'downgrade'):
                target = SKILL_MAP[slug][key]
                if target:
                    self.assertIn(target, GENERATORS, f'{slug}.{key} → {target}')

    def test_grade6_has_five_domains(self):
        self.assertEqual(sum(1 for g in TOPIC_GROUPS if g.get('grade') == 6), 5)


class Grade6GeneratorTests(SimpleTestCase):
    _check = Grade4GeneratorTests._check

    def test_all_generators_all_levels(self):
        for slug in G6_SLUGS:
            gen = GENERATORS[slug]
            for level in LEVELS:
                for _ in range(RUNS):
                    self._check(slug, gen(level))

    def test_multiply_is_exact(self):
        for level in LEVELS:
            for _ in range(30):
                q = GENERATORS['g6-multiply'](level)
                a, b = re.search(r'\*\*([\d ]+) × (\d+)\*\*', q['prompt_fr']).groups()
                self.assertEqual(int(q['correct_answers'][0]), int(a.replace(' ', '')) * int(b))

    def test_symbol_form_regroups(self):
        q = GENERATORS['g6-symbol-form']('medium')
        expr = re.search(r'\*\*(.+?)\*\*', q['prompt_fr']).group(1)
        val = {'u': 1, 'd': 10, 'c': 100, 'UM': 1_000, 'DM': 10_000, 'CM': 100_000}
        total = sum(int(k) * val[sym] for k, sym in re.findall(r'(\d+) (u|d|c|UM|DM|CM)', expr))
        self.assertEqual(int(q['correct_answers'][0]), total)

    def test_compare_matches_numbers(self):
        for _ in range(50):
            q = GENERATORS['g6-compare']('medium')
            a, b = [int(x.replace(' ', '')) for x in re.findall(r'\*\*([\d ]+)\*\*', q['prompt_fr'])]
            self.assertEqual(q['correct_answers'], ['<' if a < b else '>' if a > b else '='])

    def test_money_total_accepts_plain_number(self):
        q = GENERATORS['g6-money-compare']('easy')
        self.assertTrue(check_answer(q['correct_answers'][1], q['correct_answers'], 'money'))
        self.assertTrue(check_answer(q['correct_answers'][1] + ' $', q['correct_answers'], 'money'))

    def test_scenarios_vary(self):
        prompts = {GENERATORS['g6-rate-problem']('hard')['prompt_fr'] for _ in range(30)}
        self.assertGreater(len(prompts), 15)
