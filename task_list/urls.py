"""URLs for the ``task_list`` app."""
from django.conf.urls.defaults import patterns, url

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskListCreateView,
    TaskListDeleteView,
    TaskListListView,
    TaskListUpdateView,
    TaskListView,
    TaskUpdateView,
)


urlpatterns = patterns(
    '',
    # task list urls
    url(r'^task_list/create/$', TaskListCreateView.as_view(),
        name='task_list_create'),
    url(r'^task_list/(?P<pk>\d+)/update/$', TaskListUpdateView.as_view(),
        name='task_list_update'),
    url(r'task_list/(?P<pk>\d+)/delete/$', TaskListDeleteView.as_view(),
        name='task_list_delete'),
    url(r'task_lists/$', TaskListListView.as_view(),
        name='task_list_list'),

    # task urls
    url(r'^task_list/(?P<pk>\d+)/task/create/$', TaskCreateView.as_view(),
        name='task_create'),
    url(r'^task_list/(?P<pk>\d+)/task/(?P<task_pk>\d+)/update/$',
        TaskUpdateView.as_view(),
        name='task_update'),
    url(r'task_list/(?P<pk>\d+)/task/(?P<task_pk>\d+)/delete/$',
        TaskDeleteView.as_view(),
        name='task_delete'),
    url(r'task_list/(?P<pk>\d+)/tasks/?', TaskListView.as_view(),
        name='task_list'),
)
