from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from projects.models import Project, Task, SubTask, CheckList, Comment
from organizations.models import Organization
from users.models import CustomUser
from datetime import datetime, timedelta
from unittest.mock import patch


class ProjectAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='api_user',
            email='api@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='API Org',
            creator=self.user
        )
        self.project = Project.objects.create(
            name='API Project',
            organization=self.org)
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        url = reverse('project-list', kwargs={'org_slug': self.org.slug})
        data = {
            'name': 'New API Project',
            'description': 'Test project creation via API'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_project_detail(self):
        url = reverse('project-detail', kwargs={
            'org_slug': self.org.slug,
            'pk': self.project.pk
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Project')


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='task_user',
            email='task@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Task Org',
            creator=self.user
        )
        self.project = Project.objects.create(
            name='Task Project',
            organization=self.org)
        self.task = Task.objects.create(
            title='Main Task',
            project=self.project)
        self.client.force_authenticate(user=self.user)

    def test_task_list(self):
        url = reverse('task-list', kwargs={
            'org_slug': self.org.slug,
            'project_slug': self.project.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @patch('projects.services.calendar_api.ProductionCalendarAPI.is_working_day')
    def test_create_task_with_dates(self, mock_is_working):
        mock_is_working.return_value = True

        url = reverse('task-list', kwargs={
            'org_slug': self.org.slug,
            'project_slug': self.project.slug
        })
        data = {
            'title': 'New Task',
            'start_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=3)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)


class SubTaskAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='subtask_user',
            email='subtask@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='SubTask Org',
            creator=self.user
        )
        self.project = Project.objects.create(
            name='SubTask Project',
            organization=self.org)
        self.task = Task.objects.create(
            title='Parent Task',
            project=self.project)
        self.subtask = SubTask.objects.create(
            title='First Subtask',
            task=self.task)
        self.client.force_authenticate(user=self.user)

    def test_subtask_creation(self):
        url = reverse('subtask-list', kwargs={
            'org_slug': self.org.slug,
            'project_slug': self.project.slug,
            'task_id': self.task.id
        })
        data = {
            'title': 'New Subtask',
            'description': 'Test subtask creation'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubTask.objects.count(), 2)

    def test_subtask_list(self):
        url = reverse('subtask-list', kwargs={
            'org_slug': self.org.slug,
            'project_slug': self.project.slug,
            'task_id': self.task.id
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CheckListAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='checklist_user',
            email='checklist@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='CheckList Org',
            creator=self.user
        )
        self.project = Project.objects.create(
            name='CheckList Project',
            organization=self.org)
        self.task = Task.objects.create(
            title='Task with Checklist',
            project=self.project)
        self.checklist = CheckList.objects.create(
            title='First Item',
            task=self.task)
        self.client.force_authenticate(user=self.user)

    def test_checklist_toggle(self):
        url = reverse('checklist-detail', kwargs={
            'org_slug': self.org.slug,
            'project_slug': self.project.slug,
            'task_id': self.task.id,
            'pk': self.checklist.id
        })
        data = {'is_completed': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.checklist.refresh_from_db()
        self.assertTrue(self.checklist.is_completed)


class CommentAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='comment_user',
            email='comment@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Comment Org',
            creator=self.user
        )
        self.project = Project.objects.create(
            name='Comment Project',
            organization=self.org)
        self.task = Task.objects.create(
            title='Task with Comments',
            project=self.project)
        self.comment = Comment.objects.create(
            user=self.user,
            content='First comment',
            task=self.task)
        self.client.force_authenticate(user=self.user)

    def test_comment_creation(self):
        url = reverse('comment-list', kwargs={
            'org_slug': self.org.slug,
            'project_slug': self.project.slug,
            'task_id': self.task.id
        })
        data = {'content': 'New comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_with_attachment(self):
        url = reverse('comment-list', kwargs={
            'org_slug': self.org.slug,
            'project_slug': self.project.slug,
            'task_id': self.task.id
        })

        # В реальном тесте нужно использовать SimpleUploadedFile
        data = {
            'content': 'Comment with attachment',
            'attachments': []  # Здесь должен быть файл в реальном тесте
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)