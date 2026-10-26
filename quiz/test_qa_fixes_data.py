"""
Regression tests for the QA pre-review fixes, group B (statistics, probability, reasoning).

Each test pins one verified bug: a wrong answer key, an ambiguous choice list, a picture
that contradicts the key, or French left in the English version.
"""
import copy
import re
from fractions import Fraction

from django.test import SimpleTestCase

from .answers import check_answer
from .generators import GENERATORS
from .labels import localize_problem

LEVELS = ('easy', 'medium', 'hard')


def _gen(slug, level, n=60):
    for _ in range(n):
        yield GENERATORS[slug](level)


class StatisticsKeyTests(SimpleTestCase):
    def test_mean_key_is_sum_over_count(self):
        """g5-arithmetic-mean: the last value used to be clamped to 1, so the key was not the mean of the list."""
        for level in LEVELS:
            for q in _gen('g5-arithmetic-mean', level, 150):
                vals = [int(v) for v in re.search(r'\*\*(.+)\*\*', q['prompt_en']).group(1).split(', ')]
                mean = Fraction(sum(vals), len(vals))
                self.assertEqual(Fraction(q['correct_answers'][-1].replace(',', '.')), mean, vals)
                self.assertEqual(len(q['correct_answers']), len(set(q['correct_answers'])))
                shown = str(mean.numerator / mean.denominator).replace('.', ',')
                self.assertTrue(check_answer(shown.rstrip('0').rstrip(','), q['correct_answers']), (vals, q['correct_answers']))
                if level == 'hard':
                    self.assertEqual(mean.denominator, 2)

    def test_probability_vocab_key_matches_bag(self):
        """probability-vocab: « Certain » was keyed for a colour with 0 marbles; « également probable » on odd totals."""
        expected = {'Certain': lambda t, n: t == n, 'Impossible': lambda t, n: t == 0,
                    'Probable': lambda t, n: 2 * t > n and t < n, 'Peu probable': lambda t, n: 0 < 2 * t < n,
                    'Également probable': lambda t, n: 2 * t == n}
        for level in LEVELS:
            for q in _gen('probability-vocab', level, 150):
                en = q['prompt_en']
                target = re.search(r'Drawing an? (\w+) ball', en).group(1)
                counts = {c: int(n) for n, c in re.findall(r'(\d+) (\w+) balls?', en)}
                t = counts.get(target, 0)
                total = sum(counts.values())
                self.assertTrue(expected[q['correct_answers'][0]](t, total), en)
                self.assertNotRegex(q['prompt_fr'], r'billes (bleue|verte|violette)\b')
                self.assertNotIn('a orange', en)

    def test_read_bar_chart_bars_end_on_a_gridline(self):
        """read-bar-chart: the old chart only labelled 0, half and top, so most bars could not be read."""
        for level in LEVELS:
            for q in _gen('read-bar-chart', level):
                shape = q['shape_data'][0]
                ticks = {int(l['text']) for l in shape['labels'] if l['text'].isdigit() and l['anchor'] == 'end'}
                step = sorted(ticks)[1] - sorted(ticks)[0]
                for v in map(int, re.findall(r'monte à (\d+)', q['explanation_fr'])):
                    self.assertEqual(v % step, 0)
                self.assertEqual(int(q['correct_answers'][0]) % step, 0)
                self.assertNotIn('un(e)', q['prompt_fr'] + q['explanation_fr'])

    def test_pie_chart_largest_is_unique_and_quebec_wording(self):
        for level in LEVELS:
            for q in _gen('g5-pie-chart', level, 150):
                props = q['shape_data'][0]['proportions']
                self.assertEqual(len(set(props)), len(props), props)
                self.assertNotIn('Football', q['shape_data'][0]['categories'])
                en = localize_problem(copy.deepcopy(q), 'en')
                self.assertNotIn(' %', ' '.join(c['label'] for c in en['choices']) + en['explanation_en'])

    def test_line_graph_points_on_gridlines_and_unit_clear_of_ticks(self):
        """g4-line-graph: values fell between two ticks; the unit sat on top of the highest tick."""
        for level in LEVELS:
            for q in _gen('g4-line-graph', level):
                shape = q['shape_data'][0]
                grid_ys = {m['y1'] for m in shape['marks'] if m['type'] == 'line' and m['y1'] == m['y2'] and m['x1'] == 40}
                for d in (m for m in shape['marks'] if m['type'] == 'dot'):
                    self.assertTrue(any(abs(d['y'] - y) < 0.6 for y in grid_ys), d)
                ticks = [l for l in shape['labels'] if l['text'].isdigit() and l['anchor'] == 'end']
                units = [l for l in shape['labels'] if l['text'] in ('cm', '°C')]
                for u in units:
                    self.assertGreaterEqual(min(t['y'] for t in ticks) - 10 - u['y'], 2)
                self.assertNotIn('between on ', q['prompt_en'])
                self.assertNotIn('entre à la', q['prompt_fr'])


