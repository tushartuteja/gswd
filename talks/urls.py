from __future__ import absolute_import

from django.conf.urls import patterns, url, include

from . import views


lists_patterns = patterns(
    '',
    url(r'^$', views.TalkListListView.as_view(), name='list'),
    url(r'^create/$', views.TalkListCreateView.as_view(), name='create'),
    #url(r'^check/$', views.check.as_view(), name='check'),
    url(r'^update/(?P<slug>[-\w]+)/$', views.TalkListUpdateView.as_view(), name='update'),
    url(r'^d/(?P<slug>[-\w]+)/$', views.TalkListDetailView.as_view(), name='detail'),
)

urlpatterns = patterns(
    '',
    url(r'^lists/', include(lists_patterns, namespace='lists')),
)
