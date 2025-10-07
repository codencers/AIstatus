from django.db import models
from django.conf import settings
import uuid

class OnboardingSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_step = models.IntegerField(default=1)

class AIResponse(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ]
    session = models.ForeignKey(OnboardingSession, on_delete=models.CASCADE)
    step = models.IntegerField()
    input_payload = models.JSONField()
    output_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class IdeaDraft(models.Model):
    session = models.ForeignKey(OnboardingSession, on_delete=models.CASCADE)
    problem_text = models.TextField()
    generated_idea = models.TextField(blank=True, null=True)
    ai_response = models.OneToOneField(AIResponse, on_delete=models.CASCADE, related_name="idea_draft")
