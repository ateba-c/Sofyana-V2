"""
geometry_utils.py
Pre-computes every SVG coordinate so templates need zero arithmetic.
Each render_shape() returns a dict consumed by partials/shape_canvas.html.
"""
import math

# ── colour palette (Disney-inspired: bold, saturated, kid-friendly) ────────────
STROKES = ['#2563EB', '#EF4444', '#16A34A', '#D97706', '#9333EA', '#0891B2']
FILLS   = [
    'rgba(37,99,235,0.18)',   # royal blue
    'rgba(239,68,68,0.18)',   # vivid red
    'rgba(22,163,74,0.18)',   # bright green
    'rgba(217,119,6,0.18)',   # golden amber
    'rgba(147,51,234,0.18)',  # magic purple
    'rgba(8,145,178,0.18)',   # sky teal
]


# ── helpers ────────────────────────────────────────────────────────────────────

def _norm_fit(val_w, val_h, avail_w, avail_h, scale=0.82):
    """Return (draw_w, draw_h) scaled to fit avail box, preserving aspect ratio."""
    ratio = val_w / val_h
    if ratio > avail_w / avail_h:
        w = avail_w * scale
        h = w / ratio
    else:
        h = avail_h * scale
        w = h * ratio
    return w, h


def _right_angle_path(px, py, dx1, dy1, dx2, dy2, size=10):
    """
    Right-angle mark at vertex (px, py).
    dx1,dy1  — direction along the first side (toward the next vertex).
    dx2,dy2  — direction along the second side (toward the other vertex).
    Both vectors are normalised internally; no arithmetic needed in templates.
    """
    l1 = math.hypot(dx1, dy1)
    l2 = math.hypot(dx2, dy2)
    ux1, uy1 = dx1 / l1, dy1 / l1
    ux2, uy2 = dx2 / l2, dy2 / l2
    # three corners of the little square
    qx1, qy1 = px + ux1 * size,               py + uy1 * size
    qx2, qy2 = px + ux1 * size + ux2 * size,  py + uy1 * size + uy2 * size
    qx3, qy3 = px + ux2 * size,               py + uy2 * size
    return (f"M {qx1:.1f},{qy1:.1f} L {qx2:.1f},{qy2:.1f} L {qx3:.1f},{qy3:.1f}")


def _tick_path(ax, ay, bx, by, size=8):
    """Single tick mark at midpoint of segment A→B, perpendicular."""
    mx, my = (ax + bx) / 2, (ay + by) / 2
    dx, dy = bx - ax, by - ay
    ln = math.hypot(dx, dy)
    if ln == 0:
        return ''
    px, py = -dy / ln * size / 2, dx / ln * size / 2
    return f"M {mx-px:.1f},{my-py:.1f} L {mx+px:.1f},{my+py:.1f}"


def _label(text, x, y, anchor='middle', size=13, bold=False,
           color='#1E0A3C', transform=''):
    return dict(text=str(text), x=round(x, 1), y=round(y, 1),
                anchor=anchor, size=size, bold=bold,
                color=color, transform=transform)


def _dashed(x1, y1, x2, y2):
    return dict(type='dashed',
                x1=round(x1,1), y1=round(y1,1),
                x2=round(x2,1), y2=round(y2,1))


def _solid_line(x1, y1, x2, y2, color=None):
    d = dict(type='line',
             x1=round(x1,1), y1=round(y1,1),
             x2=round(x2,1), y2=round(y2,1))
    if color:
        d['color'] = color
    return d


# ── fraction expression renderer ──────────────────────────────────────────────

def _frac_token_width(token, fsize, cw):
    """Pixel width of one expression token (fraction, operator, or plain text)."""
    if isinstance(token, dict) and 'den' in token:
        num_w = max(len(str(token.get('num','1'))), 1) * cw
        den_w = max(len(str(token.get('den','1'))), 1) * cw
        fw    = max(num_w, den_w) + 14
        if 'whole' in token:
            fw += len(str(token['whole'])) * cw * 1.1 + 6
        return fw
    text = str(token)
    return max(len(text), 1) * cw + 4


