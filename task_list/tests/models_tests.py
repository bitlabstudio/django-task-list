"""Tests for the models of the ``task_list`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..models import (
    Category,
    Parent,
    Task,
    TaskList,
)
from .factories import TaskListFactory


class CategoryTestCase(TestCase):
    """Tests for the ``Category`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Category`` model."""
        category = Category(title='category')
        self.assertTrue(category)
        category.save()
        self.assertEqual(Category.objects.all().count(), 1, msg=(
            'There should be one category in the db.'))


class ParentTestCase(TestCase):
    """Tests for the ``Parent`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Parent`` model."""
        parent = Parent(task_list=TaskListFactory(),
                        content_object=UserFactory())
        self.assertTrue(parent)
        parent.save()
        self.assertEqual(Parent.objects.all().count(), 1, msg=(
            'There should be one parent in the db.'))


class TaskTestCase(TestCase):
    """Tests for the ``Task`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Task`` model."""
        task = Task(title='task', task_list=TaskListFactory())
        self.assertTrue(task)
        task.save()
        self.assertEqual(Task.objects.all().count(), 1, msg=(
            'There should be one task in the db.'))


class TaskListTestCase(TestCase):
    """Tests for the ``TaskList`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``TaskList`` model."""
        task_list = TaskList(title='task_list')
        task_list.users.add(UserFactory())
        self.assertTrue(task_list)
        task_list.save()
        self.assertEqual(TaskList.objects.all().count(), 1, msg=(
            'There should be one task_list in the db.'))
