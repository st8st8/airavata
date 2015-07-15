from django.apps import AppConfig
from airavata.utils import register_signals


class TestAppConfig(AppConfig):
    name = 'test_app'
    verbose_name = "Test app"

    def ready(self):
        from django.contrib.sites.models import Site
        from airavata.models import SiteAlias
        for model in [Site, SiteAlias]:
            register_signals(model)
