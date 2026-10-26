"""
vocab_reasoning_plus.py — curriculum upgrade WP10 (cross-cutting), 2026-10.

F1 · vocabulary: match a term with its meaning or its symbol, one skill per field.
F2 · « Qui a raison ? »: two children explain an answer; pick who is right and why.
Each wrong claim is a classic misconception, so the explanation teaches the fix.
"""
import random

from .kit import mc, match, pick

# ── F1 · Vocabulary ──────────────────────────────────────────────────────────
# (level, term fr, term en, meaning fr, meaning en)

VOCAB = {
    'numbers': [
        (1, 'chiffre', 'digit', 'un des signes 0, 1, 2… 9', 'one of the signs 0, 1, 2… 9'),
        (1, 'dizaine', 'ten', 'un groupe de 10 unités', 'a group of 10 ones'),
        (1, 'centaine', 'hundred', 'un groupe de 100 unités', 'a group of 100 ones'),
        (1, 'nombre pair', 'even number', 'se termine par 0, 2, 4, 6 ou 8', 'ends in 0, 2, 4, 6 or 8'),
        (1, 'nombre impair', 'odd number', 'se termine par 1, 3, 5, 7 ou 9', 'ends in 1, 3, 5, 7 or 9'),
        (2, '=', '=', 'est égal à', 'is equal to'),
        (2, '<', '<', 'est plus petit que', 'is less than'),
        (2, '>', '>', 'est plus grand que', 'is greater than'),
        (2, '≠', '≠', 'est différent de', 'is not equal to'),
        (2, 'unité de mille', 'thousand', 'un groupe de 1000 unités', 'a group of 1000 ones'),
        (3, 'valeur de position', 'place value', 'ce que vaut un chiffre selon sa place', 'what a digit is worth because of its place'),
        (3, 'régularité', 'pattern rule', 'ce qui se répète ou change toujours de la même façon', 'what repeats or always changes the same way'),
        (3, 'suite', 'sequence', 'des nombres placés dans un ordre qui suit une règle', 'numbers in an order that follows a rule'),
        (3, 'base dix', 'base ten', '10 unités font une dizaine, 10 dizaines font une centaine…', '10 ones make a ten, 10 tens make a hundred…'),
        (3, 'touche C de la calculatrice', 'calculator C key', 'efface ce qui est affiché', 'clears the display'),
    ],
    'geometry': [
        (1, 'polygone', 'polygon', 'figure fermée faite de segments', 'closed shape made of straight sides'),
        (1, 'quadrilatère', 'quadrilateral', 'polygone à 4 côtés', 'polygon with 4 sides'),
        (1, 'segment', 'line segment', 'morceau de droite entre deux points', 'piece of a line between two points'),
        (1, 'angle droit', 'right angle', 'un coin carré, comme le coin d’une feuille', 'a square corner, like the corner of a sheet of paper'),
        (1, 'cercle', 'circle', 'ligne ronde dont tous les points sont à la même distance du centre', 'round line whose points are all the same distance from the centre'),
        (1, 'ligne verticale', 'vertical line', 'ligne droite qui va de haut en bas', 'straight line that goes straight up and down'),
        (2, '//', '//', 'est parallèle à', 'is parallel to'),
        (2, '⊥', '⊥', 'est perpendiculaire à', 'is perpendicular to'),
        (2, 'parallélogramme', 'parallelogram', 'quadrilatère dont les côtés opposés sont parallèles', 'quadrilateral whose opposite sides are parallel'),
        (2, 'trapèze', 'trapezoid', 'quadrilatère avec au moins une paire de côtés parallèles', 'quadrilateral with at least one pair of parallel sides'),
        (3, 'polygone non convexe', 'concave polygon', 'polygone qui a un angle rentrant', 'polygon with a corner pointing inwards'),
        (3, 'plan cartésien', 'Cartesian plane', 'deux axes gradués pour repérer des points', 'two number lines (axes) to locate points'),
        (3, 'couple (3, 5)', 'ordered pair (3, 5)', '3 sur l’axe horizontal, puis 5 sur l’axe vertical', '3 on the horizontal axis, then 5 on the vertical axis'),
        (3, 'arête', 'edge', 'ligne où deux faces d’un solide se rencontrent', 'line where two faces of a solid meet'),
        (3, 'sommet', 'vertex', 'point où des arêtes se rencontrent', 'point where edges meet'),
    ],
    'measurement': [
        (1, 'longueur', 'length', 'combien c’est long', 'how long something is'),
        (1, 'largeur', 'width', 'combien c’est large', 'how wide something is'),
        (1, 'hauteur', 'height', 'combien c’est haut', 'how tall something is'),
        (1, 'profondeur', 'depth', 'combien c’est creux, de l’avant vers l’arrière', 'how far it goes from front to back'),
        (1, 'masse', 'mass', 'combien c’est lourd', 'how heavy something is'),
        (1, 'température', 'temperature', 'combien il fait chaud ou froid', 'how hot or cold something is'),
        (1, 'durée', 'duration', 'combien de temps ça dure', 'how much time something lasts'),
        (2, 'cm', 'cm', 'centimètre', 'centimetre'),
        (2, 'dm', 'dm', 'décimètre (10 cm)', 'decimetre (10 cm)'),
        (2, 'm', 'm', 'mètre (100 cm)', 'metre (100 cm)'),
        (2, 'mm', 'mm', 'millimètre (un dixième de cm)', 'millimetre (a tenth of a cm)'),
        (3, 'aire', 'area', 'la grandeur d’une surface', 'how much surface something covers'),
        (3, 'périmètre', 'perimeter', 'la longueur du tour d’une figure', 'the distance around a shape'),
        (3, 'volume', 'volume', 'la place qu’occupe un solide', 'how much space a solid takes up'),
        (3, 'capacité', 'capacity', 'ce qu’un contenant peut contenir', 'how much a container can hold'),
    ],
    'chance': [
        (1, 'certain', 'certain', 'arrivera à coup sûr', 'will surely happen'),
        (1, 'possible', 'possible', 'peut arriver', 'can happen'),
        (1, 'impossible', 'impossible', 'ne peut pas arriver', 'cannot happen'),
        (1, 'au hasard', 'at random', 'sans choisir et sans regarder', 'without choosing and without looking'),
        (1, 'résultat', 'outcome', 'ce qu’on obtient à la fin d’une expérience', 'what you get at the end of an experiment'),
        (2, 'hasard', 'randomness', 'on ne peut pas savoir le résultat à l’avance', 'you cannot know the result in advance'),
        (2, 'expérience aléatoire', 'random experiment', 'une expérience dont le résultat dépend du hasard', 'an experiment whose result depends on chance'),
        (2, 'également probable', 'equally likely', 'les résultats ont autant de chances', 'the outcomes have the same chance'),
        (3, 'dénombrement', 'counting outcomes', 'trouver tous les résultats possibles', 'finding all the possible outcomes'),
        (3, 'diagramme en arbre', 'tree diagram', 'un dessin avec des branches pour lister les résultats', 'a branching drawing that lists the outcomes'),
        (3, 'plus probable', 'more likely', 'a plus de chances d’arriver', 'has a better chance of happening'),
        (3, 'probabilité ½', 'probability ½', 'une chance sur deux', 'an even chance (1 in 2)'),
    ],
}
TITLES = {'numbers': ('nombres', 'numbers'), 'geometry': ('géométrie', 'geometry'),
          'measurement': ('mesure', 'measurement'), 'chance': ('hasard', 'chance')}
