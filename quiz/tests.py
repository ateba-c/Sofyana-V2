from django.test import TestCase

from .answers import (
    check_answer, infer_answer_type, parse_number, parse_duration,
    parse_coordinate, normalize_text, input_spec,
)


class ParseNumberTests(TestCase):
    def test_integers_and_decimals(self):
        self.assertEqual(parse_number('6'), 6)
        self.assertEqual(parse_number('6.0'), 6)
        self.assertEqual(parse_number('6,0'), 6)
        self.assertEqual(parse_number(' 007 '), 7)
        self.assertEqual(parse_number('3.'), 3)
        self.assertEqual(parse_number('-2,5'), parse_number('-2.5'))
        self.assertEqual(parse_number('−3'), -3)          # unicode minus

    def test_thousands_with_spaces(self):
        self.assertEqual(parse_number('1 234'), 1234)
        self.assertEqual(parse_number('1 234 567'), 1234567)
        self.assertEqual(parse_number('3 500,5'), parse_number('3500.5'))

    def test_fractions_and_mixed(self):
        self.assertEqual(parse_number('3/4'), parse_number('0.75'))
        self.assertEqual(parse_number('4/6'), parse_number('2/3'))
        self.assertEqual(parse_number('1 1/2'), parse_number('1.5'))
        self.assertIsNone(parse_number('1/0'))

    def test_units_and_currency_ignored(self):
        self.assertEqual(parse_number('12 cm'), 12)
        self.assertEqual(parse_number('5 m²'), 5)
        self.assertEqual(parse_number('20 °C'), 20)
        self.assertEqual(parse_number('$4.50'), parse_number('4.5'))
        self.assertEqual(parse_number('4,50 $'), parse_number('4.5'))
        self.assertEqual(parse_number('120 cm³'), 120)

    def test_garbage(self):
        self.assertIsNone(parse_number(''))
        self.assertIsNone(parse_number('abc'))
        self.assertIsNone(parse_number(None))


class ParseOtherTests(TestCase):
    def test_duration(self):
        self.assertEqual(parse_duration('1 h 30 min'), 90)
        self.assertEqual(parse_duration('1h30'), 90)
        self.assertEqual(parse_duration('1:30'), 90)
        self.assertEqual(parse_duration('90 min'), 90)
        self.assertEqual(parse_duration('2 h'), 120)
        self.assertEqual(parse_duration('2 heures'), 120)
        self.assertEqual(parse_duration('45'), 45)
        self.assertIsNone(parse_duration('bonjour'))

    def test_coordinate(self):
        self.assertEqual(parse_coordinate('(3, 4)'), (3, 4))
        self.assertEqual(parse_coordinate('3,4'), (3, 4))
        self.assertEqual(parse_coordinate('3 ; 4'), (3, 4))
        self.assertIsNone(parse_coordinate('3'))

    def test_normalize_text(self):
        self.assertEqual(normalize_text('  Élève !'), 'eleve')
        self.assertEqual(normalize_text('Triangle.'), normalize_text('triangle'))


class InferTests(TestCase):
    def test_inference(self):
        self.assertEqual(infer_answer_type(['42']), 'integer')
        self.assertEqual(infer_answer_type(['3 500']), 'integer')
        self.assertEqual(infer_answer_type(['3,5', '3.5']), 'decimal')
        self.assertEqual(infer_answer_type(['2/3']), 'fraction')
        self.assertEqual(infer_answer_type(['1 h 30 min', '90 min']), 'duration')
        self.assertEqual(infer_answer_type(['(3, 4)', '3, 4']), 'coordinate')
        self.assertEqual(infer_answer_type(['<']), 'symbol')
        self.assertEqual(infer_answer_type(['4,50 $', '$4.50']), 'money')
        self.assertEqual(infer_answer_type(['Yes']), 'text')
        self.assertEqual(infer_answer_type(['cm']), 'text')
        self.assertEqual(infer_answer_type(['120', '120 cm³']), 'integer')
        self.assertEqual(infer_answer_type([]), 'text')


class CheckAnswerTests(TestCase):
    """The '6 is not 6' family of bugs."""

    def test_six_equals_six(self):
        self.assertTrue(check_answer('6', ['6.0']))
        self.assertTrue(check_answer('6.0', ['6']))
        self.assertTrue(check_answer('6,0', ['6']))
        self.assertTrue(check_answer('6 cm', ['6']))
        self.assertTrue(check_answer(' 6 ', ['6']))
        self.assertFalse(check_answer('7', ['6']))

    def test_decimal_equivalents(self):
        self.assertTrue(check_answer('0.50', ['0,5']))
        self.assertTrue(check_answer('.5', ['0.5']))
        self.assertTrue(check_answer('1/2', ['0.5']))
        self.assertTrue(check_answer('0.5', ['1/2'], 'fraction'))
        self.assertFalse(check_answer('0.5', ['0.05']))

    def test_fractions(self):
        self.assertTrue(check_answer('4/6', ['2/3']))
        self.assertTrue(check_answer('1 1/2', ['3/2']))
        self.assertFalse(check_answer('2/3', ['3/2']))

    def test_duration_and_coordinates(self):
        self.assertTrue(check_answer('90 min', ['1 h 30 min'], 'duration'))
        self.assertTrue(check_answer('1h30', ['1 h 30 min']))
        self.assertFalse(check_answer('1 h 20 min', ['1 h 30 min']))
        self.assertTrue(check_answer('3;4', ['(3, 4)', '3, 4', '3,4']))
        self.assertFalse(check_answer('4, 3', ['(3, 4)']))

    def test_symbols(self):
        self.assertTrue(check_answer(' < ', ['<']))
        self.assertTrue(check_answer('<=', ['≤']))
        self.assertFalse(check_answer('>', ['<']))

    def test_text(self):
        self.assertTrue(check_answer('triangle', ['Triangle']))
        self.assertTrue(check_answer('Angle aigu', ['angle aigu', 'acute angle']))
        self.assertTrue(check_answer('CARRE', ['carré']))
        self.assertTrue(check_answer('Yes.', ['Yes']))
        self.assertFalse(check_answer('No', ['Yes']))

    def test_money(self):
        self.assertTrue(check_answer('4.5', ['4,50 $', '$4.50']))
        self.assertTrue(check_answer('4,50$', ['4,50 $']))

    def test_wrong_declared_type_never_breaks_correct_answer(self):
        # Declared 'integer' but the answer is a word: tolerant fallback still works.
        self.assertTrue(check_answer('carré', ['Carré'], 'integer'))

    def test_empty(self):
        self.assertFalse(check_answer('', ['6']))
        self.assertFalse(check_answer('6', []))


class InputSpecTests(TestCase):
    def test_spec(self):
        self.assertEqual(input_spec('integer')['inputmode'], 'numeric')
        self.assertEqual(input_spec('decimal', 'fr')['placeholder'], '3,5')
        self.assertEqual(input_spec('bogus')['answer_type'], 'bogus')
        self.assertEqual(input_spec(None)['answer_type'], 'text')
