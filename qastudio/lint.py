"""
Automated pre-review linting (spec §8, plus Sofyana-specific rules).

``lint_payload(payload, slug)`` renders the raw generator output in French and
English and runs every rule on both.  Each finding:

    {'rule': 'LINT-02', 'criterion': 'clarity', 'severity': 'error'|'warn',
     'lang': 'fr'|'en'|'', 'message': '…'}

``error`` findings auto-flag the sample for rework; ``warn`` findings are shown
to the reviewer but don't block it.  Each rule maps to one of the six rubric
criteria so the Studio can pre-fill the checklist.
"""
import re
from difflib import SequenceMatcher

from quiz.answers import check_answer

from .sampling import render_question

ERROR, WARN = 'error', 'warn'

RULES = {
    'LINT-01': ('rendering',    'Raw delimiter / markup leak'),
    'LINT-02': ('clarity',      'Repeated sentence or data'),
    'LINT-03': ('accuracy',     'Options: count, uniqueness, answer key'),
    'LINT-04': ('hint_quality', 'Hint missing, too short or gives the answer'),
    'LINT-05': ('structure',    'Data dumped inline instead of a table / list'),
    'LINT-06': ('rendering',    'French typography'),
    'LINT-07': ('clarity',      'Wrong language in the text'),
    'LINT-08': ('clarity',      'Explanation does not show the work'),
    'LINT-09': ('clarity',      'Prompt too long (cognitive load)'),
    'LINT-10': ('clarity',      'Grammar: plural / article / elision'),
    'LINT-11': ('clarity',      'Duplicated word'),
    'LINT-12': ('accuracy',     'Primary rules: no negatives, no square roots'),
    'LINT-13': ('ambiguity',    'Several choices are correct, or an answer is not accepted'),
}


def _f(rule, severity, message, lang=''):
    return {'rule': rule, 'criterion': RULES[rule][0], 'severity': severity, 'lang': lang, 'message': message}


def _plain(text):
    return re.sub(r'\*\*(.+?)\*\*', r'\1', str(text or ''))


def _texts(q, lang):
    """(where, text) for everything the child reads."""
    out = [('prompt', _plain(q.get(f'prompt_{lang}'))),
           ('hint', _plain(q.get(f'hint_{lang}')))]
    out += [('choice', str(c.get('label', ''))) for c in q.get('choices') or []]
    out += [('item', str(i.get('label', ''))) for i in q.get('items') or []]
    for p in q.get('pairs') or []:
        out += [('pair', str(p.get('left', ''))), ('pair', str(p.get('right', '')))]
    t = q.get('table') or {}
    out += [('table', str(c)) for c in t.get('headers') or []]
    out += [('table', str(c)) for row in t.get('rows') or [] for c in row]
    return out


# ── individual rules ──────────────────────────────────────────────────────────

_LEAKS = [
    (re.compile(r'\|'), 'raw pipe “|” (use a table)'),
    (re.compile(r'\t'), 'tab character'),
    (re.compile(r'\\n|\\t|\\frac|\\times'), 'escaped / LaTeX sequence'),
    (re.compile(r'[{}]'), 'curly brace (template placeholder?)'),
    (re.compile(r'^\s*(None|nan|NaN|undefined|null)\s*$|\bNone\b(?!\s+of)|\bundefined\b|\[object'),
     'programming value shown to the child'),
    (re.compile(r'</?[a-zA-Z][a-zA-Z0-9]*(\s[^<>]*)?/?>'), 'HTML tag'),
    (re.compile(r'&(lt|gt|amp|nbsp|quot);'), 'HTML entity'),
]


def rule_leaks(q, lang):
    found = []
    for where, text in _texts(q, lang):
        for pat, what in _LEAKS:
            if pat.search(text):
                found.append(_f('LINT-01', ERROR, f'{where}: {what} — « {text[:80]} »', lang))
                break
    raw_prompt = str(q.get(f'prompt_{lang}') or '')
    if raw_prompt.count('**') % 2:
        found.append(_f('LINT-01', ERROR, 'prompt: unbalanced ** bold marker', lang))
    if not _plain(raw_prompt).strip():
        found.append(_f('LINT-01', ERROR, 'prompt is empty', lang))
    return found


