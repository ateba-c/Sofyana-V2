import json
import random as _random
from django import forms
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Count, Q
from .models import QuizSet, Question, StudentSession, Student, ProblemInteraction, ParentProfile, ParentAssignment, AVATAR_SLUGS, AVATAR_EMOJIS
from .generators import GENERATORS, TOPIC_GROUPS, SKILL_MAP


# ── Error-type human-readable labels (bilingual) ──────────────────────────────
ERROR_TYPE_LABELS = {
    # Arithmetic
    'off_by_one':           {'en': 'Off by one',               'fr': 'Erreur d\'une unité'},
    'off_by_ten':           {'en': 'Off by ten',               'fr': 'Erreur d\'une dizaine'},
    'place_value':          {'en': 'Place value error',        'fr': 'Erreur de valeur de position'},
    'wrong_operation':      {'en': 'Wrong operation',          'fr': 'Mauvaise opération'},
    'partial_product':      {'en': 'Partial product error',    'fr': 'Erreur de produit partiel'},
    'factor_error':         {'en': 'Factor error',             'fr': 'Erreur de facteur'},
    'quotient_error':       {'en': 'Quotient error',           'fr': 'Erreur de quotient'},
    'digit_error':          {'en': 'Digit error',              'fr': 'Erreur de chiffre'},
    'arithmetic_error':     {'en': 'Arithmetic error',         'fr': 'Erreur de calcul'},
    # Decimal & fractions
    'decimal_shift':        {'en': 'Decimal point shifted',    'fr': 'Virgule décalée'},
    'add_across':           {'en': 'Added numerators/denominators separately', 'fr': 'Numérateurs et dénominateurs additionnés séparément'},
    'forgot_flip':          {'en': 'Forgot to flip for division', 'fr': 'Oubli d\'inverser pour la division'},
    'digit_swap':           {'en': 'Digits swapped',           'fr': 'Chiffres inversés'},
    'extra_zero':           {'en': 'Extra zero added',         'fr': 'Zéro en trop'},
    'missing_comma':        {'en': 'Missing decimal point',    'fr': 'Virgule oubliée'},
    'wrong_place':          {'en': 'Wrong decimal place',      'fr': 'Mauvaise position décimale'},
    'too_small':            {'en': 'Value too small',          'fr': 'Valeur trop petite'},
    'missing_dec':          {'en': 'Missing decimal part',     'fr': 'Partie décimale manquante'},
    'fraction_kept':        {'en': 'Fraction not converted',   'fr': 'Fraction non convertie'},
    'reversed':             {'en': 'Fraction inverted',        'fr': 'Fraction inversée'},
    # Comparison & number sense
    'reversed_comparison':  {'en': 'Comparison reversed',      'fr': 'Comparaison inversée'},
    'not_prime':            {'en': 'Number not prime',         'fr': 'Nombre non premier'},
    'not_square':           {'en': 'Not a perfect square',     'fr': 'Nombre non carré'},
    'parity_confusion':     {'en': 'Parity confusion',         'fr': 'Parité confondue'},
    'wrong_classification': {'en': 'Wrong classification',     'fr': 'Mauvaise classification'},
    'wrong_formula':        {'en': 'Wrong formula',            'fr': 'Mauvaise formule'},
    'sign_error':           {'en': 'Sign error',               'fr': 'Erreur de signe'},
    # Measurement & units
    'wrong_conversion':     {'en': 'Wrong conversion',         'fr': 'Mauvaise conversion'},
    'wrong_unit':           {'en': 'Wrong unit',               'fr': 'Mauvaise unité'},
    'wrong_quantity':       {'en': 'Wrong quantity type',      'fr': 'Mauvaise grandeur'},
    'close_unit':           {'en': 'Close unit (wrong scale)', 'fr': 'Unité proche (mauvaise échelle)'},
    'wrong_time':           {'en': 'Wrong time',               'fr': 'Heure incorrecte'},
    'wrong_temperature':    {'en': 'Wrong temperature',        'fr': 'Température incorrecte'},
    # Statistics & probability
    'wrong_probability':    {'en': 'Wrong probability',        'fr': 'Probabilité incorrecte'},
    'complement':           {'en': 'Complement confused',      'fr': 'Complémentaire confondu'},
    'ratio_not_prob':       {'en': 'Ratio ≠ probability',      'fr': 'Rapport ≠ probabilité'},
    'inverted':             {'en': 'Fraction inverted',        'fr': 'Fraction inversée'},
    'wrong_category':       {'en': 'Wrong category',           'fr': 'Mauvaise catégorie'},
    'wrong_sector':         {'en': 'Wrong pie sector',         'fr': 'Mauvais secteur'},
    'sum_not_product':      {'en': 'Added instead of multiplied', 'fr': 'Addition au lieu de multiplication'},
    'forgot_category':      {'en': 'Forgot a category',        'fr': 'Catégorie oubliée'},
    'forgot_last':          {'en': 'Forgot last item',         'fr': 'Dernier élément oublié'},
    'counted_twice':        {'en': 'Counted twice',            'fr': 'Compté deux fois'},
    'max_not_total':        {'en': 'Max confused with total',  'fr': 'Maximum confondu avec le total'},
    'max_not_diff':         {'en': 'Max confused with difference', 'fr': 'Maximum confondu avec la différence'},
    'min_not_diff':         {'en': 'Min confused with difference', 'fr': 'Minimum confondu avec la différence'},
    'added_not_subtracted': {'en': 'Added instead of subtracted', 'fr': 'Addition au lieu de soustraction'},
    # Number line & sequences
    'one_step_left':        {'en': 'One step too far left',    'fr': 'Un pas trop à gauche'},
    'one_step_right':       {'en': 'One step too far right',   'fr': 'Un pas trop à droite'},
    'two_steps_off':        {'en': 'Two steps off',            'fr': 'Deux pas de décalage'},
    'at_origin':            {'en': 'Read from origin',         'fr': 'Lu depuis l\'origine'},
    'wrong_group':          {'en': 'Wrong digit group',        'fr': 'Mauvais groupe de chiffres'},
    'wrong_fact':           {'en': 'Incorrect number fact',    'fr': 'Calcul incorrect'},
    'left_to_right':        {'en': 'Left-to-right error',      'fr': 'Erreur gauche-droite'},
    # Misc
    'distractor':           {'en': 'Random error',             'fr': 'Erreur aléatoire'},
}


