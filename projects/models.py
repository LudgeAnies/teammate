from django.db import models
from users.models import CustomUser
from organizations.models import Organization
import uuid

class Project(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('approval', 'На согласовании'),
        ('implementation', 'В работе'),
        ('completed', 'Завершен'),
        ('postponed', 'Отложен'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    invite_code = models.CharField(max_length=10, unique=True, blank=True, verbose_name="Код приглашения заказчика")
    avatar = models.ImageField(upload_to='avatars/projects', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField(blank=True, null=True)
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

    def clean(self):
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError("Дедлайн не может быть в прошлом!")
        super().clean()

    def __str__(self):
        return self.name

class UserProjectRole(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('partner', 'Заказчик'),
        ('manager', 'Менеджер'),
        ('leader', 'Руководитель'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    can_edit = models.BooleanField(default=False, verbose_name="Может редактировать")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'],
                name='unique_user_project_role'
            )
        ]
        verbose_name = "Роль в проекте"
        verbose_name_plural = "Роли в проекте"

    def __str__(self):
        return f"{self.project.name} - {self.user.username} ({self.get_role_display()})"

class Task(models.Model):
    TYPE_CHOICES = [
        ('task', 'Задача'),
        ('development', 'Разработка'),
        ('idea', 'Идея'),
        ('research', 'Исследования'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('discussion', 'В обсуждении'),
        ('implementation', 'В работе'),
        ('correction', 'В исправлении'),
        ('completed', 'Завершена'),
        ('postponed', 'Отложена'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'Высокий'),
        ('medium', 'Средний'),
        ('low', 'Низкий'),
        ('unknown', 'Неизвестный'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', db_index=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='task', db_index=True)
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')
    #deadline = models.DateTimeField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='unknown', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

     def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Дата начала не может быть позже даты завершения!")
        super().clean() #

    def __str__(self):
        return self.title

    

class SubTask(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('discussion', 'В обсуждении'),
        ('implementation', 'В работе'),
        ('correction', 'В исправлении'),
        ('completed', 'Завершена'),
        ('postponed', 'Отложена'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'Высокий'),
        ('medium', 'Средний'),
        ('low', 'Низкий'),
        ('unknown', 'Неизвестный'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', db_index=True)
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='unknown', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания!")
        if self.task and self.start_date:
            if self.start_date < self.task.start_date:
                raise ValidationError("Дата начала подзадачи не может быть раньше даты начала задачи!")
        super().clean()

    def __str__(self):
        return self.title

class TaskAssignment(models.Model):
    ROLE_CHOICES = [
        ('executor', 'Исполнитель'),
        ('responsible', 'Ответственный'),
        ('observer', 'Наблюдатель'),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.task.title} - {self.user.full_name} ({self.get_role_display()})"

class Comment(models.Model): #
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    subtask = models.ForeignKey(SubTask, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Комментарий от {self.user.username}"

class CommentAttachment(models.Model): #
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='comment_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Вложение к комментарию {self.comment.id}"

class TaskDependency(models.Model): #
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependencies')
    depends_on = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependent_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['task', 'depends_on'],
                name='unique_task_dependency'
            )
        ]

    def __str__(self):
        return f"{self.task.title} зависит от {self.depends_on.title}"

class CheckList(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    subtask = models.ForeignKey(SubTask, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({'Выполнено' if self.is_completed else 'Не выполнено'})"

class History(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    subtask = models.ForeignKey(SubTask, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.action} ({self.created_at})"