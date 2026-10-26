"""Interactive answer widgets (quiz/widgets.py): tap-to-place point, tap-to-build bar chart."""
import json
import random

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase

from . import widgets
from .generators import GENERATORS
from .models import Student


def _widget_q(slug, q_type, level='hard'):
    for _ in range(200):
        q = GENERATORS[slug](level)
        if q['q_type'] == q_type:
            return q
    raise AssertionError(f'{slug} never served a {q_type} question')


class WidgetLogicTests(SimpleTestCase):
    def test_place_point(self):
        q = widgets.place_point(('Place (−2, 3)', 'Place (−2, 3)'), (-2, 3), ('h', 'h'), ('e', 'e'),
                                xmin=-4, xmax=4, ymin=-4, ymax=4)
        self.assertTrue(widgets.check(q, '(-2, 3)'))
        self.assertTrue(widgets.check(q, '(−2,3)'))
        self.assertFalse(widgets.check(q, '(3, -2)'))
        lay = widgets.plane_layout(q['plane'])
        self.assertEqual(len(lay['nodes']), 81)
        self.assertIn('−4', [t['text'] for t in lay['xlabels']])
        shape = widgets.feedback_shape(q, '(3, -2)')
        self.assertEqual(shape['type'], 'canvas')

    def test_build_bars(self):
        q = widgets.build_bars(('p', 'p'), [('Chat', 'Cat'), ('Chien', 'Dog')], [4, 7], ('h', 'h'), ('e', 'e'), top=10)
        self.assertTrue(widgets.check(q, '[4, 7]'))
        self.assertFalse(widgets.check(q, '[7, 4]'))
        self.assertFalse(widgets.check(q, 'nonsense'))
        lay = widgets.bars_layout(q['bars'], 'en')
        self.assertEqual([c['label'] for c in lay['cols']], ['Cat', 'Dog'])
        self.assertEqual(len(lay['cols'][0]['cells']), 10)
        self.assertEqual(widgets.feedback_shape(q, '[4, 6]', 'fr')['type'], 'canvas')

    def test_ai_review_compares_widget_answers(self):
        from qastudio.ai_review import compare
        q = widgets.place_point(('p', 'p'), (2, 5), ('h', 'h'), ('e', 'e'))
        self.assertEqual(compare(q, {'answer': '(2, 5)', 'confident': True})['status'], 'match')
        self.assertEqual(compare(q, {'answer': '(5, 2)', 'confident': True})['status'], 'mismatch')


class WidgetPageTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=user, grade=6)
        self.client.login(username='kid', password='abcd')

    def test_place_point_round_trip(self):
        random.seed(1)
        for _ in range(30):
            r = self.client.get('/practice/cartesian-place-point/next/?lang=fr&level=hard')
            q = self.client.session['pq_cartesian-place-point']
            if q['q_type'] == 'place_point':
                break
        self.assertContains(r, 'Touche le croisement')
        self.assertContains(r, '@click="choose(')
        r = self.client.post('/practice/cartesian-place-point/check/', {'answer': q['correct_answers'][0], 'level': 'hard', 'lang': 'fr'})
        self.assertTrue(r.context['correct'])
        r = self.client.post('/practice/cartesian-place-point/check/', {'answer': '(0, 0)', 'level': 'hard', 'lang': 'fr'})
        self.assertFalse(r.context['correct'])
        self.assertContains(r, 'En vert : la bonne réponse')
