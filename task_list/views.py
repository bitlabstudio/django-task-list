"""Views for the ``task_list`` app."""
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    UpdateView,
)
from django.shortcuts import get_object_or_404

from .forms import (
    TaskCreateForm,
    TaskDoneToggleForm,
    TaskListCreateForm,
    TaskListUpdateForm,
    TaskUpdateForm,
    TemplateForm,
)
from .models import Task, TaskList


# ======
# Mixins
# ======


class LoginRequiredMixin(object):
    """Mixin to add a login required decorator and ctype handling to views."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # check if the user is permitted to access the content object
        self.ctype_pk = kwargs.get('ctype_pk')
        self.obj_pk = kwargs.get('obj_pk')
        if self.ctype_pk:
            try:
                self.ctype = ContentType.objects.get_for_id(self.ctype_pk)
            except ContentType.DoesNotExist:
                raise Http404
            else:
                self.obj = self.ctype.get_object_for_this_type(pk=self.obj_pk)
                if (not hasattr(self.obj, 'task_list_has_permission') or
                        not self.obj.task_list_has_permission(request)):
                    raise Http404
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(LoginRequiredMixin, self).get_context_data(**kwargs)
        # if ctype_pk in self.kwargs, add ctype to context
        if self.ctype_pk:
            ctx.update({
                'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk,
                'ctype': self.ctype, 'obj': self.obj})
        return ctx


class TaskCRUDViewMixin(object):
    """Mixin to add common methods to the task CRUD views."""
    def get_form_kwargs(self):
        kwargs = super(TaskCRUDViewMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user, 'task_list': self.task_list})
        return kwargs

    def get_success_url(self):
        kwargs = {'task_list_pk': self.object.task_list.pk}
        # if ctype_pk in self.kwargs, redirect to view version with ctype_pk
        if self.ctype_pk:
            kwargs.update({'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk})
        return reverse('task_list', kwargs=kwargs)


class TaskListCRUDViewMixin(object):
    """Mixin to add common methods to the task list CRUD views."""
    def get_form_kwargs(self):
        kwargs = super(TaskListCRUDViewMixin, self).get_form_kwargs()
        # add ctype_pk if available
        if self.ctype_pk:
            kwargs.update({'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk})
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        kwargs = {'pk': self.object.pk}
        # if ctype_pk in self.kwargs, redirect to view version with ctype_pk
        if self.ctype_pk:
            kwargs.update({'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk})
        return reverse('task_list_update', kwargs=kwargs)


class PermissionMixin(LoginRequiredMixin):
    """
    Adds a dispatch method that checks if the user is assigned to the object.

    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.object = self.get_object()
        if isinstance(self.object, Task):
            self.task_list = self.object.task_list
        else:
            self.task_list = self.object
        # since we allow to only add users to a task, that are on the task
        # list, the following check will also be secure for tasks
        if not request.user in self.task_list.users.all():
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

    def get_object(self, **kwargs):
        return get_object_or_404(TaskList, pk=self.kwargs.get('task_list_pk'))


