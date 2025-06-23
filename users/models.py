from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import pytz

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Требуется указать username')
        if not email:
            raise ValueError('Требуется указать email')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, verbose_name='Адрес электронной почты')
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': "Пользователь с таким именем уже существует.",
        },
        verbose_name='Имя пользователя'
    )
    
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фамилия')
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='media/avatars/users/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    timezone = models.CharField(max_length=32, default='UTC', choices=[(tz, tz) for tz in pytz.all_timezones])
    
    def get_local_time(self, datetime_obj):
        user_tz = pytz.timezone(self.timezone)
        return datetime_obj.astimezone(user_tz)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def __str__(self):
        return self.full_name

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_member_org', 'Новый участник организации'),
        ('new_member_project', 'Новый участник проекта'),
        ('task_assignment', 'Назначение на задачу'),
        ('project_assignment', 'Назначение на проект'),
        ('task_deadline', 'Дедлайн задачи'),
        ('project_deadline', 'Дедлайн проекта'),
        ('new_comment', 'Новый комментарий'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    related_project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True)
    related_task = models.ForeignKey('projects.Task', on_delete=models.CASCADE, null=True, blank=True)
    related_subtask = models.ForeignKey('projects.SubTask', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.email}"
