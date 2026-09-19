"""
Add the Grade 4 domains / skills to the DB taxonomy.

Re-runs the idempotent seed from 0010 (existing rows are left untouched, new
slugs from TOPIC_GROUPS / SKILL_MAP are inserted), then renumbers domain
``order`` so the home page lists grades in order (3 → 4 → 5) instead of
appending the new grade after grade 5.
"""
import importlib

from django.db import migrations
from django.utils.text import slugify


def seed_grade4(apps, schema_editor):
    seed = importlib.import_module('quiz.migrations.0010_seed_skill_taxonomy').seed
    seed(apps, schema_editor)

    # Domain order = position in TOPIC_GROUPS.
    try:
        from quiz.generators import TOPIC_GROUPS
    except Exception:
        return
    SkillDomain = apps.get_model('quiz', 'SkillDomain')
    for d_order, group in enumerate(TOPIC_GROUPS):
        grade = group.get('grade')
        base = slugify(group['name_en'].split('—')[-1].strip()) or f'domain-{d_order}'
        d_slug = f'g{grade}-{base}' if grade else base
        SkillDomain.objects.filter(slug=d_slug).update(order=d_order)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_searchquery'),
    ]

    operations = [
        migrations.RunPython(seed_grade4, noop),
    ]
