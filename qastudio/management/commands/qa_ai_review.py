"""
AI pre-review of the QA Studio samples (advisory; never changes statuses).

    python manage.py qa_ai_review                       # every skill: new/changed samples + generator diagnosis
    python manage.py qa_ai_review --skill even-odd --skill g5-data-table
    python manage.py qa_ai_review --grade 5 --workers 6
    python manage.py qa_ai_review --max-skills 10       # try it on a few skills first
    python manage.py qa_ai_review --force               # re-analyse even samples the AI has already seen

Only samples whose current output hasn't been analysed are sent, so re-running is cheap.
"""
import time

from django.core.management.base import BaseCommand, CommandError

from quiz.models import Skill
from qastudio import ai_review
from qastudio.models import QuestionSample


class Command(BaseCommand):
    help = 'AI pre-review of QA Studio samples (solve without the key, judge the 6 criteria, diagnose generators).'

    def add_arguments(self, parser):
        parser.add_argument('--skill', action='append', default=[], help='only this skill slug (repeatable)')
        parser.add_argument('--grade', type=int, action='append', default=[], help='only skills of this grade')
        parser.add_argument('--max-skills', type=int, default=0, help='stop after this many skills (0 = all)')
        parser.add_argument('--workers', type=int, default=4, help='parallel LLM calls (default 4)')
        parser.add_argument('--force', action='store_true', help='re-analyse samples already reviewed by the AI')
        parser.add_argument('--no-diagnosis', action='store_true', help='skip the per-skill generator diagnosis')

    def handle(self, *args, **opts):
        if not ai_review.is_enabled():
            raise CommandError('No LLM key configured (DEEPSEEK_API_KEY / LLM_API_KEY).')
        ai_review.expire_stale_pending()
        skills = Skill.objects.filter(is_active=True, qa_samples__isnull=False).distinct().select_related('domain')
        if opts['skill']:
            skills = skills.filter(slug__in=opts['skill'])
        if opts['grade']:
            skills = skills.filter(domain__grade__in=opts['grade'])
        skills = list(skills.order_by('domain__grade', 'order'))
        if opts['max_skills']:
            skills = skills[:opts['max_skills']]
        self.stdout.write(f'Model {ai_review.model_name()} · {len(skills)} skill(s) · {opts["workers"]} workers')
        t0 = time.time()
        stats = {'clean': 0, 'minor': 0, 'major': 0, 'error': 0}

        def progress(skill, reviews, exc):
            if exc is not None:
                self.stderr.write(f'  {skill.slug}: FAILED ({exc.__class__.__name__}: {exc})')
                return
            counts = {}
            for r in reviews.values():
                counts[r['verdict']] = counts.get(r['verdict'], 0) + 1
                stats[r['verdict']] = stats.get(r['verdict'], 0) + 1
            line = ', '.join(f'{v} {k}' for k, v in sorted(counts.items())) or 'diagnosis only'
            self.stdout.write(f'  {skill.slug}: {line}  ({time.time() - t0:.0f}s)')

        done, total = ai_review.run_skills(skills, workers=opts['workers'], force=opts['force'],
                                           with_diagnosis=not opts['no_diagnosis'], progress=progress)
        self.stdout.write(self.style.SUCCESS(
            f'{done}/{total} skill(s) analysed in {time.time() - t0:.0f}s — '
            f"{stats['major']} major, {stats['minor']} minor, {stats['clean']} clean, {stats['error']} failed."))
        waiting = QuestionSample.objects.filter(status=QuestionSample.UNREVIEWED).count()
        self.stdout.write(f'{waiting} samples still waiting for a human decision (the AI never decides).')
