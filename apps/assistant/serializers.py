from rest_framework import serializers


class AssistantSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=True,
        max_length=1000
    )