def _error_label(error_type, lang):
    """Return human-readable label for an error type slug."""
    entry = ERROR_TYPE_LABELS.get(error_type)
    if entry:
        return entry.get(lang) or entry.get('en') or error_type
    # Fallback: convert snake_case to Title Case
    return error_type.replace('_', ' ').title()


TOPIC_META = {
    topic['slug']: {
        'slug': topic['slug'],
        'group_en': group['name_en'],
        'group_fr': group['name_fr'],
        'group_icon': group['icon'],
        'name_en': topic['name_en'],
        'name_fr': topic['name_fr'],
    }
    for group in TOPIC_GROUPS
    for topic in group['topics']
}

PRIZE_CATALOG = [
    {'slug': 'cat', 'cost': 25, 'icon': AVATAR_EMOJIS['cat'], 'name_en': 'Curious Cat', 'name_fr': 'Chat Curieux', 'description_en': 'A playful buddy for practice time.', 'description_fr': 'Un ami joueur pour t accompagner.', 'type': 'avatar'},
    {'slug': 'dog', 'cost': 25, 'icon': AVATAR_EMOJIS['dog'], 'name_en': 'Brave Dog', 'name_fr': 'Chien Courageux', 'description_en': 'A happy helper who cheers each answer.', 'description_fr': 'Un compagnon joyeux qui t encourage.', 'type': 'avatar'},
    {'slug': 'frog', 'cost': 35, 'icon': AVATAR_EMOJIS['frog'], 'name_en': 'Leap Frog', 'name_fr': 'Grenouille Bondissante', 'description_en': 'Jump into the next challenge with confidence.', 'description_fr': 'Bondis vers le prochain défi.', 'type': 'avatar'},
    {'slug': 'fox', 'cost': 40, 'icon': AVATAR_EMOJIS['fox'], 'name_en': 'Smart Fox', 'name_fr': 'Renard Malin', 'description_en': 'For sharp thinkers and quick patterns.', 'description_fr': 'Pour les esprits vifs et malins.', 'type': 'avatar'},
    {'slug': 'bear', 'cost': 50, 'icon': AVATAR_EMOJIS['bear'], 'name_en': 'Strong Bear', 'name_fr': 'Ours Fort', 'description_en': 'A calm champion for steady learners.', 'description_fr': 'Un champion calme pour progresser.', 'type': 'avatar'},
    {'slug': 'butterfly', 'cost': 60, 'icon': AVATAR_EMOJIS['butterfly'], 'name_en': 'Rainbow Butterfly', 'name_fr': 'Papillon Arc-en-ciel', 'description_en': 'A bright reward for growing skills.', 'description_fr': 'Une récompense lumineuse pour tes progrès.', 'type': 'avatar'},
    {'slug': 'lion', 'cost': 70, 'icon': AVATAR_EMOJIS['lion'], 'name_en': 'Lion Leader', 'name_fr': 'Lion Leader', 'description_en': 'For students ready to roar with confidence.', 'description_fr': 'Pour les élèves prêts à rugir de confiance.', 'type': 'avatar'},
    {'slug': 'panda', 'cost': 85, 'icon': AVATAR_EMOJIS['panda'], 'name_en': 'Panda Master', 'name_fr': 'Panda Maître', 'description_en': 'A special friend for consistent effort.', 'description_fr': 'Un ami spécial pour les efforts réguliers.', 'type': 'avatar'},
    {'slug': 'octopus', 'cost': 95, 'icon': AVATAR_EMOJIS['octopus'], 'name_en': 'Octopus Genius', 'name_fr': 'Pieuvre Géniale', 'description_en': 'Handle many skills at once.', 'description_fr': 'Maîtrise plusieurs compétences à la fois.', 'type': 'avatar'},
    {'slug': 'unicorn', 'cost': 120, 'icon': AVATAR_EMOJIS['unicorn'], 'name_en': 'Magic Unicorn', 'name_fr': 'Licorne Magique', 'description_en': 'A magical prize for big progress.', 'description_fr': 'Un prix magique pour de grands progrès.', 'type': 'avatar'},
    {'slug': 'dino', 'cost': 140, 'icon': AVATAR_EMOJIS['dino'], 'name_en': 'Dino Hero', 'name_fr': 'Dino Héros', 'description_en': 'A big reward for fearless learners.', 'description_fr': 'Une grande récompense pour les élèves courageux.', 'type': 'avatar'},
    {'slug': 'rocket', 'cost': 0, 'icon': AVATAR_EMOJIS['rocket'], 'name_en': 'Starter Rocket', 'name_fr': 'Fusée de Départ', 'description_en': 'Your first avatar, ready for lift-off.', 'description_fr': 'Ton premier avatar, prêt au décollage.', 'type': 'avatar'},
]


# ── Auth forms ────────────────────────────────────────────────────────────────

class RegisterForm(forms.Form):
    username  = forms.CharField(min_length=2, max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=4)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=4)

    def clean_username(self):
        u = self.cleaned_data['username']
        if User.objects.filter(username__iexact=u).exists():
            raise forms.ValidationError('Username already taken.')
        return u

    def clean(self):
        cd = super().clean()
        if cd.get('password1') != cd.get('password2'):
            self.add_error('password2', 'Passwords do not match.')
        return cd


# ── Auth views ────────────────────────────────────────────────────────────────

def register_view(request):
    lang = request.GET.get('lang', 'en')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            Student.objects.create(user=user)
            auth_login(request, user)
            return redirect('quiz:index')
    else:
        form = RegisterForm()
    return render(request, 'quiz/register.html', {'form': form, 'lang': lang})


def login_view(request):
    lang  = request.GET.get('lang', 'en')
    error = ''
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
        )
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next') or '/'
            return redirect(next_url)
        error = 'Invalid username or password.' if lang == 'en' else 'Identifiants incorrects.'
    return render(request, 'quiz/login.html', {'error': error, 'lang': lang})


def logout_view(request):
    auth_logout(request)
    return redirect('quiz:index')


def _topic_label(topic_slug, lang='en'):
    meta = TOPIC_META.get(topic_slug, {})
    if not meta:
        return topic_slug
    return meta['name_fr'] if lang == 'fr' else meta['name_en']


