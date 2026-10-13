"""
illustrations.py — picture builders for the ``canvas`` shape type.

Every builder returns a shape dict ``{'type': 'canvas', 'vw', 'vh', 'marks', 'labels'}``
whose coordinates are final: ``geometry_utils.render_shape`` passes them straight
to ``partials/shape_canvas.html``. Mark types understood by the template:
path (d, fill, stroke, sw) · line (x1..y2, color, sw, opacity, dash) · rect (x, y, w, h,
fill, stroke, sw, rx) · circle (cx, cy, r, fill, stroke, stroke_width) · dot (x, y, r, fill).
Labels: {x, y, text, size, anchor, bold, color} plus optional ``text_en`` (picked by
labels.localize_problem for English sessions).
"""
import math

INK = '#334155'
SOFT = '#94A3B8'
BLUE, RED, GREEN, AMBER, PURPLE, TEAL = '#2563EB', '#EF4444', '#16A34A', '#D97706', '#9333EA', '#0891B2'
PALETTE = [BLUE, RED, GREEN, AMBER, PURPLE, TEAL]
TINTS = {BLUE: '#DBEAFE', RED: '#FEE2E2', GREEN: '#DCFCE7', AMBER: '#FEF3C7', PURPLE: '#F3E8FF', TEAL: '#CFFAFE'}


def _r(v):
    return round(float(v), 1)


class Canvas:
    def __init__(self, w=300, h=200, max_h=None, css_w=None):
        self.w, self.h = w, h
        self.max_h, self.css_w = max_h, css_w
        self.marks, self.labels = [], []

    # primitives ------------------------------------------------------------
    def rect(self, x, y, w, h, fill='none', stroke=INK, sw=1.5, rx=0):
        self.marks.append(dict(type='rect', x=_r(x), y=_r(y), w=_r(w), h=_r(h), fill=fill, stroke=stroke, sw=sw, rx=rx))
        return self

    def line(self, x1, y1, x2, y2, color=INK, sw=2, opacity=1, dash=''):
        m = dict(type='line', x1=_r(x1), y1=_r(y1), x2=_r(x2), y2=_r(y2), color=color, sw=sw, opacity=opacity)
        if dash:
            m['dash'] = dash
        self.marks.append(m)
        return self

    def path(self, d, fill='none', stroke=INK, sw=2):
        self.marks.append(dict(type='path', d=d, fill=fill, stroke=stroke, sw=sw))
        return self

    def poly(self, pts, fill='none', stroke=INK, sw=2, closed=True):
        d = 'M ' + ' L '.join(f'{_r(x)},{_r(y)}' for x, y in pts) + (' Z' if closed else '')
        return self.path(d, fill, stroke, sw)

    def circle(self, cx, cy, r, fill='none', stroke=INK, sw=2):
        self.marks.append(dict(type='circle', cx=_r(cx), cy=_r(cy), r=_r(r), fill=fill, stroke=stroke, stroke_width=sw))
        return self

    def dot(self, x, y, r=4, fill=INK):
        self.marks.append(dict(type='dot', x=_r(x), y=_r(y), r=r, fill=fill))
        return self

    def text(self, x, y, text, size=13, anchor='middle', bold=False, color='#1E0A3C', text_en=None):
        lbl = dict(x=_r(x), y=_r(y), text=str(text), size=size, anchor=anchor, bold=bold, color=color)
        if text_en is not None:
            lbl['text_en'] = str(text_en)
        self.labels.append(lbl)
        return self

    def arc(self, cx, cy, r, a0, a1, stroke=INK, sw=2, fill='none'):
        """Arc from angle a0 to a1 (degrees, counter-clockwise, 0 = east)."""
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        large = 1 if (a1 - a0) % 360 > 180 else 0
        return self.path(f'M {_r(x0)},{_r(y0)} A {_r(r)},{_r(r)} 0 {large},0 {_r(x1)},{_r(y1)}', fill, stroke, sw)

    def shape(self):
        d = {'type': 'canvas', 'vw': self.w, 'vh': self.h, 'marks': self.marks, 'labels': self.labels}
        if self.max_h:
            d['max_h'] = self.max_h
        if self.css_w:
            d['css_w'] = self.css_w
        return d


# ── fractions ─────────────────────────────────────────────────────────────────

def fraction_bars(rows, w=300, row_h=34, gap=14, color=BLUE, labels=None):
    """
    One or more stacked bars of the same length. rows = [(coloured, parts), …].
    ``labels`` (optional) = text drawn left of each bar. No fraction is printed.
    """
    left = 46 if labels else 10
    bar_w = w - left - 10
    h = len(rows) * row_h + (len(rows) - 1) * gap + 16
    c = Canvas(w, h, max_h=min(60 * len(rows) + 20, 200), css_w='max-w-md')
    for r, (n, d) in enumerate(rows):
        y = 8 + r * (row_h + gap)
        part = bar_w / d
        for i in range(d):
            c.rect(left + i * part, y, part, row_h, fill=TINTS[color] if i >= n else color, stroke=INK, sw=1.5)
        if labels:
            c.text(left - 8, y + row_h / 2 + 5, labels[r], size=14, anchor='end', bold=True)
    return c.shape()


def fraction_circle(n, d, r=60, color=GREEN):
    c = Canvas(2 * r + 20, 2 * r + 20, max_h=150)
    cx = cy = r + 10
    if d == 1:
        c.circle(cx, cy, r, fill=color if n else TINTS[color], stroke=INK, sw=2)
        return c.shape()
    for i in range(d):
        a0 = math.pi / 2 - i * 2 * math.pi / d
        a1 = a0 - 2 * math.pi / d
        x0, y0 = cx + r * math.cos(a0), cy - r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
        large = 1 if d == 1 else 0
        c.path(f'M {cx},{cy} L {_r(x0)},{_r(y0)} A {r},{r} 0 {large},1 {_r(x1)},{_r(y1)} Z',
               fill=color if i < n else TINTS[color], stroke=INK, sw=1.5)
    return c.shape()


def collection(total, coloured, per_row=None, color=AMBER, icon='circle'):
    """A set of objects (circles or stars), ``coloured`` of them filled."""
    per_row = per_row or (total if total <= 6 else math.ceil(total / 2) if total <= 12 else math.ceil(total / 3))
    rows = math.ceil(total / per_row)
    cell = 34
    w, h = per_row * cell + 12, rows * cell + 12
    c = Canvas(w, h, max_h=min(40 * rows + 20, 160), css_w='max-w-xs')
    for i in range(total):
        x = 6 + (i % per_row) * cell + cell / 2
        y = 6 + (i // per_row) * cell + cell / 2
        fill = color if i < coloured else '#FFFFFF'
        if icon == 'star':
            pts = []
            for k in range(10):
                rr = 14 if k % 2 == 0 else 6
                a = math.pi / 2 + k * math.pi / 5
                pts.append((x + rr * math.cos(a), y - rr * math.sin(a)))
            c.poly(pts, fill=fill, stroke=INK, sw=1.5)
        else:
            c.circle(x, y, 13, fill=fill, stroke=INK, sw=1.8)
    return c.shape()
