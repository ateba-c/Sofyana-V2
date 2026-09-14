from django.test import TestCase

from .answers import (
    check_answer, infer_answer_type, parse_number, parse_duration,
    parse_coordinate, normalize_text, input_spec,
)


class ParseNumberTests(TestCase):
    def test_integers_and_decimals(self):
        self.assertEqual(parse_number('6'), 6)
        self.assertEqual(parse_number('6.0'), 6)
        self.assertEqual(parse_number('6,0'), 6)
        self.assertEqual(parse_number(' 007 '), 7)
        self.assertEqual(parse_number('3.'), 3)
        self.assertEqual(parse_number('-2,5'), parse_number('-2.5'))
        self.assertEqual(parse_number('−3'), -3)          # unicode minus

    def test_thousands_with_spaces(self):
        self.assertEqual(parse_number('1 234'), 1234)
        self.assertEqual(parse_number('1 234 567'), 1234567)
        self.assertEqual(parse_number('3 500,5'), parse_number('3500.5'))

    def test_fractions_and_mixed(self):
        self.assertEqual(parse_number('3/4'), parse_number('0.75'))
        self.assertEqual(parse_number('4/6'), parse_number('2/3'))
        self.assertEqual(parse_number('1 1/2'), parse_number('1.5'))
        self.assertIsNone(parse_number('1/0'))

    def test_units_and_currency_ignored(self):
        self.assertEqual(parse_number('12 cm'), 12)
        self.assertEqual(parse_number('5 m²'), 5)
        self.assertEqual(parse_number('20 °C'), 20)
        self.assertEqual(parse_number('$4.50'), parse_number('4.5'))
        self.assertEqual(parse_number('4,50 $'), parse_number('4.5'))
        self.assertEqual(parse_number('120 cm³'), 120)

    def test_garbage(self):
        self.assertIsNone(parse_number(''))
        self.assertIsNone(parse_number('abc'))
        self.assertIsNone(parse_number(None))


class ParseOtherTests(TestCase):
    def test_duration(self):
        self.assertEqual(parse_duration('1 h 30 min'), 90)
        self.assertEqual(parse_duration('1h30'), 90)
        self.assertEqual(parse_duration('1:30'), 90)
        self.assertEqual(parse_duration('90 min'), 90)
        self.assertEqual(parse_duration('2 h'), 120)
        self.assertEqual(parse_duration('2 heures'), 120)
        self.assertEqual(parse_duration('45'), 45)
        self.assertIsNone(parse_duration('bonjour'))

    def test_coordinate(self):
        self.assertEqual(parse_coordinate('(3, 4)'), (3, 4))
        self.assertEqual(parse_coordinate('3,4'), (3, 4))
        self.assertEqual(parse_coordinate('3 ; 4'), (3, 4))
        self.assertIsNone(parse_coordinate('3'))

    def test_normalize_text(self):
        self.assertEqual(normalize_text('  Élève !'), 'eleve')
        self.assertEqual(normalize_text('Triangle.'), normalize_text('triangle'))


class InferTests(TestCase):
    def test_inference(self):
        self.assertEqual(infer_answer_type(['42']), 'integer')
        self.assertEqual(infer_answer_type(['3 500']), 'integer')
        self.assertEqual(infer_answer_type(['3,5', '3.5']), 'decimal')
        self.assertEqual(infer_answer_type(['2/3']), 'fraction')
        self.assertEqual(infer_answer_type(['1 h 30 min', '90 min']), 'duration')
        self.assertEqual(infer_answer_type(['(3, 4)', '3, 4']), 'coordinate')
        self.assertEqual(infer_answer_type(['<']), 'symbol')
        self.assertEqual(infer_answer_type(['4,50 $', '$4.50']), 'money')
        self.assertEqual(infer_answer_type(['Yes']), 'text')
        self.assertEqual(infer_answer_type(['cm']), 'text')
        self.assertEqual(infer_answer_type(['120', '120 cm³']), 'integer')
        self.assertEqual(infer_answer_type([]), 'text')


