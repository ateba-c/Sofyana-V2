"""
Regression tests for the QA pre-review fixes on time & measurement skills (group A):
right units, English notation, hints that do not give the answer away, keys that
match the question, explanations that follow the real numbers.
"""
import re

from django.test import SimpleTestCase

from . import illustrations as I
from .answers import check_answer, parse_duration
from .generators import GENERATORS
from .generators import clock, g4_time, measurement

RUNS = 150
LEVELS = ('easy', 'medium', 'hard')
FR_TIME = re.compile(r'\d h \d\d\b')
FR_DECIMAL = re.compile(r'\d,\d')


def samples(slug, levels=LEVELS, runs=RUNS):
    for level in levels:
        for _ in range(runs):
            yield level, GENERATORS[slug](level)


class EnglishNotationTests(SimpleTestCase):
    TIME_SLUGS = ['g3-clock-later', 'g4-clock-back', 'g5-clock-schedule', 'g6-clock-planning',
                  'g4-clock-24h', 'g4-elapsed-time', 'g4-end-time', 'read-clock']

    def test_no_french_clock_times_in_english(self):
        for slug in self.TIME_SLUGS:
            for level, q in samples(slug, runs=60):
                for k in ('prompt_en', 'hint_en', 'explanation_en'):
                    self.assertIsNone(FR_TIME.search(q[k]), f'{slug}/{level} {k}: {q[k]}')
                self.assertNotIn(' 0 h', q['hint_en'])

    def test_no_decimal_comma_in_english_conversions(self):
        for slug in ('g5-capacity-convert', 'g5-mass-convert'):
            for level, q in samples(slug):
                for k in ('prompt_en', 'hint_en', 'explanation_en'):
                    self.assertIsNone(FR_DECIMAL.search(q[k]), f'{slug}/{level} {k}: {q[k]}')
                self.assertEqual(len(q['correct_answers']), len(set(q['correct_answers'])))


class UnitChoiceTests(SimpleTestCase):
    EXPECTED = {'lettre': 'Gramme (g)', 'épices': 'Gramme (g)', 'éléphant': 'Kilogramme (kg)',
                'seringue': 'Millilitre (mL)', 'verre': 'Millilitre (mL)', 'cuillerée': 'Millilitre (mL)',
                'piscine': 'Litre (L)', 'Montréal': 'Kilomètre (km)', 'feuille de papier': 'Millimètre (mm)',
                'crayon': 'Centimètre (cm)', 'terrain de soccer': 'Mètre (m)'}

    def test_unit_by_quantity_fits_the_object(self):
        seen = set()
        for level, q in samples('unit-by-quantity'):
            correct = [c for c in q['choices'] if c['correct']]
            self.assertEqual(len(correct), 1)
            self.assertEqual(correct[0]['label'], q['correct_answers'][0])
            for word, unit in self.EXPECTED.items():
                if word in q['prompt_fr']:
                    seen.add(word)
                    self.assertEqual(q['correct_answers'][0], unit, q['prompt_fr'])
            self.assertNotIn('Litre', q['explanation_en'].replace('Litre (L)', '').replace('litre', ''))
            self.assertNotIn('|', q['hint_fr'])
        self.assertTrue({'lettre', 'seringue', 'Montréal'} <= seen)

    def test_measure_unit_objects_are_not_borderline(self):
        all_objects = [o for objs in measurement._OBJECTS.values() for o in objs]
        self.assertNotIn("le nez d'un chat", [fr for fr, _ in all_objects])


class HintTests(SimpleTestCase):
    def test_time_convert_hint_never_states_the_answer(self):
        for level, q in samples('time-convert'):
            answer = q['correct_answers'][0]
            self.assertNotIn(answer, re.findall(r'\d+', q['hint_fr']), q['hint_fr'])
            self.assertNotIn(answer, re.findall(r'\d+', q['hint_en']), q['hint_en'])
            self.assertIn(answer, q['explanation_fr'])

    def test_time_units_never_converts_a_single_unit(self):
        for level, q in samples('g4-time-units'):
            n = int(re.search(r'\*\*(\d+) ', q['prompt_fr']).group(1))
            self.assertGreaterEqual(n, 2, q['prompt_fr'])
            self.assertNotRegex(q['prompt_fr'], r'\*\* \*\*')          # « 1 jour 2 minutes » → « … et … »

    def test_conversion_hint_follows_the_direction(self):
        for slug, big, small in (('g5-capacity-convert', 'L', 'mL'), ('g5-mass-convert', 'kg', 'g')):
            for level, q in samples(slug):
                to_unit = re.search(r'en \*\*(\w+)\*\*', q['prompt_fr']).group(1)
                if to_unit == big:
                    self.assertIn('divise', q['hint_fr'])
                    self.assertIn('divide', q['hint_en'])
                else:
                    self.assertIn('multiplie', q['hint_fr'])

    def test_schedule_time_left_hint_subtracts(self):
        for level, q in samples('g5-clock-schedule'):
            if 'reste-t-il' in q['prompt_fr']:
                self.assertIn('−', q['hint_fr'])
                self.assertNotIn('Ajoute la durée totale', q['hint_fr'])
                self.assertEqual(len(q['correct_answers']), len(set(q['correct_answers'])))

    def test_planning_hint_keeps_noon_as_12(self):
        for level, q in samples('g6-clock-planning', runs=30):
            if 'reste-t-il' in q['prompt_fr']:
                continue
            self.assertIn('12 h reste 12 h', q['hint_fr'])
            self.assertNotIn('(après-midi : + 12)', q['hint_fr'])

    def test_capacity_estimate_hint_does_not_name_the_object(self):
        for level, q in samples('g3-capacity-estimate', levels=('hard',)):
            for word in ('verre', 'bouteille', 'cuillère', 'seau'):
                if word in q['prompt_fr']:
                    self.assertNotIn(word, q['hint_fr'])

    def test_protractor_estimate_hint_has_no_degree_value(self):
        for level, q in samples('g6-protractor', levels=('hard',)):
            self.assertNotIn('45°', q['hint_fr'])


