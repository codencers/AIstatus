from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from onboarding.views import OnboardingViewSet

router = DefaultRouter()
router.register(r'api/onboarding', OnboardingViewSet, basename='onboarding')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
