from django.apps import AppConfig


class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz'

    def ready(self):
        # Drop the in-process taxonomy cache whenever a Skill/SkillDomain changes.
        from . import taxonomy
        taxonomy.connect_signals()
