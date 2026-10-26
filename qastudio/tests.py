import json
from unittest import mock

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase, override_settings

from quiz import taxonomy as quiz_taxonomy
from quiz.generators import GENERATORS
from quiz.models import Skill, Student
from quiz.taxonomy import skill_map

from . import certification, proposals, sampling, services
from .lint import lint_payload
from .models import CRITERIA_KEYS, CertificationEvent, QuestionSample, ReviewerProfile, SkillCertification

ALL_OK = {k: True for k in CRITERIA_KEYS}

# What g5-data-table produced before the fix (the screenshot that started the QA Studio).
OLD_DATA_TABLE = {
    'q_type': 'multiple_choice',
    'prompt_fr': "Tableau : Football: 7 | Basketball: 15 | Natation: 4. Tableau des sports : Football: 7, Basketball: 15, "
                 "Natation: 4. Combien d'élèves au total ont répondu ?",
    'prompt_en': 'Table: Soccer: 7 | Basketball: 15 | Swimming: 4. Table of sports: Soccer: 7, Basketball: 15, '
                 'Swimming: 4. How many students answered in total?',
    'hint_fr': 'Lis bien chaque valeur avant de calculer.', 'hint_en': 'Read each value carefully before calculating.',
    'shape_data': [], 'pairs': [],
    'choices': [{'label': x, 'correct': x == '26', 'error_type': ''} for x in ('22', '33', '26', '15', '25')],
    'explanation_fr': "Étape 2 : Identifie le type de question.\nRéponse : 26",
    'explanation_en': 'Step 2: Identify the question type.\nAnswer: 26',
    'correct_answers': ['26'],
}


class DeterminismTests(SimpleTestCase):
    def test_same_seed_same_problem_for_every_generator(self):
        sm = skill_map()
        for slug in GENERATORS:
            for level in (sm.get(slug) or {}).get('level_sequence') or ['easy', 'medium', 'hard']:
                a = sampling.fingerprint(sampling.generate(slug, level, 1234))
                b = sampling.fingerprint(sampling.generate(slug, level, 1234))
                self.assertEqual(a, b, f'{slug}/{level} is not reproducible from its seed')

    def test_generate_does_not_disturb_global_random(self):
        import random
        random.seed(5)
        expected = [random.random() for _ in range(3)]
        random.seed(5)
        sampling.generate('add', 'easy', 99)
        self.assertEqual([random.random() for _ in range(3)], expected)


class LintTests(SimpleTestCase):
    def test_flags_the_original_data_table_question(self):
        rules = {f['rule'] for f in lint_payload(OLD_DATA_TABLE, 'g5-data-table') if f['severity'] == 'error'}
        self.assertIn('LINT-01', rules)          # raw pipes
        self.assertIn('LINT-02', rules)          # data written twice
        warn = {f['rule'] for f in lint_payload(OLD_DATA_TABLE, 'g5-data-table')}
        self.assertIn('LINT-08', warn)           # generic explanation

    def test_fixed_data_table_is_clean(self):
        for seed in range(1, 40):
            for level in ('easy', 'medium', 'hard'):
                found = lint_payload(sampling.generate('g5-data-table', level, seed), 'g5-data-table')
                self.assertEqual([f for f in found if f['severity'] == 'error'], [], found)

    def test_option_rules(self):
        bad = dict(OLD_DATA_TABLE, prompt_fr='Combien ?', prompt_en='How many?',
                   choices=[{'label': '5', 'correct': True}, {'label': '5', 'correct': True}])
        msgs = [f['message'] for f in lint_payload(bad, 'add') if f['rule'] == 'LINT-03']
        self.assertTrue(any('identical' in m for m in msgs))
        self.assertTrue(any('marked correct' in m for m in msgs))

    def test_negatives_only_allowed_in_signed_skills(self):
        q = dict(OLD_DATA_TABLE, prompt_fr='Quelle température ?', prompt_en='What temperature?',
                 choices=[{'label': '−5', 'correct': True}, {'label': '5', 'correct': False}])
        self.assertIn('LINT-12', {f['rule'] for f in lint_payload(q, 'add')})
        self.assertNotIn('LINT-12', {f['rule'] for f in lint_payload(q, 'g6-integer-thermometer')})
        for slug in ('g6-integer-read', 'g6-integer-order', 'g6-integer-number-line', 'g6-integer-thermometer'):
            for seed in range(1, 30):
                for level in ('easy', 'medium', 'hard'):
                    found = lint_payload(sampling.generate(slug, level, seed), slug)
                    self.assertEqual([f for f in found if f['rule'] in ('LINT-12', 'LINT-03')], [], (slug, found))

    def test_language_leak(self):
        bad = dict(OLD_DATA_TABLE, prompt_en="Combien d'élèves ont répondu dans la classe ?")
        self.assertIn('LINT-07', {f['rule'] for f in lint_payload(bad, 'add')})


