from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import OrganizationViewSet, InviteToOrganizationAPI, MyOrganizationsAPI
from projects.views import ProjectViewSet

# Основной роутер организаций
router = DefaultRouter()
router.register(r'', OrganizationViewSet, basename='organization')

# Вложенный роутер проектов
org_projects_router = NestedDefaultRouter(router, r'', lookup='org_slug')
org_projects_router.register(r'projects', ProjectViewSet, basename='organization-projects')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(org_projects_router.urls)),
    path('invite/', InviteToOrganizationAPI.as_view(), name='invite_org_api'),
    path('my/', MyOrganizationsAPI.as_view(), name='my-org-api'),
]



# from django.urls import path, include
# from .views import OrganizationCreateView, OrganizationDetailView, OrganizationSettingsView, OrganizationInviteView, OrganizationListView
# from .views import InviteToOrganizationAPI, MyOrganizationsAPI
#
# app_name = 'organizations'
#
# # urlpatterns = [
# #     path('invite/', OrganizationInviteView.as_view(), name='invite'),
# #     path('create/', OrganizationCreateView.as_view(), name='create'),
# #     path('organizations_list', OrganizationListView.as_view(), name='org_list'),
# #     path('<slug:slug>/', OrganizationDetailView.as_view(), name='detail'),
# #     path('organization/<slug:slug>/settings/', OrganizationSettingsView.as_view(), name='settings'),
# #     #path('organization/<slug:slug>/notifications/', include('notifications.urls')),
# # ]
# urlpatterns = [
#     path('invite/', InviteToOrganizationAPI.as_view(), name='invite_org_api'),
#     path('my/', MyOrganizationsAPI.as_view(), name='my_organizations_api'),
# ]