class CheckAnswerTests(TestCase):
    """The '6 is not 6' family of bugs."""

    def test_six_equals_six(self):
        self.assertTrue(check_answer('6', ['6.0']))
        self.assertTrue(check_answer('6.0', ['6']))
        self.assertTrue(check_answer('6,0', ['6']))
        self.assertTrue(check_answer('6 cm', ['6']))
        self.assertTrue(check_answer(' 6 ', ['6']))
        self.assertFalse(check_answer('7', ['6']))

    def test_decimal_equivalents(self):
        self.assertTrue(check_answer('0.50', ['0,5']))
        self.assertTrue(check_answer('.5', ['0.5']))
        self.assertTrue(check_answer('1/2', ['0.5']))
        self.assertTrue(check_answer('0.5', ['1/2'], 'fraction'))
        self.assertFalse(check_answer('0.5', ['0.05']))

    def test_fractions(self):
        self.assertTrue(check_answer('4/6', ['2/3']))
        self.assertTrue(check_answer('1 1/2', ['3/2']))
        self.assertFalse(check_answer('2/3', ['3/2']))

    def test_duration_and_coordinates(self):
        self.assertTrue(check_answer('90 min', ['1 h 30 min'], 'duration'))
        self.assertTrue(check_answer('1h30', ['1 h 30 min']))
        self.assertFalse(check_answer('1 h 20 min', ['1 h 30 min']))
        self.assertTrue(check_answer('3;4', ['(3, 4)', '3, 4', '3,4']))
        self.assertFalse(check_answer('4, 3', ['(3, 4)']))

    def test_symbols(self):
        self.assertTrue(check_answer(' < ', ['<']))
        self.assertTrue(check_answer('<=', ['≤']))
        self.assertFalse(check_answer('>', ['<']))

    def test_text(self):
        self.assertTrue(check_answer('triangle', ['Triangle']))
        self.assertTrue(check_answer('Angle aigu', ['angle aigu', 'acute angle']))
        self.assertTrue(check_answer('CARRE', ['carré']))
        self.assertTrue(check_answer('Yes.', ['Yes']))
        self.assertFalse(check_answer('No', ['Yes']))

    def test_money(self):
        self.assertTrue(check_answer('4.5', ['4,50 $', '$4.50']))
        self.assertTrue(check_answer('4,50$', ['4,50 $']))

    def test_wrong_declared_type_never_breaks_correct_answer(self):
        # Declared 'integer' but the answer is a word: tolerant fallback still works.
        self.assertTrue(check_answer('carré', ['Carré'], 'integer'))

    def test_empty(self):
        self.assertFalse(check_answer('', ['6']))
        self.assertFalse(check_answer('6', []))


class InputSpecTests(TestCase):
    def test_spec(self):
        self.assertEqual(input_spec('integer')['inputmode'], 'numeric')
        self.assertEqual(input_spec('decimal', 'fr')['placeholder'], '3,5')
        self.assertEqual(input_spec('bogus')['answer_type'], 'bogus')
        self.assertEqual(input_spec(None)['answer_type'], 'text')


# ── AI search ────────────────────────────────────────────────────────────────

from unittest import mock
from django.contrib.auth.models import User
from django.test import Client, override_settings
from .models import Skill, ParentProfile, ParentAssignment, SearchQuery, Student


