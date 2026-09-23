"""
Parent assignment tracking (Sept 2026):
- assigning several skills at once, child's grade listed first, suggestions
- history is kept: re-assigning a completed topic adds a new row, the old one stays done
- practice answers feed the open assignment (started/done dates, questions, time) and auto-complete it
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import ParentAssignment, ParentProfile, ProblemInteraction, Student


class AssignmentTrackingTests(TestCase):
    def setUp(self):
        self.parent_user = User.objects.create_user('dad', password='secret1')
        self.parent = ParentProfile.objects.create(user=self.parent_user)
        self.kid = User.objects.create_user('kid', password='abcd')
        Student.objects.create(user=self.kid, grade=4)
        self.parent.children.add(self.kid)
        self.client.login(username='dad', password='secret1')

    def test_multi_assign(self):
        r = self.client.post('/parent/assign/', {'child_id': self.kid.pk,
                                                 'topic_slugs': ['g4-roman-to-arabic', 'g4-clock-24h', 'not-a-skill']})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(set(ParentAssignment.objects.filter(student=self.kid).values_list('topic_slug', flat=True)),
                         {'g4-roman-to-arabic', 'g4-clock-24h'})
        # assigning an open topic again does not duplicate it
        self.client.post('/parent/assign/', {'child_id': self.kid.pk, 'topic_slugs': ['g4-clock-24h']})
        self.assertEqual(ParentAssignment.objects.filter(student=self.kid, topic_slug='g4-clock-24h').count(), 1)

    def test_reassign_completed_keeps_history(self):
        self.client.post('/parent/assign/', {'child_id': self.kid.pk, 'topic_slug': 'g4-roman-to-arabic'})
        a = ParentAssignment.objects.get(student=self.kid)
        a.completed_at = timezone.now()
        a.save()
        self.client.post('/parent/assign/', {'child_id': self.kid.pk, 'topic_slug': 'g4-roman-to-arabic'})
        rows = ParentAssignment.objects.filter(student=self.kid, topic_slug='g4-roman-to-arabic')
        self.assertEqual(rows.count(), 2)
        a.refresh_from_db()
        self.assertIsNotNone(a.completed_at)          # the finished one stays finished
        self.assertTrue(rows.filter(completed_at__isnull=True).exists())

    def test_practice_feeds_assignment_and_autocompletes(self):
        self.client.post('/parent/assign/', {'child_id': self.kid.pk, 'topic_slug': 'g4-roman-to-arabic'})
        a = ParentAssignment.objects.get(student=self.kid)
        a.goal = 3
        a.save()
        self.client.logout()
        self.client.login(username='kid', password='abcd')
        for _ in range(3):
            r = self.client.get('/practice/g4-roman-to-arabic/next/?level=easy')
            self.assertEqual(r.status_code, 200)
            self.assertIn('served_at', self.client.session['pq_g4-roman-to-arabic'])
            self.client.post('/practice/g4-roman-to-arabic/check/', {'level': 'easy', 'answer': '0'})
        a.refresh_from_db()
        self.assertIsNotNone(a.started_at)
        self.assertEqual(a.questions_done, 3)
        self.assertIsNotNone(a.completed_at)
        self.assertEqual(a.progress_pct, 100)
        self.assertEqual(ProblemInteraction.objects.filter(user=self.kid).count(), 3)
        # the child's home page shows the assignment with its dates
        r = self.client.get('/?lang=en')
        self.assertContains(r, 'Assigned ')
        self.assertContains(r, 'Done ')

    def test_dashboard_lists_child_grade_first_with_suggestions(self):
        self.client.post('/parent/assign/', {'child_id': self.kid.pk, 'topic_slug': 'g6-multiply'})
        r = self.client.get('/parent/?lang=en')
        self.assertEqual(r.status_code, 200)
        child = r.context['children_data'][0]
        self.assertEqual(child['assign_groups'][0]['grade'], 4)
        self.assertTrue(child['suggestions'])
        self.assertTrue(all(s['slug'] != 'g6-multiply' for s in child['suggestions']))
        self.assertContains(r, 'name="topic_slugs"')
        self.assertContains(r, 'Daily journal', status_code=200, html=False) if child['daily_log'] else None
        self.assertContains(r, 'Assigned ')
