from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.sites.models import Site, _simple_domain_name_validator
from django.utils.translation import ugettext_lazy as _

from .utils import domain_available


@python_2_unicode_compatible
class SiteAlias(models.Model):

    site = models.ForeignKey(Site, verbose_name=_('site'), related_name='aliases')
    domain = models.CharField(_('domain name alias'), max_length=100, unique=True,
                              validators=[ _simple_domain_name_validator])

    class Meta:
        verbose_name = "SiteAlias"
        verbose_name_plural = "SiteAliases"

    def __str__(self):
        return '{} ({})'.format(self.domain, self.site.domain)

    def clean(self):
        domain_available(self, Site)
        super(SiteAlias, self).clean()
