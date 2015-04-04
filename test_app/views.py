from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin
from django.contrib.sites.shortcuts import get_current_site

from polla.views import SiteFilteredViewMixin

from .models import Page


class PageListViewMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(PageListViewMixin, self).get_context_data(**kwargs)
        context['site_pages'] = Page.objects.filter(site=get_current_site(self.request))
        return context


class PageView(SiteFilteredViewMixin, PageListViewMixin, DetailView):

    template_name = 'test_app/page.html'
    model = Page


class WhichSite(PageListViewMixin, ListView):

    template_name = 'test_app/which.html'
    model = Page

    def get_context_data(self, **kwargs):
        context = super(WhichSite, self).get_context_data(**kwargs)
        context['current_site'] = get_current_site(self.request)
        return context
