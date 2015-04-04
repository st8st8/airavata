from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from test_app import urls as test_app_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'polla.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^' + settings.STATIC_URL[1:] + r'(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'', include(test_app_urls)),
]
