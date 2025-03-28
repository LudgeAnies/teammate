from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# # кастомный UserAdmin для отображения дополнительных полей
# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type', 'is_active')
#     list_filter = ('user_type', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'phone_number', 'avatar', 'user_type')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )

# admin.site.register(User, CustomUserAdmin)

# class CustomUserAdmin(UserAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'phone_number', 'user_type', 'is_active', 'is_staff')
#     list_filter = ('user_type', 'is_active', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar', 'user_type')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password', 'password2'),
#         }),
#     )
#     ordering = ('email',)
#     search_fields = ('email', 'first_name', 'last_name')

# admin.site.register(CustomUser, CustomUserAdmin)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password'),
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'avatar'),
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Тип пользователя', {
            'fields': ('user_type',),
        }),
        ('Даты', {
            'fields': ('last_login', 'created_at', 'updated_at'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'user_type', 'is_active', 'is_staff'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)