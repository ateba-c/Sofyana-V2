"""
Regression tests for the G1-C QA pass (geometry & space generators):
accuracy and ambiguity fixes found by the AI pre-review.
"""
import random

from django.test import SimpleTestCase

from .answers import check_answer
from .generators import GENERATORS
from .generators import g4_geometry as G4
from .generators import geometry_plus as GP

N = 200
LEVELS = ('easy', 'medium', 'hard')


def _samples(slug, n=N):
    for level in LEVELS:
        for _ in range(n):
            yield level, GENERATORS[slug](level)


def _correct(q):
    return [c for c in q['choices'] if c['correct']]


class LinesTests(SimpleTestCase):
    def test_perpendicular_never_offers_plain_secant(self):
        """Perpendicular lines are also secant: the third relation must exclude right angles."""
        for slug in ('parallel-perp', 'g4-lines'):
            for level, q in _samples(slug):
                labels = [c['label'] for c in q['choices']]
                self.assertNotIn('sécantes', labels, f'{slug}/{level}')
                self.assertNotIn('secantes', labels)
                self.assertFalse(any('perp' in lab and lab != 'perpendiculaires' and 'non' not in lab for lab in labels),
                                 labels)
                self.assertEqual(len(_correct(q)), 1)


class QuadrilateralTests(SimpleTestCase):
    def test_every_riddle_has_exactly_one_most_precise_name(self):
        for kind, q in G4.QUADS.items():
            for d_fr, d_en, satisfying in q['defs']:
                self.assertEqual(G4.most_precise(satisfying), [kind], d_fr)

    def test_no_general_false_property(self):
        """Never state « aucun angle droit » / « longueurs différentes » as a rule for a parallelogram, rhombus or trapezoid."""
        for slug in ('g4-quadrilateral-name', 'g4-quadrilateral-riddle', 'g4-quadrilateral-match', 'g4-quadrilateral-count'):
            for level, q in _samples(slug, 80):
                texts = [q['hint_fr'], q['hint_en'], q['prompt_fr']]
                texts += [c.get('feedback_fr', '') for c in q['choices']] + [c.get('feedback_en', '') for c in q['choices']]
                if slug != 'g4-quadrilateral-name':          # the name explanation describes the drawn figure
                    texts += [q['explanation_fr'], q['explanation_en']]
                for t in texts:
                    for bad in ('aucun angle droit', 'no right angle', 'longueurs différentes', 'different lengths'):
                        self.assertNotIn(bad, t, f'{slug}/{level}: {t}')

    def test_name_and_riddle_ask_for_most_precise_name(self):
        for slug in ('g4-quadrilateral-name', 'g4-quadrilateral-riddle'):
            for level, q in _samples(slug, 40):
                self.assertIn('le plus précis', q['prompt_fr'])
                self.assertIn('most precise', q['prompt_en'])

    def test_reverse_riddle_unique(self):
        random.seed(7)
        for _ in range(300):
            q = GENERATORS['g4-quadrilateral-riddle']('hard')
            if 'Pour quelle devinette' not in q['prompt_fr']:
                continue
            target = next(k for k, v in G4.QUADS.items() if f'**{v["fr"]}**' in q['prompt_fr'])
            answers = []
            for c in q['choices']:
                sat = next(s for v in G4.QUADS.values() for d, _, s in v['defs'] if d == c['label'])
                if G4.most_precise(sat) == [target]:
                    answers.append(c)
            self.assertEqual(len(answers), 1)
            self.assertTrue(answers[0]['correct'])

    def test_count_always_shows_the_figure(self):
        for level, q in _samples('g4-quadrilateral-count'):
            self.assertTrue(q['show_illustration'])
            kind = q['shape_data'][0]['kind']
            if 'même longueur' in q['prompt_fr']:
                self.assertIn(kind, ('square', 'rhombus'))
            self.assertNotIn('Au minimum', q['prompt_fr'])