_SENT = re.compile(r'(?<=[.?!])\s+(?=[A-ZÀ-Ý«“"(])')
_DATA_PAIR = re.compile(r'([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\' ]{1,24}?)\s*[:=]\s*(\d+(?:[.,]\d+)?)')
_NUMS = re.compile(r'\d+(?:[.,  ]\d+)*')


def _tokens(s):
    return set(re.findall(r'[\wÀ-ÿ]+', s.lower()))


def rule_repetition(q, lang):
    prompt = _plain(q.get(f'prompt_{lang}'))
    sentences = [s.strip() for s in _SENT.split(prompt) if len(_tokens(s)) >= 4]
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            a, b = sentences[i], sentences[j]
            ta, tb = _tokens(a), _tokens(b)
            jac = len(ta & tb) / len(ta | tb)
            # parallel sentences with different numbers (« Groupe A : 4… / Groupe B : 5… ») are fine
            if _NUMS.findall(a) != _NUMS.findall(b):
                continue
            if jac > 0.85 or SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.85:
                return [_f('LINT-02', ERROR, f'two sentences say the same thing: « {a[:60]} » / « {b[:60]} »', lang)]
    pairs = [(m.group(1).strip().split()[-1].lower(), m.group(2)) for m in _DATA_PAIR.finditer(prompt)]
    seen = set()
    for p in pairs:
        if p in seen:
            return [_f('LINT-02', ERROR, f'the same data is written twice (« {p[0]} : {p[1]} »)', lang)]
        seen.add(p)
    return []


def _is_num(s):
    return bool(re.fullmatch(r'[\d\s  ,.]+', s.strip())) and any(ch.isdigit() for ch in s)


def _is_numlike(s):
    """Numbers, fractions, powers, short expressions with a unit — anything that isn't a word answer."""
    s = re.sub(r'\b(plus|moins|minus|positi(?:ve|f)|n[eé]gati(?:ve|f))\b', '', s.strip(), flags=re.I)   # "moins 38" is a number read aloud
    return any(ch.isdigit() for ch in s) and len(re.sub(r'[\d\s  ,./²³⁴⁰¹×+−=()$%°]', '', s)) <= 4


def _padding(choices):
    """Filler choices added by _tagged_shuffle_mc when a generator ran out of distractors (answer + 37k)."""
    correct = next((str(c.get('label', '')) for c in choices if c.get('correct')), '')
    try:
        base = abs(int(float(correct.split('/')[0].replace(',', '.'))))
    except ValueError:
        return []
    out = []
    for c in choices:
        lab = str(c.get('label', '')).strip()
        if c.get('error_type') == 'distractor' and lab.isdigit() and int(lab) > base and (int(lab) - base) % 37 == 0:
            out.append(lab)
    return out


