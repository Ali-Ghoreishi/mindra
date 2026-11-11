from django.urls import path
from .views import DailyReportView, WeeklyReportView

urlpatterns = [
    path("daily/", DailyReportView.as_view(), name="daily-report"),
    path("weekly/", WeeklyReportView.as_view(), name="weekly-report"),
]