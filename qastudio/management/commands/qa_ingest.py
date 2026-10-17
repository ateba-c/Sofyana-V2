from django.core.management.base import BaseCommand

from quiz.models import Skill
from qastudio import services
from qastudio.models import QuestionSample


class Command(BaseCommand):
    help = ('Fill the QA Studio review queues: generate samples for every active skill (or --skill …) '
            'until each has --per-skill samples. Samples are linted; errors are flagged for rework.')

    def add_arguments(self, parser):
        parser.add_argument('--per-skill', type=int, default=12,
                            help='target number of samples per skill (existing ones count; default 12)')
        parser.add_argument('--skill', action='append', default=[], help='only this skill slug (repeatable)')
        parser.add_argument('--grade', type=int, action='append', default=[], help='only skills of this grade')

    def handle(self, *args, **opts):
        skills = Skill.objects.filter(is_active=True).select_related('domain')
        if opts['skill']:
            skills = skills.filter(slug__in=opts['skill'])
        if opts['grade']:
            skills = skills.filter(domain__grade__in=opts['grade'])
        made = flagged = 0
        for skill in skills.order_by('domain__grade', 'order'):
            have = QuestionSample.objects.filter(skill=skill).exclude(status=QuestionSample.REJECTED).count()
            need = opts['per_skill'] - have
            if need <= 0:
                continue
            try:
                created = services.ingest(skill, need)
            except Exception as exc:                        # a broken generator shouldn't stop the batch
                self.stderr.write(f'{skill.slug}: generator failed ({exc.__class__.__name__}: {exc})')
                continue
            made += len(created)
            flagged += sum(1 for s in created if s.status == QuestionSample.FLAGGED)
        self.stdout.write(self.style.SUCCESS(f'{made} samples created, {flagged} flagged by the linter.'))
