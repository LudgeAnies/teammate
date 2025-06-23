from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from projects.models import Project, Task
from organizations.models import Organization
from users.models import CustomUser
from unittest.mock import patch

# "email": "test1@example.com",
#         "username": "testuser1",
#         "first_name": "Тест",
#         "last_name": "Юзер",
#         "password": "qwerty123456",
#         "re_password": "qwerty123456",

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='test',
            last_name='user',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Test Org',
            # creator=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        url = reverse('project-list', kwargs={'org_slug': self.org.slug})
        data = {
            'name': 'новый проект',
            'description': 'описание'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)

    @patch('projects.services.calendar_api.ProductionCalendarAPI.is_working_day')
    def test_create_project_with_invalid_deadline(self, mock_is_working_day):
        mock_is_working_day.return_value = False

        url = reverse('project-list', kwargs={'org_slug': self.org.slug})
        data = {
            'name': 'New Project',
            'deadline': '2025-01-01'  # Нерабочий день
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('deadline', response.data)


class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='тестовая организация',
            # creator=self.user
        )
        self.project = Project.objects.create(
            name='тестовый проект',
            organization=self.org)
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        url = reverse('task-list', kwargs={
            'org_slug': self.org.slug,
            'project_slug': self.project.slug
        })
        data = {
            'title': 'новая задача',
            'start_date': '2025-02-10T09:00:00Z',
            'end_date': '2025-02-12T18:00:00Z'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)