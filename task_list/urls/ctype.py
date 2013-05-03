"""Ctype specific URLs for the ``task_list`` app."""
from django.conf.urls.defaults import patterns, url

from ..views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDoneToggleView,
    TaskListCreateView,
    TaskListDeleteView,
    TaskListListView,
    TaskListUpdateView,
    TaskListView,
    TaskUpdateView,
    TemplateDeleteView,
    TemplateListView,
    TemplateUpdateView,
)

urlpatterns = patterns(
    '',
    # task list ctype urls
    url(r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/$',
        TaskListListView.as_view(),
        name='task_list_list'),
    url(r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/create/$',
        TaskListCreateView.as_view(),
        name='task_list_create'),
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/(?P<pk>\d+)/update/$',  # NOQA
        TaskListUpdateView.as_view(),
        name='task_list_update'),
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/(?P<pk>\d+)/delete/$',  # NOQA
        TaskListDeleteView.as_view(),
        name='task_list_delete'),

    # template ctype urls
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/templates/$',
        TemplateListView.as_view(),
        name='template_list'),
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/template/(?P<pk>\d+)/$',  # NOQA
        TemplateUpdateView.as_view(),
        name='template_update'),
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/template/(?P<pk>\d+)/delete/$',  # NOQA
        TemplateDeleteView.as_view(),
        name='template_delete'),

    # task ctype urls
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/(?P<task_list_pk>\d+)/$',  # NOQA
        TaskListView.as_view(),
        name='task_list'),
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/(?P<task_list_pk>\d+)/create/$',  # NOQA
        TaskCreateView.as_view(),
        name='task_create'),
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/task/(?P<pk>\d+)/toggle/$',  # NOQA
        TaskDoneToggleView.as_view(),
        name='task_toggle'),
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/task/(?P<pk>\d+)/update/$',  # NOQA
        TaskUpdateView.as_view(),
        name='task_update'),
    url(
        r'^ctype/(?P<ctype_pk>\d+)/object/(?P<obj_pk>\d+)/task/(?P<pk>\d+)/delete/$',  # NOQA
        TaskDeleteView.as_view(),
        name='task_delete'),
)
