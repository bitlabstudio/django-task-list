"""Views for the ``task_list`` app."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from .forms import TaskListCreateForm
from .models import TaskList


class TaskListCreateView(CreateView):
    """View to create new task lists."""
    form_class = TaskListCreateForm
    model = TaskList
    template_name = 'task_list/task_list_create.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(TaskListCreateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TaskListCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.user})
        return kwargs

    def get_success_url(self):
        # TODO change to task_list_update once it exists
        return reverse('task_list_create')
