"""
Fill in Skill.description_* and keywords_* with the LLM, using a few real
generated problems per skill as grounding so the text describes what the
child actually sees.  These fields feed AI search and classification.

    python manage.py ai_enrich_skills            # only skills missing a description
    python manage.py ai_enrich_skills --all      # regenerate everything
    python manage.py ai_enrich_skills --slug add --slug g5-volume
    python manage.py ai_enrich_skills --dry-run  # print, don't save
"""
from django.core.management.base import BaseCommand, CommandError

from quiz.ai import client as llm
from quiz.generators import GENERATORS
from quiz.models import Skill

SYSTEM = """You are a curriculum editor for a Québec elementary-school math practice app (grades 3 to 6), bilingual French/English.
For each skill you receive its name, grade, domain and a few sample problems exactly as shown to the child.
Write, for each skill:
- description_en / description_fr: 1–2 sentences, concrete, describing what the exercise asks the child to do and what it looks like (numbers, shapes, format of the answer). Written for a parent.
- keywords_en / keywords_fr: 8–15 short comma-separated phrases a child or parent might type when looking for this kind of exercise, including informal wording, common misspellings-free synonyms, and Québec school vocabulary (e.g. "termes manquants", "droite numérique").
Return a JSON object: {"<slug>": {"description_en": "...", "description_fr": "...", "keywords_en": "...", "keywords_fr": "..."}, ...}"""


def _samples(slug, n=3):
    gen = GENERATORS.get(slug)
    if not gen:
        return []
    out = []
    for level in ('easy', 'medium', 'hard')[:n]:
        try:
            q = gen(level)
        except Exception:
            continue
        item = {
            'level': level,
            'q_type': q.get('q_type'),
            'prompt_fr': q.get('prompt_fr', ''),
            'prompt_en': q.get('prompt_en', ''),
        }
        if q.get('choices'):
            item['choices'] = [c.get('label') for c in q['choices']][:5]
        if q.get('correct_answers'):
            item['answers'] = q['correct_answers'][:3]
        if q.get('pairs'):
            item['pairs'] = [(p.get('left'), p.get('right')) for p in q['pairs']][:4]
        if q.get('items'):
            item['items'] = [i.get('label') for i in q['items']][:6]
        out.append(item)
    return out


class Command(BaseCommand):
    help = 'Generate skill descriptions & search keywords with the LLM.'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Regenerate even when a description exists')
        parser.add_argument('--slug', action='append', default=[], help='Only these skill slugs (repeatable)')
        parser.add_argument('--batch', type=int, default=5, help='Skills per LLM call')
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **opts):
        if not llm.is_configured():
            raise CommandError('LLM_API_KEY / DEEPSEEK_API_KEY is not set')
        qs = Skill.objects.select_related('domain').order_by('domain__order', 'order')
        if opts['slug']:
            qs = qs.filter(slug__in=opts['slug'])
        elif not opts['all']:
            qs = qs.filter(description_en='')
        skills = list(qs)
        if not skills:
            self.stdout.write('Nothing to do.')
            return
        self.stdout.write(f'Enriching {len(skills)} skill(s) with {llm.settings.LLM_MODEL} …')

        batch = max(1, opts['batch'])
        done = 0
        for i in range(0, len(skills), batch):
            chunk = skills[i:i + batch]
            payload = [{
                'slug': s.slug,
                'name_en': s.name_en, 'name_fr': s.name_fr,
                'grade': s.domain.grade or 'general',
                'domain_en': s.domain.name_en, 'domain_fr': s.domain.name_fr,
                'samples': _samples(s.slug),
            } for s in chunk]
            import json
            try:
                result = llm.complete_json(SYSTEM, json.dumps(payload, ensure_ascii=False),
                                           max_tokens=8192)
            except Exception as exc:          # keep going; report at the end
                self.stderr.write(f'  batch {i // batch + 1}: LLM error: {exc}')
                continue
            if not isinstance(result, dict):
                self.stderr.write(f'  batch {i // batch + 1}: unexpected reply shape')
                continue
            for s in chunk:
                data = result.get(s.slug)
                if not isinstance(data, dict):
                    self.stderr.write(f'  {s.slug}: missing in reply')
                    continue
                for field in ('description_en', 'description_fr', 'keywords_en', 'keywords_fr'):
                    val = (data.get(field) or '').strip()
                    if val:
                        setattr(s, field, val)
                if opts['dry_run']:
                    self.stdout.write(f'\n[{s.slug}] {s.description_fr}\n   kw: {s.keywords_fr}')
                else:
                    s.save(update_fields=['description_en', 'description_fr',
                                          'keywords_en', 'keywords_fr', 'updated_at'])
                done += 1
                self.stdout.write(f'  ✓ {s.slug}')
        self.stdout.write(self.style.SUCCESS(f'{done}/{len(skills)} skills enriched'
                                             + (' (dry run)' if opts['dry_run'] else '')))
