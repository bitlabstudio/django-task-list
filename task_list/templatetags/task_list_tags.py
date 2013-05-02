"""Template tags for the ``task_list`` app."""
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag()
def get_ctype_url(url_name, ctype_pk=None, obj_pk=None, **kwargs):
    """Returns the correct url wheter or not a ctype_pk is given."""
    if ctype_pk:
        kwargs.update({'ctype_pk': ctype_pk, 'obj_pk': obj_pk})
    return reverse(url_name, kwargs=kwargs)
