from django.db import models
from users.models import CustomUser
import uuid
from autoslug import AutoSlugField

class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = AutoSlugField(
        populate_from='name',
        unique=True,
        always_update=True,
        verbose_name='URL'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    invite_code = models.CharField(max_length=10, unique=True, blank=True, verbose_name='Код организации')
    avatar = models.ImageField(upload_to='media/avatars/organizations', blank=True, null=True, verbose_name='Фотография')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def save(self, *args, **kwargs):
        created = not self.pk #
        if not self.invite_code:
            self.invite_code = str(uuid.uuid4())[:10]
        # if not self.slug: #
        #     self.slug = slugify(self.name)
        #     original_slug = self.slug
        #     counter = 1
        #     while Organization.objects.filter(slug=self.slug).exists():
        #         self.slug = f"{original_slug}-{counter}"
        #         counter += 1
        super().save(*args, **kwargs)

        if created and hasattr(self, '_creator'):
            UserOrganizationRole.objects.create(
                user=self._creator,
                organization=self,
                role='admin'
        )

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

class UserOrganizationRole(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('admin', 'Администратор'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee', verbose_name="Роль")
    can_edit = models.BooleanField(default=False, verbose_name="Можно редактировать")

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