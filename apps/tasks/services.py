from django.db.models import Case, When, Value, IntegerField

from .models import Task


def get_prioritized_tasks(user):
    return (
        Task.objects
        .filter(user=user)
        .exclude(
            status__in=[
                Task.Status.COMPLETED,
                Task.Status.CANCELLED
            ]
        )
        .annotate(
            priority_order=Case(
                When(priority=Task.Priority.URGENT, then=Value(1)),
                When(priority=Task.Priority.HIGH, then=Value(2)),
                When(priority=Task.Priority.MEDIUM, then=Value(3)),
                When(priority=Task.Priority.LOW, then=Value(4)),
                output_field=IntegerField()
            )
        )
        .order_by("priority_order", "due_date")
    )