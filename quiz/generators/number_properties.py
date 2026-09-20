"""
Generators for: square numbers, prime numbers, even/odd numbers — all ≤ 200.
"""
import random
from .base import _shuffle_mc, _tagged_shuffle_mc

# ── precomputed sets (all values ≤ 200) ──────────────────────────────────────

def _sieve(limit):
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            for j in range(i * i, limit + 1, i):
                is_p[j] = False
    return [n for n in range(2, limit + 1) if is_p[n]]


LIMIT       = 200
PRIMES      = _sieve(LIMIT)                                          # [2,3,5,…,199]
PRIMES_SET  = set(PRIMES)
SQUARES     = [n * n for n in range(1, 15) if n * n <= LIMIT]       # [1,4,9,…,196]
SQUARES_SET = set(SQUARES)
COMPOSITES  = [n for n in range(4, LIMIT + 1) if n not in PRIMES_SET]
NON_SQUARES = [n for n in range(2, LIMIT + 1) if n not in SQUARES_SET]
EVENS       = list(range(2, LIMIT + 1, 2))
ODDS        = list(range(1, LIMIT,     2))
EVEN_SQUARES = [n for n in SQUARES if n % 2 == 0]   # 4,16,36,64,100,144,196
ODD_PRIMES   = [p for p in PRIMES if p % 2 != 0]    # all primes except 2


# ── helpers ───────────────────────────────────────────────────────────────────

def _binary_mc(correct_label, wrong_label, wrong_error_type='', wrong_fb_en='', wrong_fb_fr=''):
    """Return shuffled 2-choice MC list with misconception metadata on the wrong choice."""
    choices = [
        {'label': correct_label, 'correct': True,  'error_type': '',              'feedback_en': '',          'feedback_fr': ''},
        {'label': wrong_label,   'correct': False, 'error_type': wrong_error_type, 'feedback_en': wrong_fb_en, 'feedback_fr': wrong_fb_fr},
    ]
    random.shuffle(choices)
    return choices


def _yesno(is_yes, wrong_error_type='', wrong_fb_en='', wrong_fb_fr=''):
    if is_yes:
        return _binary_mc('Yes', 'No', wrong_error_type, wrong_fb_en, wrong_fb_fr)
    else:
        return _binary_mc('No', 'Yes', wrong_error_type, wrong_fb_en, wrong_fb_fr)


def _smallest_factor(n):
    for p in range(2, n):
        if n % p == 0:
            return p
    return n


def _near_non_squares(sq, n=4):
    """Return n numbers close to sq that are NOT perfect squares."""
    out, seen = [], set()
    for d in range(1, 40):
        for x in (sq + d, sq - d):
            if x > 1 and x <= LIMIT and x not in SQUARES_SET and x not in seen:
                seen.add(x)
                out.append(str(x))
                if len(out) == n:
                    return out
    return out


def _near_composites(p, n=4):
    """Return n composites close to prime p."""
    out, seen = [], set()
    for d in range(1, 60):
        for x in (p + d, p - d):
            if x > 1 and x <= LIMIT and x not in PRIMES_SET and x not in seen:
                seen.add(x)
                out.append(str(x))
                if len(out) == n:
                    return out
    return out


def _near_odds(e, n=4):
    return [str(e + d) for d in (-3, -1, 1, 3) if (e + d) > 0 and (e + d) % 2 == 1][:n]


def _near_evens(o, n=4):
    return [str(o + d) for d in (-2, 2, -4, 4) if (o + d) > 0 and (o + d) % 2 == 0][:n]


# ── SQUARE NUMBERS ─────────────────────────────────────────────────────────────

