from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="partner")
    name = models.CharField(max_length=255, verbose_name="Название компании или имя партнера")
    center = models.ForeignKey(
        'centers.Center',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partners'  # Уникальное имя для обратной связи
    )
    contact_email = models.EmailField(verbose_name="Контактный email")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    is_active = models.BooleanField(default=False, verbose_name="Активирован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return self.name
