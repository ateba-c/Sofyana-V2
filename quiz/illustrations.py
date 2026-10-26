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
import random

INK = '#334155'
SOFT = '#94A3B8'
BLUE, RED, GREEN, AMBER, PURPLE, TEAL = '#2563EB', '#EF4444', '#16A34A', '#D97706', '#9333EA', '#0891B2'
PALETTE = [BLUE, RED, GREEN, AMBER, PURPLE, TEAL]
TINTS = {BLUE: '#DBEAFE', RED: '#FEE2E2', GREEN: '#DCFCE7', AMBER: '#FEF3C7', PURPLE: '#F3E8FF', TEAL: '#CFFAFE'}
# light → dark shades used to light the faces of solids
SHADES = {BLUE: ('#EFF6FF', '#DBEAFE', '#BFDBFE'), RED: ('#FEF2F2', '#FEE2E2', '#FECACA'),
          GREEN: ('#F0FDF4', '#DCFCE7', '#BBF7D0'), AMBER: ('#FFFBEB', '#FEF3C7', '#FDE68A'),
          PURPLE: ('#FAF5FF', '#F3E8FF', '#E9D5FF'), TEAL: ('#ECFEFF', '#CFFAFE', '#A5F3FC')}
DASH = '4 3'


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

    def path(self, d, fill='none', stroke=INK, sw=2, dash=''):
        m = dict(type='path', d=d, fill=fill, stroke=stroke, sw=sw)
        if dash:
            m['dash'] = dash
        self.marks.append(m)
        return self

    def poly(self, pts, fill='none', stroke=INK, sw=2, closed=True, dash=''):
        d = 'M ' + ' L '.join(f'{_r(x)},{_r(y)}' for x, y in pts) + (' Z' if closed else '')
        return self.path(d, fill, stroke, sw, dash)

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


# ── decimals / number lines ──────────────────────────────────────────────────

