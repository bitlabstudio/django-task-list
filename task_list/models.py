"""Models for the ``task_list`` app."""
from copy import deepcopy

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.file import FilerFileField

from .constants import PRIORITY_CHOICES


class Category(models.Model):
    """
    Used to group tasks under one category.

    :title: The title of the category.

    """
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=256,
    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Parent(models.Model):
    """
    Used to bind a TaskList to an external model.

    :content_type: If the related list belongs to a certain object
      (i.e. a Wedding), this should be the object's ContentType.
    :object_id: If the related list belongs to a certain object
      (i.e. a Wedding), this should be the object's ID.
    :task_list: The task list the content object belongs to.

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
    :category: The ``Category`` this task belongs to.
    :description: A further description about the task.
    :due_date: Lets the user choose a due date for this task.
    :is_done: If the task is done, this holds the datetime, else it is None.
    :priority: Lets the user choose a priority level for this task.
    :task_list: The ``TaskList`` this task belongs to.
    :title: The title of the task.

    """
    assigned_to = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Users'),
        related_name='tasks',
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

    priority = models.CharField(
        verbose_name=_('Priority'),
        max_length=8,
        choices=PRIORITY_CHOICES,
        default='3',
    )

    task_list = models.ForeignKey(
        'task_list.TaskList',
        verbose_name=_('Task list'),
        related_name='tasks',
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=256,
    )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['due_date', 'priority', 'title']


class TaskAttachment(models.Model):
    """
    Used to attach files to a tasks.

    :file: Field that holds the file.
    :task: The task the file is attached to.

    """
    file = FilerFileField(
        verbose_name=_('Attachment'),
        blank=True, null=True,
    )

    task = models.ForeignKey(
        'task_list.Task',
        verbose_name=_('Task'),
        related_name='attachments',
    )

    def __unicode__(self):
        # TODO do something here
        return self.task.title


class TaskListManager(models.Manager):
    """Custom manager for the ``TaskList`` model."""
    def create_from_template(self, template, new_title, user):
        """Creates a new task list from a template task list."""
        # copy the template
        new_task_list = deepcopy(template)
        new_task_list.id = None
        new_task_list.is_template = False
        new_task_list.title = new_title
        new_task_list.save()
        new_task_list.users.add(user)
        # copy all tasks
        for task in template.tasks.all():
            new_task = deepcopy(task)
            new_task.id = None
            new_task.task_list = new_task_list
            new_task.save()
        return new_task_list

    def create_template_from_task_list(self, task_list, user):
        """Creates a new template task list from an existing task list."""
        # copy the instance
        new_task_list = deepcopy(task_list)
        new_task_list.id = None
        new_task_list.is_template = True
        new_task_list.save()
        # clear users and set the request user only
        new_task_list.users.add(user)
        # copy all tasks
        for task in task_list.tasks.all():
            new_task = deepcopy(task)
            new_task.id = None
            new_task.is_done = None
            new_task.due_date = None
            new_task.task_list = new_task_list
            new_task.save()
            new_task.assigned_to.clear()
        return new_task_list


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

    objects = TaskListManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
