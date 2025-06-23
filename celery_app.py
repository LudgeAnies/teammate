import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
# from django.core.mail import send_mail
# from django.utils import timezone
# from datetime import timedelta
# from projects.models import Task, TaskAssignment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TeamMate.settings')

app = Celery('TeamMate')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Проверка дедлайнов каждый день в 9:00
    sender.add_periodic_task(
        crontab(hour=9, minute=0),
        check_deadlines.s(),
        name='daily-deadline-check'
    )


@app.task(bind=True)
def check_deadlines():
    from django.utils import timezone
    from datetime import timedelta
    from projects.models import Task

    # Уведомление за 5 дней до дедлайна
    five_days_from_now = timezone.now() + timedelta(days=5)
    tasks = Task.objects.filter(
        end_date__date=five_days_from_now.date(),
        status__in=['new', 'implementation']
    )
    for task in tasks:
        send_deadline_notification.delay(
            task.id,
            '5 days remaining'
        )

    # Уведомление за 1 день до дедлайна
    one_day_from_now = timezone.now() + timedelta(days=1)
    tasks = Task.objects.filter(
        end_date__date=one_day_from_now.date(),
        status__in=['new', 'implementation']
    )
    for task in tasks:
        send_deadline_notification.delay(
            task.id,
            '1 day remaining'
        )


@app.task
def send_deadline_notification(task_id, message):
    from django.core.mail import send_mail
    from projects.models import Task, TaskAssignment
    from django.conf import settings

    task = Task.objects.get(id=task_id)
    assignees = TaskAssignment.objects.filter(task=task).select_related('user')

    for assignment in assignees:
        subject = f'Напоминание о задаче: {task.title}'
        body = f'''
        Здравствуйте{assignment.user.first_name},

        Напоминаем о том, что задача "{task.title}" должна быть выполнена в {message}.
        Deadline: {task.end_date}

        Проект: {task.project.name}

        С уважением,
        Команда Телеком БГ
        '''

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [assignment.user.email],
            fail_silently=False,
        )