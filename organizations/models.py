from django.db import models
from users.models import User

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    users = models.ManyToManyField(User, through='UserOrganizationRole')

class UserOrganizationRole(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('admin', 'Администратор'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        return f"{self.organization.name} - {self.user.username} ({self.get_role_display()})"
