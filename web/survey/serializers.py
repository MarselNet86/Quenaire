from rest_framework import serializers
from .models import User, Settlement, SurveyRequest


class UserCheckSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_id", "full_name", "username", "phone_number"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_id", "full_name", "username", "phone_number", "created_at"]


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ["id", "name", "type", "priority"]


class SurveyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyRequest
        fields = ["id", "user", "settlement", "settlement_custom", "street", "house"]