class ProposalTests(SimpleTestCase):
    def test_round_trip_and_apply(self):
        payload = sampling.generate('g5-data-table', 'easy', 7)
        start = proposals.from_payload(payload)
        self.assertEqual(start['format_type'], 'MARKDOWN_TABLE')
        self.assertFalse(proposals.differs(payload, start))
        edit = json.loads(json.dumps(start))
        edit['prompt_fr'] = 'Nouvelle consigne ?'
        edit['format_type'] = 'BULLET_LIST'
        edit['bullets'] = [['Chat : 3', 'Cat: 3']]
        self.assertTrue(proposals.differs(payload, edit))
        q = sampling.render_question(proposals.apply(payload, proposals.clean(edit)), 'g5-data-table', 'fr')
        self.assertEqual(q['prompt_fr'], 'Nouvelle consigne ?')
        self.assertEqual(q['bullets'], ['Chat : 3'])
        self.assertNotIn('table', q)


class StudioBase(TestCase):
    def setUp(self):
        self.skill = Skill.objects.get(slug='g5-data-table')
        self.other = Skill.objects.get(slug='add')
        self.master = User.objects.create_superuser('boss', password='pw-boss-123')
        self.rev_user = User.objects.create_user('rev', password='pw-rev-1234')
        self.rev = ReviewerProfile.objects.create(user=self.rev_user, role=ReviewerProfile.REVIEWER)
        self.rev.skills.add(self.skill)
        quiz_taxonomy.invalidate()

    def approve_n(self, n, user=None):
        samples = services.ingest(self.skill, n)
        for s in samples:
            s.status = QuestionSample.UNREVIEWED       # linter verdicts aside, the reviewer decides
            s.save()
            services.vote(s, user or self.rev_user, services.APPROVE, ALL_OK)
        return samples


