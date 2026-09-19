"""
Smoke + correctness tests for the Grade-4 generators.

Every generator is run many times at every level and checked for:
- a well-formed problem dict (q_type, bilingual prompts, explanations)
- multiple choice: exactly one correct option, 5 distinct labels
- text input: the declared correct answer passes ``check_answer`` under the
  declared answer_type (so the child can never be marked wrong on a right answer)
- ordering / mix_match: well-formed items / pairs
- SVG shape data renders without raising
Plus unit tests for the Roman-numeral helpers and the scenario bank.
"""
from django.test import SimpleTestCase

from .answers import check_answer
from .generators import GENERATORS, SKILL_MAP, TOPIC_GROUPS
from .generators.g4_numeration import to_roman, from_roman
from .generators import scenarios as sc
from .geometry_utils import render_shapes
from .views import _check_practice

G4_SLUGS = [s for s in GENERATORS if s.startswith('g4-')]
LEVELS = ('easy', 'medium', 'hard')
RUNS = 40


class RomanNumeralTests(SimpleTestCase):
    def test_known_values(self):
        for n, r in [(1, 'I'), (4, 'IV'), (9, 'IX'), (27, 'XXVII'), (40, 'XL'), (90, 'XC'),
                     (400, 'CD'), (555, 'DLV'), (990, 'CMXC'), (2015, 'MMXV'), (3999, 'MMMCMXCIX')]:
            self.assertEqual(to_roman(n), r)
            self.assertEqual(from_roman(r), n)

    def test_roundtrip(self):
        for n in range(1, 4000):
            self.assertEqual(from_roman(to_roman(n)), n)

    def test_typed_roman_answer_is_case_insensitive(self):
        self.assertTrue(check_answer('xxvii', ['XXVII'], 'text'))
        self.assertTrue(check_answer(' MMXV ', ['MMXV'], 'text'))
        self.assertFalse(check_answer('XXVI', ['XXVII'], 'text'))


class ScenarioBankTests(SimpleTestCase):
    def test_pluralisation(self):
        self.assertEqual(sc.qty(1, sc.THINGS['chien'], 'fr'), '1 chien')
        self.assertEqual(sc.qty(3, sc.THINGS['chien'], 'fr'), '3 chiens')
        self.assertEqual(sc.qty(3, sc.THINGS['mouton'], 'en'), '3 sheep')
        self.assertEqual(sc.qty(2, sc.THINGS['cheval'], 'fr'), '2 chevaux')
        self.assertEqual(sc.fmt_n(49526), '49 526')

    def test_scenarios_vary(self):
        prompts = {GENERATORS['g4-grouping-problem']('easy')['prompt_fr'] for _ in range(30)}
        self.assertGreater(len(prompts), 15)


class Grade4RegistryTests(SimpleTestCase):
    def test_every_skill_is_wired(self):
        group_slugs = {t['slug'] for g in TOPIC_GROUPS if g.get('grade') == 4 for t in g['topics']}
        self.assertEqual(set(G4_SLUGS), group_slugs)
        for slug in G4_SLUGS:
            self.assertIn(slug, SKILL_MAP, slug)
            for key in ('prereq', 'next', 'mastery_next', 'downgrade'):
                target = SKILL_MAP[slug][key]
                if target:
                    self.assertIn(target, GENERATORS, f'{slug}.{key} → {target}')

    def test_grade4_has_four_domains(self):
        self.assertEqual(sum(1 for g in TOPIC_GROUPS if g.get('grade') == 4), 4)


class Grade4GeneratorTests(SimpleTestCase):
    def _check(self, slug, q):
        self.assertIn(q['q_type'], ('multiple_choice', 'text_input', 'ordering', 'mix_match'), slug)
        for k in ('prompt_fr', 'prompt_en', 'hint_fr', 'hint_en', 'explanation_fr', 'explanation_en'):
            self.assertTrue(q.get(k), f'{slug}: missing {k}')
        self.assertTrue(q.get('correct_answers'), f'{slug}: no correct_answers')

        if q['q_type'] == 'multiple_choice':
            choices = q['choices']
            self.assertEqual(len(choices), 5, f'{slug}: {choices}')
            self.assertEqual(sum(1 for c in choices if c['correct']), 1, f'{slug}: {choices}')
            self.assertEqual(len({c['label'] for c in choices}), 5, f'{slug}: duplicate labels {choices}')
            idx = next(i for i, c in enumerate(choices) if c['correct'])
            self.assertTrue(_check_practice(q, str(idx)))
            self.assertFalse(_check_practice(q, str((idx + 1) % 5)))

        elif q['q_type'] == 'text_input':
            for ans in q['correct_answers']:
                self.assertTrue(check_answer(ans, q['correct_answers'], q.get('answer_type')),
                                f'{slug}: own answer {ans!r} rejected ({q.get("answer_type")}) — {q["prompt_fr"]}')
            self.assertFalse(check_answer('', q['correct_answers'], q.get('answer_type')))

        elif q['q_type'] == 'ordering':
            labels = [it['label'] for it in q['items']]
            self.assertEqual(len(labels), len(set(labels)), f'{slug}: duplicate items')
            self.assertEqual(sorted(it['order'] for it in q['items']), list(range(1, len(labels) + 1)))

        elif q['q_type'] == 'mix_match':
            lefts = [p['left'] for p in q['pairs']]
            rights = [p['right'] for p in q['pairs']]
            self.assertEqual(len(lefts), len(set(lefts)), f'{slug}: duplicate left {lefts}')
            self.assertEqual(len(rights), len(set(rights)), f'{slug}: duplicate right {rights}')

        if q.get('shape_data'):
            rendered = render_shapes(q['shape_data'])
            self.assertEqual(len(rendered), len(q['shape_data']))

    def test_all_generators_all_levels(self):
        for slug in G4_SLUGS:
            gen = GENERATORS[slug]
            for level in LEVELS:
                for _ in range(RUNS):
                    self._check(slug, gen(level))

    def test_elapsed_time_accepts_both_formats(self):
        q = GENERATORS['g4-elapsed-time']('hard')
        minutes = [a for a in q['correct_answers'] if a.endswith('min') and 'h' not in a][0]
        self.assertTrue(check_answer(minutes, q['correct_answers'], 'duration'))
        self.assertTrue(check_answer(q['correct_answers'][0].replace(' h ', 'h').replace(' min', ''),
                                     q['correct_answers'], 'duration'))

    def test_compare_symbol_matches_numbers(self):
        for _ in range(50):
            q = GENERATORS['g4-compare']('hard')
            import re
            nums = [int(x.replace(' ', '')) for x in re.findall(r'\*\*([\d ]+)\*\*', q['prompt_fr'])]
            a, b = nums
            expected = '<' if a < b else '>' if a > b else '='
            self.assertEqual(q['correct_answers'], [expected])

    def test_count_groups_arithmetic(self):
        import re
        for _ in range(50):
            q = GENERATORS['g4-count-groups']('medium')
            n = int(re.search(r'\*\*([\d ]+)\*\*', q['prompt_fr']).group(1).replace(' ', ''))
            ans = int(q['correct_answers'][0])
            for word, p in (('dizaines', 10), ('centaines', 100), ('unités de mille', 1000), ('dizaines de mille', 10000)):
                if f'**{word}**' in q['prompt_fr']:
                    self.assertEqual(ans, n // p, q['prompt_fr'])
