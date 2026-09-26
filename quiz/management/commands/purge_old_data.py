"""
Data minimisation: delete what we no longer need.

- AI search queries older than 90 days (kept only to spot content gaps)
- expired login sessions

Run nightly from cron:  .venv/bin/python manage.py purge_old_data
"""
from datetime import timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from quiz.models import SearchQuery

SEARCH_RETENTION_DAYS = 90


class Command(BaseCommand):
    help = 'Delete search queries older than 90 days and expired sessions.'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=SEARCH_RETENTION_DAYS)
        n, _ = SearchQuery.objects.filter(created_at__lt=cutoff).delete()
        call_command('clearsessions')
        self.stdout.write(f'purged {n} search queries older than {SEARCH_RETENTION_DAYS} days; expired sessions cleared')
