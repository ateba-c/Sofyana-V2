"""
Add the clock-reasoning skills (grades 3 → 6, quiz.generators.clock) to the
DB taxonomy: same idempotent seed + domain re-ordering as 0012 / 0013.
"""
import importlib

from django.db import migrations


def seed_clock(apps, schema_editor):
    m = importlib.import_module('quiz.migrations.0012_seed_grade4_skills')
    m.seed_grade4(apps, schema_editor)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_assignment_tracking'),
    ]

    operations = [
        migrations.RunPython(seed_clock, noop),
    ]
