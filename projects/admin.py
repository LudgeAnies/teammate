from django.contrib import admin
from .models import Project, UserProjectRole, Task, SubTask, TaskAssignment, Comment, CommentAttachment, CheckList, History, TaskDependency

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

class CheckListInline(admin.TabularInline):
    model = CheckList
    extra = 1

class TaskDependencyInline(admin.TabularInline):
    model = TaskDependency
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'status', 'deadline')
    list_filter = ('status', 'organization')
    search_fields = ('name', 'organization__name')
    inlines = [UserProjectRoleInline, TaskInline]

class UserProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'can_edit')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'type', 'priority', 'start_date', 'end_date', 'created_at', 'updated_at')
    list_filter = ('status', 'type', 'project')
    search_fields = ('title', 'project__name')
    inlines = [SubTaskInline, TaskAssignmentInline]

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'priority', 'start_date', 'end_date')
    list_filter = ('status', 'task')
    search_fields = ('title', 'task__title')

class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'role')
    list_filter = ('role', 'task')
    search_fields = ('task__title', 'user__first_name', 'user__last_name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('content', 'user__first_name', 'user__last_name')
    inlines = [CommentAttachmentInline]

class CommentAttachmentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('comment__content', 'file')

class CheckListAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'subtask', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'task', 'subtask')
    search_fields = ('title', 'task__title', 'subtask__title')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at', 'project', 'task', 'subtask')
    list_filter = ('created_at', 'user', 'project', 'task', 'subtask')
    search_fields = ('action', 'user__first_name', 'user__last_name')

class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ('task', 'depends_on', 'created_at')
    list_filter = ('created_at', 'task', 'depends_on')
    search_fields = ('task__title', 'depends_on__title')

admin.site.register(Project, ProjectAdmin)
admin.site.register(UserProjectRole)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(TaskAssignment, TaskAssignmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentAttachment, CommentAttachmentAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(TaskDependency, TaskDependencyAdmin)