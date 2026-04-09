import json as _json
from django import template
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
def percent(value, max_val):
    try:
        return round(int(value) / int(max_val) * 100)
    except (ValueError, ZeroDivisionError):
        return 0
