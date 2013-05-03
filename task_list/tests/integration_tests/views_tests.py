"""Tests for the views of the ``task_list`` app."""
from mock import Mock, patch

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from ...forms import (
    TaskCreateForm,
    TaskListCreateForm,
    TaskListUpdateForm,
    TaskUpdateForm,
    TemplateForm,
)
from ..factories import (
    DummyModelFactory,
    ParentFactory,
    TaskFactory,
    TaskListFactory,
)
from ..test_app.models import DummyModel


# ======
# Mixins
# ======

class PatchedViewTestMixin(ViewTestMixin):
    def should_redirect_to_login_when_anonymous(self):
        """Custom method to overwrite the one from django_libs."""
        url = self.get_url()
        resp = self.client.get(url)
        self.assertRedirects(resp, '{0}?next={1}'.format(
            reverse('dummy_login'), url))


# =====
# Tests
# =====


class TaskCreateViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TaskCreateView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'task_create'

    def get_view_kwargs(self):
        return {'task_list_pk': self.task_list.pk,
                'ctype_pk': self.parent.content_type.pk,
                'obj_pk': self.parent.object_id}

    def setUp(self):
        self.user = UserFactory()
        self.task_list = TaskListFactory()
        self.task_list.users.add(self.user)
        self.parent = ParentFactory(task_list=self.task_list,
                                    content_object__user=self.user)

    @patch.object(TaskCreateForm, 'is_valid')
    @patch.object(TaskCreateForm, 'save')
    def test_view(self, save_mock, is_valid_mock):
        """Test for the ``TaskCreateView`` view class."""
        is_valid_mock.return_value = True
        save_mock.return_value.task_list = Mock(pk=1)

        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='post', data={})
        self.is_not_callable(user=UserFactory())


class TaskDeleteViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests or the ``TaskDeleteView`` view class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task = TaskFactory()
        self.task.task_list.users.add(self.user)

    def get_view_name(self):
        return 'task_delete'

    def get_view_kwargs(self):
        return {'pk': self.task.pk}

    def test_view(self):
        """Test for the ``TaskDeleteView`` view class."""
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_not_callable(user=UserFactory(), message=(
            'The view should not be callable by other users.'))
        self.is_callable(user=self.user, method='post', data={},
                         and_redirects_to=reverse('task_list', kwargs={
                             'task_list_pk': self.task.task_list.pk}))


class TaskDoneToggleViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TaskDoneToggleView`` view class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.task = TaskFactory()
        self.task.task_list.users.add(self.user)

    def get_view_name(self):
        return 'task_toggle'

    def get_view_kwargs(self):
        return {'pk': self.task.pk}

    def test_view(self):
        """Test for the ``TaskDoneToggleView`` view class."""
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='post', data={'next': 'foo'}, message=(
            'With invalid data, and next parameter, the view should also be'
            ' callable'))
        self.is_callable(method='post', data={'task': self.task.pk})


class TaskListCreateViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TaskListCreateView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'task_list_create'

    def get_view_kwargs(self):
        return {'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk}

    def setUp(self):
        self.user = UserFactory()
        self.ctype_pk = ContentType.objects.get_for_model(DummyModel).pk
        self.obj_pk = DummyModelFactory(user=self.user).pk

    @patch.object(TaskListCreateForm, 'is_valid')
    @patch.object(TaskListCreateForm, 'save')
    def test_view(self, save_mock, is_valid_mock):
        """Test for the ``TaskListCreateView`` view class."""
        save_mock.return_value = Mock(pk=1)
        is_valid_mock.return_value = True

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
        self.ctype_pk = ContentType.objects.get_for_model(DummyModel).pk
        self.obj_pk = DummyModelFactory(user=self.user).pk

    def get_view_name(self):
        return 'task_list_list'

    def get_view_kwargs(self):
        return {'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk}

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_not_callable(kwargs={'ctype_pk': 999, 'obj_pk': 1234})


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

    @patch.object(TaskListUpdateForm, 'is_valid')
    @patch.object(TaskListUpdateForm, 'save')
    def test_view(self, save_mock, is_valid_mock):
        """Test for the ``TaskListUpdateView`` view class."""
        save_mock.return_value = Mock(pk=1)
        is_valid_mock.return_value = True

        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='post', data={})
        self.is_not_callable(user=UserFactory(), message=(
            'The view should not be callable by other users.'))


class TaskListViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TaskListView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'task_list'

    def get_view_kwargs(self):
        return {'task_list_pk': self.task.task_list.pk}

    def setUp(self):
        self.user = UserFactory()
        self.task = TaskFactory()
        self.task.task_list.users.add(self.user)

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_not_callable(user=UserFactory())


class TaskUpdateViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TaskUpdateView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'task_update'

    def get_view_kwargs(self):
        return {'pk': self.task.pk}

    def setUp(self):
        self.user = UserFactory()
        self.task = TaskFactory()
        self.task.task_list.users.add(self.user)

    @patch.object(TaskUpdateForm, 'is_valid')
    @patch.object(TaskUpdateForm, 'save')
    def test_view(self, save_mock, is_valid_mock):
        """Test for the ``TaskUpdateView`` view class."""
        is_valid_mock.return_value = True
        save_mock.return_value.task_list = Mock(pk=1)

        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='post', data={})
        self.is_not_callable(user=UserFactory())


class TemplateDeleteViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests or the ``TemplateDeleteView`` view class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.template = TaskListFactory(is_template=True)
        self.template.users.add(self.user)

    def get_view_name(self):
        return 'template_delete'

    def get_view_kwargs(self):
        return {'pk': self.template.pk}

    def test_view(self):
        """Test for the ``TemplateDeleteView`` view class."""
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_not_callable(user=UserFactory(), message=(
            'The view should not be callable by other users.'))
        self.is_callable(user=self.user, method='post', data={},
                         and_redirects_to=reverse('template_list'))


class TemplateListViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TemplateListView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'template_list'

    def setUp(self):
        self.user = UserFactory()

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)


class TemplateUpdateViewTestCase(PatchedViewTestMixin, TestCase):
    """Tests for the ``TemplateUpdateView`` view class."""
    longMessage = True

    def get_view_name(self):
        return 'template_update'

    def get_view_kwargs(self):
        return {'pk': self.task_list.pk}

    def setUp(self):
        self.user = UserFactory()
        self.task_list = TaskListFactory()
        self.task_list.users.add(self.user)

    @patch.object(TemplateForm, 'save')
    @patch.object(TemplateForm, 'is_valid')
    def test_view(self, is_valid_mock, save_mock):
        """Test for the ``TaskListUpdateView`` view class."""
        is_valid_mock.return_value = True
        save_mock.return_value = self.task_list

        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(data={'next': 'foo'}, message=(
            'If called with a next parameter, the view should be callable.'))
        self.is_callable(method='post', data={'next': 'foo'}, message=(
            'If posted with a next parameter, the view should be callable.'))
        self.is_callable(method='post', data={})
        self.is_not_callable(user=UserFactory(), message=(
            'The view should not be callable by other users.'))
