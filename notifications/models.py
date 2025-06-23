# from django.db import models
# from users.models import CustomUser
# from organizations.models import Organization
#
#
# class Notification(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация")
#     message = models.TextField(verbose_name="Сообщение")
#     is_read = models.BooleanField(default=False, verbose_name="Прочитано")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
#
#     def __str__(self):
#         return f"Уведомление для {self.user.full_name} ({self.organization.name})"
#
#     class Meta:
#         verbose_name = "Уведомление"
#         verbose_name_plural = "Уведомления"