def rule_options(q, lang):
    found = []
    qt = q.get('q_type')
    if qt == 'multiple_choice':
        choices = q.get('choices') or []
        labels = [str(c.get('label', '')).strip() for c in choices]
        if not 2 <= len(choices) <= 5:
            found.append(_f('LINT-03', ERROR, f'{len(choices)} choices (expected 2–5)', lang))
        if any(not l for l in labels):
            found.append(_f('LINT-03', ERROR, 'empty choice label', lang))
        if len({l.lower() for l in labels}) != len(labels):
            found.append(_f('LINT-03', ERROR, f'two identical choices: {labels}', lang))
        n_correct = sum(1 for c in choices if c.get('correct'))
        if n_correct != 1:
            found.append(_f('LINT-03', ERROR, f'{n_correct} choices marked correct (expected exactly 1)', lang))
        nums = [l for l in labels if _is_numlike(l)]
        if nums and len(labels) - len(nums) >= 2:
            found.append(_f('LINT-03', WARN, f'numbers mixed with word choices: {labels}', lang))
        pad = _padding(choices)
        if pad:
            found.append(_f('LINT-03', WARN, f'filler choice(s) {pad} — the generator ran out of plausible distractors: {labels}', lang))
    elif qt == 'text_input':
        answers = [str(a) for a in q.get('correct_answers') or []]
        if not answers:
            found.append(_f('LINT-03', ERROR, 'no accepted answer', lang))
        elif not check_answer(answers[0], answers, q.get('answer_type')):
            found.append(_f('LINT-13', ERROR, f'the answer key « {answers[0]} » is refused by the answer checker', lang))
    elif qt in ('build_bars', 'place_point'):
        from quiz.widgets import check as _widget_check
        answers = [str(a) for a in q.get('correct_answers') or []]
        if not answers or not _widget_check(q, answers[0]):
            found.append(_f('LINT-13', ERROR, f'the widget answer key « {answers[:1]} » is refused by its own checker', lang))
    elif qt in ('ordering', 'sorting'):
        labels = [str(i.get('label', '')) for i in q.get('items') or []]
        if len(labels) < 2 or len(set(labels)) != len(labels):
            found.append(_f('LINT-03', ERROR, f'ordering items missing or duplicated: {labels}', lang))
    elif qt == 'mix_match':
        pairs = q.get('pairs') or []
        lefts, rights = [p.get('left') for p in pairs], [p.get('right') for p in pairs]
        if len(pairs) < 2 or len(set(lefts)) != len(lefts):
            found.append(_f('LINT-03', ERROR, 'matching: fewer than 2 pairs or duplicated left side', lang))
        # sorting into a few categories (Pair / Impair) legitimately reuses answers;
        # a duplicate among otherwise distinct answers means two items can't be told apart
        if len(set(rights)) != len(rights) and len(set(rights)) > len(rights) / 2:
            found.append(_f('LINT-13', ERROR, f'matching: two left items share the same answer {rights}', lang))
    return found


def _answer_text(q):
    if q.get('q_type') == 'multiple_choice':
        for c in q.get('choices') or []:
            if c.get('correct'):
                return str(c.get('label', ''))
    answers = q.get('correct_answers') or []
    return str(answers[0]) if answers else ''


def rule_hint(q, lang):
    hint = _plain(q.get(f'hint_{lang}')).strip()
    if len(hint) < 10:
        return [_f('LINT-04', WARN, 'hint missing or shorter than 10 characters', lang)]
    # numeric answers only: vocabulary hints naturally contain the word being taught
    ans = _answer_text(q).strip()
    if ans and _is_numlike(ans) and len(re.sub(r'\D', '', ans)) >= 2:
        if re.search(r'(?<![\wÀ-ÿ])' + re.escape(ans) + r'(?![\wÀ-ÿ])', hint, re.IGNORECASE):
            return [_f('LINT-04', WARN, f'hint contains the answer « {ans} »', lang)]
    return []


def rule_inline_data(q, lang):
    if q.get('table') or q.get('shape_data'):
        return []
    prompt = _plain(q.get(f'prompt_{lang}'))
    pairs = _DATA_PAIR.findall(prompt)
    if len(pairs) >= 3:
        return [_f('LINT-05', WARN, f'{len(pairs)} “label: value” pairs written inline — show them as a table or list', lang)]
    return []


_FR_PUNCT = re.compile(r'(?<=[^\s\d  /=(_×+÷-])([:;?!])(?=\s|$)|(?<=\d)([;!])(?=\s|$)')


def rule_fr_typography(q, lang):
    if lang != 'fr':
        return []
    for where, text in _texts(q, 'fr'):
        if where in ('prompt', 'hint'):
            m = _FR_PUNCT.search(text)
            if m:
                ctx = text[max(0, m.start() - 15):m.end() + 5]
                return [_f('LINT-06', WARN, f'{where}: missing space before « {m.group(0)} » — « …{ctx}… »', lang)]
    return []


