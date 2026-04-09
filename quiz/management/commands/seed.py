"""python manage.py seed — populates demo quiz data"""
from django.core.management.base import BaseCommand
from quiz.models import QuizSet, Question, Choice, Pair


class Command(BaseCommand):
    help = 'Seed demo quiz data'

    def handle(self, *args, **options):
        QuizSet.objects.all().delete()

        quiz = QuizSet.objects.create(
            title_en='Science & Nature — Demo',
            title_fr='Sciences & Nature — Démo',
            description_en='A bilingual showcase of every question type.',
            description_fr='Une vitrine bilingue de chaque type de question.',
        )

        # ── 1. Multiple Choice (5 options) ───────────────────────────
        q1 = Question.objects.create(
            quiz_set=quiz, order=1, q_type='multiple_choice',
            prompt_en='Which planet is closest to the Sun?',
            prompt_fr='Quelle planète est la plus proche du Soleil ?',
            hint_en='It is the smallest planet in our solar system.',
            hint_fr="C'est la plus petite planète du système solaire.",
            illustration_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Mercury_in_true_color.jpg/240px-Mercury_in_true_color.jpg',
            time_limit=20, points=10,
        )
        for i, (en, fr, ok) in enumerate([
            ('Mercury', 'Mercure', True),
            ('Venus',   'Vénus',   False),
            ('Earth',   'Terre',   False),
            ('Mars',    'Mars',    False),
            ('Jupiter', 'Jupiter', False),
        ], 1):
            Choice.objects.create(question=q1, label_en=en, label_fr=fr,
                                  is_correct=ok, order=i)

        # ── 2. Text Input ─────────────────────────────────────────────
        q2 = Question.objects.create(
            quiz_set=quiz, order=2, q_type='text_input',
            prompt_en='What is the chemical symbol for water?',
            prompt_fr="Quel est le symbole chimique de l'eau ?",
            hint_en='Two hydrogen atoms, one oxygen atom.',
            hint_fr="Deux atomes d'hydrogène, un atome d'oxygène.",
            illustration_url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/24701-nature-natural-beauty.jpg/320px-24701-nature-natural-beauty.jpg',
            time_limit=15, points=10,
        )
        Choice.objects.create(question=q2, label_en='H2O', label_fr='H2O',
                              is_correct=True, order=1)

        # ── 3. Drag & Drop — sort 5 planets by size (largest first) ──
        q3 = Question.objects.create(
            quiz_set=quiz, order=3, q_type='drag_drop',
            prompt_en='Drag to sort: place the largest planet first, smallest last.',
            prompt_fr='Glissez pour trier : la plus grande planète en premier, la plus petite en dernier.',
            hint_en='Jupiter is the giant; Mercury is the smallest.',
            hint_fr='Jupiter est le plus grand ; Mercure est le plus petit.',
            time_limit=35, points=15,
        )
        for i, (en, fr) in enumerate([
            ('Jupiter', 'Jupiter'),
            ('Saturn',  'Saturne'),
            ('Uranus',  'Uranus'),
            ('Neptune', 'Neptune'),
            ('Earth',   'Terre'),
        ], 1):
            Choice.objects.create(question=q3, label_en=en, label_fr=fr,
                                  order=i, is_correct=True)

        # ── 4. Connect Many-to-Many (5 pairs) ─────────────────────────
        q4 = Question.objects.create(
            quiz_set=quiz, order=4, q_type='connect',
            prompt_en='Match each planet to its number of known moons.',
            prompt_fr='Associez chaque planète à son nombre de lunes connues.',
            hint_en='Saturn holds the record with over 140 moons.',
            hint_fr='Saturne détient le record avec plus de 140 lunes.',
            time_limit=45, points=20,
        )
        for i, (left, left_fr, right, right_fr) in enumerate([
            ('Earth',   'Terre',   '1',   '1'),
            ('Mars',    'Mars',    '2',   '2'),
            ('Uranus',  'Uranus',  '28',  '28'),
            ('Jupiter', 'Jupiter', '95',  '95'),
            ('Saturn',  'Saturne', '146', '146'),
        ], 1):
            Pair.objects.create(question=q4, left_en=left, left_fr=left_fr,
                                right_en=right, right_fr=right_fr, order=i)

        # ── 5. Mix & Match (5 pairs) ───────────────────────────────────
        q5 = Question.objects.create(
            quiz_set=quiz, order=5, q_type='mix_match',
            prompt_en='Match each scientist to their most famous discovery.',
            prompt_fr='Associez chaque scientifique à sa découverte la plus célèbre.',
            hint_en='Think gravity, penicillin, relativity, radioactivity, evolution.',
            hint_fr='Pensez gravité, pénicilline, relativité, radioactivité, évolution.',
            time_limit=45, points=20,
        )
        for i, (left, left_fr, right, right_fr) in enumerate([
            ('Newton',   'Newton',   'Gravity',        'Gravité'),
            ('Fleming',  'Fleming',  'Penicillin',      'Pénicilline'),
            ('Einstein', 'Einstein', 'Relativity',      'Relativité'),
            ('Curie',    'Curie',    'Radioactivity',   'Radioactivité'),
            ('Darwin',   'Darwin',   'Evolution',       'Évolution'),
        ], 1):
            Pair.objects.create(question=q5, left_en=left, left_fr=left_fr,
                                right_en=right, right_fr=right_fr, order=i)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded quiz "{quiz.title_en}" with {quiz.questions.count()} questions.'
        ))

        self._seed_geometry()

    # ── Geometry quiz ──────────────────────────────────────────────────────────
    def _seed_geometry(self):
        geo = QuizSet.objects.create(
            title_en='Geometry Playground',
            title_fr='Terrain de jeu — Géométrie',
            description_en='Shapes, areas, perimeters, and more — every question type.',
            description_fr='Formes, aires, périmètres et plus — tous les types de questions.',
        )

        # ── Q1: Single rectangle — find the area (text input) ───────────────
        q1 = Question.objects.create(
            quiz_set=geo, order=1, q_type='text_input',
            prompt_en='What is the area of this rectangle? (give a number)',
            prompt_fr='Quelle est l\'aire de ce rectangle ? (donnez un nombre)',
            hint_en='Area = width × height',
            hint_fr='Aire = largeur × hauteur',
            shape_data=[{
                'type': 'rectangle', 'width': 8, 'height': 5,
                'labels': {'w': '8 cm', 'h': '5 cm', 'inner': 'A = ?'}
            }],
            time_limit=25, points=10,
        )
        Choice.objects.create(question=q1, label_en='40', label_fr='40', is_correct=True)

        # ── Q2: Right triangle — identify it (multiple choice, 5 options) ───
        q2 = Question.objects.create(
            quiz_set=geo, order=2, q_type='multiple_choice',
            prompt_en='What type of triangle is this?',
            prompt_fr='Quel type de triangle est-ce ?',
            hint_en='One angle is exactly 90°.',
            hint_fr='Un angle est exactement 90°.',
            shape_data=[{
                'type': 'right_triangle', 'a': 3, 'b': 4,
                'labels': {'a': '3', 'b': '4', 'c': '5'}
            }],
            time_limit=20, points=10,
        )
        for i, (en, fr, ok) in enumerate([
            ('Right triangle',        'Triangle rectangle',       True),
            ('Equilateral triangle',  'Triangle équilatéral',     False),
            ('Isosceles triangle',    'Triangle isocèle',         False),
            ('Scalene triangle',      'Triangle scalène',         False),
            ('Obtuse triangle',       'Triangle obtus',           False),
        ], 1):
            Choice.objects.create(question=q2, label_en=en, label_fr=fr,
                                  is_correct=ok, order=i)

        # ── Q3: Circle — find the area (multiple choice) ─────────────────────
        q3 = Question.objects.create(
            quiz_set=geo, order=3, q_type='multiple_choice',
            prompt_en='What is the area of this circle? (use π)',
            prompt_fr='Quelle est l\'aire de ce cercle ? (utilisez π)',
            hint_en='Area of a circle = π × r²',
            hint_fr='Aire d\'un cercle = π × r²',
            shape_data=[{
                'type': 'circle', 'radius': 7,
                'labels': {'r': 'r = 7 cm'}
            }],
            time_limit=25, points=10,
        )
        for i, (en, fr, ok) in enumerate([
            ('49π cm²',  '49π cm²',  True),
            ('14π cm²',  '14π cm²',  False),
            ('98π cm²',  '98π cm²',  False),
            ('7π cm²',   '7π cm²',   False),
            ('28π cm²',  '28π cm²',  False),
        ], 1):
            Choice.objects.create(question=q3, label_en=en, label_fr=fr,
                                  is_correct=ok, order=i)

        # ── Q4: Two similar rectangles — which has the bigger area? (MC) ────
        q4 = Question.objects.create(
            quiz_set=geo, order=4, q_type='multiple_choice',
            prompt_en='Shape A and Shape B — which one has the greater area?',
            prompt_fr='Forme A et Forme B — laquelle a la plus grande aire ?',
            hint_en='Compute A = w × h for each.',
            hint_fr='Calculez A = l × h pour chacune.',
            shape_data=[
                {'type': 'rectangle', 'width': 6, 'height': 4,
                 'title': 'Shape A', 'labels': {'w': '6', 'h': '4'}},
                {'type': 'rectangle', 'width': 3, 'height': 9,
                 'title': 'Shape B', 'labels': {'w': '3', 'h': '9'}},
            ],
            time_limit=30, points=10,
        )
        for i, (en, fr, ok) in enumerate([
            ('Shape A',              'Forme A',               False),
            ('Shape B',              'Forme B',               True),
            ('They are equal',       'Elles sont égales',     False),
            ('Cannot be determined', 'Impossible à déterminer', False),
        ], 1):
            Choice.objects.create(question=q4, label_en=en, label_fr=fr,
                                  is_correct=ok, order=i)

        # ── Q5: Three dissimilar shapes — drag to sort by area asc ──────────
        q5 = Question.objects.create(
            quiz_set=geo, order=5, q_type='drag_drop',
            prompt_en='Drag to rank these shapes: smallest area first.',
            prompt_fr='Glissez pour classer ces formes : la plus petite aire en premier.',
            hint_en='Rectangle 4×3=12, Equilateral s=6≈15.6, Parallelogram 8×2=16.',
            hint_fr='Rectangle 4×3=12, Équilatéral c=6≈15.6, Parallélogramme 8×2=16.',
            shape_data=[
                {'type': 'rectangle',           'width': 4, 'height': 3,
                 'title': 'A', 'labels': {'w': '4', 'h': '3'}},
                {'type': 'equilateral_triangle', 'side': 6,
                 'title': 'B', 'labels': {'side': '6'}},
                {'type': 'parallelogram',        'base': 8, 'height': 2,
                 'title': 'C', 'labels': {'base': '8', 'h': '2'}},
            ],
            time_limit=40, points=15,
        )
        for i, (en, fr) in enumerate([
            ('Shape A',   'Forme A'),
            ('Shape B',   'Forme B'),
            ('Shape C',   'Forme C'),
        ], 1):
            Choice.objects.create(question=q5, label_en=en, label_fr=fr,
                                  is_correct=True, order=i)

        # ── Q6: Connect shape label to its area formula ───────────────────
        q6 = Question.objects.create(
            quiz_set=geo, order=6, q_type='connect',
            prompt_en='Shapes A–D are shown above. Match each to its area formula.',
            prompt_fr='Les formes A–D sont affichées ci-dessus. Associez chacune à sa formule d\'aire.',
            hint_en='Think: b×h, ½b×h, π r², ½(a+b)×h.',
            hint_fr='Pensez : b×h, ½b×h, π r², ½(a+b)×h.',
            shape_data=[
                {'type': 'rectangle',   'width': 5, 'height': 3,
                 'title': 'A', 'labels': {'w': '5', 'h': '3'}},
                {'type': 'right_triangle', 'a': 4, 'b': 3,
                 'title': 'B', 'labels': {'a': '4', 'b': '3', 'c': '5'}},
                {'type': 'circle',      'radius': 4,
                 'title': 'C', 'labels': {'r': 'r = 4'}},
                {'type': 'trapezoid',   'top': 3, 'bottom': 7, 'height': 4,
                 'title': 'D', 'labels': {'top': '3', 'bottom': '7', 'h': '4'}},
            ],
            time_limit=50, points=20,
        )
        for i, (l_en, l_fr, r_en, r_fr) in enumerate([
            ('Shape A', 'Forme A', 'b × h',         'b × h'),
            ('Shape B', 'Forme B', '½ × b × h',     '½ × b × h'),
            ('Shape C', 'Forme C', 'π × r²',        'π × r²'),
            ('Shape D', 'Forme D', '½ × (a+b) × h', '½ × (a+b) × h'),
        ], 1):
            Pair.objects.create(question=q6, left_en=l_en, left_fr=l_fr,
                                right_en=r_en, right_fr=r_fr, order=i)

        # ── Q7: Four shapes — mix & match to their names ─────────────────────
        q7 = Question.objects.create(
            quiz_set=geo, order=7, q_type='mix_match',
            prompt_en='Match each shape (A–D) to its correct name.',
            prompt_fr='Associez chaque forme (A–D) à son nom correct.',
            hint_en='Look at the number of sides and their properties.',
            hint_fr='Regardez le nombre de côtés et leurs propriétés.',
            shape_data=[
                {'type': 'equilateral_triangle', 'side': 5,
                 'title': 'A', 'labels': {'side': '5'}},
                {'type': 'parallelogram', 'base': 6, 'height': 3,
                 'title': 'B', 'labels': {'base': '6', 'h': '3'}},
                {'type': 'trapezoid', 'top': 3, 'bottom': 6, 'height': 3,
                 'title': 'C', 'labels': {'top': '3', 'bottom': '6', 'h': '3'}},
                {'type': 'isosceles_triangle', 'base': 6, 'height': 5,
                 'title': 'D', 'labels': {'base': '6', 'h': '5'}},
            ],
            time_limit=35, points=15,
        )
        for i, (l_en, l_fr, r_en, r_fr) in enumerate([
            ('Shape A', 'Forme A', 'Equilateral Triangle', 'Triangle équilatéral'),
            ('Shape B', 'Forme B', 'Parallelogram',        'Parallélogramme'),
            ('Shape C', 'Forme C', 'Trapezoid',            'Trapèze'),
            ('Shape D', 'Forme D', 'Isosceles Triangle',   'Triangle isocèle'),
        ], 1):
            Pair.objects.create(question=q7, left_en=l_en, left_fr=l_fr,
                                right_en=r_en, right_fr=r_fr, order=i)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded quiz "{geo.title_en}" with {geo.questions.count()} questions.'
        ))

        self._seed_arithmetic()
        self._seed_decimals()

    # ── helpers ────────────────────────────────────────────────────────────────

    @staticmethod
    def _expr(op1, operator, op2, result='?', fmt='horizontal'):
        return [{'type': 'expression', 'op1': str(op1),
                 'operator': operator, 'op2': str(op2),
                 'result': str(result), 'format': fmt}]

    # ── Arithmetic A / D / M / S ───────────────────────────────────────────────
    def _seed_arithmetic(self):
        quiz = QuizSet.objects.create(
            title_en='Arithmetic — + - x div',
            title_fr='Arithmétique — + - x div',
            description_en='Addition, subtraction, multiplication and division.',
            description_fr='Addition, soustraction, multiplication et division.',
        )
        E = self._expr   # shorthand

        # ── Addition ──────────────────────────────────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=1, q_type='text_input',
            prompt_en='Calculate the sum.',
            prompt_fr='Calculez la somme.',
            hint_en='Line up the digits and add column by column.',
            hint_fr='Alignez les chiffres et additionnez colonne par colonne.',
            shape_data=E(246, '+', 379), time_limit=30, points=10,
        )
        Choice.objects.create(question=q, label_en='625', label_fr='625', is_correct=True)

        q = Question.objects.create(
            quiz_set=quiz, order=2, q_type='multiple_choice',
            prompt_en='Choose the correct sum.',
            prompt_fr='Choisissez la bonne somme.',
            hint_en='1 048 + 523 — watch the carries.',
            hint_fr='1 048 + 523 — attention aux retenues.',
            shape_data=E(1048, '+', 523, fmt='vertical'), time_limit=25, points=10,
        )
        for i, (en, ok) in enumerate([
            ('1 571', True), ('1 471', False), ('1 671', False),
            ('1 561', False), ('1 581', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Subtraction ───────────────────────────────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=3, q_type='text_input',
            prompt_en='Calculate the difference.',
            prompt_fr='Calculez la différence.',
            hint_en='You may need to borrow from the next column.',
            hint_fr='Vous devrez peut-être emprunter à la colonne suivante.',
            shape_data=E(1000, '−', 347), time_limit=30, points=10,
        )
        Choice.objects.create(question=q, label_en='653', label_fr='653', is_correct=True)

        q = Question.objects.create(
            quiz_set=quiz, order=4, q_type='multiple_choice',
            prompt_en='Choose the correct difference.',
            prompt_fr='Choisissez la bonne différence.',
            hint_en='5 004 − 2 887 — subtract, borrowing where needed.',
            hint_fr='5 004 − 2 887 — soustrayez en empruntant si nécessaire.',
            shape_data=E(5004, '−', 2887, fmt='vertical'), time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('2 117', True), ('2 217', False), ('2 107', False),
            ('3 117', False), ('2 127', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Multiplication ────────────────────────────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=5, q_type='text_input',
            prompt_en='Calculate the product.',
            prompt_fr='Calculez le produit.',
            hint_en='24 × 8 — multiply each digit of 24 by 8.',
            hint_fr='24 × 8 — multipliez chaque chiffre de 24 par 8.',
            shape_data=E(24, '×', 8, fmt='vertical'), time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='192', label_fr='192', is_correct=True)

        q = Question.objects.create(
            quiz_set=quiz, order=6, q_type='multiple_choice',
            prompt_en='Choose the correct product.',
            prompt_fr='Choisissez le bon produit.',
            hint_en='35 × 12 = 35 × 10 + 35 × 2.',
            hint_fr='35 × 12 = 35 × 10 + 35 × 2.',
            shape_data=E(35, '×', 12, fmt='vertical'), time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('420', True), ('360', False), ('400', False),
            ('385', False), ('432', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Division ──────────────────────────────────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=7, q_type='text_input',
            prompt_en='Calculate the quotient.',
            prompt_fr='Calculez le quotient.',
            hint_en='144 ÷ 12 — how many 12s fit in 144?',
            hint_fr='144 ÷ 12 — combien de fois 12 va dans 144 ?',
            shape_data=E(144, '÷', 12), time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='12', label_fr='12', is_correct=True)

        q = Question.objects.create(
            quiz_set=quiz, order=8, q_type='multiple_choice',
            prompt_en='Choose the correct quotient.',
            prompt_fr='Choisissez le bon quotient.',
            hint_en='504 ÷ 7 — how many 7s fit in 504?',
            hint_fr='504 ÷ 7 — combien de fois 7 va dans 504 ?',
            shape_data=E(504, '÷', 7), time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('72', True), ('63', False), ('81', False),
            ('68', False), ('78', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Identify the operation (mix & match) ─────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=9, q_type='mix_match',
            prompt_en='Match each expression to the correct operation name.',
            prompt_fr='Associez chaque expression à son nom d\'opération.',
            hint_en='Look at the symbol between the numbers.',
            hint_fr='Regardez le symbole entre les nombres.',
            shape_data=[
                {'type': 'expression', 'op1': '12', 'operator': '+',
                 'op2': '8',  'result': '20', 'format': 'horizontal', 'title': 'A'},
                {'type': 'expression', 'op1': '20', 'operator': '−',
                 'op2': '8',  'result': '12', 'format': 'horizontal', 'title': 'B'},
                {'type': 'expression', 'op1': '4',  'operator': '×',
                 'op2': '5',  'result': '20', 'format': 'horizontal', 'title': 'C'},
                {'type': 'expression', 'op1': '20', 'operator': '÷',
                 'op2': '4',  'result': '5',  'format': 'horizontal', 'title': 'D'},
            ],
            time_limit=30, points=15,
        )
        for i, (l_en, l_fr, r_en, r_fr) in enumerate([
            ('A', 'A', 'Addition',       'Addition'),
            ('B', 'B', 'Subtraction',    'Soustraction'),
            ('C', 'C', 'Multiplication', 'Multiplication'),
            ('D', 'D', 'Division',       'Division'),
        ], 1):
            Pair.objects.create(question=q, left_en=l_en, left_fr=l_fr,
                                right_en=r_en, right_fr=r_fr, order=i)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded quiz "{quiz.title_en}" with {quiz.questions.count()} questions.'
        ))

    # ── Decimal Arithmetic ─────────────────────────────────────────────────────
    def _seed_decimals(self):
        quiz = QuizSet.objects.create(
            title_en='Decimal Arithmetic',
            title_fr='Arithmétique décimale',
            description_en='Add, subtract, multiply and divide with decimal numbers.',
            description_fr='Additionner, soustraire, multiplier et diviser des décimaux.',
        )
        E = self._expr

        # ── Decimal addition ──────────────────────────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=1, q_type='text_input',
            prompt_en='Calculate the sum.',
            prompt_fr='Calculez la somme.',
            hint_en='Line up the decimal points first.',
            hint_fr='Alignez d\'abord la virgule décimale.',
            shape_data=E('3.5', '+', '2.7'), time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='6.2', label_fr='6.2', is_correct=True)

        q = Question.objects.create(
            quiz_set=quiz, order=2, q_type='multiple_choice',
            prompt_en='Choose the correct sum.',
            prompt_fr='Choisissez la bonne somme.',
            hint_en='12.48 + 7.6 — align the decimal points.',
            hint_fr='12.48 + 7.6 — alignez les virgules.',
            shape_data=E('12.48', '+', '7.6', fmt='vertical'), time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('20.08', True), ('19.08', False), ('20.18', False),
            ('19.48', False), ('20.8', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Decimal subtraction ───────────────────────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=3, q_type='text_input',
            prompt_en='Calculate the difference.',
            prompt_fr='Calculez la différence.',
            hint_en='10.0 − 3.6 — align decimal points and borrow if needed.',
            hint_fr='10.0 − 3.6 — alignez et empruntez si nécessaire.',
            shape_data=E('10.0', '−', '3.6'), time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='6.4', label_fr='6.4', is_correct=True)

        q = Question.objects.create(
            quiz_set=quiz, order=4, q_type='multiple_choice',
            prompt_en='Choose the correct difference.',
            prompt_fr='Choisissez la bonne différence.',
            hint_en='8.05 − 2.7 — remember to align the decimal points.',
            hint_fr='8.05 − 2.7 — alignez bien les virgules.',
            shape_data=E('8.05', '−', '2.7', fmt='vertical'), time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('5.35', True), ('5.45', False), ('6.35', False),
            ('5.25', False), ('5.3', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Decimal multiplication ────────────────────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=5, q_type='text_input',
            prompt_en='Calculate the product.',
            prompt_fr='Calculez le produit.',
            hint_en='0.4 × 6 — think of it as 4 × 6 = 24, then shift the decimal.',
            hint_fr='0.4 × 6 — pensez à 4 × 6 = 24 puis déplacez la virgule.',
            shape_data=E('0.4', '×', '6'), time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='2.4', label_fr='2.4', is_correct=True)

        q = Question.objects.create(
            quiz_set=quiz, order=6, q_type='multiple_choice',
            prompt_en='Choose the correct product.',
            prompt_fr='Choisissez le bon produit.',
            hint_en='1.5 × 2.4 — count decimal places: 1 + 1 = 2 total.',
            hint_fr='1.5 × 2.4 — comptez les décimales : 1 + 1 = 2 au total.',
            shape_data=E('1.5', '×', '2.4', fmt='vertical'), time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('3.6', True), ('3.06', False), ('36.0', False),
            ('0.36', False), ('3.16', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Decimal division ──────────────────────────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=7, q_type='text_input',
            prompt_en='Calculate the quotient.',
            prompt_fr='Calculez le quotient.',
            hint_en='8.4 ÷ 4 — how many 4s fit in 8.4?',
            hint_fr='8.4 ÷ 4 — combien de fois 4 va dans 8.4 ?',
            shape_data=E('8.4', '÷', '4'), time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='2.1', label_fr='2.1', is_correct=True)

        q = Question.objects.create(
            quiz_set=quiz, order=8, q_type='multiple_choice',
            prompt_en='Choose the correct quotient.',
            prompt_fr='Choisissez le bon quotient.',
            hint_en='7.2 ÷ 0.9 — multiply both by 10: 72 ÷ 9.',
            hint_fr='7.2 ÷ 0.9 — multipliez par 10 : 72 ÷ 9.',
            shape_data=E('7.2', '÷', '0.9'), time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('8', True), ('0.8', False), ('80', False),
            ('7.2', False), ('9', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Drag to sort: order decimals smallest → largest ───────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=9, q_type='drag_drop',
            prompt_en='Drag to sort these decimals from smallest to largest.',
            prompt_fr='Glissez pour trier ces décimaux du plus petit au plus grand.',
            hint_en='Compare digit by digit from left to right after the decimal point.',
            hint_fr='Comparez chiffre par chiffre de gauche à droite après la virgule.',
            shape_data=[],   # no shape — pure text drag
            time_limit=35, points=15,
        )
        for i, (en, fr) in enumerate([
            ('0.35', '0,35'), ('0.4', '0,4'),
            ('0.75', '0,75'), ('0.8', '0,8'), ('1.02', '1,02'),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=fr,
                                  is_correct=True, order=i)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded quiz "{quiz.title_en}" with {quiz.questions.count()} questions.'
        ))

        self._seed_fractions()

    # ── Fraction Arithmetic ────────────────────────────────────────────────────
    def _seed_fractions(self):
        quiz = QuizSet.objects.create(
            title_en='Fraction Arithmetic',
            title_fr='Arithmétique des fractions',
            description_en='Add, subtract, multiply and divide fractions.',
            description_fr='Additionner, soustraire, multiplier et diviser des fractions.',
        )
        F = self._frac

        # ── Q1: Same-denominator addition (text_input) ───────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=1, q_type='text_input',
            prompt_en='Calculate the sum. Write your answer as a fraction (e.g. 3/4).',
            prompt_fr='Calculez la somme. Écrivez votre réponse sous forme de fraction (ex: 3/4).',
            hint_en='Same denominator — just add the numerators.',
            hint_fr='Même dénominateur — additionnez juste les numérateurs.',
            shape_data=F({'num': 1, 'den': 4}, '+', {'num': 2, 'den': 4}),
            time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='3/4', label_fr='3/4', is_correct=True)

        # ── Q2: Different-denominator addition (multiple choice) ─────────────
        q = Question.objects.create(
            quiz_set=quiz, order=2, q_type='multiple_choice',
            prompt_en='Choose the correct sum.',
            prompt_fr='Choisissez la bonne somme.',
            hint_en='Find a common denominator: 2 and 3 share 6.',
            hint_fr='Trouvez un dénominateur commun : 2 et 3 donnent 6.',
            shape_data=F({'num': 1, 'den': 2}, '+', {'num': 1, 'den': 3}),
            time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('5/6', True), ('2/5', False), ('2/6', False), ('1/6', False), ('3/5', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Q3: Same-denominator subtraction (text_input) ────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=3, q_type='text_input',
            prompt_en='Calculate the difference. Simplify if possible.',
            prompt_fr='Calculez la différence. Simplifiez si possible.',
            hint_en='Same denominator — subtract numerators, then simplify.',
            hint_fr='Même dénominateur — soustrayez les numérateurs, puis simplifiez.',
            shape_data=F({'num': 3, 'den': 4}, '−', {'num': 1, 'den': 4}),
            time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='1/2', label_fr='1/2', is_correct=True)
        Choice.objects.create(question=q, label_en='2/4', label_fr='2/4', is_correct=True)

        # ── Q4: Different-denominator subtraction (multiple choice) ──────────
        q = Question.objects.create(
            quiz_set=quiz, order=4, q_type='multiple_choice',
            prompt_en='Choose the correct difference.',
            prompt_fr='Choisissez la bonne différence.',
            hint_en='Common denominator of 6 and 3 is 6. Convert 1/3 to 2/6.',
            hint_fr='Dénominateur commun de 6 et 3 est 6. Convertissez 1/3 en 2/6.',
            shape_data=F({'num': 5, 'den': 6}, '−', {'num': 1, 'den': 3}),
            time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('1/2', True), ('4/3', False), ('3/6', False), ('2/3', False), ('4/6', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Q5: Fraction multiplication (text_input) ─────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=5, q_type='text_input',
            prompt_en='Calculate the product. Simplify your answer.',
            prompt_fr='Calculez le produit. Simplifiez votre réponse.',
            hint_en='Multiply numerators together, then denominators. Simplify.',
            hint_fr='Multipliez les numérateurs ensemble, puis les dénominateurs. Simplifiez.',
            shape_data=F({'num': 2, 'den': 3}, '×', {'num': 3, 'den': 4}),
            time_limit=30, points=10,
        )
        Choice.objects.create(question=q, label_en='1/2', label_fr='1/2', is_correct=True)
        Choice.objects.create(question=q, label_en='6/12', label_fr='6/12', is_correct=True)

        # ── Q6: Fraction division (multiple choice) ───────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=6, q_type='multiple_choice',
            prompt_en='Choose the correct quotient.',
            prompt_fr='Choisissez le bon quotient.',
            hint_en='Dividing by a fraction = multiplying by its reciprocal.',
            hint_fr='Diviser par une fraction = multiplier par son inverse.',
            shape_data=F({'num': 3, 'den': 4}, '÷', {'num': 1, 'den': 2}),
            time_limit=30, points=10,
        )
        for i, (en, ok) in enumerate([
            ('3/2', True), ('3/8', False), ('2/3', False), ('4/3', False), ('6/4', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Q7: Mixed number addition (multiple choice) ───────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=7, q_type='multiple_choice',
            prompt_en='Choose the correct sum.',
            prompt_fr='Choisissez la bonne somme.',
            hint_en='Add whole numbers separately, then add the fractions.',
            hint_fr='Additionnez les entiers séparément, puis les fractions.',
            shape_data=F({'whole': 1, 'num': 1, 'den': 2}, '+',
                         {'whole': 2, 'num': 1, 'den': 4}),
            time_limit=35, points=10,
        )
        for i, (en, ok) in enumerate([
            ('3 3/4', True), ('3 1/2', False), ('4 1/4', False),
            ('3 1/4', False), ('4 3/4', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── Q8: Simplify a fraction (text_input) ──────────────────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=8, q_type='text_input',
            prompt_en='Simplify the fraction. Write your answer as a fraction (e.g. 3/4).',
            prompt_fr='Simplifiez la fraction. Écrivez sous forme de fraction (ex: 3/4).',
            hint_en='Find the GCD of 6 and 8, then divide both by it.',
            hint_fr='Trouvez le PGCD de 6 et 8, puis divisez les deux par ce nombre.',
            shape_data=[{'type': 'fraction_expr',
                         'op1': {'num': 6, 'den': 8},
                         'operator': '=',
                         'result': {'num': '?', 'den': '?'},
                         'format': 'simplify'}],
            time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='3/4', label_fr='3/4', is_correct=True)

        # ── Q9: Sort fractions smallest to largest (drag_drop) ────────────────
        q = Question.objects.create(
            quiz_set=quiz, order=9, q_type='drag_drop',
            prompt_en='Drag to sort these fractions from smallest to largest.',
            prompt_fr='Glissez pour trier ces fractions du plus petit au plus grand.',
            hint_en='Convert to a common denominator, then compare numerators.',
            hint_fr='Convertissez au même dénominateur, puis comparez les numérateurs.',
            shape_data=[],
            time_limit=40, points=15,
        )
        for i, (en, fr) in enumerate([
            ('1/6', '1/6'), ('1/4', '1/4'), ('1/3', '1/3'), ('1/2', '1/2'), ('2/3', '2/3'),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=fr,
                                  is_correct=True, order=i)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded quiz "{quiz.title_en}" with {quiz.questions.count()} questions.'
        ))

        self._seed_units()

    # ── Metric Conversions ─────────────────────────────────────────────────────
    def _seed_units(self):
        quiz = QuizSet.objects.create(
            title_en='Metric Conversions',
            title_fr='Conversions métriques',
            description_en='Length, mass and volume: converting across the kilo-to-milli scale.',
            description_fr='Longueur, masse et volume : conversions de kilo en milli.',
        )

        # ── LENGTH ──────────────────────────────────────────────────────────────

        # Q1 — km → m  (text_input)
        q = Question.objects.create(
            quiz_set=quiz, order=1, q_type='text_input',
            prompt_en='Convert 3.5 km to metres.',
            prompt_fr='Convertissez 3,5 km en mètres.',
            hint_en='1 km = 1 000 m — multiply by 1 000.',
            hint_fr='1 km = 1 000 m — multipliez par 1 000.',
            shape_data=self._conv('3.5 km', 'm'),
            time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='3500', label_fr='3500', is_correct=True)

        # Q2 — cm → m  (multiple choice)
        q = Question.objects.create(
            quiz_set=quiz, order=2, q_type='multiple_choice',
            prompt_en='250 cm is equal to how many metres?',
            prompt_fr='250 cm équivaut à combien de mètres ?',
            hint_en='1 m = 100 cm — divide by 100.',
            hint_fr='1 m = 100 cm — divisez par 100.',
            shape_data=self._conv('250 cm', 'm'),
            time_limit=25, points=10,
        )
        for i, (en, ok) in enumerate([
            ('2.5 m', True), ('25 m', False), ('0.25 m', False),
            ('2 500 m', False), ('0.025 m', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # Q3 — mm → cm  (text_input)
        q = Question.objects.create(
            quiz_set=quiz, order=3, q_type='text_input',
            prompt_en='Convert 45 mm to centimetres.',
            prompt_fr='Convertissez 45 mm en centimètres.',
            hint_en='1 cm = 10 mm — divide by 10.',
            hint_fr='1 cm = 10 mm — divisez par 10.',
            shape_data=self._conv('45 mm', 'cm'),
            time_limit=20, points=10,
        )
        Choice.objects.create(question=q, label_en='4.5', label_fr='4,5', is_correct=True)
        Choice.objects.create(question=q, label_en='4,5', label_fr='4,5', is_correct=True)

        # Q4 — m → mm  (multiple choice)
        q = Question.objects.create(
            quiz_set=quiz, order=4, q_type='multiple_choice',
            prompt_en='2.4 m is equal to how many millimetres?',
            prompt_fr='2,4 m équivaut à combien de millimètres ?',
            hint_en='1 m = 1 000 mm — multiply by 1 000.',
            hint_fr='1 m = 1 000 mm — multipliez par 1 000.',
            shape_data=self._conv('2.4 m', 'mm'),
            time_limit=25, points=10,
        )
        for i, (en, ok) in enumerate([
            ('2 400 mm', True), ('240 mm', False), ('24 000 mm', False),
            ('24 mm', False), ('2.4 mm', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── MASS ────────────────────────────────────────────────────────────────

        # Q5 — kg → g  (text_input)
        q = Question.objects.create(
            quiz_set=quiz, order=5, q_type='text_input',
            prompt_en='Convert 2.5 kg to grams.',
            prompt_fr='Convertissez 2,5 kg en grammes.',
            hint_en='1 kg = 1 000 g — multiply by 1 000.',
            hint_fr='1 kg = 1 000 g — multipliez par 1 000.',
            shape_data=self._conv('2.5 kg', 'g'),
            time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='2500', label_fr='2500', is_correct=True)

        # Q6 — mg → g  (multiple choice)
        q = Question.objects.create(
            quiz_set=quiz, order=6, q_type='multiple_choice',
            prompt_en='650 mg is equal to how many grams?',
            prompt_fr='650 mg équivaut à combien de grammes ?',
            hint_en='1 g = 1 000 mg — divide by 1 000.',
            hint_fr='1 g = 1 000 mg — divisez par 1 000.',
            shape_data=self._conv('650 mg', 'g'),
            time_limit=25, points=10,
        )
        for i, (en, ok) in enumerate([
            ('0.65 g', True), ('6.5 g', False), ('65 g', False),
            ('0.065 g', False), ('6 500 g', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── VOLUME ──────────────────────────────────────────────────────────────

        # Q7 — L → mL  (text_input)
        q = Question.objects.create(
            quiz_set=quiz, order=7, q_type='text_input',
            prompt_en='Convert 4 L to millilitres.',
            prompt_fr='Convertissez 4 L en millilitres.',
            hint_en='1 L = 1 000 mL — multiply by 1 000.',
            hint_fr='1 L = 1 000 mL — multipliez par 1 000.',
            shape_data=self._conv('4 L', 'mL'),
            time_limit=20, points=10,
        )
        Choice.objects.create(question=q, label_en='4000', label_fr='4000', is_correct=True)

        # Q8 — mL → L  (multiple choice)
        q = Question.objects.create(
            quiz_set=quiz, order=8, q_type='multiple_choice',
            prompt_en='7 500 mL is equal to how many litres?',
            prompt_fr='7 500 mL équivaut à combien de litres ?',
            hint_en='1 L = 1 000 mL — divide by 1 000.',
            hint_fr='1 L = 1 000 mL — divisez par 1 000.',
            shape_data=self._conv('7 500 mL', 'L'),
            time_limit=25, points=10,
        )
        for i, (en, ok) in enumerate([
            ('7.5 L', True), ('75 L', False), ('0.75 L', False),
            ('750 L', False), ('7 500 L', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # ── SORT & MATCH ────────────────────────────────────────────────────────

        # Q9 — drag_drop: sort length units smallest → largest
        q = Question.objects.create(
            quiz_set=quiz, order=9, q_type='drag_drop',
            prompt_en='Drag to sort these units of length from smallest to largest.',
            prompt_fr='Glissez pour trier ces unités de longueur de la plus petite à la plus grande.',
            hint_en='1 km = 1 000 m = 100 000 cm = 1 000 000 mm.',
            hint_fr='1 km = 1 000 m = 100 000 cm = 1 000 000 mm.',
            shape_data=[],
            time_limit=30, points=10,
        )
        for i, (en, fr) in enumerate([
            ('mm', 'mm'), ('cm', 'cm'), ('m', 'm'), ('km', 'km'),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=fr,
                                  is_correct=True, order=i)

        # Q10 — connect: match each unit to its base-unit equivalent
        q = Question.objects.create(
            quiz_set=quiz, order=10, q_type='connect',
            prompt_en='Match each unit to its equivalent in the base unit.',
            prompt_fr='Associez chaque unité à son équivalent en unité de base.',
            hint_en='kilo = × 1 000, centi = ÷ 100, milli = ÷ 1 000.',
            hint_fr='kilo = × 1 000, centi = ÷ 100, milli = ÷ 1 000.',
            shape_data=[],
            time_limit=45, points=20,
        )
        for i, (l_en, l_fr, r_en, r_fr) in enumerate([
            ('1 km',  '1 km',  '1 000 m',    '1 000 m'),
            ('1 m',   '1 m',   '100 cm',      '100 cm'),
            ('1 cm',  '1 cm',  '10 mm',       '10 mm'),
            ('1 kg',  '1 kg',  '1 000 g',     '1 000 g'),
            ('1 L',   '1 L',   '1 000 mL',    '1 000 mL'),
        ], 1):
            Pair.objects.create(question=q, left_en=l_en, left_fr=l_fr,
                                right_en=r_en, right_fr=r_fr, order=i)

        # Q11 — mix_match: match metric prefix to its meaning
        q = Question.objects.create(
            quiz_set=quiz, order=11, q_type='mix_match',
            prompt_en='Match each metric prefix to its meaning.',
            prompt_fr='Associez chaque préfixe métrique à sa signification.',
            hint_en='kilo = thousand, hecto = hundred, deci = tenth, centi = hundredth, milli = thousandth.',
            hint_fr='kilo = mille, hecto = cent, déci = dixième, centi = centième, milli = millième.',
            shape_data=[],
            time_limit=35, points=15,
        )
        for i, (l_en, l_fr, r_en, r_fr) in enumerate([
            ('kilo-',  'kilo-',  '× 1 000', '× 1 000'),
            ('hecto-', 'hecto-', '× 100',   '× 100'),
            ('deci-',  'déci-',  '÷ 10',    '÷ 10'),
            ('centi-', 'centi-', '÷ 100',   '÷ 100'),
            ('milli-', 'milli-', '÷ 1 000', '÷ 1 000'),
        ], 1):
            Pair.objects.create(question=q, left_en=l_en, left_fr=l_fr,
                                right_en=r_en, right_fr=r_fr, order=i)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded quiz "{quiz.title_en}" with {quiz.questions.count()} questions.'
        ))

        self._seed_comparisons()

    # ── Number Comparisons ─────────────────────────────────────────────────────
    def _seed_comparisons(self):
        quiz = QuizSet.objects.create(
            title_en='Comparing Numbers',
            title_fr='Comparer des nombres',
            description_en='Integers, decimals, fractions — and mixing all three.',
            description_fr='Entiers, décimaux, fractions — et les trois ensemble.',
        )
        C = self._cmp

        # ══ INTEGERS ══════════════════════════════════════════════════════════

        # Q1 — MC: 47 □ 74
        q = Question.objects.create(
            quiz_set=quiz, order=1, q_type='multiple_choice',
            prompt_en='Which symbol correctly compares these two numbers?',
            prompt_fr='Quel symbole compare correctement ces deux nombres ?',
            hint_en='47 is less than 74 — which symbol shows that?',
            hint_fr='47 est inférieur à 74 — quel symbole l\'indique ?',
            shape_data=C('47', '74'),
            time_limit=20, points=10,
        )
        for i, (en, ok) in enumerate([
            ('<', True), ('>', False), ('=', False), ('≥', False), ('≤', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # Q2 — text_input: -3 □ -8
        q = Question.objects.create(
            quiz_set=quiz, order=2, q_type='text_input',
            prompt_en='Type >, < or = to compare these integers.',
            prompt_fr='Tapez >, < ou = pour comparer ces entiers.',
            hint_en='-3 is to the right of -8 on the number line.',
            hint_fr='-3 est à droite de -8 sur la droite numérique.',
            shape_data=C('-3', '-8'),
            time_limit=20, points=10,
        )
        Choice.objects.create(question=q, label_en='>', label_fr='>', is_correct=True)

        # Q3 — MC: 0 □ -1
        q = Question.objects.create(
            quiz_set=quiz, order=3, q_type='multiple_choice',
            prompt_en='Which symbol correctly compares these two numbers?',
            prompt_fr='Quel symbole compare correctement ces deux nombres ?',
            hint_en='Zero is always greater than any negative number.',
            hint_fr='Zéro est toujours supérieur à tout nombre négatif.',
            shape_data=C('0', '-1'),
            time_limit=20, points=10,
        )
        for i, (en, ok) in enumerate([
            ('>', True), ('<', False), ('=', False), ('≤', False), ('≥', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # Q4 — drag_drop: sort integers -5, -1, 0, 4, 12 (smallest first)
        q = Question.objects.create(
            quiz_set=quiz, order=4, q_type='drag_drop',
            prompt_en='Drag to sort these integers from smallest to largest.',
            prompt_fr='Glissez pour trier ces entiers du plus petit au plus grand.',
            hint_en='Negative numbers are to the left of zero on the number line.',
            hint_fr='Les nombres négatifs sont à gauche du zéro sur la droite numérique.',
            shape_data=[],
            time_limit=30, points=10,
        )
        for i, label in enumerate(['-5', '-1', '0', '4', '12'], 1):
            Choice.objects.create(question=q, label_en=label, label_fr=label,
                                  is_correct=True, order=i)

        # ══ DECIMALS ══════════════════════════════════════════════════════════

        # Q5 — text_input: 3.14 □ 3.41
        q = Question.objects.create(
            quiz_set=quiz, order=5, q_type='text_input',
            prompt_en='Type >, < or = to compare these decimals.',
            prompt_fr='Tapez >, < ou = pour comparer ces décimaux.',
            hint_en='Compare tenths first: 3.1_ vs 3.4_ — which tenths digit is larger?',
            hint_fr='Comparez d\'abord les dixièmes : 3,1_ vs 3,4_ — quel chiffre des dixièmes est plus grand ?',
            shape_data=C('3.14', '3.41'),
            time_limit=20, points=10,
        )
        Choice.objects.create(question=q, label_en='<', label_fr='<', is_correct=True)

        # Q6 — MC: 0.7 □ 0.70
        q = Question.objects.create(
            quiz_set=quiz, order=6, q_type='multiple_choice',
            prompt_en='Which symbol correctly compares these two decimals?',
            prompt_fr='Quel symbole compare correctement ces deux décimaux ?',
            hint_en='Trailing zeros after the decimal point do not change the value.',
            hint_fr='Les zéros après la virgule ne changent pas la valeur.',
            shape_data=C('0.7', '0.70'),
            time_limit=20, points=10,
        )
        for i, (en, ok) in enumerate([
            ('=', True), ('<', False), ('>', False), ('≠', False), ('≤', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # Q7 — drag_drop: sort decimals 0.09, 0.1, 0.9, 1.01 (smallest first)
        q = Question.objects.create(
            quiz_set=quiz, order=7, q_type='drag_drop',
            prompt_en='Drag to sort these decimals from smallest to largest.',
            prompt_fr='Glissez pour trier ces décimaux du plus petit au plus grand.',
            hint_en='0.09 < 0.1 — compare digit by digit from left to right.',
            hint_fr='0,09 < 0,1 — comparez chiffre par chiffre de gauche à droite.',
            shape_data=[],
            time_limit=30, points=10,
        )
        for i, label in enumerate(['0.09', '0.1', '0.9', '1.01'], 1):
            Choice.objects.create(question=q, label_en=label, label_fr=label,
                                  is_correct=True, order=i)

        # ══ FRACTIONS ═════════════════════════════════════════════════════════

        # Q8 — MC: 1/2 □ 2/3
        q = Question.objects.create(
            quiz_set=quiz, order=8, q_type='multiple_choice',
            prompt_en='Which symbol correctly compares these two fractions?',
            prompt_fr='Quel symbole compare correctement ces deux fractions ?',
            hint_en='Cross-multiply: 1×3=3 vs 2×2=4. Which is smaller?',
            hint_fr='Produit en croix : 1×3=3 vs 2×2=4. Lequel est plus petit ?',
            shape_data=C({'num': 1, 'den': 2}, {'num': 2, 'den': 3}),
            time_limit=25, points=10,
        )
        for i, (en, ok) in enumerate([
            ('<', True), ('>', False), ('=', False), ('≥', False), ('≤', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # Q9 — text_input: 3/4 □ 6/8
        q = Question.objects.create(
            quiz_set=quiz, order=9, q_type='text_input',
            prompt_en='Type >, < or = to compare these fractions.',
            prompt_fr='Tapez >, < ou = pour comparer ces fractions.',
            hint_en='Simplify 6/8 — divide both by 2.',
            hint_fr='Simplifiez 6/8 — divisez les deux par 2.',
            shape_data=C({'num': 3, 'den': 4}, {'num': 6, 'den': 8}),
            time_limit=25, points=10,
        )
        Choice.objects.create(question=q, label_en='=', label_fr='=', is_correct=True)

        # Q10 — drag_drop: sort fractions 1/4, 1/3, 1/2, 3/4 (smallest first)
        q = Question.objects.create(
            quiz_set=quiz, order=10, q_type='drag_drop',
            prompt_en='Drag to sort these fractions from smallest to largest.',
            prompt_fr='Glissez pour trier ces fractions du plus petit au plus grand.',
            hint_en='Same numerator: bigger denominator = smaller fraction.',
            hint_fr='Même numérateur : plus grand dénominateur = fraction plus petite.',
            shape_data=[],
            time_limit=35, points=10,
        )
        for i, label in enumerate(['1/4', '1/3', '1/2', '3/4'], 1):
            Choice.objects.create(question=q, label_en=label, label_fr=label,
                                  is_correct=True, order=i)

        # ══ MIXED (integers, decimals, fractions) ═════════════════════════════

        # Q11 — MC: 0.5 □ 1/2
        q = Question.objects.create(
            quiz_set=quiz, order=11, q_type='multiple_choice',
            prompt_en='Which symbol correctly compares these two numbers?',
            prompt_fr='Quel symbole compare correctement ces deux nombres ?',
            hint_en='Convert: 1/2 = 0.5. Are they the same?',
            hint_fr='Convertissez : 1/2 = 0,5. Sont-ils identiques ?',
            shape_data=C('0.5', {'num': 1, 'den': 2}),
            time_limit=25, points=15,
        )
        for i, (en, ok) in enumerate([
            ('=', True), ('<', False), ('>', False), ('≤', False), ('≥', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # Q12 — MC: 3/4 □ 0.8
        q = Question.objects.create(
            quiz_set=quiz, order=12, q_type='multiple_choice',
            prompt_en='Which symbol correctly compares these two numbers?',
            prompt_fr='Quel symbole compare correctement ces deux nombres ?',
            hint_en='Convert 3/4 to a decimal: 3 ÷ 4 = 0.75. Compare 0.75 and 0.8.',
            hint_fr='Convertissez 3/4 en décimal : 3 ÷ 4 = 0,75. Comparez 0,75 et 0,8.',
            shape_data=C({'num': 3, 'den': 4}, '0.8'),
            time_limit=25, points=15,
        )
        for i, (en, ok) in enumerate([
            ('<', True), ('>', False), ('=', False), ('≤', False), ('≥', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # Q13 — MC: 1.25 □ 5/4
        q = Question.objects.create(
            quiz_set=quiz, order=13, q_type='multiple_choice',
            prompt_en='Which symbol correctly compares these two numbers?',
            prompt_fr='Quel symbole compare correctement ces deux nombres ?',
            hint_en='5/4 = 1.25. They represent the same value.',
            hint_fr='5/4 = 1,25. Ils représentent la même valeur.',
            shape_data=C('1.25', {'num': 5, 'den': 4}),
            time_limit=25, points=15,
        )
        for i, (en, ok) in enumerate([
            ('=', True), ('<', False), ('>', False), ('≤', False), ('≥', False),
        ], 1):
            Choice.objects.create(question=q, label_en=en, label_fr=en, is_correct=ok, order=i)

        # Q14 — drag_drop: sort mixed 1/4, 0.3, 1/3, 0.5 (smallest first)
        q = Question.objects.create(
            quiz_set=quiz, order=14, q_type='drag_drop',
            prompt_en='Drag to sort these numbers from smallest to largest.',
            prompt_fr='Glissez pour trier ces nombres du plus petit au plus grand.',
            hint_en='Convert all to decimals: 1/4=0.25, 1/3≈0.333.',
            hint_fr='Convertissez en décimaux : 1/4=0,25, 1/3≈0,333.',
            shape_data=[],
            time_limit=40, points=15,
        )
        for i, label in enumerate(['1/4', '0.3', '1/3', '0.5'], 1):
            Choice.objects.create(question=q, label_en=label, label_fr=label,
                                  is_correct=True, order=i)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded quiz "{quiz.title_en}" with {quiz.questions.count()} questions.'
        ))

    @staticmethod
    def _cmp(op1, op2, symbol='□'):
        """Display a comparison A □ B using fraction_expr compare format."""
        return [{'type': 'fraction_expr',
                 'op1': op1, 'operator': symbol, 'op2': op2,
                 'format': 'compare'}]

    @staticmethod
    def _conv(_from_val, _to_unit):
        """No canvas for conversion questions — the text prompt is sufficient."""
        return []

    @staticmethod
    def _frac(op1, operator, op2, result=None, fmt='operation', title=''):
        if result is None:
            result = {'num': '?', 'den': '?'}
        return [{'type': 'fraction_expr', 'op1': op1, 'operator': operator,
                 'op2': op2, 'result': result, 'format': fmt, 'title': title}]