def hundred_grid(shaded, size=10, color=BLUE, cell=16):
    """A size×size grid (10×10 → hundredths, 1 row → tenths) with ``shaded`` cells filled row by row."""
    rows = size if size == 10 else 1
    cols = 10
    c = Canvas(cols * cell + 8, rows * cell + 8, max_h=170 if rows > 1 else 50, css_w='max-w-xs')
    for i in range(rows * cols):
        x = 4 + (i % cols) * cell
        y = 4 + (i // cols) * cell
        c.rect(x, y, cell, cell, fill=color if i < shaded else '#FFFFFF', stroke=SOFT, sw=1)
    c.rect(4, 4, cols * cell, rows * cell, stroke=INK, sw=2)
    return c.shape()


def number_line(majors, minor=0, point=None, w=320, mark='?', point_color=BLUE):
    """
    majors: labels at evenly spaced major ticks — each a str or (fr, en).
    minor:  number of sub-intervals between two majors.
    point:  position of the marked point in minor steps from the first major.
    """
    c = Canvas(w, 74, max_h=90, css_w='max-w-md')
    x0, x1, y = 18, w - 18, 38
    c.line(x0, y, x1, y, sw=2.5, opacity=1)
    seg = (x1 - x0) / (len(majors) - 1)
    for i, lab in enumerate(majors):
        x = x0 + i * seg
        c.line(x, y - 9, x, y + 9, sw=2.5, opacity=1)
        fr, en = (lab, None) if not isinstance(lab, tuple) else lab
        c.text(x, y + 26, fr, size=13, bold=True, text_en=en)
        if minor and i < len(majors) - 1:
            for k in range(1, minor):
                xm = x + k * seg / minor
                c.line(xm, y - 5, xm, y + 5, sw=1.5, opacity=1)
    if point is not None:
        xp = x0 + point * seg / (minor or 1)
        c.dot(xp, y, r=6, fill=point_color)
        c.text(xp, y - 14, mark, size=15, bold=True, color=point_color)
    return c.shape()


# ── operations ───────────────────────────────────────────────────────────────

def dot_array(rows, cols, color=RED, split_col=None):
    """rows × cols dots; ``split_col`` colours the columns after it blue and draws a dashed cut (distributivity)."""
    cell = 22 if max(rows, cols) <= 10 else 16
    w, h = cols * cell + 16, rows * cell + 16
    c = Canvas(w, h, max_h=min(rows * 24 + 30, 190), css_w='max-w-sm' if cols > 10 else 'max-w-xs')
    for r in range(rows):
        for k in range(cols):
            col = color if split_col is None or k < split_col else BLUE
            c.circle(8 + k * cell + cell / 2, 8 + r * cell + cell / 2, cell * 0.32, fill=col, stroke=col, sw=1)
    if split_col:
        x = 8 + split_col * cell
        c.line(x, 2, x, h - 2, color=INK, sw=2, dash='5 4')
    return c.shape()


def factor_tree(tree, hide=None):
    """
    tree: int (leaf) or (value, left, right). ``hide`` = a value to replace by « ? »
    (first occurrence, searched top-down). Prime leaves are circled.
    """
    def leaves(t):
        return 1 if isinstance(t, int) else leaves(t[1]) + leaves(t[2])

    def depth(t):
        return 1 if isinstance(t, int) else 1 + max(depth(t[1]), depth(t[2]))

    n_leaves, dep = leaves(tree), depth(tree)
    w, h = max(160, n_leaves * 56), dep * 58 + 10
    c = Canvas(w, h, max_h=min(dep * 60 + 20, 220), css_w='max-w-sm')
    hidden = [False]

    def draw(t, x0, x1, y):
        val = t if isinstance(t, int) else t[0]
        x = (x0 + x1) / 2
        if not isinstance(t, int):
            nl = leaves(t[1])
            total = leaves(t)
            xm = x0 + (x1 - x0) * nl / total
            for (a, b, child) in ((x0, xm, t[1]), (xm, x1, t[2])):
                c.line(x, y + 10, (a + b) / 2, y + 40, color=SOFT, sw=2)
                draw(child, a, b, y + 58)
        label = str(val)
        if hide is not None and val == hide and not hidden[0]:
            hidden[0] = True
            label = '?'
        if isinstance(t, int):
            c.circle(x, y - 4, 15, fill=TINTS[GREEN], stroke=GREEN, sw=2)
        c.text(x, y + 1, label, size=15, bold=True, color=PURPLE if label == '?' else '#1E0A3C')

    draw(tree, 0, w, 22)
    return c.shape()


# ── geometry: panels ─────────────────────────────────────────────────────────

LETTERS = 'ABCDEFGH'


def panels(n, cell_w=110, cell_h=110, cols=None, letters=True, css_w='max-w-lg'):
    """
    A canvas split into ``n`` boxes (rows of ``cols``), each with a letter under it.
    ``letters`` may also be a list of labels (str or (fr, en)), one per box.
    Returns (canvas, boxes) where boxes[i] = (x0, y0, w, h) is the drawing area of box i.
    """
    cols = cols or (n if n <= 3 else math.ceil(n / 2))
    rows = math.ceil(n / cols)
    lab_h = 22 if letters else 0
    names = letters if isinstance(letters, (list, tuple)) else LETTERS
    w, h = cols * cell_w, rows * (cell_h + lab_h)
    c = Canvas(w, h, max_h=min(rows * 150, 300), css_w=css_w)
    boxes = []
    for i in range(n):
        r, k = divmod(i, cols)
        in_row = cols if r < rows - 1 else n - r * cols     # centre a short last row
        x0 = k * cell_w + (cols - in_row) * cell_w / 2
        y0 = r * (cell_h + lab_h)
        boxes.append((x0 + 6, y0 + 6, cell_w - 12, cell_h - 12))
        if letters:
            fr, en = names[i] if isinstance(names[i], tuple) else (names[i], None)
            c.text(x0 + cell_w / 2, y0 + cell_h + 14, fr, size=15 if len(fr) == 1 else 13, bold=True,
                   color=PURPLE if len(fr) == 1 else INK, text_en=en)
    return c, boxes


def _fit(pts, box, pad=4):
    """Scale and centre a list of point lists (screen coords) into box = (x0, y0, w, h)."""
    xs = [x for poly in pts for x, _ in poly]
    ys = [y for poly in pts for _, y in poly]
    bw, bh = (max(xs) - min(xs)) or 1, (max(ys) - min(ys)) or 1
    x0, y0, w, h = box
    k = min((w - 2 * pad) / bw, (h - 2 * pad) / bh)
    ox = x0 + (w - bw * k) / 2 - min(xs) * k
    oy = y0 + (h - bh * k) / 2 - min(ys) * k
    return [[(ox + x * k, oy + y * k) for x, y in poly] for poly in pts], k


# ── geometry: solids (orthographic view from above-right) ────────────────────

def _ngon(n, r=1.0, start=None):
    start = (math.pi / 2 if n % 2 else math.pi / n + math.pi / 2) if start is None else start
    return [(r * math.cos(start + 2 * math.pi * i / n), r * math.sin(start + 2 * math.pi * i / n)) for i in range(n)]


def _base(kind):
    """Base polygon (x, z) and height of a prism/pyramid kind."""
    if kind == 'cube':
        return [(-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5)], 1.0
    if kind == 'rect-prism':
        return [(-.85, -.45), (.85, -.45), (.85, .45), (-.85, .45)], 0.9
    n = {'tri': 3, 'square': 4, 'pent': 5, 'hex': 6}[kind.split('-')[0]]
    return _ngon(n, 0.75, start=-math.pi / 2 + (0.35 if n == 3 else 0.2)), 1.25


def _mesh(kind):
    base, h = _base(kind)
    n = len(base)
    if kind.endswith('pyramid'):
        verts = [(x, 0, z) for x, z in base] + [(0, h, 0)]
        faces = [list(range(n))] + [[i, (i + 1) % n, n] for i in range(n)]
    else:
        verts = [(x, 0, z) for x, z in base] + [(x, h, z) for x, z in base]
        faces = [list(range(n)), list(range(n, 2 * n))] + [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return verts, faces


def _rot(p, yaw=-0.55, pitch=0.42):
    x, y, z = p
    x1 = x * math.cos(yaw) + z * math.sin(yaw)
    z1 = -x * math.sin(yaw) + z * math.cos(yaw)
    y2 = y * math.cos(pitch) - z1 * math.sin(pitch)
    z2 = y * math.sin(pitch) + z1 * math.cos(pitch)
    return x1, y2, z2


def draw_solid(c, kind, box, color=BLUE, hidden=True):
    """Draw a solid in ``box``. Polyhedra: cube, rect-prism, tri/square/pent/hex-prism and -pyramid.
    Curved: cylinder, cone, sphere. Hidden edges are dashed."""
    if kind in ('cylinder', 'cone', 'sphere'):
        return _draw_round(c, kind, box, color)
    light, mid, dark = SHADES[color]
    verts, faces = _mesh(kind)
    R = [_rot(v) for v in verts]
    (fitted,), _k = _fit([[(x, -y) for x, y, _ in R]], box, pad=6)
    cen = [sum(v[i] for v in R) / len(R) for i in range(3)]
    vis = []
    for f in faces:
        a, b, cc = R[f[0]], R[f[1]], R[f[2]]
        u = [b[i] - a[i] for i in range(3)]
        v = [cc[i] - a[i] for i in range(3)]
        nrm = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        fc = [sum(R[j][i] for j in f) / len(f) for i in range(3)]
        if sum(nrm[i] * (fc[i] - cen[i]) for i in range(3)) < 0:
            nrm = [-x for x in nrm]
        ln = math.sqrt(sum(x * x for x in nrm)) or 1
        vis.append((nrm[2] / ln > 1e-6, nrm[1] / ln, f))
    edges = {}
    for visible, _ny, f in vis:
        for i in range(len(f)):
            e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
            edges[e] = edges.get(e, False) or visible
    for visible, ny, f in vis:
        if visible:
            fill = light if ny > 0.5 else mid if ny > -0.2 else dark
            c.poly([fitted[j] for j in f], fill=fill, stroke='none', sw=0)
    if hidden:
        for (i, j), visible in edges.items():
            if not visible:
                c.line(*fitted[i], *fitted[j], color=SOFT, sw=1.6, dash=DASH)
    for (i, j), visible in edges.items():
        if visible:
            c.line(*fitted[i], *fitted[j], color=INK, sw=2.2)
    return c


def _ellipse_half(cx, cy, rx, ry, front):
    """Lower (front=True) or upper half of an ellipse, from left to right."""
    sweep = 0 if front else 1
    return f'M {_r(cx - rx)},{_r(cy)} A {_r(rx)},{_r(ry)} 0 0,{sweep} {_r(cx + rx)},{_r(cy)}'


def _draw_round(c, kind, box, color):
    light, mid, dark = SHADES[color]
    x0, y0, w, h = box
    cx = x0 + w / 2
    if kind == 'sphere':
        r = min(w, h) / 2 - 6
        cy = y0 + h / 2
        c.circle(cx, cy, r, fill=mid, stroke=INK, sw=2.2)
        c.circle(cx - r * .35, cy - r * .35, r * .22, fill=light, stroke='none', sw=0)
        c.path(_ellipse_half(cx, cy, r, r * 0.3, True), stroke=INK, sw=1.6)
        c.path(_ellipse_half(cx, cy, r, r * 0.3, False), stroke=SOFT, sw=1.4, dash=DASH)
        return c
    r = min(w * 0.38, h * 0.36)
    ry = r * 0.36
    top, bot = y0 + 8 + ry, y0 + h - 8 - ry
    front_bot = _ellipse_half(cx, bot, r, ry, True)[len(f'M {_r(cx - r)},{_r(bot)} '):]
    if kind == 'cylinder':
        body = f'M {_r(cx - r)},{_r(top)} L {_r(cx - r)},{_r(bot)} {front_bot} L {_r(cx + r)},{_r(top)}'
        c.path(body + ' Z', fill=mid, stroke='none', sw=0)
        c.path(_ellipse_half(cx, bot, r, ry, False), stroke=SOFT, sw=1.4, dash=DASH)
        c.path(body, stroke=INK, sw=2.2)
        c.path(f'M {_r(cx - r)},{_r(top)} A {_r(r)},{_r(ry)} 0 1,1 {_r(cx + r)},{_r(top)} '
               f'A {_r(r)},{_r(ry)} 0 1,1 {_r(cx - r)},{_r(top)} Z', fill=light, stroke=INK, sw=2.2)
        return c
    # cone, apex on top
    body = f'M {_r(cx)},{_r(y0 + 6)} L {_r(cx - r)},{_r(bot)} {front_bot} Z'
    c.path(body, fill=mid, stroke='none', sw=0)
    c.path(_ellipse_half(cx, bot, r, ry, False), stroke=SOFT, sw=1.4, dash=DASH)
    c.path(body, stroke=INK, sw=2.2)
    return c


def solid(kind, color=BLUE, size=150):
    c = Canvas(size, size, max_h=170, css_w='max-w-[11rem]')
    draw_solid(c, kind, (0, 0, size, size), color)
    return c.shape()


# ── geometry: nets ───────────────────────────────────────────────────────────

def _outward(p, q, ref):
    """Unit normal of segment p→q pointing away from ref."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    if (mx - ref[0]) * nx + (my - ref[1]) * ny < 0:
        nx, ny = -nx, -ny
    return nx, ny


def _centroid(poly):
    return sum(x for x, _ in poly) / len(poly), sum(y for _, y in poly) / len(poly)


def _on_edge_rect(p, q, depth, ref):
    nx, ny = _outward(p, q, ref)
    return [p, q, (q[0] + nx * depth, q[1] + ny * depth), (p[0] + nx * depth, p[1] + ny * depth)]


def _on_edge_tri(p, q, height, ref):
    nx, ny = _outward(p, q, ref)
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    return [p, q, (m[0] + nx * height, m[1] + ny * height)]


def _on_edge_ngon(p, q, n, ref):
    """Regular n-gon built on segment p→q, on the side away from ref."""
    side = math.hypot(q[0] - p[0], q[1] - p[1])
    nx, ny = _outward(p, q, ref)
    ap = side / (2 * math.tan(math.pi / n))
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    ctr = (m[0] + nx * ap, m[1] + ny * ap)
    R = side / (2 * math.sin(math.pi / n))
    a0 = math.atan2(p[1] - ctr[1], p[0] - ctr[0])
    return [(ctr[0] + R * math.cos(a0 + 2 * math.pi * i / n), ctr[1] + R * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]


# Six squares that do NOT fold into a cube (distractors).
_BAD_CUBES = [
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1)],
]


def net_polys(kind, variant=0):
    """
    Faces of the net of ``kind`` as polygons (unit coords, y down).
    cube / rect-prism: variant 0 = cross, 1 = T-shape, 2 = zig-zag lids.
    Non-folding nets (distractors): 'bad-cube' (variants 0–2) and 'bad-pyramid' (a face missing).
    """
    if kind == 'bad-cube':
        return [[(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)] for x, y in _BAD_CUBES[variant % 3]]
    if kind in ('cube', 'rect-prism'):
        l, wd, h = (1, 1, 1) if kind == 'cube' else (1.6, 0.8, 1)
        polys, x = [], 0
        for wv in (l, wd, l, wd):
            polys.append([(x, 0), (x + wv, 0), (x + wv, h), (x, h)])
            x += wv
        top_i, bot_i = [(0, 0), (2, 0), (0, 2)][variant % 3]
        a, b = polys[top_i], polys[bot_i]
        polys.append(_on_edge_rect(a[0], a[1], wd, _centroid(a)))
        polys.append(_on_edge_rect(b[3], b[2], wd, _centroid(b)))
        return polys
    if kind == 'bad-pyramid':
        base = [(0, 0), (1, 0), (1, 1), (0, 1)]
        ctr = _centroid(base)
        return [base] + [_on_edge_tri(base[i], base[(i + 1) % 4], 0.9, ctr) for i in range(3)]
    n = {'tri': 3, 'square': 4, 'pent': 5, 'hex': 6}[kind.split('-')[0]]
    if kind.endswith('prism'):
        h = 1.6
        polys = [[(i, 0), (i + 1, 0), (i + 1, h), (i, h)] for i in range(n)]
        k = n // 2 if n > 3 else 1
        a = polys[k]
        b = polys[k if variant % 2 == 0 else 0]
        polys.append(_on_edge_ngon(a[0], a[1], n, _centroid(a)))
        polys.append(_on_edge_ngon(b[3], b[2], n, _centroid(b)))
        return polys
    if kind.endswith('pyramid'):
        base = _ngon(n, 0.7 if n == 3 else 0.6)
        ctr = _centroid(base)
        side = math.hypot(base[1][0] - base[0][0], base[1][1] - base[0][1])
        ht = side * (0.87 if n == 3 else 1.0 if n == 4 else 1.15)
        return [base] + [_on_edge_tri(base[i], base[(i + 1) % n], ht, ctr) for i in range(n)]
    raise ValueError(kind)


def draw_net(c, kind, box, color=BLUE, variant=0):
    light, mid, _ = SHADES[color]
    x0, y0, w, h = box
    if kind == 'cylinder':
        r = min(w / 5.2, h / 6.6)                    # rectangle 2.4 r high + two circles
        rw, rh = 2 * math.pi * r * 0.75, 2.4 * r
        rx, ry = x0 + (w - rw) / 2, y0 + (h - rh) / 2
        c.rect(rx, ry, rw, rh, fill=mid, stroke=INK, sw=2)
        c.circle(rx + rw / 2, ry - r, r, fill=light, stroke=INK, sw=2)
        c.circle(rx + rw / 2, ry + rh + r, r, fill=light, stroke=INK, sw=2)
        return c
    if kind == 'cone':
        R = min(w * 0.42, h * 0.5)
        cx, cy = x0 + w / 2, y0 + 4
        a0, a1 = 235, 305           # sector opening downward
        p0 = (cx + R * math.cos(math.radians(a0)), cy - R * math.sin(math.radians(a0)))
        p1 = (cx + R * math.cos(math.radians(a1)), cy - R * math.sin(math.radians(a1)))
        c.path(f'M {_r(cx)},{_r(cy)} L {_r(p0[0])},{_r(p0[1])} A {_r(R)},{_r(R)} 0 0,0 {_r(p1[0])},{_r(p1[1])} Z',
               fill=mid, stroke=INK, sw=2)
        rr = min(R * (a1 - a0) / 360 * 1.6, (y0 + h - (cy + R)) / 2.1)
        c.circle(cx, cy + R + rr, rr, fill=light, stroke=INK, sw=2)
        return c
    fitted, _ = _fit(net_polys(kind, variant), box, pad=4)
    for i, poly in enumerate(fitted):
        c.poly(poly, fill=mid if i % 2 else light, stroke=INK, sw=1.8)
    return c


def net(kind, color=BLUE, variant=0, w=220, h=170):
    c = Canvas(w, h, max_h=180, css_w='max-w-xs')
    draw_net(c, kind, (0, 0, w, h), color, variant)
    return c.shape()


# ── geometry: polygons, triangles, circles ──────────────────────────────────

def draw_polygon(c, pts, box, color=BLUE, fill=True):
    (fitted,), _ = _fit([pts], box, pad=6)
    c.poly(fitted, fill=SHADES[color][1] if fill else 'none', stroke=INK, sw=2.2)
    return fitted


def _tick(c, p, q, n):
    """n small tick marks across the middle of segment p–q (equal sides)."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy) or 1
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    for i in range(n):
        o = (i - (n - 1) / 2) * 5
        cx, cy = mx + ux * o, my + uy * o
        c.line(cx - nx * 6, cy - ny * 6, cx + nx * 6, cy + ny * 6, color=INK, sw=2)


def _right_mark(c, v, a, b, s=11):
    """Small square at vertex v between rays v→a and v→b."""
    def unit(p):
        dx, dy = p[0] - v[0], p[1] - v[1]
        ln = math.hypot(dx, dy) or 1
        return dx / ln, dy / ln
    u, w = unit(a), unit(b)
    c.poly([(v[0] + u[0] * s, v[1] + u[1] * s), (v[0] + (u[0] + w[0]) * s, v[1] + (u[1] + w[1]) * s),
            (v[0] + w[0] * s, v[1] + w[1] * s)], closed=False, stroke=INK, sw=1.6)


def triangle(pts, ticks=None, right_at=None, color=BLUE, labels=None, size=(200, 160)):
    """
    pts: 3 vertices (y down). ticks: {edge index: tick count} (edge i = pts[i]→pts[i+1]).
    right_at: vertex index with a right-angle mark. labels: optional edge labels (str or (fr, en)).
    """
    c = Canvas(*size, max_h=170, css_w='max-w-xs')
    f = draw_polygon(c, pts, (16, 16, size[0] - 32, size[1] - 32), color)
    for i, n in (ticks or {}).items():
        _tick(c, f[i], f[(i + 1) % 3], n)
    if right_at is not None:
        _right_mark(c, f[right_at], f[(right_at + 1) % 3], f[(right_at + 2) % 3])
    if labels:
        ctr = _centroid(f)
        for i, lab in enumerate(labels):
            if lab:
                p, q = f[i], f[(i + 1) % 3]
                nx, ny = _outward(p, q, ctr)
                fr, en = (lab, None) if not isinstance(lab, tuple) else lab
                c.text((p[0] + q[0]) / 2 + nx * 14, (p[1] + q[1]) / 2 + ny * 14 + 5, fr, size=13, bold=True, text_en=en)
    return c.shape()


def circle_parts(part, r=62, color=BLUE, value=None, angle=70):
    """
    A circle with its centre O and one highlighted part: 'radius', 'diameter', 'chord',
    'circumference', 'central-angle'. ``value`` (optional) labels the highlighted length.
    """
    size = 2 * r + 40
    c = Canvas(size, size, max_h=180, css_w='max-w-[12rem]')
    cx = cy = size / 2
    light = SHADES[color][1]
    hi = RED

    def pt(deg):
        return cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg))

    ring = part == 'circumference'
    c.circle(cx, cy, r, fill=light, stroke=hi if ring else INK, sw=4.5 if ring else 2.2)
    lab_at = None
    if part == 'radius':
        p = pt(30)
        c.line(cx, cy, *p, color=hi, sw=3.5)
        lab_at = ((cx + p[0]) / 2 - 4, (cy + p[1]) / 2 - 9)
    elif part == 'diameter':
        p, q = pt(20), pt(200)
        c.line(*q, *p, color=hi, sw=3.5)
        lab_at = (cx + r * 0.45, cy - r * 0.45)        # above the right half of the line
    elif part == 'chord':
        p, q = pt(140), pt(40)
        c.line(*p, *q, color=hi, sw=3.5)
        lab_at = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 - 9)
    elif part == 'central-angle':
        c.line(cx, cy, *pt(10), color=INK, sw=2.2)
        c.line(cx, cy, *pt(10 + angle), color=INK, sw=2.2)
        c.arc(cx, cy, 20, 10, 10 + angle, stroke=hi, sw=3.5)
    c.dot(cx, cy, r=3.5, fill=INK)
    c.text(cx - 6, cy + 18, 'O', size=13, bold=True)
    if value and lab_at:
        c.text(*lab_at, value, size=13, bold=True, color=hi)
    return c.shape()


