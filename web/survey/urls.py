from django.urls import path
from .views import SurveyCreateAPIView

urlpatterns = [
    path("create/", SurveyCreateAPIView.as_view(), name="survey-create"),
]
