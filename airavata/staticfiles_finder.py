import os
from collections import OrderedDict

from django.contrib.staticfiles.finders import FileSystemFinder, BaseFinder
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.models import Site
from django.conf import settings

from airavata.utils import get_domain_path


class SiteFinder(FileSystemFinder):

    def __init__(self, app_name=None, *args, **kwargs):
        self.locations = []
        self.storages = OrderedDict()
        for site in Site.objects.all():
            current = get_domain_path(site.domain)
            root = os.path.join(settings.POLLA_SITES_DIR, current, 'static')
            if os.path.exists(root) and (current, root) not in self.locations:
                self.locations.append((current, root))

        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage
        BaseFinder.__init__(self, *args, **kwargs)
