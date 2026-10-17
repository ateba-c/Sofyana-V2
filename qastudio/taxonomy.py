"""
Generic N-tier taxonomy (spec §2) mapped onto Sofyana's tables.

    Tier 1  level_group  ← grade band (Quebec cycles) from SkillDomain.grade
    Tier 2  domain       ← mathematical field, from the skill's audit refs (QC-xxx)
    Tier 3  category     ← SkillDomain (e.g. « 5e année — Statistiques & Probabilité »)
    Tier 4  subtopic     ← Skill  (the certification unit)

To adapt the hierarchy for another curriculum, change TIERS: each tier is
(key, label_fr, label_en, resolver), where resolver(skill) → (id, title).
"""
from quiz.curriculum import CURRICULUM_REFS

# Audit entry ranges per field (docs/curriculum/PLAN.md scorecard: 131 / 40 / 38 / 11 / 16)
_FIELDS = [
    (1, 131, 'arithmetic', 'Arithmétique', 'Arithmetic'),
    (132, 171, 'geometry', 'Géométrie', 'Geometry'),
    (172, 209, 'measurement', 'Mesure', 'Measurement'),
    (210, 220, 'statistics', 'Statistique', 'Statistics'),
    (221, 236, 'probability', 'Probabilité', 'Probability'),
]
_FIELD_HINTS = [('geometr', 'geometry'), ('shape', 'geometry'), ('space', 'geometry'), ('measur', 'measurement'),
                ('time', 'measurement'), ('money', 'measurement'), ('conversion', 'measurement'),
                ('statist', 'statistics'), ('data', 'statistics'), ('probab', 'probability'), ('chance', 'probability')]


def _field_meta(key):
    for lo, hi, k, fr, en in _FIELDS:
        if k == key:
            return k, fr, en
    return _FIELDS[0][2:]


def field_of(skill):
    refs = CURRICULUM_REFS.get(skill.slug) or []
    counts = {}
    for r in refs:
        for lo, hi, key, *_ in _FIELDS:
            if lo <= r <= hi:
                counts[key] = counts.get(key, 0) + 1
    if counts:
        return _field_meta(max(counts, key=counts.get))
    name = f'{skill.domain.slug} {skill.slug}'.lower()
    for hint, key in _FIELD_HINTS:
        if hint in name:
            return _field_meta(key)
    return _field_meta('arithmetic')


def band_of(skill):
    g = skill.domain.grade
    if g is None:
        return 'general', 'Enrichissement (général)', 'Enrichment (general)'
    if g <= 2:
        return 'cycle_1', '1er cycle (1re–2e année)', 'Cycle 1 (grades 1–2)'
    if g <= 4:
        return 'cycle_2', '2e cycle (3e–4e année)', 'Cycle 2 (grades 3–4)'
    return 'cycle_3', '3e cycle (5e–6e année)', 'Cycle 3 (grades 5–6)'


TIERS = [
    ('level_group', 'Niveau', 'Level group', lambda s: band_of(s)),
    ('domain',      'Domaine', 'Domain',     lambda s: field_of(s)),
    ('category',    'Catégorie', 'Category', lambda s: (s.domain.slug, s.domain.name_fr or s.domain.name_en, s.domain.name_en)),
    ('subtopic',    'Compétence', 'Subtopic', lambda s: (s.slug, s.name_fr or s.name_en, s.name_en)),
]


def path(skill):
    """[{tier, id, title_fr, title_en}, …] from the broadest tier to the skill."""
    out = []
    for key, _, _, resolver in TIERS:
        ident, fr, en = resolver(skill)
        out.append({'tier': key, 'id': ident, 'title_fr': fr, 'title_en': en})
    return out


def ids(skill):
    """{'level_id', 'domain_id', 'category_id', 'subtopic_id'} as in the question JSON schema."""
    p = path(skill)
    return {
        'level_id': p[0]['id'], 'domain_id': p[1]['id'], 'category_id': p[2]['id'],
        'subtopic_id': p[3]['id'], 'subtopic_display_name': p[3]['title_fr'],
    }
