"""
Clock-reasoning skills (grades 3 → 6): every problem draws a clock for the
current time and the answer follows from reading it, then adding / subtracting.
"""
import re

from django.test import SimpleTestCase, TestCase

from .answers import check_answer, parse_duration
from .generators import GENERATORS, SKILL_MAP, TOPIC_GROUPS
from .generators import clock
from .geometry_utils import render_shapes
from .views import _check_practice

CLOCK_SLUGS = ['g3-clock-later', 'g4-clock-back', 'g5-clock-schedule', 'g6-clock-planning']
LEVELS = ('easy', 'medium', 'hard')
RUNS = 60
TIME_RE = re.compile(r'^(\d{1,2}) h (\d{2})$')


class ClockGeneratorTests(SimpleTestCase):
    def test_registered_everywhere(self):
        grouped = {t['slug']: g['grade'] for g in TOPIC_GROUPS for t in g['topics']}
        for slug, grade in zip(CLOCK_SLUGS, (3, 4, 5, 6)):
            self.assertIn(slug, GENERATORS)
            self.assertIn(slug, SKILL_MAP)
            self.assertEqual(grouped[slug], grade)

    def test_every_problem_has_a_clock_and_a_checkable_answer(self):
        for slug in CLOCK_SLUGS:
            gen = GENERATORS[slug]
            for level in LEVELS:
                for _ in range(RUNS):
                    q = gen(level)
                    self.assertTrue(q['show_illustration'])
                    self.assertEqual(q['shape_data'][0]['type'], 'clock', slug)
                    self.assertTrue(1 <= q['shape_data'][0]['hours'] <= 12)
                    self.assertTrue(0 <= q['shape_data'][0]['minutes'] <= 59)
                    render_shapes(q['shape_data'])
                    for k in ('prompt_fr', 'prompt_en', 'explanation_fr', 'explanation_en', 'hint_fr', 'hint_en'):
                        self.assertTrue(q[k], f'{slug}/{level}: {k} empty')
                    if q['q_type'] == 'multiple_choice':
                        labels = [c['label'] for c in q['choices']]
                        self.assertEqual(len(labels), len(set(labels)), f'{slug}/{level}: duplicate choices {labels}')
                        self.assertEqual(sum(1 for c in q['choices'] if c['correct']), 1)
                        self.assertTrue(all(TIME_RE.match(l) for l in labels), labels)
                    else:
                        self.assertEqual(q['answer_type'], 'duration')
                        for a in q['correct_answers']:
                            self.assertTrue(check_answer(a, q['correct_answers'], 'duration'), f'{slug}/{level}: {a!r}')
                        self.assertTrue(_check_practice(q, q['correct_answers'][0]))
                    # no negative or past-midnight times anywhere
                    for a in q['correct_answers']:
                        self.assertFalse(str(a).startswith('-'))
                        m = TIME_RE.match(str(a))
                        if m:
                            self.assertLess(int(m.group(1)), 24, f'{slug}/{level}: {a}')

    def test_grade3_stays_on_the_12h_face(self):
        for level in LEVELS:
            for _ in range(RUNS):
                q = clock.g3_clock_later_gen(level)
                h = int(TIME_RE.match(q['correct_answers'][0]).group(1))
                self.assertTrue(1 <= h <= 12)

    def test_grade5_two_step_answer_is_consistent(self):
        """Started N ago, lasts D: end = now − N + D; the explanation carries the same numbers."""
        for _ in range(RUNS):
            q = clock.g5_clock_schedule_gen('hard')
            now_h, now_m = q['shape_data'][0]['hours'], q['shape_data'][0]['minutes']
            ago = parse_duration(re.search(r'il y a \*\*(.+?)\*\*', q['prompt_fr']).group(1))
            dur = parse_duration(re.search(r'durer \*\*(.+?)\*\*', q['prompt_fr']).group(1))
            self.assertGreater(dur, ago)
            answer = parse_duration(q['correct_answers'][0])
            if 'terminera' in q['prompt_fr']:
                # end time, on a 24-h clock: now (12-h face, PM or AM) − ago + dur
                now_candidates = {(now_h % 12) * 60 + now_m, (now_h % 12 + 12) * 60 + now_m}
                self.assertIn(answer, {n - ago + dur for n in now_candidates})
            else:
                self.assertEqual(answer, dur - ago)

    def test_grade6_hard_uses_24h_and_multi_step(self):
        seen = set()
        for _ in range(RUNS):
            q = clock.g6_clock_planning_gen('hard')
            seen.add('pause' in q['prompt_fr'])
            seen.add('partir' in q['prompt_fr'])
            self.assertIn("l'après-midi", q['prompt_fr'])
            self.assertGreaterEqual(q['explanation_fr'].count('Étape'), 3)
        self.assertIn(True, seen)

    def test_typed_forms_all_accepted(self):
        answers = clock._answers_for_time(16 * 60 + 45)
        for typed in ('16 h 45', '16:45', '16h45', '4 h 45', '4:45'):
            self.assertTrue(check_answer(typed, answers, 'duration'), typed)
        self.assertFalse(check_answer('16 h 50', answers, 'duration'))


class ClockPracticePageTests(TestCase):
    def test_pages_render_for_a_student(self):
        from django.contrib.auth.models import User
        from .models import Student
        u = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=u, grade=5)
        self.client.login(username='kid', password='abcd')
        for slug in CLOCK_SLUGS:
            r = self.client.get(f'/practice/{slug}/?lang=fr')
            self.assertEqual(r.status_code, 200, slug)
            r = self.client.get(f'/practice/{slug}/next/?level=hard')
            self.assertEqual(r.status_code, 200, slug)
            self.assertIn(b'<svg', r.content)