# ── geometry: square grids (symmetry, translation, area, maps) ──────────────

def draw_grid(c, box, cols, rows, cells=None, cell=None, axis=None, arrow=None,
              col_labels=None, row_labels=None, icons=None, points=None, axes_numbers=False):
    """
    Square grid in box. cells: {(col, row): colour} filled squares (row 0 = top).
    axis: ('v', grid line) or ('h', grid line) — dashed red line of symmetry.
    arrow: ((c0, r0), (c1, r1)) translation arrow between grid nodes (row 0 = top).
    icons: {(col, row): text}. points: {(x, y): label} on nodes, y counted from the bottom.
    axes_numbers: number the nodes 0…cols / 0…rows along the bottom and left (first quadrant).
    Returns (cell, gx, gy).
    """
    x0, y0, w, h = box
    lab = 18 if (col_labels or row_labels or axes_numbers) else 0
    cell = cell or min((w - lab) / cols, (h - lab) / rows)
    gx = x0 + lab + (w - lab - cols * cell) / 2
    gy = y0 + (h - lab - rows * cell) / 2
    for (k, r), col in (cells or {}).items():
        c.rect(gx + k * cell, gy + r * cell, cell, cell, fill=col, stroke='none', sw=0)
    for k in range(cols + 1):
        c.line(gx + k * cell, gy, gx + k * cell, gy + rows * cell, color=SOFT, sw=1, opacity=0.9)
    for r in range(rows + 1):
        c.line(gx, gy + r * cell, gx + cols * cell, gy + r * cell, color=SOFT, sw=1, opacity=0.9)
    if axes_numbers:
        c.line(gx, gy + rows * cell, gx + cols * cell + 8, gy + rows * cell, color=INK, sw=2)
        c.line(gx, gy + rows * cell, gx, gy - 8, color=INK, sw=2)
        for k in range(cols + 1):
            c.text(gx + k * cell, gy + rows * cell + 15, str(k), size=11, bold=True)
        for r in range(1, rows + 1):
            c.text(gx - 6, gy + (rows - r) * cell + 4, str(r), size=11, bold=True, anchor='end')
    if col_labels:
        for k, t in enumerate(col_labels):
            c.text(gx + k * cell + cell / 2, gy + rows * cell + 15, t, size=12, bold=True)
    if row_labels:
        for r, t in enumerate(row_labels):
            c.text(gx - 6, gy + r * cell + cell / 2 + 4, t, size=12, bold=True, anchor='end')
    for (k, r), t in (icons or {}).items():
        c.text(gx + k * cell + cell / 2, gy + r * cell + cell * 0.72, t, size=round(cell * 0.62))
    if axis:
        if axis[0] == 'v':
            x = gx + axis[1] * cell
            c.line(x, gy - 6, x, gy + rows * cell + 6, color=RED, sw=2.6, dash='6 4')
        else:
            y = gy + axis[1] * cell
            c.line(gx - 6, y, gx + cols * cell + 6, y, color=RED, sw=2.6, dash='6 4')
    if arrow:
        (a0, b0), (a1, b1) = arrow
        X0, Y0, X1, Y1 = gx + a0 * cell, gy + b0 * cell, gx + a1 * cell, gy + b1 * cell
        c.line(X0, Y0, X1, Y1, color=GREEN, sw=3)
        ang = math.atan2(Y1 - Y0, X1 - X0)
        for s in (0.45, -0.45):
            c.line(X1, Y1, X1 - 11 * math.cos(ang + s), Y1 - 11 * math.sin(ang + s), color=GREEN, sw=3)
        c.dot(X0, Y0, r=3.5, fill=GREEN)
    for (px, py), t in (points or {}).items():
        X, Y = gx + px * cell, gy + (rows - py) * cell
        c.dot(X, Y, r=4.5, fill=PURPLE)
        c.text(X + 8, Y - 6, t, size=13, bold=True, color=PURPLE, anchor='start')
    return cell, gx, gy


