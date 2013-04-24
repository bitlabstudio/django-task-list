"""Forms for the ``task_list`` app."""
from django import forms

from .models import TaskList


class TaskListCreateForm(forms.ModelForm):
    """ModelForm to create an instance of the ``TaskList`` model."""
    class Meta:
        model = TaskList
        fields = ('title',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TaskListCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(TaskListCreateForm, self).save(*args, **kwargs)
        instance.users.add(self.user)
        return instance
