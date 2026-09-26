"""
Practice session counters and the problem-solving unlock:
- opening a skill page starts a fresh session (streak / done / score at 0)
- the feedback carries the server-side correct count, so the score badge is right
- the 5th correct answer at Hard announces the unlocked Résolution level
- plain division stays integer division; decimal skills never exceed 4 decimals
"""
import re

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase

from .generators import GENERATORS, RESOLUTION
from .models import Student


class PracticeSessionTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=self.u, grade=3)
        self.client.login(username='kid', password='abcd')

    def _answer_correct(self, topic, level):
        self.client.get(f'/practice/{topic}/next/?level={level}')
        q = self.client.session[f'pq_{topic}']
        idx = next(i for i, c in enumerate(q['choices']) if c['correct'])
        return self.client.post(f'/practice/{topic}/check/?lang=en', {'level': level, 'answer': str(idx)})

    def test_counters_reset_on_page_open_and_score_is_server_side(self):
        for _ in range(3):
            r = self._answer_correct('divide', 'easy')
        self.assertContains(r, 'data-total="3"')
        self.assertContains(r, 'data-correct-count="3"')
        # reopening the page starts over
        self.client.get('/practice/divide/?lang=en&level=easy')
        self.assertNotIn('ps_divide', self.client.session)
        r = self._answer_correct('divide', 'easy')
        self.assertContains(r, 'data-total="1"')
        self.assertContains(r, 'data-correct-count="1"')

    def test_resolution_unlock_banner_on_fifth_hard_correct(self):
        for i in range(1, 6):
            r = self._answer_correct('divide', 'hard')
            html = r.content.decode()
            self.assertEqual('Well done! You unlocked' in html, i == 5, f'answer #{i}')
        # a 6th correct does not repeat the banner; the page now offers the level
        r = self._answer_correct('divide', 'hard')
        self.assertNotIn('Well done! You unlocked', r.content.decode())
        r = self.client.get('/practice/divide/?lang=en&level=resolution')
        self.assertTrue(r.context['resolution_unlocked'])
        self.assertEqual(r.context['level'], 'resolution')
        r = self.client.get('/practice/divide/next/?level=resolution&lang=en')
        self.assertNotRegex(r.content.decode(), r'What is \d+ ÷ \d+\?')


class DivisionAnswerRulesTests(SimpleTestCase):
    def test_plain_division_is_integer(self):
        for level in ('easy', 'medium', 'hard'):
            for _ in range(60):
                q = GENERATORS['divide'](level)
                for a in q['correct_answers']:
                    self.assertRegex(str(a), r'^\d+$')

    def test_decimal_answers_have_at_most_4_places(self):
        dec = re.compile(r'\d[.,](\d+)')
        cases = [(s, g, ('easy', 'medium', 'hard')) for s, g in GENERATORS.items()]
        cases += [(s, g, ('resolution',)) for s, g in RESOLUTION.items()]
        for slug, gen, levels in cases:
            for level in levels:
                for _ in range(15):
                    q = gen(level)
                    for a in q.get('correct_answers') or []:
                        for m in dec.finditer(str(a)):
                            self.assertLessEqual(len(m.group(1)), 4, f'{slug}/{level}: {a}')
