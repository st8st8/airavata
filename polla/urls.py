from __future__ import unicode_literals
import copy
import importlib
from django.core.exceptions import ImproperlyConfigured
from .utils import get_current_path
from .exceptions import NoRequestFound
from django.conf import settings


POLLA_PATCHED_RESOLVER = False

class UrlPatterns(object):

    def __init__(self, defaults=[]):
        if not settings.POLLA_REPLACE_DOTS_IN_DOMAINS:
            raise ImproperlyConfigured("POLLA_REPLACE_DOTS_IN_DOMAINS needs to be set to True in order to use this functionality")
        self.defaults = defaults
        self.extras = []

    def get_site_urls(self):
        try:
            current = get_current_path()
        except NoRequestFound:
            ## No request was found, falling back to defaults
            return None
        try:
            site_urls_module = importlib.import_module('sites.{}.urls'.format(current))
            patterns = getattr(site_urls_module, 'urlpatterns', None)
            return patterns
        except ImportError:
            pass
        except ValueError:
            pass
        return None

    def get_non_extra_urls(self):
        site_urls = self.get_site_urls()
        if site_urls is None:
            site_urls = copy.copy(self.defaults)
        return site_urls

    def get_current_urls(self):
        extras = copy.copy(self.extras)
        site_urls = self.get_non_extra_urls()
        site_urls.extend(extras)
        return site_urls

    def __iter__(self):
        return iter(self.get_current_urls())

    def __repr__(self):
        return '<{mod}.{cls}>'.format(
            mod=self.__class__.__module__,
            cls=self.__class__.__name__
        )

    def __str__(self):
        return '{}'.format(self.get_current_urls())

    __unicode__ = __str__

    def __contains__(self, other):
        if other in self.extras:
            return True
        urls = self.get_non_extra_urls()
        return other in urls

    def __len__(self):
        urls = self.get_current_urls()
        return len(urls)

    def __nonzero__(self):
        if len(self.extras):
            return True
        urls = self.get_non_extra_urls()
        return len(urls) > 0

    __bool__ = __nonzero__

    def __eq__(self, other):
        if self.defaults != other.defaults or self.extras != other.extras:
            return False
        return True

    def __add__(self, other):
        self.extras.extend(other)
        return self

    def __sub__(self, other):
        raise NotImplemented

    def __reversed__(self):
        to_reverse = list(self.get_current_urls())
        return reversed(to_reverse)

if not POLLA_PATCHED_RESOLVER:
    from .utils import get_resolver, get_ns_resolver
    from django.core import urlresolvers
    urlresolvers.get_resolver = get_resolver
    urlresolvers.get_ns_resolver = get_ns_resolver
    POLLA_PATCHED_RESOLVER = True
