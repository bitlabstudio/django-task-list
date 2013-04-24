"""Models for the ``task_list`` app."""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.file import FilerFileField

from .constants import PRIORITY_CHOICES


class Category(models.Model):
    """
    Used to groub tasks under one category.

    :title: The title of the category.

    """
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=256,
    )

    def __unicode__(self):
        return self.title


class Parent(models.Model):
    """
    Used to bind a TaskList to an external model.

    :content_type: If this image belongs to a certain object (i.e. a Wedding),
      this should be the object's ContentType.
    :object_id: If this image belongs to a certain object (i.e. a Wedding),
      this should be the object's ID.
    """
    content_type = models.ForeignKey(
        ContentType,
        null=True, blank=True,
    )

    object_id = models.PositiveIntegerField(
        null=True, blank=True
    )

    content_object = generic.GenericForeignKey('content_type', 'object_id')

    task_list = models.ForeignKey(
        'task_list.TaskList',
        verbose_name=_('parent'),
    )


class Task(models.Model):
    """
    Holds all information about the actual task.

    :assigned_to: Can point to one or more users, assigned to this task.
    :attachment: A file attachment.
    :category: The ``Category`` this task belongs to.
    :description: A further description about the task.
    :due_date: Lets the user chose a due date for this task.
    :is_done: If the task is done, this holds the datetime, else it is None.
    :is_example: Is True if this task was generated as pre-filled example.
    :priority: Lets the user chose a priority level for this task.
    :task_list: The ``TaskList`` this task belongs to.
    :title: The title of the task.

    """
    assigned_to = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Users'),
        related_name='task_lists',
    )

    attachment = FilerFileField(
        verbose_name=_('Attachment'),
        blank=True, null=True,
    )

    category = models.ForeignKey(
        'task_list.Category',
        verbose_name=_('Category'),
        blank=True, null=True,
    )

    description = models.TextField(
        verbose_name=_('Description'),
        max_length=4000,
        blank=True,
    )

    due_date = models.DateField(
        verbose_name=_('Due date'),
        blank=True, null=True,
    )

    is_done = models.DateField(
        verbose_name=_('Is done'),
        blank=True, null=True,
    )

    is_example = models.BooleanField(
        verbose_name=_('Is example'),
        default=False,
    )

    priority = models.CharField(
        verbose_name=_('Priority'),
        max_length=8,
        choices=PRIORITY_CHOICES,
        default='1',
    )

    task_list = models.ForeignKey(
        'task_list.TaskList',
        verbose_name=_('Task list'),
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=256,
    )

    def __unicode__(self):
        return self.title


class TaskList(models.Model):
    """
    Holds general information about a task list.

    :users: The users, that are able to access this list.
    :title: The title of this task list.
    :is_template: True, if the task list is saved as non-editable template that
        can be used to initialize a new list.

    """
    users = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Users'),
        related_name='task_lists',
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=256,
    )

    is_template = models.BooleanField(
        verbose_name=_('Is template'),
        default=False,
    )

    def __unicode__(self):
        return self.title
