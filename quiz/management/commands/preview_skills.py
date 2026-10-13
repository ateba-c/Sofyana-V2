"""
Content-review gallery: render sample problems of some skills to one HTML page
(and optionally a PNG through headless Chrome/Edge) to eyeball prompts + pictures.

    python manage.py preview_skills g3-ruler-mm g6-protractor --lang fr --png out.png
    python manage.py preview_skills --prefix g1- --samples 3
"""
import html
import random
import shutil
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from quiz.generators import GENERATORS, SKILL_MAP, generator_for
from quiz.labels import localize_problem
from quiz.templatetags.quiz_extras import shape_canvas

BROWSERS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    'google-chrome', 'chromium', 'chromium-browser',
]


class Command(BaseCommand):
    help = 'Render sample problems of the given skills into an HTML (and PNG) gallery.'

    def add_arguments(self, parser):
        parser.add_argument('slugs', nargs='*')
        parser.add_argument('--prefix', default='')
        parser.add_argument('--lang', default='fr')
        parser.add_argument('--samples', type=int, default=2)
        parser.add_argument('--seed', type=int, default=None)
        parser.add_argument('--out', default='skill_preview.html')
        parser.add_argument('--png', default='')
        parser.add_argument('--width', type=int, default=1400)

    def handle(self, *args, **o):
        if o['seed'] is not None:
            random.seed(o['seed'])
        slugs = list(o['slugs']) + [s for s in GENERATORS if o['prefix'] and s.startswith(o['prefix'])]
        cards = []
        for slug in slugs:
            for level in SKILL_MAP.get(slug, {}).get('level_sequence', ['easy', 'medium', 'hard']):
                gen = generator_for(slug, level)
                for _ in range(o['samples']):
                    q = gen() if level == 'resolution' else gen(level)
                    q = localize_problem(q, o['lang'])
                    cards.append(self._card(slug, level, q, o['lang']))
        page = ('<!doctype html><meta charset="utf-8"><script src="https://cdn.tailwindcss.com"></script>'
                '<style>body{font-family:Nunito,system-ui;margin:12px;background:#F8FAFC}'
                '.g{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}'
                '.c{background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:8px;font-size:12px}'
                '.c svg{max-width:100%}.h{font-weight:800;color:#6366F1}.a{color:#16A34A;font-weight:700}</style>'
                f'<div class="g">{"".join(cards)}</div>')
        Path(o['out']).write_text(page, encoding='utf-8')
        self.stdout.write(f'{len(cards)} cards -> {o["out"]}')
        if o['png']:
            self._shot(Path(o['out']).resolve(), o['png'], o['width'], len(cards))

    def _card(self, slug, level, q, lang):
        pic = render_to_string('partials/shape_canvas.html', shape_canvas(q.get('shape_data') or [], lang)) \
            if q.get('shape_data') else ''
        opts = ''
        if q.get('choices'):
            opts = ' · '.join(('✔' if c['correct'] else '') + html.escape(str(c['label'])) for c in q['choices'])
        elif q.get('pairs'):
            opts = ' · '.join(f"{html.escape(str(p['left']))}→{html.escape(str(p['right']))}" for p in q['pairs'])
        elif q.get('items'):
            opts = ' < '.join(html.escape(str(i['label'])) for i in sorted(q['items'], key=lambda i: i['order']))
        prompt = q.get(f'prompt_{lang}') or q.get('prompt_fr', '')
        return (f'<div class="c"><div class="h">{slug} · {level} · {q["q_type"]}</div>'
                f'<div>{html.escape(prompt)}</div>{pic}<div>{opts}</div>'
                f'<div class="a">= {html.escape(", ".join(map(str, q.get("correct_answers", []))))}</div></div>')

    def _shot(self, page, png, width, n):
        exe = next((b for b in BROWSERS if Path(b).exists() or shutil.which(b)), None)
        if not exe:
            self.stderr.write('No Chrome/Edge found for --png')
            return
        height = 260 * ((n + 3) // 4) + 60
        subprocess.run([exe, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        f'--window-size={width},{height}', f'--screenshot={Path(png).resolve()}',
                        '--virtual-time-budget=4000', page.as_uri()],
                       check=False, capture_output=True, timeout=90)
        self.stdout.write(f'PNG -> {png}')