def _topic_card_groups(student=None, grade_filter=None):
    ratings = (student.skill_ratings if student else {}) or {}
    groups = []
    for group in TOPIC_GROUPS:
        # Apply grade filter: None/0 = all, N = only groups where grade == N
        if grade_filter and group.get('grade') != grade_filter:
            continue
        topics = []
        for topic in group['topics']:
            stat = ratings.get(topic['slug'], {})
            total = stat.get('total', 0)
            correct = stat.get('correct', 0)
            topics.append({
                **topic,
                'answered': total,
                'accuracy': round(correct / total * 100) if total else None,
            })
        groups.append({**group, 'topics': topics})
    return groups


def _prize_cards(student, lang='en'):
    unlocked = set(student.unlocked_avatars or [])
    unlocked.add(student.avatar_slug)
    unlocked.add('rocket')
    cards = []
    for prize in PRIZE_CATALOG:
        cards.append({
            **prize,
            'name': prize['name_fr'] if lang == 'fr' else prize['name_en'],
            'description': prize['description_fr'] if lang == 'fr' else prize['description_en'],
            'is_unlocked': prize['slug'] in unlocked,
            'is_selected': prize['slug'] == student.avatar_slug,
            'can_afford': student.total_stars >= prize['cost'],
        })
    cards.sort(key=lambda item: (item['cost'], item['slug']))
    return cards


def _student_level(stars):
    if stars >= 200: return 7
    if stars >= 150: return 6
    if stars >= 100: return 5
    if stars >= 60:  return 4
    if stars >= 30:  return 3
    if stars >= 10:  return 2
    return 1


def index(request):
    lang = request.GET.get('lang', 'en')
    # Parents land on their own dashboard
    if request.user.is_authenticated and hasattr(request.user, 'parent_profile'):
        from django.urls import reverse
        return redirect(f"{reverse('quiz:parent_dashboard')}?lang={lang}")

    quizsets = QuizSet.objects.prefetch_related('questions').all()
    student  = getattr(request.user, 'student', None) if request.user.is_authenticated else None
    recent_count = ProblemInteraction.objects.filter(user=request.user).count() if request.user.is_authenticated else 0

    # Parent assignments for this student
    parent_assignments = []
    if student:
        parent_assignments = list(
            ParentAssignment.objects.filter(student=request.user)
            .select_related('parent__user')
        )

    # Recent topics (for "Recent skills" tab)
    recent_topics = []
    if student:
        from django.db.models import Max
        recent_topics = list(
            ProblemInteraction.objects.filter(user=request.user)
            .values('topic')
            .annotate(last=Max('created_at'))
            .order_by('-last')
            .values_list('topic', flat=True)[:6]
        )

    # Student level
    level = _student_level(student.total_stars if student else 0)

    # Grade filter (school grade, separate from gamification level)
    try:
        grade_filter = int(request.GET.get('grade', 0)) or None
    except (ValueError, TypeError):
        grade_filter = None

    is_guest = not request.user.is_authenticated
    template = 'quiz/index_landing.html' if is_guest else 'quiz/index.html'
    return render(request, template, {
        'quizsets':           quizsets,
        'lang':               lang,
        'topic_groups':       _topic_card_groups(student, grade_filter=grade_filter),
        'all_topic_groups':   _topic_card_groups(student),   # unfiltered, for sidebar lookups
        'recent_count':       recent_count,
        'is_guest':           is_guest,
        'parent_assignments': parent_assignments,
        'recent_topics':      recent_topics,
        'student_level':      level,
        'grade_filter':       grade_filter,
        'available_grades':   sorted(set(g['grade'] for g in TOPIC_GROUPS if g.get('grade'))),
    })


def playground(request, quiz_id):
    quiz    = get_object_or_404(QuizSet, pk=quiz_id)
    lang    = request.GET.get('lang', 'en')
    q_index = int(request.GET.get('q', 0))
    questions = list(quiz.questions.prefetch_related('choices', 'pairs').all())

    if not questions:
        return render(request, 'quiz/empty.html', {'quiz': quiz})

    q_index  = max(0, min(q_index, len(questions) - 1))
    question = questions[q_index]

    session_id = request.session.get(f'session_{quiz_id}')
    if not session_id:
        session = StudentSession.objects.create(
            quiz_set=quiz,
            max_score=sum(q.points for q in questions),
            language=lang,
        )
        request.session[f'session_{quiz_id}'] = session.pk
    else:
        session = StudentSession.objects.get(pk=session_id)

    choices = list(question.choices.all())
    _random.shuffle(choices)
    context = {
        'quiz':                quiz,
        'question':            question,
        'questions':           questions,
        'q_index':             q_index,
        'total':               len(questions),
        'lang':                lang,
        'session':             session,
        'session_answers_json': json.dumps(session.answers),
        'progress':            round((q_index / len(questions)) * 100),
        'shuffled_choices':    choices,
    }
    return render(request, 'quiz/playground.html', context)


def question_partial(request, quiz_id, q_index):
    """htmx partial — swaps just the question area"""
    quiz      = get_object_or_404(QuizSet, pk=quiz_id)
    lang      = request.GET.get('lang', 'en')
    questions = list(quiz.questions.prefetch_related('choices', 'pairs').all())
    q_index   = max(0, min(int(q_index), len(questions) - 1))
    question  = questions[q_index]

    session_id = request.session.get(f'session_{quiz_id}')
    session    = StudentSession.objects.get(pk=session_id) if session_id else None

    choices = list(question.choices.all())
    _random.shuffle(choices)
    context = {
        'quiz':             quiz,
        'question':         question,
        'questions':        questions,
        'q_index':          q_index,
        'total':            len(questions),
        'lang':             lang,
        'session':          session,
        'progress':         round((q_index / len(questions)) * 100),
        'partial':          True,
        'shuffled_choices': choices,
    }
    return render(request, 'partials/question_area.html', context)


