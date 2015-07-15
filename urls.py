from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from test_app import urls as test_app_urls
from airavata import urls


urlpatterns = urls.UrlPatterns([
    # Examples:
    # url(r'^$', 'airavata.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(test_app_urls)),
])

urlpatterns += [
    url(r'^' + settings.STATIC_URL[1:] + r'(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
