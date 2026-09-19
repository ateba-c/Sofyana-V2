"""
Add the Grade 6 domains / skills to the DB taxonomy (same mechanism as 0012).
"""
import importlib

from django.db import migrations


def seed_grade6(apps, schema_editor):
    m = importlib.import_module('quiz.migrations.0012_seed_grade4_skills')
    m.seed_grade4(apps, schema_editor)      # idempotent seed + domain re-ordering


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_seed_grade4_skills'),
    ]

    operations = [
        migrations.RunPython(seed_grade6, noop),
    ]
