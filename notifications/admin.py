from django.contrib import admin
from .models import CustomUser, Organization, Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'message', 'is_read', 'created_at')
    list_filter = ('user', 'organization', 'is_read')
    search_fields = ('user__first_name', 'user__last_name', 'organization__name')

admin.site.register(Notification, NotificationAdmin)