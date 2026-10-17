from django.core.management.base import BaseCommand

from qastudio import services


class Command(BaseCommand):
    help = ('Re-run every sample\'s generator with its seed. Samples whose output changed (code was edited) '
            'go back to the review queue and certifications are recounted. Run after each deploy.')

    def handle(self, *args, **opts):
        n = services.refresh_all()
        self.stdout.write(self.style.SUCCESS(f'{n} sample(s) regenerated because their generator changed.'))
