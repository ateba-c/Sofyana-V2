"""
Tests for the curriculum-upgrade skills (quiz/generators/registry_plus.py).

Every skill: wired everywhere, has audit refs, and 40 problems × 3 levels pass the
shared structural check. Below that, one correctness test per skill whose answer
can be recomputed from the prompt.
"""
import random
import json
import re
from fractions import Fraction

from django.test import SimpleTestCase

from .answers import check_answer
from .curriculum import CURRICULUM_REFS
from .generators import GENERATORS, SKILL_MAP, TOPIC_GROUPS
from .generators.registry_plus import PLUS_GENERATORS
from .test_g4_generators import Grade4GeneratorTests

PLUS = list(PLUS_GENERATORS)
LEVELS = ('easy', 'medium', 'hard')
RUNS = 40


def _q(slug, level='medium'):
    return GENERATORS[slug](level)


class PlusRegistryTests(SimpleTestCase):
    def test_wired_everywhere(self):
        in_groups = {t['slug'] for g in TOPIC_GROUPS for t in g['topics']}
        for slug in PLUS:
            self.assertIs(GENERATORS[slug], PLUS_GENERATORS[slug], slug)
            self.assertIn(slug, in_groups, slug)
            self.assertIn(slug, SKILL_MAP, slug)
            for key in ('prereq', 'next', 'mastery_next', 'downgrade'):
                target = SKILL_MAP[slug][key]
                if target:
                    self.assertIn(target, GENERATORS, f'{slug}.{key} → {target}')

    def test_curriculum_refs(self):
        for slug in PLUS:
            self.assertTrue(CURRICULUM_REFS.get(slug), f'{slug} has no QC refs in quiz/curriculum.py')

    def test_slugs_carry_their_grade(self):
        grade_of = {t['slug']: g.get('grade') for g in TOPIC_GROUPS for t in g['topics']}
        for slug in PLUS:
            m = re.match(r'g(\d)-', slug)
            if m:
                self.assertEqual(grade_of[slug], int(m.group(1)), slug)


class PlusGeneratorTests(SimpleTestCase):
    _check = Grade4GeneratorTests._check

    def test_all_generators_all_levels(self):
        for slug in PLUS:
            for level in LEVELS:
                for _ in range(RUNS):
                    q = GENERATORS[slug](level)
                    self._check(slug, q)
                    for c in q.get('choices') or []:
                        self.assertNotRegex(str(c['label']), r'^\d{2,}$' if '/' in q['correct_answers'][0] else r'^$',
                                            f'{slug}: padded with a bare number {c}')


def _frac_in(text):
    return [Fraction(int(a), int(b)) for a, b in re.findall(r'(\d+)/(\d+)', text)]


