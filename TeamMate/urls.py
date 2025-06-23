from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from users.views import YandexSocialAuthView
from users.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('accounts/', include('allauth.urls')),
    path('api/users/', include('users.urls')),
    path('api/organizations/', include('organizations.urls')),
    path('api/', include('projects.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.social.urls')),
    path("api/auth/custom-login/", CustomLoginView.as_view(), name="custom-login"),
    path("api/auth/social/yandex/", YandexSocialAuthView.as_view(), name="yandex_social_auth"),
    #re_path(r'^.*$', TemplateView.as_view(template_name='base.html')),
    re_path(r'^(?!admin|api|static|media).*$', TemplateView.as_view(template_name='base.html')),
]



# from django.contrib import admin
# from django.urls import include, path, re_path
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.generic import TemplateView
# from rest_framework import routers
# from rest_framework_nested import routers
# from projects.views import (
#     ProjectViewSet, TaskViewSet,
#     SubTaskViewSet, CommentViewSet
# )
# from organizations.views import OrganizationViewSet
#
# router = routers.DefaultRouter()
# router.register(r'organizations', OrganizationViewSet, basename='organization')
# router.register(r'users', UserViewSet, basename='user')
#
# # Вложенность: organizations -> projects
# org_projects_router = routers.NestedDefaultRouter(router, r'organizations', lookup='org')
# org_projects_router.register(r'projects', ProjectViewSet, basename='organization-projects')
#
# # projects -> tasks
# project_tasks_router = routers.NestedDefaultRouter(org_projects_router, r'projects', lookup='project')
# project_tasks_router.register(r'tasks', TaskViewSet, basename='project-tasks')
#
# # tasks -> subtasks
# task_subtasks_router = routers.NestedDefaultRouter(project_tasks_router, r'tasks', lookup='task')
# task_subtasks_router.register(r'subtasks', SubTaskViewSet, basename='task-subtasks')
#
# # subtasks -> comments
# subtask_comments_router = routers.NestedDefaultRouter(task_subtasks_router, r'subtasks', lookup='subtask')
# subtask_comments_router.register(r'comments', CommentViewSet, basename='subtask-comments')
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('api/', include(org_projects_router.urls)),
#     path('api/', include(project_tasks_router.urls)),
#     path('api/', include(task_subtasks_router.urls)),
#     path('api/', include(subtask_comments_router.urls)),
#     # SPA fallback:
#     # re_path(r'^.*$', TemplateView.as_view(template_name='base.html')),
# ]

# router = routers.DefaultRouter()
# router.register(r'projects', ProjectViewSet, basename='proj_router')
# router.register(r'organizations', ProjectViewSet, basename='org_router')
# # router.register(r'tasks', TaskViewSet, basename='task')
# # router.register(r'subtasks', SubTaskViewSet, basename='subtask')
# # router.register(r'comments', CommentViewSet, basename='comment')
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/auth/', include('rest_framework.urls')),
#     path('api/', include(router.urls)),
#
#     path('accounts/', include('allauth.urls')),
#     # path('accounts/', include('otp_allauth.urls')), #
#     # path('accounts/', include(allauth_2fa_urls)),
#     path('accounts/mfa/', include('allauth.mfa.urls')),
#     path('organizations/', include(('organizations.urls', 'organizations'), namespace="organizations")),
#     path('api/organizations/<slug:org_slug>/', include([
#         path('projects/', include(('projects.urls', 'projects'), namespace="projects")),
#     ])),
#
#     re_path(r'^.*$', TemplateView.as_view(template_name='base.html')),
#     # path('projects/', include(('projects.urls', 'projects'), namespace="projects")),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # на проде медиафайлы должны обслуживаться сервером
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
