"""AI pre-review tests. The LLM is always mocked: no network, no cost."""
import json
from unittest import mock

from django.test import override_settings

from quiz.models import Skill

from . import ai_review, certification, services
from .models import CRITERIA_KEYS, AIReview, QuestionSample, SkillDiagnosis
from .tests import ALL_OK, StudioBase


def fake_llm(calls):
    """Stand-in for quiz.ai.client.complete_json: the solver always answers choices 1 and 2."""
    def complete_json(system, user, **kw):
        calls.append(system[:40])
        data = json.loads(user)
        if 'Solve each problem' in system:
            return {'results': [{'id': p['id'], 'answer': '?', 'correct_choices': [1, 2], 'confident': True,
                                 'ambiguous': False, 'note': ''} for p in data['problems']]}
        if 'review generated math questions' in system:
            return {'results': [{'id': q['id'], 'verdict': 'clean', 'summary': 'RAS',
                                 'criteria': {k: {'ok': True, 'reason': ''} for k in CRITERIA_KEYS},
                                 'suggestion': {'prompt_fr': 'Nouvelle consigne ?', 'format_type': 'PLAIN_TEXT',
                                                'choices': [{'label_fr': '1. 7', 'label_en': '1) 7', 'correct': True},
                                                            {'label_fr': '2. 1.5', 'label_en': '2. 1.5', 'correct': False}]}}
                                for q in data['questions']]}
        return {'summary': 'Générateur correct.', 'issues': [
            {'title': 'Choix ambigus', 'criterion': 'ambiguity', 'severity': 'major', 'samples': ['Q-1'],
             'fix': 'Filtrer.'}]}
    return complete_json


class SyncThread:
    """Runs a background job inline (tests)."""
    def __init__(self, target, daemon=None):
        self.target = target

    def start(self):
        self.target()


