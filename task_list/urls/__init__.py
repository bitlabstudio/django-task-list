"""URLs for the ``task_list`` app."""
from django.conf.urls.defaults import include, patterns, url


urlpatterns = patterns(
    '',
    url(r'^', include('task_list.urls.simple')),
    url(r'^', include('task_list.urls.ctype')),
)
