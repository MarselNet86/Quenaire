from django.contrib import admin
from .models import SurveyRequest


@admin.register(SurveyRequest)
class SurveyRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "street", "house", "current_services", "created_at")
    search_fields = ("name", "phone", "street", "house")
    list_filter = ("current_services", "created_at")
