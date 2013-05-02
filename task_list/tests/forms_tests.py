"""Tests for the forms of the ``task_list`` app."""
from datetime import date

from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..forms import (
    TaskCreateForm,
    TaskDoneToggleForm,
    TaskListCreateForm,
    TaskListUpdateForm,
    TaskUpdateForm,
    TemplateForm,
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


class TaskDoneToggleFormTestCase(TestCase):
    """Test for the ``TaskDoneToggleForm`` form class."""
    longMessage = True

    def setUp(self):
        self.task = TaskFactory()
        self.valid_data = {'task': self.task.pk}

    def test_form(self):
        form = TaskDoneToggleForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), msg='The form should be valid.')
        form.save()
        self.assertEqual(type(Task.objects.get().is_done), date, msg=(
            'After save is called, is_done should be a date.'))

        form.save()
        self.assertEqual(Task.objects.get().is_done, None, msg=(
            'After save is called again, is_done should be None again.'))


class TaskListCreateFormTestCase(TestCase):
    """Test for the ``TaskListCreateForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.template = TaskListFactory(is_template=True)
        self.template.users.add(self.user)
        self.task = TaskFactory(task_list=self.template)
        self.valid_data = {
            'title': 'task list title',
        }
        self.from_template_data = {
            'title': 'task list title',
            'template': self.template.pk,
        }

    def test_form_validates_and_saves(self):
        form = TaskListCreateForm(data=self.valid_data, user=self.user)
        self.assertTrue(form.is_valid(), msg=(
            'With correct data, the form should be valid.'))

        instance = form.save()
        self.assertEqual(
            TaskList.objects.filter(is_template=False).count(), 1, msg=(
                'After save is called, there should be one task list in the'
                ' db.'))

        self.assertEqual(instance.users.all()[0], self.user, msg=(
            'After save, the user should be assigned to the list.'))

        form = TaskListCreateForm(data={}, user=self.user)
        self.assertFalse(form.is_valid(), msg=(
            'Without correct data, the form should not be valid.'))

        form = TaskListCreateForm(data=self.from_template_data, user=self.user)
        self.assertTrue(form.is_valid(), msg=(
            'With correct data, the form should be valid. Errors: {0}'.format(
                form.errors)))

        form.save()
        self.assertEqual(
            TaskList.objects.filter(is_template=False).count(), 2, msg=(
                'After save is called, there should be another task list in'
                ' the db.'))
        self.assertEqual(Task.objects.all().count(), 2, msg=(
            'After save is called, there should be two tasks in the db.'))


class TaskListUpdateFormTestCase(TestCase):
    """Test for the ``TaskListUpdateForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task = TaskFactory()
        self.task_list = self.task.task_list
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
        bad_data = self.valid_data.copy()
        bad_data.update({'assigned_to': [self.other_user.pk]})
        form = TaskUpdateForm(data=bad_data, user=self.user,
                              task_list=self.task.task_list,
                              instance=self.task)
        self.assertFalse(form.is_valid(), msg=(
            'With incorrect data, the form should not be valid.'))

        self.task.task_list.users.add(self.other_user)

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


class TemplateFormTestCase(TestCase):
    """Tests for the ``TemplateForm`` form class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task_list = TaskListFactory(title='title')
        self.task_list.users.add(self.user)
        self.task = TaskFactory(task_list=self.task_list)
        self.existing_template = TaskListFactory(is_template=True, title='bar')
        self.existing_template.users.add(self.user)
        self.valid_data = {'title': 'my title'}

    def test_form(self):
        form = TemplateForm(data=self.valid_data, user=self.user,
                            instance=self.task_list)
        self.assertTrue(form.is_valid(), msg=(
            'With correct data, the form should be valid.'))
        instance = form.save()
        self.assertEqual(TaskList.objects.all().count(), 3, msg=(
            'After the list is saved as a template, there should be 3 task'
            ' lists in the db.'))
        self.assertEqual(Task.objects.all().count(), 2, msg=(
            'After the list is saved as a template, there should be 2 tasks'
            ' in the db.'))

        bad_data = self.valid_data.copy()
        bad_data.update({'title': self.existing_template.title})
        form = TemplateForm(data=bad_data, user=self.user,
                            instance=instance)
        self.assertFalse(form.is_valid(), msg=(
            'With incorrect data, the form should not be valid.'))

        data = self.valid_data.copy()
        data.update({'title': 'changed the title'})
        form = TemplateForm(data=data, user=self.user, instance=instance)
        self.assertTrue(form.is_valid(), msg=(
            'With correct data, the form should be valid.'))
        form.save()
        self.assertEqual(TaskList.objects.all().count(), 3, msg=(
            'After template is saved again, there should still be 3 task'
            ' lists in the db.'))
        self.assertEqual(Task.objects.all().count(), 2, msg=(
            'After the template is saved again, there should still be 2 tasks'
            ' in the db.'))
