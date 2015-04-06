## ugly fix for threadlocals' Python 2 compatibility
## see https://github.com/nebstrebor/django-threadlocals/pull/2
## for more info

from threadlocals.threadlocals import set_thread_variable

class ThreadLocalMiddleware(object):
    """Middleware that puts the request object in thread local storage."""

    def process_request(self, request):
        set_thread_variable('request', request)