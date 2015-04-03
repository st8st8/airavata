from django.apps import AppConfig


class PollaAppConfig(AppConfig):

    name = 'polla'
    verbose_name = 'Polla'

    def ready(self):
        from .utils import _get_site_by_request, domain_available
        from django.contrib.sites.models import SiteManager, Site

        SiteManager._get_site_by_request = _get_site_by_request

        old_site_clean = getattr(Site, 'clean', None)

        def site_clean(self):
            domain_available(self, Site)
            if old_site_clean is not None:
                old_site_clean(self)

        Site.clean = site_clean
