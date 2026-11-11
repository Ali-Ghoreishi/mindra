from django.utils import timezone
from datetime import timedelta

from apps.tasks.models import Task


def get_daily_report(user):
    today = timezone.localdate()

    tasks = Task.objects.filter(user=user, created_at__date=today)

    return {
        "date": today,
        "total_tasks": tasks.count(),
        "completed": tasks.filter(status=Task.Status.COMPLETED).count(),
        "pending": tasks.filter(status=Task.Status.PENDING).count(),
        "in_progress": tasks.filter(status=Task.Status.IN_PROGRESS).count(),
        "overdue": tasks.filter(due_date__lt=timezone.now())
        .exclude(status__in=[Task.Status.COMPLETED, Task.Status.CANCELLED])
        .count(),
    }


def get_weekly_report(user):
    today = timezone.localdate()

    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=7)

    tasks = Task.objects.filter(
        user=user, created_at__date__gte=start_date, created_at__date__lt=end_date
    )

    return {
        "start_date": start_date,
        "end_date": end_date - timedelta(days=1),
        "total_tasks": tasks.count(),
        "completed": tasks.filter(status=Task.Status.COMPLETED).count(),
        "pending": tasks.filter(status=Task.Status.PENDING).count(),
        "in_progress": tasks.filter(status=Task.Status.IN_PROGRESS).count(),
        "cancelled": tasks.filter(status=Task.Status.CANCELLED).count(),
    }
