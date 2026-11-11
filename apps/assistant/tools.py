from apps.reminders.models import Reminder
from apps.reports.services import get_daily_report
from apps.tasks.models import Task
from apps.tasks.services import get_overdue_tasks, get_prioritized_tasks


def create_task(
    user, title, description="", priority=Task.Priority.MEDIUM, due_date=None
):
    return Task.objects.create(
        user=user,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
    )


def create_reminder(user, task_id, remind_at):
    task = Task.objects.get(id=task_id, user=user)

    return Reminder.objects.create(task=task, remind_at=remind_at)


def get_daily_report_tool(user):
    return get_daily_report(user)


def get_overdue_tasks_tool(user):
    tasks = get_overdue_tasks(user)

    return list(tasks.values("id", "title", "priority", "due_date"))


def get_prioritized_tasks_tool(user):
    tasks = get_prioritized_tasks(user)

    return list(tasks.values("id", "title", "priority", "due_date"))