def review_question_partial(request, quiz_id, q_pk):
    """Frozen review partial: shows submitted answer vs correct answer."""
    quiz     = get_object_or_404(QuizSet, pk=quiz_id)
    lang     = request.GET.get('lang', 'en')
    question = get_object_or_404(Question, pk=q_pk)

    session_id = request.session.get(f'session_{quiz_id}')
    session    = StudentSession.objects.get(pk=session_id) if session_id else None

    submitted_answer = None
    was_correct      = None
    if session:
        ans = session.answers.get(str(q_pk))
        if ans:
            submitted_answer = ans.get('answer')   # list of choice PKs (strings)
            was_correct      = ans.get('correct')

    submitted_pks = [str(pk) for pk in (submitted_answer or [])]

    choice_display = []
    for c in question.choices.all():
        label = (c.label_fr or c.label_en) if lang == 'fr' else c.label_en
        choice_display.append({
            'label':       label,
            'is_correct':  c.is_correct,
            'was_selected': str(c.pk) in submitted_pks,
        })

    context = {
        'quiz':             quiz,
        'question':         question,
        'lang':             lang,
        'choice_display':   choice_display,
        'was_correct':      was_correct,
        'submitted':        submitted_answer is not None,
        'submitted_answer': submitted_answer,
    }
    return render(request, 'partials/review_question.html', context)


@require_POST
def submit_answer(request, quiz_id, q_index):
    quiz      = get_object_or_404(QuizSet, pk=quiz_id)
    questions = list(quiz.questions.prefetch_related('choices', 'pairs').all())
    q_index   = max(0, min(int(q_index), len(questions) - 1))
    question  = questions[q_index]
    try:
        body   = json.loads(request.body)
        answer = body.get('answer')
        lang   = body.get('lang', 'en')
    except (json.JSONDecodeError, AttributeError):
        answer = request.POST.get('answer')
        lang   = request.POST.get('lang', 'en')

    correct    = _check_answer(question, answer)
    points_won = question.points if correct else 0

    session_id = request.session.get(f'session_{quiz_id}')
    if session_id:
        session = StudentSession.objects.get(pk=session_id)
        answers = session.answers
        if str(question.pk) not in answers:
            answers[str(question.pk)] = {
                'answer':  answer,
                'correct': correct,
                'points':  points_won,
            }
            session.answers = answers
            session.score   = sum(v['points'] for v in answers.values())
            session.save()

    return JsonResponse({
        'correct':    correct,
        'points':     points_won,
        'q_index':    q_index,
        'next_index': min(q_index + 1, len(questions) - 1),
        'is_last':    q_index == len(questions) - 1,
        'score':      session.score if session_id else 0,
        'max_score':  quiz.questions.aggregate(total=Sum('points'))['total'] or 0,
        'feedback_en': _feedback(question, correct, 'en'),
        'feedback_fr': _feedback(question, correct, 'fr'),
    })


def scoreboard(request, quiz_id):
    quiz       = get_object_or_404(QuizSet, pk=quiz_id)
    lang       = request.GET.get('lang', 'en')
    session_id = request.session.get(f'session_{quiz_id}')
    session    = StudentSession.objects.get(pk=session_id) if session_id else None
    questions  = list(quiz.questions.prefetch_related('choices', 'pairs').all())

    if session and not session.finished_at:
        session.finished_at = timezone.now()
        session.save()

    context = {
        'quiz':      quiz,
        'session':   session,
        'questions': questions,
        'lang':      lang,
    }
    return render(request, 'quiz/scoreboard.html', context)


# ---------- practice views ----------

@login_required
def practice_page(request, topic):
    if topic not in GENERATORS:
        from django.http import Http404
        raise Http404
    lang  = request.GET.get('lang', 'en')
    level = request.GET.get('level', 'medium')
    topic_info = None
    for g in TOPIC_GROUPS:
        for t in g['topics']:
            if t['slug'] == topic:
                topic_info = t
                break

    # Parent assignments for this student
    parent_assignments = []
    if request.user.is_authenticated:
        pas = ParentAssignment.objects.filter(student=request.user, completed_at__isnull=True).select_related('parent__user')[:6]
        # Enrich with topic display name
        all_topics = {t['slug']: t for g in TOPIC_GROUPS for t in g['topics']}
        for pa in pas:
            ti = all_topics.get(pa.topic_slug, {})
            parent_assignments.append({
                'slug': pa.topic_slug,
                'name_fr': ti.get('name_fr', pa.topic_slug),
                'name_en': ti.get('name_en', pa.topic_slug),
                'parent_name': pa.parent.user.get_full_name() or pa.parent.user.username,
            })

    # Machine recommendations: next + mastery_next from SKILL_MAP
    skill_info = SKILL_MAP.get(topic, {})
    all_topics = {t['slug']: t for g in TOPIC_GROUPS for t in g['topics']}
    recommendations = []
    for key, label_fr, label_en, icon in [
        ('next',         'Prochaine étape',    'Next step',        '➡️'),
        ('mastery_next', 'Après maîtrise',     'After mastery',    '🏆'),
    ]:
        slug = skill_info.get(key)
        if slug and slug in GENERATORS and slug != topic:
            ti = all_topics.get(slug, {})
            recommendations.append({
                'slug':     slug,
                'name_fr':  ti.get('name_fr', slug),
                'name_en':  ti.get('name_en', slug),
                'label_fr': label_fr,
                'label_en': label_en,
                'icon':     icon,
            })

    return render(request, 'quiz/practice.html', {
        'topic':              topic,
        'level':              level,
        'lang':               lang,
        'topic_info':         topic_info,
        'topic_groups':       _topic_card_groups(request.user.student),
        'levels':             [('easy', 'Easy', 'Facile'), ('medium', 'Medium', 'Moyen'), ('hard', 'Hard', 'Difficile')],
        'parent_assignments': parent_assignments,
        'recommendations':    recommendations,
    })


@login_required
def practice_next(request, topic):
    """htmx GET — generate and return the next question partial."""
    if topic not in GENERATORS:
        from django.http import Http404
        raise Http404
    import random as _random
    lang  = request.GET.get('lang', 'en')
    level = request.GET.get('level', 'medium')
    # Student dismissed a suggestion — snooze it for 5 more questions
    if request.GET.get('snooze') == '1':
        key = f'ps_{topic}'
        stats = request.session.get(key, {})
        stats['snooze'] = 5
        request.session[key] = stats
    q = GENERATORS[topic](level)
    # Generators that always need an illustration set show_illustration=True themselves;
    # for the rest, show it probabilistically (or always for classic geometry).
    if not q.get('show_illustration'):
        q['show_illustration'] = (
            topic in ('geometry-area', 'geometry-perimeter') or _random.random() < 0.30
        )
    request.session[f'pq_{topic}'] = q
    return render(request, 'partials/practice_question.html', {
        'question': q,
        'topic':    topic,
        'level':    level,
        'lang':     lang,
    })


