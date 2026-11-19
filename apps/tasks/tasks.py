import logging
from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone

from .models import Task

logger = logging.getLogger(__name__)


@shared_task
def remove_old_tasks():
    old_tasks = Task.objects.filter(
        status__in=[
            Task.Status.COMPLETED,
            Task.Status.CANCELLED,
        ],
        due_date__lt=timezone.now() - timedelta(days=10),
    )

    task_titles = list(old_tasks.values_list("title", flat=True))
    task_count = len(task_titles)

    if task_count == 0:
        logger.info("No old tasks found for deletion.")
        return 0

    old_tasks.delete()

    logger.info(
        "Deleted %s old tasks: %s",
        task_count,
        ", ".join(task_titles),
    )

    return task_count
