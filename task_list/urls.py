"""URLs for the ``task_list`` app."""
from django.conf.urls.defaults import patterns, url

from .views import TaskListCreateView


urlpatterns = patterns(
    '',
    url(r'^task_list/create/$', TaskListCreateView.as_view(),
        name='task_list_create'),
)
