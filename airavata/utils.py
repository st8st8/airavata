from __future__ import unicode_literals

from django.apps import apps
from django.contrib.sites.models import SITE_CACHE
from django.db.models import Q
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.http.request import split_domain_port
from django.conf import settings
from django.utils.lru_cache import lru_cache

from allowedsites import Sites as ASites, CachedAllowedSites as ACachedAllowedSites

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
        if 'airavata.middleware.ThreadLocalMiddleware' in settings.MIDDLEWARE_CLASSES:
            from threadlocals.threadlocals import get_thread_variable
            host = get_thread_variable('requested_host')
            if host is None:
                raise NoRequestFound("HostName could not be retrieved")
            return host
        else:
            raise ImproperlyConfigured("You should either provide a request or install threadlocals")
    domain_host, domain_port = split_domain_port(request.get_host())
    return domain_host


def _get_site_by_request(self, request=None):
    host = _get_host(request)
    # Looking for domain in django.contib.site.Site and airavata.SiteAlias
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
    try:
        site = get_current_site(request)
        return get_domain_path(site.domain)
    except NoRequestFound:
        ## Request hasn't been loaded, rather than crashing we will return a blank value
        return ''


## Allowed hosts - adapted from https://github.com/kezabelle/django-allowedsites


class Sites(ASites):

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


class AllowedSites(Sites):

    __slots__ = ('defaults',)


class CachedAllowedSites(Sites, ACachedAllowedSites):

    __slots__ = ('defaults', 'key')


## Cache invalidation

def register_signals(model):
    from django.db.models.signals import post_save, post_delete
    post_save.connect(CachedAllowedSites.update_cache, sender=model, dispatch_uid='update_allowedsites')
    post_delete.connect(CachedAllowedSites.update_cache, sender=model, dispatch_uid='update_allowedsites')


## Resolver

@lru_cache(maxsize=None)
def get_resolver_for_site(urlconf, site):
    from django.core.urlresolvers import RegexURLResolver
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    return RegexURLResolver(r'^/', urlconf)


def get_resolver(urlconf):
    current_site = get_current_path()
    return get_resolver_for_site(urlconf, current_site)


@lru_cache(maxsize=None)
def get_ns_resolver_for_site(ns_pattern, resolver, site):
    from django.core.urlresolvers import RegexURLResolver
    ns_resolver = RegexURLResolver(ns_pattern, resolver.url_patterns)
    return RegexURLResolver(r'^/', [ns_resolver])


def get_ns_resolver(ns_pattern, resolver):
    current_site = get_current_path()
    return get_ns_resolver_for_site(ns_pattern, resolver, current_site)


## Upload path builder

def upload_path(path_or_callable=''):
    if callable(path_or_callable):
        return lambda instance, filename: '{}/{}'.format(get_current_path(), path_or_callable(instance, filename))
    else:
        return lambda instance, filename: '{}/{}{}'.format(
            get_current_path(),
            '{}/'.format(path_or_callable) if path_or_callable != '' else '',
            filename
        )