class PolygonTests(SimpleTestCase):
    def test_non_convex_polygons_have_a_visible_dent(self):
        for depth in (0.85, 0.6, 0.35):
            for _ in range(300):
                pts = GP.concave_polygon(random.randint(4, 7), depth)
                self.assertFalse(GP.is_convex(pts))
                self.assertTrue(GP.is_simple(pts))
                self.assertGreaterEqual(GP.max_interior_angle(pts), 200)

    def test_count_sides_english_article(self):
        random.seed(1)
        for level, q in _samples('count-sides'):
            self.assertNotIn('a octagon', q['explanation_en'])
            self.assertNotIn('--', q['explanation_fr'])
            self.assertIn('côtés', q['explanation_fr'])

    def test_perimeter_triangles_are_possible(self):
        for level, q in _samples('perimeter-labeled', 400):
            for s in q['shape_data']:
                if s['type'] == 'labeled_triangle':
                    a, b, c = sorted(s['sides'])
                    self.assertLess(c, a + b, s['sides'])


class SolidTests(SimpleTestCase):
    def test_cube_and_rectangular_prism_never_both_true(self):
        """A cube is a rectangular prism (and a prism): never offer both names for a cube."""
        for slug in ('g3-solid-picture', 'g3-net-match'):
            for level, q in _samples(slug):
                labels = {c['label'] for c in q['choices']}
                if 'cube' in [c['label'] for c in _correct(q)]:
                    self.assertNotIn('prisme à base rectangulaire', labels, f'{slug}/{level}')
                    self.assertNotIn('prisme', labels, f'{slug}/{level}')
                if q['correct_answers'] and q['correct_answers'][0] == '6 carrés':
                    self.assertNotIn('6 rectangles', labels)

    def test_french_elisions(self):
        for slug in ('g3-prism-or-pyramid', 'g3-net-match', 'g6-polyhedron-net'):
            for level, q in _samples(slug):
                text = q['prompt_fr'] + ' ' + q['explanation_fr']
                for bad in ('de hexagone', 'que un', 'de **arêtes', 'de arêtes'):
                    self.assertNotIn(bad, text, f'{slug}/{level}')

    def test_identify_solid_english_descriptions(self):
        for level, q in _samples('identify-solid', 50):
            for p in q['pairs']:
                self.assertIn('right_en', p)
                self.assertNotRegex(p['right_en'], r'\b0 (vertex|edge|straight edge|flat face)\b')
            self.assertNotIn('Un cube a 6 faces carrées', q['hint_fr'])


class CoordinateTests(SimpleTestCase):
    def test_cartesian_coord_accepts_usual_forms(self):
        random.seed(2)
        for _ in range(50):
            q = GENERATORS['cartesian-coord']('hard')
            self.assertEqual(q['answer_type'], 'coordinate')
            x, y = q['shape_data'][0]['px'], q['shape_data'][0]['py']
            for typed in (f'({x}, {y})', f'({x},{y})', f'{x}, {y}', f'{x},{y}'):
                self.assertTrue(check_answer(typed, q['correct_answers'], q['answer_type']), typed)
            if x != y:
                self.assertFalse(check_answer(f'({y}, {x})', q['correct_answers'], q['answer_type']))

    def test_feminine_agreement(self):
        for level in ('easy', 'medium'):
            for _ in range(20):
                q = GENERATORS['cartesian-coord'](level)
                self.assertTrue(q['prompt_fr'].startswith('Quelle est'))
                self.assertTrue(q['explanation_fr'].splitlines()[-1].startswith('Réponse : l\'')
                                , q['explanation_fr'])

    def test_place_point_letters_stay_inside_the_grid(self):
        seen = []
        orig = GP.I.grid

        def spy(cols, rows, **kw):
            seen.append((cols, kw.get('points')))
            return orig(cols, rows, **kw)
        GP.I.grid = spy
        try:
            for level, q in _samples('cartesian-place-point'):
                size, points = seen[-1]
                self.assertEqual(len(points), 5)
                for (x, y) in points:
                    self.assertTrue(0 <= x < size and 0 <= y < size, (x, y, size))
                self.assertEqual(len(_correct(q)), 1)
        finally:
            GP.I.grid = orig
