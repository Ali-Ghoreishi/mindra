from django.urls import path

from .views import (
    OverdueTaskListView,
    PrioritizedTaskListView,
    TaskDetailView,
    TaskListCreateView,
    TaskWithRemindersCreateView,
)

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("prioritized/", PrioritizedTaskListView.as_view(), name="task-prioritized"),
    path("<uuid:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("overdue/", OverdueTaskListView.as_view(), name="task-overdue"),
    path(
        "with-reminders/",
        TaskWithRemindersCreateView.as_view(),
        name="task-with-reminders",
    ),
]
