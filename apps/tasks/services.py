from django.db import transaction
from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone

from apps.reminders.models import Reminder

from .models import Task


def get_prioritized_tasks(user):
    return (
        Task.objects.filter(user=user)
        .exclude(status__in=[Task.Status.COMPLETED, Task.Status.CANCELLED])
        .annotate(
            priority_order=Case(
                When(priority=Task.Priority.URGENT, then=Value(1)),
                When(priority=Task.Priority.HIGH, then=Value(2)),
                When(priority=Task.Priority.MEDIUM, then=Value(3)),
                When(priority=Task.Priority.LOW, then=Value(4)),
                output_field=IntegerField(),
            )
        )
        .order_by("priority_order", "due_date")
    )


def get_overdue_tasks(user):
    return (
        Task.objects.filter(user=user, due_date__lt=timezone.now())
        .exclude(status__in=[Task.Status.COMPLETED, Task.Status.CANCELLED])
        .order_by("due_date")
    )


def create_task_with_reminders(validated_data, user):
    reminders = validated_data.pop("reminders")

    with transaction.atomic():
        task = Task.objects.create(user=user, **validated_data)

        for remind_at in reminders:
            Reminder.objects.create(task=task, remind_at=remind_at)

    return task
