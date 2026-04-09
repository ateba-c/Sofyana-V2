"""
missing_terms.py — Grade-3 missing-term generators.

Topics (content.md Thème 1, section 8):
  missing_addend_gen      typed  –  a + __ = c  →  find c - a
  missing_subtrahend_gen  typed  –  a - __ = c  →  find a - c

Difficulty governs number range:
  easy   → single / small double digits (0-20)
  medium → 2-3 digit numbers (10-500)
  hard   → 3-4 digit numbers (100-5000), larger gaps
"""

import random
from .base import _tagged_shuffle_mc


def missing_addend_gen(level: str = 'medium') -> dict:
    """
    Typed — find the missing addend:  a + __ = c
    The answer is always non-negative.
    """
    if level == 'easy':
        a = random.randint(0, 15)
        c = random.randint(a, 20)
    elif level == 'medium':
        a = random.randint(10, 400)
        c = random.randint(a, a + random.randint(10, 300))
    else:
        a = random.randint(100, 4000)
        c = random.randint(a, a + random.randint(100, 2000))

    missing = c - a  # always ≥ 0

    return {
        'q_type': 'text_input',
        'prompt_fr': f'Complète : **{a} + ___ = {c}**',
        'prompt_en': f'Complete: **{a} + ___ = {c}**',
        'hint_fr': f'Cherche combien il faut ajouter à {a} pour obtenir {c}.',
        'hint_en': f'Find how much you must add to {a} to get {c}.',
        'shape_data': [],
        'choices': [],
        'correct_answers': [str(missing)],
        'time_limit': 30,
        'points': 1,
        'explanation_fr': (
            f'Si {a} + ___ = {c}, alors ___ = {c} − {a} = **{missing}**.\n'
            f'La soustraction est l\'opération inverse de l\'addition.'
        ),
        'explanation_en': (
            f'If {a} + ___ = {c}, then ___ = {c} − {a} = **{missing}**.\n'
            f'Subtraction is the inverse of addition.'
        ),
    }


def missing_subtrahend_gen(level: str = 'medium') -> dict:
    """
    Typed — find the missing subtrahend:  a - __ = c
    Guarantees result (a - c) ≥ 0.
    """
    if level == 'easy':
        c = random.randint(0, 15)
        a = random.randint(c, 20)
    elif level == 'medium':
        c = random.randint(0, 300)
        a = random.randint(c + 10, c + 400)
    else:
        c = random.randint(0, 3000)
        a = random.randint(c + 100, c + 3000)

    missing = a - c  # always ≥ 0

    return {
        'q_type': 'text_input',
        'prompt_fr': f'Complète : **{a} - ___ = {c}**',
        'prompt_en': f'Complete: **{a} - ___ = {c}**',
        'hint_fr': f'Cherche ce qu\'on enlève à {a} pour obtenir {c}.',
        'hint_en': f'Find what is subtracted from {a} to get {c}.',
        'shape_data': [],
        'choices': [],
        'correct_answers': [str(missing)],
        'time_limit': 30,
        'points': 1,
        'explanation_fr': (
            f'Si {a} − ___ = {c}, alors ___ = {a} − {c} = **{missing}**.\n'
            f'Vérifie : {a} − {missing} = {c} ✓'
        ),
        'explanation_en': (
            f'If {a} − ___ = {c}, then ___ = {a} − {c} = **{missing}**.\n'
            f'Check: {a} − {missing} = {c} ✓'
        ),
    }
