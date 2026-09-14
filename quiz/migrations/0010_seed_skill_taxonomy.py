"""
Seed SkillDomain / Skill from the legacy hardcoded TOPIC_GROUPS and SKILL_MAP
lists so the DB taxonomy starts identical to what the app shipped with.
Idempotent: existing rows (by slug) are left untouched.
"""
from django.db import migrations
from django.utils.text import slugify


def seed(apps, schema_editor):
    SkillDomain = apps.get_model('quiz', 'SkillDomain')
    Skill = apps.get_model('quiz', 'Skill')
    try:
        from quiz.generators import TOPIC_GROUPS, SKILL_MAP, GENERATORS
    except Exception:            # generators package changed/removed: nothing to seed
        return

    skills_by_slug = {}
    for d_order, group in enumerate(TOPIC_GROUPS):
        grade = group.get('grade')
        base = slugify(group['name_en'].split('—')[-1].strip()) or f'domain-{d_order}'
        d_slug = f'g{grade}-{base}' if grade else base
        domain, _ = SkillDomain.objects.get_or_create(
            slug=d_slug,
            defaults={
                'name_en': group['name_en'], 'name_fr': group.get('name_fr', ''),
                'icon': group.get('icon', '🧩'), 'grade': grade, 'order': d_order,
            },
        )
        for s_order, topic in enumerate(group['topics']):
            info = SKILL_MAP.get(topic['slug'], {})
            skill, _ = Skill.objects.get_or_create(
                slug=topic['slug'],
                defaults={
                    'domain': domain,
                    'name_en': topic['name_en'], 'name_fr': topic.get('name_fr', ''),
                    'generator_slug': topic['slug'] if topic['slug'] in GENERATORS else '',
                    'level_sequence': info.get('level_sequence') or ['easy', 'medium', 'hard'],
                    'order': s_order,
                },
            )
            skills_by_slug[skill.slug] = skill

    # Second pass: learning-path links.
    for slug, info in SKILL_MAP.items():
        skill = skills_by_slug.get(slug)
        if not skill:
            continue
        changed = False
        for field, key in (('prereq', 'prereq'), ('next_skill', 'next'),
                           ('mastery_next', 'mastery_next'), ('downgrade', 'downgrade')):
            target = skills_by_slug.get(info.get(key) or '')
            if target and getattr(skill, f'{field}_id') is None:
                setattr(skill, field, target)
                changed = True
        if changed:
            skill.save()


def unseed(apps, schema_editor):
    apps.get_model('quiz', 'Skill').objects.all().delete()
    apps.get_model('quiz', 'SkillDomain').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_skill_taxonomy'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