@login_required
@require_POST
def practice_check(request, topic):
    """htmx POST — validate answer, return feedback partial."""
    q_data = request.session.get(f'pq_{topic}')
    if not q_data:
        from django.http import Http404
        raise Http404
    lang   = request.POST.get('lang', 'en')
    level  = request.POST.get('level', 'medium')
    answer = request.POST.get('answer', '').strip()

    correct = _check_practice(q_data, answer)

    # ── Extended session stats ────────────────────────────────────────────────
    key   = f'ps_{topic}'
    stats = request.session.get(key, {
        'streak': 0, 'total': 0, 'wrong_streak': 0,
        'level_correct': 0, 'level_total': 0,
    })
    # Migrate old sessions that only had streak/total
    stats.setdefault('wrong_streak', 0)
    stats.setdefault('level_correct', 0)
    stats.setdefault('level_total', 0)

    if correct:
        stats['streak']        += 1
        stats['wrong_streak']   = 0
        stats['level_correct'] += 1
    else:
        stats['streak']       = 0
        stats['wrong_streak'] += 1
    stats['total']       += 1
    stats['level_total'] += 1
    request.session[key]  = stats

    # ── Misconception feedback from tagged distractor ─────────────────────────
    misconception_feedback = ''
    error_type = ''
    answer_data = None   # structured data for ordering / mix_match feedback
    try:
        answer_index = int(answer)
    except (ValueError, TypeError):
        answer_index = None

    q_type = q_data.get('q_type')

    if q_type == 'multiple_choice' and not correct and answer_index is not None:
        try:
            chosen = q_data['choices'][answer_index]
            error_type = chosen.get('error_type', '')
            fb_key = f'feedback_{lang}' if lang == 'fr' else 'feedback_en'
            misconception_feedback = chosen.get(fb_key) or chosen.get('feedback_en', '')
        except (IndexError, KeyError, TypeError):
            pass

    elif q_type in ('ordering', 'sorting'):
        try:
            submitted_labels = json.loads(answer) if answer else []
            label_to_order   = {item['label']: item['order']
                                 for item in q_data.get('items', [])}
            answer_data = [
                {
                    'label':        label,
                    'submitted_pos': i + 1,
                    'correct_pos':  label_to_order.get(label, 0),
                    'is_correct':   label_to_order.get(label, 0) == i + 1,
                }
                for i, label in enumerate(submitted_labels)
            ]
        except (ValueError, TypeError):
            answer_data = []

    elif q_type == 'mix_match':
        try:
            submitted = json.loads(answer) if answer else {}
            answer_data = [
                {
                    'left':           p['left'],
                    'right_correct':  p['right'],
                    'right_submitted': submitted.get(p['left'], ''),
                    'is_correct':     submitted.get(p['left']) == p['right'],
                }
                for p in q_data.get('pairs', [])
            ]
        except (ValueError, TypeError):
            answer_data = []

    # ── Star + interaction tracking ───────────────────────────────────────────
    LEVEL_STARS  = {'easy': 1, 'medium': 2, 'hard': 3}
    stars_earned = 0
    stars_value  = LEVEL_STARS.get(level, 1)
    ProblemInteraction.objects.create(
        user=request.user, topic=topic, level=level,
        is_correct=correct,
        points_earned=stars_value if correct else 0,
        error_type=error_type,
    )
    from django.db.models import F
    if correct:
        stars_earned = stars_value
        Student.objects.filter(user=request.user).update(total_stars=F('total_stars') + stars_value)
        student = Student.objects.get(user=request.user)
        sr = student.skill_ratings
        entry = sr.get(topic, {'correct': 0, 'total': 0})
        entry['total']   += 1
        entry['correct'] += 1
        sr[topic] = entry
        student.skill_ratings = sr
        student.save(update_fields=['skill_ratings'])
    else:
        student = Student.objects.get(user=request.user)
        sr = student.skill_ratings
        entry = sr.get(topic, {'correct': 0, 'total': 0})
        entry['total'] += 1
        sr[topic] = entry
        student.skill_ratings = sr
        student.save(update_fields=['skill_ratings'])

    # ── Adaptive progression suggestion ──────────────────────────────────────
    skill_info = SKILL_MAP.get(topic, {})
    suggested_action  = None
    suggested_level   = level
    suggested_topic   = None
    level_seq = skill_info.get('level_sequence', ['easy', 'medium', 'hard'])

    # Respect snooze: student already dismissed a suggestion, don't nag for N more questions
    snooze = stats.get('snooze', 0)
    if snooze > 0:
        stats['snooze'] = snooze - 1
        request.session[key] = stats
    else:
        if correct and stats['streak'] >= 5:
            idx = level_seq.index(level) if level in level_seq else -1
            if idx < len(level_seq) - 1:
                suggested_action = 'level_up'
                suggested_level  = level_seq[idx + 1]
            elif skill_info.get('mastery_next'):
                suggested_action = 'mastery'
                suggested_topic  = skill_info['mastery_next']

        elif not correct and stats['wrong_streak'] >= 3:
            idx = level_seq.index(level) if level in level_seq else 1
            if idx > 0:
                suggested_action = 'level_down'
                suggested_level  = level_seq[idx - 1]
            elif skill_info.get('downgrade'):
                suggested_action = 'prerequisite'
                suggested_topic  = skill_info['downgrade']

    expl_key = 'explanation_en' if lang != 'fr' else 'explanation_fr'
    _updated_student = Student.objects.filter(user=request.user).values('total_stars').first()
    total_stars_now  = _updated_student['total_stars'] if _updated_student else 0
    return render(request, 'partials/practice_feedback.html', {
        'correct':               correct,
        'streak':                stats['streak'],
        'total':                 stats['total'],
        'wrong_streak':          stats['wrong_streak'],
        'stars_earned':          stars_earned,
        'total_stars':           total_stars_now,
        'explanation':           q_data.get(expl_key, q_data.get('explanation_en', '')),
        'misconception_feedback': misconception_feedback,
        'error_type':            error_type,
        'question':              q_data,
        'answer':                answer,
        'answer_index':          answer_index,
        'answer_data':           answer_data,
        'topic':                 topic,
        'level':                 level,
        'lang':                  lang,
        'suggested_action':      suggested_action,
        'suggested_level':       suggested_level,
        'suggested_topic':       suggested_topic,
    })


