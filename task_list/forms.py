"""Forms for the ``task_list`` app."""
from django import forms

from .models import TaskList


class TaskListFormMixin(object):
    """Mixin to add common methods to all TaskList forms."""
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TaskListFormMixin, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(TaskListFormMixin, self).save(*args, **kwargs)
        if not self.user in instance.users.all():
            instance.users.add(self.user)
        return instance


class TaskListCreateForm(TaskListFormMixin, forms.ModelForm):
    """ModelForm to create an instance of the ``TaskList`` model."""
    class Meta:
        model = TaskList
        fields = ('title',)


class TaskListUpdateForm(TaskListFormMixin, forms.ModelForm):
    """ModelForm to update an instance of the ``TaskList`` model."""
    class Meta:
        model = TaskList
        fields = ('title', 'users')
