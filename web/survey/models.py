from django.db import models


class User(models.Model):
    user_id = models.BigIntegerField("ID", unique=True, db_index=True)  # Telegram ID
    full_name = models.CharField("Имя", max_length=255, blank=True, null=True)
    username = models.CharField("Юзернейм", max_length=255, blank=True, null=True)  # @tag
    phone_number = models.CharField("Номер тг", max_length=20, blank=True, null=True)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)  # дата регистрации в системе

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.full_name} ({self.user_id})"


class Settlement(models.Model):
    name = models.CharField("Название", max_length=150, db_index=True)
    type = models.CharField("Тип",
        max_length=20,
        choices=[
            ('city', 'Город'),
            ('village', 'Село'),
            ('pgt', 'Пгт'),
            ('settlement', 'Поселок'),
        ],
        default='city'
    )
    priority = models.PositiveIntegerField("Приоритет", default=999)  # сортировка в топ-10

    class Meta:
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенные пункты"
        ordering = ['priority', 'name']

    def __str__(self):
        return self.name
    

class SurveyRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )

    settlement = models.ForeignKey(
        Settlement,
        on_delete=models.PROTECT,
        related_name="surveys",
        verbose_name="Населённый пункт",
        blank=True, null=True
    )

    settlement_custom = models.CharField("Свой населённый пункт", max_length=150, blank=True, null=True)


    street = models.CharField("Улица", max_length=128)
    house = models.CharField("Дом", max_length=32)
    apartment_number = models.CharField(
        "Номер квартиры",
        max_length=32,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        if self.settlement:
            name = self.settlement.name
        elif self.settlement_custom:
            name = self.settlement_custom
        else:
            name = "Неизвестный населённый пункт"

        return f"{name}: {self.street} {self.house}"
