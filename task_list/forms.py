"""Forms for the ``task_list`` app."""
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from .models import Parent, Task, TaskList


# ======
# Mixins
# ======

class TaskFormMixin(object):
    """Mixin to add common methods to all Task and TaskList forms."""
    def __init__(self, user, ctype_pk=None, obj_pk=None, *args, **kwargs):
        self.user = user
        self.ctype_pk = ctype_pk
        self.obj_pk = obj_pk
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

        # if a template is given, the instance is created from it
        if template:
            self.instance = TaskList.objects.create_from_template(
                template, self.cleaned_data.get('title'), self.user)

        instance = super(TaskListCreateForm, self).save(*args, **kwargs)

        # if a ctype was given, attach the list to the object
        if self.ctype_pk:
            ctype = ContentType.objects.get_for_id(self.ctype_pk)
            parent = Parent.objects.get_or_create(
                content_type_id=ctype.pk, object_id=self.obj_pk,
                task_list=instance)[0]
            parent.save()

        return instance


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

    def clean_title(self):
        data = self.data.get('title')
        if data:
            try:
                matching_list = TaskList.objects.get(
                    users=self.user, is_template=True, title=data)
            except:
                pass
            else:
                if not self.instance.pk == matching_list.pk:
                    raise forms.ValidationError(_(
                        'You have already created a template with this name.'))
        return data

    def save(self, *args, **kwargs):
        # if the instance is a template already, we just update it
        if self.instance.is_template:
            return super(TemplateForm, self).save(*args, **kwargs)
        return TaskList.objects.create_template_from_task_list(self.instance,
                                                               self.user)
