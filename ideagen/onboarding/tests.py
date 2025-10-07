import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from onboarding.models import OnboardingSession, AIResponse, IdeaDraft
from django.contrib.auth import get_user_model
from onboarding.tasks import generate_idea_task

User = get_user_model()

@pytest.mark.django_db
def test_post_problem_creates_idea_draft():
    user = User.objects.create_user(username='testuser1', password='pass')
    session = OnboardingSession.objects.create(user=user)
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('onboarding-step1', args=[session.id])
    data = {"problem_text": "A detailed and real problem statement for a startup."}
    resp = client.post(url, data, format='json')
    assert resp.status_code == 202
    assert AIResponse.objects.count() == 1
    assert IdeaDraft.objects.count() == 1

@pytest.mark.django_db
def test_task_fills_generated_idea():
    user = User.objects.create_user(username='testuser2', password='pass')
    session = OnboardingSession.objects.create(user=user)
    ai_response = AIResponse.objects.create(
        session=session,
        step=1,
        input_payload={"problem_text": "Another realistic problem"},
        status="pending"
    )
    idea_draft = IdeaDraft.objects.create(
        session=session,
        problem_text="Another realistic problem",
        ai_response=ai_response
    )
    # Simulate Celery worker (run synchronously)
    generate_idea_task(ai_response.id)
    idea_draft.refresh_from_db()
    ai_response.refresh_from_db()

    assert ai_response.status == "success"
    assert idea_draft.generated_idea.startswith("This is a generated startup idea")
