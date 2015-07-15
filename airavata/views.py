from django.contrib.sites.shortcuts import get_current_site


class SiteFilteredViewMixin(object):

    site_field = 'site'

    def get_queryset(self):
        qs = super(SiteFilteredViewMixin, self).get_queryset()
        kwargs = {
          self.site_field: get_current_site(self.request),
        }
        return qs.filter(**kwargs)