# ---------- helpers ----------

def _check_practice(q_data, answer):
    qt = q_data.get('q_type')
    if qt == 'multiple_choice':
        try:
            return q_data['choices'][int(answer)]['correct']
        except (ValueError, IndexError, KeyError, TypeError):
            return False
    elif qt == 'text_input':
        from .generators.base import _normalize_answer
        norm = _normalize_answer(answer)
        return norm.lower() in [_normalize_answer(a).lower() for a in q_data.get('correct_answers', [])]
    elif qt in ('ordering', 'sorting'):
        try:
            submitted = json.loads(answer)
            correct   = [item['label'] for item in
                         sorted(q_data['items'], key=lambda x: x['order'])]
            return submitted == correct
        except (ValueError, KeyError, TypeError):
            return False
    elif qt == 'mix_match':
        try:
            submitted = json.loads(answer)
            return all(
                submitted.get(p['left']) == p['right']
                for p in q_data.get('pairs', [])
            )
        except (ValueError, TypeError):
            return False
    return False


def _check_answer(question, answer):
    qt = question.q_type
    if qt == 'multiple_choice':
        correct_ids = set(
            str(c.pk) for c in question.choices.filter(is_correct=True)
        )
        if isinstance(answer, list):
            return set(str(a) for a in answer) == correct_ids
        return str(answer) in correct_ids

    elif qt == 'text_input':
        correct_labels = [
            c.label_en.strip().lower()
            for c in question.choices.filter(is_correct=True)
        ]
        return str(answer).strip().lower() in correct_labels

    elif qt == 'drag_drop':
        # answer = [{id, pos}, ...] — check each item's submitted pos matches its correct order
        if not isinstance(answer, list):
            return False
        choices = {str(c.pk): c.order for c in question.choices.all()}
        submitted = {str(item['id']): item['pos'] for item in answer if 'id' in item and 'pos' in item}
        return all(submitted.get(cid, -1) == order for cid, order in choices.items())

    elif qt in ('connect', 'mix_match'):
        if not isinstance(answer, dict):
            return False
        pairs = {str(p.pk): str(p.right_en) for p in question.pairs.all()}
        return all(answer.get(k, '').strip().lower() == v.strip().lower()
                   for k, v in pairs.items())
    return False


# ── Profile / Avatar (Phase 6) ────────────────────────────────────────────────

@login_required
def profile_view(request):
    lang    = request.GET.get('lang', 'en')
    student = request.user.student
    if request.method == 'POST':
        slug = request.POST.get('avatar', '')
        if slug in AVATAR_SLUGS:
            student.avatar_slug = slug
            student.save(update_fields=['avatar_slug'])
        return redirect(f"{request.path}?lang={lang}")
    avatars = [{'slug': s, 'emoji': AVATAR_EMOJIS[s]} for s in AVATAR_SLUGS]
    return render(request, 'quiz/profile.html', {
        'lang':    lang,
        'student': student,
        'avatars': avatars,
    })


