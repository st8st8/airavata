from django.test import TestCase
from django.contrib.sites.models import Site

from mock import patch, Mock

from .factories import SiteFactory, SiteAliasFactory


class SiteAliasTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.site = SiteFactory.create()
        cls.first_alias = SiteAliasFactory.create()
        cls.second_alias = SiteAliasFactory.create(site=cls.first_alias.site)

    def _assert_site_is(self, site_id, domain):
        with patch('polla.utils._get_host', Mock(return_value=domain)):
            self.assertEqual(site_id, Site.objects._get_site_by_request(None).pk)

    def testFindMainHost(self):
        self._assert_site_is(self.site.pk, self.site.domain)

    def testFindAliasHost(self):
        self._assert_site_is(self.first_alias.site.pk, self.first_alias.domain)
        self._assert_site_is(self.first_alias.site.pk, self.second_alias.domain)
