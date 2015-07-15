from factory import fuzzy, lazy_attribute, SubFactory
from factory.django import DjangoModelFactory
from django.contrib.sites.models import Site
from django.utils.text import slugify

from airavata.models import SiteAlias
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

    site = SubFactory(SiteFactory)
    title = fuzzy.FuzzyText(prefix='Title: ')
    body = fuzzy.FuzzyText(prefix='Body: ')

    @lazy_attribute
    def slug(self):
        return slugify(self.title)
