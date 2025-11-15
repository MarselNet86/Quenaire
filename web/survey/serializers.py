from rest_framework import serializers
from .models import SurveyRequest


class SurveyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyRequest
        fields = "__all__"
