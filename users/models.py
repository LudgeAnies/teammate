from django.db import models
from django.contrib.auth.models import AbstractUser

# class UserManager(BaseUserManager):
#     def _create_user(self, email, password, **kwargs):
#         if not email:
#             raise ValueError("Email is required")

#         email = self.normalize_email(email)
#         user = self.model(email=email, **kwargs)
#         user.set_password(password)
#         user.save()
#         return user

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('customer', 'Заказчик'),
    ]
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='employee')
    avatar = models.ImageField(upload_to='avatars/users/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        full_name = f"{first_name} {last_name}"
        return full_name