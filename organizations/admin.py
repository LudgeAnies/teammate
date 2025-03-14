from django.contrib import admin
from .models import Organization, UserOrganizationRole

# Inline для отображения ролей пользователей в организации
class UserOrganizationRoleInline(admin.TabularInline):
    model = UserOrganizationRole
    extra = 1
    
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'invite_code', 'created_at')
    search_fields = ('name', 'invite_code')
    inlines = [UserOrganizationRoleInline]

class UserOrganizationRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role')
    list_filter = ('role', 'organization')
    search_fields = ('user__username', 'organization__name')

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(UserOrganizationRole, UserOrganizationRoleAdmin)