from django.db import models
from users.User import User
from organizations.models import Organization


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete.models.CASCADE, verbose_name="Пользователь")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация")
    message = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}"
        return f"Уведомление для {full_name} ({self.organization.name})"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
