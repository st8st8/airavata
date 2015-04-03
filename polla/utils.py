from django.contrib.sites.models import SITE_CACHE
from django.db.models import Q
from django.core.exceptions import ValidationError


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

def _get_host(request):
    return request.get_host().split(':')[0]


def _get_site_by_request(self, request):
    host = _get_host(request)
    # Looking for domain in django.contib.site.Site and polla.SiteAlias
    if host not in SITE_CACHE:
      site = self.get(Q(domain__iexact=host) | Q(aliases__domain__iexact=host))
      SITE_CACHE[host] = site
    return SITE_CACHE[host]