class TaskDeleteView(PermissionMixin, DeleteView):
    """View that lets the user delete a task."""
    model = Task
    template_name = 'task_list/task_delete.html'

    def get_success_url(self):
        kwargs = {'task_list_pk': self.task_list.pk}
        if self.ctype_pk:
            kwargs.update({'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk})
        return reverse('task_list', kwargs=kwargs)


class TaskDoneToggleView(PermissionMixin, FormView):
    """A view to toggle a tasks done state."""
    form_class = TaskDoneToggleForm
    template_name = 'task_list/task_form.html'

    def form_invalid(self, form):
        """
        This should never occur. It is merely to be sure, we never get stuck
        on this view. So we redirect back to the success url, which in any
        case should be the next parameter.

        """
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, querset=None):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        next = self.request.POST.get('next')
        if next:
            return next
        return reverse('task_list_list')


class TaskListCreateView(LoginRequiredMixin, TaskListCRUDViewMixin,
                         CreateView):
    """View to create new task lists."""
    form_class = TaskListCreateForm
    model = TaskList
    template_name = 'task_list/task_list_create.html'

    def get_context_data(self, **kwargs):
        ctx = super(TaskListCreateView, self).get_context_data(**kwargs)
        ctx.update({'templates': TaskList.objects.filter(
            users=self.request.user, is_template=True)})
        return ctx


class TaskListDeleteView(PermissionMixin, DeleteView):
    """View to let users delete a task list and all tasks."""
    model = TaskList
    template_name = 'task_list/task_list_delete.html'

    def get_success_url(self):
        kwargs = {}
        if self.ctype_pk:
            kwargs.update({'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk})
        return reverse('task_list_list', kwargs=kwargs)


class TaskListListView(LoginRequiredMixin, ListView):
    """View to list all TaskList objects for the current user."""
    model = TaskList
    template_name = 'task_list/task_list_list.html'

    def get_queryset(self):
        ctype = None
        if self.ctype_pk:
            try:
                ctype = ContentType.objects.get_for_id(self.ctype_pk)
            except ContentType.DoesNotExist:
                pass
        return TaskList.objects.filter(
            users__pk=self.request.user.pk, is_template=False,
            parent__content_type=ctype, parent__object_id=self.obj_pk)


class TaskListUpdateView(TaskListCRUDViewMixin, PermissionMixin, UpdateView):
    """A view to update a task list."""
    form_class = TaskListUpdateForm
    model = TaskList
    template_name = 'task_list/task_list_update.html'

    def get_success_url(self):
        kwargs = {}
        if self.ctype_pk:
            kwargs.update({'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk})
        return reverse('task_list_list', kwargs=kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    """
    A view that lists all tasks of a task list and allows to toggle is_done.

    """
    model = Task
    template_name = 'task_list/task_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.task_list = get_object_or_404(TaskList, pk=kwargs.get(
            'task_list_pk'))
        if not request.user in self.task_list.users.all() or (
                self.task_list.is_template):
            raise Http404
        return super(TaskListView, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(task_list=self.task_list)

    def get_context_data(self, **kwargs):
        ctx = super(TaskListView, self).get_context_data(**kwargs)
        ctx.update({'task_list': self.task_list})
        return ctx


class TaskUpdateView(PermissionMixin, TaskCRUDViewMixin, UpdateView):
    """View to update tasks."""
    form_class = TaskUpdateForm
    model = Task
    template_name = 'task_list/task_update.html'


class TemplateDeleteView(PermissionMixin, DeleteView):
    """View to let users delete a template."""
    model = TaskList
    template_name = 'task_list/template_delete.html'

    def get_success_url(self):
        kwargs = {}
        if self.ctype_pk:
            kwargs.update({'ctype_pk': self.ctype_pk, 'obj_pk': self.obj_pk})
        return reverse('template_list', kwargs=kwargs)


class TemplateListView(LoginRequiredMixin, ListView):
    """
    View to list all TaskList objects marked as template for the current user.

    """
    model = TaskList
    template_name = 'task_list/template_list.html'

    def get_queryset(self):
        return TaskList.objects.filter(users__pk=self.request.user.pk,
                                       is_template=True)


class TemplateUpdateView(TaskListCRUDViewMixin, PermissionMixin, UpdateView):
    """View to manage a task list, that is marked as template."""
    form_class = TemplateForm
    model = TaskList
    template_name = 'task_list/template_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(TemplateUpdateView, self).get_context_data(**kwargs)
        next = self.request.GET.get('next') or self.request.POST.get('next')
        if next:
            ctx.update({'next': next})
        return ctx

    def get_success_url(self):
        next = self.request.POST.get('next')
        if next:
            return next
        return reverse('template_update', kwargs={'pk': self.object.pk})
