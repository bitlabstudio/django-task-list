"""Factories for the models of the ``task_list`` app."""
import factory

from ..models import (
    Category,
    Parent,
    Task,
    TaskList,
)


class CategoryFactory(factory.Factory):
    """Factory for the ``Category`` model."""
    FACTORY_FOR = Category

    title = factory.Sequence(lambda n: 'category{0}'.format(n))


class ParentFactory(factory.Factory):
    """Factory for the ``Parent`` model."""
    FACTORY_FOR = Parent

    content_object = factory.SubFactory(
        'django_libs.tests.factories.UserFactory')
    task_list = factory.SubFactory('task_list.tests.factories.TaskListFactory')


class TaskListFactory(factory.Factory):
    """Factory for the ``TaskList`` model."""
    FACTORY_FOR = TaskList

    title = factory.Sequence(lambda n: 'list{0}'.format(n))


class TaskFactory(factory.Factory):
    """Factory for the ``Task`` model."""
    FACTORY_FOR = Task

    title = factory.Sequence(lambda n: 'task{0}'.format(n))
    task_list = factory.SubFactory('task_list.tests.factories.TaskListFactory')
