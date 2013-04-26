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
    url(r'^$', TaskListListView.as_view(),
        name='task_list_list'),
    url(r'^create/$', TaskListCreateView.as_view(),
        name='task_list_create'),
    url(r'^(?P<pk>\d+)/update/$', TaskListUpdateView.as_view(),
        name='task_list_update'),
    url(r'^(?P<pk>\d+)/delete/$', TaskListDeleteView.as_view(),
        name='task_list_delete'),

    # /tasks/ctype/15/object/1/... same urls as above

    # task urls
    # name this pk `task_list_pk`
    url(r'^(?P<pk>\d+)/$', TaskListView.as_view(),
        name='task_list'),
    url(r'^(?P<pk>\d+)/create/$', TaskCreateView.as_view(),
        name='task_create'),
    url(r'^task/(?P<pk>\d+)/update/$',
        TaskUpdateView.as_view(),
        name='task_update'),
    url(r'^task/(?P<pk>\d+)/delete/$',
        TaskDeleteView.as_view(),
        name='task_delete'),
)
