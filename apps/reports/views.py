from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DailyReportSerializer, WeeklyReportSerializer
from .services import get_daily_report, get_weekly_report


class DailyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        report = get_daily_report(request.user)

        serializer = DailyReportSerializer(report)

        return Response(serializer.data)


class WeeklyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        report = get_weekly_report(request.user)
        serializer = WeeklyReportSerializer(report)

        return Response(serializer.data)