# One hint per field, tied to what the words are about
HINTS = {
    'numbers': ('Pense à un exemple avec de vrais nombres pour chaque mot, puis élimine.',
                'Think of an example with real numbers for each word, then eliminate.'),
    'geometry': ('Dessine chaque mot dans ta tête (ou sur une feuille) et compare avec chaque définition.',
                 'Picture each word (or sketch it) and compare it with each meaning.'),
    'measurement': ('Pense à un objet de la classe : qu’est-ce qu’on mesure avec chaque mot ?',
                    'Think of an object in the classroom: what does each word measure?'),
    'chance': ('Pense à une pièce, un dé ou un sac de billes pour chaque mot.',
               'Think of a coin, a die or a bag of marbles for each word.'),
}


def _vocab_gen(field):
    def gen(level='easy'):
        top = {'easy': 1, 'medium': 2, 'hard': 3}[level]
        pool = [v for v in VOCAB[field] if v[0] <= top]
        newest = [v for v in pool if v[0] == top]
        n = min(4, len(pool))                       # 3 pairs when a field has only 3 starter words
        chosen = random.sample(newest, min(2, len(newest)))
        rest = [v for v in pool if v not in chosen]
        chosen += random.sample(rest, n - len(chosen))
        random.shuffle(chosen)
        pairs = [((t_fr, t_en), (m_fr, m_en)) for _, t_fr, t_en, m_fr, m_en in chosen]
        t = TITLES[field]
        return match((f'Vocabulaire ({t[0]}) : associe chaque mot ou symbole à ce qu’il veut dire.',
                      f'Vocabulary ({t[1]}): match each word or symbol with its meaning.'),
                     pairs,
                     HINTS[field],
                     ([f'{a[0]} : {b[0]}' for a, b in pairs], [f'{a[1]}: {b[1]}' for a, b in pairs]))
    gen.__name__ = f'vocab_{field}_gen'
    gen.__doc__ = f'Vocabulary of {field}: term ↔ meaning/symbol (WP10).'
    return gen