@login_required
def dashboard(request):
    from datetime import date, timedelta

    lang = request.GET.get('lang', 'en')
    tab = request.GET.get('tab', 'session')
    tabs = [
        ('session', 'Activity', 'Activité'),
        ('trends', 'Weekly', 'Semaine'),
        ('insights', 'Strengths', 'Forces'),
        ('misconceptions', 'Mistakes', 'Erreurs'),
    ]
    interactions_qs = ProblemInteraction.objects.filter(user=request.user)
    solved = interactions_qs.count()
    correct = interactions_qs.filter(is_correct=True).count()
    best_streak = 0
    current_streak = 0
    for result in interactions_qs.values_list('is_correct', flat=True).order_by('created_at'):
        if result:
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            current_streak = 0

    ctx = {
        'lang': lang,
        'tab': tab,
        'tabs': tabs,
        'page_title': 'Progrès' if lang == 'fr' else 'Progress',
        'page_subtitle': 'Ton parcours d apprentissage en maths et langage.' if lang == 'fr' else 'Your maths and language learning journey.',
        'summary_cards': [
            {'label_en': 'Stars', 'label_fr': 'Étoiles', 'value': request.user.student.total_stars, 'tone': 'amber', 'icon': '⭐'},
            {'label_en': 'Solved', 'label_fr': 'Réponses', 'value': solved, 'tone': 'indigo', 'icon': '🎯'},
            {'label_en': 'Accuracy', 'label_fr': 'Précision', 'value': f"{round(correct / solved * 100) if solved else 0}%", 'tone': 'emerald', 'icon': '📈'},
            {'label_en': 'Best Streak', 'label_fr': 'Meilleure série', 'value': best_streak, 'tone': 'sky', 'icon': '🔥'},
        ],
    }

    if tab == 'session':
        ctx['interactions'] = [
            {
                'topic': _topic_label(item.topic, lang),
                'group_icon': TOPIC_META.get(item.topic, {}).get('group_icon', '🧩'),
                'level': item.level,
                'is_correct': item.is_correct,
                'points_earned': item.points_earned,
                'created_at': item.created_at,
            }
            for item in interactions_qs[:18]
        ]

    elif tab == 'trends':
        today = date.today()
        days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        qs = (
            interactions_qs
            .filter(created_at__date__gte=days[0])
            .values('created_at__date')
            .annotate(total=Count('id'), correct=Count('id', filter=Q(is_correct=True)))
        )
        by_date = {row['created_at__date']: row for row in qs}
        bars = []
        for d in days:
            row = by_date.get(d, {'total': 0, 'correct': 0})
            total = row['total']
            pct = round(row['correct'] / total * 100) if total else 0
            bars.append({'date': d, 'total': total, 'pct': pct})
        ctx['bars'] = bars

    elif tab == 'insights':
        qs = (
            interactions_qs
            .values('topic')
            .annotate(total=Count('id'), correct=Count('id', filter=Q(is_correct=True)))
        )
        strengths = []
        opportunities = []
        for row in qs:
            if row['total'] < 5:
                continue
            pct = round(row['correct'] / row['total'] * 100)
            entry = {'topic': _topic_label(row['topic'], lang), 'pct': pct, 'total': row['total'], 'slug': row['topic']}
            if pct >= 70:
                strengths.append(entry)
            elif pct < 60:
                opportunities.append(entry)
        ctx['strengths'] = sorted(strengths, key=lambda x: -x['pct'])
        ctx['opportunities'] = sorted(opportunities, key=lambda x: x['pct'])

    elif tab == 'misconceptions':
        raw_errors = (
            interactions_qs
            .filter(is_correct=False)
            .exclude(error_type='')
            .values('error_type')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        ctx['error_types'] = [
            {'error_type': _error_label(r['error_type'], lang), 'count': r['count']}
            for r in raw_errors
        ]
        topic_errors = {}
        qs2 = (
            interactions_qs
            .filter(is_correct=False)
            .exclude(error_type='')
            .values('topic', 'error_type')
            .annotate(count=Count('id'))
            .order_by('topic', '-count')
        )
        for row in qs2:
            label = _topic_label(row['topic'], lang)
            if label not in topic_errors:
                topic_errors[label] = []
            if len(topic_errors[label]) < 3:
                topic_errors[label].append({
                    'error_type': _error_label(row['error_type'], lang),
                    'count': row['count'],
                    'slug': row['topic'],
                })
        ctx['topic_errors'] = topic_errors

    if request.headers.get('HX-Request'):
        return render(request, 'partials/dashboard_body.html', ctx)
    return render(request, 'quiz/dashboard.html', ctx)


@login_required
def prizes_view(request):
    lang = request.GET.get('lang', 'en')
    student = request.user.student
    unlocked = set(student.unlocked_avatars or [])
    unlocked.add('rocket')
    unlocked.add(student.avatar_slug)

    if request.method == 'POST':
        action = request.POST.get('action')
        slug = request.POST.get('slug', '')
        catalog = {item['slug']: item for item in PRIZE_CATALOG}
        if slug in catalog:
            prize = catalog[slug]
            if action == 'unlock':
                if slug not in unlocked and student.total_stars >= prize['cost']:
                    unlocked.add(slug)
                    student.unlocked_avatars = sorted(unlocked)
                    student.total_stars = max(0, student.total_stars - prize['cost'])
                    student.save(update_fields=['unlocked_avatars', 'total_stars'])
            elif action == 'select' and slug in unlocked:
                student.avatar_slug = slug
                student.unlocked_avatars = sorted(unlocked)
                student.save(update_fields=['avatar_slug', 'unlocked_avatars'])
        return redirect(f"{request.path}?lang={lang}")

    cards = _prize_cards(student, lang)
    unlocked_count = len([item for item in cards if item['is_unlocked']])
    latest_unlocked = None
    unlocked_cards = [item for item in cards if item['is_unlocked'] and item['cost'] > 0]
    if unlocked_cards:
        latest_unlocked = sorted(unlocked_cards, key=lambda item: (item['cost'], item['slug']))[-1]
    return render(request, 'quiz/prizes.html', {
        'lang': lang,
        'student': student,
        'prizes': cards,
        'latest_unlocked': latest_unlocked,
        'unlocked_count': unlocked_count,
    })


@login_required
def profile_view(request):
    lang = request.GET.get('lang', 'en')
    student = request.user.student
    unlocked = set(student.unlocked_avatars or [])
    unlocked.add('rocket')
    unlocked.add(student.avatar_slug)
    if request.method == 'POST':
        slug = request.POST.get('avatar', '')
        if slug in AVATAR_SLUGS and slug in unlocked:
            student.avatar_slug = slug
            student.unlocked_avatars = sorted(unlocked)
            student.save(update_fields=['avatar_slug', 'unlocked_avatars'])
        return redirect(f"{request.path}?lang={lang}")
    interactions = ProblemInteraction.objects.filter(user=request.user)
    avatars = [
        {'slug': s, 'emoji': AVATAR_EMOJIS[s], 'is_unlocked': s in unlocked}
        for s in AVATAR_SLUGS
    ]
    return render(request, 'quiz/profile.html', {
        'lang': lang,
        'student': student,
        'avatars': avatars,
        'solved_count': interactions.count(),
        'accuracy_pct': round(interactions.filter(is_correct=True).count() / interactions.count() * 100) if interactions.exists() else 0,
    })


def _feedback(question, correct, lang):
    if correct:
        return "Correct! Great job." if lang == 'en' else "Correct ! Bravo."
    hints = {'en': question.hint_en, 'fr': question.hint_fr}
    h = hints.get(lang, '') or hints['en']
    base = ("Not quite. " if lang == 'en' else "Pas tout à fait. ")
    return base + h if h else (
        "Try again!" if lang == 'en' else "Réessaie !"
    )


# ── Parent / Guardian views ───────────────────────────────────────────────────

class ParentRegisterForm(forms.Form):
    username  = forms.CharField(min_length=2, max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=6)

    def clean_username(self):
        u = self.cleaned_data['username']
        if User.objects.filter(username__iexact=u).exists():
            raise forms.ValidationError('Username already taken.')
        return u

    def clean(self):
        cd = super().clean()
        if cd.get('password1') != cd.get('password2'):
            self.add_error('password2', 'Passwords do not match.')
        return cd


def parent_register_view(request):
    lang = request.GET.get('lang', 'en')
    if request.method == 'POST':
        form = ParentRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            ParentProfile.objects.create(user=user)
            auth_login(request, user)
            from django.urls import reverse
            return redirect(f"{reverse('quiz:parent_dashboard')}?lang={lang}")
    else:
        form = ParentRegisterForm()
    return render(request, 'quiz/parent_register.html', {'form': form, 'lang': lang})


@login_required
def parent_dashboard_view(request):
    from datetime import date, timedelta
    lang = request.GET.get('lang', 'en')
    try:
        parent = request.user.parent_profile
    except Exception:
        return redirect('quiz:index')

    children_data = []
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday

    for child_user in parent.children.select_related('student').all():
        interactions = ProblemInteraction.objects.filter(user=child_user)
        week_interactions = interactions.filter(created_at__date__gte=week_start)
        total_week = week_interactions.count()
        correct_week = week_interactions.filter(is_correct=True).count()
        stars_week = week_interactions.aggregate(s=Sum('points_earned'))['s'] or 0

        # Days active this week
        active_days = week_interactions.values('created_at__date').distinct().count()

        # Topics practiced this week
        topics_week = list(
            week_interactions.values('topic').distinct().values_list('topic', flat=True)
        )
        topic_labels = [_topic_label(t, lang) for t in topics_week[:5]]

        # 7-day daily bars
        days_7 = [today - timedelta(days=i) for i in range(6, -1, -1)]
        day_qs = (interactions.filter(created_at__date__gte=days_7[0])
                  .values('created_at__date')
                  .annotate(total=Count('id'), correct=Count('id', filter=Q(is_correct=True))))
        by_date = {r['created_at__date']: r for r in day_qs}
        daily_bars = []
        for d in days_7:
            row = by_date.get(d, {'total': 0, 'correct': 0})
            t = row['total']
            daily_bars.append({'date': d, 'total': t, 'pct': round(row['correct']/t*100) if t else 0})

        # Per-topic accuracy for this child
        topic_acc = {}
        for row in (interactions.values('topic')
                    .annotate(total=Count('id'), correct=Count('id', filter=Q(is_correct=True)))
                    .filter(total__gte=5)):
            topic_acc[row['topic']] = round(row['correct']/row['total']*100)

        # Global averages for comparison
        global_topic_acc = {}
        for row in (ProblemInteraction.objects.values('topic')
                    .annotate(total=Count('id'), correct=Count('id', filter=Q(is_correct=True)))
                    .filter(total__gte=20)):
            global_topic_acc[row['topic']] = round(row['correct']/row['total']*100)

        # Build comparison list (topics with enough data)
        comparison = []
        for topic, child_pct in topic_acc.items():
            global_pct = global_topic_acc.get(topic)
            if global_pct is not None:
                comparison.append({
                    'topic': _topic_label(topic, lang),
                    'child_pct': child_pct,
                    'global_pct': global_pct,
                    'diff': child_pct - global_pct,
                })
        comparison.sort(key=lambda x: -abs(x['diff']))

        try:
            student = child_user.student
            avatar = student.avatar_emoji()
            total_stars = student.total_stars
        except Exception:
            avatar = '🧒'
            total_stars = 0

        children_data.append({
            'username':       child_user.username,
            'user_id':        child_user.pk,
            'avatar':         avatar,
            'total_stars':    total_stars,
            'week_total':     total_week,
            'week_correct':   correct_week,
            'week_accuracy':  round(correct_week/total_week*100) if total_week else 0,
            'stars_week':     stars_week,
            'active_days':    active_days,
            'topics_week':    topic_labels,
            'daily_bars':     daily_bars,
            'comparison':     comparison[:5],
            'all_time_total': interactions.count(),
        })

    # Handle child linking
    link_error = ''
    link_success = ''
    if request.method == 'POST':
        child_username = request.POST.get('child_username', '').strip()
        try:
            child_user = User.objects.get(username__iexact=child_username)
            if hasattr(child_user, 'student'):
                parent.children.add(child_user)
                link_success = f"Linked to {child_user.username}!"
            else:
                link_error = "That account is not a student account."
        except User.DoesNotExist:
            link_error = "No student found with that username."
        return redirect(f'/parent/?lang={lang}')

    # Per-child assignments for parent dashboard display
    from .generators import TOPIC_GROUPS as TG
    all_topics = [
        {'slug': t['slug'], 'name_en': t['name_en'], 'name_fr': t['name_fr'], 'icon': g['icon']}
        for g in TG for t in g['topics']
    ]
    child_assignments = {}
    for child_user in parent.children.all():
        child_assignments[child_user.username] = list(
            ParentAssignment.objects.filter(parent=parent, student=child_user)
            .order_by('-assigned_at')
        )

    return render(request, 'quiz/parent_dashboard.html', {
        'lang':             lang,
        'children_data':    children_data,
        'child_assignments': child_assignments,
        'all_topics':       all_topics,
        'link_error':       request.GET.get('link_error', ''),
        'link_success':     request.GET.get('link_success', ''),
    })


@require_POST
@login_required
def assign_topic_view(request):
    lang = request.GET.get('lang', 'en')
    try:
        parent = request.user.parent_profile
    except Exception:
        return redirect('quiz:index')
    topic_slug = request.POST.get('topic_slug', '').strip()
    child_id   = request.POST.get('child_id', '')
    if topic_slug and child_id:
        try:
            child = User.objects.get(pk=child_id)
            if child in parent.children.all():
                ParentAssignment.objects.get_or_create(
                    parent=parent, student=child, topic_slug=topic_slug
                )
        except User.DoesNotExist:
            pass
    return redirect(f'/parent/?lang={lang}')


@require_POST
@login_required
def unassign_topic_view(request):
    lang = request.GET.get('lang', 'en')
    try:
        parent = request.user.parent_profile
    except Exception:
        return redirect('quiz:index')
    assignment_id = request.POST.get('assignment_id', '')
    if assignment_id:
        ParentAssignment.objects.filter(pk=assignment_id, parent=parent).delete()
    return redirect(f'/parent/?lang={lang}')


@require_POST
@login_required
def parent_reset_child_password_view(request):
    lang = request.GET.get('lang', 'en')
    try:
        parent = request.user.parent_profile
    except Exception:
        return redirect('quiz:index')

    child_username = request.POST.get('child_username', '').strip()
    new_password   = request.POST.get('new_password', '').strip()
    confirm        = request.POST.get('confirm_password', '').strip()

    # Verify the child belongs to this parent
    child_user = parent.children.filter(username__iexact=child_username).first()
    if not child_user:
        messages.error(request, 'Child not found or not linked to your account.')
        return redirect(f'/parent/?lang={lang}')
    if len(new_password) < 4:
        messages.error(request, 'Password must be at least 4 characters.')
        return redirect(f'/parent/?lang={lang}')
    if new_password != confirm:
        messages.error(request, 'Passwords do not match.')
        return redirect(f'/parent/?lang={lang}')

    child_user.set_password(new_password)
    child_user.save()
    messages.success(request, f"Password for {child_user.username} has been reset.")
    return redirect(f'/parent/?lang={lang}')


@require_POST
@login_required
def complete_assignment_view(request):
    from django.utils import timezone
    lang = request.GET.get('lang', 'en')
    assignment_id = request.POST.get('assignment_id', '')
    if assignment_id:
        ParentAssignment.objects.filter(
            pk=assignment_id, student=request.user
        ).update(completed_at=timezone.now())
    return redirect(f'/?lang={lang}')
