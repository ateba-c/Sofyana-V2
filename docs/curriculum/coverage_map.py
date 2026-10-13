# Usage: python docs/curriculum/coverage_map.py docs/curriculum/AUDIT_REFERENCE.md <out.md>
# Builds the per-entry coverage table from the audit matrix + a hand-made status map.
# C = covered, P = partial, M = missing, X = off-screen (physical manipulation / calculator), D = decision needed
import sys, io, collections, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
AUDIT = sys.argv[1]

S = {
# ── Numération: naturels
1: ('P', 'g4-before-after, number-sequence', 'No G1–2 counting (<100) — WP1'),
2: ('P', 'number-sequence, g4-skip-sequence', 'Descending only at hard; nothing for G1–2 — WP1'),
3: ('C', 'number-sequence, g4-skip-sequence', 'Add G1–2 range (by 2, 5, 10 under 100) — WP1'),
4: ('M', '—', 'Count a drawn collection (tap/type) — WP1'),
5: ('M', '—', 'Count on from a given number — WP1'),
6: ('P', 'count-groups', 'Text only; needs drawn groups of 10 — WP1'),
7: ('C', 'count-groups, g4-grouping-problem, g6-count-groups', ''),
8: ('P', 'read-number, write-number, g5-large-integer', 'Writing stops at 9 999; G5–6 need typed up to 999 999. EN sessions show French number words — WP0'),
9: ('M', '—', 'Visual grouped objects (bags of 10) — WP1'),
10: ('P', 'base10-match, build-number', 'Text "3 centaines…", no base-10 block picture — WP1'),
11: ('P', 'money-match, g6-symbol-form', 'No abacus picture — WP1'),
12: ('C', 'expanded-form, decomposition-match, g4-expanded-form, g6-additive-form, g6-symbol-form, g6-multiplicative-form', 'Add non-standard splits (123 = 50+50+23) — WP4'),
13: ('M', '—', 'Equivalent expressions (52 = 40+12 = 104÷2) — WP4'),
14: ('C', 'compare-int, g4-compare, g6-compare', 'Add G1–2 range — WP1'),
15: ('C', 'order-numbers, g4-order-numbers, g6-order, g6-extreme', ''),
16: ('P', 'even-odd, squares, primes, number-classify', 'No triangular numbers; no "describe the rule" — WP4'),
17: ('P', 'g4-number-line-point, g5-number-line', 'No hundred chart — WP1'),
18: ('C', 'even-odd, number-classify', ''),
19: ('C', 'squares, primes, number-classify', ''),
20: ('C', 'number-classify, primes (match)', ''),
21: ('P', 'round-ten, round-hundred', 'Rounding yes; estimating a drawn collection no — WP1'),
22: ('P', 'squares (N²)', 'No cubes / exponent notation 2³ — WP4'),
23: ('P', 'compare-int, digit-position', 'Vocabulary used, never assessed — WP10'),
24: ('P', 'digit-position, g4-digit-position, primes', 'No ≠ symbol — WP10'),
25: ('P', 'g6-digit-position, squares', 'No exponent/cube vocabulary — WP4'),
# ── Fractions
26: ('P', 'fraction-shape', 'G3 skill; no G1–2 half/third/quarter of everyday objects — WP1'),
27: ('C', 'fraction-shape, fraction-collection', 'Only bar pictures; add circles, sets — WP2'),
28: ('C', 'fraction-shape, fraction-collection', ''),
29: ('M', '—', 'Senses of a fraction (sharing, division 3÷4 = 3/4, ratio) — WP2'),
30: ('P', 'fraction-shape (distractor feedback)', 'Needs explicit numerator/denominator items — WP2'),
31: ('M', '—', 'Read/write "trois quarts" ↔ 3/4 — WP2'),
32: ('P', 'compare-fraction (vs 1)', 'No comparing to 0 or to ½ — WP2'),
33: ('M', '—', 'Equivalent fractions (visual, then numeric) — WP2'),
34: ('P', 'fraction-to-decimal (tenths), g5-probability-forms', 'No hundredths, no percentages in context — WP3'),
35: ('C', 'g6-fraction-order', ''),
36: ('P', 'compare-fraction', 'Not limited to "one denominator a multiple of the other" — WP2'),
37: ('P', 'compare-fraction (hard)', 'Not a dedicated same-numerator item — WP2'),
38: ('C', 'g6-fraction-on-line, g6-fraction-between', ''),
39: ('P', 'fraction-shape', 'No demi/tiers/quart vocabulary item — WP2'),
40: ('P', '—', 'Numerator/denominator, equivalent fraction vocabulary — WP2'),
# ── Décimaux
41: ('P', 'g5-decimal-forms', 'No pictures (10×10 grid, money) — WP3'),
42: ('P', 'g5-decimal-forms', 'Text only — WP3'),
43: ('C', 'read-decimal, g5-decimal-write', 'read-decimal goes to ten-thousandths (out of scope) — WP0'),
44: ('P', 'g5-decimal-write', 'No item on the role of the decimal point — WP3'),
45: ('C', 'g5-decimal-write', ''),
46: ('P', 'g5-decimal-forms', 'No 12 tenths = 1.2 or 0.5 = 0.50 items — WP3'),
47: ('M', '—', 'Decimals on a number line between two whole numbers — WP3'),
48: ('M', '—', 'Decimals on a number line between two decimals — WP3'),
49: ('C', 'compare-decimal', ''),
50: ('M', '—', 'Round / truncate decimals — WP3'),
51: ('C', 'compare-decimal (sort)', ''),
52: ('P', 'fraction-to-decimal', 'Tenths only — WP3'),
53: ('P', 'g5-probability-forms', 'Only inside probability — WP3'),
54: ('P', 'g5-decimal-write', 'Vocabulary not assessed — WP10'),
55: ('C', 'g5-decimal-write (hard)', ''),
# ── Entiers relatifs
56: ('D', '—', 'Conflicts with the "no negatives" rule — WP9'),
57: ('D', '—', 'WP9'),
58: ('D', 'cartesian-coord (1st quadrant only)', 'WP9'),
59: ('D', 'g5-temperature (positive only)', 'WP9'),
60: ('D', '—', 'WP9'),
61: ('D', '—', 'WP9'),
# ── Sens des opérations
62: ('C', 'choose-operation, multiply-context, word-problem', 'Add G1–2 range — WP1'),
63: ('P', 'word-problem, missing-addend (resolution)', 'Meanings of +/− (join, separate, compare) not distinguished; no schemas — WP4'),
64: ('P', 'word-problem', 'Same as above — WP4'),
65: ('P', 'g6-comparative-phrase', 'Comparison meaning only — WP4'),
66: ('M', '—', 'G1–2 equal groups / sharing pictures — WP1'),
67: ('C', 'multiply-context, repeated-addition, division-sharing', 'Add "how many groups" division and arrays — WP4'),
68: ('M', '—', 'True/false equalities (3 + 2 = 6 − 1) — WP4'),
69: ('P', 'fact-family', 'Multiplication only; need +/− fact families — WP4'),
70: ('P', 'fact-family', 'No commutativity/associativity items — WP4'),
71: ('M', '—', 'Distributivity (7 × 12 = 7 × 10 + 7 × 2) — WP4'),
72: ('P', 'g5-decimal-mult (resolution: "one expression")', 'Need "pick the expression for this story" — WP4'),
73: ('P', 'choose-operation', 'Vocabulary not assessed — WP10'),
74: ('P', 'fact-family', 'Factor/product/quotient/remainder vocabulary — WP10'),
75: ('P', 'g5 resolution (money)', 'Decimal +/− stories not a dedicated skill — WP3'),
76: ('P', 'g5 resolution (money)', 'WP3'),
77: ('P', 'g5 resolution (money)', 'WP3'),
78: ('P', 'g5-order-ops resolution (unit price)', 'WP3'),
79: ('M', '—', 'Decimal equivalences via properties — WP3'),
80: ('M', '—', 'WP3'),
81: ('P', 'g5-order-ops', 'Natural numbers only — WP3'),
82: ('P', 'fraction-shape/-collection resolution', 'Stories of a fraction of a quantity only — WP2'),
# ── Calcul: naturels
83: ('P', 'round-ten/round-hundred resolution', 'No "estimate this sum" item — WP4'),
84: ('P', 'g6-estimate-product, g6-rate-problem', 'No division estimate — WP4'),
85: ('P', 'add/subtract (easy)', 'Not restricted to 0+0…10+10; no G1–2 fact skill — WP1'),
86: ('M', '—', 'Strategies (doubles, make-10) — WP1'),
87: ('P', 'add/subtract (easy)', 'No timed fluency mode — WP4'),
88: ('P', 'add/subtract', 'Multiple choice; no mental-math framing — WP0/WP4'),
89: ('P', 'multiply/divide', 'Multiple choice — WP0'),
90: ('M', '—', 'G1–2 add/sub with drawings (number line, base-10) — WP1'),
91: ('P', 'add (hard)', 'Multiple choice; no column layout — WP0/WP4'),
92: ('P', 'subtract (hard)', 'Multiple choice; no column layout — WP0/WP4'),
93: ('C', 'missing-addend, missing-subtrahend', 'Lacks □ + b = c and □ − b = c forms — WP4'),
94: ('P', 'multiply/divide (easy), fact-family', 'Not restricted to 0×0…10×10 tables — WP4'),
95: ('M', '—', 'Multiplication strategies (doubling, ×5 = ×10 ÷ 2) — WP4'),
96: ('P', 'multiply (easy)', 'No timed tables mode — WP4'),
97: ('P', 'repeated-addition, division-sharing', 'No arrays/drawings — WP4'),
98: ('C', 'g6-multiply, g6-partial-products', ''),
99: ('P', 'divide (hard)', 'Multiple choice; no long-division steps; remainders only in resolution — WP4'),
100: ('M', '—', 'Missing factor/divisor (a × □ = c) — WP4'),
101: ('M', '—', 'Prime factorisation (factor tree) — WP4'),
102: ('P', 'squares (N²)', 'No powers beyond squares — WP4'),
103: ('M', '—', 'Divisibility by 2, 3, 4, 5, 6, 8, 9, 10 — WP4'),
104: ('C', 'g5-order-ops', ''),
105: ('M', '—', 'Non-numeric patterns (shapes/colours) — WP1'),
106: ('C', 'number-sequence, g4-skip-sequence', ''),
107: ('P', 'number-sequence', 'Only +/− constant steps; no ×2, square or triangular sequences — WP4'),
108: ('C', 'number-sequence, g4-skip-sequence', ''),
109: ('X', '—', 'Calculator use — out of scope (optional on-screen calculator)'),
110: ('X', '—', 'Calculator'),
111: ('X', '—', 'Calculator'),
112: ('P', 'number-sequence', 'Vocabulary — WP10'),
# ── Calcul: fractions
113: ('M', '—', 'Build equivalent fractions — WP2'),
114: ('M', '—', 'Simplify a fraction (dedicated skill) — WP2'),
115: ('P', 'fraction-add, fraction-subtract', 'Generators exceed scope (unrelated denominators); need a scoped G6 skill — WP2'),
116: ('M', 'fraction-multiply is fraction × fraction', 'Whole number × fraction (3 × 2/5, ⅓ of 12) — WP2'),
117: ('M', '—', 'Simplest-form vocabulary — WP2'),
# ── Calcul: décimaux
118: ('M', '—', 'Estimate a decimal sum/difference — WP3'),
119: ('M', '—', 'Estimate a decimal product/quotient — WP3'),
120: ('P', 'decimal-add, decimal-subtract', 'Multiple choice — WP0'),
121: ('P', 'g5-decimal-mult, g5-decimal-div', ''),
122: ('P', 'decimal-divide (÷10)', 'No ×10/100/1000 or ÷100/1000 skill — WP3'),
123: ('C', 'decimal-add, decimal-subtract', 'Switch to typed answers — WP0'),
124: ('P', 'decimal-multiply', 'Hard goes to thousandths (out of scope); g5-decimal-mult covers decimal × whole only — WP0/WP3'),
125: ('C', 'g5-decimal-div, decimal-divide', ''),
126: ('C', 'money-change, money-match', ''),
# ── Utilisation des nombres
127: ('P', 'fraction-to-decimal, g5-decimal-forms', 'Decimal → fraction direction weak — WP3'),
128: ('P', 'g5-probability-forms', 'Only as matching inside probability — WP3'),
129: ('P', 'g5-probability-forms', 'WP3'),
130: ('M', '—', 'Choose the right notation for the context — WP3'),
131: ('P', 'g5-pie-chart', 'Percentage never taught on its own — WP3'),
# ── Géométrie: espace
132: ('M', '—', 'Spatial relations (left/right, above/below) — WP5'),
133: ('M', '—', 'Locate on a map/grid (B3, routes) — WP5'),
134: ('C', 'g4-number-line-point, g5-number-line, g6-fraction-on-line', ''),
135: ('C', 'cartesian-coord', 'Ask to place a point too, not only read — WP5'),
136: ('D', '—', 'Four quadrants need negatives — WP9'),
137: ('P', 'cartesian-coord', 'WP10'),
138: ('C', 'cartesian-coord (hard)', ''),
# ── Solides
139: ('M', '—', 'Match everyday objects to solids (ball → sphere) — WP5'),
140: ('X', '—', 'Building solids is physical; offer a guided activity'),
141: ('P', 'identify-solid', 'Matches text descriptions; no pictures of the solids — WP5'),
142: ('P', 'identify-solid', 'Flat/curved surface vocabulary — WP5'),
143: ('P', 'identify-solid, g5-solid-counts', 'No "which faces does this prism have" item — WP5'),
144: ('C', 'identify-solid, g5-solid-counts', ''),
145: ('M', '—', 'Classify prisms vs pyramids — WP5'),
146: ('M', '—', 'Nets — WP5'),
147: ('M', '—', 'Match prism ↔ net — WP5'),
148: ('M', '—', 'Match pyramid ↔ net — WP5'),
149: ('M', '—', 'Convex polyhedron ↔ net — WP5'),
150: ('P', 'g5-solid-counts', 'Net vocabulary missing — WP5'),
151: ('C', 'g5-euler', ''),
152: ('P', 'g5-euler', 'Polyhedron/convex not taught — WP5'),
# ── Figures planes
153: ('M', '—', 'Open/closed, curved/broken lines — WP1'),
154: ('P', 'name-polygon, g4-quadrilateral-name', 'No circle or rhombus at G1–2 level — WP1'),
155: ('C', 'g4-quadrilateral-riddle, count-sides', ''),
156: ('P', 'name-polygon', 'WP10'),
157: ('M', '—', 'Convex / non-convex polygons — WP5'),
158: ('C', 'parallel-perp, g4-lines', 'Identify only (construction off-screen)'),
159: ('C', 'g4-quadrilateral-riddle, g4-quadrilateral-count, g4-quadrilateral-match', ''),
160: ('C', 'g4-quadrilateral-name, g4-quadrilateral-match', ''),
161: ('P', 'g4-quadrilateral-*', 'No ⊥ // symbols — WP10'),
162: ('M', '—', 'Triangles: scalene/isosceles/equilateral/right — WP5'),
163: ('M', '—', 'Classify triangles — WP5'),
164: ('M', '—', 'Circle: radius, diameter, circumference, central angle — WP5'),
165: ('M', '—', 'WP5'),
# ── Frises et dallages
166: ('M', '—', 'Congruent (isometric) figures — WP5'),
167: ('M', '—', 'Geometric patterns — WP1/WP5'),
168: ('M', '—', 'Reflection / line of symmetry — WP5'),
169: ('M', '—', 'Translation — WP5'),
170: ('M', '—', 'WP5'),
171: ('M', '—', 'WP5'),
# ── Longueurs
172: ('M', '—', 'Compare lengths (pictures) — WP1'),
173: ('X', '—', 'Building rulers is physical'),
174: ('M', '—', 'Measure with non-standard units (paper clips) — WP1'),
175: ('M', '—', 'Read a ruler (cm) — WP6'),
176: ('M', 'measure-unit (choose unit)', 'Read a ruler in mm — WP6'),
177: ('P', 'measure-unit', 'Estimating km — WP6'),
178: ('C', 'convert-length', 'Generic skill includes units outside the list — WP0'),
179: ('C', 'convert-length', ''),
180: ('C', 'perimeter-labeled, geometry-perimeter', ''),
181: ('P', 'measure-unit', 'WP10'),
182: ('C', 'perimeter-labeled, convert-length', ''),
183: ('C', 'measure-unit, convert-length', ''),
# ── Surfaces / volumes
184: ('M', '—', 'Area by counting squares — WP6'),
185: ('P', 'geometry-area', 'Formula only, unitless; no cm²/m² — WP6'),
186: ('P', 'geometry-area', 'WP10'),
187: ('M', '—', 'cm², dm², m² — WP6'),
188: ('M', '—', 'Volume by counting cubes — WP6'),
189: ('C', 'g5-volume', ''),
190: ('C', 'g5-volume', ''),
191: ('P', 'g5-volume', 'No dm³ or cm³ ↔ L — WP6'),
# ── Angles
192: ('P', 'identify-angle', 'Classifies one angle; no comparing two — WP6'),
193: ('C', 'identify-angle', ''),
194: ('M', '—', 'Estimate/measure angles in degrees (on-screen protractor) — WP6'),
195: ('M', '—', 'WP6'),
# ── Capacités / masses
196: ('M', '—', 'Non-standard capacity (how many cups fill the jug) — WP6'),
197: ('P', 'unit-by-quantity', 'Unit choice only; no estimating amounts — WP6'),
198: ('C', 'g5-capacity-convert, convert-volume', ''),
199: ('C', 'unit-by-quantity, g5-capacity-convert', ''),
200: ('M', '—', 'Balance scales — WP6'),
201: ('P', 'unit-by-quantity', 'No estimating or reading a scale — WP6'),
202: ('C', 'g5-mass-convert, convert-mass', ''),
203: ('C', 'g5-mass-convert', ''),
# ── Temps / températures
204: ('C', 'read-clock, g4-elapsed-time, g4-end-time, clock skills', 'No G1–2 o’clock/half-past skill — WP1'),
205: ('C', 'time-convert, g4-time-units', ''),
206: ('C', 'read-clock, g4-clock-24h', ''),
207: ('P', 'time-convert', 'No calendar, days of the week, months or seasons — WP1/WP6'),
208: ('P', 'g5-thermometer, g5-temperature', 'Positive only (see WP9); nothing below G5 — WP6'),
209: ('C', 'g5-thermometer', ''),
# ── Statistique
210: ('M', '—', 'Pick a good survey question — WP7'),
211: ('P', 'g5-data-table', 'Read only; no tallying/organising — WP7'),
212: ('P', 'read-bar-chart', 'No pictograph — WP7'),
213: ('M', '—', 'Line graph — WP7'),
214: ('C', 'g5-pie-chart, read-bar-chart, g5-data-table', ''),
215: ('M', '—', 'Build a bar chart/pictograph (interactive) — WP7'),
216: ('M', '—', 'Build bar chart/line graph — WP7'),
217: ('C', 'g5-arithmetic-mean', ''),
218: ('P', 'read-bar-chart', 'WP10'),
219: ('M', '—', 'WP7'),
220: ('C', 'g5-pie-chart, g5-arithmetic-mean', ''),
# ── Probabilité
221: ('M', '—', 'Variability of outcomes — WP8'),
222: ('M', '—', 'Equally likely (fair die, spinner) — WP8'),
223: ('M', '—', 'Independence of trials ("after 3 heads…") — WP8'),
224: ('M', '—', 'Virtual experiments (dice, spinners) — WP8'),
225: ('C', 'probability-vocab', ''),
226: ('P', 'probability-vocab', 'No "equally likely" or comparing two events — WP8'),
227: ('M', '—', 'Prediction vs result — WP8'),
228: ('M', '—', 'Record results in a table — WP8'),
229: ('P', 'g5-count-outcomes', 'G5 only; G1–2 simple listing missing — WP8'),
230: ('P', 'g5-count-outcomes', 'Multiplication only; no tree diagram picture — WP8'),
231: ('M', '—', 'Theoretical vs experimental probability — WP8'),
232: ('P', 'g5-probability-frac', 'No 0–1 probability line — WP8'),
233: ('C', 'g5-probability-frac, g5-probability-forms', ''),
234: ('M', '—', 'Compare experiment with theory — WP8'),
235: ('M', '—', 'Simulation — WP8'),
236: ('P', 'probability-vocab', 'WP10'),
}

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from coverage_upgrades import UPGRADES  # noqa: E402
S.update(UPGRADES)