class CertificationTests(StudioBase):
    def test_state_machine_and_events(self):
        cert = certification.cert_for(self.skill)
        cert.threshold = 3
        cert.save()
        samples = self.approve_n(3)
        cert.refresh_from_db()
        self.assertEqual((cert.state, cert.approved_count), (SkillCertification.CERTIFIED, 3))
        self.assertTrue(CertificationEvent.objects.filter(skill=self.skill, event=certification.EVENT_CERTIFIED).exists())
        services.vote(samples[0], self.rev_user, services.REWORK, ALL_OK, note='typo')
        cert.refresh_from_db()
        self.assertEqual(cert.state, SkillCertification.DEGRADED)
        self.assertTrue(CertificationEvent.objects.filter(event=certification.EVENT_DEGRADED).exists())
        services.vote(samples[0], self.rev_user, services.APPROVE, ALL_OK)
        cert.refresh_from_db()
        self.assertEqual(cert.state, SkillCertification.CERTIFIED)

    def test_vote_rules(self):
        s = services.ingest(self.skill, 1)[0]
        with self.assertRaises(services.QAError):
            services.vote(s, self.rev_user, services.APPROVE, {**ALL_OK, 'clarity': False})
        with self.assertRaises(services.QAError):
            services.vote(s, self.rev_user, services.REJECT, ALL_OK, note='')
        with self.assertRaises(services.QAError):
            services.vote(s, self.rev_user, services.REWORK, ALL_OK, note='')
        services.save_proposal(s, self.rev_user, {'prompt_fr': 'x'})
        with self.assertRaises(services.QAError):
            services.vote(s, self.rev_user, services.APPROVE, ALL_OK)
        services.vote(s, self.rev_user, services.REWORK, ALL_OK)            # the proposal is the explanation
        self.assertEqual(QuestionSample.objects.get(pk=s.pk).status, QuestionSample.FLAGGED)

    def test_scope(self):
        s = services.ingest(self.other, 1)[0]
        with self.assertRaises(services.QAError):
            services.vote(s, self.rev_user, services.APPROVE, ALL_OK)
        self.rev.domains.add(self.other.domain)
        services.vote(s, self.rev_user, services.APPROVE, ALL_OK)

    def test_generator_change_reopens_approved_samples(self):
        cert = certification.cert_for(self.skill)
        cert.threshold = 2
        cert.save()
        samples = self.approve_n(2)
        # simulate a code change: what was approved is no longer what the generator produces
        QuestionSample.objects.filter(pk=samples[0].pk).update(fingerprint='0' * 64)
        self.assertEqual(services.refresh_all(), 1)
        s = QuestionSample.objects.get(pk=samples[0].pk)
        self.assertTrue(s.stale)
        self.assertIn(s.status, (QuestionSample.UNREVIEWED, QuestionSample.FLAGGED))
        cert.refresh_from_db()
        self.assertEqual((cert.state, cert.approved_count), (SkillCertification.DEGRADED, 1))

    @override_settings(QA_WEBHOOK_URL='https://example.test/hook', QA_WEBHOOK_SECRET='s3cret')
    def test_webhook_payload_is_signed(self):
        cert = certification.cert_for(self.skill)
        cert.threshold = 1
        cert.save()
        with mock.patch('qastudio.certification.threading.Thread') as thread:
            self.approve_n(1)
        url, payload, _ = thread.call_args.kwargs['args']
        self.assertEqual(url, 'https://example.test/hook')
        self.assertEqual(payload['event'], certification.EVENT_CERTIFIED)
        self.assertEqual(payload['subtopic_id'], 'g5-data-table')
        with mock.patch('urllib.request.urlopen') as urlopen:
            urlopen.return_value.__enter__.return_value.status = 200
            certification._post_webhook(url, payload, CertificationEvent.objects.first().pk)
        req = urlopen.call_args.args[0]
        self.assertTrue(req.headers['X-sofyana-signature'].startswith('sha256='))
        self.assertEqual(CertificationEvent.objects.first().webhook_status, 'HTTP 200')


class GateTests(StudioBase):
    def setUp(self):
        super().setUp()
        self.kid = User.objects.create_user('kid', password='pw-kid-1234')
        Student.objects.create(user=self.kid, grade=5)

    def tearDown(self):
        quiz_taxonomy.invalidate()

    @override_settings(QA_GATE_ENABLED=True)
    def test_uncertified_skill_is_hidden_and_locked(self):
        quiz_taxonomy.invalidate()
        self.client.login(username='kid', password='pw-kid-1234')
        r = self.client.get('/practice/g5-data-table/?lang=fr')
        self.assertEqual(r.status_code, 403)
        self.assertContains(r, 'Bientôt disponible', status_code=403)
        self.assertNotIn('g5-data-table', quiz_taxonomy.topic_meta())
        certification.set_override(certification.cert_for(self.skill), 'unlock')
        self.assertEqual(self.client.get('/practice/g5-data-table/?lang=fr').status_code, 200)
        self.assertIn('g5-data-table', quiz_taxonomy.topic_meta())

    def test_gate_off_by_default(self):
        self.client.login(username='kid', password='pw-kid-1234')
        self.assertEqual(self.client.get('/practice/g5-data-table/?lang=fr').status_code, 200)


