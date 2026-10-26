"""
Regression tests for the parent-feedback round (Sept 2026):
- parents create a child account that is linked to them, with a default grade
- the child's home page opens on their grade
- re-assigning a completed topic adds fresh homework and keeps the history; all assignments show in the practice sidebar
- no square roots anywhere, and no negative numbers outside the grade-6 integer skills (decision D2,
  2026-10-26: negatives only where they occur naturally — temperatures, sea level, floors, 4-quadrant plane)
"""
import re

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from .generators import GENERATORS
from .generators.resolution_plus import SIGNED_SKILLS
from .models import ParentAssignment, ParentProfile, Student

NEG = re.compile(r'(?<![\w\d])[-−]\s?\d')


class NoNegativesNoRootsTests(SimpleTestCase):
    def test_every_generator(self):
        for slug, gen in GENERATORS.items():
            for level in ('easy', 'medium', 'hard'):
                for _ in range(25):
                    q = gen(level)
                    texts = [q.get('prompt_fr', ''), q.get('prompt_en', '')]
                    texts += [str(c.get('label') or c.get('label_en') or '') for c in q.get('choices', [])]
                    texts += [str(a) for a in q.get('correct_answers', [])]
                    texts += [p['left'] + ' ' + p['right'] for p in q.get('pairs', [])]
                    texts += [i['label'] for i in q.get('items', [])]
                    blob = '\n'.join(texts)
                    self.assertNotIn('√', blob, f'{slug}/{level}: square root shown')
                    if slug in SIGNED_SKILLS:
                        continue
                    for a in q.get('correct_answers', []):
                        self.assertFalse(str(a).strip().startswith(('-', '−')), f'{slug}/{level}: negative answer {a!r}')
                    for c in q.get('choices', []):
                        lab = str(c.get('label') or c.get('label_en') or '')
                        self.assertFalse(lab.strip().startswith(('-', '−')), f'{slug}/{level}: negative choice {lab!r}')

    def test_signed_skills_are_the_integer_domain_only(self):
        self.assertTrue(SIGNED_SKILLS)
        for slug in SIGNED_SKILLS:      # grade 6 integers + grade 5 temperatures (audit QC-056→061, 136, 208)
            self.assertTrue(slug.startswith('g6-') or slug in ('g5-thermometer', 'g5-temperature'), slug)


class ParentFlowTests(TestCase):
    def setUp(self):
        self.parent_user = User.objects.create_user('mom', password='secret1')
        self.parent = ParentProfile.objects.create(user=self.parent_user)
        self.client.login(username='mom', password='secret1')

    def test_create_child_links_and_sets_grade(self):
        r = self.client.post('/parent/create-child/?lang=fr',
                             {'child_username': 'kid', 'child_password': 'abcd', 'child_grade': '4'})
        self.assertEqual(r.status_code, 302)
        kid = User.objects.get(username='kid')
        self.assertIn(kid, self.parent.children.all())
        self.assertEqual(kid.student.grade, 4)
        # duplicate username refused
        r = self.client.post('/parent/create-child/', {'child_username': 'KID', 'child_password': 'abcd', 'child_grade': '4'})
        self.assertEqual(User.objects.filter(username__iexact='kid').count(), 1)

    def test_child_home_defaults_to_own_grade(self):
        self.client.post('/parent/create-child/', {'child_username': 'kid', 'child_password': 'abcd', 'child_grade': '6'})
        self.client.logout()
        self.client.login(username='kid', password='abcd')
        r = self.client.get('/')
        self.assertEqual(r.context['grade_filter'], 6)
        r = self.client.get('/?grade=0')
        self.assertIsNone(r.context['grade_filter'])
        r = self.client.get('/?grade=3')
        self.assertEqual(r.context['grade_filter'], 3)

    def test_set_child_grade(self):
        self.client.post('/parent/create-child/', {'child_username': 'kid', 'child_password': 'abcd', 'child_grade': '3'})
        kid = User.objects.get(username='kid')
        self.client.post('/parent/set-child-grade/', {'child_id': kid.pk, 'child_grade': '5'})
        kid.student.refresh_from_db()
        self.assertEqual(kid.student.grade, 5)

    def test_reassign_completed_topic_adds_fresh_homework(self):
        self.client.post('/parent/create-child/', {'child_username': 'kid', 'child_password': 'abcd', 'child_grade': '4'})
        kid = User.objects.get(username='kid')
        self.client.post('/parent/assign/', {'child_id': kid.pk, 'topic_slug': 'g4-roman-to-arabic'})
        a = ParentAssignment.objects.get(student=kid, topic_slug='g4-roman-to-arabic')
        a.completed_at = timezone.now()
        a.save()
        self.client.post('/parent/assign/', {'child_id': kid.pk, 'topic_slug': 'g4-roman-to-arabic'})
        a.refresh_from_db()
        self.assertIsNotNone(a.completed_at)   # history kept
        self.assertEqual(ParentAssignment.objects.filter(student=kid).count(), 2)
        self.assertEqual(ParentAssignment.objects.filter(student=kid, completed_at__isnull=True).count(), 1)

    def test_all_open_assignments_in_practice_sidebar(self):
        self.client.post('/parent/create-child/', {'child_username': 'kid', 'child_password': 'abcd', 'child_grade': '4'})
        kid = User.objects.get(username='kid')
        slugs = [s for s in GENERATORS if s.startswith('g4-')][:9]
        for s in slugs:
            self.client.post('/parent/assign/', {'child_id': kid.pk, 'topic_slug': s})
        self.client.logout()
        self.client.login(username='kid', password='abcd')
        r = self.client.get(f'/practice/{slugs[0]}/')
        shown = {pa['slug'] for pa in r.context['parent_assignments']}
        self.assertEqual(shown, set(slugs))
        self.assertTrue(all(pa['grade'] == 4 for pa in r.context['parent_assignments']))

    def test_parent_dashboard_renders_with_grades(self):
        self.client.post('/parent/create-child/', {'child_username': 'kid', 'child_password': 'abcd', 'child_grade': '4'})
        kid = User.objects.get(username='kid')
        self.client.post('/parent/assign/', {'child_id': kid.pk, 'topic_slug': 'g6-multiply'})
        for lang in ('fr', 'en'):
            r = self.client.get(f'/parent/?lang={lang}')
            self.assertEqual(r.status_code, 200)
            html = r.content.decode()
            self.assertIn('name="topic_slugs"', html)
            self.assertIn('6e année' if lang == 'fr' else 'Grade 6', html)
            self.assertIn('parent/create-child/', html)
