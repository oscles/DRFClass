from django.conf.urls import url

from pastebin.views import snippet_view, SnippetView, detail_view, list_view, update_view, delete_view
from .views import get_snippets

urlpatterns = [
    url(r'^$', get_snippets, name='snippets'),
    url(r'^(?P<pk>\d+)$', get_snippets, name='snippets'),
    url(r'^cbv/$', snippet_view),
    url(r'^cbv/(?P<pk>\d+)/$', snippet_view),
    url(r'^viewset/(?P<pk>\d+)/update/$', update_view),
    url(r'^viewset/(?P<pk>\d+)/delete/$', delete_view),
    url(r'^viewset/(?P<pk>\d+)/$', detail_view),
    url(r'^viewset/$', list_view),
]
