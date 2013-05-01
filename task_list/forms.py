"""Forms for the ``task_list`` app."""
from copy import deepcopy

from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from .models import Task, TaskList


# ======
# Mixins
# ======

class TaskFormMixin(object):
    """Mixin to add common methods to all Task and TaskList forms."""
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TaskFormMixin, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(TaskFormMixin, self).save(*args, **kwargs)
        if hasattr(instance, 'users'):
            user_list = instance.users
        else:
            user_list = instance.assigned_to
        if not self.user in user_list.all():
            user_list.add(self.user)
        return instance


# =====
# Forms
# =====

class TaskCreateForm(TaskFormMixin, forms.ModelForm):
    """ModelForm to create an instance of the ``Task`` model."""
    class Meta:
        model = Task
        fields = ('title',)

    def __init__(self, user, task_list, *args, **kwargs):
        # add optional param ctype_pk
        self.task_list = task_list
        super(TaskCreateForm, self).__init__(user, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.task_list = self.task_list
        instance = super(TaskCreateForm, self).save(*args, **kwargs)
        # if self.ctype, create Parent instance and connect this task list
        # to parent instance
        return instance


class TaskDoneToggleForm(forms.Form):
    """Form to toggle a tasks done status."""
    task = forms.ModelChoiceField(
        queryset=Task.objects.all(),
    )

    def save(self):
        task = self.cleaned_data.get('task')
        if task.is_done:
            task.is_done = None
        else:
            task.is_done = now()
        task.save()
        return task


class TaskListCreateForm(TaskFormMixin, forms.ModelForm):
    """ModelForm to create an instance of the ``TaskList`` model."""
    template = forms.ModelChoiceField(
        label=_('Copy tasks from template.'),
        queryset=None,
        required=False,
    )

    class Meta:
        model = TaskList
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super(TaskListCreateForm, self).__init__(*args, **kwargs)
        self.fields['template'].queryset = TaskList.objects.filter(
            users=self.user, is_template=True)

    def save(self, *args, **kwargs):
        template = self.cleaned_data.get('template')

        # if no template is given, we just save a new task list
        if not template:
            return super(TaskListCreateForm, self).save(*args, **kwargs)

        # if a template is given, we copy it to be the instance

        # copy the template
        title = self.cleaned_data['title']
        self.instance = deepcopy(template)
        self.instance.id = None
        self.instance.is_template = False
        self.instance.title = title
        self.instance.save()
        # copy all tasks
        self.instance.users.add(self.user)
        for task in template.tasks.all():
            new_task = deepcopy(task)
            new_task.id = None
            new_task.task_list = self.instance
            new_task.save()
        return self.instance


class TaskListUpdateForm(TaskFormMixin, forms.ModelForm):
    """ModelForm to update an instance of the ``TaskList`` model."""
    class Meta:
        model = TaskList
        fields = ('title', 'users')


class TaskUpdateForm(TaskFormMixin, forms.ModelForm):
    """ModelForm to update an instance of the ``TaskList`` model."""
    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'priority',
                  'due_date', 'assigned_to')

    def __init__(self, user, task_list, *args, **kwargs):
        self.task_list = task_list
        super(TaskUpdateForm, self).__init__(user, *args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(
            pk__in=[list_user.pk for list_user in self.task_list.users.all()])

    def save(self, *args, **kwargs):
        self.instance.task_list = self.task_list
        return super(TaskUpdateForm, self).save(*args, **kwargs)


class TemplateForm(forms.ModelForm):
    """Form to manage ``TaskList`` instances, that are marked as template."""
    class Meta:
        model = TaskList
        fields = ('title',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TemplateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TemplateForm, self).clean()
        title = cleaned_data.get('title')
        if title and TaskList.objects.filter(
                users=self.user, is_template=True, title=title).exists():
            raise forms.ValidationError(_(
                'You have already created a template with this name.'))
        return cleaned_data

    def save(self, *args, **kwargs):
        # if the instance is a template already, we just update it
        if self.instance.is_template:
            return super(TemplateForm, self).save(*args, **kwargs)

        # if the instance is no template, we create a new one and leave the
        # instance untouched

        # copy the instance
        new_task_list = deepcopy(self.instance)
        new_task_list.id = None
        new_task_list.is_template = True
        new_task_list.save()
        # clear users and set the request user only
        new_task_list.users.clear()
        new_task_list.users.add(self.user)
        # copy all tasks
        for task in self.instance.tasks.all():
            new_task = deepcopy(task)
            new_task.id = None
            new_task.is_done = None
            new_task.due_date = None
            new_task.task_list = new_task_list
            new_task.save()
            new_task.assigned_to.clear()
        return new_task_list
