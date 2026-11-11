from rest_framework import serializers

from .models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ["id", "task", "remind_at", "is_sent", "created_at"]
        read_only_fields = ["id", "is_sent", "created_at"]

    def validate_task(self, value):
        user = self.context["request"].user

        if value.user != user:
            raise serializers.ValidationError(
                "You do not have permission to create a reminder for this task."
            )

        return value