class SearchEngineTests(TestCase):
    def setUp(self):
        from .ai import search as s
        s._catalog_cache.clear()
        Skill.objects.filter(slug='missing-addend').update(
            keywords_fr='terme manquant, nombre manquant, addition à trou',
            description_en='Find the missing number in an addition like 12 + ___ = 20.')

    def test_keyword_fallback_matches_keywords_and_names(self):
        from .ai.search import keyword_search
        res = keyword_search('le nombre manquant dans une addition', 'fr')
        self.assertTrue(res)
        self.assertEqual(res[0]['slug'], 'missing-addend')
        self.assertTrue(0 < res[0]['score'] <= 1)

    def test_keyword_fallback_empty(self):
        from .ai.search import keyword_search
        self.assertEqual(keyword_search('', 'fr'), [])
        self.assertEqual(keyword_search('zzzz qqqq', 'fr'), [])

    @override_settings(LLM_API_KEY='')
    def test_search_skills_uses_keyword_when_unconfigured(self):
        from .ai.search import search_skills
        res, engine = search_skills('nombre manquant addition', 'fr')
        self.assertEqual(engine, 'keyword')
        self.assertEqual(res[0]['slug'], 'missing-addend')

    @override_settings(LLM_API_KEY='x')
    def test_llm_results_are_validated(self):
        from .ai.search import search_skills
        fake = {'results': [{'slug': 'not-a-skill', 'score': 0.9, 'why': 'nope'},
                            {'slug': 'g5-volume', 'score': '0.8', 'why': 'volume'},
                            {'slug': 'g5-volume', 'score': 0.7, 'why': 'dup'},
                            {'slug': 'add', 'score': 7, 'why': 'clamped'}]}
        with mock.patch('quiz.ai.client.complete_json', return_value=fake):
            res, engine = search_skills('volume', 'en')
        self.assertEqual(engine, 'llm')
        self.assertEqual([r['slug'] for r in res], ['g5-volume', 'add'])
        self.assertEqual(res[0]['score'], 0.8)
        self.assertEqual(res[1]['score'], 1.0)

    @override_settings(LLM_API_KEY='x')
    def test_llm_failure_falls_back(self):
        from .ai.search import search_skills
        with mock.patch('quiz.ai.client.complete_json', side_effect=RuntimeError('boom')):
            res, engine = search_skills('nombre manquant', 'fr')
        self.assertEqual(engine, 'keyword')
        self.assertEqual(res[0]['slug'], 'missing-addend')


@override_settings(ALLOWED_HOSTS=['testserver'], LLM_API_KEY='')
class SearchViewTests(TestCase):
    def setUp(self):
        from .ai import search as s
        s._catalog_cache.clear()
        Skill.objects.filter(slug='missing-addend').update(keywords_fr='nombre manquant, addition à trou')
        self.kid = User.objects.create_user('kid', password='pw1234')
        Student.objects.create(user=self.kid)
        self.parent = User.objects.create_user('mom', password='pw1234')
        pp = ParentProfile.objects.create(user=self.parent)
        pp.children.add(self.kid)
        self.c = Client()

    def test_requires_login(self):
        self.assertEqual(self.c.get('/search/').status_code, 302)

    def test_page_renders_for_kid_and_parent(self):
        self.c.login(username='kid', password='pw1234')
        r = self.c.get('/search/?lang=fr')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Trouver un exercice')
        self.c.login(username='mom', password='pw1234')
        r = self.c.get('/search/?lang=en')
        self.assertContains(r, 'assign it to your child')

    def test_kid_search_gets_practice_button_and_is_logged(self):
        self.c.login(username='kid', password='pw1234')
        r = self.c.post('/search/run/', {'lang': 'fr', 'q': 'le nombre manquant dans une addition'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '/practice/missing-addend/')
        self.assertContains(r, 'Pratiquer')
        self.assertNotContains(r, 'Assigner')
        sq = SearchQuery.objects.get()
        self.assertEqual(sq.user, self.kid)
        self.assertEqual(sq.engine, 'keyword')
        self.assertEqual(sq.results[0]['slug'], 'missing-addend')

    def test_parent_gets_assign_button_and_can_assign_inline(self):
        self.c.login(username='mom', password='pw1234')
        r = self.c.post('/search/run/', {'lang': 'fr', 'q': 'nombre manquant addition'})
        self.assertContains(r, 'Assigner à kid')
        r = self.c.post('/parent/assign/?lang=fr',
                        {'child_id': self.kid.pk, 'topic_slug': 'missing-addend'},
                        HTTP_HX_REQUEST='true')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Assigné à kid')
        self.assertTrue(ParentAssignment.objects.filter(student=self.kid, topic_slug='missing-addend').exists())

    def test_empty_and_bad_image(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        self.c.login(username='kid', password='pw1234')
        r = self.c.post('/search/run/', {'lang': 'fr', 'q': ''})
        self.assertContains(r, 'ajoute une photo')
        bad = SimpleUploadedFile('x.txt', b'hello', content_type='text/plain')
        r = self.c.post('/search/run/', {'lang': 'en', 'q': '', 'photo': bad})
        self.assertContains(r, 'Unsupported image')
        self.assertEqual(SearchQuery.objects.count(), 0)
