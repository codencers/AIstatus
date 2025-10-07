from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import OnboardingSession, AIResponse, IdeaDraft
from .serializers import IdeaDraftSerializer
from .tasks import generate_idea_task

class OnboardingViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['post'], url_path='steps/1')
    def step1(self, request, pk=None):
        session = get_object_or_404(OnboardingSession, id=pk)
        serializer = IdeaDraftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        problem_text = serializer.validated_data['problem_text']

        ai_response = AIResponse.objects.create(
            session=session,
            step=1,
            input_payload={'problem_text': problem_text},
            status='pending'
        )
        idea_draft = IdeaDraft.objects.create(
            session=session,
            problem_text=problem_text,
            ai_response=ai_response
        )
        task = generate_idea_task.delay(ai_response.id)
        return Response({"task_id": str(ai_response.id), "status": "pending"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'], url_path='tasks/(?P<task_id>[^/.]+)/status')
    def task_status(self, request, pk=None, task_id=None):
        session = get_object_or_404(OnboardingSession, id=pk)
        ai_response = get_object_or_404(AIResponse, session=session, id=task_id)
        data = {
            "status": ai_response.status,
            "output_text": ai_response.output_text
        }
        return Response(data)
