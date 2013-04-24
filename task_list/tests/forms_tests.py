"""Tests for the forms of the ``task_list`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..forms import (
    TaskCreateForm,
    TaskListCreateForm,
    TaskListUpdateForm,
    TaskUpdateForm,
)
from ..models import Task, TaskList
from .factories import TaskFactory, TaskListFactory


class TaskCreateFormTestCase(TestCase):
    """Test for the ``TaskCreateForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task_list = TaskListFactory()
        self.task_list.users.add(self.user)
        self.valid_data = {
            'title': 'task title',
        }

    def test_form_validates_and_saves(self):
        form = TaskCreateForm(data=self.valid_data, user=self.user,
                              task_list=self.task_list)
        self.assertTrue(form.is_valid(), msg=(
            'With correct data, the form should be valid.'))

        instance = form.save()
        self.assertEqual(TaskList.objects.all().count(), 1, msg=(
            'After save is called, there should be one task in the db.'))

        self.assertEqual(instance.assigned_to.all()[0], self.user, msg=(
            'After save, the user should be assigned to the task.'))

        form = TaskCreateForm(data={}, user=self.user,
                              task_list=self.task_list)
        self.assertFalse(form.is_valid(), msg=(
            'Without correct data, the form should not be valid.'))


class TaskListCreateFormTestCase(TestCase):
    """Test for the ``TaskListCreateForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.valid_data = {
            'title': 'task list title',
        }

    def test_form_validates_and_saves(self):
        form = TaskListCreateForm(data=self.valid_data, user=self.user)
        self.assertTrue(form.is_valid(), msg=(
            'With correct data, the form should be valid.'))

        instance = form.save()
        self.assertEqual(TaskList.objects.all().count(), 1, msg=(
            'After save is called, there should be one task list in the db.'))

        self.assertEqual(instance.users.all()[0], self.user, msg=(
            'After save, the user should be assigned to the list.'))

        form = TaskListCreateForm(data={}, user=self.user)
        self.assertFalse(form.is_valid(), msg=(
            'Without correct data, the form should not be valid.'))


class TaskListUpdateFormTestCase(TestCase):
    """Test for the ``TaskListUpdateForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task_list = TaskListFactory()
        self.task_list.users.add(self.user)
        self.other_user = UserFactory()
        self.valid_data = {
            'title': 'task list title',
            'users': [self.other_user.pk],
        }

    def test_form_validates_and_saves(self):
        form = TaskListUpdateForm(data=self.valid_data, user=self.user,
                                  instance=self.task_list)
        self.assertTrue(form.is_valid(), msg=(
            'With correct data, the form should be valid.'))

        instance = form.save()
        self.assertEqual(TaskList.objects.all().count(), 1, msg=(
            'After save is called, there should be one task list in the db.'))

        self.assertEqual(self.task_list.users.count(), 2, msg=(
            'There should be two users assigned.'))

        self.assertEqual(instance.users.all()[0], self.user, msg=(
            'After save, the user should be assigned to the list.'))

        form = TaskListUpdateForm(data={}, user=self.user,
                                  instance=self.task_list)
        self.assertFalse(form.is_valid(), msg=(
            'Without correct data, the form should not be valid.'))


class TaskUpdateFormTestCase(TestCase):
    """Test for the ``TaskUpdateForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task = TaskFactory()
        self.task.task_list.users.add(self.user)
        self.task.assigned_to.add(self.user)
        self.other_user = UserFactory()
        self.valid_data = {
            'title': 'task list title',
            'assigned_to': [self.other_user.pk],
            'priority': '3',
        }

    def test_form_validates_and_saves(self):
        form = TaskUpdateForm(data=self.valid_data, user=self.user,
                              task_list=self.task.task_list,
                              instance=self.task)
        self.assertTrue(form.is_valid(), msg=(
            'With correct data, the form should be valid.'))

        instance = form.save()
        self.assertEqual(Task.objects.all().count(), 1, msg=(
            'After save is called, there should be one task in the db.'))

        self.assertEqual(self.task.assigned_to.count(), 2, msg=(
            'There should be two users assigned.'))

        self.assertEqual(instance.assigned_to.all()[0], self.user, msg=(
            'After save, the user should be assigned to the task.'))

        form = TaskUpdateForm(data={}, user=self.user,
                              task_list=self.task.task_list,
                              instance=instance)
        self.assertFalse(form.is_valid(), msg=(
            'Without correct data, the form should not be valid.'))
