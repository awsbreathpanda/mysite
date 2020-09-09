from polls.views import IndexView
from django.urls.conf import re_path

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
]
