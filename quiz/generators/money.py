"""
money.py — Grade-3 money generators.

Topics (content.md Thème 2, section 14):
  money_change_gen        QCM       – calculate change after a purchase
  money_composition_gen   mix_match – match amount to coin/bill combination

All amounts use at most 2 decimal places (cents).
Amounts stay ≤ 20 $ to remain grade-3 appropriate.

Difficulty:
  easy   → whole-dollar amounts, small prices
  medium → amounts with cents, moderate prices
  hard   → cent-heavy amounts, multiple steps
"""

import random
from .base import _tagged_shuffle_mc


def _fmt_money(amount_cents: int) -> str:
    """Return amount in '3,50 $' format (French convention)."""
    dollars = amount_cents // 100
    cents   = amount_cents % 100
    if cents:
        return f'{dollars},{cents:02d} $'
    return f'{dollars} $'


def _fmt_money_en(amount_cents: int) -> str:
    """Return amount in '$3.50' format."""
    dollars = amount_cents // 100
    cents   = amount_cents % 100
    if cents:
        return f'${dollars}.{cents:02d}'
    return f'${dollars}'


# ─── Coin/bill combinations ────────────────────────────────────────────────────

_DENOMINATIONS = [1, 5, 10, 25, 100, 200, 500, 1000, 2000]  # cents
_DENOM_NAMES_FR = {1: '1¢', 5: '5¢', 10: '10¢', 25: '25¢',
                   100: '1 $', 200: '2 $', 500: '5 $',
                   1000: '10 $', 2000: '20 $'}
_DENOM_NAMES_EN = {1: '1¢', 5: '5¢', 10: '10¢', 25: '25¢',
                   100: '$1', 200: '$2', 500: '$5',
                   1000: '$10', 2000: '$20'}


def _make_combination(amount_cents: int) -> str:
    """Greedy coin decomposition of amount in French labels."""
    remaining = amount_cents
    parts = []
    for denom in sorted(_DENOMINATIONS, reverse=True):
        count = remaining // denom
        if count:
            lbl = _DENOM_NAMES_FR[denom]
            parts.append(f'{count}×{lbl}')
            remaining -= count * denom
    return ' + '.join(parts) if parts else '0¢'


# ─── 1. money_change_gen ──────────────────────────────────────────────────────

def money_change_gen(level: str = 'medium') -> dict:
    """
    QCM — item costs {price}, student pays {paid}, what is the change?
    All amounts in cents internally.
    """
    if level == 'easy':
        # Whole dollars only
        price_cents = random.choice([100, 200, 300, 500]) * random.randint(1, 4)
        paid_cents  = random.choice([500, 1000, 2000])
        while paid_cents < price_cents:
            paid_cents = random.choice([500, 1000, 2000])
    elif level == 'medium':
        # Prices with 25¢ increments
        price_cents = random.randint(1, 19) * 100 + random.choice([0, 25, 50, 75])
        paid_cents  = random.choice([500, 1000, 2000])
        while paid_cents < price_cents:
            paid_cents = random.choice([1000, 2000])
    else:
        # Arbitrary cent amounts
        price_cents = random.randint(50, 1999)
        paid_cents  = random.choice([500, 1000, 2000])
        while paid_cents < price_cents:
            paid_cents = random.choice([1000, 2000])

    change_cents = paid_cents - price_cents
    price_str    = _fmt_money(price_cents)
    paid_str     = _fmt_money(paid_cents)
    change_str   = _fmt_money(change_cents)
    price_en     = _fmt_money_en(price_cents)
    paid_en      = _fmt_money_en(paid_cents)
    change_en    = _fmt_money_en(change_cents)

    wrong1 = _fmt_money(paid_cents + price_cents)   # add instead of subtract
    wrong2 = _fmt_money(price_cents - (price_cents % 100) if price_cents % 100 else price_cents)
    wrong3 = _fmt_money(change_cents + 25 if change_cents + 25 <= paid_cents else max(0, change_cents - 25))
    wrong4 = _fmt_money(price_cents)                # gave the price back

    choices = _tagged_shuffle_mc(change_str, [
        (wrong1,
         'wrong_operation',
         'To find change, subtract the price from what was paid.',
         'Pour la monnaie, soustrais le prix de la somme payée.'),
        (wrong3,
         'off_by_cents',
         'Close! Check your cents carefully.',
         'Presque ! Vérifie bien les centimes.'),
        (wrong4,
         'gave_back_price',
         'You gave the price, not the change.',
         'Tu as donné le prix, pas la monnaie.'),
        (price_str,
         'confusion',
         'The change is what remains after paying.',
         'La monnaie est ce qu\'il reste après avoir payé.'),
    ])

    return {
        'q_type': 'multiple_choice',
        'prompt_fr': (
            f'Un objet coûte **{price_str}**. '
            f'Tu paies avec **{paid_str}**. '
            f'Quelle monnaie reçois-tu ?'
        ),
        'prompt_en': (
            f'An item costs **{price_en}**. '
            f'You pay with **{paid_en}**. '
            f'What change do you receive?'
        ),
        'hint_fr': 'Monnaie = somme payée − prix de l\'objet.',
        'hint_en': 'Change = amount paid − item price.',
        'shape_data': [],
        'choices': choices,
        'correct_answers': [change_str, change_en],
        'time_limit': 35,
        'points': 1,
        'explanation_fr': (
            f'Monnaie = {paid_str} − {price_str} = **{change_str}**'
        ),
        'explanation_en': (
            f'Change = {paid_en} − {price_en} = **{change_en}**'
        ),
    }


# ─── 2. money_composition_gen ─────────────────────────────────────────────────

def money_composition_gen(level: str = 'medium') -> dict:
    """
    Mix & match — match each amount to its coin/bill combination.
    3-4 pairs.
    """
    count = 3 if level == 'easy' else 4

    if level == 'easy':
        # Whole dollars, simple denominations
        pool_cents = [c * 100 for c in random.sample(range(1, 11), count)]
    elif level == 'medium':
        pool_cents = [random.randint(1, 10) * 100 + random.choice([0, 25, 50])
                      for _ in range(count + 5)]
        # Deduplicate
        seen = set()
        pool_cents = [x for x in pool_cents if x not in seen and not seen.add(x)][:count]
    else:
        pool_cents = [random.randint(50, 2000) for _ in range(count + 5)]
        seen = set()
        pool_cents = [x for x in pool_cents if x not in seen and not seen.add(x)][:count]

    pairs = []
    for cents in pool_cents[:count]:
        left  = _fmt_money(cents)
        right = _make_combination(cents)
        pairs.append({'left': left, 'right': right})

    return {
        'q_type': 'mix_match',
        'prompt_fr': 'Associe chaque montant à la bonne combinaison de pièces ou billets.',
        'prompt_en': 'Match each amount to the correct coin/bill combination.',
        'hint_fr': 'Additionne chaque pièce ou billet pour vérifier le total.',
        'hint_en': 'Add up each coin or bill to check the total.',
        'shape_data': [],
        'choices': [],
        'pairs': pairs,
        'correct_answers': [p['right'] for p in pairs],
        'time_limit': 45,
        'points': count,
        'explanation_fr': '\n'.join(f'{p["left"]} → {p["right"]}' for p in pairs),
        'explanation_en': '\n'.join(f'{p["left"]} → {p["right"]}' for p in pairs),
    }
