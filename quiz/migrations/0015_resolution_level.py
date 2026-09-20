"""
Give qualifying skills a 4th level, "resolution" (problem solving), in their
DB level_sequence.  The list of qualifying skills lives in code
(quiz.generators.resolution.RESOLUTION_FAMILIES).
"""
from django.db import migrations


def add_level(apps, schema_editor):
    Skill = apps.get_model('quiz', 'Skill')
    try:
        from quiz.generators.resolution import RESOLUTION_FAMILIES
    except Exception:
        return
    for skill in Skill.objects.filter(slug__in=list(RESOLUTION_FAMILIES)):
        seq = list(skill.level_sequence or ['easy', 'medium', 'hard'])
        if 'resolution' not in seq:
            seq.append('resolution')
            skill.level_sequence = seq
            skill.save(update_fields=['level_sequence'])


def remove_level(apps, schema_editor):
    Skill = apps.get_model('quiz', 'Skill')
    for skill in Skill.objects.all():
        seq = [lv for lv in (skill.level_sequence or []) if lv != 'resolution']
        if seq != list(skill.level_sequence or []):
            skill.level_sequence = seq
            skill.save(update_fields=['level_sequence'])


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_student_grade'),
    ]

    operations = [
        migrations.RunPython(add_level, remove_level),
    ]
