from django.urls import path
from .views import UserCheckView, SettlementListView, SurveyCreateView, UserRegisterView

urlpatterns = [
    path("user/check/", UserCheckView.as_view()),
    path("user/register/", UserRegisterView.as_view()),
    path("settlements/", SettlementListView.as_view()),
    path("survey/create/", SurveyCreateView.as_view()),
]
