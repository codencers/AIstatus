from rest_framework import serializers
from .models import IdeaDraft

class IdeaDraftSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='ai_response.status', read_only=True)

    class Meta:
        model = IdeaDraft
        fields = ['problem_text', 'generated_idea', 'status']

    def validate_problem_text(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Problem text must be at least 20 characters.")
        return value
