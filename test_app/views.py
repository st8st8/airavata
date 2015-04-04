from django.views.generic import DetailView, TemplateView
from django.views.generic.base import ContextMixin
from django.contrib.sites.shortcuts import get_current_site

from .models import Page


class PageListViewMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(PageListViewMixin, self).get_context_data(**kwargs)
        context['site_pages'] = Page.objects.filter(site=get_current_site(self.request))
        return context


class PageView(PageListViewMixin, DetailView):

    template_name = 'test_app/page.html'
    model = Page

    def get_queryset(self):
        qs = super(PageView, self).get_queryset()
        return qs.filter(site=get_current_site(self.request))


class WhichSite(PageListViewMixin, TemplateView):

    template_name = 'test_app/which.html'

    def get_context_data(self, **kwargs):
        context = super(WhichSite, self).get_context_data(**kwargs)
        context['current_site'] = get_current_site(self.request)
        return context
