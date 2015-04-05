from django.conf.urls import url

from test_app.views import WhichSite, PageView


urlpatterns = [
    url(r'^$', WhichSite.as_view(), name='homepage'),
    url(r'^(?P<slug>[\w-]+)\.html$', PageView.as_view(), name='page'),
]