def grid(cols, rows, cell=22, **kw):
    lab = 18 if (kw.get('col_labels') or kw.get('row_labels') or kw.get('axes_numbers')) else 0
    w, h = cols * cell + lab + 12, rows * cell + lab + 12
    c = Canvas(w, h, max_h=min(rows * cell + 50, 240), css_w='max-w-sm')
    draw_grid(c, (6, 6, w - 12, h - 12), cols, rows, cell=cell, **kw)
    return c.shape()


# ── measurement: ruler ───────────────────────────────────────────────────────

def ruler(cm, start_mm, length_mm, mm_ticks=True, color=AMBER, obj='pencil'):
    """
    A ruler 0…cm with an object (pencil or ribbon) lying from start_mm to start_mm + length_mm.
    """
    unit = 300 / max(cm, 1)
    w = cm * unit + 40
    c = Canvas(w, 104, max_h=120, css_w='max-w-lg')
    x0, ry = 20, 50
    # object above the ruler
    xa, xb = x0 + start_mm / 10 * unit, x0 + (start_mm + length_mm) / 10 * unit
    if obj == 'pencil':
        tip = min(14, (xb - xa) * 0.25)
        c.poly([(xa, 22), (xb - tip, 22), (xb, 32), (xb - tip, 42), (xa, 42)], fill=SHADES[color][2], stroke=INK, sw=1.8)
        c.poly([(xb - tip, 22), (xb, 32), (xb - tip, 42)], fill='#FDE68A', stroke=INK, sw=1.5)
        c.rect(xa, 22, min(8, (xb - xa) * 0.15), 20, fill='#FCA5A5', stroke=INK, sw=1.5)
    else:
        c.rect(xa, 26, xb - xa, 14, fill=SHADES[color][2], stroke=INK, sw=1.8, rx=2)
    c.line(xa, 18, xa, ry, color=SOFT, sw=1, dash='3 3')
    c.line(xb, 18, xb, ry, color=SOFT, sw=1, dash='3 3')
    # ruler body
    c.rect(x0 - 10, ry, cm * unit + 20, 46, fill='#FEF9C3', stroke=INK, sw=1.8, rx=4)
    for k in range(cm * 10 + 1):
        x = x0 + k / 10 * unit
        if k % 10 == 0:
            c.line(x, ry, x, ry + 18, color=INK, sw=1.8)
            c.text(x, ry + 33, str(k // 10), size=12, bold=True)
        elif k % 5 == 0 and mm_ticks:
            c.line(x, ry, x, ry + 12, color=INK, sw=1.2)
        elif mm_ticks:
            c.line(x, ry, x, ry + 7, color=INK, sw=0.9)
    c.text(x0 + cm * unit, ry + 44, 'cm', size=10, anchor='end', color=SOFT)
    return c.shape()


# ── measurement: cube stacks (isometric) ────────────────────────────────────

def cube_stack(heights, color=BLUE, unit=26):
    """
    heights[y][x] = number of unit cubes in the tower at (x, y); y = 0 is the back row.
    Isometric view, painter's order by depth (x + y + z).
    """
    light, mid, dark = SHADES[color]
    cx, sy = unit * 0.866, unit * 0.5

    def P(x, y, z):
        return (x - y) * cx, (x + y) * sy - z * unit

    # row 0 = back (small y); the viewer sits on the +x, +y, +z side: depth = x + y + z
    cubes = [(x, y, z) for y, row in enumerate(heights) for x, hgt in enumerate(row) for z in range(hgt)]
    pts = [P(x + a, y + b, z + cz) for x, y, z in cubes for a in (0, 1) for b in (0, 1) for cz in (0, 1)] or [(0, 0)]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    w, h = maxx - minx + 16, maxy - miny + 16
    c = Canvas(w, h, max_h=min(h + 10, 200), css_w='max-w-xs')
    ox, oy = 8 - minx, 8 - miny

    def Q(x, y, z):
        px, py = P(x, y, z)
        return px + ox, py + oy

    for x, y, z in sorted(cubes, key=lambda t: (t[0] + t[1] + t[2], t[2])):
        top = [Q(x, y, z + 1), Q(x + 1, y, z + 1), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)]
        left = [Q(x, y + 1, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)]
        right = [Q(x + 1, y, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x + 1, y, z + 1)]
        c.poly(left, fill=mid, stroke=INK, sw=1.4)
        c.poly(right, fill=dark, stroke=INK, sw=1.4)
        c.poly(top, fill=light, stroke=INK, sw=1.4)
    return c.shape()


# ── measurement: angles and protractor ──────────────────────────────────────

def draw_angle(c, box, degrees, ray=1.0, rot=0, color=BLUE, arc=True):
    """An angle of ``degrees`` with its vertex placed so the figure fits in box; ``ray`` scales the rays (0.4–1)."""
    x0, y0, w, h = box
    R = min(w, h) * 0.8 * ray
    a0, a1 = math.radians(rot), math.radians(rot + degrees)
    p0 = (R * math.cos(a0), -R * math.sin(a0))
    p1 = (R * math.cos(a1), -R * math.sin(a1))
    xs, ys = [0, p0[0], p1[0]], [0, p0[1], p1[1]]
    vx = x0 + (w - (max(xs) - min(xs))) / 2 - min(xs)
    vy = y0 + (h - (max(ys) - min(ys))) / 2 - min(ys)
    c.line(vx, vy, vx + p0[0], vy + p0[1], color=INK, sw=2.4)
    c.line(vx, vy, vx + p1[0], vy + p1[1], color=INK, sw=2.4)
    if arc:
        if abs(degrees - 90) < 0.5:
            _right_mark(c, (vx, vy), (vx + p0[0], vy + p0[1]), (vx + p1[0], vy + p1[1]), s=10)
        else:
            c.arc(vx, vy, 14, rot, rot + degrees, stroke=color, sw=2.4)
    c.dot(vx, vy, r=3, fill=INK)
    return c


def protractor(degrees, base_left=False, show_inner=False, color=RED):
    """
    A protractor with an angle whose vertex is at the centre. One ray lies on the 0° line
    (right side, or left side when ``base_left``). Outer scale counts from the right.
    """
    R = 120
    c = Canvas(2 * R + 40, R + 46, max_h=190, css_w='max-w-sm')
    cx, cy = R + 20, R + 22
    c.path(f'M {cx - R},{cy} A {R},{R} 0 0,1 {cx + R},{cy} Z', fill='#EFF6FF', stroke=INK, sw=1.8)
    for d in range(0, 181):
        a = math.radians(d)
        cos, sin = math.cos(a), math.sin(a)
        ln = 14 if d % 10 == 0 else 9 if d % 5 == 0 else 5
        c.line(cx + R * cos, cy - R * sin, cx + (R - ln) * cos, cy - (R - ln) * sin, color=INK, sw=1 if d % 10 else 1.4)
        if d % 10 == 0:
            c.text(cx + (R - 24) * cos, cy - (R - 24) * sin + 4, str(d), size=9, bold=True)
            if show_inner:
                c.text(cx + (R - 40) * cos, cy - (R - 40) * sin + 4, str(180 - d), size=8, color=SOFT)
    c.line(cx - R, cy, cx + R, cy, color=INK, sw=1.4)
    c.dot(cx, cy, r=3.5, fill=INK)
    start = 180 if base_left else 0
    end = 180 - degrees if base_left else degrees
    for d in (start, end):
        a = math.radians(d)
        c.line(cx, cy, cx + (R + 14) * math.cos(a), cy - (R + 14) * math.sin(a), color=color, sw=3)
    lo, hi_ = sorted((start, end))
    c.arc(cx, cy, 22, lo, hi_, stroke=color, sw=2.5)
    return c.shape()


# ── measurement: balance scale, measuring jug ───────────────────────────────

def balance(left, right, tilt=0):
    """
    Two-pan balance. left/right: lists of labels (emoji or « 100 g »). tilt: −1 left pan down,
    0 level, 1 right pan down.
    """
    # 344 wide: up to 5 weights (spread over 120 px) stay inside the canvas on either pan
    c = Canvas(344, 170, max_h=180, css_w='max-w-sm')
    cx, top = 172, 40
    d = 16 * tilt                      # right end goes down when tilt = 1
    c.poly([(cx - 30, 160), (cx + 30, 160), (cx + 6, 150), (cx - 6, 150)], fill=SOFT, stroke=INK, sw=1.5)
    c.line(cx, 150, cx, top, color=INK, sw=4)
    c.line(cx - 110, top - d, cx + 110, top + d, color=INK, sw=4)
    c.dot(cx, top, r=5, fill=INK)
    for side, items in ((-1, left), (1, right)):
        ex, ey = cx + side * 110, top + side * d
        pan_y = ey + 62
        c.line(ex, ey, ex - 36, pan_y, color=SOFT, sw=1.5)
        c.line(ex, ey, ex + 36, pan_y, color=SOFT, sw=1.5)
        c.path(f'M {ex - 44},{pan_y} Q {ex},{pan_y + 22} {ex + 44},{pan_y} Z', fill='#E2E8F0', stroke=INK, sw=1.8)
        n = len(items)
        weights = [it for it in items if any(ch.isdigit() for ch in (it if isinstance(it, str) else it[0]))]
        gap = min(40, 120 / max(n, 1)) if weights else min(26, 80 / max(n, 1))
        for k, it in enumerate(items):
            fr, en = (it, None) if not isinstance(it, tuple) else it
            x = ex + (k - (n - 1) / 2) * gap
            if any(ch.isdigit() for ch in fr):
                bw = min(38, gap - 3)
                c.rect(x - bw / 2, pan_y - 22, bw, 20, fill=SHADES[AMBER][2], stroke=INK, sw=1.2, rx=3)
                c.text(x, pan_y - 8, fr, size=11 if bw >= 34 else 9, bold=True, text_en=en)
            else:
                c.text(x, pan_y - 4, fr, size=22, text_en=en)
    return c.shape()


def jug(capacity_ml, level_ml, step_ml, label_every=None, color=BLUE):
    """A measuring jug graduated every ``step_ml`` (labels every ``label_every``), filled to ``level_ml``."""
    label_every = label_every or step_ml * 2
    c = Canvas(170, 190, max_h=190, css_w='max-w-[12rem]')
    x0, x1, yb, yt = 40, 120, 176, 22
    c.path(f'M {x1},{yt} L {x1 + 22},{yt + 30} L {x1 + 22},{yt + 110} L {x1},{yt + 130}', stroke=INK, sw=3)   # handle
    lvl = yb - (yb - yt - 10) * level_ml / capacity_ml
    c.rect(x0, lvl, x1 - x0, yb - lvl, fill=SHADES[color][2], stroke='none', sw=0)
    c.line(x0, lvl, x1, lvl, color=color, sw=2)
    c.path(f'M {x0},{yt} L {x0},{yb} L {x1},{yb} L {x1},{yt}', stroke=INK, sw=2.5)
    v = step_ml
    while v <= capacity_ml:
        y = yb - (yb - yt - 10) * v / capacity_ml
        big = v % label_every == 0
        c.line(x0, y, x0 + (16 if big else 9), y, color=INK, sw=1.6 if big else 1)
        if big:
            c.text(x0 - 4, y + 4, f'{v}', size=10, bold=True, anchor='end')
        v += step_ml
    c.text(x0 - 4, yt - 6, 'mL', size=10, anchor='end', color=SOFT)
    return c.shape()


# ── statistics: bar chart, line graph, pictograph ───────────────────────────

def _nice_step(top):
    for s in (1, 2, 5, 10, 20, 25, 50, 100):
        if top / s <= 8:
            return s
    return 200


def draw_bar_chart(c, box, cats, vals, color=BLUE, step=None, top=None, title=None, small=False):
    """Vertical bar chart in box. cats: labels (str or (fr, en)). Grid lines every ``step``.
    color: one colour, a list (one per bar) or 'multi' (palette)."""
    x0, y0, w, h = box
    top = top or max(vals)
    step = step or _nice_step(top)
    top = -(-top // step) * step
    left, bottom = (22 if small else 34), (16 if small else 24)
    gx, gy, gw, gh = x0 + left, y0 + (4 if small else 10), w - left - 4, h - bottom - (4 if small else 10)
    fs = 8 if small else 11
    v = 0
    while v <= top:
        y = gy + gh - gh * v / top
        c.line(gx, y, gx + gw, y, color='#E2E8F0', sw=1, opacity=1)
        c.text(gx - 4, y + 3, str(v), size=fs, anchor='end', color=INK)
        v += step
    c.line(gx, gy, gx, gy + gh, color=INK, sw=1.6)
    c.line(gx, gy + gh, gx + gw, gy + gh, color=INK, sw=1.6)
    n = len(cats)
    slot = gw / n
    for i, (cat, val) in enumerate(zip(cats, vals)):
        bw = slot * 0.6
        bx = gx + i * slot + (slot - bw) / 2
        bh = gh * val / top
        col = color[i] if isinstance(color, (list, tuple)) else PALETTE[i % len(PALETTE)] if color == 'multi' else color
        c.rect(bx, gy + gh - bh, bw, bh, fill=col, stroke=INK, sw=1)
        fr, en = (cat, None) if not isinstance(cat, tuple) else cat
        c.text(bx + bw / 2, gy + gh + (11 if small else 16), fr, size=fs if not small else 9, bold=True, text_en=en)
    return c


def bar_chart(cats, vals, color=BLUE, step=None, ylabel=None):
    c = Canvas(320, 200, max_h=210, css_w='max-w-md')
    draw_bar_chart(c, (0, 0, 320, 200), cats, vals, color, step)
    return c.shape()


def line_graph(xlabels, vals, step=None, unit='', color=RED):
    """A broken-line graph: one point per x label, joined by segments."""
    c = Canvas(340, 210, max_h=220, css_w='max-w-md')
    top = max(vals)
    step = step or _nice_step(top)
    top = -(-top // step) * step + (step if top % step == 0 else 0)
    gx, gy, gw, gh = 40, 18, 290, 162
    v = 0
    while v <= top:
        y = gy + gh - gh * v / top
        c.line(gx, y, gx + gw, y, color='#E2E8F0', sw=1, opacity=1)
        c.text(gx - 5, y + 4, f'{v}', size=10, anchor='end')
        v += step
    if unit:
        c.text(gx - 5, gy - 2, unit, size=9, anchor='end', color=SOFT)
    c.line(gx, gy, gx, gy + gh, color=INK, sw=1.6)
    c.line(gx, gy + gh, gx + gw, gy + gh, color=INK, sw=1.6)
    n = len(vals)
    pts = [(gx + (i + 0.5) * gw / n, gy + gh - gh * v / top) for i, v in enumerate(vals)]
    c.poly(pts, closed=False, stroke=color, sw=2.6)
    for (x, y), lab in zip(pts, xlabels):
        c.dot(x, y, r=4, fill=color)
        fr, en = (lab, None) if not isinstance(lab, tuple) else lab
        c.text(x, gy + gh + 16, fr, size=10, bold=True, text_en=en)
    return c.shape()


def pictograph(cats, vals, icon, per, half_ok=False):
    """
    Rows of icons: one icon = ``per`` items (key printed under the chart). A value that is a
    half multiple of ``per`` ends with a half icon when ``half_ok``.
    """
    rows = len(cats)
    max_icons = max(math.ceil(v / per) for v in vals)
    cell = 26
    w = 96 + max_icons * cell + 10
    h = rows * 32 + 34
    c = Canvas(w, h, max_h=min(h + 10, 230), css_w='max-w-md')
    for r, (cat, v) in enumerate(zip(cats, vals)):
        y = 8 + r * 32
        fr, en = (cat, None) if not isinstance(cat, tuple) else cat
        c.text(88, y + 19, fr, size=12, bold=True, anchor='end', text_en=en)
        c.line(94, y + 30, w - 6, y + 30, color='#E2E8F0', sw=1, opacity=1)
        full, rest = divmod(v, per)
        for k in range(full):
            c.text(108 + k * cell, y + 21, icon, size=19)
        if rest:
            # half icon: draw the icon, then cover its right half
            x = 108 + full * cell
            c.text(x, y + 21, icon, size=19)
            c.rect(x, y + 1, cell / 2 + 1, 28, fill='#FFFFFF', stroke='none', sw=0)
    c.line(94, 4, 94, rows * 32 + 8, color=INK, sw=1.4)
    c.text(10, h - 6, f'{icon} = {per}', size=13, bold=True, anchor='start', color=PURPLE,
           text_en=f'{icon} = {per}')
    return c.shape()


# ── probability: spinner, bag of marbles, probability line, tree diagram ────

def draw_spinner(c, box, sectors, arrow=True):
    """sectors: list of colours, one per equal sector — or (colour, weight) pairs for unequal sectors."""
    x0, y0, w, h = box
    r = min(w, h) / 2 - 4
    cx, cy = x0 + w / 2, y0 + h / 2
    parts = [(s, 1) if isinstance(s, str) else s for s in sectors]
    total = sum(wt for _, wt in parts)
    a = math.pi / 2
    for col, wt in parts:
        span = 2 * math.pi * wt / total
        if span >= 2 * math.pi - 1e-9:
            c.circle(cx, cy, r, fill=col, stroke=INK, sw=1.6)
            break
        x1, y1 = cx + r * math.cos(a), cy - r * math.sin(a)
        x2, y2 = cx + r * math.cos(a - span), cy - r * math.sin(a - span)
        large = 1 if span > math.pi else 0
        c.path(f'M {_r(cx)},{_r(cy)} L {_r(x1)},{_r(y1)} A {_r(r)},{_r(r)} 0 {large},1 {_r(x2)},{_r(y2)} Z',
               fill=col, stroke=INK, sw=1.6)
        a -= span
    if arrow:
        c.line(cx, cy, cx + r * 0.55, cy - r * 0.35, color=INK, sw=3)
        c.dot(cx, cy, r=4, fill=INK)
    return c


def spinner(sectors, size=150):
    c = Canvas(size, size, max_h=160, css_w='max-w-[10rem]')
    draw_spinner(c, (0, 0, size, size), sectors)
    return c.shape()


def draw_bag(c, box, counts):
    """A bag (rounded outline) with marbles: counts = [(colour, n), …]."""
    x0, y0, w, h = box
    c.path(f'M {_r(x0 + w * .2)},{_r(y0 + h * .18)} Q {_r(x0)},{_r(y0 + h * .55)} {_r(x0 + w * .12)},{_r(y0 + h * .92)} '
           f'L {_r(x0 + w * .88)},{_r(y0 + h * .92)} Q {_r(x0 + w)},{_r(y0 + h * .55)} {_r(x0 + w * .8)},{_r(y0 + h * .18)} Z',
           fill='#F8FAFC', stroke=INK, sw=2)
    c.line(x0 + w * .2, y0 + h * .18, x0 + w * .8, y0 + h * .18, color=INK, sw=3)
    balls = [col for col, n in counts for _ in range(n)]
    random.shuffle(balls)
    n = len(balls)
    per = 4 if n <= 12 else 5
    rr = min(w / (2 * per + 3), 9)
    for i, col in enumerate(balls):
        row, k = divmod(i, per)
        in_row = min(per, n - row * per)
        x = x0 + w / 2 + (k - (in_row - 1) / 2) * (2 * rr + 3)
        y = y0 + h * .82 - row * (2 * rr + 3)
        c.circle(x, y, rr, fill=col, stroke=INK, sw=1.2)
    return c


def bag(counts, size=(140, 130)):
    c = Canvas(*size, max_h=140, css_w='max-w-[9rem]')
    draw_bag(c, (4, 4, size[0] - 8, size[1] - 8), counts)
    return c.shape()


def tree_diagram(first, second, hide=None):
    """
    Two-stage tree. first, second: label lists (str or (fr, en)). ``hide`` = (i, j) puts « ? »
    on second-stage leaf j of branch i.
    """
    n1, n2 = len(first), len(second)
    leaves = n1 * n2
    row = 22
    h = leaves * row + 16
    c = Canvas(300, h, max_h=min(h + 10, 300), css_w='max-w-sm')
    root = (16, h / 2)
    c.dot(*root, r=4, fill=INK)
    for i, a in enumerate(first):
        ym = 8 + (i * n2 + n2 / 2) * row
        mid = (120, ym)
        c.line(*root, mid[0] - 30, ym, color=SOFT, sw=2)
        fa, ea = (a, None) if not isinstance(a, tuple) else a
        c.text(mid[0] - 26, ym + 4, fa, size=12, bold=True, anchor='start', text_en=ea)
        for j, b in enumerate(second):
            y = 8 + (i * n2 + j + 0.5) * row
            c.line(mid[0] + 22, ym, 214, y, color=SOFT, sw=1.6)
            fb, eb = (b, None) if not isinstance(b, tuple) else b
            if hide == (i, j):
                fb, eb = '?', None
            c.text(220, y + 4, fb, size=12, bold=True, anchor='start', color=PURPLE if fb == '?' else '#1E0A3C', text_en=eb)
    return c.shape()


def prob_line(marks, w=330):
    """A 0–1 probability line with lettered points: marks = [(position 0..1, letter)]."""
    c = Canvas(w, 92, max_h=100, css_w='max-w-md')
    x0, x1, y = 20, w - 20, 40
    c.line(x0, y, x1, y, color=INK, sw=2.5)
    for v, lab in ((0, '0'), (0.5, '½'), (1, '1')):
        x = x0 + v * (x1 - x0)
        c.line(x, y - 8, x, y + 8, color=INK, sw=2)
        c.text(x, y + 26, lab, size=13, bold=True)
    c.text(x0, y + 44, 'impossible', size=10, color=SOFT, text_en='impossible')
    c.text(x1, y + 44, 'certain', size=10, color=SOFT, text_en='certain')
    for v, letter in marks:
        x = x0 + v * (x1 - x0)
        c.dot(x, y, r=6, fill=PURPLE)
        c.text(x, y - 13, letter, size=14, bold=True, color=PURPLE)
    return c.shape()


# ── grades 1–2: counting, base ten, hundred chart ───────────────────────────

def emoji_set(icon, n, per_row=10, group_tens=False, scatter=False, size=22):
    """n copies of an emoji. group_tens: rows of 10 with a gap after 5 (ten-frame feel). scatter: random spots."""
    if scatter:
        w, h = 320, 170
        c = Canvas(w, h, max_h=180, css_w='max-w-md')
        spots = set()
        while len(spots) < n:
            spots.add((random.randrange(14, w - 14, 18), random.randrange(22, h - 4, 18)))
        for x, y in spots:
            c.text(x, y, icon, size=size - 6)
        return c.shape()
    per_row = 10 if group_tens else per_row
    rows = -(-n // per_row)
    cell = size + 8
    w = per_row * cell + (12 if group_tens else 0) + 10
    c = Canvas(w, rows * cell + 10, max_h=min(rows * (cell + 4) + 20, 260), css_w='max-w-md')
    for k in range(n):
        r, i = divmod(k, per_row)
        x = 8 + i * cell + cell / 2 + (12 if group_tens and i >= 5 else 0)
        c.text(x, 6 + r * cell + cell * 0.8, icon, size=size)
    return c.shape()


def base_ten(hundreds, tens, ones, unit=9, color=BLUE):
    """Base-ten blocks: flats (100), rods (10), small cubes (1)."""
    light, mid, dark = SHADES[color]
    w = hundreds * (10 * unit + 10) + tens * (unit + 7) + 20 + (-(-ones // 5)) * (unit + 4) + 20
    h = 10 * unit + 20
    c = Canvas(max(w, 80), h, max_h=min(h + 10, 140), css_w='max-w-md')
    x = 8
    for _ in range(hundreds):
        c.rect(x, 8, 10 * unit, 10 * unit, fill=mid, stroke=INK, sw=1.5)
        for k in range(1, 10):
            c.line(x + k * unit, 8, x + k * unit, 8 + 10 * unit, color=dark, sw=0.8, opacity=1)
            c.line(x, 8 + k * unit, x + 10 * unit, 8 + k * unit, color=dark, sw=0.8, opacity=1)
        x += 10 * unit + 10
    for _ in range(tens):
        c.rect(x, 8, unit, 10 * unit, fill=mid, stroke=INK, sw=1.5)
        for k in range(1, 10):
            c.line(x, 8 + k * unit, x + unit, 8 + k * unit, color=dark, sw=0.8, opacity=1)
        x += unit + 7
    x += 10
    for k in range(ones):
        col, row = divmod(k, 5)
        c.rect(x + col * (unit + 4), 8 + 10 * unit - (row + 1) * (unit + 4) + 4, unit, unit, fill=light, stroke=INK, sw=1.3)
    return c.shape()


def hundred_window(start_row, start_col, rows, cols, hide, show_all=False):
    """
    A window of the 1–100 chart: rows × cols cells starting at row/col (0-based).
    ``hide`` = the number replaced by « ? ». Other cells show their numbers.
    """
    cell = 36
    c = Canvas(cols * cell + 8, rows * cell + 8, max_h=rows * cell + 20, css_w='max-w-xs')
    for r in range(rows):
        for k in range(cols):
            n = (start_row + r) * 10 + start_col + k + 1
            x, y = 4 + k * cell, 4 + r * cell
            q = n == hide
            c.rect(x, y, cell, cell, fill=TINTS[PURPLE] if q else '#FFFFFF', stroke=SOFT, sw=1)
            c.text(x + cell / 2, y + cell / 2 + 5, '?' if q else str(n), size=14 if not q else 17, bold=True,
                   color=PURPLE if q else INK)
    return c.shape()


def number_jumps(start, jumps, end_label='?'):
    """Open number line: arcs from ``start`` for each jump (+10, +3…). Labels the landing points except the last."""
    total = sum(abs(j) for j in jumps)
    w = 340
    c = Canvas(w, 96, max_h=110, css_w='max-w-md')
    x0, x1, y = 20, w - 20, 66
    c.line(x0 - 6, y, x1 + 6, y, color=INK, sw=2)
    scale = (x1 - x0) / max(total, 1)
    sign = 1 if jumps[0] > 0 else -1
    pos = start
    x = x0 if sign > 0 else x1
    c.line(x, y - 7, x, y + 7, color=INK, sw=2)
    c.text(x, y + 22, str(start), size=13, bold=True)
    for k, j in enumerate(jumps):
        nx = x + sign * abs(j) * scale
        mid = (x + nx) / 2
        hgt = 18 + min(abs(j), 10) * 2
        c.path(f'M {_r(x)},{y} Q {_r(mid)},{y - 2 * hgt} {_r(nx)},{y}', stroke=GREEN, sw=2.2)
        c.text(mid, y - hgt - 6, f'{"+" if j > 0 else "−"}{abs(j)}', size=12, bold=True, color=GREEN)
        pos += j
        c.line(nx, y - 7, nx, y + 7, color=INK, sw=2)
        last = k == len(jumps) - 1
        c.text(nx, y + 22, end_label if last else str(pos), size=13 if not last else 15, bold=True,
               color=PURPLE if last else INK)
        x = nx
    return c.shape()


def equal_groups(groups, each, icon='🍪'):
    """``groups`` circles (plates) with ``each`` emoji in each."""
    per_row = min(groups, 4)
    rows = -(-groups // per_row)
    pw = 84
    c = Canvas(per_row * (pw + 8) + 8, rows * (pw + 8) + 8, max_h=min(rows * 100 + 10, 220), css_w='max-w-md')
    for g in range(groups):
        r, k = divmod(g, per_row)
        cx, cy = 8 + k * (pw + 8) + pw / 2, 8 + r * (pw + 8) + pw / 2
        c.circle(cx, cy, pw / 2 - 2, fill='#F8FAFC', stroke=SOFT, sw=2)
        cols = 3 if each > 4 else 2
        for i in range(each):
            rr, cc = divmod(i, cols)
            nrows = -(-each // cols)
            x = cx + (cc - (cols - 1) / 2) * 20
            y = cy + (rr - (nrows - 1) / 2) * 20 + 6
            c.text(x, y, icon, size=16)
    return c.shape()


# ── grades 1–2: plane shapes and lines ───────────────────────────────────────

def plane_shape_pts(kind, rot=0.0, stretch=1.0):
    """Unit points for square, rectangle, triangle, rhombus, or None for a circle."""
    if kind == 'circle':
        return None
    base = {
        'square': [(-1, -1), (1, -1), (1, 1), (-1, 1)],
        'rectangle': [(-1.6 * stretch, -0.8), (1.6 * stretch, -0.8), (1.6 * stretch, 0.8), (-1.6 * stretch, 0.8)],
        'triangle': [(-1.1, 0.8), (1.1, 0.8), (0.2 * stretch, -1.1)],
        'rhombus': [(0, -1.3), (0.8, 0), (0, 1.3), (-0.8, 0)],
        'pentagon': _ngon(5), 'hexagon': _ngon(6),
    }[kind]
    cs, sn = math.cos(rot), math.sin(rot)
    return [(x * cs - y * sn, x * sn + y * cs) for x, y in base]


def draw_plane_shape(c, kind, box, color=BLUE, rot=0.0, stretch=1.0, scale=1.0):
    x0, y0, w, h = box
    if kind == 'circle':
        r = min(w, h) / 2 * 0.8 * scale
        c.circle(x0 + w / 2, y0 + h / 2, r, fill=SHADES[color][1], stroke=INK, sw=2.2)
        return
    pts = plane_shape_pts(kind, rot, stretch)
    if scale != 1.0:
        mw, mh = w * (1 - scale) / 2, h * (1 - scale) / 2
        box = (x0 + mw, y0 + mh, w * scale, h * scale)
    draw_polygon(c, pts, box, color)


def draw_line_kind(c, box, closed, curved, color=INK):
    """Open/closed, curved/broken lines for grade 1."""
    x0, y0, w, h = box
    cx, cy = x0 + w / 2, y0 + h / 2
    if curved:
        if closed:
            c.path(f'M {_r(cx - w * .35)},{_r(cy)} C {_r(cx - w * .35)},{_r(cy - h * .5)} {_r(cx + w * .2)},{_r(cy - h * .45)} '
                   f'{_r(cx + w * .35)},{_r(cy - h * .05)} C {_r(cx + w * .45)},{_r(cy + h * .4)} {_r(cx - w * .3)},{_r(cy + h * .45)} '
                   f'{_r(cx - w * .35)},{_r(cy)} Z', stroke=color, sw=3)
        else:
            c.path(f'M {_r(x0 + 6)},{_r(cy + h * .2)} C {_r(cx - w * .2)},{_r(cy - h * .5)} {_r(cx + w * .1)},{_r(cy + h * .5)} '
                   f'{_r(x0 + w - 6)},{_r(cy - h * .2)}', stroke=color, sw=3)
    else:
        pts = [(cx - w * .38, cy + h * .25), (cx - w * .15, cy - h * .35), (cx + w * .1, cy + h * .1), (cx + w * .38, cy - h * .3),
               (cx + w * .3, cy + h * .35)]
        c.poly(pts, closed=closed, stroke=color, sw=3)


def clip_measure(length, clip_w=34):
    """A ribbon above a row of paper clips laid end to end from the same start."""
    w = length * clip_w + 40
    c = Canvas(max(w, 160), 92, max_h=100, css_w='max-w-md')
    x0 = 16
    c.rect(x0, 14, length * clip_w, 16, fill=SHADES[RED][2], stroke=INK, sw=1.6, rx=3)
    for k in range(length):                  # exactly as many clips as the ribbon is long
        x = x0 + k * clip_w
        c.rect(x + 2, 50, clip_w - 4, 16, fill='none', stroke=SOFT, sw=2.2, rx=8)
        c.rect(x + 7, 54, clip_w - 14, 8, fill='none', stroke=SOFT, sw=1.6, rx=4)
    c.line(x0, 8, x0, 72, color=SOFT, sw=1, dash='3 3')
    c.line(x0 + length * clip_w, 8, x0 + length * clip_w, 72, color=SOFT, sw=1, dash='3 3')
    return c.shape()