vocab_numbers_gen = _vocab_gen('numbers')
vocab_geometry_gen = _vocab_gen('geometry')
vocab_measurement_gen = _vocab_gen('measurement')
vocab_chance_gen = _vocab_gen('chance')


# ── F2 · Who is right? ───────────────────────────────────────────────────────

KIDS = [('Léa', 'Tom'), ('Inès', 'Samuel'), ('Maya', 'Noah'), ('Zoé', 'Malik'), ('Rose', 'Adam')]


def _who(claim_a, claim_b, a_right, b_right, why, story, hint=None):
    """claim_x = (fr, en). Returns an MC problem with 5 mutually exclusive choices."""
    a, b = pick(KIDS)
    if random.random() < 0.5:
        a, b = b, a
    if random.random() < 0.5:                      # the right claim is not always said second
        claim_a, claim_b, a_right, b_right = claim_b, claim_a, b_right, a_right
    # « Seulement X » so that « X a raison » is not also true when both are right
    opts = [(f'Seulement {a} a raison.', f'Only {a} is right.'), (f'Seulement {b} a raison.', f'Only {b} is right.'),
            ('Les deux ont raison.', 'Both are right.'), ('Aucun des deux n’a raison.', 'Neither is right.'),
            ('On ne peut pas savoir.', 'We cannot tell.')]
    k = 2 if a_right and b_right else 0 if a_right else 1 if b_right else 3
    lead_fr, lead_en = (f'{story[0]} ' if story[0] else ''), (f'{story[1]} ' if story[1] else '')
    return mc((f'{lead_fr}{a} dit : « {claim_a[0]} » {b} dit : « {claim_b[0]} » Qui a raison ?',
               f'{lead_en}{a} says: “{claim_a[1]}” {b} says: “{claim_b[1]}” Who is right?'),
              opts[k], [o for j, o in enumerate(opts) if j != k],
              hint or ('Vérifie chaque phrase toi-même avant de choisir.', 'Check each statement yourself before choosing.'),
              why, time_limit=60)


