"""
A student's grade lives in their profile: chosen at registration, changeable
in the profile page, and it puts their grade's material first on the home
page, in the sidebar search and in the AI search results.
"""
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Student


class StudentGradeTests(TestCase):
    def test_register_with_grade(self):
        r = self.client.post('/register/', {'username': 'zoe', 'password1': 'abcd', 'password2': 'abcd', 'grade': '4'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(User.objects.get(username='zoe').student.grade, 4)
        # unknown grade → None (all grades)
        self.client.logout()
        self.client.post('/register/', {'username': 'max', 'password1': 'abcd', 'password2': 'abcd', 'grade': '9'})
        self.assertIsNone(User.objects.get(username='max').student.grade)

    def test_register_page_lists_grades(self):
        r = self.client.get('/register/?lang=fr')
        self.assertContains(r, 'name="grade"')
        self.assertContains(r, '4e année')

    def test_change_grade_in_profile(self):
        u = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=u, grade=3)
        self.client.login(username='kid', password='abcd')
        r = self.client.get('/profile/?lang=en')
        self.assertContains(r, 'My grade')
        self.client.post('/profile/?lang=en', {'grade': '5'})
        u.student.refresh_from_db()
        self.assertEqual(u.student.grade, 5)
        # home page now opens on grade 5 and the sidebar shows it
        r = self.client.get('/?lang=en')
        self.assertEqual(r.context['grade_filter'], 5)
        self.assertContains(r, 'Grade 5')
        self.assertContains(r, 'const myGrade = 5;')
        # back to all grades
        self.client.post('/profile/', {'grade': ''})
        u.student.refresh_from_db()
        self.assertIsNone(u.student.grade)
        r = self.client.get('/?lang=en')
        self.assertContains(r, 'const myGrade = null;')

    def test_avatar_post_still_works(self):
        u = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=u, grade=3)
        self.client.login(username='kid', password='abcd')
        self.client.post('/profile/', {'avatar': 'rocket'})
        u.student.refresh_from_db()
        self.assertEqual(u.student.grade, 3)

    def test_search_results_put_my_grade_first(self):
        u = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=u, grade=6)
        self.client.login(username='kid', password='abcd')
        fake = [{'slug': 'g4-clock-24h', 'why': ''}, {'slug': 'read-clock', 'why': ''},
                {'slug': 'g6-clock-planning', 'why': ''}, {'slug': 'g5-clock-schedule', 'why': ''}]
        with patch('quiz.ai.search.search_skills', return_value=(fake, 'keyword')):
            r = self.client.post('/search/run/?lang=en', {'q': 'clock'})
        self.assertEqual(r.status_code, 200)
        slugs = [x['slug'] for x in r.context['results']]
        self.assertEqual(slugs, ['g6-clock-planning', 'g4-clock-24h', 'read-clock', 'g5-clock-schedule'])
        self.assertContains(r, 'my grade')
