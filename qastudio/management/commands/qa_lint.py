"""
Lint report over fresh samples, without touching the review queues.

    python manage.py qa_lint                     # 8 samples per skill and level, every skill
    python manage.py qa_lint --samples 30 --errors-only
    python manage.py qa_lint --skill g5-data-table --show 5
    python manage.py qa_lint --markdown report.md
"""
import collections

from django.core.management.base import BaseCommand

from quiz.generators import GENERATORS
from quiz.models import Skill
from qastudio import sampling
from qastudio.lint import RULES, lint_payload


class Command(BaseCommand):
    help = 'Run the automated QA rules on generated samples and print a ranked report (nothing is saved).'

    def add_arguments(self, parser):
        parser.add_argument('--samples', type=int, default=8, help='samples per skill and level (default 8)')
        parser.add_argument('--skill', action='append', default=[], help='only this skill slug (repeatable)')
        parser.add_argument('--errors-only', action='store_true')
        parser.add_argument('--show', type=int, default=1, help='example messages per (skill, rule)')
        parser.add_argument('--markdown', help='also write the report to this Markdown file')

    def handle(self, *args, **opts):
        skills = {s.slug: s for s in Skill.objects.select_related('domain')}
        slugs = opts['skill'] or sorted(GENERATORS)
        hits = collections.defaultdict(lambda: {'n': 0, 'severity': 'warn', 'examples': []})
        total = 0
        for slug in slugs:
            skill = skills.get(slug)
            levels = sampling.levels_for(skill) if skill else sampling.DEFAULT_LEVELS
            for level in levels:
                for seed in range(1, opts['samples'] + 1):
                    total += 1
                    try:
                        payload = sampling.generate(slug, level, seed)
                    except Exception as exc:
                        h = hits[(slug, 'CRASH')]
                        h['n'] += 1
                        h['severity'] = 'error'
                        if len(h['examples']) < opts['show']:
                            h['examples'].append(f'{level} seed {seed}: {exc.__class__.__name__}: {exc}')
                        continue
                    for f in lint_payload(payload, slug):
                        if opts['errors_only'] and f['severity'] != 'error':
                            continue
                        h = hits[(slug, f['rule'])]
                        h['n'] += 1
                        if f['severity'] == 'error':
                            h['severity'] = 'error'
                        if len(h['examples']) < opts['show']:
                            h['examples'].append(f"{level} seed {seed} [{f['lang']}]: {f['message']}")

        by_skill = collections.defaultdict(list)
        for (slug, rule), h in hits.items():
            by_skill[slug].append((rule, h))
        ranked = sorted(by_skill.items(),
                        key=lambda kv: (-sum(h['n'] for r, h in kv[1] if h['severity'] == 'error'),
                                        -sum(h['n'] for r, h in kv[1])))
        lines = [f'# QA lint report — {total} samples, {len(slugs)} skills, {len(ranked)} skills with findings', '']
        for slug, items in ranked:
            name = skills[slug].name_fr if slug in skills else slug
            n_err = sum(h['n'] for r, h in items if h['severity'] == 'error')
            lines.append(f'## {slug} — {name} ({n_err} error hits)')
            for rule, h in sorted(items, key=lambda x: (x[1]['severity'] != 'error', x[0])):
                label = RULES.get(rule, ('', 'generator crashed'))[1]
                lines.append(f"- **{rule}** {h['severity']} ×{h['n']} — {label}")
                for e in h['examples']:
                    lines.append(f'  - {e}')
            lines.append('')
        report = '\n'.join(lines)
        self.stdout.write(report)
        if opts['markdown']:
            with open(opts['markdown'], 'w', encoding='utf-8') as fh:
                fh.write(report)
