import os

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import StaticNode
from django.conf import settings

from ..utils import get_current_path

register = template.Library()


def static(path):
    site_path = get_current_path()
    if os.path.exists(os.path.join(settings.POLLA_SITES_DIR, site_path, 'static', path)):
        return staticfiles_storage.url(os.path.join(site_path, path))
    return staticfiles_storage.url(path)


class StaticFilesNode(StaticNode):

    def url(self, context):
        path = self.path.resolve(context)
        return static(path)


@register.tag('static')
def do_static(parser, token):
    return StaticFilesNode.handle_token(parser, token)