rows = []
for l in open(AUDIT, encoding='utf-8'):
    if not l.startswith('| QC-'):
        continue
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    n = int(c[0][3:])
    dom = c[1]
    t = c[2]
    t = re.sub(r'\s+', ' ', t)
    if len(t) > 140:
        t = t[:140].rstrip() + '…'
    grades = ' '.join(x if x != '—' else '·' for x in c[3:9])
    rows.append((n, dom, t, grades))
assert len(rows) == 236 and set(S) == set(range(1, 237)), (len(rows), set(range(1, 237)) - set(S))

def field(dom):
    if dom.startswith('Arithmétique'):
        return 'Arithmetic'
    return dom.split('/')[0].strip()

LBL = {'C': 'Covered', 'P': 'Partial', 'M': 'Missing', 'X': 'Off-screen', 'D': 'Decision needed'}
tot = collections.Counter(S[n][0] for n, *_ in rows)
byf = collections.defaultdict(collections.Counter)
for n, dom, t, g in rows:
    byf[field(dom)][S[n][0]] += 1

# entries whose G1/G2 columns are active
g12 = [n for n, d, t, g in rows if g.split()[0] != '·' or g.split()[1] != '·']
g12c = collections.Counter(S[n][0] for n in g12)

out = []
out.append('| Field | Entries | Covered | Partial | Missing | Off-screen | Decision |')
out.append('|---|---|---|---|---|---|---|')
for f in ['Arithmetic', 'Géométrie', 'Mesure', 'Statistique', 'Probabilité']:
    c = byf[f]
    out.append(f"| {f} | {sum(c.values())} | {c['C']} | {c['P']} | {c['M']} | {c['X']} | {c['D']} |")
out.append(f"| **Total** | **236** | **{tot['C']}** | **{tot['P']}** | **{tot['M']}** | **{tot['X']}** | **{tot['D']}** |")
out.append('')
out.append(f"Entries active in grade 1 or 2: {len(g12)}. Covered {g12c['C']}, partial {g12c['P']}, missing {g12c['M']}, off-screen {g12c['X']} (most 'covered' ones are only covered by grade 3+ skills with larger numbers).")
summary = '\n'.join(out)

tbl = ['| ID | Objective | 1 2 3 4 5 6 | Status | Sofyana skills | Gap / action |', '|---|---|---|---|---|---|']
cur = None
for n, dom, t, g in rows:
    sub = dom.replace('Arithmétique / ', '')
    if sub != cur:
        tbl.append(f'| | **{sub}** | | | | |')
        cur = sub
    st, sk, note = S[n]
    tbl.append(f'| QC-{n:03d} | {t} | `{g}` | {LBL[st]} | {sk} | {note} |')
open(sys.argv[2], 'w', encoding='utf-8').write(summary + '\n\n<!--TABLE-->\n' + '\n'.join(tbl) + '\n')
print(summary)

