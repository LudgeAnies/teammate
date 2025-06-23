from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from projects.models import Project, Task, SubTask, CheckList, Comment
from organizations.models import Organization
from users.models import CustomUser
from unittest.mock import patch
from django.utils import timezone

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Test Org',
        )
        self.project = Project.objects.create(
            name='Test Project',
            organization=self.org,
            deadline=timezone.now() + timedelta(days=30))

    def test_project_creation(self):
        self.assertEqual(self.project.status, 'new')
        self.assertEqual(str(self.project), 'Test Project')

    def test_project_slug_auto_generation(self):
        self.assertTrue(len(self.project.slug) > 0)

    @patch('projects.services.calendar_api.ProductionCalendarAPI.is_working_day')
    def test_project_deadline_validation(self, mock_is_working):
        mock_is_working.return_value = False
        project = Project(
            name='Invalid Project',
            organization=self.org,
            deadline=timezone.now() + timedelta(days=1))

        with self.assertRaises(ValidationError):
            project.full_clean()


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='dev',
            email='dev@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Dev Org',
        )
        self.project = Project.objects.create(
            name='Dev Project',
            organization=self.org)
        self.task = Task.objects.create(
            title='Main Task',
            project=self.project,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7))

    def test_task_creation(self):
        self.assertEqual(self.task.type, 'task')
        self.assertEqual(self.task.priority, 'unknown')
        self.assertEqual(str(self.task), 'Main Task')

    def test_task_dates_validation(self):
        invalid_task = Task(
            title='Invalid Task',
            project=self.project,
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now())

        with self.assertRaises(ValidationError):
            invalid_task.full_clean()

    @patch('projects.services.calendar_api.ProductionCalendarAPI.get_working_days_count')
    def test_working_days_calculation(self, mock_working_days):
        mock_working_days.return_value = 5
        self.assertEqual(self.task.working_days, 5)
        self.assertEqual(self.task.working_hours, 40)


class SubTaskModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='QA Org',
        )
        self.project = Project.objects.create(
            name='QA Project',
            organization=self.org)
        self.task = Task.objects.create(
            title='Testing Task',
            project=self.project,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=14))
        self.subtask = SubTask.objects.create(
            title='Unit Tests',
            task=self.task,
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=3))

    def test_subtask_creation(self):
        self.assertEqual(self.subtask.status, 'new')
        self.assertEqual(str(self.subtask), 'Unit Tests')

    def test_subtask_date_validation(self):
        # Подзадача не может начинаться раньше задачи
        invalid_subtask = SubTask(
            title='Invalid Subtask',
            task=self.task,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1))

        with self.assertRaises(ValidationError):
            invalid_subtask.full_clean()


class CheckListModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='designer',
            email='designer@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Design Org',
        )
        self.project = Project.objects.create(
            name='Design Project',
            organization=self.org)
        self.task = Task.objects.create(
            title='UI Design',
            project=self.project)
        self.checklist = CheckList.objects.create(
            title='Design Review',
            task=self.task,
            project=self.project)

    def test_checklist_creation(self):
        self.assertFalse(self.checklist.is_completed)
        self.assertEqual(str(self.checklist), 'Design Review (Не выполнено)')
        self.assertEqual(self.checklist.project, self.project)

    def test_checklist_completion(self):
        self.checklist.is_completed = True
        self.checklist.save()
        self.assertEqual(str(self.checklist), 'Design Review (Выполнено)')


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Review Org',
        )
        self.project = Project.objects.create(
            name='Review Project',
            organization=self.org)
        self.task = Task.objects.create(
            title='Code Review',
            project=self.project)
        self.comment = Comment.objects.create(
            user=self.user,
            content='Initial comment',
            task=self.task)

    def test_comment_creation(self):
        self.assertEqual(str(self.comment), 'Комментарий от reviewer')
        self.assertEqual(self.comment.content, 'Initial comment')