"""QC-079 / QC-080: equivalences with decimals — every key recomputed from the prompt."""
import re
from fractions import Fraction

from django.test import SimpleTestCase

from .answers import check_answer, parse_number
from .generators import GENERATORS, SKILL_MAP
from .generators.resolution import RESOLUTION

SLUGS = ('g4-decimal-equivalences', 'g5-decimal-properties')


def value(expr):
    """Exact value of '3,96 + 4,61' / '9 × 6 + 9 × 0.7' / '13.1 − 8.9'."""
    e = expr.replace('**', '').replace(',', '.').replace('×', '*').replace('÷', '/').replace('−', '-')
    e = re.sub(r'\d+(?:\.\d+)?', lambda m: f'Fraction("{m.group()}")', e)
    return eval(e, {'Fraction': Fraction})


class DecimalEquivalenceTests(SimpleTestCase):
    def test_wired_with_four_levels(self):
        for slug in SLUGS:
            self.assertIn(slug, GENERATORS)
            self.assertEqual(SKILL_MAP[slug]['level_sequence'][-1], 'resolution')
            for _ in range(50):
                RESOLUTION[slug]()

    def test_keys(self):
        for slug in SLUGS:
            for level in ('easy', 'medium', 'hard'):
                for _ in range(300):
                    q = GENERATORS[slug](level)
                    p = q['prompt_en']
                    self.assertNotRegex(p, r'\d,\d', f'French decimal comma in English: {p}')
                    if q['q_type'] == 'multiple_choice':
                        target = value(re.search(r'\*\*(.+?)\*\*', p).group(1))
                        equal = [c for c in q['choices'] if value(c.get('label_en', c['label'])) == target]
                        self.assertEqual(len(equal), 1, (p, [c['label'] for c in q['choices']]))
                        self.assertTrue(equal[0]['correct'])
                        continue
                    for a in q['correct_answers']:
                        self.assertTrue(check_answer(a, q['correct_answers'], 'decimal'))
                    got = parse_number(q['correct_answers'][0])
                    self.assertGreater(got, 0)
                    exprs = re.findall(r'\*\*(.+?)\*\*', p)
                    last = exprs[-1]
                    if '?' in last:                                   # "a + b = c + ?" / "n × a = n × w + n × ?"
                        left, right = last.split('=')
                        self.assertEqual(value(left), value(right.replace('?', str(got))), p)
                    elif 'Without calculating' in p or 'Calculate' in p or 'Multiplying' in p:
                        self.assertEqual(value(last), got, p)
