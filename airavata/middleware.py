from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.request import split_domain_port
from threadlocals.threadlocals import set_thread_variable

from airavata import models


class ThreadLocalMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    """Middleware that puts the request object in thread local storage."""

    def __call__(self, request):
        domain_host, domain_port = split_domain_port(request.get_host())
        set_thread_variable('requested_host', domain_host)
        response = self.get_response(request)
        return response


class SessionHostDomainMiddleware(SessionMiddleware):
    key = 'host-aliai'

    def process_response(self, request, response):
        ret = super(SessionHostDomainMiddleware, self).process_response(request, response)

        host = request.get_host().split(':')[0]
        from django.core.cache import cache
        aliai = cache.get(self.key, None)
        if not aliai or "reset-host-aliai" in request.GET:
            aliai = [x.domain for x in models.SiteAlias.objects.all()]
            cache.set(self.key, aliai)

        # If using a valid host, then adjust session cookies to this domain
        if host in aliai:
            try:
                response.cookies[settings.SESSION_COOKIE_NAME]['domain'] = host
            except KeyError:
                pass

        return ret