def who_numbers_gen(level='easy'):
    """Who is right? — numbers and operations (cross-cutting reasoning)."""
    kind = pick(['place', 'order'] if level == 'easy' else ['decimal', 'order', 'fraction'] if level == 'medium' else ['decimal', 'fraction', 'times10'])
    if kind == 'place':
        n = random.randint(21, 98)
        while n % 10 in (0, n // 10):
            n = random.randint(21, 98)
        t, o = divmod(n, 10)
        return _who((f'Dans {n}, le chiffre {t} vaut {t}.', f'In {n}, the digit {t} is worth {t}.'),
                    (f'Dans {n}, le chiffre {t} vaut {t * 10}.', f'In {n}, the digit {t} is worth {t * 10}.'),
                    False, True,
                    (f'Le {t} est à la position des dizaines : il vaut {t} dizaines = {t * 10}.', f'The {t} is in the tens place: it is worth {t} tens = {t * 10}.'),
                    ('On parle de la valeur d’un chiffre.', 'We talk about the value of a digit.'),
                    ('Repère la position du chiffre : unités ou dizaines ?', 'Find the place of the digit: ones or tens?'))
    if kind == 'order':
        a, b = random.randint(21, 89), random.randint(21, 89)
        while a == b:
            b = random.randint(21, 89)
        hi, lo = max(a, b), min(a, b)
        wrong_first = random.random() < 0.5
        order_hint = ('Compare d’abord les dizaines. La pointe du signe > montre le plus petit nombre.',
                      'Compare the tens first. The point of the > sign points at the smaller number.')
        return _who((f'{lo} > {hi}', f'{lo} > {hi}'), (f'{hi} > {lo}', f'{hi} > {lo}'), False, True,
                    (f'{hi} a plus de dizaines (ou autant de dizaines et plus d’unités) : {hi} > {lo}.', f'{hi} has more tens (or the same tens and more ones): {hi} > {lo}.'),
                    ('On compare deux nombres.', 'We compare two numbers.'), order_hint) if wrong_first else \
            _who((f'{hi} > {lo}', f'{hi} > {lo}'), (f'{hi} < {lo}', f'{hi} < {lo}'), True, False,
                 (f'{hi} est plus grand : {hi} > {lo}.', f'{hi} is greater: {hi} > {lo}.'), ('On compare deux nombres.', 'We compare two numbers.'), order_hint)
    if kind == 'decimal':
        # classic misconception: « more digits means bigger » (0,45 > 0,7)
        x = random.randint(3, 9)
        y = random.randint(11, x * 10 - 1)
        while y % 10 == 0:
            y = random.randint(11, x * 10 - 1)
        big, small = f'0,{x}', f'0,{y}'
        big_en, small_en = big.replace(',', '.'), small.replace(',', '.')
        return _who((f'{small} est plus grand que {big}, car il a plus de chiffres.', f'{small_en} is greater than {big_en} because it has more digits.'),
                    (f'{big} est plus grand que {small}.', f'{big_en} is greater than {small_en}.'),
                    False, True,
                    (f'Compare les dixièmes : {x} dixièmes > {y // 10} dixième{"s" if y // 10 > 1 else ""}, donc {big} > {small}. Le nombre de chiffres ne compte pas.',
                     f'Compare the tenths: {x} tenths > {y // 10} tenth{"s" if y // 10 != 1 else ""}, so {big_en} > {small_en}. The number of digits does not matter.'),
                    ('On compare deux nombres décimaux.', 'We compare two decimals.'),
                    ('Compare d’abord les dixièmes, le premier chiffre après la virgule.', 'Compare the tenths first, the first digit after the decimal point.'))
    if kind == 'fraction':
        d = random.randint(2, 6)
        n = random.randint(1, d - 1)
        return _who((f'{n}/{d} est plus petit que {n}/{d * 2}, car {d} < {d * 2}.', f'{n}/{d} is smaller than {n}/{d * 2} because {d} < {d * 2}.'),
                    (f'{n}/{d} est plus grand que {n}/{d * 2} : les parts sont plus grosses.', f'{n}/{d} is greater than {n}/{d * 2}: the parts are bigger.'),
                    False, True,
                    (f'Même numérateur : plus le dénominateur est petit, plus les parts sont grandes. {n}/{d} > {n}/{d * 2}.',
                     f'Same numerator: the smaller the denominator, the bigger the parts. {n}/{d} > {n}/{d * 2}.'),
                    ('On compare deux fractions.', 'We compare two fractions.'),
                    ('Même numérateur : compare la taille des parts. En combien de parts coupe-t-on le tout ?',
                     'Same numerator: compare the size of the parts. Into how many parts is the whole cut?'))
    v = random.randint(2, 9) + random.choice([0.5, 0.3, 0.2])
    s, e = f'{v:g}'.replace('.', ','), f'{v:g}'
    r = f'{v * 10:g}'
    return _who((f'{s} × 10 = {s}0 : on ajoute un zéro.', f'{e} × 10 = {e}0: just add a zero.'),
                (f'{s} × 10 = {r} : chaque chiffre avance d’une position.', f'{e} × 10 = {r}: each digit moves up one place.'),
                False, True,
                (f'{s}0 vaut encore {s}. × 10 déplace les chiffres : {s} × 10 = {r}.', f'{e}0 is still {e}. × 10 moves the digits: {e} × 10 = {r}.'),
                ('On multiplie un nombre décimal par 10.', 'We multiply a decimal by 10.'),
                ('Avec × 10, chaque chiffre vaut 10 fois plus : il avance d’une position vers la gauche.',
                 'With × 10, each digit is worth 10 times more: it moves one place to the left.'))


def who_geometry_gen(level='easy'):
    """Who is right? — shapes and measures (cross-cutting reasoning)."""
    items = [
        (1, ('Un carré est aussi un rectangle.', 'A square is also a rectangle.'),
         ('Un carré n’est jamais un rectangle.', 'A square is never a rectangle.'), True, False,
         ('Un carré a 4 angles droits, comme tout rectangle : c’est un rectangle spécial.', 'A square has 4 right angles like every rectangle: it is a special rectangle.'),
         ('On parle des quadrilatères.', 'We are talking about quadrilaterals.'),
         ('Qu’est-ce qu’il faut pour être un rectangle ? Compte les angles droits du carré.', 'What does a shape need to be a rectangle? Count the right angles of a square.')),
        (1, ('Un triangle qu’on a fait tourner n’est plus un triangle.', 'A rotated triangle is no longer a triangle.'),
         ('Il a toujours 3 côtés : c’est encore un triangle.', 'It still has 3 sides: it is still a triangle.'), False, True,
         ('Faire tourner une figure ne change ni ses côtés ni ses angles.', 'Rotating a shape does not change its sides or angles.'),
         ('On fait tourner un triangle.', 'We rotate a triangle.'),
         ('Imagine un triangle en carton que tu fais tourner : combien de côtés a-t-il encore ?', 'Picture a cardboard triangle that you rotate: how many sides does it still have?')),
        (2, ('Plus les côtés d’un angle sont longs, plus l’angle est grand.', 'The longer the arms, the bigger the angle.'),
         ('La taille d’un angle dépend de son ouverture, pas de la longueur des côtés.', 'An angle’s size depends on how wide it opens, not on arm length.'), False, True,
         ('On mesure l’ouverture : allonger les côtés ne change pas l’angle.', 'We measure the opening: longer arms do not change the angle.'),
         ('On parle de la mesure des angles.', 'We talk about how angles are measured.'),
         ('Imagine une porte qui s’ouvre : est-ce la longueur de la porte ou son ouverture qui fait l’angle ?', 'Picture a door opening: is the angle made by the length of the door or by how wide it opens?')),
        (2, ('Un cube a 6 faces.', 'A cube has 6 faces.'), ('Un cube a 8 sommets.', 'A cube has 8 vertices.'), True, True,
         ('Les deux phrases sont vraies : 6 faces, 8 sommets, 12 arêtes.', 'Both are true: 6 faces, 8 vertices, 12 edges.'),
         ('On décrit un cube.', 'We describe a cube.'),
         ('Imagine un dé : compte ses faces, puis ses sommets (les coins).', 'Picture a die: count its faces, then its vertices (corners).')),
        (3, ('Deux figures qui ont le même périmètre ont la même aire.', 'Two shapes with the same perimeter have the same area.'),
         ('Un rectangle 1 × 5 et un carré 3 × 3 ont le même périmètre mais pas la même aire.', 'A 1 × 5 rectangle and a 3 × 3 square have the same perimeter but different areas.'), False, True,
         ('Périmètres : 12 et 12. Aires : 5 et 9. Même périmètre ne veut pas dire même aire.', 'Perimeters: 12 and 12. Areas: 5 and 9. Same perimeter does not mean same area.'),
         ('On compare l’aire et le périmètre.', 'We compare area and perimeter.'),
         ('Calcule le périmètre et l’aire des deux figures, puis compare.', 'Work out the perimeter and the area of both shapes, then compare.')),
        (3, ('1 m² = 100 cm²', '1 m² = 100 cm²'), ('1 m² = 10 000 cm²', '1 m² = 10,000 cm²'), False, True,
         ('Un carré de 1 m de côté mesure 100 cm × 100 cm = 10 000 cm².', 'A square 1 m wide is 100 cm × 100 cm = 10,000 cm².'),
         ('On convertit une aire.', 'We convert an area.'),
         ('Dessine un carré de 1 m de côté : combien de centimètres mesure chaque côté ?', 'Picture a square 1 m wide: how many centimetres long is each side?')),
        (3, ('Le diamètre est deux fois le rayon.', 'The diameter is twice the radius.'), ('Le rayon est la moitié du diamètre.', 'The radius is half the diameter.'), True, True,
         ('Les deux disent la même chose : d = 2 × r.', 'Both say the same thing: d = 2 × r.'), ('On parle du cercle.', 'We talk about the circle.'),
         ('Le diamètre traverse tout le cercle ; le rayon va du centre au bord.', 'The diameter goes right across the circle; the radius goes from the centre to the edge.')),
    ]
    top = {'easy': 1, 'medium': 2, 'hard': 3}[level]
    _, ca, cb, ra, rb, why, story, hint = pick([it for it in items if it[0] <= top and it[0] >= top - 1])
    return _who(ca, cb, ra, rb, why, story, hint)


def who_data_gen(level='easy'):
    """Who is right? — data and chance (cross-cutting reasoning)."""
    k = random.randint(3, 6)
    items = [
        # « pile » = tails, « face » = heads
        (1, ('Si la pièce donne pile 3 fois, face doit sortir au prochain lancer.', 'After 3 tails, heads must come next.'),
         ('Pile et face ont toujours autant de chances.', 'Heads and tails always have the same chance.'), False, True,
         ('La pièce ne se souvient pas des lancers précédents.', 'The coin does not remember earlier tosses.'),
         ('On lance une pièce de monnaie équilibrée.', 'We toss a fair coin.'),
         ('Une pièce peut-elle se souvenir de ce qu’elle a donné avant ?', 'Can a coin remember what it gave before?')),
        (1, ('Tirer une bille verte de ce sac est impossible.', 'Picking a green marble from this bag is impossible.'),
         ('Tirer une bille verte de ce sac est peu probable, mais possible.', 'Picking a green marble from this bag is unlikely but possible.'), True, False,
         ('Il n’y a aucune bille verte dans le sac : c’est impossible.', 'There is no green marble in the bag: it is impossible.'),
         ('Un sac ne contient que des billes rouges.', 'A bag holds only red marbles.'),
         ('Y a-t-il au moins une bille verte dans le sac ?', 'Is there at least one green marble in the bag?')),
        (2, ('Sur ce dé, le 6 est plus difficile à obtenir que le 2.', 'On this die, 6 is harder to roll than 2.'),
         ('Chaque face a 1 chance sur 6.', 'Each face has a 1 in 6 chance.'), False, True,
         ('Un dé équilibré donne la même chance à chaque face : 1 chance sur 6.', 'A fair die gives every face the same chance: 1 in 6.'),
         ('On lance un dé équilibré à 6 faces.', 'We roll a fair six-sided die.'),
         ('Combien de faces a le dé ? Chacune a-t-elle la même chance ?', 'How many faces does the die have? Does each one have the same chance?')),
        (2, ('Dans le diagramme, la bande la plus haute montre la réponse la plus choisie.', 'In the bar chart, the tallest bar shows the most chosen answer.'),
         ('La bande la plus large montre la réponse la plus choisie.', 'The widest bar shows the most chosen answer.'), True, False,
         ('C’est la hauteur de la bande qui donne le nombre, pas sa largeur.', 'The height of the bar gives the number, not its width.'),
         ('On lit un diagramme à bandes.', 'We read a bar chart.'),
         ('Sur quel axe lit-on le nombre de réponses ?', 'On which axis do you read the number of answers?')),
        (3, ('La moyenne de 2, 4 et 9 est 5.', 'The mean of 2, 4 and 9 is 5.'), ('La moyenne de 2, 4 et 9 est 4, le nombre du milieu.', 'The mean of 2, 4 and 9 is 4, the middle number.'), True, False,
         ('Moyenne = (2 + 4 + 9) ÷ 3 = 15 ÷ 3 = 5. Le nombre du milieu n’est pas la moyenne.', 'Mean = (2 + 4 + 9) ÷ 3 = 15 ÷ 3 = 5. The middle number is not the mean.'),
         ('On calcule une moyenne.', 'We work out a mean.'),
         ('Pour la moyenne, additionne toutes les valeurs, puis divise par leur nombre.', 'For the mean, add all the values, then divide by how many there are.')),
        (3, ('Avec 1000 lancers, la fréquence de pile sera proche de ½.', 'With 1000 tosses, the share of tails will be close to ½.'),
         ('Avec 10 lancers, on aura toujours exactement 5 piles.', 'With 10 tosses you always get exactly 5 tails.'), True, False,
         ('Beaucoup d’essais → proche de ½ ; peu d’essais → les résultats varient.', 'Many trials → close to ½; few trials → results vary.'),
         ('On lance une pièce de monnaie équilibrée.', 'We toss a fair coin.'),
         ('Avec peu de lancers, le hasard fait beaucoup varier les résultats ; avec beaucoup de lancers, moins.', 'With few tosses chance makes results vary a lot; with many tosses, less.')),
    ]
    top = {'easy': 1, 'medium': 2, 'hard': 3}[level]
    _, ca, cb, ra, rb, why, story, hint = pick([it for it in items if top - 1 <= it[0] <= top])
    return _who(ca, cb, ra, rb, why, story, hint)
