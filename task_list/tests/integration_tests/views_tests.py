"""Tests for the views of the ``task_list`` app."""
from mock import Mock

from django.core.urlresolvers import reverse
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from ...forms import TaskListCreateForm, TaskListUpdateForm
from ..factories import TaskListFactory


# ======
# Mixins
# ======

class PatchedViewTestMixin(ViewTestMixin):
    def should_redirect_to_login_when_anonymous(self):
        """Custom method to overwrite the one from django_libs."""
        url = self.get_url()
        resp = self.client.get(url)
        self.assertRedirects(resp, '{0}?next={1}'.format('/', url))


# =====
# Tests
# =====

class TaskListCreateViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TaskListCreateView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'task_list_create'

    def setUp(self):
        self.user = UserFactory()
        self.old_is_valid = TaskListCreateForm.is_valid
        self.old_save = TaskListCreateForm.save
        TaskListCreateForm.is_valid = Mock(return_value=True)
        false_list = Mock(pk=1)
        TaskListCreateForm.save = Mock(return_value=false_list)

    def tearDown(self):
        TaskListCreateForm.is_valid = self.old_is_valid
        TaskListCreateForm.save = self.old_save

    def test_view(self):
        """Test for the ``TaskListCreateView`` view class."""
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='post', data={})


class TaskListDeleteViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests or the ``TaskListDeleteView`` view class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task_list = TaskListFactory()
        self.task_list.users.add(self.user)

    def get_view_name(self):
        return 'task_list_delete'

    def get_view_kwargs(self):
        return {'pk': self.task_list.pk}

    def test_view(self):
        """Test for the ``TaskListDeleteView`` view class."""
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_not_callable(user=UserFactory(), message=(
            'The view should not be callable by other users.'))
        self.is_callable(user=self.user, method='post', data={},
                         and_redirects_to=reverse('task_list_list'))


class TaskListListViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests fo the ``TaskListListView`` view class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task_list = TaskListFactory()
        self.task_list.users.add(self.user)

    def get_view_name(self):
        return 'task_list_list'

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)


class TaskListUpdateViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TaskListCreateView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'task_list_update'

    def get_view_kwargs(self):
        return {'pk': self.task_list.pk}

    def setUp(self):
        self.user = UserFactory()
        self.task_list = TaskListFactory()
        self.task_list.users.add(self.user)
        self.old_is_valid = TaskListUpdateForm.is_valid
        self.old_save = TaskListUpdateForm.save
        TaskListUpdateForm.is_valid = Mock(return_value=True)
        false_list = Mock(pk=1)
        TaskListUpdateForm.save = Mock(return_value=false_list)

    def tearDown(self):
        TaskListUpdateForm.is_valid = self.old_is_valid
        TaskListUpdateForm.save = self.old_save

    def test_view(self):
        """Test for the ``TaskListUpdateView`` view class."""
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='post', data={})
        self.is_not_callable(user=UserFactory(), message=(
            'The view should not be callable by other users.'))
