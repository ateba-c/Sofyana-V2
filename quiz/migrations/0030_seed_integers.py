"""Curriculum upgrade WP9 (integers, decision D2): seed the grade-6 integer skills, their audit refs and their 4th level."""
import importlib

from django.db import migrations


def seed(apps, schema_editor):
    importlib.import_module('quiz.migrations.0020_curriculum_refs').seed_all(apps, schema_editor)
    importlib.import_module('quiz.migrations.0015_resolution_level').add_level(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0029_resolution_level_plus'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
