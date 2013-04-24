"""Views for the ``task_list`` app."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TaskListCreateForm, TaskListUpdateForm
from .models import TaskList


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


class TaskListCRUDViewMixin(object):
    """Mixin to add common methods to the task list CRUD views."""
    def get_form_kwargs(self):
        kwargs = super(TaskListCRUDViewMixin, self).get_form_kwargs()
        kwargs.update({'user': self.user})
        return kwargs

    def get_success_url(self):
        return reverse('task_list_update', kwargs={'pk': self.object.pk})


class TaskListPermissionMixin(object):
    """
    Adds a dispatch method that checks if the user is assigned to the list.

    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        task_list = get_object_or_404(TaskList, pk=kwargs.get('pk'))
        if not self.user in task_list.users.all():
            raise Http404
        return super(TaskListPermissionMixin, self).dispatch(
            request, *args, **kwargs)


# =====
# Views
# =====

class TaskListCreateView(LoginRequiredMixin, TaskListCRUDViewMixin,
                         CreateView):
    """View to create new task lists."""
    form_class = TaskListCreateForm
    model = TaskList
    template_name = 'task_list/task_list_create.html'


class TaskListDeleteView(LoginRequiredMixin, TaskListPermissionMixin,
                         DeleteView):
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


class TaskListUpdateView(TaskListCRUDViewMixin, TaskListPermissionMixin,
                         UpdateView):
    """A view to update a task list."""
    form_class = TaskListUpdateForm
    model = TaskList
    template_name = 'task_list/task_list_update.html'
