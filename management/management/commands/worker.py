from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Run celery worker'

    def handle(self, *args, **options):
        subprocess.run(["celery", "-A", "core", "worker", "-l", "INFO", "--concurrency", "1", "-P", "solo"])