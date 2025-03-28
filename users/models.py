from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

# class CustomUser(AbstractUser):
#     USER_TYPE_CHOICES = [
#         ('employee', 'Сотрудник'),
#         ('customer', 'Заказчик'),
#     ]
#     first_name = models.CharField(max_length=255, verbose_name='Имя')
#     last_name = models.CharField(max_length=255, verbose_name='Фамилия')
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     is_active = models.BooleanField(default=False)
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='employee')
#     avatar = models.ImageField(upload_to='avatars/users/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"

#     def __str__(self):
#         full_name = f"{first_name} {last_name}"
#         return full_name


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
    USER_TYPE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('customer', 'Заказчик'),
    ]
    
    # Делаем email обязательным и уникальным
    email = models.EmailField('email address', unique=True, blank=False)
    
    # Делаем username обязательным (AbstractUser уже делает его уникальным)
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        blank=False,
        help_text='Обязательное поле. 150 символов или меньше. Только буквы, цифры и @/./+/-/_',
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': "Пользователь с таким именем уже существует.",
        },
    )
    
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    #phone_number = models.CharField(max_length=15, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, region='RU')
    is_active = models.BooleanField(default=False) # выключить в false после реализации двухфакторки
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='employee')
    avatar = models.ImageField(upload_to='avatars/users/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def full_name(self):
        #return f"{self.first_name} {self.last_name}"
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    # def clean(self):
    #     if self.avatar:
    #         try:
    #             w, h = get_image_dimensions(self.avatar.file)
    #             if w > 1024 or h > 1024:
    #                 raise ValidationError("Размер изображения не должен превышать 1024x1024 пикселей")
    #         except AttributeError:
    #             pass
    #     super().clean()

    def __str__(self):
        return self.full_name