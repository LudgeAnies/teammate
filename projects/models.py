from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from autoslug import AutoSlugField
from datetime import timedelta
from users.models import CustomUser
from organizations.models import Organization
from .services.calendar_api import ProductionCalendarAPI

class Project(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('approval', 'На согласовании'),
        ('implementation', 'В работе'),
        ('completed', 'Завершен'),
        ('postponed', 'Отложен'),
    ]
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = AutoSlugField(
        populate_from='name',
        unique=True,
        always_update=True,
        verbose_name='URL'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/avatars/projects', blank=True, null=True, verbose_name='Фотография')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', verbose_name='Статус проекта')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='Дедлайн')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def clean(self):
        super().clean()
        # if self.deadline and self.deadline < timezone.now():
        #     raise ValidationError("Дедлайн не может быть в прошлом!")

        if self.deadline:
            if not ProductionCalendarAPI.is_working_day(self.deadline):
                raise ValidationError(f"Дедлайн {self.deadline.date()} является выходным днем")

    def get_total_working_days(self):
        tasks = self.task_set.all()
        if not tasks.exists():
            return 0

        start_dates = [t.start_date.date() for t in tasks if t.start_date]
        end_dates = [t.end_date.date() for t in tasks if t.end_date]

        if not start_dates or not end_dates:
            return 0

        min_date = min(start_dates)
        max_date = max(end_dates)

        return ProductionCalendarAPI.get_working_days_count(min_date, max_date)
    
    def get_total_working_hours(self):
        total = 0
        for task in self.task_set.all():
            if task.working_hours:
                total += task.working_hours
        return total

    def __str__(self):
        return self.name

class UserProjectRole(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('manager', 'Менеджер'),
        ('leader', 'Руководитель'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='Роль на проекте')
    can_edit = models.BooleanField(default=False, verbose_name="Можно редактировать")

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
        ('research', 'Исследование'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('discussion', 'В обсуждении'),
        ('implementation', 'В работе'),
        ('correction', 'В исправлении'),
        ('completed', 'Завершено'),
        ('postponed', 'Отложено'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'Высокий'),
        ('medium', 'Средний'),
        ('low', 'Низкий'),
        ('unknown', 'Неизвестный'),
    ]

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', db_index=True, verbose_name='Статус задачи')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='task', db_index=True, verbose_name='Тип задачи')
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')
    #deadline = models.DateTimeField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='unknown', db_index=True, verbose_name='Приоритет задачи')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def clean(self):
        super().clean() #

        # Проверяем, что дата начала не позже даты окончания
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания!")

        # Проверяем, что дедлайн задачи не позже дедлайна проекта
        if self.project.deadline and self.end_date and self.end_date > self.project.deadline:
            raise ValidationError("Дедлайн задачи не может быть позже даты проекта!")

        if self.start_date:
            if not ProductionCalendarAPI.is_working_day(self.start_date):
                raise ValidationError(f"Дата начала {self.start_date.date()} является выходным днем")

        if self.end_date:
            if not ProductionCalendarAPI.is_working_day(self.end_date):
                raise ValidationError(f"Дата окончания {self.end_date.date()} является выходным днем")

        # # Проверяем, что дата не в прошлом
        # if self.start_date and self.start_date < timezone.now():
        #     raise ValidationError("Start date cannot be in the past")

    @property
    def working_days(self):
        if not self.start_date or not self.end_date:
            return 0
        return ProductionCalendarAPI.get_working_days_count(
            self.start_date.date(),
            self.end_date.date()
        )

    @property
    def working_hours(self):
        # Предполагаем 8-часовой рабочий день
        return self.working_days * 8

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

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', db_index=True, verbose_name='Статус подзадачи')
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='unknown', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'

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
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, verbose_name='Роль в задаче')

    class Meta:
        verbose_name = 'Роль в задаче'
        verbose_name_plural = 'Роли в задаче'

    def __str__(self):
        return f"{self.task.title} - {self.user.full_name} ({self.get_role_display()})"

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий от {self.user.username}"

class CommentAttachment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='comment_attachments/', verbose_name='Вложение')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вложение к комментарию'
        verbose_name_plural = 'Вложения к комментарию'

    def __str__(self):
        return f"Вложение к комментарию {self.comment.id}"

class CheckList(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Задание')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Чеклист'
        verbose_name_plural = 'Чеклисты'

    def clean(self): #
        if not any([self.project, self.task, self.subtask]):
            raise ValidationError("Чеклист должен быть привязан к проекту, задаче или подзадаче")
        if sum(bool(x) for x in [self.project, self.task, self.subtask]) > 1:
            raise ValidationError("Чеклист может быть привязан только к одному объекту")

    def __str__(self):
        return f"{self.title} ({'Выполнено' if self.is_completed else 'Не выполнено'})"

class History(models.Model):
    ACTION_TYPES = [
        ('org_create', 'Создание организации'),
        ('org_update', 'Изменение организации'),
        ('project_create', 'Создание проекта'),
        ('project_update', 'Изменение проекта'),
        ('project_status', 'Изменение статуса проекта'),
        ('task_create', 'Создание задачи'),
        ('task_update', 'Изменение задачи'),
        ('task_status', 'Изменение статуса задачи'),
        ('task_deadline', 'Изменение сроков задачи'),
        ('subtask_create', 'Создание подзадачи'),
        ('subtask_update', 'Изменение подзадачи'),
        ('subtask_status', 'Изменение статуса подзадачи'),
        ('subtask_deadline', 'Изменение сроков подзадачи'),
        ('member_add', 'Добавление участника'),
        ('member_remove', 'Удаление участника'),
        ('role_change', 'Изменение роли'),
        ('comment_add', 'Добавление комментария'),
        ('attachment_add', 'Добавление вложения'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    description = models.TextField(blank=True, null=True) # blank и null временно
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    subtask = models.ForeignKey(SubTask, on_delete=models.CASCADE, null=True, blank=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'История изменений'
        verbose_name_plural = 'История изменений'

    def __str__(self):
        return f"{self.get_action_display()} - {self.created_at}"