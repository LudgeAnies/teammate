from django.db import models
from users.models import User
from organizations.models import Organization

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserProjectRole(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('partner', 'Партнер'),
        ('manager', 'Менеджер'),
        ('leader', 'Руководитель'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaskAssignment(models.Model):
    ROLE_CHOICES = [
        ('executor', 'Исполнитель'),
        ('responsible', 'Ответственный'),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)