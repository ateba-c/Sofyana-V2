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