def _render_fraction_expr(shape: dict, vw: float, vh: float,
                          pad: float, color_idx: int) -> dict:
    """
    Renders a fraction arithmetic expression.

    shape keys:
      op1, op2   — fraction dict  {'num': N, 'den': D}
                   or mixed number {'whole': W, 'num': N, 'den': D}
                   or plain string / number for whole-number operands
      operator   — '+', '−', '×', '÷'
      result     — {'num': '?', 'den': '?'}  (fraction slot)
                   or '?' (single ? for whole-number answer)
      format     — 'operation' (default) | 'simplify' | 'compare'
    """
    stroke   = STROKES[color_idx % len(STROKES)]
    OP_COLORS = {'+': '#16A34A', '−': '#EF4444', '-': '#EF4444',
                 '×': '#9333EA', '*': '#9333EA', '÷': '#D97706', '/': '#D97706',
                 '?': '#94a3b8', '□': '#94a3b8'}

    out = dict(type='fraction_expr', stroke=stroke, fill='none', sw=0,
               path='', circle=None, labels=[], marks=[],
               vw=vw, vh=vh, title=shape.get('title', ''))

    fsize    = 22           # digit font-size inside fractions
    cw       = fsize * 0.63 # estimated char width
    op_fsize = 26           # operator font-size
    gap      = 6            # vertical gap between digit and fraction bar

    # Fraction bar is at the vertical midline of the canvas
    bar_y    = vh / 2

    # ── build token list ────────────────────────────────────────────────────
    op1      = shape.get('op1', {'num': 1, 'den': 2})
    operator = shape.get('operator', '+')
    op2      = shape.get('op2', {'num': 1, 'den': 3})
    result   = shape.get('result', {'num': '?', 'den': '?'})
    fmt      = shape.get('format', 'operation')

    if fmt == 'simplify':
        tokens = [op1, '=', result]
    elif fmt == 'compare':
        tokens = [op1, operator, op2]   # operator will be '?' or '□'
    else:
        tokens = [op1, operator, op2, '=', result]

    # ── compute total width ─────────────────────────────────────────────────
    tok_gap = 16
    widths  = [_frac_token_width(t, fsize, cw) for t in tokens]
    total_w = sum(widths) + tok_gap * (len(tokens) - 1)

    # scale down if it overflows
    scale   = min(1.0, (vw - 2 * pad) / total_w) if total_w > 0 else 1.0
    eff_gap = tok_gap * scale

    # ── render each token ───────────────────────────────────────────────────
    x = (vw - total_w * scale) / 2

    for token, raw_w in zip(tokens, widths):
        w  = raw_w * scale
        cx = x + w / 2

        # ── fraction dict ────────────────────────────────────────────────
        if isinstance(token, dict) and 'den' in token:
            num_str   = str(token.get('num', ''))
            den_str   = str(token.get('den', ''))
            whole     = token.get('whole')
            is_answer = (num_str == '?' or den_str == '?')

            if whole is not None:
                ws      = str(whole)
                ww      = len(ws) * cw * 1.1 * scale + 6 * scale
                frac_cx = cx + (w - ww) / 2 - 2
                out['labels'].append(_label(
                    ws, cx - w/2 + ww/2,
                    bar_y + fsize * 0.38 * scale,
                    anchor='middle',
                    size=max(12, int(fsize * 1.05 * scale)),
                    bold=True, color='#1E0A3C'
                ))
            else:
                frac_cx = cx

            bar_hw  = (w / 2 - (6 * scale if whole else 2)) * (1 if not whole else 0.7)
            n_color = stroke if is_answer else '#1E0A3C'
            d_color = stroke if is_answer else '#1E0A3C'

            # fraction bar
            out['marks'].append(_solid_line(
                frac_cx - bar_hw, bar_y,
                frac_cx + bar_hw, bar_y,
                color='#1E0A3C'
            ))
            # numerator (baseline above the bar)
            out['labels'].append(_label(
                num_str, frac_cx, bar_y - gap * scale - 2,
                anchor='middle',
                size=max(12, int(fsize * scale)),
                bold=True, color=n_color
            ))
            # denominator (baseline below the bar)
            out['labels'].append(_label(
                den_str, frac_cx, bar_y + gap * scale + fsize * 0.82 * scale,
                anchor='middle',
                size=max(12, int(fsize * scale)),
                bold=True, color=d_color
            ))

        # ── whole-number operand (string / int) ─────────────────────────
        elif not isinstance(token, dict):
            text     = str(token)
            is_op    = text in OP_COLORS
            is_eq    = (text == '=')
            is_ans   = (text == '?')
            color    = (OP_COLORS[text] if is_op and not is_eq
                        else 'rgba(255,255,255,0.30)' if is_eq
                        else stroke if is_ans
                        else '#1E0A3C')
            out['labels'].append(_label(
                text, cx, bar_y + op_fsize * 0.38 * scale,
                anchor='middle',
                size=max(12, int(op_fsize * scale)),
                bold=True, color=color
            ))

        x += w + eff_gap

    return out


# ── public API ─────────────────────────────────────────────────────────────────

