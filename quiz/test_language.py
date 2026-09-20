"""
One language, end to end: the session language sticks, and every part of a
question (prompt, hint, choices, pairs, items) is in that language.
"""
import re

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase

from .generators import GENERATORS
from .labels import localize_problem, translate_label
from .models import Student

FRENCH_WORDS = re.compile(
    r'(?<![\wÀ-ÿ])(unités?|dizaines?|centaines?|milliers?|dixièmes?|centièmes?|millièmes?|'
    r'parallèles|perpendiculaires|sécantes|carré|losange|trapèze|parallélogramme|aigu|obtus|'
    r'sommets?|arêtes?|soustraction|habitants|visiteurs|places|Été|Automne|Hiver|Printemps|'
    r'Rouge|Bleu|Vert|Jaune|Chien|Oiseau|Poisson|Pomme|Banane|Natation|Oui|Non|et|cent|mille|'
    r'vingt|trente|quarante|cinquante|soixante|quatre|dix|deux|trois|cinq|sept|huit|neuf)(?![\wÀ-ÿ])',
    re.IGNORECASE)
ENGLISH_ONLY = re.compile(r'(?<![\wÀ-ÿ])(Yes|No|Prime|Composite|Even|Odd|and)(?![\wÀ-ÿ])')


def _labels(q):
    out = [c['label'] for c in q.get('choices') or []]
    out += [p['left'] for p in q.get('pairs') or []] + [p['right'] for p in q.get('pairs') or []]
    out += [i['label'] for i in q.get('items') or []]
    return out


class TranslateLabelTests(SimpleTestCase):
    def test_vocabulary(self):
        self.assertEqual(translate_label('dizaines de mille', 'en'), 'ten thousands')
        self.assertEqual(translate_label('centaines (c)', 'en'), 'hundreds (c)')
        self.assertEqual(translate_label('1 et 2', 'en'), '1 and 2')
        self.assertEqual(translate_label('5 faces, 6 sommets, 9 arêtes', 'en'), '5 faces, 6 vertices, 9 edges')
        self.assertEqual(translate_label('Kilomètre (km)', 'en'), 'Kilometre (km)')
        self.assertEqual(translate_label('4 h 05', 'en'), '4:05')
        self.assertEqual(translate_label('106 481 places', 'en'), '106 481 seats')
        self.assertEqual(translate_label('Yes', 'fr'), 'Oui')
        self.assertEqual(translate_label('Prime', 'fr'), 'Premier')
        # numbers / symbols untouched
        self.assertEqual(translate_label('3/4', 'en'), '3/4')
        self.assertEqual(translate_label('12 cm', 'en'), '12 cm')

    def test_every_generator_localizes_both_ways(self):
        for slug, gen in GENERATORS.items():
            for level in ('easy', 'medium', 'hard'):
                for _ in range(15):
                    q_en = localize_problem(gen(level), 'en')
                    for lab in _labels(q_en):
                        self.assertIsNone(FRENCH_WORDS.search(lab), f'{slug}/{level} EN label still French: {lab!r}')
                    q_fr = localize_problem(gen(level), 'fr')
                    for lab in _labels(q_fr):
                        self.assertIsNone(ENGLISH_ONLY.search(lab), f'{slug}/{level} FR label in English: {lab!r}')
                    # localized mix_match / ordering keys stay consistent with what is displayed
                    if q_en.get('q_type') == 'mix_match':
                        self.assertEqual(q_en['correct_answers'], [p['right'] for p in q_en['pairs']])
                    if q_en.get('q_type') == 'ordering':
                        self.assertEqual(set(q_en['correct_answers']), {i['label'] for i in q_en['items']})


class StickyLanguageTests(TestCase):
    def setUp(self):
        u = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=u, grade=4)
        self.client.login(username='kid', password='abcd')

    def test_language_sticks_across_requests(self):
        self.client.get('/?lang=fr')
        r = self.client.get('/practice/g4-quadrilateral-name/')          # no lang param
        self.assertEqual(r.context['lang'], 'fr')
        r = self.client.get('/practice/g4-quadrilateral-name/next/?level=easy')
        self.assertEqual(r.context['lang'], 'fr')
        q = self.client.session['pq_g4-quadrilateral-name']
        self.assertTrue(all(c['label'] in ('carré', 'rectangle', 'parallélogramme', 'losange', 'trapèze') for c in q['choices']))
        # switch to English explicitly → everything English, and it sticks
        r = self.client.get('/practice/g4-quadrilateral-name/next/?lang=en&level=easy')
        q = self.client.session['pq_g4-quadrilateral-name']
        self.assertTrue(all(c['label'] in ('square', 'rectangle', 'parallelogram', 'rhombus', 'trapezoid') for c in q['choices']))
        r = self.client.get('/')
        self.assertEqual(r.context['lang'], 'en')

    def test_default_is_french(self):
        r = self.client.get('/')
        self.assertEqual(r.context['lang'], 'fr')

    def test_check_uses_localized_choices(self):
        self.client.get('/practice/g4-lines/next/?lang=en&level=easy')
        q = self.client.session['pq_g4-lines']
        idx = next(i for i, c in enumerate(q['choices']) if c['correct'])
        r = self.client.post('/practice/g4-lines/check/', {'answer': str(idx), 'level': 'easy', 'lang': 'en'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['correct'])
