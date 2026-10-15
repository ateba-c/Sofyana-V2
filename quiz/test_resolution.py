"""
4th level "Résolution": generators are sound, the level appears in the sequence of
qualifying skills only, it unlocks after 5 correct at hard, and the engine serves
its problems.
"""
from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase

from .answers import check_answer
from .generators import GENERATORS, SKILL_MAP, generator_for
from .generators.resolution import RESOLUTION, RESOLUTION_FAMILIES
from .labels import localize_problem
from .models import ProblemInteraction, Student
from .test_language import FRENCH_WORDS


class ResolutionGeneratorTests(SimpleTestCase):
    def test_all_families_all_slugs(self):
        for slug, gen in RESOLUTION.items():
            self.assertIn(slug, GENERATORS)
            for _ in range(60):
                q = gen('resolution')
                self.assertEqual(q['q_type'], 'text_input')
                for k in ('prompt_fr', 'prompt_en', 'hint_fr', 'hint_en', 'explanation_fr', 'explanation_en'):
                    self.assertTrue(q.get(k), f'{slug}: missing {k}')
                self.assertIn('Étape 1', q['explanation_fr'])
                for a in q['correct_answers']:
                    self.assertFalse(str(a).startswith(('-', '−')), f'{slug}: negative {a}')
                    self.assertTrue(check_answer(a, q['correct_answers'], q['answer_type']), f'{slug}: {a} rejected')
                self.assertFalse(check_answer('', q['correct_answers'], q['answer_type']))
                q_en = localize_problem(gen('resolution'), 'en')
                text = q_en['prompt_en']
                for name in ('Saint-Marc', 'Trois-Rivières', 'Val-d’Or', 'Val-des-Pins'):
                    text = text.replace(name, '')
                self.assertIsNone(FRENCH_WORDS.search(text), q_en['prompt_en'])

    def test_stories_vary(self):
        prompts = {RESOLUTION['g4-elapsed-time']()['prompt_fr'] for _ in range(30)}
        self.assertGreater(len(prompts), 20)

    def test_level_sequences(self):
        for slug in RESOLUTION_FAMILIES:
            self.assertEqual(SKILL_MAP[slug]['level_sequence'], ['easy', 'medium', 'hard', 'resolution'], slug)
        for slug, info in SKILL_MAP.items():
            if slug not in RESOLUTION_FAMILIES:
                self.assertNotIn('resolution', info['level_sequence'], slug)
        self.assertIs(generator_for('g4-elapsed-time', 'resolution'), RESOLUTION['g4-elapsed-time'])
        self.assertIs(generator_for('g4-elapsed-time', 'hard'), GENERATORS['g4-elapsed-time'])
        self.assertIs(generator_for('g4-roman-to-arabic', 'resolution'), GENERATORS['g4-roman-to-arabic'])


class ResolutionEngineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=self.user, grade=4)
        self.client.login(username='kid', password='abcd')

    def test_pill_locked_until_five_hard_correct(self):
        r = self.client.get('/practice/g4-elapsed-time/?lang=fr')
        self.assertEqual([lv for lv, _, _ in r.context['levels']], ['easy', 'medium', 'hard', 'resolution'])
        self.assertFalse(r.context['resolution_unlocked'])
        r = self.client.get('/practice/g4-elapsed-time/?lang=fr&level=resolution')
        self.assertEqual(r.context['level'], 'hard')
        self.assertIn('débloquer', r.context['locked_notice'])
        for _ in range(5):
            ProblemInteraction.objects.create(user=self.user, topic='g4-elapsed-time', level='hard', is_correct=True)
        r = self.client.get('/practice/g4-elapsed-time/?lang=fr&level=resolution')
        self.assertEqual(r.context['level'], 'resolution')
        self.assertTrue(r.context['resolution_unlocked'])
        self.assertEqual(r.context['locked_notice'], '')

    def test_non_qualifying_skill_has_three_levels(self):
        r = self.client.get('/practice/g4-roman-to-arabic/?lang=fr')
        self.assertEqual(len(r.context['levels']), 3)

    def test_next_serves_resolution_problem_and_check_works(self):
        self.client.get('/practice/g6-money-compare/next/?lang=fr&level=resolution')
        q = self.client.session['pq_g6-money-compare']
        self.assertEqual(q.get('level'), 'resolution')
        r = self.client.post('/practice/g6-money-compare/check/', {'answer': q['correct_answers'][0], 'level': 'resolution', 'lang': 'fr'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['correct'])
        self.assertEqual(r.context['level_name'], 'Résolution')

    def test_level_up_from_hard_suggests_resolution(self):
        for _ in range(5):
            self.client.get('/practice/g4-end-time/next/?lang=fr&level=hard')
            q = self.client.session['pq_g4-end-time']
            r = self.client.post('/practice/g4-end-time/check/', {'answer': q['correct_answers'][0], 'level': 'hard', 'lang': 'fr'})
        self.assertEqual(r.context['suggested_action'], 'level_up')
        self.assertEqual(r.context['suggested_level'], 'resolution')
        self.assertEqual(r.context['suggested_level_name'], 'Résolution')


class ResolutionPlusTests(SimpleTestCase):
    """Task F3: the curriculum-upgrade skills that got a 4th level, and their new story families."""

    def test_plus_skills_have_four_levels(self):
        from .generators.resolution_plus import FAMILIES_PLUS
        for slug in FAMILIES_PLUS:
            self.assertEqual(SKILL_MAP[slug]['level_sequence'], ['easy', 'medium', 'hard', 'resolution'], slug)
            self.assertIs(generator_for(slug, 'resolution'), RESOLUTION[slug])
        for slug in ('g3-vocab-numbers', 'g4-who-is-right-numbers', 'g3-convex'):   # naming / reasoning skills stay at 3
            self.assertNotIn('resolution', SKILL_MAP[slug]['level_sequence'])

    def test_answers_recompute(self):
        import re
        from fractions import Fraction
        from .answers import parse_number
        from .generators import resolution_plus as rp
        nums = lambda q: [int(x) for x in re.findall(r'\*\*(\d+)', q['prompt_en'].replace(',', ''))]
        for _ in range(200):
            q = rp.angles(6)
            if 'In a triangle' in q['prompt_en']:
                a, b = nums(q)
                self.assertEqual(int(q['correct_answers'][0]) + a + b, 180)
            q = rp.recipe_fractions(6)
            m = re.findall(r'\*\*(\d+)/(\d+)\*\*', q['prompt_en'])
            if 'cup more' in q['prompt_en']:
                self.assertEqual(parse_number(q['correct_answers'][0]), sum(Fraction(int(n), int(d)) for n, d in m))
            q = rp.plant_growth(4)
            if 'week 6' in q['prompt_en']:
                h = nums(q)
                step = h[1] - h[0]
                self.assertGreater(step, 0)
                self.assertEqual([h[i + 1] - h[i] for i in range(3)], [step] * 3)
                self.assertEqual(int(q['correct_answers'][0]), h[3] + 2 * step)
            q = rp.balance(3)
            self.assertGreater(int(q['correct_answers'][0]), 0)
            q = rp.powers_story(6)
            self.assertGreater(int(q['correct_answers'][0]), 0)
            q = rp.remainder_trips(4)
            total, size = nums(q)[:2]
            if 'needed so everyone' in q['prompt_en']:
                self.assertEqual(int(q['correct_answers'][0]), -(-total // size))
            elif 'full' in q['prompt_en']:
                self.assertEqual(int(q['correct_answers'][0]), total // size)
            else:
                self.assertEqual(int(q['correct_answers'][0]), total % size)
