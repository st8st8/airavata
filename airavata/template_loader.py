import io

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.template.base import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader
from django.utils._os import safe_join
from .utils import get_current_path
from .exceptions import NoRequestFound


class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        try:
            current = get_current_path()
        except NoRequestFound:
            return False

        try:
            return safe_join(settings.POLLA_SITES_DIR, current, 'templates', template_name)
        except SuspiciousFileOperation:
            return False

    def load_template_source(self, template_name, template_dirs=None):
        tried = ''
        filepath = self.get_template_sources(template_name, template_dirs)
        if filepath:
            try:
                with io.open(filepath, encoding=self.engine.file_charset) as fp:
                    return fp.read(), filepath
            except IOError:
                tried = filepath
        error_msg = "Tried %s" % tried
        raise TemplateDoesNotExist(error_msg)

    load_template_source.is_usable = True
