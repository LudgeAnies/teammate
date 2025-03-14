from django.contrib import admin
from .models import Project, UserProjectRole, Task, SubTask, TaskAssignment, Comment, CommentAttachment

# Inline для отображения ролей пользователей в проекте
class UserProjectRoleInline(admin.TabularInline):
    model = UserProjectRole
    extra = 1

# Inline для отображения задач в проекте
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

# Inline для отображения подзадач в задаче
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

# Inline для отображения назначений задач
class TaskAssignmentInline(admin.TabularInline):
    model = TaskAssignment
    extra = 1

# Inline для отображения вложений в комментариях
class CommentAttachmentInline(admin.TabularInline):
    model = CommentAttachment
    extra = 1

# Админка для Project
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'status', 'deadline')
    list_filter = ('status', 'organization')
    search_fields = ('name', 'organization__name')
    inlines = [UserProjectRoleInline, TaskInline]

# Админка для Task
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'type', 'deadline')
    list_filter = ('status', 'type', 'project')
    search_fields = ('title', 'project__name')
    inlines = [SubTaskInline, TaskAssignmentInline]

# Админка для SubTask
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status')
    list_filter = ('status', 'task')
    search_fields = ('title', 'task__title')

# Админка для TaskAssignment
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'role')
    list_filter = ('role', 'task')
    search_fields = ('task__title', 'user__username')

# Админка для Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('content', 'user__username')
    inlines = [CommentAttachmentInline]

# Админка для CommentAttachment
class CommentAttachmentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('comment__content', 'file')

# Регистрация моделей
admin.site.register(Project, ProjectAdmin)
admin.site.register(UserProjectRole)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(TaskAssignment, TaskAssignmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentAttachment, CommentAttachmentAdmin)