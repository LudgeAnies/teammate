from django.db import models
from users.models import CustomUser
import uuid

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    invite_code = models.CharField(max_length=10, unique=True, blank=True, verbose_name='Код организации')
    avatar = models.ImageField(upload_to='avatars/organizations', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = str(uuid.uuid4())[:10]
        super().save(*args, **kwargs)

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
        return self.name

    #users = models.ManyToManyField(User, through='UserOrganizationRole')

class UserOrganizationRole(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('admin', 'Администратор'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee', verbose_name="Роль")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'organization'],
                name='unique_user_organization_role'
            )
        ]
        verbose_name = "Роль в организации"
        verbose_name_plural = "Роли в организации"

    def __str__(self):
        return f"{self.organization.name} - {self.user.full_name} ({self.get_role_display()})"