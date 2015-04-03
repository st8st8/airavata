from django.apps import AppConfig


class PollaAppConfig(AppConfig):

    name = 'polla'
    verbose_name = 'Polla'

    def ready(self):
        from .utils import _get_site_by_request
        from django.contrib.sites.models import SiteManager

        SiteManager._get_site_by_request = _get_site_by_request
