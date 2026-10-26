"""
facts.py — per-fact tracking for fact-fluency skills (workplan B4.16, audit QC-087 / 094 / 096).

A *fact* is one basic fact family: 7 × 8, 8 × 7 and 56 ÷ 7 are the same fact "7×8"; 9 + 6, 6 + 9 and 15 − 6
are the same fact "6+9". Every answer on a fact skill records its fact in ``ProblemInteraction.item``. A fact is
*weak* when it was missed and has not been answered correctly twice in a row since. The practice view then serves
weak facts more often (``serve``), and the feedback lists the facts still to review.
"""
import random
import re

FACT_SKILLS = {'g4-times-tables', 'g1-add-facts', 'g1-sub-facts'}
REVIEW_SHARE = 0.5          # share of questions taken from the weak facts when there are some
FIXED_AFTER = 2             # correct answers in a row that clear a missed fact

_FACT_RE = re.compile(r'^\*\*\s*(\d+)\s*([×÷+−-])\s*(\d+)\s*=\s*\?\s*\*\*$')


def fact_key(q):
    """'7×8' / '6+9' for a fact question, '' for anything else."""
    m = _FACT_RE.match((q.get('prompt_fr') or '').strip())
    if not m:
        return ''
    a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
    if op == '×':
        x, y = a, b
    elif op == '÷':
        if not b or a % b:
            return ''
        x, y = b, a // b
    elif op == '+':
        x, y = a, b
    else:                                   # a − b = c  →  the fact b + c
        if b > a:
            return ''
        x, y = b, a - b
    x, y = sorted((x, y))
    return f"{x}{'×' if op in '×÷' else '+'}{y}"


def label(key):
    """Display form: '7×8' → '7 × 8'."""
    return re.sub(r'([×+])', r' \1 ', key)


def weak_facts(user, topic, window=300):
    """Facts of ``topic`` still to review for ``user``, most recently missed first."""
    from .models import ProblemInteraction
    rows = (ProblemInteraction.objects.filter(user=user, topic=topic).exclude(item='')
            .order_by('-created_at').values_list('item', 'is_correct')[:window])
    state = {}                              # item -> (correct answers since the last miss, missed at all)
    order = []
    for item, ok in rows:                   # newest first
        if item in state and state[item][1] is not None:
            continue
        run, _ = state.get(item, (0, None))
        if ok:
            state[item] = (run + 1, None)
        else:
            state[item] = (run, True)       # found the most recent miss
            if run < FIXED_AFTER:
                order.append(item)
    return order


def serve(gen, level, weak, tries=60):
    """A problem from ``gen(level)``; when there are weak facts, about half the time one of them."""
    q = gen(level)
    if not weak or random.random() >= REVIEW_SHARE:
        return q
    wanted = set(weak)
    for _ in range(tries):
        if fact_key(q) in wanted:
            return q
        q = gen(level)
    return q                                 # the weak facts belong to another level: serve a normal question
