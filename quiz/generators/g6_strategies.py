"""
g6_strategies.py — Grade-6 word-problem reading strategies (content_g6.md §7).

Topics:
  g6_relevant_info_gen        QCM             – which piece of information is useless for the question?
  g6_comparative_phrase_gen   typed (integer) – "X is 7 000 m/h faster than Y" → Y + 7 000 (hard adds a distractor fact)
"""
import random
from .base import _tagged_shuffle_mc
from . import scenarios as sc


def _build(level):
    """A comparative story: two facts + one question, optional distractor fact."""
    c = random.choice(sc.COMPARATIVES)
    (a_fr, a_en), (b_fr, b_en) = random.sample(c['subjects'], 2)
    base = random.randint(c['lo'], c['hi'])
    mode = random.choice(['more', 'less'] if level != 'hard' else ['more', 'less', 'times'])
    if mode == 'times':
        diff = random.randint(2, 4)
        answer = base * diff
        calc = f'{sc.fmt_n(base)} × {diff} = {sc.fmt_n(answer)}'
    else:
        if level == 'easy':
            diff = random.randint(1, 9) * 10 ** (len(str(base)) - 2)
        else:
            diff = random.randint(1, 99) * 10 ** max(0, len(str(base)) - 3)
        if mode == 'more':
            answer = base + diff
            calc = f'{sc.fmt_n(base)} + {sc.fmt_n(diff)} = {sc.fmt_n(answer)}'
        else:
            diff = min(diff, base - 1)
            answer = base - diff
            calc = f'{sc.fmt_n(base)} − {sc.fmt_n(diff)} = {sc.fmt_n(answer)}'
    cap = lambda t: t[0].upper() + t[1:]
    fact1_fr = c['fact_fr'].format(S=cap(a_fr), n=sc.fmt_n(base))
    fact1_en = c['fact_en'].format(S=cap(a_en), n=sc.fmt_n(base))
    fact2_fr = c[mode + '_fr'].format(S=cap(b_fr), T=a_fr, n=sc.fmt_n(diff))
    fact2_en = c[mode + '_en'].format(S=cap(b_en), T=a_en, n=sc.fmt_n(diff))
    q_fr = c['q_fr'].format(S=b_fr)
    q_en = c['q_en'].format(S=b_en)
    d_fr, d_en, dlo, dhi = random.choice(sc.DISTRACTOR_FACTS)
    dn = sc.fmt_n(random.randint(dlo, dhi))
    dist_fr, dist_en = d_fr.format(n=dn), d_en.format(n=dn)
    return dict(fact1_fr=fact1_fr, fact1_en=fact1_en, fact2_fr=fact2_fr, fact2_en=fact2_en,
                q_fr=q_fr, q_en=q_en, dist_fr=dist_fr, dist_en=dist_en, answer=answer, calc=calc,
                unit=c['unit'], attr_fr=c['attr_fr'], attr_en=c['attr_en'])


def g6_relevant_info_gen(level='easy'):
    s = _build(level)
    facts_fr = [s['fact1_fr'], s['fact2_fr'], s['dist_fr']]
    facts_en = [s['fact1_en'], s['fact2_en'], s['dist_en']]
    order = list(range(3))
    random.shuffle(order)
    story_fr = ' '.join(facts_fr[i] for i in order)
    story_en = ' '.join(facts_en[i] for i in order)
    correct = (s['dist_fr'], s['dist_en'])
    tagged = [
        ((s['fact1_fr'], s['fact1_en']), 'needed_fact', 'This gives the starting value you need.', 'Cette donnée donne la valeur de départ nécessaire.'),
        ((s['fact2_fr'], s['fact2_en']), 'needed_fact', 'This gives the comparison you need.', 'Cette donnée donne la comparaison nécessaire.'),
        (('Toutes les informations sont utiles.', 'All the information is useful.'), 'all_useful', 'One fact talks about something else entirely.', "Une donnée parle d'autre chose."),
        (("Aucune information n'est utile.", 'No information is useful.'), 'none_useful', 'Two facts are needed to answer.', 'Deux données sont nécessaires pour répondre.'),
    ]
    return {
        'q_type': 'multiple_choice',
        'prompt_fr': f"{story_fr} **{s['q_fr']}**\n\nQuelle information est **inutile** pour répondre à la question ?",
        'prompt_en': f"{story_en} **{s['q_en']}**\n\nWhich piece of information is **not needed** to answer the question?",
        'hint_fr': 'Relis la question : de quoi parle-t-elle ? Une donnée qui parle d\'autre chose est inutile.',
        'hint_en': 'Reread the question: what is it about? A fact about something else is not needed.',
        'show_illustration': False, 'shape_data': [],
        'choices': _tagged_shuffle_mc(correct, tagged), 'pairs': [],
        'explanation_en': f"The question is about the {s['attr_en']}. Useless: “{s['dist_en']}”. Needed: {s['calc']}.",
        'explanation_fr': f"La question porte sur la {s['attr_fr']}. Inutile : « {s['dist_fr']} ». Nécessaire : {s['calc']}.",
        'correct_answers': [s['dist_fr'], s['dist_en']],
    }


def g6_comparative_phrase_gen(level='easy'):
    s = _build(level)
    facts_fr = [s['fact1_fr'], s['fact2_fr']]
    facts_en = [s['fact1_en'], s['fact2_en']]
    if level == 'hard':
        facts_fr.append(s['dist_fr']); facts_en.append(s['dist_en'])
        random.shuffle(facts_fr)
        order = [facts_fr.index(f) for f in facts_fr]
        facts_en = [[s['fact1_en'], s['fact2_en'], s['dist_en']][[s['fact1_fr'], s['fact2_fr'], s['dist_fr']].index(f)] for f in facts_fr]
    return {
        'q_type': 'text_input', 'answer_type': 'integer',
        'prompt_fr': f"{' '.join(facts_fr)} **{s['q_fr']}**",
        'prompt_en': f"{' '.join(facts_en)} **{s['q_en']}**",
        'hint_fr': "« plus … que » → addition ; « moins … que » → soustraction ; « fois plus » → multiplication. Ignore les données qui ne concernent pas la question.",
        'hint_en': '“more … than” → add; “less … than” → subtract; “times more” → multiply. Ignore facts unrelated to the question.',
        'show_illustration': False, 'shape_data': [], 'choices': [], 'pairs': [],
        'explanation_en': f"Translate the comparison into an operation: {s['calc']} {s['unit']}.",
        'explanation_fr': f"Traduis la comparaison en opération : {s['calc']} {s['unit']}.",
        'correct_answers': [str(s['answer'])],
    }
