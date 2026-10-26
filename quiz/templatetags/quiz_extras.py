import json as _json
import re as _re
from django import template
from django.utils.html import escape as _escape
from django.utils.safestring import mark_safe
from quiz.geometry_utils import render_shapes as _render_shapes

register = template.Library()


@register.inclusion_tag('partials/shape_canvas.html')
def shape_canvas(shape_data, lang='en'):
    shapes = _render_shapes(shape_data or [])
    return {'shapes': shapes, 'count': len(shapes), 'lang': lang}


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(str(key))
    return None


@register.filter
def split_lines(value):
    """Split a \n-separated explanation into a list of non-empty lines."""
    if not value:
        return []
    return [line.strip() for line in str(value).split('\n') if line.strip()]


@register.filter
def to_json(value):
    """Serialize a Python value to a JSON string safe for inline JavaScript."""
    return mark_safe(_json.dumps(value))


@register.filter
def speech(value):
    """Plain text for read-aloud: drop **bold** markers."""
    return _re.sub(r'\*\*(.+?)\*\*', r'\1', str(value or ''))


@register.filter
def speech_choices(choices):
    """JSON list of the choice labels (multiple choice), read after the question."""
    import json
    labels = [str(c.get('label', '')) for c in (choices or []) if isinstance(c, dict)]
    return json.dumps(labels, ensure_ascii=False)        # autoescaping makes it attribute-safe


@register.filter
def md_bold(value):
    """Render **text** as <strong>text</strong>. Escapes HTML first for safety."""
    if not value:
        return value
    safe = _escape(str(value))
    result = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', safe)
    return mark_safe(result)


@register.filter
def percent(value, max_val):
    try:
        return round(int(value) / int(max_val) * 100)
    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
def ordinal_fr(n):
    """French school-grade ordinal: 1 → « 1re », 2 → « 2e »…"""
    try:
        n = int(n)
    except (TypeError, ValueError):
        return n
    return '1re' if n == 1 else f'{n}e'


@register.filter
def bars_layout(spec, lang='fr'):
    """Geometry of the tap-to-build bar chart (quiz/widgets.py)."""
    from quiz.widgets import bars_layout as _bars
    return _bars(spec or {}, lang)


@register.filter
def plane_layout(spec):
    """Geometry of the tap-to-place point grid (quiz/widgets.py)."""
    from quiz.widgets import plane_layout as _plane
    return _plane(spec or {})


@register.filter
def outcome_weights(outcomes):
    """Simulator outcome weights as a plain list for the browser."""
    return [float(o.get('w', 1)) for o in outcomes or []]
