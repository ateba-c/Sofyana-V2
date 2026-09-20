import json

from django.utils.safestring import mark_safe

from .taxonomy import skill_index


def student_context(request):
    if not request.user.is_authenticated:
        return {'student': None, 'parent_profile': None}
    try:
        student = request.user.student
    except Exception:
        student = None
    try:
        parent_profile = request.user.parent_profile
    except Exception:
        parent_profile = None
    return {'student': student, 'parent_profile': parent_profile}


def taxonomy_context(request):
    """Skill list for the search widget, straight from the DB taxonomy."""
    # json.dumps escapes '<' etc. only via ensure_ascii; force HTML-safe escapes
    # so the payload can never break out of the <script> tag.
    payload = json.dumps(skill_index(), ensure_ascii=False)
    payload = payload.replace('</', '<\\/').replace('<', '\\u003c').replace('>', '\\u003e')
    return {'skill_index_json': mark_safe(payload)}


def lang_context(request):
    """Session-sticky UI language for templates whose view does not pass one."""
    from .labels import resolve_lang
    return {'lang': resolve_lang(request)}
