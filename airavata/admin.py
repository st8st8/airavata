from django.contrib import admin

from .models import SiteAlias


@admin.register(SiteAlias)
class SiteAliasAdmin(admin.ModelAdmin):

    list_display = ('domain', 'get_site_domain', 'get_site_name')

    def get_site_name(self, obj):
        return obj.site.name
    get_site_name.short_description = 'Site name'
    get_site_name.admin_order_field = 'site__name'

    def get_site_domain(self, obj):
        return obj.site.name
    get_site_domain.short_description = 'Main domain'
    get_site_domain.admin_order_field = 'site__domain'
