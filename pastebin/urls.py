from django.conf.urls import url

from pastebin.views import snippet_view, SnippetView
from .views import get_snippets

urlpatterns = [
    url(r'^$', get_snippets, name='snippets'),
    url(r'^(?P<pk>\d+)$', get_snippets, name='snippets'),
    url(r'^cbv/$', snippet_view),
    url(r'^cbv/(?P<pk>\d+)/$', snippet_view)
]