def squares_gen(level='medium'):
    if level == 'easy':
        # "Is N a perfect square?"  Yes / No
        pool = SQUARES[:7] + [n for n in NON_SQUARES if n < 50]
        n    = random.choice(pool)
        is_sq = n in SQUARES_SET
        return {
            'q_type':          'multiple_choice',
            'prompt_en':       f'Is {n} a perfect square?',
            'prompt_fr':       f'{n} est-il un carré parfait ?',
            'hint_en':         'Perfect squares: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100 …',
            'hint_fr':         'Carrés parfaits : 1, 4, 9, 16, 25, 36, 49, 64, 81, 100 …',
            'shape_data':      [],
            'choices':         _yesno(
                is_sq,
                wrong_error_type='not_square',
                wrong_fb_en="That number is not a perfect square — try multiplying a whole number by itself.",
                wrong_fb_fr="Ce nombre n'est pas un carré parfait — essaie de multiplier un entier par lui-même.",
            ),
            'correct_answers': ['Yes' if is_sq else 'No'],
            'time_limit':      15,
            'points':          1,
            'explanation_en':  (f'{n} = {int(n**0.5)}² — yes, it is a perfect square.'
                                if is_sq else f'{n} is not a perfect square.'),
            'explanation_fr':  (f'{n} = {int(n**0.5)}² — oui, c\'est un carré parfait.'
                                if is_sq else f'{n} n\'est pas un carré parfait.'),
        }

    elif level == 'medium':
        # 25% chance: mix_match — match N² to its value
        if random.random() < 0.25:
            bases  = random.sample(range(2, 13), 4)
            pairs  = [{'left': f'{b}²', 'right': str(b * b)} for b in bases]
            explanation_en = 'Correct pairs:\n' + '\n'.join(
                f'{p["left"]} = {p["right"]}' for p in pairs
            )
            explanation_fr = 'Paires correctes :\n' + '\n'.join(
                f'{p["left"]} = {p["right"]}' for p in pairs
            )
            return {
                'q_type':          'mix_match',
                'prompt_en':       'Match each expression to its value.',
                'prompt_fr':       'Associez chaque expression à sa valeur.',
                'hint_en':         'N² means N × N.',
                'hint_fr':         'N² signifie N × N.',
                'shape_data':      [],
                'pairs':           pairs,
                'correct_answers': [],
                'time_limit':      30,
                'points':          3,
                'explanation_en':  explanation_en,
                'explanation_fr':  explanation_fr,
            }

        # "Which of these is a perfect square?"
        sq          = random.choice(SQUARES[1:])           # skip 1 (too obvious)
        distractors = _near_non_squares(sq, 4)
        tagged_candidates = [
            (
                d,
                'not_square',
                "That number is not a perfect square — try multiplying a whole number by itself.",
                "Ce nombre n'est pas un carré parfait — essaie de multiplier un entier par lui-même.",
            )
            for d in distractors
        ]
        choices     = _tagged_shuffle_mc(str(sq), tagged_candidates)
        root        = int(sq ** 0.5)
        return {
            'q_type':          'multiple_choice',
            'prompt_en':       'Which of these is a perfect square?',
            'prompt_fr':       'Lequel de ces nombres est un carré parfait ?',
            'hint_en':         'A perfect square is the product of a whole number with itself.',
            'hint_fr':         'Un carré parfait est le produit d\'un entier par lui-même.',
            'shape_data':      [],
            'choices':         choices,
            'correct_answers': [str(sq)],
            'time_limit':      20,
            'points':          2,
            'explanation_en':  (f'Step 1: Look for a whole number that × itself = {sq}.\n'
                                f'Step 2: Check: {root} × {root} = {sq}.\n'
                                f'Answer: {sq} = {root}²'),
            'explanation_fr':  (f'Étape 1 : Cherche un entier qui × lui-même = {sq}.\n'
                                f'Étape 2 : Vérifie : {root} × {root} = {sq}.\n'
                                f'Réponse : {sq} = {root}²'),
        }

    else:  # hard — squares only (no square roots in primary school)
        # 25% chance: mix_match — match n² to its value
        if random.random() < 0.25:
            roots = random.sample(range(3, 15), 4)
            pairs = [{'left': f'{r}²', 'right': str(r * r)} for r in roots]
            return {
                'q_type':          'mix_match',
                'prompt_en':       'Match each square to its value.',
                'prompt_fr':       'Associe chaque carré à sa valeur.',
                'hint_en':         'n² means n × n.',
                'hint_fr':         'n² veut dire n × n.',
                'show_illustration': False,
                'shape_data':      [],
                'choices':         [],
                'pairs':           pairs,
                'correct_answers': [p['right'] for p in pairs],
                'time_limit':      35,
                'points':          3,
                'explanation_en':  '\n'.join(f'{r}² = {r} × {r} = {r * r}' for r in roots),
                'explanation_fr':  '\n'.join(f'{r}² = {r} × {r} = {r * r}' for r in roots),
            }

        if random.random() < 0.5:
            # "What is 12²?"
            root = random.randint(6, 15)
            sq = root * root
            tagged_candidates = [
                (str(root * 2), 'doubled', 'n² means n × n, not n × 2.', 'n² veut dire n × n, pas n × 2.'),
                (str((root + 1) ** 2), 'off_by_one', 'Check: which number times itself?', 'Vérifie : quel nombre fois lui-même ?'),
                (str((root - 1) ** 2), 'off_by_one', 'Check: which number times itself?', 'Vérifie : quel nombre fois lui-même ?'),
                (str(sq + root), 'wrong_product', 'Multiply carefully.', 'Multiplie soigneusement.'),
                (str(sq - root), 'wrong_product', 'Multiply carefully.', 'Multiplie soigneusement.'),
            ]
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       f'What is {root}²?',
                'prompt_fr':       f'Combien vaut {root}² ?',
                'hint_en':         f'{root}² = {root} × {root}.',
                'hint_fr':         f'{root}² = {root} × {root}.',
                'show_illustration': False,
                'shape_data':      [],
                'choices':         _tagged_shuffle_mc(str(sq), tagged_candidates),
                'pairs':           [],
                'correct_answers': [str(sq)],
                'time_limit':      20,
                'points':          2,
                'explanation_en':  f'{root}² = {root} × {root} = {sq}',
                'explanation_fr':  f'{root}² = {root} × {root} = {sq}',
            }

        # "Which number, multiplied by itself, gives N?"
        root = random.randint(4, 15)
        sq = root * root
        return {
            'q_type':          'text_input',
            'answer_type':     'integer',
            'prompt_en':       f'Which number, multiplied by itself, gives {sq}?',
            'prompt_fr':       f'Quel nombre, multiplié par lui-même, donne {sq} ?',
            'hint_en':         f'Try the squares you know: 10 × 10 = 100, 12 × 12 = 144…',
            'hint_fr':         f'Essaie les carrés que tu connais : 10 × 10 = 100, 12 × 12 = 144…',
            'show_illustration': False,
            'shape_data':      [],
            'choices':         [],
            'pairs':           [],
            'correct_answers': [str(root)],
            'time_limit':      25,
            'points':          2,
            'explanation_en':  f'{root} × {root} = {sq}, so the number is {root}.',
            'explanation_fr':  f'{root} × {root} = {sq}, donc le nombre est {root}.',
        }


