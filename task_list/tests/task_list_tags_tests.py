"""Tests for the template tags of the ``task_list`` app."""
from django.test import TestCase

from ..templatetags.task_list_tags import get_ctype_url
from .factories import TaskListFactory


class GetCtypeUrlTestCase(TestCase):
    """Tests for the ``get_ctype_url`` template tag."""
    longMessage = True

    def test_tag(self):
        """Tests for the ``get_ctype_url`` template tag."""
        task_list = TaskListFactory()
        self.assertEqual(
            get_ctype_url('task_list', task_list_pk=task_list.pk),
            '/{0}/'.format(task_list.pk),
            msg='Template tag did not return the correct url.')
        self.assertEqual(
            get_ctype_url('task_list', ctype_pk=1, obj_pk=2,
                          task_list_pk=task_list.pk),
            '/ctype/1/object/2/{0}/'.format(task_list.pk), msg=(
                'Template tag did not return the correct url.'))
