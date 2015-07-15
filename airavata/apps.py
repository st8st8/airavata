from django.apps import AppConfig


class PollaAppConfig(AppConfig):

    name = 'airavata'
    verbose_name = 'Polla'

    def ready(self):
        from .utils import _get_site_by_request, domain_available, load_settings
        from . import settings as airavata_settings
        from django.contrib.sites.models import SiteManager, Site

        load_settings(airavata_settings)

        from django.conf import settings
        if 'airavata.middleware.ThreadLocalMiddleware' in settings.MIDDLEWARE_CLASSES:
            from .utils import get_current_site
            from django.contrib.sites import shortcuts
            shortcuts.get_current_site = get_current_site

        SiteManager._get_site_by_request = _get_site_by_request

        old_site_clean = getattr(Site, 'clean', None)

        def site_clean(self):
            domain_available(self, Site)
            if old_site_clean is not None:
                old_site_clean(self)

        Site.clean = site_clean