def primes_gen(level='medium'):
    if level == 'easy':
        # "Is N prime?"  Yes / No — small numbers
        pool_p = PRIMES[:12]            # 2 … 37
        pool_c = COMPOSITES[:12]        # 4, 6, 8, 9, 10 …
        n      = random.choice(pool_p + pool_c)
        is_p   = n in PRIMES_SET
        sf     = _smallest_factor(n) if not is_p else None
        return {
            'q_type':          'multiple_choice',
            'prompt_en':       f'Is {n} a prime number?',
            'prompt_fr':       f'{n} est-il un nombre premier ?',
            'hint_en':         'A prime has exactly two factors: 1 and itself.',
            'hint_fr':         'Un premier a exactement deux diviseurs : 1 et lui-même.',
            'shape_data':      [],
            'choices':         _yesno(
                is_p,
                wrong_error_type='not_prime',
                wrong_fb_en="That number is composite — check if it's divisible by a small prime.",
                wrong_fb_fr="Ce nombre est composé — vérifie s'il est divisible par un petit nombre premier.",
            ),
            'correct_answers': ['Yes' if is_p else 'No'],
            'time_limit':      15,
            'points':          1,
            'explanation_en':  (f'{n} is prime — its only factors are 1 and {n}.'
                                if is_p else f'{n} is not prime — it is divisible by {sf}.'),
            'explanation_fr':  (f'{n} est premier — ses seuls diviseurs sont 1 et {n}.'
                                if is_p else f'{n} n\'est pas premier — il est divisible par {sf}.'),
        }

    elif level == 'medium':
        # 25% chance: mix_match — match number → Prime or Composite
        if random.random() < 0.25:
            primes_pool     = [p for p in PRIMES if p < 100]
            composites_pool = [c for c in COMPOSITES if c < 100]
            chosen_primes   = random.sample(primes_pool, 2)
            chosen_comps    = random.sample(composites_pool, 2)
            pairs = (
                [{'left': str(p), 'right': 'Prime'} for p in chosen_primes] +
                [{'left': str(c), 'right': 'Composite'} for c in chosen_comps]
            )
            random.shuffle(pairs)
            explanation_en = 'Correct pairs:\n' + '\n'.join(
                f'{p["left"]} → {p["right"]}' for p in pairs
            )
            explanation_fr = 'Paires correctes :\n' + '\n'.join(
                f'{p["left"]} → {p["right"]}' for p in pairs
            )
            return {
                'q_type':          'mix_match',
                'prompt_en':       'Match each number to its type: Prime or Composite.',
                'prompt_fr':       'Associez chaque nombre à son type : Premier ou Composé.',
                'hint_en':         'A prime has exactly two factors: 1 and itself.',
                'hint_fr':         'Un nombre premier a exactement deux diviseurs : 1 et lui-même.',
                'shape_data':      [],
                'pairs':           pairs,
                'correct_answers': [],
                'time_limit':      30,
                'points':          3,
                'explanation_en':  explanation_en,
                'explanation_fr':  explanation_fr,
            }

        # "Which of these is prime?"  (numbers < 100)
        pool        = [p for p in PRIMES if p < 100]
        correct     = random.choice(pool)
        distractors = _near_composites(correct, 4)
        tagged_candidates = [
            (
                d,
                'not_prime',
                "That number is composite — check if it's divisible by a small prime.",
                "Ce nombre est composé — vérifie s'il est divisible par un petit nombre premier.",
            )
            for d in distractors
        ]
        choices     = _tagged_shuffle_mc(str(correct), tagged_candidates)
        return {
            'q_type':          'multiple_choice',
            'prompt_en':       'Which of these is a prime number?',
            'prompt_fr':       'Lequel de ces nombres est un nombre premier ?',
            'hint_en':         'Try dividing each by 2, 3, 5, 7 …',
            'hint_fr':         'Essayez de diviser chacun par 2, 3, 5, 7 …',
            'shape_data':      [],
            'choices':         choices,
            'correct_answers': [str(correct)],
            'time_limit':      25,
            'points':          2,
            'explanation_en':  f'{correct} is prime — its only factors are 1 and {correct}.',
            'explanation_fr':  f'{correct} est premier — ses seuls diviseurs sont 1 et {correct}.',
        }

    else:  # hard
        # 25% chance: mix_match — match larger numbers → Prime or Composite
        if random.random() < 0.25:
            primes_pool     = [p for p in PRIMES if 50 <= p <= LIMIT]
            composites_pool = [c for c in COMPOSITES if 50 <= c <= LIMIT]
            chosen_primes   = random.sample(primes_pool, 2)
            chosen_comps    = random.sample(composites_pool, 2)
            pairs = (
                [{'left': str(p), 'right': 'Prime'} for p in chosen_primes] +
                [{'left': str(c), 'right': 'Composite'} for c in chosen_comps]
            )
            random.shuffle(pairs)
            explanation_en = 'Correct pairs:\n' + '\n'.join(
                f'{p["left"]} → {p["right"]}' for p in pairs
            )
            explanation_fr = 'Paires correctes :\n' + '\n'.join(
                f'{p["left"]} → {p["right"]}' for p in pairs
            )
            return {
                'q_type':          'mix_match',
                'prompt_en':       'Match each number to its type: Prime or Composite.',
                'prompt_fr':       'Associez chaque nombre à son type : Premier ou Composé.',
                'hint_en':         'Test divisibility by 2, 3, 5, 7, 11, 13.',
                'hint_fr':         'Testez la divisibilité par 2, 3, 5, 7, 11, 13.',
                'shape_data':      [],
                'pairs':           pairs,
                'correct_answers': [],
                'time_limit':      40,
                'points':          4,
                'explanation_en':  explanation_en,
                'explanation_fr':  explanation_fr,
            }

        if random.random() < 0.5:
            # "Which of these (100–200) is prime?"
            pool        = [p for p in PRIMES if 100 <= p <= LIMIT]
            correct     = random.choice(pool)
            distractors = _near_composites(correct, 4)
            tagged_candidates = [
                (
                    d,
                    'not_prime',
                    "That number is composite — check if it's divisible by a small prime.",
                    "Ce nombre est composé — vérifie s'il est divisible par un petit nombre premier.",
                )
                for d in distractors
            ]
            choices     = _tagged_shuffle_mc(str(correct), tagged_candidates)
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       'Which of these numbers (100 – 200) is prime?',
                'prompt_fr':       'Lequel de ces nombres (100 – 200) est premier ?',
                'hint_en':         'Test divisibility by 2, 3, 5, 7, 11, 13 (all primes ≤ √200).',
                'hint_fr':         'Testez la divisibilité par 2, 3, 5, 7, 11, 13.',
                'shape_data':      [],
                'choices':         choices,
                'correct_answers': [str(correct)],
                'time_limit':      35,
                'points':          3,
                'explanation_en':  f'{correct} is prime.',
                'explanation_fr':  f'{correct} est premier.',
            }
        else:
            # "Which of these is NOT prime?"  (4 primes + 1 composite)
            pool       = [p for p in PRIMES if p < 100]
            four_p     = random.sample(pool, 4)
            composite  = None
            for p in four_p:
                cands = [x for x in (p+1, p-1, p+2, p-2)
                         if x > 1 and x not in PRIMES_SET and x <= LIMIT]
                if cands:
                    composite = random.choice(cands)
                    break
            if not composite:
                composite = random.choice(COMPOSITES)
            sf       = _smallest_factor(composite)
            pos      = random.randint(0, 4)
            all_ch   = [
                {
                    'label': str(p),
                    'correct': False,
                    'error_type': 'not_prime',
                    'feedback_en': "That number is composite — check if it's divisible by a small prime.",
                    'feedback_fr': "Ce nombre est composé — vérifie s'il est divisible par un petit nombre premier.",
                }
                for p in four_p
            ]
            all_ch.insert(pos, {'label': str(composite), 'correct': True, 'error_type': '', 'feedback_en': '', 'feedback_fr': ''})
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       'Which of these is NOT a prime number?',
                'prompt_fr':       'Lequel de ces nombres n\'est PAS un nombre premier ?',
                'hint_en':         'The composite number has more than two factors.',
                'hint_fr':         'Le nombre composé a plus de deux diviseurs.',
                'shape_data':      [],
                'choices':         all_ch[:5],
                'correct_answers': [str(composite)],
                'time_limit':      30,
                'points':          3,
                'explanation_en':  f'{composite} is not prime — it is divisible by {sf}.',
                'explanation_fr':  f'{composite} n\'est pas premier — il est divisible par {sf}.',
            }


