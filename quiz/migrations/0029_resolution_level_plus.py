"""Curriculum upgrade F3: the 4th level for the new skills (FAMILIES_PLUS in resolution_plus.py), same rule as 0015."""
import importlib

from django.db import migrations


def add_level(apps, schema_editor):
    importlib.import_module('quiz.migrations.0015_resolution_level').add_level(apps, schema_editor)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('quiz', '0028_seed_vocab_reasoning')]
    operations = [migrations.RunPython(add_level, noop)]
