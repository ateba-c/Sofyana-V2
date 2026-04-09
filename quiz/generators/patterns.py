"""
patterns.py — Grade-3 patterns & fact-family generators (content2.md Thème 4 §18, §25).

Topics:
  number_sequence_gen   typed_input – find the next term in an arithmetic sequence
  fact_family_gen       ordering    – complete a multiplication/division fact family

Difficulty (number_sequence_gen):
  easy   → start 10-100, step in {5, 10}
  medium → start 10-500, step in {5, 10, 25, 50}
  hard   → start 10-5000, step in {5, 10, 25, 50, 100, 250}; some decreasing sequences

Difficulty (fact_family_gen):
  easy   → factors 2-5
  medium → factors 2-9 (standard times table)
  hard   → factors 6-12; student sees fewer facts (only 2 of the 4 shown)
"""
import random
from .base import _tagged_shuffle_mc

# ─────────────────────────────────────────────────────────────────────────────
# number_sequence_gen
# ─────────────────────────────────────────────────────────────────────────────

def number_sequence_gen(level='easy'):
    if level == 'easy':
        start   = random.randint(1, 20) * 5
        step    = random.choice([5, 10])
        n_shown = 4
        ascending = True
    elif level == 'medium':
        start     = random.randint(1, 50) * 10
        step      = random.choice([5, 10, 25, 50])
        n_shown   = 4
        ascending = True
    else:
        start     = random.randint(1, 200) * 25
        step      = random.choice([10, 25, 50, 100, 250])
        n_shown   = 4
        ascending = random.choice([True, False])

    terms = []
    for i in range(n_shown + 1):
        if ascending:
            terms.append(start + i * step)
        else:
            terms.append(start - i * step)

    shown   = terms[:n_shown]
    answer  = terms[n_shown]

    direction = "augmente" if ascending else "diminue"
    direction_en = "increases" if ascending else "decreases"

    seq_str = ", ".join(str(t) for t in shown) + ", ..."

    return {
        'q_type':          'text_input',
        'prompt_fr':       f"La suite {seq_str} — quel est le prochain nombre ?",
        'prompt_en':       f"The sequence {seq_str} — what is the next number?",
        'hint_fr':         f"La suite {direction} de {step} à chaque fois.",
        'hint_en':         f"The sequence {direction_en} by {step} each time.",
        'show_illustration': False,
        'shape_data':      [],
        'choices':         [],
        'pairs':           [],
        'explanation_en': (
            f'Step 1: Find the common difference by subtracting two consecutive terms.\n'
            f'Step 2: The sequence {"increases" if ascending else "decreases"} by {step} each time.\n'
            f'Step 3: Apply to the last shown term: {shown[-1]} {"+" if ascending else "-"} {step} = {answer}.\n'
            f'Answer: {answer}'
        ),
        'explanation_fr': (
            f'Étape 1 : Trouve la raison en soustrayant deux termes consécutifs.\n'
            f'Étape 2 : La suite {"augmente" if ascending else "diminue"} de {step} à chaque fois.\n'
            f'Étape 3 : Applique au dernier terme affiché : {shown[-1]} {"+" if ascending else "-"} {step} = {answer}.\n'
            f'Réponse : {answer}'
        ),
        'correct_answers': [str(answer)],
    }


# ─────────────────────────────────────────────────────────────────────────────
# fact_family_gen
# ─────────────────────────────────────────────────────────────────────────────

def fact_family_gen(level='easy'):
    if level == 'easy':
        a = random.randint(2, 5)
        b = random.randint(2, 5)
    elif level == 'medium':
        a = random.randint(2, 9)
        b = random.randint(2, 9)
    else:
        a = random.randint(6, 12)
        b = random.randint(6, 12)

    prod = a * b

    # The 4 related facts
    all_facts = [
        f"{a} × {b} = {prod}",
        f"{b} × {a} = {prod}",
        f"{prod} ÷ {a} = {b}",
        f"{prod} ÷ {b} = {a}",
    ]

    # For hard level, hide one; for easy/medium, show 3 and ask for the 4th
    n_shown = 2 if level == 'hard' else 3
    random.shuffle(all_facts)
    hidden_fact = all_facts[0]
    shown_facts = all_facts[1:]

    shown_str = "  |  ".join(shown_facts[:n_shown])

    # Parse the answer from the hidden fact (number after '=')
    answer_str = hidden_fact.split('=')[1].strip()

    # Distractors: nearby numbers
    distractors = [
        str(prod + 1), str(prod - 1),
        str(a + b), str(a * b + a),
    ]
    distractors = [d for d in distractors if d != answer_str]

    tagged_candidates = [
        (d, 'wrong_fact',
         "Check the relationship between multiplication and division.",
         "Vérifie le lien entre la multiplication et la division.")
        for d in distractors[:4]
    ]

    # Present the hidden fact with a blank
    blank_fact = hidden_fact.split('=')[0] + "= ___"

    return {
        'q_type':          'multiple_choice',
        'prompt_fr':       f"Famille de calculs : {shown_str}\nComplète : {blank_fact}",
        'prompt_en':       f"Fact family: {shown_str}\nComplete: {blank_fact}",
        'hint_fr':         "La multiplication et la division sont des opérations inverses.",
        'hint_en':         "Multiplication and division are inverse operations.",
        'show_illustration': False,
        'shape_data':      [],
        'choices':         _tagged_shuffle_mc(answer_str, tagged_candidates),
        'pairs':           [],
        'explanation_en': (
            f'Step 1: A fact family uses the same three numbers: {a}, {b}, and {prod}.\n'
            f'Step 2: The four related facts are: {a}×{b}={prod}, {b}×{a}={prod}, {prod}÷{a}={b}, {prod}÷{b}={a}.\n'
            f'Step 3: The missing fact is: {hidden_fact}.\n'
            f'Answer: {answer_str}'
        ),
        'explanation_fr': (
            f'Étape 1 : Une famille de calculs utilise les mêmes trois nombres : {a}, {b} et {prod}.\n'
            f'Étape 2 : Les quatre calculs sont : {a}×{b}={prod}, {b}×{a}={prod}, {prod}÷{a}={b}, {prod}÷{b}={a}.\n'
            f'Étape 3 : Le calcul manquant est : {hidden_fact}.\n'
            f'Réponse : {answer_str}'
        ),
        'correct_answers': [answer_str],
    }
