"""Factories for the models of the ``task_list`` app."""
import factory
from django_libs.tests.factories import UserFactory

from ..models import (
    Category,
    Task,
    TaskList,
)


class CategoryFactory(factory.Factory):
    """Factory for the ``Category`` model."""
    FACTORY_FOR = Category

    title = factory.Sequence(lambda n: 'category{0}'.format(n))


class TaskListFactory(factory.Factory):
    """Factory for the ``TaskList`` model."""
    FACTORY_FOR = TaskList

    title = factory.Sequence(lambda n: 'list{0}'.format(n))

    @classmethod
    def _prepare(cls, create, **kwargs):
        obj = super(TaskFactory, cls)._prepare(create, **kwargs)
        if create:
            obj.users.add(UserFactory())
        return obj


class TaskFactory(factory.Factory):
    """Factory for the ``Task`` model."""
    FACTORY_FOR = Task

    title = factory.Sequence(lambda n: 'task{0}'.format(n))
    task_list = factory.SubFactory(TaskListFactory)
