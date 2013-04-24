"""Tests for the forms of the ``task_list`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..forms import TaskListCreateForm
from ..models import TaskList


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