_FR_WORDS = re.compile(r"\b(le|la|les|des|du|une|est|sont|combien|quel|quelle|avec|pour|dans|élèves|chaque|qui)\b", re.I)
_EN_WORDS = re.compile(r"\b(the|and|how|many|which|what|is|are|of|with|each|students)\b", re.I)


def rule_language(q, lang):
    found = []
    for where, text in _texts(q, lang):
        if where in ('prompt', 'hint', 'choice'):
            words = set(w.lower() for w in (_FR_WORDS if lang == 'en' else _EN_WORDS).findall(text))
            if len(words) >= 2:
                other = 'French' if lang == 'en' else 'English'
                found.append(_f('LINT-07', ERROR, f'{where}: {other} words in the {lang.upper()} version ({", ".join(sorted(words))}) — « {text[:70]} »', lang))
                break
    # explanations are built separately and often keep English answer words (« 35 → Odd »)
    expl = str(q.get(f'explanation_{lang}') or '')
    m = (_EN_SCHOOL if lang == 'fr' else _FR_SCHOOL).search(expl)
    if m:
        found.append(_f('LINT-07', WARN, f'explanation: « {m.group(0)} » in the {lang.upper()} version — « {expl[:70]} »', lang))
    return found


_EN_SCHOOL = re.compile(r'\b(Odd|Even|Prime|Composite|Step|Answer|Yes|No|True|False|times)\b')
_FR_SCHOOL = re.compile(r'\b(Impair|Pair|Premier|Composé|Étape|Réponse|Oui|Non|Vrai|Faux|fois)\b')


_GENERIC_EXPL = ['type de question', "applique l'opération correcte", 'identify the question type',
                 'apply the correct operation']


def rule_explanation(q, lang):
    expl = str(q.get(f'explanation_{lang}') or '').strip()
    if not expl:
        return [_f('LINT-08', WARN, 'no explanation', lang)]
    low = expl.lower()
    if any(g in low for g in _GENERIC_EXPL):
        return [_f('LINT-08', WARN, 'generic explanation (does not solve this problem)', lang)]
    ans = _answer_text(q)
    if _is_num(ans) and not re.search(r'\d', expl):
        return [_f('LINT-08', WARN, 'numeric answer but the explanation shows no calculation', lang)]
    return []


def rule_length(q, lang):
    prompt = _plain(q.get(f'prompt_{lang}'))
    n_sent = len([s for s in _SENT.split(prompt) if s.strip()])
    if len(prompt) > 450:
        return [_f('LINT-09', ERROR, f'prompt is {len(prompt)} characters', lang)]
    if len(prompt) > 260 or n_sent > 4:
        return [_f('LINT-09', WARN, f'prompt is {len(prompt)} characters / {n_sent} sentences', lang)]
    return []


_EN_ONE_PLURAL = re.compile(r'\b1 (?!\w*ss\b)([a-z]+s)\b')
_EN_A_VOWEL = re.compile(r'(?:^|(?<=[\s(]))a (?!one|once|uni|use|usu|eu|ur)([aeio]\w+)')
_FR_DE_LE = re.compile(r'\b(de|à) (le|les)\b', re.I)
_FR_ELISION = re.compile(r"\b(le|la|de|que|je|ne|se|me|te)\s+([aeiouéèêàâîôû]\w*)")
_FR_ONE_PLURAL = re.compile(r'\b1 ([a-zà-ÿ]+s)\b')
_FR_SINGULAR_S = {'fois', 'mois', 'pas', 'bus', 'cas', 'prix', 'bras', 'corps', 'souris', 'temps', 'poids', 'jus',
                  'repas', 'colis', 'tapis', 'avis', 'dos', 'os', 'nez', 'gaz', 'pois', 'ours', 'fils', 'cours', 'bois'}