class ClockKeyTests(SimpleTestCase):
    def test_clock_back_accepts_both_readings_of_the_face(self):
        for level, q in samples('g4-clock-back'):
            mins = parse_duration(q['correct_answers'][0])
            if 60 <= mins % 720:
                other = mins + 720 if mins < 720 else mins - 720
                h, m = divmod(other, 60)
                self.assertTrue(check_answer(f'{h} h {m:02d}', q['correct_answers'], 'duration'), q['correct_answers'])

    def test_end_time_is_24h_only(self):
        for level, q in samples('g4-end-time'):
            end = parse_duration(q['correct_answers'][0])
            if end >= 13 * 60:
                h, m = divmod(end - 720, 60)
                self.assertFalse(check_answer(f'{h} h {m:02d}', q['correct_answers'], 'duration'))
            self.assertTrue(check_answer(q['correct_answers'][0], q['correct_answers'], 'duration'))

    def test_read_clock_explanation_places_the_hour_hand(self):
        for level, q in samples('read-clock'):
            m = q['shape_data'][0]['minutes']
            if m:
                self.assertIn('entre le', q['explanation_fr'])
                self.assertNotIn('pointe vers', q['explanation_fr'])


class ExplanationTests(SimpleTestCase):
    def test_g5_elapsed_steps_stay_between_start_and_end(self):
        for level, q in samples('g5-elapsed-time'):
            start, end = [parse_duration(t) for t in re.findall(r'\*\*(\d+:\d\d)\*\*', q['prompt_fr'])]
            for t in re.findall(r'\b(\d+:\d\d)\b', q['explanation_fr']):
                self.assertTrue(start <= parse_duration(t) <= end, q['explanation_fr'])
            self.assertTrue(check_answer(f'{end - start} min', q['correct_answers'], 'duration'))

    def test_g4_elapsed_no_tautology_under_an_hour(self):
        for level, q in samples('g4-elapsed-time'):
            self.assertEqual(len(q['correct_answers']), len(set(q['correct_answers'])))
            self.assertNotRegex(q['explanation_fr'], r'= (\d+ min) = \1')

    def test_end_time_shows_the_minute_carry(self):
        for level, q in samples('g4-end-time', levels=('hard',)):
            start_m = int(re.search(r'commence à \*\*\d+ h (\d\d)\*\*', q['prompt_fr']).group(1))
            dur = parse_duration(re.search(r'dure \*\*(.+?)\*\*', q['prompt_fr']).group(1))
            if start_m + dur % 60 >= 60:
                self.assertIn('Minutes :', q['explanation_fr'])


class ContextTests(SimpleTestCase):
    def test_activities_fit_the_time_of_day_and_duration(self):
        for _ in range(500):
            start, dur = g4_time._times('hard')
            act = clock.pick_activity_for(start, dur)
            lo, hi, longest = clock._ACT_LIMITS.get(act[0], (None, None, 240))
            self.assertLessEqual(dur, longest)
            if lo is not None:
                self.assertGreaterEqual(start, lo)
        for level, q in samples('g4-end-time'):
            if 'lecture du soir' in q['prompt_fr']:
                self.assertGreaterEqual(int(re.search(r'à \*\*(\d+) h', q['prompt_fr']).group(1)), 18)

    def test_french_elisions(self):
        bad = re.compile(r"\bde (le|un|une) ")
        for slug in ('g5-area-units', 'g6-volume-units', 'g3-capacity-estimate', 'g3-balance-scale', 'g5-estimate-length'):
            for level, q in samples(slug, runs=80):
                self.assertIsNone(bad.search(q['prompt_fr']), f'{slug}: {q["prompt_fr"]}')
                self.assertNotIn('une trombone', q['prompt_fr'] + q['explanation_fr'])

    def test_thermometer_readings_match_the_level(self):
        for level, q in samples('g5-thermometer'):
            t = q['shape_data'][0]['temp']
            if level != 'easy':
                self.assertNotEqual(t % 10, 0, f'{level}: {t} sits on a numbered mark')
        for level, q in samples('g3-thermometer', levels=('easy', 'medium')):
            s = q['shape_data'][0]
            self.assertLess(s['temp'], s['max_temp'])

    def test_balance_weights_fit_in_the_picture(self):
        for n in range(1, 6):
            shape = I.balance(['🍎'], ['500 g'] * n)
            for mk in shape['marks']:
                if mk.get('type') == 'rect':
                    self.assertGreaterEqual(mk['x'], 0)
                    self.assertLessEqual(mk['x'] + mk['w'], shape['vw'])
