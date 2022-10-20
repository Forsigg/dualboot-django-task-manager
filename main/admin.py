from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Tag
from .models import Task


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'executor', 'created_at', 'edited_at',
                    'deadline', 'author', 'state', 'get_tags')


task_manager_admin_site.register(User, UserAdmin)

