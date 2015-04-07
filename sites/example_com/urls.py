from django.conf.urls import url, include
from django.views.generic import TemplateView

from test_app import urls as test_app_urls


urlpatterns = [
    url(r'^test/a\.html$', TemplateView.as_view(template_name='test_app/test-a.html'), name='test-a'),
    url(r'^test/b\.html$', TemplateView.as_view(template_name='test_app/test-b.html'), name='test-b'),
    url(r'', include(test_app_urls)),
]
