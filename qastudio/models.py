"""
QA Studio data model.

Sofyana questions are *generated*, not stored: each skill has a generator that
builds a new problem every time.  So the Studio reviews **samples**: a generator
run for (skill, level) with a fixed random seed.  The same seed always gives the
same problem, so a sample can be shown again, and the fingerprint of its output
tells us when the generator code has changed since a reviewer approved it.

Certification unit (taxonomy tier 4, "subtopic") = a Skill.  A skill is
CERTIFIED when it has at least ``threshold`` approved, up-to-date samples.
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from quiz.models import Skill, SkillDomain

CRITERIA = [
    ('rendering',    'Affichage & rendu',        'Rendering'),
    ('clarity',      'Clarté & vocabulaire',     'Clarity & vocabulary'),
    ('structure',    'Structure des données',    'Data structure'),
    ('accuracy',     'Exactitude mathématique',  'Mathematical accuracy'),
    ('ambiguity',    "Absence d'ambiguïté",      'No ambiguity'),
    ('hint_quality', "Pertinence de l'indice",   'Hint quality'),
]
CRITERIA_KEYS = [c[0] for c in CRITERIA]


def default_threshold():
    return getattr(settings, 'QA_DEFAULT_THRESHOLD', 10)


class ReviewerProfile(models.Model):
    MASTER, REVIEWER = 'ROLE_MASTER', 'ROLE_REVIEWER'
    ROLES = [(MASTER, 'Master reviewer'), (REVIEWER, 'Pedagogical reviewer')]

    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='qa_profile')
    role        = models.CharField(max_length=20, choices=ROLES, default=REVIEWER)
    all_skills  = models.BooleanField(default=False, help_text="Scope = everything (['ALL'])")
    skills      = models.ManyToManyField(Skill, blank=True, related_name='qa_reviewers')
    domains     = models.ManyToManyField(SkillDomain, blank=True, related_name='qa_reviewers',
                                         help_text='Every skill of these domains is in scope')
    grades      = models.JSONField(default=list, blank=True,
                                   help_text='Whole grade bands in scope, e.g. [3, 4]')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    @property
    def is_master(self):
        return self.role == self.MASTER or self.user.is_superuser


class SkillCertification(models.Model):
    LOCKED, CERTIFIED, DEGRADED = 'LOCKED', 'CERTIFIED', 'DEGRADED'
    STATES = [(LOCKED, 'Locked'), (CERTIFIED, 'Certified'), (DEGRADED, 'Degraded')]
    OVERRIDES = [('', 'None (automatic)'), ('unlock', 'Force unlock'), ('lock', 'Force lock')]

    skill           = models.OneToOneField(Skill, on_delete=models.CASCADE, related_name='qa_cert')
    threshold       = models.PositiveSmallIntegerField(default=default_threshold)
    approved_count  = models.PositiveIntegerField(default=0)
    state           = models.CharField(max_length=10, choices=STATES, default=LOCKED)
    override        = models.CharField(max_length=10, choices=OVERRIDES, blank=True, default='')
    certified_at    = models.DateTimeField(null=True, blank=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.skill.slug}: {self.state} {self.approved_count}/{self.threshold}'

    @property
    def is_live(self):
        """Visible to students when the QA gate is on."""
        if self.override == 'unlock':
            return True
        if self.override == 'lock':
            return False
        return self.state == self.CERTIFIED


class QuestionSample(models.Model):
    UNREVIEWED, FLAGGED, APPROVED, REJECTED = 'UNREVIEWED', 'FLAGGED_FOR_REWORK', 'APPROVED', 'REJECTED'
    STATUSES = [(UNREVIEWED, 'Unreviewed'), (FLAGGED, 'Flagged for rework'),
                (APPROVED, 'Approved'), (REJECTED, 'Rejected')]

    skill        = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='qa_samples')
    level        = models.CharField(max_length=12)
    seed         = models.BigIntegerField()
    payload      = models.JSONField(help_text='Raw generator output for this seed (before localization)')
    fingerprint  = models.CharField(max_length=64, db_index=True)
    status       = models.CharField(max_length=20, choices=STATUSES, default=UNREVIEWED, db_index=True)
    checklist    = models.JSONField(default=dict, blank=True, help_text='{criterion: true/false}')
    lint         = models.JSONField(default=list, blank=True, help_text='[{rule, criterion, severity, lang, message}]')
    proposal     = models.JSONField(null=True, blank=True,
                                    help_text='Reviewer rewrite: what the question should look like (input for a generator fix)')
    stale        = models.BooleanField(default=False,
                                       help_text='The generator now gives a different problem for this seed (code changed)')
    reviewed_by  = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    reviewed_at  = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('skill', 'level', 'seed')]
        ordering = ['skill__domain__grade', 'skill__order', 'level', 'id']

    def __str__(self):
        return f'Q-{self.pk} {self.skill.slug}/{self.level}#{self.seed}'

    @property
    def code(self):
        return f'Q-{self.pk}'

    @property
    def lint_errors(self):
        return [f for f in self.lint if f.get('severity') == 'error']

    @property
    def lint_warnings(self):
        return [f for f in self.lint if f.get('severity') != 'error']


class AuditEntry(models.Model):
    """Every action on a sample: votes, edits, comments, linter flags, staleness."""
    sample     = models.ForeignKey(QuestionSample, on_delete=models.CASCADE, related_name='audit')
    user       = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
                                   help_text='Empty = system (linter, generator refresh)')
    action     = models.CharField(max_length=30)
    note       = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']

    @property
    def actor(self):
        if self.user_id is None:
            return 'Système'
        return self.user.get_full_name() or self.user.username


class CertificationEvent(models.Model):
    """EVENT_SUBTOPIC_CERTIFIED / EVENT_SUBTOPIC_DEGRADED log (also sent to the webhook, if configured)."""
    skill        = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='qa_events')
    event        = models.CharField(max_length=40)
    from_state   = models.CharField(max_length=10)
    to_state     = models.CharField(max_length=10)
    approved     = models.PositiveIntegerField()
    threshold    = models.PositiveSmallIntegerField()
    webhook_status = models.CharField(max_length=60, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
