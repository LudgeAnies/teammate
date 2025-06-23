from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import timedelta
from projects.models import Project, Task
from organizations.models import Organization
from users.models import CustomUser
from django.utils import timezone
from unittest.mock import patch


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Test Org'
        )

    @patch('projects.services.calendar_api.ProductionCalendarAPI.is_working_day')
    def test_project_deadline_validation(self, mock_is_working_day):
        # Настраиваем mock для возврата False (нерабочий день)
        mock_is_working_day.return_value = False

        project = Project(
            name='Test Project',
            organization=self.org,
            deadline=timezone.now() + timedelta(days=5))

        with self.assertRaises(ValidationError):
            project.full_clean()

    @patch('projects.services.calendar_api.ProductionCalendarAPI.get_working_days_count')
    def test_working_days_calculation(self, mock_get_working_days_count):
        mock_get_working_days_count.return_value = 10

        project = Project.objects.create(
            name='Test Project',
            organization=self.org,
            deadline=timezone.now() + timedelta(days=30))

        task = Task.objects.create(
            title='Test Task',
            project=project,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=10))

        self.assertEqual(task.working_days, 10)
        self.assertEqual(task.working_hours, 80)


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Test Org'
        )
        self.project = Project.objects.create(
            name='Test Project',
            organization=self.org)

    @patch('projects.services.calendar_api.ProductionCalendarAPI.is_working_day')
    def test_task_date_validation(self, mock_is_working_day):
        mock_is_working_day.return_value = False

        task = Task(
            title='Invalid Task',
            project=self.project,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1))

        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_dates_ordering(self):
        task = Task(
            title='Test Task',
            project=self.project,
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now())

        with self.assertRaises(ValidationError):
            task.full_clean()