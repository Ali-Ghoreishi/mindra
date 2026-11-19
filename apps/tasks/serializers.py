from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TaskWithRemindersSerializer(serializers.ModelSerializer):
    reminders = serializers.ListField(
        child=serializers.DateTimeField(),
        allow_empty=False,
        max_length=2
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "reminders",
        ]
