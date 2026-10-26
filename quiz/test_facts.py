"""B4.16 — per-fact tracking for fact-fluency skills (quiz/facts.py)."""
import random

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase

from . import facts
from .generators import GENERATORS
from .models import ProblemInteraction, Student


def _q(prompt):
    return {'prompt_fr': prompt}


class FactKeyTests(SimpleTestCase):
    def test_same_family_same_key(self):
        self.assertEqual(facts.fact_key(_q('**7 × 8 = ?**')), '7×8')
        self.assertEqual(facts.fact_key(_q('**8 × 7 = ?**')), '7×8')
        self.assertEqual(facts.fact_key(_q('**56 ÷ 7 = ?**')), '7×8')
        self.assertEqual(facts.fact_key(_q('**9 + 6 = ?**')), '6+9')
        self.assertEqual(facts.fact_key(_q('**15 − 6 = ?**')), '6+9')
        self.assertEqual(facts.fact_key(_q('Combien de pommes ?')), '')
        self.assertEqual(facts.label('7×8'), '7 × 8')

    def test_every_fact_skill_question_has_a_key(self):
        for slug in facts.FACT_SKILLS:
            for level in ('easy', 'medium', 'hard'):
                for _ in range(200):
                    self.assertTrue(facts.fact_key(GENERATORS[slug](level)), slug)

    def test_serve_prefers_weak_facts(self):
        random.seed(4)
        gen = GENERATORS['g4-times-tables']
        hits = sum(facts.fact_key(facts.serve(gen, 'hard', ['7×8'])) == '7×8' for _ in range(200))
        self.assertGreater(hits, 60)          # ~50 % targeted + the odd natural hit (1 fact out of ~40)
        self.assertEqual(facts.serve(gen, 'hard', []).get('q_type'), 'text_input')


class WeakFactTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=self.user, grade=4)

    def _answer(self, item, ok):
        ProblemInteraction.objects.create(user=self.user, topic='g4-times-tables', level='hard', is_correct=ok, item=item)

    def test_missed_until_right_twice(self):
        self._answer('6×7', True)
        self._answer('7×8', False)
        self.assertEqual(facts.weak_facts(self.user, 'g4-times-tables'), ['7×8'])
        self._answer('7×8', True)
        self.assertEqual(facts.weak_facts(self.user, 'g4-times-tables'), ['7×8'])
        self._answer('7×8', True)
        self.assertEqual(facts.weak_facts(self.user, 'g4-times-tables'), [])
        self._answer('7×8', False)
        self.assertEqual(facts.weak_facts(self.user, 'g4-times-tables'), ['7×8'])

    def test_practice_flow_records_and_shows_facts(self):
        self.client.login(username='kid', password='abcd')
        self.client.get('/practice/g4-times-tables/next/?lang=fr&level=hard')
        q = self.client.session['pq_g4-times-tables']
        self.assertTrue(q['fact'])
        r = self.client.post('/practice/g4-times-tables/check/', {'answer': '-1', 'level': 'hard', 'lang': 'fr'})
        self.assertEqual(ProblemInteraction.objects.get().item, q['fact'])
        self.assertContains(r, 'Faits à revoir')
        self.assertContains(r, facts.label(q['fact']))
