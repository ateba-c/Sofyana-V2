"""Extend the 4th level to grade 3 / grade 5 / general arithmetic skills (same rule as 0015)."""
import importlib

from django.db import migrations


def add_level(apps, schema_editor):
    importlib.import_module('quiz.migrations.0015_resolution_level').add_level(apps, schema_editor)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('quiz', '0015_resolution_level')]
    operations = [migrations.RunPython(add_level, noop)]