@override_settings(LLM_API_KEY='test-key')
class AIReviewTests(StudioBase):
    def test_compare(self):
        q = {'q_type': 'multiple_choice', 'choices': [{'label': 'A', 'correct': False}, {'label': 'B', 'correct': True},
                                                      {'label': 'C', 'correct': False}]}
        self.assertEqual(ai_review.compare(q, {'correct_choices': [2]})['status'], 'match')
        self.assertEqual(ai_review.compare(q, {'correct_choices': [2, 3]})['status'], 'multiple')
        self.assertEqual(ai_review.compare(q, {'correct_choices': [1]})['status'], 'mismatch')
        self.assertEqual(ai_review.compare(q, {'correct_choices': [2], 'ambiguous': True})['status'], 'unsure')
        self.assertEqual(ai_review.compare(q, None)['status'], 'none')
        t = {'q_type': 'text_input', 'correct_answers': ['1/2'], 'answer_type': ''}
        self.assertEqual(ai_review.compare(t, {'answer': '0,5'})['status'], 'match')
        self.assertEqual(ai_review.compare(t, {'answer': '3'})['status'], 'mismatch')

    def test_blind_description_hides_the_key(self):
        s = services.ingest(self.skill, 1)[0]
        blind, _ = ai_review.describe(s, with_key=False)
        text = json.dumps(blind, ensure_ascii=False)
        self.assertNotIn('answer_key', text)
        self.assertNotIn('explanation', text)
        full, _ = ai_review.describe(s, with_key=True)
        self.assertIn('correct_choice', full['answer_key'])

    def test_run_saves_advisory_reviews_and_diagnosis(self):
        samples = services.ingest(self.skill, 3)
        before = {s.pk: s.status for s in samples}
        calls = []
        with mock.patch('quiz.ai.client.complete_json', side_effect=fake_llm(calls)):
            done, total = ai_review.run_skills([self.skill], workers=1)
        self.assertEqual((done, total), (1, 1))
        for s in samples:
            r = s.ai_reviews.first()
            # the solver disagreed with the key (picked choices 1 and 2): 'clean' is overruled
            self.assertIn(r.solver['status'], ('multiple', 'mismatch'))
            self.assertEqual(r.verdict, AIReview.MAJOR)
            self.assertGreaterEqual(r.risk, 40)
            self.assertEqual(r.suggestion['prompt_fr'], 'Nouvelle consigne ?')
            self.assertEqual([c['label_fr'] for c in r.suggestion['choices']], ['7', '1.5'])   # numbering stripped
            self.assertEqual(r.suggestion['choices'][0]['label_en'], '7')
            self.assertEqual(QuestionSample.objects.get(pk=s.pk).status, before[s.pk])     # advisory only
        d = SkillDiagnosis.objects.get(skill=self.skill)
        self.assertEqual(d.issues[0]['severity'], 'major')
        self.assertEqual(len(calls), 3)            # solve + review (one chunk) + diagnosis
        calls.clear()                              # nothing new: a second run makes no call
        with mock.patch('quiz.ai.client.complete_json', side_effect=fake_llm(calls)):
            ai_review.run_skills([self.skill], workers=1)
        self.assertEqual(calls, [])
        self.assertEqual(certification.cert_for(self.skill).approved_count, 0)   # never counts toward N

    def test_llm_failure_is_recorded_not_raised(self):
        services.ingest(self.skill, 2)
        with mock.patch('quiz.ai.client.complete_json', side_effect=RuntimeError('boom')):
            ai_review.run_skills([self.skill], workers=1)
        self.assertTrue(AIReview.objects.filter(verdict=AIReview.ERROR, error__contains='boom').exists())
        self.assertIn('boom', SkillDiagnosis.objects.get(skill=self.skill).error)

    def test_queue_tabs_and_risk_order(self):
        a, b, c = services.ingest(self.skill, 3)
        QuestionSample.objects.filter(pk__in=[a.pk, b.pk, c.pk]).update(status=QuestionSample.UNREVIEWED)
        for s, verdict, risk in ((a, 'clean', 0), (b, 'major', 90), (c, 'minor', 25)):
            AIReview.objects.create(sample=s, fingerprint=s.fingerprint, model='m', verdict=verdict, risk=risk)
        skills = Skill.objects.filter(pk=self.skill.pk)
        self.assertEqual([s.pk for s in services.queue(skills, 'todo')], [b.pk, c.pk, a.pk])
        self.assertEqual([s.pk for s in services.queue(skills, 'ai_issues')], [b.pk, c.pk])
        self.assertEqual([s.pk for s in services.queue(skills, 'ai_clean')], [a.pk])
        # a review of an older output of the generator doesn't count
        QuestionSample.objects.filter(pk=b.pk).update(fingerprint='f' * 64)
        self.assertEqual([s.pk for s in services.queue(skills, 'ai_issues')], [c.pk])

    def test_agreement(self):
        a, b = services.ingest(self.skill, 2)
        for s in (a, b):
            s.status = QuestionSample.UNREVIEWED
            s.save()
            AIReview.objects.create(sample=s, fingerprint=s.fingerprint, model='m', verdict='clean',
                                    criteria={k: {'ok': True, 'reason': ''} for k in CRITERIA_KEYS})
        services.vote(a, self.rev_user, services.APPROVE, ALL_OK)
        services.vote(b, self.rev_user, services.REWORK, {**ALL_OK, 'accuracy': False}, note='faux')
        ag = ai_review.agreement(Skill.objects.filter(pk=self.skill.pk))
        self.assertEqual((ag['overall']['n'], ag['overall']['agree'], ag['overall']['missed']), (2, 1, 1))
        acc = next(c for c in ag['criteria'] if c['key'] == 'accuracy')
        self.assertEqual((acc['n'], acc['missed']), (2, 1))
        self.assertEqual([s.pk for s in ag['missed_examples']], [b.pk])

    def test_views(self):
        s = services.ingest(self.skill, 1)[0]
        self.client.login(username='rev', password='pw-rev-1234')
        r = self.client.get(f'/qa/s/{s.pk}/?skill=g5-data-table')
        self.assertContains(r, 'Pré-revue IA')
        self.assertContains(r, 'IA ⚠')
        calls = []
        with mock.patch('quiz.ai.client.complete_json', side_effect=fake_llm(calls)), \
                mock.patch('qastudio.ai_review.threading.Thread', SyncThread), \
                mock.patch('qastudio.ai_review.close_old_connections'):
            self.assertEqual(self.client.post(f'/qa/s/{s.pk}/ai/').status_code, 302)
        r = self.client.get(f'/qa/s/{s.pk}/?skill=g5-data-table')
        self.assertContains(r, 'Problème important')
        self.assertContains(r, 'Voir la correction proposée')
        self.assertEqual(self.client.get('/qa/ai/status/').json(), {'pending': 0})
        # skill-wide runs cost money: masters only
        self.assertEqual(self.client.post('/qa/skill/g5-data-table/ai/').status_code, 403)
        self.client.login(username='boss', password='pw-boss-123')
        with mock.patch('quiz.ai.client.complete_json', side_effect=fake_llm(calls)), \
                mock.patch('qastudio.ai_review.threading.Thread', SyncThread), \
                mock.patch('qastudio.ai_review.close_old_connections'):
            self.assertEqual(self.client.post('/qa/skill/g5-data-table/ai/', {'force': '1'}).status_code, 302)
        r = self.client.get('/qa/?skill=g5-data-table')
        self.assertContains(r, 'Diagnostic du générateur')
        self.assertContains(r, 'Choix ambigus')
        self.assertContains(r, 'Fiabilité IA')

    @override_settings(LLM_API_KEY='')
    def test_without_llm_the_studio_hides_ai(self):
        s = services.ingest(self.skill, 1)[0]
        self.client.login(username='rev', password='pw-rev-1234')
        r = self.client.get(f'/qa/s/{s.pk}/?skill=g5-data-table')
        self.assertNotContains(r, 'Pré-revue IA')
        self.assertNotContains(r, 'IA ⚠')
