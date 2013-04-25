"""Custom model admins for the models of the ``task_list`` app."""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (
    Category,
    Parent,
    Task,
    TaskAttachment,
    TaskList,
)


class TitleMixin(object):
    """Mixin to get titles of related objects."""
    def task_list_title(self, obj):
        return obj.task_list.title
    task_list_title.short_description = _('Task list title')

    def category_title(self, obj):
        if obj.category:
            return obj.category.title
    category_title.short_description = _('Category title')


class CategoryAdmin(admin.ModelAdmin):
    """Custom admin for the ``Category`` model."""
    list_display = ('title',)
    search_fields = ['title']


class ParentAdmin(TitleMixin, admin.ModelAdmin):
    """Custom admin for the ``Parent`` model."""
    list_display = ('task_list_title', )


class TaskAdmin(TitleMixin, admin.ModelAdmin):
    """Custom admin for the ``Task`` model."""
    list_display = ('title', 'task_list_title', 'category_title', 'is_done')
    search_fields = ['title', 'description', 'category__title',
                     'task_list__title']


class TaskAttachmentAdmin(admin.ModelAdmin):
    """Custom admin for the ``TaskAttachment`` model."""
    list_display = ('task_title',)

    def task_title(self, obj):
        return obj.task.title
    task_title.short_description = _('Task title')


class TaskListAdmin(admin.ModelAdmin):
    """Custom admin for the ``TaskList`` model."""
    list_display = ('title', 'is_template')
    search_fields = ['title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskAttachment, TaskAttachmentAdmin)
admin.site.register(TaskList, TaskListAdmin)
