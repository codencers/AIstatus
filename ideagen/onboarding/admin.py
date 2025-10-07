from django.contrib import admin
from .models import OnboardingSession, AIResponse, IdeaDraft

admin.site.register(OnboardingSession)
admin.site.register(AIResponse)
admin.site.register(IdeaDraft)
