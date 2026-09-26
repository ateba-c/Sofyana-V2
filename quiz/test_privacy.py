"""
Launch hygiene: favicon, parent email confirmation, account deletion, legal page,
data retention command.
"""
import re
from datetime import timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from .models import ParentProfile, ProblemInteraction, SearchQuery, Student


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', SITE_URL='https://sofyana.app')
class ParentEmailTests(TestCase):
    def test_register_sends_confirmation_and_link_verifies(self):
        r = self.client.post('/parent/register/?lang=fr', {'username': 'mom', 'email': 'Mom@Example.com',
                                                           'password1': 'secret1', 'password2': 'secret1'})
        self.assertEqual(r.status_code, 302)
        user = User.objects.get(username='mom')
        self.assertEqual(user.email, 'mom@example.com')
        self.assertFalse(user.parent_profile.email_verified)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('mom@example.com', mail.outbox[0].to)
        link = re.search(r'https://sofyana\.app(/parent/verify/[^\s?]+)', mail.outbox[0].body).group(1)
        # dashboard nags until verified
        r = self.client.get('/parent/?lang=en')
        self.assertContains(r, 'Please confirm your email')
        r = self.client.get(link + '?lang=en')
        self.assertEqual(r.status_code, 302)
        user.parent_profile.refresh_from_db()
        self.assertTrue(user.parent_profile.email_verified)
        r = self.client.get('/parent/?lang=en')
        self.assertNotContains(r, 'Please confirm your email')

    def test_bad_token_is_rejected(self):
        r = self.client.get('/parent/verify/not-a-token/?lang=en')
        self.assertEqual(r.status_code, 302)
        self.assertIn('/login/', r.url)

    def test_email_required_and_unique_for_parents(self):
        r = self.client.post('/parent/register/', {'username': 'dad', 'password1': 'secret1', 'password2': 'secret1'})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username='dad').exists())
        self.client.post('/parent/register/', {'username': 'dad', 'email': 'd@x.com', 'password1': 'secret1', 'password2': 'secret1'})
        self.client.logout()
        r = self.client.post('/parent/register/', {'username': 'dad2', 'email': 'D@x.com', 'password1': 'secret1', 'password2': 'secret1'})
        self.assertFalse(User.objects.filter(username='dad2').exists())

    def test_existing_parent_adds_email_and_resends(self):
        u = User.objects.create_user('old', password='secret1')
        ParentProfile.objects.create(user=u)
        self.client.login(username='old', password='secret1')
        r = self.client.get('/parent/?lang=en')
        self.assertContains(r, 'Add an email address')
        self.client.post('/parent/email/', {'email': 'old@x.com'})
        u.refresh_from_db()
        self.assertEqual(u.email, 'old@x.com')
        self.assertEqual(len(mail.outbox), 1)


class DeleteAccountTests(TestCase):
    def test_parent_deletion_removes_own_children_only(self):
        p1 = User.objects.create_user('p1', password='secret1'); pp1 = ParentProfile.objects.create(user=p1)
        p2 = User.objects.create_user('p2', password='secret1'); pp2 = ParentProfile.objects.create(user=p2)
        only_mine = User.objects.create_user('kid1', password='abcd'); Student.objects.create(user=only_mine)
        shared = User.objects.create_user('kid2', password='abcd'); Student.objects.create(user=shared)
        pp1.children.add(only_mine, shared); pp2.children.add(shared)
        ProblemInteraction.objects.create(user=only_mine, topic='add', is_correct=True)
        self.client.login(username='p1', password='secret1')
        r = self.client.post('/account/delete/', {'confirm': 'nope'})
        self.assertTrue(User.objects.filter(username='p1').exists())
        r = self.client.post('/account/delete/?lang=en', {'confirm': 'DELETE'})
        self.assertEqual(r.status_code, 302)
        self.assertFalse(User.objects.filter(username__in=['p1', 'kid1']).exists())
        self.assertTrue(User.objects.filter(username__in=['p2', 'kid2']).count() == 2)
        self.assertEqual(ProblemInteraction.objects.filter(user__username='kid1').count(), 0)

    def test_student_deletes_self(self):
        u = User.objects.create_user('kid', password='abcd'); Student.objects.create(user=u)
        self.client.login(username='kid', password='abcd')
        r = self.client.get('/profile/?lang=fr')
        self.assertContains(r, 'Supprimer mon compte')
        self.client.post('/account/delete/', {'confirm': 'DELETE'})
        self.assertFalse(User.objects.filter(username='kid').exists())


class LegalAndHygieneTests(TestCase):
    def test_legal_page_both_languages_and_footers(self):
        for url, needle in (('/privacy/?lang=en', 'What we keep'), ('/confidentialite/?lang=fr', 'Ce que nous gardons')):
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertContains(r, needle)
            self.assertContains(r, 'favicon.svg')
        r = self.client.get('/?lang=fr')
        self.assertContains(r, '/privacy/')
        r = self.client.get('/parent/register/?lang=en')
        self.assertContains(r, 'name="email"')
        self.assertContains(r, 'privacy policy')

    def test_purge_old_data(self):
        u = User.objects.create_user('kid', password='abcd')
        old = SearchQuery.objects.create(user=u, query='old')
        SearchQuery.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(days=91))
        SearchQuery.objects.create(user=u, query='fresh')
        call_command('purge_old_data')
        self.assertEqual(list(SearchQuery.objects.values_list('query', flat=True)), ['fresh'])
