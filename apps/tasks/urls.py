from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
    OverdueTaskListView,
    PrioritizedTaskListView,
)


urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("prioritized/", PrioritizedTaskListView.as_view(), name="task-prioritized"),
    path("<uuid:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("overdue/", OverdueTaskListView.as_view(), name="task-overdue"),
]