_EN_SINGULAR_S = {'bus', 'gas', 'plus', 'is', 'was', 'has', 'this', 'its', 'minus', 'class', 'glass', 'grass'}


def rule_grammar(q, lang):
    for where, text in _texts(q, lang):
        if where not in ('prompt', 'hint', 'choice'):
            continue
        if lang == 'en':
            m = _EN_ONE_PLURAL.search(text)
            if m and m.group(1) not in _EN_SINGULAR_S:
                return [_f('LINT-10', WARN, f'{where}: « {m.group(0)} » (singular after 1)', lang)]
            m = _EN_A_VOWEL.search(text)
            if m:
                return [_f('LINT-10', WARN, f'{where}: « {m.group(0)} » (an before a vowel)', lang)]
        else:
            m = _FR_DE_LE.search(text)
            if m:
                return [_f('LINT-10', WARN, f'{where}: « {m.group(0)} » (du / des / au / aux)', lang)]
            m = _FR_ELISION.search(text)
            if m and m.group(2).lower() not in ('onze', 'un', 'une', 'huit', 'huitième', 'oui', 'y'):
                return [_f('LINT-10', WARN, f"{where}: « {m.group(0)} » (élision : l', d', qu'…)", lang)]
            m = _FR_ONE_PLURAL.search(text)
            if m and m.group(1).lower() not in _FR_SINGULAR_S:
                return [_f('LINT-10', WARN, f'{where}: « {m.group(0)} » (singulier après 1)', lang)]
    return []


_DUP_WORD = re.compile(r'\b([A-Za-zÀ-ÿ]+)\s+\1\b', re.I)


def rule_duplicate_word(q, lang):
    for where, text in _texts(q, lang):
        if where in ('prompt', 'hint'):
            m = _DUP_WORD.search(text)
            if m and m.group(1).lower() not in ('nous', 'vous', 'that', 'had'):
                return [_f('LINT-11', WARN, f'{where}: « {m.group(0)} »', lang)]
    return []


def rule_primary(q, lang, signed=False):
    found = []
    blob = '\n'.join(t for _, t in _texts(q, lang))
    if '√' in blob:
        found.append(_f('LINT-12', ERROR, 'square root shown (not primary)', lang))
    values = [str(a) for a in q.get('correct_answers') or []] + [str(c.get('label', '')) for c in q.get('choices') or []]
    neg = [v for v in values if v.strip().startswith(('-', '−'))]
    if neg and not signed:
        found.append(_f('LINT-12', ERROR, f'negative number in answers/choices: {neg}', lang))
    return found


ALL_RULES = [rule_leaks, rule_repetition, rule_options, rule_hint, rule_inline_data, rule_fr_typography,
             rule_language, rule_explanation, rule_length, rule_grammar, rule_duplicate_word, rule_primary]


def lint_question(q, lang, signed=False):
    """``signed``: the skill is one where negatives are natural (temperatures, integers, 4-quadrant plane)."""
    found = []
    for rule in ALL_RULES:
        found += rule(q, lang, signed) if rule is rule_primary else rule(q, lang)
    return found


def lint_payload(payload, slug):
    from quiz.generators.resolution_plus import SIGNED_SKILLS
    findings = []
    for lang in ('fr', 'en'):
        q = render_question(payload, slug, lang)
        findings += lint_question(q, lang, signed=slug in SIGNED_SKILLS)
    # one finding per (rule, message) — the same structural problem shows in both languages
    out, seen = [], set()
    for f in findings:
        key = (f['rule'], f['message'] if f['lang'] == '' else f['message'] + f['lang'])
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out


def checklist_from_lint(findings):
    """Pre-fill the rubric: a criterion with a lint error starts unchecked; the rest are for the reviewer."""
    failing = {f['criterion'] for f in findings if f['severity'] == ERROR}
    return {k: False for k in failing}
