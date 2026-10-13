"""
Fill Skill.curriculum_ref from quiz/curriculum.py (audit QC references) where it
is still empty, after re-running the idempotent taxonomy seed so skills added in
code since the last seed exist. Later seed migrations just call ``seed_all``.
"""
import importlib

from django.db import migrations


def seed_all(apps, schema_editor):
    importlib.import_module('quiz.migrations.0012_seed_grade4_skills').seed_grade4(apps, schema_editor)
    try:
        from quiz.curriculum import ref_string
    except Exception:
        return
    Skill = apps.get_model('quiz', 'Skill')
    for skill in Skill.objects.filter(curriculum_ref=''):
        ref = ref_string(skill.slug)
        if ref:
            skill.curriculum_ref = ref
            skill.save(update_fields=['curriculum_ref'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0019_parent_email_verified'),
    ]

    operations = [
        migrations.RunPython(seed_all, noop),
    ]
