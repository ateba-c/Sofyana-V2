"""
Read-side helpers for the skill taxonomy.

Views and templates ask these functions instead of importing the hardcoded
lists from ``quiz.generators``.  Results come from the database (SkillDomain /
Skill) and are cached in-process; the cache is dropped whenever a Skill or
SkillDomain is saved or deleted.  If the tables are empty (fresh checkout
before the seed migration ran) we fall back to the legacy lists so nothing
breaks.
"""
from django.db.models.signals import post_save, post_delete

_cache = {}


def invalidate(**kwargs):
    _cache.clear()


def _load():
    if 'groups' in _cache:
        return
    from .models import Skill
    try:
        skills = list(
            Skill.objects.filter(is_active=True)
            .select_related('domain', 'prereq', 'next_skill', 'mastery_next', 'downgrade')
            .order_by('domain__order', 'domain_id', 'order', 'id')
        )
    except Exception:            # table missing (pre-migration) → legacy fallback
        skills = []
    if not skills:
        from .generators import TOPIC_GROUPS, SKILL_MAP
        _cache['groups'] = [dict(g, topics=[dict(t) for t in g['topics']]) for g in TOPIC_GROUPS]
        _cache['skill_map'] = dict(SKILL_MAP)
        _cache['answer_types'] = {}
    else:
        groups, by_domain = [], {}
        skill_map, answer_types = {}, {}
        for s in skills:
            d = s.domain
            if d.id not in by_domain:
                by_domain[d.id] = {
                    'slug': d.slug, 'name_en': d.name_en, 'name_fr': d.name_fr or d.name_en,
                    'icon': d.icon, 'grade': d.grade, 'topics': [],
                }
                groups.append(by_domain[d.id])
            by_domain[d.id]['topics'].append({
                'slug': s.slug, 'name_en': s.name_en, 'name_fr': s.name_fr or s.name_en,
            })
            skill_map[s.slug] = {
                'prereq':         s.prereq.slug if s.prereq else None,
                'next':           s.next_skill.slug if s.next_skill else None,
                'mastery_next':   s.mastery_next.slug if s.mastery_next else None,
                'downgrade':      s.downgrade.slug if s.downgrade else None,
                'level_sequence': s.level_sequence or ['easy', 'medium', 'hard'],
            }
            if s.answer_type:
                answer_types[s.slug] = s.answer_type
        _cache['groups'] = groups
        _cache['skill_map'] = skill_map
        _cache['answer_types'] = answer_types

    meta = {}
    for g in _cache['groups']:
        for t in g['topics']:
            meta[t['slug']] = {
                'slug': t['slug'],
                'group_en': g['name_en'], 'group_fr': g['name_fr'], 'group_icon': g['icon'],
                'grade': g.get('grade'),
                'name_en': t['name_en'], 'name_fr': t['name_fr'],
            }
    _cache['meta'] = meta
    _cache['index'] = [
        {'slug': t['slug'], 'en': t['name_en'], 'fr': t['name_fr'], 'icon': g['icon'],
         'gen': g['name_en'], 'gen_fr': g['name_fr'], 'grade': g.get('grade')}
        for g in _cache['groups'] for t in g['topics']
    ]


def topic_groups():
    """[{name_en, name_fr, icon, grade, topics: [{slug, name_en, name_fr}]}] — same shape as legacy TOPIC_GROUPS."""
    _load()
    return _cache['groups']


def topic_meta():
    """{slug: {slug, group_en, group_fr, group_icon, grade, name_en, name_fr}}"""
    _load()
    return _cache['meta']


def skill_map():
    """{slug: {prereq, next, mastery_next, downgrade, level_sequence}} — same shape as legacy SKILL_MAP."""
    _load()
    return _cache['skill_map']


def skill_index():
    """Flat list for the search widget: [{slug, en, fr, icon, gen, gen_fr, grade}]"""
    _load()
    return _cache['index']


def answer_type_for(slug):
    """Editor-declared answer type for a skill, or '' to infer from the problem."""
    _load()
    return _cache['answer_types'].get(slug, '')


def available_grades():
    return sorted({g['grade'] for g in topic_groups() if g.get('grade')})


def connect_signals():
    from .models import Skill, SkillDomain
    for model in (Skill, SkillDomain):
        post_save.connect(invalidate, sender=model, weak=False, dispatch_uid=f'taxonomy_save_{model.__name__}')
        post_delete.connect(invalidate, sender=model, weak=False, dispatch_uid=f'taxonomy_del_{model.__name__}')
