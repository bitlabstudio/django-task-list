"""Tests for the models of the ``task_list`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..models import Task, TaskList
from .factories import (
    CategoryFactory,
    ParentFactory,
    TaskAttachmentFactory,
    TaskFactory,
    TaskListFactory,
)


class CategoryTestCase(TestCase):
    """Tests for the ``Category`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Category`` model."""
        category = CategoryFactory()
        self.assertTrue(category.pk)


class ParentTestCase(TestCase):
    """Tests for the ``Parent`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Parent`` model."""
        parent = ParentFactory()
        self.assertTrue(parent.pk)


class TaskTestCase(TestCase):
    """Tests for the ``Task`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Task`` model."""
        task = TaskFactory()
        self.assertTrue(task.pk)


class TaskAttachmentTestCase(TestCase):
    """Tests for the ``TestAttachment``model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``TaskAttachment`` model."""
        attachment = TaskAttachmentFactory()
        self.assertTrue(attachment.pk)


class TaskListManagerTestCase(TestCase):
    """Tests for the ``TaskListManager`` custom manager."""
    longMessage = True

    def setUp(self):
        self.task_list = TaskListFactory()
        self.task = TaskFactory(task_list=self.task_list)
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.task_list.users.add(self.user, self.other_user)

    def test_manager(self):
        """Tests for the ``TaskListManager`` custom manager."""
        template = TaskList.objects.create_template_from_task_list(
            self.task_list, self.user)
        self.assertEqual(TaskList.objects.all().count(), 2, msg=(
            'After creating a template, there should be 2 task lists in the'
            ' database.'))
        self.assertEqual(Task.objects.all().count(), 2, msg=(
            'After creating a template, there should be 2 tasks in the'
            ' database.'))
        self.assertTrue(template.is_template, msg=(
            'Task list should be a template.'))
        self.assertEqual(template.users.count(), 1, msg=(
            'The template should only have 1 user assigned.'))
        self.assertEqual(template.tasks.count(), 1, msg=(
            'The template should have one task.'))

        task_list = TaskList.objects.create_from_template(
            template, 'new', self.user)
        self.assertEqual(TaskList.objects.all().count(), 3, msg=(
            'After creating a task list, there should be 3 task lists in the'
            ' database.'))
        self.assertEqual(Task.objects.all().count(), 3, msg=(
            'After creating a task list, there should be 3 tasks in the'
            ' database.'))
        self.assertFalse(task_list.is_template, msg=(
            'Task list should not be a template.'))
        self.assertEqual(task_list.users.count(), 1, msg=(
            'The task list should still have 1 user assigned.'))
        self.assertEqual(template.tasks.count(), 1, msg=(
            'The task list should have one task.'))


class TaskListTestCase(TestCase):
    """Tests for the ``TaskList`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``TaskList`` model."""
        task_list = TaskListFactory()
        self.assertTrue(task_list.pk)
