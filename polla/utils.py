from __future__ import unicode_literals

from django.apps import apps
from django.contrib.sites.models import SITE_CACHE
from django.db.models import Q
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.http.request import split_domain_port
from django.conf import settings
from .exceptions import NoRequestFound



def load_settings(app_settings):
    for app_setting in dir(app_settings):
        ## only import settings, not imported modules or methods
        set_settings = dir(settings)
        if app_setting == app_setting.upper() and app_setting not in set_settings:
            setattr(settings, app_setting, getattr(app_settings, app_setting))

## Model Validation


def domain_available(obj, site_klass):
    from django.utils.translation import ugettext_lazy as _

    qs = site_klass.objects.all()
    q2 = Q(aliases__domain__iexact=obj.domain)
    if obj.pk and obj.pk is not None:
      if isinstance(obj, site_klass):
        qs = qs.exclude(pk=obj.pk)
      else:
        q2 = ~Q(aliases__pk=obj.pk) & q2
    try:
        qs.get(Q(domain__iexact=obj.domain) | q2)
        raise ValidationError(_("A site or an alias with that domain name already exists"),
                              code='invalid')
    except site_klass.DoesNotExist:
        pass


## AppConfig

def _get_host(request=None):
    if request is None:
        ## FIXME: https://github.com/nebstrebor/django-threadlocals/pull/2
        # if 'threadlocals.middleware.ThreadLocalMiddleware' in settings.MIDDLEWARE_CLASSES:
        if 'polla.middleware.ThreadLocalMiddleware' in settings.MIDDLEWARE_CLASSES:
            from threadlocals.threadlocals import get_current_request
            request = get_current_request()
        else:
            raise ImproperlyConfigured("You should either provide a request or install threadlocals")
    if request is None:
        raise NoRequestFound("No request was provided nor could it be retrieved")
    domain_host, domain_port = split_domain_port(request.get_host())
    return domain_host


def _get_site_by_request(self, request=None):
    host = _get_host(request)
    # Looking for domain in django.contib.site.Site and polla.SiteAlias
    if host not in SITE_CACHE:
      site = self.get(Q(domain__iexact=host) | Q(aliases__domain__iexact=host))
      SITE_CACHE[host] = site
    return SITE_CACHE[host]


def get_current_site(request=None):
    if apps.is_installed('django.contrib.sites'):
        from .models import Site
        if not hasattr(settings, 'SITE_ID') and request is None:
            return _get_site_by_request(Site.objects, request)
        else:
            return Site.objects.get_current(request)
    else:
        from django.contrib.sites.requests import RequestSite
        return RequestSite(request)


## Loaders

def get_domain_path(domain):
    if settings.POLLA_REPLACE_DOTS_IN_DOMAINS:
        domain = domain.replace('.', '_')
    return domain.lower()


def get_current_path(request=None):
    site = get_current_site(request)
    return get_domain_path(site.domain)


## Allowed hosts - adapted from https://github.com/kezabelle/django-allowedsites


class ForceAllowedHostCheck(object):

    def process_request(self, request):
        request.get_host()
        return None


class Sites(object):

    """
    Base class for ``AllowedSites`` and ``CachedAllowedSites``.
    """

    __slots__ = ('defaults',)

    def __init__(self, defaults=None):
        if defaults is None:
            defaults = ()
        self.defaults = frozenset(defaults)

    def get_raw_sites(self):
        from django.contrib.sites.models import Site
        return Site.objects.all().iterator()

    def get_raw_aliases(self):
        from .models import SiteAlias
        return SiteAlias.objects.all().iterator()

    def get_domains(self):
        """
        Yields domains *without* any ports defined, as that's what
        `validate_host` wants
        """
        raw_sites = self.get_raw_sites()
        raw_aliases = self.get_raw_aliases()
        domains = set()
        for domain_list in (raw_sites, raw_aliases):
            raw_domains = (item.domain for item in domain_list)
            for domain in raw_domains:
                domain_host, domain_port = split_domain_port(domain)
                domains.add(domain_host)

        return frozenset(domains)

    def get_merged_allowed_hosts(self):
        domains = self.get_domains()
        return self.defaults.union(domains)

    def __iter__(self):
        return iter(self.get_merged_allowed_hosts())

    def __repr__(self):
        return '<{mod}.{cls} for sites: {sites}>'.format(
            mod=self.__class__.__module__, cls=self.__class__.__name__,
            sites=str(self))

    def __str__(self):
        return ', '.join(self.get_merged_allowed_hosts())

    __unicode__ = __str__

    def __contains__(self, other):
        if other in self.defaults:
            return True
        if other in self.get_domains():
            return True
        return False

    def __len__(self):
        return len(self.get_merged_allowed_hosts())

    def __nonzero__(self):
        # ask in order, so that a query *may* not be necessary.
        if len(self.defaults) > 0:
            return True
        if len(self.get_domains()) > 0:
            return True
        return False

    __bool__ = __nonzero__

    def __eq__(self, other):
        # fail early.
        if self.defaults != other.defaults:
            return False
        side_a = self.get_merged_allowed_hosts()
        side_b = other.get_merged_allowed_hosts()
        return side_a == side_b

    def __add__(self, other):
        more_defaults = self.defaults.union(other.defaults)
        return self.__class__(defaults=more_defaults)

    def __sub__(self, other):
        less_defaults = self.defaults.difference(other.defaults)
        return self.__class__(defaults=less_defaults)


class AllowedSites(Sites):

    """
    This only exists to allow isinstance to differentiate between
    the various Site subclasses
    """
    __slots__ = ('defaults',)


class CachedAllowedSites(Sites):

    """
    Sets the given ``Site`` and ``SiteAlias`` domains into the ``default`` cache.
    Expects the cache to be shared between processes, such that
    a signal listening for ``Site`` creates will be able to add to
    the cache's contents for other processes to pick up on.
    """
    __slots__ = ('defaults', 'key')

    def __init__(self, *args, **kwargs):
        self.key = 'allowedsites'
        super(CachedAllowedSites, self).__init__(*args, **kwargs)

    def _get_cached_sites(self):
        from django.core.cache import cache
        results = cache.get(self.key, None)
        return results

    def get_merged_allowed_hosts(self):
        sites = self._get_cached_sites()
        if sites is None:
            sites = self._set_cached_sites()
        return self.defaults.union(sites)

    def _set_cached_sites(self, **kwargs):
        """
        Forces whatever is in the DB into the cache.
        """
        from django.core.cache import cache
        in_db = self.get_domains()
        cache.set(self.key, in_db)
        return in_db

    @classmethod
    def update_cache(cls, **kwargs):
        """
        May be used as a post_save or post_delete signal listener.
        Replaces whatever is in the cache with the sites in the DB
        *at this moment*
        """
        cls()._set_cached_sites(**kwargs)


## Cache invalidation

def register_signals(model):
    from django.db.models.signals import post_save, post_delete
    post_save.connect(CachedAllowedSites.update_cache, sender=model, dispatch_uid='update_allowedsites')
    post_delete.connect(CachedAllowedSites.update_cache, sender=model, dispatch_uid='update_allowedsites')

