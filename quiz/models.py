from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class QuizSet(models.Model):
    title_en = models.CharField(max_length=200)
    title_fr = models.CharField(max_length=200, blank=True)
    description_en = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_en


QUESTION_TYPES = [
    ('multiple_choice', _('Multiple Choice')),
    ('drag_drop',       _('Drag & Drop')),
    ('connect',         _('Connect Many-to-Many')),
    ('mix_match',       _('Mix & Match')),
    ('text_input',      _('Text Input')),
]


class Question(models.Model):
    quiz_set         = models.ForeignKey(QuizSet, related_name='questions', on_delete=models.CASCADE)
    order            = models.PositiveIntegerField(default=0)
    q_type           = models.CharField(max_length=30, choices=QUESTION_TYPES, default='multiple_choice')
    prompt_en        = models.TextField()
    prompt_fr        = models.TextField(blank=True)
    hint_en          = models.TextField(blank=True)
    hint_fr          = models.TextField(blank=True)
    explanation_en   = models.TextField(blank=True,
                           help_text='Step-by-step worked solution (English). One step per line.')
    explanation_fr   = models.TextField(blank=True,
                           help_text='Step-by-step worked solution (French). One step per line.')
    illustration_url = models.URLField(blank=True)
    shape_data       = models.JSONField(default=list, blank=True,
                           help_text='List of shape dicts rendered as SVG canvas')
    time_limit       = models.PositiveIntegerField(default=30, help_text='seconds')
    points           = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"[{self.q_type}] {self.prompt_en[:60]}"


class Choice(models.Model):
    """Used by multiple_choice, drag_drop, mix_match"""
    question   = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    label_en   = models.CharField(max_length=300)
    label_fr   = models.CharField(max_length=300, blank=True)
    is_correct = models.BooleanField(default=False)
    group      = models.CharField(max_length=50, blank=True)
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label_en


class Pair(models.Model):
    """Left <-> Right pairs for connect / mix-match"""
    question = models.ForeignKey(Question, related_name='pairs', on_delete=models.CASCADE)
    left_en  = models.CharField(max_length=300)
    left_fr  = models.CharField(max_length=300, blank=True)
    right_en = models.CharField(max_length=300)
    right_fr = models.CharField(max_length=300, blank=True)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class StudentSession(models.Model):
    quiz_set    = models.ForeignKey(QuizSet, on_delete=models.CASCADE)
    started_at  = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    score       = models.PositiveIntegerField(default=0)
    max_score   = models.PositiveIntegerField(default=0)
    answers     = models.JSONField(default=dict)
    language    = models.CharField(max_length=5, default='en')

    def percentage(self):
        if self.max_score == 0:
            return 0
        return round(self.score / self.max_score * 100)


# ── User profile & progress tracking ─────────────────────────────────────────

AVATAR_SLUGS = ['cat', 'dog', 'fox', 'lion', 'bear', 'panda',
                'frog', 'butterfly', 'octopus', 'unicorn', 'dino', 'rocket']

AVATAR_EMOJIS = {
    'cat': '🐱', 'dog': '🐶', 'fox': '🦊', 'lion': '🦁',
    'bear': '🐻', 'panda': '🐼', 'frog': '🐸', 'butterfly': '🦋',
    'octopus': '🐙', 'unicorn': '🦄', 'dino': '🦖', 'rocket': '🚀',
}


class Student(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    avatar_slug   = models.CharField(max_length=20, default='rocket')
    total_stars   = models.PositiveIntegerField(default=0)
    unlocked_avatars = models.JSONField(default=list, blank=True)
    skill_ratings = models.JSONField(default=dict, blank=True)  # {topic: {correct: int, total: int}}
    created_at    = models.DateTimeField(auto_now_add=True)

    def avatar_emoji(self):
        return AVATAR_EMOJIS.get(self.avatar_slug, '🚀')

    def __str__(self):
        return f'{self.user.username} ({self.avatar_emoji()})'


class ProblemInteraction(models.Model):
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions')
    topic              = models.CharField(max_length=50, db_index=True)
    level              = models.CharField(max_length=10, default='medium')
    is_correct         = models.BooleanField()
    points_earned      = models.PositiveSmallIntegerField(default=0)
    time_taken_seconds = models.PositiveSmallIntegerField(default=0)
    error_type         = models.CharField(max_length=60, blank=True, default='',
                             help_text='Misconception category for wrong answers')
    created_at         = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        mark = '✓' if self.is_correct else '✗'
        return f'{self.user.username} {mark} {self.topic} ({self.level})'


class ParentProfile(models.Model):
    """Guardian/parent account linked to one or more student children."""
    user     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    children = models.ManyToManyField(User, related_name='parents', blank=True,
                   help_text='Student accounts this parent is linked to')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Parent: {self.user.username}'


class ParentAssignment(models.Model):
    """A skill topic assigned by a parent to a specific child student."""
    parent     = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='assignments')
    student    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_assignments')
    topic_slug = models.CharField(max_length=50, db_index=True)
    note       = models.CharField(max_length=200, blank=True)
    assigned_at  = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-assigned_at']
        unique_together = [('parent', 'student', 'topic_slug')]

    def __str__(self):
        done = '✓' if self.completed_at else '○'
        return f'{done} {self.parent.user.username} → {self.student.username}: {self.topic_slug}'
