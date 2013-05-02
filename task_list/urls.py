"""URLs for the ``task_list`` app."""
from django.conf.urls.defaults import patterns, url

from .views import (
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
    # task list urls
    url(r'^$', TaskListListView.as_view(),
        name='task_list_list'),
    url(r'^create/$', TaskListCreateView.as_view(),
        name='task_list_create'),
    url(r'^(?P<pk>\d+)/update/$', TaskListUpdateView.as_view(),
        name='task_list_update'),
    url(r'^(?P<pk>\d+)/delete/$', TaskListDeleteView.as_view(),
        name='task_list_delete'),

    # template urls
    url(r'^templates/$', TemplateListView.as_view(),
        name='template_list'),
    url(r'^template/(?P<pk>\d+)/$', TemplateUpdateView.as_view(),
        name='template_update'),
    url(r'^template/(?P<pk>\d+)/delete/$', TemplateDeleteView.as_view(),
        name='template_delete'),

    # task urls
    url(r'^(?P<task_list_pk>\d+)/$', TaskListView.as_view(),
        name='task_list'),
    url(r'^(?P<task_list_pk>\d+)/create/$', TaskCreateView.as_view(),
        name='task_create'),
    url(r'^task/(?P<pk>\d+)/toggle/$',
        TaskDoneToggleView.as_view(),
        name='task_toggle'),
    url(r'^task/(?P<pk>\d+)/update/$',
        TaskUpdateView.as_view(),
        name='task_update'),
    url(r'^task/(?P<pk>\d+)/delete/$',
        TaskDeleteView.as_view(),
        name='task_delete'),

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
