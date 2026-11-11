from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import AssistantSerializer
from .agent import AssistantAgent


class AssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssistantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]

        agent = AssistantAgent()
        result = agent.process(
            user=request.user,
            message=message
        )

        return Response({
            "message": message,
            "result": result
        })