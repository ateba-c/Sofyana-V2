"""
Reproducible samples of generated questions.

``generate(slug, level, seed)`` seeds the ``random`` module (every generator
draws from it), runs the generator and returns its raw output.  The same seed
gives the same problem as long as the generator code doesn't change, which is
what ``fingerprint`` detects.
"""
import copy
import hashlib
import json
import random
import secrets

from quiz.answers import infer_answer_type, input_spec
from quiz.generators import GENERATORS, generator_for
from quiz.labels import localize_problem
from quiz.taxonomy import answer_type_for

DEFAULT_LEVELS = ['easy', 'medium', 'hard']


def levels_for(skill):
    return list(skill.level_sequence or DEFAULT_LEVELS)


def new_seed():
    return secrets.randbelow(2**31 - 1) + 1


def _jsonable(obj):
    """Tuples → lists etc., exactly as the payload will be stored in the JSONField."""
    return json.loads(json.dumps(obj, ensure_ascii=False, default=str))


def generate(slug, level, seed):
    gen = generator_for(slug, level) or GENERATORS.get(slug)
    if gen is None:
        raise KeyError(f'no generator for {slug}')
    state = random.getstate()
    try:
        random.seed(seed)
        return _jsonable(gen(level))
    finally:
        random.setstate(state)          # don't disturb anyone else's random stream


def fingerprint(payload):
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode('utf-8')).hexdigest()


def render_question(payload, slug, lang):
    """The question dict exactly as practice_next would hand it to the template."""
    q = localize_problem(copy.deepcopy(payload), lang)
    if q.get('q_type') == 'text_input':
        q['answer_type'] = (q.get('answer_type') or answer_type_for(slug)
                            or infer_answer_type(q.get('correct_answers', [])))
        q['input'] = input_spec(q['answer_type'], lang)
    return q


def correct_index(q):
    for i, c in enumerate(q.get('choices') or []):
        if c.get('correct'):
            return i
    return None
