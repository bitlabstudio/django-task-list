"""Tests for the models of the ``task_list`` app."""
from django.test import TestCase

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


class TaskListTestCase(TestCase):
    """Tests for the ``TaskList`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``TaskList`` model."""
        task_list = TaskListFactory()
        self.assertTrue(task_list.pk)
