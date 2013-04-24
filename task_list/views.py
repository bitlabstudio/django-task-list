"""Views for the ``task_list`` app."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    TaskCreateForm,
    TaskListCreateForm,
    TaskListUpdateForm,
    TaskUpdateForm,
)
from .models import Task, TaskList


# ======
# Mixins
# ======

class LoginRequiredMixin(object):
    """Mixin to add a basic login required decorated dispatch method."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class TaskCRUDViewMixin(object):
    """Mixin to add common methods to the task CRUD views."""
    pk_url_kwarg = 'task_pk'

    def get_form_kwargs(self):
        kwargs = super(TaskCRUDViewMixin, self).get_form_kwargs()
        kwargs.update({'user': self.user, 'task_list': self.task_list})
        return kwargs

    def get_success_url(self):
        return reverse('task_update', kwargs={
            'pk': self.task_list.pk, 'task_pk': self.object.pk})


class TaskListCRUDViewMixin(object):
    """Mixin to add common methods to the task list CRUD views."""
    def get_form_kwargs(self):
        kwargs = super(TaskListCRUDViewMixin, self).get_form_kwargs()
        kwargs.update({'user': self.user})
        return kwargs

    def get_success_url(self):
        return reverse('task_list_update', kwargs={'pk': self.object.pk})


class PermissionMixin(object):
    """
    Adds a dispatch method that checks if the user is assigned to the object.

    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.task_list = get_object_or_404(TaskList, pk=kwargs.get('pk'))
        # since we allow to only add users to a task, that are on the task
        # list, the following check will also be secure for tasks
        if not self.user in self.task_list.users.all():
            raise Http404
        return super(PermissionMixin, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(PermissionMixin, self).get_context_data(**kwargs)
        ctx.update({'task_list': self.task_list})
        return ctx


# =====
# Views
# =====

class TaskCreateView(PermissionMixin, TaskCRUDViewMixin, CreateView):
    """View to create new tasks."""
    form_class = TaskCreateForm
    model = Task
    template_name = 'task_list/task_create.html'


class TaskDeleteView(PermissionMixin, DeleteView):
    """View that lets the user delete a task."""
    model = Task
    template_name = 'task_list/task_delete.html'

    def get_success_url(self):
        return reverse('task_list', kwargs={'pk': self.task_list.pk})


class TaskListCreateView(LoginRequiredMixin, TaskListCRUDViewMixin,
                         CreateView):
    """View to create new task lists."""
    form_class = TaskListCreateForm
    model = TaskList
    template_name = 'task_list/task_list_create.html'


class TaskListDeleteView(PermissionMixin, DeleteView):
    """View to let users delete a task list and all tasks."""
    model = TaskList
    template_name = 'task_list/task_list_delete.html'

    def get_success_url(self):
        return reverse('task_list_list')


class TaskListListView(LoginRequiredMixin, ListView):
    """View to list all TaskList objects for the current user."""
    template_name = 'task_list/task_list_list.html'

    def get_queryset(self):
        return TaskList.objects.filter(users__pk=self.user.pk)


class TaskListUpdateView(TaskListCRUDViewMixin, PermissionMixin, UpdateView):
    """A view to update a task list."""
    form_class = TaskListUpdateForm
    model = TaskList
    template_name = 'task_list/task_list_update.html'


class TaskListView(PermissionMixin, ListView):
    """A view that lists all tasks of a task list."""
    template_name = 'task_list/task_list.html'

    def get_queryset(self):
        return self.task_list.tasks.all()


class TaskUpdateView(PermissionMixin, TaskCRUDViewMixin, UpdateView):
    """View to update tasks."""
    form_class = TaskUpdateForm
    model = Task
    template_name = 'task_list/task_update.html'
