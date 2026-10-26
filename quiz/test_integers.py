"""WP9 — grade 6 integers (decision D2, 2026-10-26: negative numbers only where they occur naturally)."""
import re

from django.test import SimpleTestCase, TestCase

from .answers import check_answer, input_spec, parse_number, infer_answer_type
from .generators import GENERATORS, SKILL_MAP, TOPIC_GROUPS
from .generators import integers_plus as ip
from .generators.resolution import RESOLUTION
from .generators.resolution_plus import SIGNED_SKILLS
from .models import Skill
from .test_language import FRENCH_WORDS

LEVELS = ('easy', 'medium', 'hard')


def num(label):
    return parse_number(label.replace('°C', ''))


class IntegerGeneratorTests(SimpleTestCase):
    def test_wired_and_grade_6(self):
        group = next(g for g in TOPIC_GROUPS if g['name_en'] == 'Grade 6 — Integers')
        self.assertEqual(group['grade'], 6)
        self.assertEqual({t['slug'] for t in group['topics']}, SIGNED_SKILLS)
        for slug in SIGNED_SKILLS:
            self.assertIn(slug, GENERATORS)
            self.assertIn(slug, SKILL_MAP)

    def test_structure_and_answers(self):
        for slug in SIGNED_SKILLS:
            for level in LEVELS:
                for _ in range(150):
                    q = GENERATORS[slug](level)
                    for k in ('prompt_fr', 'prompt_en', 'hint_fr', 'hint_en', 'explanation_fr', 'explanation_en'):
                        self.assertTrue(q.get(k), f'{slug}/{level}: {k}')
                    self.assertIsNone(FRENCH_WORDS.search(q['prompt_en']), q['prompt_en'])
                    self.assertNotIn('√', q['prompt_fr'] + q['prompt_en'])
                    self.assertIsNone(re.search(r'(?<![\w(])-\d', q['prompt_fr'] + q['prompt_en']),
                                      f'{slug}: hyphen used as a minus sign in {q["prompt_fr"]!r}')
                    if q['q_type'] == 'text_input':
                        for a in q['correct_answers']:
                            self.assertTrue(check_answer(a, q['correct_answers'], q['answer_type']), (slug, a))
                    if q['q_type'] == 'multiple_choice':
                        self.assertEqual(sum(c['correct'] for c in q['choices']), 1)
                        self.assertEqual(len({c['label'] for c in q['choices']}), 5)

    def test_thermometer_reading_matches_picture(self):
        for level in ('easy', 'medium'):
            for _ in range(100):
                q = ip.g6_integer_thermometer_gen(level)
                t = q['shape_data'][0]['temp']
                self.assertEqual(num(q['correct_answers'][0]), t)
                self.assertTrue(-20 <= t <= 20)

    def test_temperature_changes(self):
        for _ in range(300):
            q = ip.g6_integer_thermometer_gen('hard')
            got = num(q['correct_answers'][0])
            vals = [int(v.replace('−', '-')) for v in re.findall(r'−?\d+(?= °C| degrés)', q['prompt_fr'])]
            if 'monte' in q['prompt_fr']:
                self.assertEqual(got, vals[0] + vals[1])
                self.assertLess(vals[0], 0)
            elif 'baisse' in q['prompt_fr']:
                self.assertEqual(got, vals[0] - vals[1])
                self.assertLess(got, 0)
            else:
                self.assertEqual(got, vals[1] - vals[0])

    def test_number_line_point_is_the_answer(self):
        for level in ('easy', 'medium'):
            for _ in range(100):
                q = ip.g6_integer_number_line_gen(level)
                self.assertLess(num(q['correct_answers'][0]), 0)

    def test_compare_symbol_is_right(self):
        for level in LEVELS:
            for _ in range(200):
                q = ip.g6_integer_compare_gen(level)
                a, b = [int(v.replace('−', '-')) for v in re.findall(r'(−?\d+)(?: °C| m)? ___ (−?\d+)', q['prompt_fr'])[-1]]
                self.assertEqual(q['correct_answers'][0], '<' if a < b else '>')

    def test_order_is_sorted(self):
        for level in LEVELS:
            for _ in range(200):
                q = ip.g6_integer_order_gen(level)
                vals = [num(it['label']) for it in sorted(q['items'], key=lambda i: i['order'])]
                self.assertEqual(len(set(vals)), len(vals))
                self.assertTrue(vals == sorted(vals) or vals == sorted(vals, reverse=True))
                self.assertTrue(any(v < 0 for v in vals))

    def test_cartesian_quadrants(self):
        for _ in range(200):
            q = ip.g6_cartesian_4q_gen('medium')
            x, y = [int(v.replace('−', '-')) for v in re.search(r'\((−?\d+), (−?\d+)\)', q['prompt_fr']).groups()]
            want = {(1, 1): 'I', (-1, 1): 'II', (-1, -1): 'III', (1, -1): 'IV'}[(1 if x > 0 else -1, 1 if y > 0 else -1)]
            self.assertEqual(q['correct_answers'][0], f'Quadrant {want}')

    def test_resolution_stories(self):
        for slug in ('g6-integer-thermometer', 'g6-integer-number-line', 'g6-integer-compare'):
            for _ in range(200):
                q = RESOLUTION[slug]()
                for a in q['correct_answers']:
                    self.assertTrue(check_answer(a, q['correct_answers'], q['answer_type']))

    def test_signed_answers_and_keyboard(self):
        self.assertEqual(parse_number('− 4'), -4)
        self.assertEqual(parse_number('-12 °C'), -12)
        self.assertTrue(check_answer('-7', ['−7'], 'signed'))
        self.assertFalse(check_answer('7', ['−7'], 'signed'))
        self.assertEqual(infer_answer_type(['−3']), 'signed')
        self.assertTrue(input_spec('signed', 'fr')['signed'])
        self.assertEqual(input_spec('signed')['inputmode'], 'numeric')


class IntegerPageTests(TestCase):
    def test_practice_page_shows_sign_key(self):
        from django.contrib.auth.models import User
        from .models import Student
        user = User.objects.create_user('kid6', password='abcd')
        Student.objects.create(user=user, grade=6)
        self.client.login(username='kid6', password='abcd')
        self.assertTrue(Skill.objects.filter(slug='g6-integer-thermometer').exists())
        for _ in range(15):
            r = self.client.get('/practice/g6-integer-number-line/next/?lang=fr&level=easy')
            self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Changer le signe')
