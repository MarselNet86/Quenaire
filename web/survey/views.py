from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Settlement, SurveyRequest
from .serializers import (
    UserCheckSerializer, UserSerializer,
    SettlementSerializer, SurveyRequestSerializer, UserCreateSerializer
)


class UserCheckView(APIView):
    """
    Проверка: пользователь существует в базе или нет.
    """
    def post(self, request):
        serializer = UserCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]

        try:
            user = User.objects.get(user_id=user_id)
            return Response({"exists": True, "user": UserSerializer(user).data})
        except User.DoesNotExist:
            return Response({"exists": False})


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.update_or_create(
                user_id=serializer.validated_data["user_id"],
                defaults=serializer.validated_data
            )
            return Response({
                "success": True,
                "created": created,
                "user": UserSerializer(user).data
            })
        return Response({"success": False, "errors": serializer.errors}, status=400)


class SettlementListView(APIView):
    """
    Возвращает список всех населённых пунктов.
    """
    def get(self, request):
        settlements = Settlement.objects.all()
        return Response(SettlementSerializer(settlements, many=True).data)


class SurveyCreateView(APIView):
    """
    Создание заявки.
    """
    def post(self, request):
        serializer = SurveyRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=201)
        return Response({"success": False, "errors": serializer.errors}, status=400)
