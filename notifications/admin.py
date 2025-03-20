from django.contrib import admin
from .models import User, Organization

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'message', 'is_read', 'created_at')
    list_filter = ('user', 'organization', 'is_read')
    search_fields = ('user', 'organization')

admin.site.register(Notification, NotificationAdmin)