from django.db import models


class SurveyRequest(models.Model):
    street = models.CharField("Улица", max_length=128)
    house = models.CharField("Дом", max_length=32)
    name = models.CharField("Имя", max_length=128)
    phone = models.CharField("Телефон", max_length=32)

    SERVICES = [
        ("mobile", "Мобильная связь"),
        ("copper", "Медный телефон"),
    ]

    current_services = models.CharField(
        "Текущие услуги",
        max_length=32,
        choices=SERVICES
    )

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} ({self.street} {self.house})"
