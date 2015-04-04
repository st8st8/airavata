from factory import fuzzy, lazy_attribute, SubFactory
from factory.django import DjangoModelFactory
from django.contrib.sites.models import Site

from polla.models import SiteAlias
from ..models import Page


class SiteFactory(DjangoModelFactory):

    class Meta:
        model = Site

    name = fuzzy.FuzzyText()

    @lazy_attribute
    def domain(self):
        return '{}.com'.format(self.name)


class SiteAliasFactory(DjangoModelFactory):

    class Meta:
        model = SiteAlias

    site = SubFactory(SiteFactory)
    domain = fuzzy.FuzzyText()


class PageFactory(DjangoModelFactory):

    class Meta:
        model = Page

    title = fuzzy.FuzzyText(prefix='Title: ')
    body = fuzzy.FuzzyText(prefix='Body: ')