class PictographTests(SimpleTestCase):
    def test_half_symbol_is_drawn_as_half(self):
        """g3-pictograph: half symbols were a full emoji with a white rect *under* it (labels paint last)."""
        for q in _gen('g3-pictograph', 'hard', 120):
            shape = q['shape_data'][0]
            self.assertFalse(any(m['type'] == 'rect' and m.get('fill') == '#FFFFFF' for m in shape['marks']))
            if 'en tout' not in q['prompt_fr']:          # only the « total » question lists every row
                continue
            per = int(re.search(r'vaut (\d+)', q['prompt_fr']).group(1))
            circles = sum(1 for m in shape['marks'] if m['type'] == 'circle') - 1          # minus the key
            halves = sum(1 for m in shape['marks'] if m['type'] == 'path' and m.get('fill') not in (None, 'none'))
            self.assertEqual(halves, sum(1 for v in self._values(q) if v % per), q['explanation_fr'])
            self.assertEqual(circles, sum(v // per for v in self._values(q)))

    @staticmethod
    def _values(q):
        rows = [r for r in q['explanation_fr'].split('\n') if ' × ' in r and ' : ' in r]
        if rows:
            return [int(r.rsplit('= ', 1)[1]) for r in rows]
        return []

    def test_french_elision_and_neutral_icons(self):
        for level in LEVELS:
            for q in _gen('g3-pictograph', level):
                self.assertNotRegex(q['prompt_fr'], r'\bde [éeaio]')
                self.assertNotRegex(q['explanation_fr'], r'\b1 symboles\b')
                self.assertNotRegex(q['prompt_fr'], '🍎|⚽|🐾')


class ProbabilityTests(SimpleTestCase):
    def test_pile_is_tails(self):
        """« pile » is tails, « face » is heads — the English said the opposite."""
        for slug in ('g4-independence', 'g4-variability', 'g5-simulation', 'g3-list-outcomes', 'g5-who-is-right-data'):
            for level in LEVELS:
                for q in _gen(slug, level, 40):
                    for c in q.get('choices') or []:
                        fr, en = c['label'], c.get('label_en') or ''
                        if re.search(r'\bpiles?\b', fr) and not re.search(r'\bfaces?\b', fr):
                            self.assertIn('tails', en, (fr, en))
                    if re.search(r'\bpiles?\b', q['prompt_fr']) and not re.search(r'\bfaces?\b', q['prompt_fr']):
                        self.assertNotIn('heads', q['prompt_en'], q['prompt_en'])
        q = GENERATORS['g3-list-outcomes']('hard')
        for _ in range(40):
            q = GENERATORS['g3-list-outcomes']('hard')
            if q['q_type'] == 'multiple_choice':
                break
        self.assertIn('TT, TH, HT, HH', q['correct_answers'])

    def test_probability_frac_choices_and_wording(self):
        """Complement equal to the answer (3/6) used to be replaced by an unrelated « 40 »."""
        for level in LEVELS:
            for q in _gen('g5-probability-frac', level, 150):
                right = Fraction(q['correct_answers'][0])
                values = [Fraction(c['label']) for c in q['choices'] if '/' in c['label']]
                self.assertEqual(len(values), len(q['choices']), [c['label'] for c in q['choices']])
                self.assertEqual(sum(v == right for v in values), 1)
                self.assertNotIn('(s)', q['explanation_fr'] + q['explanation_en'])
                self.assertNotRegex(q['prompt_fr'], r'une bille (rouges|bleues|vertes|jaunes|oranges|violettes)\b')
                self.assertNotIn("1 d'autres", q['prompt_fr'])

    def test_probability_forms_english_notation(self):
        for level in LEVELS:
            for q in _gen('g5-probability-forms', level):
                en = localize_problem(copy.deepcopy(q), 'en')
                text = ' '.join(p['left'] + ' ' + p['right'] for p in en['pairs']) + en['explanation_en'] + en['hint_en']
                self.assertNotRegex(text, r'\d,\d')
                self.assertNotIn(' %', text)
                self.assertEqual(en['correct_answers'], [p['right'] for p in en['pairs']])

    def test_simulation_data_agrees_with_key(self):
        for q in _gen('g5-simulation', 'hard', 120):
            if not q.get('bullets'):
                continue
            (s, a), (b_, b) = [tuple(map(int, re.findall(r'(\d+) lancers, (\d+)', x[0])[0])) for x in q['bullets']]
            self.assertLess(abs(Fraction(b, b_) - Fraction(1, 2)), abs(Fraction(a, s) - Fraction(1, 2)))

    def test_independence_pronouns_and_hints(self):
        for level in LEVELS:
            for q in _gen('g4-independence', level):
                self.assertNotIn('Elle a tiré', q['prompt_fr'])
                self.assertNotIn('la pièce est lancée', ' '.join(c['label'] for c in q['choices']))
                self.assertNotIn('La pièce, le dé ou la roulette', q['hint_fr'])

    def test_variability_prediction_not_certain(self):
        for level in LEVELS:
            for q in _gen('g4-variability', level):
                self.assertNotIn('Que va-t-il se passer', q['prompt_fr'])
                self.assertRegex(q['explanation_fr'], r'[.!]$')


class CountingTests(SimpleTestCase):
    def test_count_outcomes_coherent_and_plausible(self):
        """Categories were drawn at random (shirts + flavours); choices were padded with +37 numbers."""
        from .generators.g5_stats import _OUTCOME_SCENARIOS
        allowed = [{c[0] for c in cats} for _, cats in _OUTCOME_SCENARIOS]
        for level in LEVELS:
            for q in _gen('g5-count-outcomes', level, 150):
                cats = {b[0].split(' : ')[0].lower() for b in q['bullets']}
                self.assertTrue(any(cats <= s for s in allowed), cats)
                nums = [int(b[0].split(' : ')[1].split()[0]) for b in q['bullets']]
                total = 1
                for n in nums:
                    total *= n
                self.assertEqual(q['correct_answers'], [str(total)])
                self.assertEqual(len(q['choices']), 5)
                self.assertTrue(all(c['correct'] or c['error_type'] not in ('', 'distractor') for c in q['choices']))

    def test_euler_articles_and_distractors(self):
        for level in LEVELS:
            for q in _gen('g5-euler', level):
                self.assertNotRegex(q['prompt_en'], r'\bA [AEIOU]')
                self.assertNotRegex(q['prompt_fr'], r'Un pyramide|Une? [A-ZÉ]')
                if q['prompt_fr'].startswith('Une pyramide'):
                    self.assertIn('a-t-elle', q['prompt_fr'])
                self.assertTrue(all(c['correct'] or c['error_type'] != 'distractor' for c in q['choices']))
                self.assertRegex(q['explanation_en'], r'Isolate the unknown: [VEF] = ')     # the isolation is shown

    def test_solid_counts_profiles_unique_and_complete(self):
        """Cube and rectangular prism (6/8/12) could both be on the left: two valid matchings."""
        for level in LEVELS:
            for q in _gen('g5-solid-counts', level, 100):
                rights = [p['right'] for p in q['pairs']]
                self.assertEqual(len(rights), len(set(rights)))
                for r in rights:
                    self.assertRegex(r, r'^\d+ faces, \d+ sommets, \d+ arêtes$')
                self.assertNotIn('Un cube a 6 faces', q['hint_fr'])


class ReasoningTests(SimpleTestCase):
    def test_who_is_right_choices_exclusive(self):
        """« X a raison » was also true when « Les deux ont raison » was the key."""
        for slug in ('g4-who-is-right-numbers', 'g5-who-is-right-shapes', 'g5-who-is-right-data'):
            for level in LEVELS:
                for q in _gen(slug, level, 40):
                    labels = [c['label'] for c in q['choices']]
                    self.assertFalse(any(re.fullmatch(r'\w+ a raison\.', l) for l in labels), labels)
                    self.assertEqual(q['prompt_fr'], q['prompt_fr'].strip())
                    self.assertEqual(q['prompt_en'], q['prompt_en'].strip())
                    self.assertNotIn('Vérifie chaque phrase toi-même', q['hint_fr'])
                    self.assertNotRegex(q['prompt_fr'], r'« C’est peu probable')

    def test_vocab_chance_and_survey_wording(self):
        for level in LEVELS:
            for q in _gen('g4-vocab-chance', level, 30):
                for p in q['pairs']:
                    if p['left'] == 'hasard':
                        self.assertNotEqual(p['left_en'], 'chance')
            for q in _gen('g4-survey-question', level, 40):
                self.assertNotIn('demander à les', q['explanation_fr'])
                self.assertNotIn('pas une seule', q['hint_fr'])

    def test_easy_vocab_sets_vary(self):
        for slug in ('g3-vocab-geometry', 'g3-vocab-measurement', 'g4-vocab-chance'):
            sets = {frozenset(p['left'] for p in GENERATORS[slug]('easy')['pairs']) for _ in range(40)}
            self.assertGreater(len(sets), 1, slug)
