from django.contrib.sites.models import SITE_CACHE
from django.db.models import Q


## AppConfig

def _get_host(request):
    return request.get_host().split(':')[0]


def _get_site_by_request(self, request):
    host = _get_host(request)
    # Looking for domain in django.contib.site.Site and polla.SiteAlias
    if host not in SITE_CACHE:
      site = self.get(Q(domain__iexact=host) | Q(aliases__domain__iexact=host))
      SITE_CACHE[host] = site
    return SITE_CACHE[host]
