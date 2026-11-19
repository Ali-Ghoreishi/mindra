from django.utils import timezone
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
import logging

from config.utils.translation import translate

from .models import Task
from .serializers import TaskSerializer
from .services import get_prioritized_tasks

logger = logging.getLogger(__name__)



# Handles listing tasks (GET) and creating a new task (POST).
class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = [
        "created_at",
        "updated_at",
        "due_date",
        "priority",
    ]
    ordering = ["-created_at"]

    # Create
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        response.data["message"] = translate(
            "task.created", title=response.data["title"]
        )

        return response

    # ----------

    # List
    def get_queryset(self):
        # print(vars(self.request))
        queryset = Task.objects.filter(user=self.request.user)
        # print(queryset.query)
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        logger.info("Fetching tasks for user: %s", self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["message"] = translate("common.success")
        return response

    # ----------


# Handles retrieving (GET), updating (PUT/PATCH), and deleting (DELETE) a specific task.
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    # Retrieve, Update, PATCH, Delete
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    # Retrieve
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data["message"] = translate("common.success")
        return response

    # Update (PUT)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data["message"] = translate(
            "task.updated", title=response.data["title"]
        )
        return response

    # Partial Update (PATCH)
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        response.data["message"] = translate(
            "task.updated", title=response.data["title"]
        )
        return response

    # # Delete (DELETE)
    # def destroy(self, request, *args, **kwargs):
    #     response = super().destroy(request, *args, **kwargs)
    #     response.data = {"message": translate("task.deleted")}
    #     return response

    # ----------


# Handles listing overdue tasks (GET).
class OverdueTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Task.objects.filter(
                user=self.request.user,
                due_date__lt=timezone.now(),
            )
            .exclude(
                status__in=[
                    Task.Status.COMPLETED,
                    Task.Status.CANCELLED,
                ]
            )
            .order_by("due_date")
        )


# Handles listing prioritized tasks (GET).
class PrioritizedTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_prioritized_tasks(self.request.user)