class ViewTests(StudioBase):
    def test_access(self):
        self.assertEqual(self.client.get('/qa/').status_code, 302)                   # login first
        User.objects.create_user('nobody', password='pw-nobody-1')
        self.client.login(username='nobody', password='pw-nobody-1')
        self.assertEqual(self.client.get('/qa/').status_code, 403)                   # no reviewer profile

    def test_reviewer_flow(self):
        s = services.ingest(self.skill, 2)[0]
        self.client.login(username='rev', password='pw-rev-1234')
        r = self.client.get(f'/qa/s/{s.pk}/?skill=g5-data-table')
        self.assertContains(r, s.code)
        self.assertContains(r, 'Grille pédagogique')
        # simulator: the real practice page, with the question routed to this sample
        r = self.client.get(f'/qa/s/{s.pk}/frame/?lang=fr')
        self.assertContains(r, 'practice-area')
        self.assertContains(r, f'/qa/s/{s.pk}/question/')
        r = self.client.get(f'/qa/s/{s.pk}/question/?lang=fr')
        self.assertContains(r, "Nombre d&#x27;élèves")                              # the table is rendered
        q = self.client.session[f'qa_q_{s.pk}']
        idx = sampling.correct_index(q)
        r = self.client.post(f'/qa/s/{s.pk}/check/', {'answer': str(idx), 'lang': 'fr'})
        self.assertTrue(r.context['correct'])
        # live draft preview
        draft = proposals.from_payload(s.payload)
        draft['prompt_fr'] = 'Consigne réécrite par la réviseure ?'
        r = self.client.post(f'/qa/s/{s.pk}/draft/', json.dumps(draft), content_type='application/json')
        self.assertEqual(r.status_code, 204)
        self.assertContains(self.client.get(f'/qa/s/{s.pk}/question/?lang=fr&draft=1'), 'Consigne réécrite')
        # vote
        data = {'action': 'approve', 'note': '', **{f'c_{k}': 'on' for k in CRITERIA_KEYS}}
        r = self.client.post(f'/qa/s/{s.pk}/vote/', data)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(QuestionSample.objects.get(pk=s.pk).status, QuestionSample.APPROVED)

    def test_master_tools(self):
        self.client.login(username='boss', password='pw-boss-123')
        r = self.client.post('/qa/skill/add/ingest/', {'count': '3'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(QuestionSample.objects.filter(skill=self.other).count(), 3)
        r = self.client.post('/qa/team/', {'username': 'newrev', 'password': 'longpassword', 'role': 'ROLE_REVIEWER',
                                           'grades': ['3', '4']})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(ReviewerProfile.objects.get(user__username='newrev').grades, [3, 4])
        r = self.client.post('/qa/skill/add/settings/', {'threshold': '15', 'override': 'lock'})
        self.assertEqual(SkillCertification.objects.get(skill=self.other).threshold, 15)
        data = self.client.get('/qa/export.json').json()
        self.assertEqual(len(data['items']), 3)
        item = data['items'][0]
        self.assertEqual(set(item['taxonomy']), {'level_id', 'domain_id', 'category_id', 'subtopic_id', 'subtopic_display_name'})
        self.assertIn(item['prompt']['format_type'], ('PLAIN_TEXT', 'MARKDOWN_TABLE', 'BULLET_LIST', 'IMAGE_PROMPT'))
        self.assertEqual(self.client.get('/qa/export.csv').status_code, 200)
        self.assertEqual(self.client.get('/qa/').status_code, 200)
        # reviewers can't use master tools
        self.client.login(username='rev', password='pw-rev-1234')
        self.assertEqual(self.client.post('/qa/skill/add/ingest/', {'count': '3'}).status_code, 403)
        self.assertEqual(self.client.get('/qa/export.json').status_code, 403)
