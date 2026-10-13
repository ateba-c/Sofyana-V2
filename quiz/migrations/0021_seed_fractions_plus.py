"""Curriculum upgrade WP2 (fractions): seed the new skills and their audit refs."""
import importlib

from django.db import migrations


def seed(apps, schema_editor):
    importlib.import_module('quiz.migrations.0020_curriculum_refs').seed_all(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0020_curriculum_refs'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
