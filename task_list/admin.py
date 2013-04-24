"""Custom model admins for the models of the ``task_list`` app."""
from django.contrib import admin

from .models import (
    Category,
    Parent,
    Task,
    TaskList,
)


class TitleMixin(object):
    """Mixin to get titles of related objects."""
    def task_list_title(self, obj):
        return obj.task_list.title

    def category_title(self, obj):
        return obj.category.title


class CategoryAdmin(admin.ModelAdmin):
    """Custom admin for the ``Category`` model."""
    list_display = ('title',)
    search_fields = ['title']


class ParentAdmin(TitleMixin, admin.ModelAdmin):
    """Custom admin for the ``Parent`` model."""
    list_display = ('task_list_title', )


class TaskAdmin(TitleMixin, admin.ModelAdmin):
    """Custom admin for the ``Task`` model."""
    list_display = ('title', 'task_list_title', 'category_title', 'is_done',
                    'is_example')
    search_fields = ['title', 'description', 'category_title',
                     'task_list_title']


class TaskListAdmin(admin.ModelAdmin):
    """Custom admin for the ``TaskList`` model."""
    list_display = ('title', 'is_template')
    search_fields = ['title']


admin.site.register(TaskList, TaskListAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Category, CategoryAdmin)
