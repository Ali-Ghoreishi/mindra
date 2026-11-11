import uuid

from django.db import models


class Reminder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    task = models.ForeignKey(
        "tasks.Task", on_delete=models.CASCADE, related_name="reminders"
    )

    remind_at = models.DateTimeField()

    is_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.task.title}"