def render_shape(shape: dict, vw: float = 260, vh: float = 185,
                 pad: float = 32, color_idx: int = 0) -> dict:
    """
    Convert a shape definition dict into a dict of SVG-ready data.

    Supported types: rectangle, square, right_triangle, equilateral_triangle,
                     isosceles_triangle, circle, parallelogram, trapezoid
    """
    stype  = shape.get('type', 'rectangle')
    stroke = shape.get('stroke', STROKES[color_idx % len(STROKES)])
    fill   = shape.get('fill',   FILLS[color_idx % len(FILLS)])

    out = dict(
        type=stype, stroke=stroke, fill=fill, sw=3.5,
        path='', circle=None,
        labels=[], marks=[], lines=[],
        vw=vw, vh=vh,
        title=shape.get('title', ''),
    )

    lbs = shape.get('labels', {})      # user-supplied label overrides
    avail_w, avail_h = vw - 2 * pad, vh - 2 * pad

    # ── rectangle / square ──────────────────────────────────────────────────
    if stype in ('rectangle', 'square'):
        w_val = float(shape.get('width', shape.get('side', 6)))
        h_val = float(shape.get('height', shape.get('side', 6)))
        dw, dh = _norm_fit(w_val, h_val, avail_w, avail_h - 10)
        x0, y0 = (vw - dw) / 2, (vh - dh) / 2
        out['path'] = (f"M {x0:.1f},{y0:.1f} h {dw:.1f} "
                       f"v {dh:.1f} h -{dw:.1f} Z")
        # width label — top centre
        out['labels'].append(_label(lbs.get('w', f'{w_val:g}'),
                                    vw/2, y0 - 12))
        # height label — left, rotated
        out['labels'].append(_label(lbs.get('h', f'{h_val:g}'),
                                    x0 - 14, vh / 2, anchor='middle',
                                    transform=f'rotate(-90,{x0-14:.1f},{vh/2:.1f})'))
        # optional inner label (e.g. "A = ?")
        if lbs.get('inner'):
            out['labels'].append(_label(lbs['inner'], vw/2, vh/2 + 6,
                                        size=15, bold=True, color=stroke))

    # ── right triangle ───────────────────────────────────────────────────────
    elif stype == 'right_triangle':
        a = float(shape.get('a', 3))
        b = float(shape.get('b', 4))
        dw, dh = _norm_fit(a, b, avail_w - 10, avail_h - 20)
        x0 = (vw - dw) / 2
        y0 = (vh + dh) / 2
        p1 = (x0, y0)             # right-angle vertex (bottom-left)
        p2 = (x0 + dw, y0)        # bottom-right
        p3 = (x0, y0 - dh)        # top-left
        out['path'] = (f"M {p1[0]:.1f},{p1[1]:.1f} "
                       f"L {p2[0]:.1f},{p2[1]:.1f} "
                       f"L {p3[0]:.1f},{p3[1]:.1f} Z")
        # right-angle mark: use actual side directions from p1 → p2 and p1 → p3
        out['marks'].append(dict(
            type='path',
            d=_right_angle_path(
                p1[0], p1[1],
                p2[0] - p1[0], p2[1] - p1[1],   # along base (right)
                p3[0] - p1[0], p3[1] - p1[1],   # along height (up in SVG = negative y)
                10
            ),
            stroke=stroke
        ))
        # side labels
        c_val = lbs.get('c', f'{math.sqrt(a**2+b**2):.4g}')
        out['labels'].append(_label(lbs.get('a', f'{a:g}'),
                                    (p1[0]+p2[0])/2, p1[1]+18))
        out['labels'].append(_label(lbs.get('b', f'{b:g}'),
                                    p1[0]-16, (p1[1]+p3[1])/2,
                                    transform=f'rotate(-90,{p1[0]-16:.1f},{(p1[1]+p3[1])/2:.1f})'))
        out['labels'].append(_label(str(c_val),
                                    (p2[0]+p3[0])/2+14,
                                    (p2[1]+p3[1])/2, anchor='start'))
        if lbs.get('inner'):
            cx = (p1[0]+p2[0]+p3[0])/3
            cy = (p1[1]+p2[1]+p3[1])/3 + 4
            out['labels'].append(_label(lbs['inner'], cx, cy,
                                        size=14, bold=True, color=stroke))

    # ── equilateral triangle ─────────────────────────────────────────────────
    elif stype == 'equilateral_triangle':
        s = float(shape.get('side', 6))
        ds = min(avail_w, avail_h - 20) * 0.88
        dh_t = ds * math.sqrt(3) / 2
        cx_t = vw / 2
        y_bot = (vh + dh_t) / 2
        p1 = (cx_t - ds/2, y_bot)
        p2 = (cx_t + ds/2, y_bot)
        p3 = (cx_t, y_bot - dh_t)
        out['path'] = (f"M {p1[0]:.1f},{p1[1]:.1f} "
                       f"L {p2[0]:.1f},{p2[1]:.1f} "
                       f"L {p3[0]:.1f},{p3[1]:.1f} Z")
        sl = lbs.get('side', f'{s:g}')
        out['labels'].append(_label(sl, cx_t, p1[1]+18))
        out['labels'].append(_label(sl, (p1[0]+p3[0])/2-18,
                                    (p1[1]+p3[1])/2, anchor='end'))
        out['labels'].append(_label(sl, (p2[0]+p3[0])/2+18,
                                    (p2[1]+p3[1])/2, anchor='start'))
        # equal-side tick marks
        for pa, pb in [(p1,p2),(p1,p3),(p2,p3)]:
            d = _tick_path(pa[0],pa[1],pb[0],pb[1])
            if d:
                out['marks'].append(dict(type='path', d=d, stroke=stroke))
        if lbs.get('inner'):
            cy_t = (p1[1]+p2[1]+p3[1])/3
            out['labels'].append(_label(lbs['inner'], cx_t, cy_t+5,
                                        size=14, bold=True, color=stroke))

    # ── isosceles triangle ───────────────────────────────────────────────────
    elif stype == 'isosceles_triangle':
        base   = float(shape.get('base', 6))
        height = float(shape.get('height', 5))
        dw, dh_t = _norm_fit(base, height, avail_w - 10, avail_h - 20)
        cx_t = vw / 2
        y_bot = (vh + dh_t) / 2
        p1 = (cx_t - dw/2, y_bot)
        p2 = (cx_t + dw/2, y_bot)
        p3 = (cx_t, y_bot - dh_t)
        out['path'] = (f"M {p1[0]:.1f},{p1[1]:.1f} "
                       f"L {p2[0]:.1f},{p2[1]:.1f} "
                       f"L {p3[0]:.1f},{p3[1]:.1f} Z")
        leg = math.sqrt((base/2)**2 + height**2)
        out['labels'].append(_label(lbs.get('base', f'{base:g}'),
                                    cx_t, p1[1]+18))
        out['labels'].append(_label(lbs.get('leg', f'{leg:.4g}'),
                                    (p1[0]+p3[0])/2-18,
                                    (p1[1]+p3[1])/2, anchor='end'))
        out['labels'].append(_label(lbs.get('leg', f'{leg:.4g}'),
                                    (p2[0]+p3[0])/2+18,
                                    (p2[1]+p3[1])/2, anchor='start'))
        # height dashed + label
        out['marks'].append(_dashed(cx_t, y_bot, cx_t, y_bot-dh_t))
        out['labels'].append(_label(lbs.get('h', f'{height:g}'),
                                    cx_t+14, (y_bot*2-dh_t)/2, anchor='start'))
        # equal-leg tick marks
        for pa, pb in [(p1,p3),(p2,p3)]:
            d = _tick_path(pa[0],pa[1],pb[0],pb[1])
            if d:
                out['marks'].append(dict(type='path', d=d, stroke=stroke))
        if lbs.get('inner'):
            cy_t = (p1[1]+p2[1]+p3[1])/3
            out['labels'].append(_label(lbs['inner'], cx_t, cy_t+4,
                                        size=14, bold=True, color=stroke))

    # ── circle ───────────────────────────────────────────────────────────────
    elif stype == 'circle':
        r_val = float(shape.get('radius', 5))
        dr = min(avail_w, avail_h) / 2 - 8
        cx, cy = vw/2, vh/2
        out['circle'] = dict(cx=round(cx,1), cy=round(cy,1), r=round(dr,1))
        # radius line (horizontal to the right)
        out['marks'].append(_solid_line(cx, cy, cx+dr, cy))
        # centre dot
        out['marks'].append(dict(type='dot', x=round(cx,1), y=round(cy,1)))
        r_lbl = lbs.get('r', f'r = {r_val:g}')
        out['labels'].append(_label(r_lbl, cx + dr/2, cy - 10))
        if lbs.get('inner'):
            out['labels'].append(_label(lbs['inner'], cx, cy+20,
                                        size=14, bold=True, color=stroke))

    # ── parallelogram ────────────────────────────────────────────────────────
    elif stype == 'parallelogram':
        base   = float(shape.get('base', 8))
        height = float(shape.get('height', 4))
        slant  = float(shape.get('slant_ratio', 0.3))
        avail_draw = min(avail_w * 0.78, avail_h * base/height * 0.78)
        db = avail_draw
        dh_p = db * height / base
        off  = db * slant
        x0   = (vw - db - off) / 2
        y0   = (vh + dh_p) / 2
        p1   = (x0, y0)
        p2   = (x0+db, y0)
        p3   = (x0+db+off, y0-dh_p)
        p4   = (x0+off, y0-dh_p)
        out['path'] = (f"M {p1[0]:.1f},{p1[1]:.1f} "
                       f"L {p2[0]:.1f},{p2[1]:.1f} "
                       f"L {p3[0]:.1f},{p3[1]:.1f} "
                       f"L {p4[0]:.1f},{p4[1]:.1f} Z")
        out['labels'].append(_label(lbs.get('base', f'{base:g}'),
                                    (p1[0]+p2[0])/2, p1[1]+18))
        # height dashed line between parallel sides
        h_x = p2[0] + off/2
        out['marks'].append(_dashed(h_x, y0, h_x, y0-dh_p))
        out['labels'].append(_label(lbs.get('h', f'{height:g}'),
                                    h_x+12, y0-dh_p/2, anchor='start'))
        if lbs.get('inner'):
            cx_p = (p1[0]+p2[0]+p3[0]+p4[0])/4
            cy_p = (p1[1]+p2[1]+p3[1]+p4[1])/4
            out['labels'].append(_label(lbs['inner'], cx_p, cy_p,
                                        size=14, bold=True, color=stroke))

    # ── trapezoid ────────────────────────────────────────────────────────────
    elif stype == 'trapezoid':
        top_v    = float(shape.get('top', 4))
        bottom_v = float(shape.get('bottom', 8))
        height   = float(shape.get('height', 4))
        db = min(avail_w * 0.82, avail_h * bottom_v/height * 0.82)
        dh_t = db * height / bottom_v
        dt   = db * top_v / bottom_v
        x0   = (vw - db) / 2
        y_bot= (vh + dh_t) / 2
        y_top= y_bot - dh_t
        off  = (db - dt) / 2
        p1   = (x0, y_bot)
        p2   = (x0+db, y_bot)
        p3   = (x0+db-off, y_top)
        p4   = (x0+off, y_top)
        out['path'] = (f"M {p1[0]:.1f},{p1[1]:.1f} "
                       f"L {p2[0]:.1f},{p2[1]:.1f} "
                       f"L {p3[0]:.1f},{p3[1]:.1f} "
                       f"L {p4[0]:.1f},{p4[1]:.1f} Z")
        out['labels'].append(_label(lbs.get('bottom', f'{bottom_v:g}'),
                                    (p1[0]+p2[0])/2, p1[1]+18))
        out['labels'].append(_label(lbs.get('top', f'{top_v:g}'),
                                    (p3[0]+p4[0])/2, y_top-12))
        h_x = vw/2
        out['marks'].append(_dashed(h_x, y_bot, h_x, y_top))
        out['labels'].append(_label(lbs.get('h', f'{height:g}'),
                                    h_x+12, (y_bot+y_top)/2, anchor='start'))
        if lbs.get('inner'):
            out['labels'].append(_label(lbs['inner'], vw/2, (y_bot+y_top)/2,
                                        size=14, bold=True, color=stroke))

    # ── angle (grade-3: identify acute / right / obtuse) ─────────────────────
    elif stype == 'angle':
        degrees = float(shape.get('degrees', 60))
        import math as _math
        cx, cy = vw / 2, vh * 0.62           # vertex near bottom-centre
        arm_len = min(avail_w, avail_h) * 0.55

        # First ray: horizontal right
        x1, y1 = cx + arm_len, cy
        # Second ray: rotated by `degrees` counter-clockwise
        rad = _math.radians(degrees)
        x2 = cx + arm_len * _math.cos(rad)
        y2 = cy - arm_len * _math.sin(rad)

        out['marks'].append(_solid_line(cx, cy, x1, y1))
        out['marks'].append(_solid_line(cx, cy, x2, y2))

        # Arc from first ray to second ray
        arc_r = arm_len * 0.32
        # SVG arc: start and end points
        ax1 = cx + arc_r
        ay1 = cy
        ax2 = cx + arc_r * _math.cos(rad)
        ay2 = cy - arc_r * _math.sin(rad)
        large = 1 if degrees > 180 else 0
        sweep = 1  # counter-clockwise in SVG coords means sweep=0 (y inverted)
        out['path'] = (
            f"M {ax1:.1f},{ay1:.1f} "
            f"A {arc_r:.1f},{arc_r:.1f} 0 {large},0 {ax2:.1f},{ay2:.1f}"
        )

        # Right-angle mark for 90°
        if abs(degrees - 90) < 2:
            sq = arm_len * 0.13
            out['marks'].append(dict(
                type='path',
                d=f"M {cx+sq:.1f},{cy:.1f} L {cx+sq:.1f},{cy-sq:.1f} L {cx:.1f},{cy-sq:.1f}",
                stroke=stroke,
            ))
            out['path'] = ''   # no arc for right angle — the square IS the mark

        # Vertex dot
        out['marks'].append(dict(type='dot', x=round(cx, 1), y=round(cy, 1)))

    # ── line_pair (grade-3: parallel / perpendicular / intersecting) ──────────
    elif stype == 'line_pair':
        relation = shape.get('relation', 'parallel')  # 'parallel'|'perpendicular'|'intersecting'
        import math as _math
        cx, cy = vw / 2, vh / 2
        half_w = avail_w * 0.45
        half_h = avail_h * 0.38

        if relation == 'parallel':
            # Two horizontal lines, offset vertically
            offset = avail_h * 0.22
            out['marks'].append(_solid_line(cx - half_w, cy - offset,
                                            cx + half_w, cy - offset))
            out['marks'].append(_solid_line(cx - half_w, cy + offset,
                                            cx + half_w, cy + offset))
            # Arrow tips (little chevrons) to suggest lines extend
            for y_off in [cy - offset, cy + offset]:
                out['marks'].append(dict(
                    type='path',
                    d=(f"M {cx+half_w-8:.1f},{y_off-5:.1f} "
                       f"L {cx+half_w:.1f},{y_off:.1f} "
                       f"L {cx+half_w-8:.1f},{y_off+5:.1f}"),
                    stroke=stroke,
                ))
                out['marks'].append(dict(
                    type='path',
                    d=(f"M {cx-half_w+8:.1f},{y_off-5:.1f} "
                       f"L {cx-half_w:.1f},{y_off:.1f} "
                       f"L {cx-half_w+8:.1f},{y_off+5:.1f}"),
                    stroke=stroke,
                ))
            # Tick marks to indicate equal spacing
            out['marks'].append(dict(
                type='path',
                d=_tick_path(cx - half_w, cy - offset, cx + half_w, cy - offset),
                stroke=stroke,
            ))
            out['marks'].append(dict(
                type='path',
                d=_tick_path(cx - half_w, cy + offset, cx + half_w, cy + offset),
                stroke=stroke,
            ))

        elif relation == 'perpendicular':
            # Cross: horizontal + vertical
            out['marks'].append(_solid_line(cx - half_w, cy, cx + half_w, cy))
            out['marks'].append(_solid_line(cx, cy - half_h, cx, cy + half_h))
            # Right-angle mark
            sq = 10
            out['marks'].append(dict(
                type='path',
                d=f"M {cx+sq:.1f},{cy:.1f} L {cx+sq:.1f},{cy-sq:.1f} L {cx:.1f},{cy-sq:.1f}",
                stroke=stroke,
            ))
            out['marks'].append(dict(type='dot', x=round(cx, 1), y=round(cy, 1)))

        else:  # intersecting (oblique)
            angle_rad = _math.radians(35)
            out['marks'].append(_solid_line(cx - half_w, cy,
                                            cx + half_w, cy))
            dx = half_w * _math.cos(angle_rad)
            dy = half_w * _math.sin(angle_rad)
            out['marks'].append(_solid_line(cx - dx, cy + dy,
                                            cx + dx, cy - dy))

    # ── polygon (grade-3: name by side count) ────────────────────────────────
    elif stype == 'polygon':
        import math as _math
        sides = int(shape.get('sides', 4))
        r = min(avail_w, avail_h) * 0.42
        cx, cy = vw / 2, vh / 2 + 8
        # Rotate so a flat edge is at the bottom (rotate by -π/sides + π/2 for odd, else -π/sides)
        start_angle = -_math.pi / 2 - (0 if sides % 2 == 0 else 0)
        pts = []
        for i in range(sides):
            a = start_angle + 2 * _math.pi * i / sides
            pts.append((cx + r * _math.cos(a), cy + r * _math.sin(a)))
        path_parts = [f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"]
        for px, py in pts[1:]:
            path_parts.append(f"L {px:.1f},{py:.1f}")
        path_parts.append("Z")
        out['path'] = ' '.join(path_parts)

        # Optional side-count label in centre
        lbs = shape.get('labels', {})
        if lbs.get('inner'):
            out['labels'].append(_label(lbs['inner'], vw / 2, vh / 2 + 6,
                                        size=15, bold=True, color=stroke))

    # ── fraction_bar (grade-3: coloured parts of a bar) ──────────────────────
    elif stype == 'fraction_bar':
        numerator   = int(shape.get('numerator', 1))
        denominator = int(shape.get('denominator', 4))
        if denominator < 1:
            denominator = 1
        numerator = max(0, min(numerator, denominator))

        bar_w = avail_w * 0.88
        bar_h = avail_h * 0.40
        bx    = (vw - bar_w) / 2
        by    = (vh - bar_h) / 2
        part  = bar_w / denominator

        # Draw each part
        for i in range(denominator):
            px = bx + i * part
            is_colored = i < numerator
            part_fill  = fill if is_colored else 'rgba(200,200,200,0.18)'
            part_stroke = stroke
            out['marks'].append(dict(
                type='path',
                d=(f"M {px:.1f},{by:.1f} h {part:.1f} "
                   f"v {bar_h:.1f} h -{part:.1f} Z"),
                stroke=part_stroke,
                fill=part_fill,
                sw=2,
            ))

        # Fraction label below bar
        frac_text = f'{numerator}/{denominator}'
        lbs = shape.get('labels', {})
        out['labels'].append(_label(
            lbs.get('frac', frac_text),
            vw / 2, by + bar_h + 22,
            size=15, bold=True, color=stroke,
        ))

    # ── fraction_circle (grade-3: pie chart style) ────────────────────────────
    elif stype == 'fraction_circle':
        import math as _math
        numerator   = int(shape.get('numerator', 1))
        denominator = int(shape.get('denominator', 4))
        if denominator < 1:
            denominator = 1
        numerator = max(0, min(numerator, denominator))

        r  = min(avail_w, avail_h) * 0.38
        cx = vw / 2
        cy = vh / 2
        out['circle'] = dict(cx=round(cx, 1), cy=round(cy, 1), r=round(r, 1))

        angle_per_slice = 2 * _math.pi / denominator
        start = -_math.pi / 2   # start at 12 o'clock

        # Draw colored sectors
        for i in range(denominator):
            a_start = start + i * angle_per_slice
            a_end   = a_start + angle_per_slice
            x1, y1  = cx + r * _math.cos(a_start), cy + r * _math.sin(a_start)
            x2, y2  = cx + r * _math.cos(a_end),   cy + r * _math.sin(a_end)
            large   = 1 if angle_per_slice > _math.pi else 0
            is_col  = i < numerator
            sec_fill = fill if is_col else 'rgba(200,200,200,0.18)'
            if denominator == 1:
                # Full circle already drawn via out['circle']
                if is_col:
                    out['fill'] = fill
                continue
            out['marks'].append(dict(
                type='path',
                d=(f"M {cx:.1f},{cy:.1f} "
                   f"L {x1:.1f},{y1:.1f} "
                   f"A {r:.1f},{r:.1f} 0 {large},1 {x2:.1f},{y2:.1f} Z"),
                stroke=stroke,
                fill=sec_fill,
                sw=2,
            ))

        # Fraction label
        lbs = shape.get('labels', {})
        frac_text = f'{numerator}/{denominator}'
        out['labels'].append(_label(
            lbs.get('frac', frac_text),
            vw / 2, cy + r + 22,
            size=15, bold=True, color=stroke,
        ))

    # ── fraction expression ───────────────────────────────────────────────────
    elif stype == 'fraction_expr':
        return _render_fraction_expr(shape, vw, vh, pad, color_idx)

    # ── labeled rectangle (grade-3: perimeter with side labels) ─────────────
    elif stype == 'labeled_rect':
        w_val = float(shape.get('w_val', 5))
        h_val = float(shape.get('h_val', 3))
        unit  = shape.get('unit', 'cm')
        dw, dh = _norm_fit(w_val, h_val, avail_w - 10, avail_h - 28)
        x0, y0 = (vw - dw) / 2, (vh - dh) / 2
        x1, y1 = x0 + dw, y0 + dh
        cx_m, cy_m = (x0 + x1) / 2, (y0 + y1) / 2
        out['path'] = (f"M {x0:.1f},{y0:.1f} L {x1:.1f},{y0:.1f} "
                       f"L {x1:.1f},{y1:.1f} L {x0:.1f},{y1:.1f} Z")
        tw = f"{int(w_val)} {unit}"
        th = f"{int(h_val)} {unit}"
        out['labels'].append(_label(tw, cx_m, y0 - 8,  anchor='middle', size=11, bold=True, color=stroke))
        out['labels'].append(_label(tw, cx_m, y1 + 15, anchor='middle', size=11, bold=True, color=stroke))
        out['labels'].append(_label(th, x0 - 10, cy_m + 4, anchor='end',   size=11, bold=True, color=stroke))
        out['labels'].append(_label(th, x1 + 10, cy_m + 4, anchor='start', size=11, bold=True, color=stroke))

    # ── labeled triangle (grade-3: perimeter with side labels) ───────────────
    elif stype == 'labeled_triangle':
        sides    = shape.get('sides', [5, 5, 5])
        unit     = shape.get('unit', 'cm')
        s_vis    = min(avail_w, avail_h - 15) * 0.85
        h_tri    = s_vis * math.sqrt(3) / 2
        cx, cy   = vw / 2, vh / 2 + 6
        p0 = (cx,            cy - h_tri * 2 / 3)
        p1 = (cx - s_vis / 2, cy + h_tri / 3)
        p2 = (cx + s_vis / 2, cy + h_tri / 3)
        pts = [p0, p1, p2]
        out['path'] = (f"M {p0[0]:.1f},{p0[1]:.1f} "
                       f"L {p1[0]:.1f},{p1[1]:.1f} "
                       f"L {p2[0]:.1f},{p2[1]:.1f} Z")
        gx = sum(p[0] for p in pts) / 3
        gy = sum(p[1] for p in pts) / 3
        for i in range(3):
            a_pt, b_pt = pts[i], pts[(i + 1) % 3]
            mx_s, my_s = (a_pt[0] + b_pt[0]) / 2, (a_pt[1] + b_pt[1]) / 2
            dx_s, dy_s = mx_s - gx, my_s - gy
            length_s   = math.sqrt(dx_s * dx_s + dy_s * dy_s) or 1
            off        = 17
            lx_s = mx_s + off * dx_s / length_s
            ly_s = my_s + off * dy_s / length_s
            out['labels'].append(_label(f"{sides[i]} {unit}", lx_s, ly_s,
                                        anchor='middle', size=11, bold=True, color=stroke))

    # ── clock (grade-3: read analog time) ────────────────────────────────────
    elif stype == 'clock':
        hours   = int(shape.get('hours',   3))
        minutes = int(shape.get('minutes', 0))
        r  = min(avail_w, avail_h) * 0.44
        cx, cy = vw / 2, vh / 2
        out['circle'] = dict(cx=round(cx, 1), cy=round(cy, 1), r=round(r, 1))
        for i in range(1, 13):
            ang = math.radians(i * 30 - 90)
            tk  = r * 0.13 if (i % 3 == 0) else r * 0.07
            out['marks'].append(dict(type='line',
                                     x1=round(cx + (r - tk) * math.cos(ang), 1),
                                     y1=round(cy + (r - tk) * math.sin(ang), 1),
                                     x2=round(cx + r * math.cos(ang), 1),
                                     y2=round(cy + r * math.sin(ang), 1),
                                     color=stroke))
            nr = r - tk - r * 0.18
            out['labels'].append(_label(str(i),
                                        cx + nr * math.cos(ang),
                                        cy + nr * math.sin(ang) + 3,
                                        anchor='middle', size=max(7, int(r * 0.22)),
                                        bold=True, color='#1C1018'))
        h_ang = math.radians((hours % 12 + minutes / 60) * 30 - 90)
        out['marks'].append(dict(type='line',
                                  x1=round(cx, 1), y1=round(cy, 1),
                                  x2=round(cx + r * 0.55 * math.cos(h_ang), 1),
                                  y2=round(cy + r * 0.55 * math.sin(h_ang), 1),
                                  color=stroke))
        m_ang = math.radians(minutes * 6 - 90)
        out['marks'].append(dict(type='line',
                                  x1=round(cx, 1), y1=round(cy, 1),
                                  x2=round(cx + r * 0.78 * math.cos(m_ang), 1),
                                  y2=round(cy + r * 0.78 * math.sin(m_ang), 1),
                                  color=stroke))
        out['marks'].append(dict(type='dot', x=round(cx, 1), y=round(cy, 1)))

    # ── bar chart (grade-3: read a bar chart) ─────────────────────────────────
    elif stype == 'bar_chart':
        ch_labels = shape.get('chart_labels', ['A', 'B', 'C'])
        ch_values = shape.get('chart_values', [5, 8, 3])
        highlight = shape.get('highlight',    None)
        left_m, bottom_m, top_m, right_m = 28, vh - 20, 10, vw - 6
        plot_h   = bottom_m - top_m
        plot_w   = right_m  - left_m
        max_v    = max(ch_values) if ch_values else 10
        nice_max = max_v + (0 if max_v % 2 == 0 else 1)
        n        = len(ch_labels)
        bar_area = plot_w / n
        bar_w    = bar_area * 0.58
        out['marks'].append(dict(type='line', x1=left_m, y1=top_m,    x2=left_m,   y2=bottom_m, color='#374151'))
        out['marks'].append(dict(type='line', x1=left_m, y1=bottom_m, x2=right_m,  y2=bottom_m, color='#374151'))
        for tv in [0, nice_max // 2, nice_max]:
            ty = bottom_m - (tv / nice_max * plot_h if nice_max else 0)
            out['marks'].append(dict(type='line', x1=left_m - 3, y1=ty, x2=left_m, y2=ty, color='#374151'))
            out['labels'].append(_label(str(tv), left_m - 5, ty + 3,
                                        anchor='end', size=8, bold=False, color='#374151'))
        for i, (lab, val) in enumerate(zip(ch_labels, ch_values)):
            bcx  = left_m + (i + 0.5) * bar_area
            bx   = bcx - bar_w / 2
            btop = bottom_m - (val / nice_max * plot_h if nice_max else 0)
            rect = (f"M {bx:.1f},{btop:.1f} "
                    f"L {bx + bar_w:.1f},{btop:.1f} "
                    f"L {bx + bar_w:.1f},{bottom_m:.1f} "
                    f"L {bx:.1f},{bottom_m:.1f} Z")
            bar_col = stroke if lab == highlight else fill
            out['marks'].append(dict(type='path', d=rect, fill=bar_col, stroke=stroke, sw='1.5'))
            out['labels'].append(_label(lab, bcx, bottom_m + 13,
                                        anchor='middle', size=8, bold=True, color='#374151'))

    # ── grid point (grade-3: cartesian coordinates) ───────────────────────────
    elif stype == 'grid_point':
        px        = int(shape.get('px', 3))
        py        = int(shape.get('py', 2))
        grid_size = int(shape.get('grid_size', 6))
        # Layout: origin bottom-left, axes with tick labels
        margin    = 22
        cell      = min((vw - margin - 10) / grid_size, (vh - margin - 10) / grid_size)
        ox        = margin                       # origin x in SVG
        oy        = vh - margin                  # origin y in SVG (y-axis flipped)
        # Axis lines
        out['marks'].append(dict(type='line', x1=ox, y1=oy, x2=ox + grid_size * cell, y2=oy, color='#374151'))
        out['marks'].append(dict(type='line', x1=ox, y1=oy, x2=ox, y2=oy - grid_size * cell, color='#374151'))
        # Grid lines + tick labels
        for i in range(0, grid_size + 1):
            gx_i = ox + i * cell
            gy_i = oy - i * cell
            # Vertical grid line
            out['marks'].append(dict(type='line', x1=gx_i, y1=oy, x2=gx_i, y2=oy - grid_size * cell, color='#D1D5DB'))
            # Horizontal grid line
            out['marks'].append(dict(type='line', x1=ox, y1=gy_i, x2=ox + grid_size * cell, y2=gy_i, color='#D1D5DB'))
            # X-axis label
            out['labels'].append(_label(str(i), gx_i, oy + 12, anchor='middle', size=9, bold=True, color='#374151'))
            # Y-axis label
            if i > 0:
                out['labels'].append(_label(str(i), ox - 7, gy_i + 3, anchor='end', size=9, bold=True, color='#374151'))
        # The point
        svgx = ox + px * cell
        svgy = oy - py * cell
        out['marks'].append(dict(type='dot', x=round(svgx, 1), y=round(svgy, 1)))
        # Label "A" above the dot
        out['labels'].append(_label('A', svgx, svgy - 8, anchor='middle', size=11, bold=True, color=stroke))

    # ── thermometer ─────────────────────────────────────────────────────────
    elif stype == 'thermometer':
        temp     = shape.get('temp', 20)
        min_temp = shape.get('min_temp', 0)
        max_temp = shape.get('max_temp', 40)
        step     = shape.get('step', 5)

        # Layout
        tube_x   = vw / 2
        tube_top = 30
        tube_bot = vh - 50
        tube_h   = tube_bot - tube_top
        tube_r   = 8     # inner radius
        bulb_r   = 18    # bulb radius
        bulb_cy  = tube_bot + bulb_r - 4
        label_x  = tube_x + tube_r + 22

        temp_range = max_temp - min_temp
        def _t2y(t):
            """Temperature → SVG y (higher temp = smaller y)."""
            frac = (t - min_temp) / temp_range
            return tube_bot - frac * tube_h

        fill_y   = _t2y(temp)
        fill_h   = tube_bot - fill_y

        mercury  = '#EF4444'
        mercury_t = 'rgba(239,68,68,0.25)'

        # Tube background
        out['lines'].append(dict(
            x1=tube_x - tube_r, y1=tube_top,
            x2=tube_x - tube_r, y2=tube_bot,
            stroke='#9CA3AF', width=1,
        ))
        out['lines'].append(dict(
            x1=tube_x + tube_r, y1=tube_top,
            x2=tube_x + tube_r, y2=tube_bot,
            stroke='#9CA3AF', width=1,
        ))
        # Mercury fill rect (drawn as a thin mark)
        if fill_h > 0:
            out['marks'].append(dict(
                type='rect',
                x=round(tube_x - tube_r + 1, 1),
                y=round(fill_y, 1),
                w=round(tube_r * 2 - 2, 1),
                h=round(fill_h + bulb_r, 1),
                fill=mercury,
                stroke='none',
            ))
        # Bulb circle
        out['marks'].append(dict(
            type='circle',
            cx=round(tube_x, 1),
            cy=round(bulb_cy, 1),
            r=bulb_r,
            fill=mercury,
            stroke='#9CA3AF',
            stroke_width=1,
        ))
        # Tick marks and labels
        t = min_temp
        while t <= max_temp:
            ty = _t2y(t)
            tick_len = 12 if t % (step * 2) == 0 else 7
            out['lines'].append(dict(
                x1=round(tube_x + tube_r, 1), y1=round(ty, 1),
                x2=round(tube_x + tube_r + tick_len, 1), y2=round(ty, 1),
                stroke='#374151', width=1,
            ))
            if t % (step * 2) == 0 or step >= 10:
                out['labels'].append(_label(
                    f"{t} °C", label_x + tick_len - 2, ty + 4,
                    anchor='start', size=9, bold=False, color='#374151',
                ))
            t += step

    # ── number_line_svg ──────────────────────────────────────────────────────
    elif stype == 'number_line_svg':
        nl_start  = shape.get('nl_start', 0)
        nl_end    = shape.get('nl_end', 100)
        nl_step   = shape.get('nl_step', 10)
        nl_target = shape.get('nl_target', 50)

        margin_l = 40
        margin_r = 40
        line_y   = vh / 2
        line_w   = vw - margin_l - margin_r
        n_ticks  = round((nl_end - nl_start) / nl_step) + 1
        tick_gap = line_w / (n_ticks - 1) if n_ticks > 1 else line_w

        # Main axis
        lx = margin_l
        rx = vw - margin_r
        out['lines'].append(dict(x1=lx, y1=line_y, x2=rx, y2=line_y, stroke='#374151', width=2))

        for i in range(n_ticks):
            val = nl_start + i * nl_step
            x   = round(lx + i * tick_gap, 1)
            is_target = (val == nl_target)
            tick_h = 12 if not is_target else 16
            out['lines'].append(dict(
                x1=x, y1=round(line_y - tick_h / 2, 1),
                x2=x, y2=round(line_y + tick_h / 2, 1),
                stroke='#374151', width=2 if not is_target else 1,
            ))
            out['labels'].append(_label(
                str(val), x, round(line_y + tick_h / 2 + 14, 1),
                anchor='middle', size=10, bold=is_target, color='#374151',
            ))

        # Target dot + question mark
        tx = round(lx + ((nl_target - nl_start) / nl_step) * tick_gap, 1)
        out['marks'].append(dict(type='dot', x=tx, y=round(line_y - 18, 1)))
        out['labels'].append(_label('?', tx, round(line_y - 28, 1),
                                    anchor='middle', size=13, bold=True, color=stroke))

    # ── pie_chart_multi ──────────────────────────────────────────────────────
    elif stype == 'pie_chart_multi':
        categories   = shape.get('categories', ['A', 'B'])
        proportions  = shape.get('proportions', [50, 50])
        highlight    = shape.get('highlight', None)   # category name to emphasise

        cx_pie = vw / 2 - 20
        cy_pie = vh / 2
        r_pie  = min(vw, vh) * 0.34

        total     = sum(proportions)
        angle_deg = -90.0   # start at top
        pie_fills = ['#2563EB', '#EF4444', '#16A34A', '#D97706', '#9333EA', '#0891B2']
        legend_y0 = cy_pie - r_pie * 0.6
        legend_x  = cx_pie + r_pie + 18

        for idx, (cat, prop) in enumerate(zip(categories, proportions)):
            sweep = 360 * prop / total
            a1    = math.radians(angle_deg)
            a2    = math.radians(angle_deg + sweep)
            lx1   = cx_pie + r_pie * math.cos(a1)
            ly1   = cy_pie + r_pie * math.sin(a1)
            lx2   = cx_pie + r_pie * math.cos(a2)
            ly2   = cy_pie + r_pie * math.sin(a2)
            large = 1 if sweep > 180 else 0
            fill_c = pie_fills[idx % len(pie_fills)]
            alpha  = '0.90' if (highlight is None or cat == highlight) else '0.30'

            out['marks'].append(dict(
                type='pie_slice',
                cx=round(cx_pie, 1), cy=round(cy_pie, 1),
                r=round(r_pie, 1),
                lx1=round(lx1, 1), ly1=round(ly1, 1),
                lx2=round(lx2, 1), ly2=round(ly2, 1),
                large_arc=large,
                fill=fill_c,
                alpha=alpha,
                stroke='#fff',
            ))
            # Percentage label inside slice
            mid_a = math.radians(angle_deg + sweep / 2)
            lbl_x = cx_pie + r_pie * 0.62 * math.cos(mid_a)
            lbl_y = cy_pie + r_pie * 0.62 * math.sin(mid_a)
            out['labels'].append(_label(
                f"{prop}%", round(lbl_x, 1), round(lbl_y + 4, 1),
                anchor='middle', size=10, bold=True, color='#fff',
            ))
            # Legend swatch + text
            swatch_y = legend_y0 + idx * 22
            out['marks'].append(dict(
                type='rect',
                x=round(legend_x, 1), y=round(swatch_y - 9, 1),
                w=14, h=14,
                fill=fill_c, stroke='none',
            ))
            out['labels'].append(_label(
                cat, legend_x + 18, swatch_y + 4,
                anchor='start', size=10, bold=(cat == highlight), color='#1E293B',
            ))
            angle_deg += sweep

    # ── arithmetic expression ────────────────────────────────────────────────
    elif stype == 'expression':
        op1      = str(shape.get('op1', ''))
        operator = shape.get('operator', '+')
        op2      = str(shape.get('op2', ''))
        result   = str(shape.get('result', '?'))
        fmt      = shape.get('format', 'horizontal')

        OP_COLORS = {'+': '#22C55E', '−': '#EF4444', '-': '#EF4444',
                     '×': '#a78bfa', '*': '#a78bfa',
                     '÷': '#F59E0B', '/': '#F59E0B'}
        op_color = OP_COLORS.get(operator, stroke)

        if fmt == 'horizontal':
            fsize  = 32
            cw     = fsize * 0.60      # approx digit width
            gap    = fsize * 0.65      # gap between tokens
            parts  = [
                (op1,      '#1E0A3C'),
                (operator, op_color),
                (op2,      '#1E0A3C'),
                ('=',      'rgba(255,255,255,0.30)'),
                (result,   stroke),
            ]
            widths = [max(len(t), 1) * cw for t, _ in parts]
            total  = sum(widths) + gap * (len(parts) - 1)
            x      = (vw - total) / 2
            cy     = vh / 2 + fsize * 0.38
            for (text, color), w in zip(parts, widths):
                out['labels'].append(_label(text, x + w / 2, cy,
                                            anchor='middle', size=fsize,
                                            bold=True, color=color))
                x += w + gap

        elif fmt == 'vertical':
            fsize  = 30
            cw     = fsize * 0.65
            # width = longest of (op1, op2+operator_slot)
            line_w = max(len(op1), len(op2) + 2) * cw + 24
            cx     = vw / 2
            lx, rx = cx - line_w / 2, cx + line_w / 2

            y1     = vh / 2 - 28    # op1 row
            y2     = vh / 2 + 4     # operator + op2 row
            bar_y  = y2 + 16        # horizontal rule
            y3     = bar_y + fsize  # result row

            # op1 — right-aligned
            out['labels'].append(_label(op1, rx - 6, y1,
                                        anchor='end', size=fsize,
                                        bold=True, color='#1E0A3C'))
            # operator — left-aligned, op2 — right-aligned
            out['labels'].append(_label(operator, lx + 6, y2,
                                        anchor='start', size=fsize,
                                        bold=True, color=op_color))
            out['labels'].append(_label(op2, rx - 6, y2,
                                        anchor='end', size=fsize,
                                        bold=True, color='#1E0A3C'))
            # dividing bar
            out['marks'].append(_solid_line(lx, bar_y, rx, bar_y))
            # result — right-aligned
            out['labels'].append(_label(result, rx - 6, y3,
                                        anchor='end', size=fsize,
                                        bold=True, color=stroke))

    return out


def render_shapes(shape_data: list, count_override: int | None = None) -> list:
    """
    Render a list of shape dicts.
    Chooses canvas size by shape type and count.
    """
    n = count_override or len(shape_data)
    is_expr        = shape_data and all(s.get('type') == 'expression'      for s in shape_data)
    is_frac_expr   = shape_data and all(s.get('type') == 'fraction_expr'   for s in shape_data)
    is_thermometer = shape_data and shape_data[0].get('type') == 'thermometer'
    is_number_line = shape_data and shape_data[0].get('type') == 'number_line_svg'
    is_pie_chart   = shape_data and shape_data[0].get('type') == 'pie_chart_multi'

    if is_thermometer:
        vw, vh, pad = 160, 260, 10
    elif is_number_line:
        vw, vh, pad = 340, 100, 14
    elif is_pie_chart:
        vw, vh, pad = 340, 200, 12
    elif is_frac_expr:
        # Fraction expressions need extra width for stacked numerator/denominator
        vw, vh, pad = 360, 155, 18
    elif is_expr:
        # Arithmetic expressions — wide and short, one row each
        vw, vh, pad = 300, 140, 18
    elif n == 1:
        vw, vh = 280, 190
        pad = max(28, vw * 0.12)
    elif n == 2:
        vw, vh = 210, 165
        pad = max(28, vw * 0.12)
    else:
        vw, vh = 180, 145
        pad = max(28, vw * 0.12)

    return [render_shape(s, vw=vw, vh=vh, pad=pad, color_idx=i)
            for i, s in enumerate(shape_data)]
