"""URLs for the ``task_list`` app."""
from django.conf.urls.defaults import patterns, url

from .views import TaskListCreateView, TaskListDeleteView, TaskListUpdateView


urlpatterns = patterns(
    '',
    url(r'^task_list/create/$', TaskListCreateView.as_view(),
        name='task_list_create'),
    url(r'^task_list/(?P<pk>\d+)/update/$', TaskListUpdateView.as_view(),
        name='task_list_update'),
    url(r'task_list/(?P<pk>\d+)/delete/$', TaskListDeleteView.as_view(),
        name='task_list_delete'),
)