class FractionsPlusTests(SimpleTestCase):
    def test_fraction_shape_never_prints_the_answer(self):
        for level in LEVELS:
            for _ in range(60):
                q = _q('fraction-shape', level)
                texts = [l['text'] for s in q['shape_data'] for l in s.get('labels', [])]
                self.assertNotIn(q['correct_answers'][0], texts)
                n, d = map(int, q['correct_answers'][0].split('/'))
                self.assertTrue(0 < n < d)

    def test_benchmark_is_right(self):
        names = ['égale à 0', 'entre 0 et ½', 'égale à ½', 'entre ½ et 1', 'égale à 1', 'plus grande que 1']
        for level in LEVELS:
            for _ in range(60):
                q = _q('g4-fraction-benchmark', level)
                f = _frac_in(q['prompt_fr'])[0]
                want = 0 if f == 0 else 1 if f < Fraction(1, 2) else 2 if f == Fraction(1, 2) else 3 if f < 1 else 4 if f == 1 else 5
                self.assertEqual(q['correct_answers'][0], names[want])

    def test_equivalent_missing_term(self):
        for _ in range(80):
            q = _q('g4-equivalent-fractions', 'medium')
            if q['q_type'] != 'text_input':
                continue
            m = re.search(r'(\d+)/(\d+) = (\?|\d+)/(\?|\d+)', q['prompt_fr'])
            a, b, c, d = m.groups()
            ans = int(q['correct_answers'][0])
            c, d = (ans, int(d)) if c == '?' else (int(c), ans)
            self.assertEqual(Fraction(int(a), int(b)), Fraction(c, d))

    def test_not_equivalent_is_the_odd_one(self):
        for _ in range(40):
            q = GENERATORS['g4-equivalent-fractions']('hard')
            if 'pas' not in q['prompt_fr']:
                continue
            target = _frac_in(q['prompt_fr'])[0]
            for c in q['choices']:
                self.assertEqual(Fraction(c['label']) != target, c['correct'], c)

    def test_orderings_are_sorted(self):
        for slug in ('g5-order-same-numerator', 'g6-order-related-denominators'):
            for level in LEVELS:
                for _ in range(30):
                    q = _q(slug, level)
                    vals = [Fraction(it['label']) for it in sorted(q['items'], key=lambda i: i['order'])]
                    desc = 'décroissant' in q['prompt_fr']
                    self.assertEqual(vals, sorted(vals, reverse=desc), slug)
                    self.assertEqual(len(set(vals)), len(vals))

    def test_related_denominators_really_related(self):
        for _ in range(40):
            q = _q('g6-order-related-denominators', 'hard')
            dens = [Fraction(it['label']).denominator * 0 + int(it['label'].split('/')[1]) for it in q['items']]
            big = max(dens)
            self.assertTrue(all(big % d == 0 for d in dens), dens)

    def test_simplify_answer_is_irreducible_and_equal(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-simplify-fraction', level)
                ans = q['correct_answers'][0]
                n, d = map(int, ans.split('/'))
                self.assertEqual(Fraction(n, d).denominator, d)
                if 'Réduis' in q['prompt_fr']:
                    self.assertEqual(_frac_in(q['prompt_fr'])[0], Fraction(n, d))

    def test_add_related_value(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-fraction-add-related', level)
                a, b = _frac_in(q['prompt_fr'])[:2]
                want = a - b if '−' in q['prompt_fr'] else a + b
                self.assertGreater(want, 0)
                self.assertTrue(check_answer(str(want), q['correct_answers'], 'fraction'), q['prompt_fr'])

    def test_whole_times_fraction_value(self):
        for _ in range(60):
            q = _q('g6-whole-times-fraction', 'medium')
            if '×' in q['prompt_fr']:
                w = int(re.search(r'\*\*(\d+) ×', q['prompt_fr']).group(1))
                f = _frac_in(q['prompt_fr'])[0]
                self.assertEqual(Fraction(q['correct_answers'][0]), w * f)
            else:
                f = _frac_in(q['prompt_fr'])[0]
                total = int(re.search(r'de (\d+)\*\*', q['prompt_fr']).group(1))
                self.assertEqual(int(q['correct_answers'][0]), f * total)

    def test_fraction_words_typed_answer(self):
        for _ in range(40):
            q = _q('g3-fraction-words', 'hard')
            if q['q_type'] == 'text_input':
                self.assertTrue(check_answer(q['correct_answers'][0], q['correct_answers'], 'fraction'))


def _dec_in(text):
    return [Fraction(x.replace(',', '.')) for x in re.findall(r'\*\*(\d+(?:,\d+)?)', text)]


class DecimalsPlusTests(SimpleTestCase):
    def test_round_and_truncate(self):
        from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
        places = {"à l'unité près": 0, 'au dixième près': 1, 'au centième près': 2,
                  'au dixième (': 1, 'au centième (': 2}     # truncation wording has no « près »
        for level in LEVELS:
            for _ in range(60):
                q = _q('g4-round-decimal', level)
                x = Decimal(re.search(r'\*\*([\d,]+)\*\*', q['prompt_fr']).group(1).replace(',', '.'))
                to = next(v for k, v in places.items() if k in q['prompt_fr'])
                mode = ROUND_DOWN if q['prompt_fr'].startswith('Tronque') else ROUND_HALF_UP
                want = x.quantize(Decimal(1).scaleb(-to), rounding=mode)
                self.assertTrue(check_answer(str(want), q['correct_answers'], 'decimal'), (q['prompt_fr'], q['correct_answers']))

    def test_power_of_ten(self):
        for level in LEVELS:
            for _ in range(60):
                q = _q('g5-times-power-of-ten', level)
                m = re.search(r'\*\*([\d,]+) (×|÷) (\d+)\*\*', q['prompt_fr'])
                x, op, f = Fraction(m.group(1).replace(',', '.')), m.group(2), int(m.group(3))
                want = x * f if op == '×' else x / f
                self.assertEqual(Fraction(q['correct_answers'][-1]), want)   # deduplicated for whole results

    def test_percent_values(self):
        for level in LEVELS:
            for _ in range(60):
                q = _q('g6-percent', level)
                p = q['prompt_fr']
                if 'de ' in p and p.startswith('Combien font'):
                    pct, base = map(int, re.search(r'\*\*(\d+) % de (\d+)\*\*', p).groups())
                    self.assertEqual(int(q['correct_answers'][0]), pct * base // 100)
                elif p.startswith('Écris **') and 'pourcentage' in p:
                    val = _frac_in(p)[0] if '/' in p else _dec_in(p)[0]
                    self.assertTrue(check_answer(str(val * 100), q['correct_answers'], 'integer'), p)

    def test_decimal_grid_counts_squares(self):
        for _ in range(60):
            q = _q('g4-decimal-grid', 'medium')
            if not q['shape_data']:
                continue
            filled = sum(1 for m in q['shape_data'][0]['marks'] if m['type'] == 'rect' and m['fill'] not in ('#FFFFFF', 'none'))
            cells = sum(1 for m in q['shape_data'][0]['marks'] if m['type'] == 'rect' and m['fill'] != 'none')
            self.assertEqual(Fraction(q['correct_answers'][1]), Fraction(filled, cells))

    def test_story_answers_accept_both_notations(self):
        for _ in range(60):
            q = _q('g5-decimal-story', 'hard')
            for a in q['correct_answers']:
                self.assertTrue(check_answer(a.replace(',', '.'), q['correct_answers'], q['answer_type']))

    def test_percent_sign_is_accepted(self):
        self.assertTrue(check_answer('25 %', ['25 %', '25'], 'integer'))
        self.assertTrue(check_answer('25%', ['25'], 'integer'))
        self.assertIsNone(__import__('quiz.answers', fromlist=['parse_duration']).parse_duration('25 %'))


class PrimaryLimitsTests(SimpleTestCase):
    def test_decimals_stop_at_thousandths(self):
        dec = re.compile(r'\d[.,](\d+)')
        for slug in PLUS:
            for level in LEVELS:
                for _ in range(25):
                    for a in GENERATORS[slug](level).get('correct_answers') or []:
                        for m in dec.finditer(str(a)):
                            self.assertLessEqual(len(m.group(1)), 3, f'{slug}/{level}: {a}')


def _eval(expr):
    return eval(expr.replace('×', '*').replace('÷', '//').replace('−', '-'), {'__builtins__': {}})


class OperationsPlusTests(SimpleTestCase):
    def test_exactly_one_true_equality(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g3-equality-true', level)
                for c in q['choices']:
                    left, right = c['label'].split(' = ')
                    self.assertEqual(_eval(left) == _eval(right), c['correct'], c['label'])

    def test_equivalent_expression_choices(self):
        for _ in range(60):
            q = _q('g4-equivalent-expressions', 'medium')
            a, b = map(int, re.findall(r'\*\*(\d+) \+ (\d+)', q['prompt_fr'])[0])
            if q['q_type'] == 'text_input':
                r = int(re.search(r'= (\d+) \+ \?', q['prompt_fr']).group(1))
                self.assertEqual(r + int(q['correct_answers'][0]), a + b)
            else:
                for c in q['choices']:
                    self.assertEqual(_eval(c['label']) == a + b, c['correct'], c['label'])

    def test_missing_factor(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g4-missing-factor', level)
                expr = re.search(r'\*\*(.+)\*\*', q['prompt_fr']).group(1).replace('?', q['correct_answers'][0])
                left, right = expr.split(' = ')
                self.assertEqual(_eval(left), int(right), expr)

    def test_division_remainder(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g4-division-remainder', level)
                m = re.search(r'\*\*([\d ]+) ÷ (\d+)\*\*', q['prompt_fr'])
                if not m:
                    continue
                n, d = int(m.group(1).replace(' ', '')), int(m.group(2))
                want = n // d if 'quotient' in q['prompt_fr'] else n % d
                self.assertEqual(int(q['correct_answers'][0]), want)

    def test_expression_for_story_single_right_value(self):
        for level in LEVELS:
            for _ in range(30):
                q = _q('g5-expression-for-story', level)
                right = next(c for c in q['choices'] if c['correct'])['label']
                for c in q['choices']:
                    if not c['correct']:
                        self.assertNotEqual(c['label'], right)

    def test_divisibility_single_answer(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-divisibility', level)
                k = int(re.search(r'par (\d+)', q['prompt_fr']).group(1))
                for c in q['choices']:
                    self.assertEqual(int(c['label']) % k == 0, c['correct'], (k, c['label']))

    def test_prime_factorisation(self):
        from math import prod
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-prime-factors', level)
                n = int(re.search(r'\*\*(\d+)\*\*', q['prompt_fr']).group(1))
                if q['q_type'] == 'multiple_choice':
                    fs = [int(x) for x in q['correct_answers'][0].split(' × ')]
                    self.assertEqual(prod(fs), n)
                    self.assertTrue(all(all(f % k for k in range(2, f)) for f in fs))

    def test_powers_values(self):
        sup = {'²': 2, '³': 3, '⁴': 4, '⁵': 5}
        for level in LEVELS:
            for _ in range(40):
                q = _q('g6-powers', level)
                m = re.match(r'Calcule : \*\*(\d+)([²³⁴⁵])\*\*', q['prompt_fr'])
                if m:
                    self.assertEqual(int(q['correct_answers'][0]), int(m.group(1)) ** sup[m.group(2)])

    def test_times_tables_within_10(self):
        for level in LEVELS:
            for _ in range(60):
                q = _q('g4-times-tables', level)
                nums = list(map(int, re.findall(r'\d+', q['prompt_fr'])))
                if '×' in q['prompt_fr']:
                    self.assertTrue(all(x <= 10 for x in nums), nums)
                    self.assertEqual(int(q['correct_answers'][0]), nums[0] * nums[1])

    def test_write_large_number_accepts_grouping(self):
        for _ in range(30):
            q = _q('g6-write-large-number', 'hard')
            n = q['correct_answers'][0]
            self.assertTrue(check_answer(f'{int(n):,}'.replace(',', ' '), q['correct_answers'], 'integer'))


class GeometryPlusTests(SimpleTestCase):
    """WP5: answers recomputed from the picture or the prompt."""

    def test_triangle_shapes_match_their_type(self):
        import math
        from .generators.geometry_plus import _triangle_of
        for kind in ('equi', 'iso-right', 'iso', 'scal-right', 'scal'):
            for _ in range(30):
                pts, _t, right, _s, _a = _triangle_of(kind)
                d = sorted(math.dist(pts[i], pts[(i + 1) % 3]) for i in range(3))
                equal = sum(abs(d[i] - d[j]) < 1e-6 for i, j in ((0, 1), (1, 2), (0, 2)))
                is_right = abs(d[0] ** 2 + d[1] ** 2 - d[2] ** 2) < 1e-6
                sides = {3: 'equi', 1: 'iso', 0: 'scal'}[equal]
                expected = sides if sides == 'equi' else sides + ('-right' if is_right else '')
                self.assertEqual(expected, kind, (kind, d))
                self.assertEqual(right is not None, is_right, kind)

    def test_triangle_angles_add_up(self):
        for _ in range(80):
            q = _q('g6-triangle-type', 'hard')
            angles = list(map(int, re.findall(r'(\d+)°', q['prompt_fr'])))
            if angles:
                self.assertEqual(sum(angles), 180, q['prompt_fr'])

    def test_convex_builders(self):
        from .generators.geometry_plus import concave_polygon, convex_polygon, is_convex
        for _ in range(100):
            self.assertTrue(is_convex(convex_polygon(random.randint(4, 7))))
            self.assertFalse(is_convex(concave_polygon(random.randint(4, 7), random.choice([0.35, 0.6, 0.85]))))

    def test_euler_holds_for_every_polyhedron(self):
        from .generators.geometry_plus import FACES, FVE
        for kind, (f, v, e) in FVE.items():
            self.assertEqual(f + v - e, 2, kind)
            self.assertEqual(sum(n for n, _ in FACES[kind]), f, kind)

    def test_circle_radius_diameter(self):
        for _ in range(60):
            q = _q('g6-circle-parts', 'medium')
            n = int(re.findall(r'(\d+) cm', q['prompt_fr'])[0])
            expected = n * 2 if 'rayon de ce cercle' in q['prompt_fr'] else n // 2
            self.assertEqual(int(q['correct_answers'][0]), expected)

    def test_translation_of_a_point(self):
        for _ in range(80):
            q = _q('g6-translation', 'hard')
            m = re.search(r'A \((\d+), (\d+)\) glisse de (.*)\. Quelles', q['prompt_fr'])
            if not m:
                continue
            x, y = int(m.group(1)), int(m.group(2))
            for n, way in re.findall(r'(\d+) carreaux? vers la? ?l?e? ?(droite|gauche|haut|bas)', m.group(3)):
                n = int(n)
                x += n if way == 'droite' else -n if way == 'gauche' else 0
                y += n if way == 'haut' else -n if way == 'bas' else 0
            self.assertGreaterEqual(min(x, y), 0)                     # no negatives
            self.assertIn(f'({x}, {y})', q['correct_answers'])

    def test_translation_arrow_matches_picture(self):
        from .generators.geometry_plus import _dir_words
        from quiz import illustrations as I
        blue, green = I.SHADES[I.BLUE][2], I.SHADES[I.GREEN][2]
        for _ in range(60):
            q = _q('g6-translation', 'easy')
            rects = [m for m in q['shape_data'][0]['marks'] if m['type'] == 'rect']
            cell = rects[0]['w']
            b = min((m['x'], m['y']) for m in rects if m['fill'] == blue)
            g = min((m['x'], m['y']) for m in rects if m['fill'] == green)
            bx, by = min(m['x'] for m in rects if m['fill'] == blue), min(m['y'] for m in rects if m['fill'] == blue)
            gx, gy = min(m['x'] for m in rects if m['fill'] == green), min(m['y'] for m in rects if m['fill'] == green)
            dx, dy = round((gx - bx) / cell), round((by - gy) / cell)
            self.assertEqual(q['correct_answers'][0], _dir_words(dx, dy)[0], (b, g))

    def test_grid_map_square_matches_picture(self):
        for _ in range(60):
            q = _q('g3-grid-map', 'easy')
            labels = q['shape_data'][0]['labels']
            emoji = q['prompt_fr'].split()[-2]
            icon = next(l for l in labels if l['text'] == emoji)
            cols = [l for l in labels if l['text'].isalpha() and len(l['text']) == 1]
            rows = [l for l in labels if l['text'].isdigit()]
            col = min(cols, key=lambda l: abs(l['x'] - icon['x']))['text']
            row = min(rows, key=lambda l: abs(l['y'] - icon['y']))['text']
            self.assertEqual(q['correct_answers'][0], col + row)

    def test_place_point_letter_matches_coordinates(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('cartesian-place-point', level)
                x, y = map(int, re.search(r'\((\d+), (\d+)\)', q['prompt_fr']).groups())
                if q['q_type'] == 'place_point':          # tap-to-place variant: the key is the coordinate itself
                    self.assertIn(f'({x}, {y})', q['correct_answers'])
                    continue
                shape = q['shape_data'][0]
                nums = {}
                for l in shape['labels']:
                    if l['text'].isdigit():
                        nums.setdefault(l['text'], []).append(l)
                zero = nums['0'][0]
                one_x = next(l for l in nums['1'] if abs(l['y'] - zero['y']) < 1)
                cell = one_x['x'] - zero['x']
                bottom = zero['y'] - 15
                letter = next(l for l in shape['labels'] if l['text'] == q['correct_answers'][0])
                px, py = letter['x'] - 8, letter['y'] + 6
                self.assertEqual((round((px - zero['x']) / cell), round((bottom - py) / cell)), (x, y))

    def test_symmetry_axes_counts(self):
        expected = {'carré': 4, 'rectangle': 2, 'triangle équilatéral': 3, 'triangle isocèle': 1,
                    'triangle scalène': 0, 'losange': 2, 'parallélogramme': 0, 'pentagone régulier': 5,
                    'hexagone régulier': 6}
        for _ in range(60):
            q = _q('g3-symmetry-axis', 'hard')
            name = re.search(r'\(une? (.*)\)', q['prompt_fr']).group(1)
            self.assertEqual(int(q['correct_answers'][0]), expected[name], name)

    def test_motifs_have_no_symmetry(self):
        from .generators.geometry_plus import _mirror_h, _mirror_v, _rot90, motif
        for _ in range(100):
            m = motif(random.randint(4, 5), 3, 3)
            self.assertNotIn(m, (_mirror_v(m), _mirror_h(m), _rot90(m), _rot90(_rot90(m))))


class MeasurementPlusTests(SimpleTestCase):
    """WP6: answers recomputed from the picture or the prompt."""

    def test_ruler_length_matches_picture(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g3-ruler-mm', level)
                shape = q['shape_data'][0]
                ends = sorted(m['x1'] for m in shape['marks'] if m['type'] == 'line' and m.get('dash') == '3 3')
                zero = next(l['x'] for l in shape['labels'] if l['text'] == '0')
                one = next(l['x'] for l in shape['labels'] if l['text'] == '1')
                mm = round((ends[1] - ends[0]) / (one - zero) * 10)
                expected = mm // 10 if level == 'easy' else mm
                self.assertEqual(int(q['correct_answers'][0]), expected, level)

    def test_area_counts_coloured_squares(self):
        from quiz import illustrations as I
        for level in LEVELS:
            for _ in range(40):
                q = _q('g3-area-count-squares', level)
                marks = q['shape_data'][0]['marks']
                full = sum(1 for m in marks if m['type'] == 'rect' and m['fill'] not in ('none', '#FFFFFF'))
                halves = sum(1 for m in marks if m['type'] == 'path' and m['fill'] != 'none')
                self.assertEqual(halves % 2, 0)
                self.assertEqual(int(q['correct_answers'][0]), full + halves // 2, level)

    def test_balance_weights_add_up(self):
        for _ in range(40):
            q = _q('g3-balance-scale', 'easy')
            grams = [int(l['text'].split()[0]) for l in q['shape_data'][0]['labels'] if l['text'].endswith(' g')]
            self.assertEqual(int(q['correct_answers'][1]), sum(grams))

    def test_balance_shared_mass(self):
        for _ in range(60):
            q = _q('g3-balance-scale', 'hard')
            if not q['shape_data']:
                continue
            labels = q['shape_data'][0]['labels']
            grams = sum(int(l['text'].split()[0]) for l in labels if l['text'].endswith(' g'))
            fruit = len([l for l in labels if not l['text'].endswith(' g')])
            self.assertEqual(int(q['correct_answers'][1]) * fruit, grams)

    def test_conversions(self):
        factors = {('m²', 'dm²'): 100, ('dm²', 'cm²'): 100, ('dm²', 'm²'): 0.01, ('cm²', 'dm²'): 0.01,
                   ('dm³', 'L'): 1, ('L', 'cm³'): 1000, ('cm³', 'mL'): 1, ('dm³', 'cm³'): 1000}
        for slug in ('g5-area-units', 'g6-volume-units'):
            for _ in range(80):
                q = _q(slug, 'hard')
                m = re.search(r'\*\*([\d ]+) (\S+) = \? (\S+)\*\*', q['prompt_fr'])
                if m:
                    n = int(m.group(1).replace(' ', ''))
                    self.assertEqual(int(q['correct_answers'][0]), round(n * factors[(m.group(2), m.group(3))]))

    def test_box_volume_and_area(self):
        for _ in range(40):
            q = _q('g6-volume-units', 'medium')
            a, b, h = map(int, re.findall(r'(\d+) cm', q['prompt_fr'])[:3])
            self.assertEqual(int(q['correct_answers'][-1]), a * b * h)
            self.assertTrue(check_answer(f'{a * b * h} cm3', q['correct_answers'], 'integer'))

    def test_capacity_cups(self):
        for _ in range(40):
            q = _q('g3-capacity-estimate', 'easy')
            cup = int(re.search(r'contient (\d+) mL', q['prompt_fr']).group(1))
            m = re.search(r'carafe de (\d+) (mL|L)', q['prompt_fr'])
            jug = int(m.group(1)) * (1000 if m.group(2) == 'L' else 1)
            self.assertEqual(int(q['correct_answers'][0]) * cup, jug)

    def test_estimates_never_offer_an_equivalent_amount(self):
        to_ml = {'mL': 1, 'L': 1000}
        for _ in range(80):
            q = _q('g3-capacity-estimate', 'hard')
            vals = []
            for c in q['choices']:
                num, unit = c['label'].rsplit(' ', 1)          # the number may hold a narrow no-break space
                vals.append(int(num.replace(' ', '')) * to_ml[unit])
            self.assertEqual(len(vals), len(set(vals)), q['choices'])

    def test_no_negative_temperatures(self):
        # D2 (2026-10-26): below-zero readings only on the grade-5 hard level (winter scale)
        for slug, level in [(s, lv) for s in ('g3-thermometer', 'g5-thermometer') for lv in LEVELS
                            if not (s == 'g5-thermometer' and lv == 'hard')]:
            if True:
                for _ in range(30):
                    q = _q(slug, level)
                    for s in q['shape_data']:
                        if s.get('type') == 'thermometer':
                            self.assertGreaterEqual(s['min_temp'], 0, slug)
                    self.assertNotIn('−', q['correct_answers'][0])
                    self.assertGreaterEqual(int(re.sub(r'\D', '', q['correct_answers'][-1]) or 0), 0)

    def test_thermometer_value_is_readable(self):
        for slug in ('g3-thermometer', 'g5-thermometer'):
            for level in LEVELS:
                for _ in range(30):
                    s = next((x for x in _q(slug, level)['shape_data'] if x.get('type') == 'thermometer'), None)
                    if s:
                        tick = s.get('minor') or s['step']
                        self.assertEqual((s['temp'] - s['min_temp']) % tick, 0, (slug, level, s))


class StatsProbabilityPlusTests(SimpleTestCase):
    """WP7–WP8: answers recomputed from the picture or the prompt."""

    def test_pictograph_value_matches_icons(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g3-pictograph', level)
                if 'ont choisi **' not in q['prompt_fr'] or 'plutôt' in q['prompt_fr']:
                    continue
                shape = q['shape_data'][0]
                cat = re.search(r'ont choisi \*\*(.+?)\*\*', q['prompt_fr']).group(1)
                per = int(re.search(r'vaut (\d+)', q['prompt_fr']).group(1))
                row = next(l for l in shape['labels'] if l['text'] == cat)
                icon = shape['labels'][-1]['text'].split('=')[0].strip()     # '⭐ = 2', or '= 4' after a drawn disc
                if icon:      # emoji symbols (no half symbols)
                    whole = len([l for l in shape['labels'] if l['text'] == icon and abs(l['y'] - row['y'] - 2) <= 3])
                    halves = 0
                else:         # discs drawn as marks: a circle = 1 symbol, a half-disc path = ½
                    whole = len([m for m in shape['marks'] if m['type'] == 'circle' and abs(m['cy'] - row['y'] + 4) <= 3])
                    halves = len([m for m in shape['marks'] if m['type'] == 'path' and m.get('fill') != 'none'
                                  and abs(float(m['d'].split()[1].split(',')[1]) + 10 - row['y'] + 4) <= 3])
                self.assertEqual(int(q['correct_answers'][0]), round((whole + halves / 2) * per), (cat, level))

    def test_line_graph_reading(self):
        for _ in range(40):
            q = _q('g4-line-graph', 'easy')
            shape = q['shape_data'][0]
            ticks = sorted(((l['y'], int(l['text'])) for l in shape['labels'] if l['text'].isdigit() and l['anchor'] == 'end'))
            (y_hi, v_hi), (y_lo, v_lo) = ticks[0], ticks[-1]
            dots = [m for m in shape['marks'] if m['type'] == 'dot']
            values = [round(v_lo + (y_lo - 4 - d['y']) * (v_hi - v_lo) / (y_lo - y_hi)) for d in dots]
            self.assertIn(int(q['correct_answers'][0]), values)

    def test_tally_marks_count(self):
        for _ in range(40):
            q = _q('g3-tally-table', 'medium')
            shape = q['shape_data'][0]
            cat = re.search(r'pour \*\*(.+?)\*\*', q['prompt_fr']).group(1)
            row = next(l for l in shape['labels'] if l['text'] == cat)
            lines = [m for m in shape['marks'] if m['type'] == 'line' and row['y'] - 20 <= min(m['y1'], m['y2']) <= row['y'] + 6]
            self.assertEqual(int(q['correct_answers'][0]), len(lines))   # 4 strokes + 1 bar per five

    def test_raw_data_count(self):
        for _ in range(40):
            q = _q('g3-tally-table', 'easy')
            emoji = q['prompt_fr'].split()[-2]
            n = sum(1 for l in q['shape_data'][0]['labels'] if l['text'] == emoji)
            self.assertEqual(int(q['correct_answers'][0]), n)

    def test_build_chart_single_matching_panel(self):
        for level in LEVELS:
            for _ in range(30):
                q = _q('g3-build-chart', level)
                vals = [int(row[1]) for row in q['table']['rows']]
                if q['q_type'] == 'build_bars':            # tap-to-build variant: the key is the table itself
                    self.assertEqual(json.loads(q['correct_answers'][0]), vals)
                    continue
                n = len(vals)
                bars = [m for m in q['shape_data'][0]['marks'] if m['type'] == 'rect']
                panels = [[b['h'] for b in bars[k * n:(k + 1) * n]] for k in range(5)]
                unit = max(max(p) for p in panels) / max(max(vals), 1)
                # a panel matches when every bar is the same multiple of its value
                matches = []
                for k, p in enumerate(panels):
                    scale = p[0] / vals[0]
                    if all(abs(h - v * scale) < 1.0 for h, v in zip(p, vals)):
                        matches.append(k)
                self.assertEqual(len(matches), 1, (vals, panels))
                self.assertEqual(q['correct_answers'][0], 'ABCDE'[matches[0]])
                self.assertGreater(unit, 0)

    def test_probability_line_matches_bag(self):
        from fractions import Fraction
        for level in LEVELS:
            for _ in range(40):
                q = _q('g5-probability-line', level)
                bag, line = q['shape_data']
                balls = [m for m in bag['marks'] if m['type'] == 'circle']
                red = sum(1 for b in balls if b['fill'] == '#EF4444')
                p = Fraction(red, len(balls))
                x0, x1 = 20, line['vw'] - 20
                letter = next(l for l in line['labels'] if l['text'] == q['correct_answers'][0])
                self.assertAlmostEqual((letter['x'] - x0) / (x1 - x0), float(p), places=2)

    def test_tree_leaves(self):
        for _ in range(30):
            q = _q('g5-tree-diagram', 'easy')
            shape = q['shape_data'][0]
            leaves = [l for l in shape['labels'] if l['x'] == 220]
            self.assertEqual(int(q['correct_answers'][0]), len(leaves))

    def test_spinner_outcomes(self):
        for _ in range(30):
            q = _q('g3-list-outcomes', 'easy')
            fills = {m['fill'] for m in q['shape_data'][0]['marks'] if m['type'] in ('path', 'circle') and m['fill'] not in ('none',)}
            self.assertEqual(int(q['correct_answers'][0]), len(fills))

    def test_equally_likely_spinners(self):
        for _ in range(40):
            q = _q('g3-equally-likely', 'easy')
            self.assertEqual(len(q['choices']), 5)
            self.assertIn(q['correct_answers'][0], 'ABCDE')


class EarlyGradesTests(SimpleTestCase):
    """WP1 (grades 1–2): answers recomputed from the picture or the prompt."""

    def test_count_objects(self):
        for level in LEVELS:
            for _ in range(30):
                q = _q('g1-count-objects', level)
                labels = q['shape_data'][0]['labels']
                self.assertEqual(int(q['correct_answers'][0]), len(labels))

    def test_base_ten_blocks(self):
        for level in ('easy', 'hard'):
            for _ in range(30):
                q = _q('g2-tens-ones-picture', level)
                rects = [m for m in q['shape_data'][0]['marks'] if m['type'] == 'rect']
                unit = min(r['w'] for r in rects)
                value = sum(100 if r['w'] > 5 * unit else 10 if r['h'] > 5 * unit else 1 for r in rects)
                self.assertEqual(int(q['correct_answers'][0]), value)

    def test_hundred_chart(self):
        for level in LEVELS:
            for _ in range(30):
                q = _q('g2-hundred-chart', level)
                labels = q['shape_data'][0]['labels']
                hole = next(l for l in labels if l['text'] == '?')
                ref = next(l for l in labels if l['text'].isdigit())
                dx, dy = round((hole['x'] - ref['x']) / 36), round((hole['y'] - ref['y']) / 36)
                self.assertEqual(int(q['correct_answers'][0]), int(ref['text']) + dx + 10 * dy)

    def test_number_line_jumps(self):
        for level in LEVELS:
            for _ in range(30):
                q = _q('g2-add-sub-2digit', level)
                labels = q['shape_data'][0]['labels']
                start = int(labels[0]['text'])
                jumps = [int(l['text'].replace('−', '-')) for l in labels if l['text'][0] in '+−']
                self.assertEqual(int(q['correct_answers'][0]), start + sum(jumps))

    def test_equal_groups_total(self):
        for _ in range(30):
            q = _q('g2-equal-groups', 'easy')
            self.assertEqual(int(q['correct_answers'][0]), len(q['shape_data'][0]['labels']))

    def test_facts_and_missing_numbers(self):
        for slug in ('g1-add-facts', 'g1-sub-facts', 'g1-missing-number'):
            for level in LEVELS:
                for _ in range(40):
                    q = _q(slug, level)
                    expr = re.search(r'\*\*(.+?)\*\*', q['prompt_fr']).group(1).replace('−', '-')
                    ans = q['correct_answers'][0]
                    left, right = expr.replace('?', ans).split('=')
                    if right.strip() == '':
                        right = ans
                    self.assertEqual(eval(left), eval(right), (slug, expr, ans))
                    if slug != 'g1-missing-number':
                        self.assertLessEqual(int(ans), 20)

    def test_true_equality_single(self):
        for level in LEVELS:
            for _ in range(40):
                q = _q('g1-true-equality', level)
                true = [c for c in q['choices'] if eval(c['label'].replace('−', '-').replace('=', '=='))]
                self.assertEqual(len(true), 1)
                self.assertTrue(true[0]['correct'])

    def test_clock_matches(self):
        for level in ('easy', 'medium'):
            for _ in range(30):
                q = _q('g1-clock-hour-half', level)
                s = q['shape_data']
                s = s[0] if isinstance(s, list) else s
                h, m = s['hours'], s['minutes']
                self.assertEqual(q['correct_answers'][0], f'{h} h {m:02d}' if m else f'{h} h')

    def test_paper_clips(self):
        for level in ('easy', 'medium'):
            for _ in range(30):
                q = _q('g1-measure-units', level)
                outer = [m for m in q['shape_data'][0]['marks'] if m['type'] == 'rect' and m['rx'] == 8]
                self.assertEqual(int(q['correct_answers'][0]), len(outer))

    def test_same_shape_is_unique(self):
        import math
        def sides(d):
            pts = [tuple(map(float, p.split(','))) for p in re.findall(r'-?[\d.]+,-?[\d.]+', d)]
            return sorted(round(math.dist(pts[i], pts[(i + 1) % len(pts)])) for i in range(len(pts)))
        for level in LEVELS:
            for _ in range(30):
                q = _q('g1-same-shape-size', level)
                polys = [m['d'] for m in q['shape_data'][0]['marks'] if m['type'] == 'path']
                model, options = sides(polys[0]), [sides(p) for p in polys[1:]]
                same = [k for k, o in enumerate(options) if len(o) == len(model) and all(abs(a - b) <= 1 for a, b in zip(o, model))]
                self.assertEqual(len(same), 1, (model, options))
                self.assertEqual(q['correct_answers'][0], 'ABCDE'[same[0]])

    def test_early_grades_hidden_by_default(self):
        from django.test import override_settings
        from . import taxonomy
        taxonomy.invalidate()
        self.assertNotIn(1, taxonomy.available_grades())
        self.assertNotIn(2, taxonomy.available_grades())
        with override_settings(SHOW_EARLY_GRADES=True):
            taxonomy.invalidate()
            self.assertIn(1, taxonomy.available_grades())
            self.assertIn(2, taxonomy.available_grades())
        taxonomy.invalidate()


class ReadAloudTests(SimpleTestCase):
    def test_button_on_every_question_type(self):
        import json
        from django.template.loader import render_to_string
        for slug in ('g4-independence', 'g3-story-meaning', 'g2-order', 'g6-choose-notation'):
            q = _q(slug, 'medium')
            html = render_to_string('partials/practice_question.html', {'question': q, 'lang': 'fr', 'topic': slug, 'level': 'medium'})
            self.assertIn('sayAloud(this)', html, slug)
            m = re.search(r"data-choices='([^']*)'", html)
            labels = json.loads(m.group(1).replace('&quot;', '"').replace('&#x27;', "'").replace('&amp;', '&'))
            if q['q_type'] == 'multiple_choice':
                self.assertEqual(labels, [c['label'] for c in q['choices']])
            self.assertNotIn('**', re.search(r'data-say="([^"]*)"', html).group(1))


class VocabReasoningTests(SimpleTestCase):
    def test_vocab_meanings_are_unique(self):
        for slug in ('g3-vocab-numbers', 'g3-vocab-geometry', 'g3-vocab-measurement', 'g4-vocab-chance'):
            for level in LEVELS:
                for _ in range(30):
                    pairs = _q(slug, level)['pairs']
                    self.assertGreaterEqual(len(pairs), 3)
                    self.assertEqual(len({p['right'] for p in pairs}), len(pairs), slug)
                    self.assertEqual(len({p['left'] for p in pairs}), len(pairs), slug)

    def test_who_is_right_has_one_answer(self):
        for slug in ('g4-who-is-right-numbers', 'g5-who-is-right-shapes', 'g5-who-is-right-data'):
            for level in LEVELS:
                for _ in range(40):
                    q = _q(slug, level)
                    self.assertEqual(sum(c['correct'] for c in q['choices']), 1)
                    self.assertNotIn('On ne peut pas savoir', q['correct_answers'][0])
