from rest_framework import permissions
from organizations.models import UserOrganizationRole
from .models import UserProjectRole

class IsOrganizationAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        org_slug = view.kwargs.get('org_slug')
        return UserOrganizationRole.objects.filter(
            user=request.user,
            organization__slug=org_slug,
            role='admin'
        ).exists()

class IsProjectLeader(permissions.BasePermission):
    def has_permission(self, request, view):
        project_slug = view.kwargs.get('project_slug')
        return UserProjectRole.objects.filter(
            user=request.user,
            project__slug=project_slug,
            role='leader'
        ).exists()

class IsProjectManagerOrLeader(permissions.BasePermission):
    def has_permission(self, request, view):
        project_slug = view.kwargs.get('project_slug')
        return UserProjectRole.objects.filter(
            user=request.user,
            project__slug=project_slug,
            role__in=['manager', 'leader']
        ).exists()

class IsTaskResponsible(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.taskassignment_set.filter(
            user=request.user,
            role='responsible'
        ).exists()