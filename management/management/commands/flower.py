from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Run flower for celery'

    def handle(self, *args, **options):
        subprocess.run(["celery", "-A", "core", "flower"])
