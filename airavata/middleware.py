from django.http.request import split_domain_port
from threadlocals.threadlocals import set_thread_variable


class ThreadLocalMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    """Middleware that puts the request object in thread local storage."""

    def __call__(self, request):
        domain_host, domain_port = split_domain_port(request.get_host())
        set_thread_variable('requested_host', domain_host)
        response = self.get_response(request)
        return response