# ── EVEN / ODD ─────────────────────────────────────────────────────────────────

def even_odd_gen(level='medium'):
    if level == 'easy':
        # "Is N even or odd?"
        n      = random.randint(1, 100)
        is_even = n % 2 == 0
        return {
            'q_type':          'multiple_choice',
            'prompt_en':       f'Is {n} even or odd?',
            'prompt_fr':       f'{n} est-il pair ou impair ?',
            'hint_en':         'Even numbers end in 0, 2, 4, 6 or 8.',
            'hint_fr':         'Les nombres pairs se terminent par 0, 2, 4, 6 ou 8.',
            'shape_data':      [],
            'choices':         (
                _binary_mc(
                    'Even', 'Odd',
                    wrong_error_type='parity_confusion',
                    wrong_fb_en="Check the last digit — even numbers end in 0,2,4,6,8.",
                    wrong_fb_fr="Vérifie le dernier chiffre — les nombres pairs se terminent par 0,2,4,6,8.",
                ) if is_even else
                _binary_mc(
                    'Odd', 'Even',
                    wrong_error_type='parity_confusion',
                    wrong_fb_en="Check the last digit — even numbers end in 0,2,4,6,8.",
                    wrong_fb_fr="Vérifie le dernier chiffre — les nombres pairs se terminent par 0,2,4,6,8.",
                )
            ),
            'correct_answers': ['Even' if is_even else 'Odd'],
            'time_limit':      10,
            'points':          1,
            'explanation_en':  f'{n} is {"even" if is_even else "odd"}.',
            'explanation_fr':  f'{n} est {"pair" if is_even else "impair"}.',
        }

    elif level == 'medium':
        # 25% chance: mix_match — match numbers → Even or Odd
        if random.random() < 0.25:
            chosen_evens = random.sample(EVENS[:50], 2)
            chosen_odds  = random.sample(ODDS[:50], 2)
            pairs = (
                [{'left': str(e), 'right': 'Even'} for e in chosen_evens] +
                [{'left': str(o), 'right': 'Odd'}  for o in chosen_odds]
            )
            random.shuffle(pairs)
            explanation_en = 'Correct pairs:\n' + '\n'.join(
                f'{p["left"]} → {p["right"]}' for p in pairs
            )
            explanation_fr = 'Paires correctes :\n' + '\n'.join(
                f'{p["left"]} → {p["right"]}' for p in pairs
            )
            return {
                'q_type':          'mix_match',
                'prompt_en':       'Match each number to Even or Odd.',
                'prompt_fr':       'Associez chaque nombre à Pair ou Impair.',
                'hint_en':         'Even numbers end in 0, 2, 4, 6 or 8.',
                'hint_fr':         'Les nombres pairs se terminent par 0, 2, 4, 6 ou 8.',
                'shape_data':      [],
                'pairs':           pairs,
                'correct_answers': [],
                'time_limit':      20,
                'points':          2,
                'explanation_en':  explanation_en,
                'explanation_fr':  explanation_fr,
            }

        subtype = random.choice(['which_even', 'which_odd'])
        if subtype == 'which_even':
            correct     = random.choice(EVENS)
            distractors = _near_odds(correct, 4)
            tagged_candidates = [
                (
                    d,
                    'parity_confusion',
                    "Check the last digit — even numbers end in 0,2,4,6,8.",
                    "Vérifie le dernier chiffre — les nombres pairs se terminent par 0,2,4,6,8.",
                )
                for d in distractors
            ]
            choices     = _tagged_shuffle_mc(str(correct), tagged_candidates)
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       'Which of these is an even number?',
                'prompt_fr':       'Lequel de ces nombres est pair ?',
                'hint_en':         'Even numbers are exactly divisible by 2.',
                'hint_fr':         'Les nombres pairs sont divisibles par 2 sans reste.',
                'shape_data':      [],
                'choices':         choices,
                'correct_answers': [str(correct)],
                'time_limit':      15,
                'points':          1,
                'explanation_en':  f'{correct} is even ({correct} ÷ 2 = {correct // 2}).',
                'explanation_fr':  f'{correct} est pair ({correct} ÷ 2 = {correct // 2}).',
            }
        else:
            correct     = random.choice(ODDS)
            distractors = _near_evens(correct, 4)
            tagged_candidates = [
                (
                    d,
                    'parity_confusion',
                    "Check the last digit — even numbers end in 0,2,4,6,8.",
                    "Vérifie le dernier chiffre — les nombres pairs se terminent par 0,2,4,6,8.",
                )
                for d in distractors
            ]
            choices     = _tagged_shuffle_mc(str(correct), tagged_candidates)
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       'Which of these is an odd number?',
                'prompt_fr':       'Lequel de ces nombres est impair ?',
                'hint_en':         'Odd numbers leave remainder 1 when divided by 2.',
                'hint_fr':         'Les nombres impairs donnent un reste de 1 quand divisés par 2.',
                'shape_data':      [],
                'choices':         choices,
                'correct_answers': [str(correct)],
                'time_limit':      15,
                'points':          1,
                'explanation_en':  f'{correct} is odd ({correct} ÷ 2 = {correct // 2} remainder 1).',
                'explanation_fr':  f'{correct} est impair ({correct} ÷ 2 = {correct // 2} reste 1).',
            }

    else:  # hard — cross-property questions
        # 25% chance: mix_match — match numbers → Even or Odd (larger numbers)
        if random.random() < 0.25:
            chosen_evens = random.sample([e for e in EVENS if e > 100], 2)
            chosen_odds  = random.sample([o for o in ODDS  if o > 100], 2)
            pairs = (
                [{'left': str(e), 'right': 'Even'} for e in chosen_evens] +
                [{'left': str(o), 'right': 'Odd'}  for o in chosen_odds]
            )
            random.shuffle(pairs)
            explanation_en = 'Correct pairs:\n' + '\n'.join(
                f'{p["left"]} → {p["right"]}' for p in pairs
            )
            explanation_fr = 'Paires correctes :\n' + '\n'.join(
                f'{p["left"]} → {p["right"]}' for p in pairs
            )
            return {
                'q_type':          'mix_match',
                'prompt_en':       'Match each number to Even or Odd.',
                'prompt_fr':       'Associez chaque nombre à Pair ou Impair.',
                'hint_en':         'Check the last digit to determine parity.',
                'hint_fr':         'Regardez le dernier chiffre pour déterminer la parité.',
                'shape_data':      [],
                'pairs':           pairs,
                'correct_answers': [],
                'time_limit':      25,
                'points':          3,
                'explanation_en':  explanation_en,
                'explanation_fr':  explanation_fr,
            }

        subtype = random.choice(['even_square', 'only_even_prime',
                                 'odd_and_prime', 'divisible_4'])

        if subtype == 'even_square':
            correct     = random.choice(EVEN_SQUARES)
            distractors = random.sample([str(n) for n in EVENS
                                         if n not in SQUARES_SET][:30], 4)
            tagged_candidates = [
                (
                    d,
                    'not_square',
                    "That number is not a perfect square — try multiplying a whole number by itself.",
                    "Ce nombre n'est pas un carré parfait — essaie de multiplier un entier par lui-même.",
                )
                for d in distractors
            ]
            choices     = _tagged_shuffle_mc(str(correct), tagged_candidates)
            root        = int(correct ** 0.5)
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       'Which of these is both EVEN and a perfect square?',
                'prompt_fr':       'Lequel est à la fois PAIR et un carré parfait ?',
                'hint_en':         'Even perfect squares: 4, 16, 36, 64, 100, 144, 196.',
                'hint_fr':         'Carrés parfaits pairs : 4, 16, 36, 64, 100, 144, 196.',
                'shape_data':      [],
                'choices':         choices,
                'correct_answers': [str(correct)],
                'time_limit':      25,
                'points':          3,
                'explanation_en':  f'{correct} = {root}² and is even.',
                'explanation_fr':  f'{correct} = {root}² et est pair.',
            }

        elif subtype == 'only_even_prime':
            # 2 is the only even prime — a classic "gotcha"
            distractors = random.sample([str(n) for n in EVENS
                                         if n not in PRIMES_SET and n > 2][:20], 4)
            tagged_candidates = [
                (
                    d,
                    'not_prime',
                    "That number is composite — check if it's divisible by a small prime.",
                    "Ce nombre est composé — vérifie s'il est divisible par un petit nombre premier.",
                )
                for d in distractors
            ]
            choices     = _tagged_shuffle_mc('2', tagged_candidates)
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       'Which of these is both EVEN and PRIME?',
                'prompt_fr':       'Lequel est à la fois PAIR et PREMIER ?',
                'hint_en':         'There is only one even prime number.',
                'hint_fr':         'Il n\'existe qu\'un seul nombre premier pair.',
                'shape_data':      [],
                'choices':         choices,
                'correct_answers': ['2'],
                'time_limit':      25,
                'points':          3,
                'explanation_en':  '2 is the only even prime — every other even number is divisible by 2, so composite.',
                'explanation_fr':  '2 est le seul premier pair — tout autre nombre pair est divisible par 2, donc composé.',
            }

        elif subtype == 'odd_and_prime':
            correct     = random.choice([p for p in ODD_PRIMES if p < 100])
            odd_compos  = [n for n in ODDS if n > 1 and n not in PRIMES_SET]
            distractors = random.sample([str(n) for n in odd_compos[:30]], 4)
            tagged_candidates = [
                (
                    d,
                    'not_prime',
                    "That number is composite — check if it's divisible by a small prime.",
                    "Ce nombre est composé — vérifie s'il est divisible par un petit nombre premier.",
                )
                for d in distractors
            ]
            choices     = _tagged_shuffle_mc(str(correct), tagged_candidates)
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       'Which of these odd numbers is also PRIME?',
                'prompt_fr':       'Lequel de ces nombres impairs est aussi PREMIER ?',
                'hint_en':         'Not all odd numbers are prime (e.g. 9 = 3 × 3 is odd but composite).',
                'hint_fr':         'Tous les impairs ne sont pas premiers (ex: 9 = 3 × 3 est impair mais composé).',
                'shape_data':      [],
                'choices':         choices,
                'correct_answers': [str(correct)],
                'time_limit':      30,
                'points':          3,
                'explanation_en':  f'{correct} is an odd prime — its only factors are 1 and {correct}.',
                'explanation_fr':  f'{correct} est un premier impair — ses seuls diviseurs sont 1 et {correct}.',
            }

        else:  # divisible_4
            div4        = list(range(4, LIMIT + 1, 4))
            correct     = random.choice(div4)
            even_not4   = [n for n in EVENS if n % 4 != 0]
            distractors = random.sample([str(n) for n in even_not4[:30]], 4)
            tagged_candidates = [
                (
                    d,
                    'parity_confusion',
                    "Check the last digit — even numbers end in 0,2,4,6,8.",
                    "Vérifie le dernier chiffre — les nombres pairs se terminent par 0,2,4,6,8.",
                )
                for d in distractors
            ]
            choices     = _tagged_shuffle_mc(str(correct), tagged_candidates)
            return {
                'q_type':          'multiple_choice',
                'prompt_en':       'Which of these is divisible by 4?',
                'prompt_fr':       'Lequel de ces nombres est divisible par 4 ?',
                'hint_en':         'Check the last two digits — they must form a multiple of 4.',
                'hint_fr':         'Regardez les deux derniers chiffres — ils doivent former un multiple de 4.',
                'shape_data':      [],
                'choices':         choices,
                'correct_answers': [str(correct)],
                'time_limit':      20,
                'points':          2,
                'explanation_en':  f'{correct} ÷ 4 = {correct // 4} exactly.',
                'explanation_fr':  f'{correct} ÷ 4 = {correct // 4} exactement.',
            }
