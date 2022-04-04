from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Run celery beat'

    def handle(self, *args, **options):
        subprocess.run(["celery", "-A", "core", "beat", "-l", "INFO"])
