from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter

from organizations.urls import org_projects_router
from .views import TaskViewSet, SubTaskViewSet, CommentViewSet

# Вложенные роутеры (продолжение цепочки из organizations/urls.py)
project_tasks_router = NestedDefaultRouter(org_projects_router, r'projects', lookup='project_slug')
project_tasks_router.register(r'tasks', TaskViewSet, basename='project-tasks')

task_subtasks_router = NestedDefaultRouter(project_tasks_router, r'tasks', lookup='task')
task_subtasks_router.register(r'subtasks', SubTaskViewSet, basename='task-subtasks')

subtask_comments_router = NestedDefaultRouter(task_subtasks_router, r'subtasks', lookup='subtask')
subtask_comments_router.register(r'comments', CommentViewSet, basename='subtask-comments')

urlpatterns = [
    path('', include(project_tasks_router.urls)),
    path('', include(task_subtasks_router.urls)),
    path('', include(subtask_comments_router.urls)),
]



# from django.urls import include, path
# from .views import (
#     ProjectCreateView,
#     ProjectDetailView,
#     TaskListView,
#     CommentListView,
#     TaskDetailView,
#     ProjectSettingsView,
#     ProjectViewSet,
#     TaskViewSet,
#     SubTaskViewSet,
#     CommentViewSet
# )

# app_name = 'projects'

# urlpatterns = [
#     path('organization/<slug:org_slug>/create/project/', ProjectCreateView.as_view(), name='create'),
#     path('organization/<slug:org_slug>/project/<slug:project_slug>/', ProjectDetailView.as_view(), name='detail'),
#     path('organization/<slug:org_slug>/project/<slug:project_slug>/settings/', ProjectSettingsView.as_view(), name='settings'),
#     path('organization/<slug:org_slug>/project/<slug:project_slug>/tasks/', TaskListView.as_view(), name='task_list'),
#
#     path('organization/<slug:org_slug>/project/<slug:project_slug>/tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
# #     path('organization/<slug:org_slug>/project/<slug:project_slug>/tasks/<int:task_id>/subtasks/', SubtaskListView.as_view(), name='subtask_list'),
#
#     path('organization/<slug:org_slug>/project/<slug:project_slug>/comments/', CommentListView.as_view(), name='project_comments'),
#     path('organization/<slug:org_slug>/project/<slug:project_slug>/tasks/<int:task_id>/comments/', CommentListView.as_view(), name='task_comments'),
#     path('organization/<slug:org_slug>/project/<slug:project_slug>/tasks/<int:task_id>/subtasks/<int:subtask_id>/comments/', CommentListView.as_view(), name='subtask_comments'),
# ]

# urlpatterns = [
#     path('create/', ProjectCreateView.as_view(), name='create'),
#     path('<slug:project_slug>/', ProjectDetailView.as_view(), name='detail'),
#     path('<slug:project_slug>/settings/', ProjectSettingsView.as_view(), name='settings'),
#     path('<slug:project_slug>/tasks/', TaskListView.as_view(), name='task_list'),
#
#     path('<slug:project_slug>/tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
# #     path('organization/<slug:org_slug>/project/<slug:project_slug>/tasks/<int:task_id>/subtasks/', SubtaskListView.as_view(), name='subtask_list'),
#
#     path('<slug:project_slug>/comments/', CommentListView.as_view(), name='project_comments'),
#     path('<slug:project_slug>/tasks/<int:task_id>/comments/', CommentListView.as_view(), name='task_comments'),
#     path('<slug:project_slug>/tasks/<int:task_id>/subtasks/<int:subtask_id>/comments/', CommentListView.as_view(), name='subtask_comments'),
#
#     path('<slug:project_slug>/tasks/', include([
#         path('', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
#         path('<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-detail'),
#         path('<int:task_id>/subtasks/', include([
#             path('', SubTaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='subtask-list'),
#             path('<int:pk>/', SubTaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='subtask-detail'),
#         ])),
#         path('<int:task_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-comments'),
#     ])),
#     path('<slug:project_slug>/comments/', CommentViewSet.as_view({'get': 'list'}), name='project-comments'),
# ]