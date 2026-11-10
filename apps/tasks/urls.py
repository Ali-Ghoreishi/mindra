from django.urls import path
from .views import TaskListCreateView, TaskDetailView, OverdueTaskListView


urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<uuid:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("overdue/", OverdueTaskListView.as_view(), name="task-overdue"),
]
