from polls.views import DetailView, IndexView, ResultView
from django.urls.conf import re_path

urlpatterns = [
    re_path(r'^detail/(?P<id>\d+)$', DetailView.as_view(), name='detail'),
    re_path(r'^result/(?P<id>\d+)$', ResultView.as_view(), name='result'),
    re_path(r'^$', IndexView.as_view(), name='index'),
]
