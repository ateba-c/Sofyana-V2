"""
widgets.py — layout for the interactive answer widgets (curriculum workplan: D7.4 tap-to-build chart, C5.13
tap-to-place point). Generators describe *what* to build; this module computes the SVG geometry the template
loops over, and the static pictures shown in the feedback.

Question shapes:
    q_type 'build_bars'   q['bars']  = {'cats_fr': [...], 'cats_en': [...], 'top': 10, 'step': 1}
                          correct_answers = ['[4, 7, 3]']   (bar heights, JSON)
    q_type 'place_point'  q['plane'] = {'xmin': 0, 'xmax': 8, 'ymin': 0, 'ymax': 8, 'points': {'A': [1, 2]}}
                          correct_answers = ['(3, 5)'], answer_type 'coordinate'
"""
import json

from .answers import check_answer, parse_coordinate
from .illustrations import Canvas, BLUE, GREEN, RED, PURPLE, INK, SOFT

BAR_W, BAR_GAP, LEFT, TOP, BOTTOM = 46, 18, 34, 12, 40


def _minus(n):
    return f'−{abs(n)}' if n < 0 else str(n)


def bars_layout(spec, lang='fr'):
    cats = spec.get(f'cats_{lang}') or spec.get('cats_fr') or []
    top, step = int(spec.get('top', 10)), int(spec.get('step', 1))
    rows = top // step
    cell = max(14, min(26, 220 // max(rows, 1)))
    h = rows * cell
    vw = LEFT + len(cats) * (BAR_W + BAR_GAP) + BAR_GAP
    vh = TOP + h + BOTTOM
    base = TOP + h
    cols = []
    for i, label in enumerate(cats):
        x = LEFT + BAR_GAP + i * (BAR_W + BAR_GAP)
        cells = [{'v': (r + 1) * step, 'y': base - (r + 1) * cell, 'h': cell} for r in range(rows)]
        cols.append({'i': i, 'x': x, 'w': BAR_W, 'cx': x + BAR_W / 2, 'label': label, 'cells': cells})
    grid = [{'y': base - r * cell, 'v': r * step, 'label': r % max(1, rows // 5 or 1) == 0 or r == rows}
            for r in range(rows + 1)]
    return {'vw': vw, 'vh': vh, 'base': base, 'cell': cell, 'step': step, 'top': top, 'cols': cols, 'grid': grid,
            'right': vw - 6, 'label_y': base + 18, 'n': len(cats)}


def plane_layout(spec):
    x0, x1, y0, y1 = (int(spec.get(k)) for k in ('xmin', 'xmax', 'ymin', 'ymax'))
    cell = max(20, min(30, 300 // max(x1 - x0, y1 - y0)))
    pad = 26
    vw = (x1 - x0) * cell + 2 * pad
    vh = (y1 - y0) * cell + 2 * pad
    px = lambda x: pad + (x - x0) * cell
    py = lambda y: pad + (y1 - y) * cell
    nodes = [{'x': x, 'y': y, 'px': px(x), 'py': py(y), 'key': f'{x},{y}'}
             for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    vlines = [{'p': px(x), 'axis': x == 0} for x in range(x0, x1 + 1)]
    hlines = [{'p': py(y), 'axis': y == 0} for y in range(y0, y1 + 1)]
    ox, oy = px(max(x0, min(0, x1))), py(max(y0, min(0, y1)))
    xlabels = [{'p': px(x), 'text': _minus(x)} for x in range(x0, x1 + 1) if x != 0 or x0 == 0]
    ylabels = [{'p': py(y), 'text': _minus(y)} for y in range(y0, y1 + 1) if y != 0]
    points = [{'label': k, 'px': px(v[0]), 'py': py(v[1])} for k, v in (spec.get('points') or {}).items()]
    return {'vw': vw, 'vh': vh, 'cell': cell, 'nodes': nodes, 'vlines': vlines, 'hlines': hlines,
            'top': pad, 'bottom': vh - pad, 'left': pad, 'right': vw - pad, 'ox': ox, 'oy': oy,
            'xlabels': xlabels, 'ylabels': ylabels, 'points': points, 'xl_y': oy + 15, 'yl_x': ox - 5}


# ── checking ─────────────────────────────────────────────────────────────────

def check(q, answer):
    if q.get('q_type') == 'build_bars':
        try:
            got = [int(v) for v in json.loads(answer)]
            return got == json.loads(q['correct_answers'][0])
        except (ValueError, TypeError, KeyError, IndexError):
            return False
    if q.get('q_type') == 'place_point':
        return check_answer(answer, q.get('correct_answers', []), 'coordinate')
    return False


# ── feedback pictures ────────────────────────────────────────────────────────

def feedback_shape(q, answer, lang='fr'):
    """A static picture of the expected answer (and the child's, when different) for the feedback panel."""
    if q.get('q_type') == 'build_bars':
        lay = bars_layout(q['bars'], lang)
        want = json.loads(q['correct_answers'][0])
        try:
            got = [int(v) for v in json.loads(answer)]
        except (ValueError, TypeError):
            got = []
        c = Canvas(lay['vw'], lay['vh'], max_h=260, css_w='max-w-md')
        for g in lay['grid']:
            c.line(LEFT, g['y'], lay['right'], g['y'], color=SOFT, sw=1)
            if g['label']:
                c.text(LEFT - 6, g['y'] + 4, g['v'], size=10, anchor='end', bold=True)
        for col in lay['cols']:
            v = want[col['i']]
            hgt = v / lay['step'] * lay['cell']
            c.rect(col['x'], lay['base'] - hgt, col['w'], hgt, fill=GREEN, stroke='none', sw=0, rx=3)
            if col['i'] < len(got) and got[col['i']] != v:
                gy = lay['base'] - got[col['i']] / lay['step'] * lay['cell']
                c.line(col['x'] - 3, gy, col['x'] + col['w'] + 3, gy, color=RED, sw=3, dash='5 3')
            c.text(col['cx'], lay['base'] - hgt - 5, v, size=11, bold=True, color=GREEN)
            c.text(col['cx'], lay['label_y'], col['label'], size=11, bold=True)
        return c.shape()
    if q.get('q_type') == 'place_point':
        spec = q['plane']
        lay = plane_layout(spec)
        c = Canvas(lay['vw'], lay['vh'], max_h=320, css_w='max-w-sm')
        for ln in lay['vlines']:
            c.line(ln['p'], lay['top'], ln['p'], lay['bottom'], color=INK if ln['axis'] else SOFT, sw=2 if ln['axis'] else 1)
        for ln in lay['hlines']:
            c.line(lay['left'], ln['p'], lay['right'], ln['p'], color=INK if ln['axis'] else SOFT, sw=2 if ln['axis'] else 1)
        for t in lay['xlabels']:
            c.text(t['p'], lay['xl_y'], t['text'], size=10, bold=True)
        for t in lay['ylabels']:
            c.text(lay['yl_x'], t['p'] + 4, t['text'], size=10, bold=True, anchor='end')
        for p in lay['points']:
            c.dot(p['px'], p['py'], r=5, fill=PURPLE)
            c.text(p['px'] + 7, p['py'] - 7, p['label'], size=13, bold=True, color=PURPLE, anchor='start')
        want = parse_coordinate(q['correct_answers'][0])
        got = parse_coordinate(answer or '')
        if got and got != want:
            gx, gy = (lay['left'] + (float(got[0]) - spec['xmin']) * lay['cell'], lay['top'] + (spec['ymax'] - float(got[1])) * lay['cell'])
            c.circle(gx, gy, 8, fill='none', stroke=RED, sw=3)
        wx, wy = (lay['left'] + (float(want[0]) - spec['xmin']) * lay['cell'], lay['top'] + (spec['ymax'] - float(want[1])) * lay['cell'])
        c.dot(wx, wy, r=7, fill=GREEN)
        return c.shape()
    return None


# ── builders for generators ──────────────────────────────────────────────────

def place_point(prompt, target, hint, explanation, xmin=0, xmax=8, ymin=0, ymax=8, points=None, **extra):
    """Tap-to-place question: the child taps the node at ``target`` = (x, y)."""
    from .generators.kit import _base
    x, y = target
    key = f'({_minus(x)}, {_minus(y)})'
    q = _base('place_point', prompt, hint, explanation, [key, f'({x}, {y})'], None,
              plane={'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax,
                     'points': {k: list(v) for k, v in (points or {}).items()}},
              answer_type='coordinate', **extra)
    return q


def build_bars(prompt, cats, values, hint, explanation, top=None, step=1, shape=None, **extra):
    """Tap-to-build bar chart: ``cats`` are labels or (fr, en) pairs, ``values`` the expected heights."""
    from .generators.kit import _base
    top = top or max(values) + step
    fr = [c[0] if isinstance(c, tuple) else c for c in cats]
    en = [c[1] if isinstance(c, tuple) else c for c in cats]
    return _base('build_bars', prompt, hint, explanation, [json.dumps(list(values))], shape,
                 bars={'cats_fr': fr, 'cats_en': en, 'top': top, 'step': step}, **extra)
