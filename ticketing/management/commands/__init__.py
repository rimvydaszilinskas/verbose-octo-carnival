import logging

from django.core.management.base import BaseCommand

from ticketing.models import Ticket


class Command(BaseCommand):
    """
    Check all tasks for timeouts

    If time exceeds `DEFAULT_TASK_TIMEOUT` in settings, the task is marked as aborted
    """
    help = 'Check tasks for timeouts/alerts'

    def handle(self, *args, **options):
        pass
