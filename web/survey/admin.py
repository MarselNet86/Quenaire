from django.contrib import admin
from .models import User, Settlement, SurveyRequest


# --------------------------
# Пользователи
# --------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "full_name",
        "username",
        "phone_number",
        "created_at",
    )
    search_fields = (
        "user_id",
        "full_name",
        "username",
        "phone_number",
    )
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Основное", {
            "fields": ("user_id", "full_name", "username", "phone_number")
        }),
        ("Системное", {
            "fields": ("created_at",),
        }),
    )


# --------------------------
# Населённые пункты
# --------------------------
@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "priority")
    search_fields = ("name",)
    list_filter = ("type",)
    ordering = ("priority", "name")

    fieldsets = (
        ("Основное", {
            "fields": ("name", "type")
        }),
        ("Системное", {
            "fields": ("priority",),
        }),
    )


# --------------------------
# Заявки
# --------------------------
@admin.register(SurveyRequest)
class SurveyRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user_display",
        "phone_display",
        "settlement_display",
        "street",
        "house",
        "apartment_number",
        "created_at",
    )

    search_fields = (
        "street",
        "house",
        "settlement__name",
        "settlement_custom",
        "user__full_name",
        "user__phone_number",
    )

    list_filter = ("settlement", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Пользователь", {
            "fields": ("user",)
        }),
        ("Адрес", {
            "fields": ("settlement", "settlement_custom", "street", "house", "apartment_number",)
        }),
        ("Системное", {
            "fields": ("created_at",),
        }),
    )

    # ---------- кастомные отображения ----------
    def user_display(self, obj):
        return obj.user.full_name if obj.user else "—"
    user_display.short_description = "Имя"

    def phone_display(self, obj):
        return obj.user.phone_number if obj.user else "—"
    phone_display.short_description = "Телефон"

    def settlement_display(self, obj):
        if obj.settlement:
            return obj.settlement.name
        elif obj.settlement_custom:
            return f"📝 {obj.settlement_custom}"
        return "—"
    settlement_display.short_description = "Населённый пункт"

