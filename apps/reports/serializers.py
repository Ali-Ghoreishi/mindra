from rest_framework import serializers


class DailyReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_tasks = serializers.IntegerField()
    completed = serializers.IntegerField()
    pending = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    overdue = serializers.IntegerField()


class WeeklyReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    total_tasks = serializers.IntegerField()
    completed = serializers.IntegerField()
    pending = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    cancelled = serializers.IntegerField()
