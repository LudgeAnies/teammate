from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse
from rest_framework import viewsets, permissions
from .serializers import (
    ProjectSerializer, TaskSerializer,
    SubTaskSerializer, CommentSerializer
)
from .forms import ProjectForm
from .models import Project, Task, SubTask, Comment, UserProjectRole
from organizations.models import Organization

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['organization', 'status']

    def get_queryset(self):
        org_slug = self.kwargs.get('org_slug')
        return Project.objects.filter(
            organization__slug=org_slug,
            organization__userorganizationrole__user=self.request.user
        )

    def perform_create(self, serializer):
        org = Organization.objects.get(slug=self.kwargs['org_slug'])
        serializer.save(organization=org)
        # Автоматически назначаем роль руководителя создателю проекта
        UserProjectRole.objects.create(
            user=self.request.user,
            project=serializer.instance,
            role='leader'
        )

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['project', 'status', 'type', 'priority']

    def get_queryset(self):
        project_slug = self.kwargs.get('project_slug')
        return Task.objects.filter(
            project__slug=project_slug,
            project__organization__userorganizationrole__user=self.request.user
        )

    def perform_create(self, serializer):
        project = Project.objects.get(slug=self.kwargs['project_slug'])
        serializer.save(project=project)

class SubTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return SubTask.objects.filter(
            task__id=task_id,
            task__project__organization__userorganizationrole__user=self.request.user
        )

    def perform_create(self, serializer):
        task = Task.objects.get(id=self.kwargs['task_id'])
        serializer.save(task=task)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if 'project_id' in self.kwargs:
            return Comment.objects.filter(project_id=self.kwargs['project_id'])
        elif 'task_id' in self.kwargs:
            return Comment.objects.filter(task=self.kwargs['task_id'])
        elif 'subtask_id' in self.kwargs:
            return Comment.objects.filter(subtask=self.kwargs['subtask_id'])
        return Comment.objects.none()

    def perform_create(self, serializer):
        if 'project_id' in self.kwargs:
            project = Project.objects.get(id=self.kwargs['project_id'])
            serializer.save(user=self.request.user, project=project)
        elif 'task_id' in self.kwargs:
            task = Task.objects.get(id=self.kwargs['task_id'])
            serializer.save(user=self.request.user, task=task)
        elif 'subtask_id' in self.kwargs:
            subtask = SubTask.objects.get(id=self.kwargs['subtask_id'])
            serializer.save(user=self.request.user, subtask=subtask)

class ProjectCreateView(CreateView):
    form_class = ProjectForm
    template_name = 'projects/create.html'

    # def form_valid(self, form): # изначальный вариант
    #     form.instance.organization = Organization.objects.get(slug=self.kwargs['org_slug'])
    #     return super().form_valid(form)

    def form_valid(self, form): # новый вариант
        form.instance.organization = get_object_or_404(Organization, slug=self.kwargs['org_slug'])
        return super().form_valid(form)


    # def get_success_url(self): # изначальный вариант
    #     return reverse('projects:detail', kwargs={'slug': self.project.slug})

    def get_success_url(self): # новый вариант
        return reverse('projects:detail', kwargs={
            'org_slug': self.object.organization.slug,
            'project_slug': self.object.slug
        })


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'project_slug'
    context_object_name = 'project'

    def get_queryset(self):
        return super().get_queryset().filter(organization__slug=self.kwargs['org_slug'])

class ProjectSettingsView(DetailView):
    pass

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/list.html'
    
    def get_queryset(self):
        return Task.objects.filter(project__slug=self.kwargs['project_slug'])

class TaskDetailView(DetailView):
    model = Task
    template_name = 'projects/detail_task.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        return super().get_queryset().filter(
            project__slug=self.kwargs['project_slug'],
            project__organization__slug=self.kwargs['org_slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(task=self.object).order_by('-created_at')

        context['project'] = get_object_or_404(
            Project,
            slug=self.kwargs['project_slug'],
            organization__slug=self.kwargs['org_slug']
        )
        return context

class CommentListView(ListView):
    model = Comment
    template_name = 'comments/list.html'
    
    def get_queryset(self):
        # Логика для разных типов комментариев
        if 'task_id' in self.kwargs:
            return Comment.objects.filter(task=self.kwargs['task_id'])
        elif 'subtask_id' in self.kwargs:
            return Comment.objects.filter(subtask=self.kwargs['subtask_id'])
        else:
            return Comment.objects.filter(project__slug=self.kwargs['project_slug'])

