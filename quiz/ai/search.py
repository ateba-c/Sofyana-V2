"""
AI problem search: a kid or parent describes an exercise they saw (text and/or
a photo of the homework) and we return the matching skills, ranked.

Two engines:
- ``llm_search``     — the whole skill catalogue (≈90 skills with descriptions
                       and keywords, ~6k tokens) goes in the system prompt and
                       the model ranks it.  Handles paraphrase, both languages,
                       and images.
- ``keyword_search`` — cheap lexical fallback used when the LLM is not
                       configured or fails.

``search_skills`` picks the engine and always returns the same shape:
[{'slug', 'score' (0-1), 'why'}]  (why is in the requested language).
"""
import json
import re
import unicodedata

from . import client as llm
from ..taxonomy import topic_meta

_catalog_cache = {}

MAX_RESULTS = 5

SYSTEM = """You are the search engine of Sofyana, a Québec elementary-school math practice app (grades 3–6), bilingual French/English.
A child or a parent describes an exercise they saw (homework, textbook, a photo). Your job: pick the skills from the CATALOGUE below that best match what they describe.

Rules:
- Only use slugs that exist in the catalogue. Never invent one.
- Return the best {max_results} matches at most, ordered from best to worst. Return fewer if only a few are relevant, and an empty list if nothing fits.
- "score" is your confidence between 0 and 1.
- "why" is ONE short, friendly sentence in {lang_name} telling the user why this skill matches what they described (mention the concrete thing they described). No markdown.
- If an image is provided, read the exercise in it (numbers, shapes, wording) and match on that.
- If the description is in one language and the catalogue text in another, match on meaning.

CATALOGUE (JSON list of skills):
{catalog}

Answer with JSON: {{"results": [{{"slug": "...", "score": 0.0, "why": "..."}}]}}"""


def _strip_accents(s):
    s = unicodedata.normalize('NFKD', s)
    return ''.join(ch for ch in s if not unicodedata.combining(ch))


def _catalog():
    """Compact JSON of the active skills for the prompt (cached with the taxonomy)."""
    from ..models import Skill
    from .. import taxonomy
    key = id(taxonomy._cache.get('groups'))     # changes whenever the taxonomy cache reloads
    if _catalog_cache.get('key') != key:
        rows = []
        for s in Skill.objects.filter(is_active=True).select_related('domain'):
            rows.append({
                'slug': s.slug,
                'grade': s.domain.grade or 'any',
                'domain': s.domain.name_fr or s.domain.name_en,
                'name_fr': s.name_fr, 'name_en': s.name_en,
                'desc_fr': s.description_fr, 'desc_en': s.description_en,
                'kw_fr': s.keywords_fr, 'kw_en': s.keywords_en,
            })
        _catalog_cache['key'] = key
        _catalog_cache['json'] = json.dumps(rows, ensure_ascii=False, separators=(',', ':'))
        _catalog_cache['rows'] = rows
    return _catalog_cache


def keyword_search(query, lang='fr', limit=MAX_RESULTS):
    """Lexical fallback: score skills by overlapping words in names, descriptions, keywords."""
    q = _strip_accents(query.lower())
    words = {w for w in re.findall(r'[a-z0-9]{3,}', q)}
    if not words:
        return []
    scored = []
    for row in _catalog()['rows']:
        hay_name = _strip_accents(f"{row['name_fr']} {row['name_en']}".lower())
        hay_kw = _strip_accents(f"{row['kw_fr']} {row['kw_en']}".lower())
        hay_desc = _strip_accents(f"{row['desc_fr']} {row['desc_en']} {row['domain']}".lower())
        score = 0.0
        for w in words:
            if w in hay_name:
                score += 3
            if w in hay_kw:
                score += 2
            if w in hay_desc:
                score += 1
        if score:
            scored.append((score, row['slug']))
    scored.sort(reverse=True)
    top = scored[0][0] if scored else 1
    why = 'Correspond aux mots de ta description.' if lang == 'fr' else 'Matches the words in your description.'
    return [{'slug': slug, 'score': round(min(1.0, sc / (top + 1e-9)) * 0.7, 2), 'why': why}
            for sc, slug in scored[:limit]]


def llm_search(query, lang='fr', image=None, limit=MAX_RESULTS):
    """
    image: optional (base64_data, media_type) tuple.
    Raises on LLM failure; callers should fall back to keyword_search.
    """
    system = SYSTEM.format(
        max_results=limit,
        lang_name='French' if lang == 'fr' else 'English',
        catalog=_catalog()['json'],
    )
    content = []
    if image:
        data, media_type = image
        content.append(llm.image_block(data, media_type))
    text = (query or '').strip()
    if not text:
        text = ("Voici une photo d'un exercice. Trouve les habiletés correspondantes."
                if lang == 'fr' else 'Here is a photo of an exercise. Find the matching skills.')
    content.append({'type': 'text', 'text': f'Description: {text}'})
    reply = llm.complete_json(system, content, max_tokens=800, temperature=0.1)
    results = reply.get('results', []) if isinstance(reply, dict) else reply
    valid = topic_meta()
    out, seen = [], set()
    for r in results or []:
        if not isinstance(r, dict):
            continue
        slug = str(r.get('slug', '')).strip()
        if slug not in valid or slug in seen:
            continue
        seen.add(slug)
        try:
            score = max(0.0, min(1.0, float(r.get('score', 0.5))))
        except (TypeError, ValueError):
            score = 0.5
        out.append({'slug': slug, 'score': round(score, 2), 'why': str(r.get('why', '')).strip()})
        if len(out) >= limit:
            break
    return out


def search_skills(query, lang='fr', image=None, limit=MAX_RESULTS):
    """Returns (results, engine) where engine is 'llm' or 'keyword'."""
    if llm.is_configured():
        try:
            return llm_search(query, lang, image=image, limit=limit), 'llm'
        except Exception:
            pass
    return keyword_search(query or '', lang, limit=limit), 'keyword'
