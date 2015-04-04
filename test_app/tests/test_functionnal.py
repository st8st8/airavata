from __future__ import unicode_literals
import six

from django.core.urlresolvers import reverse
from django.conf import settings

from django_webtest import WebTest

from django.contrib.sites.models import Site
from .factories import SiteFactory, SiteAliasFactory, PageFactory


class PageSiteTest(WebTest):

    @classmethod
    def setUpTestData(cls):
        cls.site_a = SiteFactory.create()

        cls.site_b = SiteFactory.create()
        cls.alias_b = SiteAliasFactory.create(site=cls.site_b)

        cls.site_a_pageCount = 3
        cls.site_a_totalPages = cls.site_a_pageCount + 2
        cls.pages_a = [PageFactory.create(site=cls.site_a) for i in range(cls.site_a_pageCount)]
        cls.hello_a = PageFactory.create(title='Hello', site=cls.site_a)
        cls.hello_world = PageFactory.create(title='Hello world', site=cls.site_a)

        cls.site_b_pageCount = 5
        cls.site_b_totalPages = cls.site_b_pageCount + 1
        cls.pages_b = [PageFactory.create(site=cls.site_b) for i in range(cls.site_b_pageCount)]
        cls.hello_b = PageFactory.create(title='Hello', site=cls.site_b)

    def _test_site_id(self, site, content):
        if six.PY2:
            self.assertRegexpMatches(content.decode(), 'class="site_id">{}<\/span'.format(site.pk))
        else:
            self.assertRegex(content.decode(), 'class="site_id">{}<\/span'.format(site.pk))

    def _test_site(self, site, domain, should_pass=True):
        if six.PY2:
            domain = str(domain)
        if should_pass:
            response = self.app.get(reverse('homepage'), extra_environ={'HTTP_HOST': domain})

            ## Testing ALLOWED_HOSTS
            self.assertNotEqual(response.status_code, 400,
                    'Request to host {} are allowed'.format(domain))

            ## Testing the correct site is returned
            self.assertEqual(response.status_code, 200)
            self._test_site_id(site, response.content)
        else:
            ## Testing ALLOWED_HOSTS
            ## Test server does not enforce ALLOWED_HOSTS so we will be checking
            ## For Site.DoesNotExist instead
            self.assertRaises(Site.DoesNotExist,
                    self.app.get, reverse('homepage'), extra_environ={'HTTP_HOST': domain}
            )

    def testSite(self):
        for site, domain in [
                (self.site_a, self.site_a.domain),
                (self.site_b, self.site_b.domain),
                (self.site_b, self.alias_b.domain),
            ]:
            self._test_site(site, domain)
        self._test_site(None, 'brol', False)

    def _assert_page_count(self, domain, count):
        if six.PY2:
            domain = str(domain)
        response = self.app.get(reverse('homepage'), extra_environ={'HTTP_HOST': domain})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.html.findAll(attrs={'class': 'page'})), count)

    def testSiteFilteredViewMixinPageCount(self):
        for domain, count in [
                (self.site_a.domain, self.site_a_totalPages),
                (self.site_b.domain, self.site_b_totalPages),
                (self.alias_b.domain, self.site_b_totalPages),
            ]:
            self._assert_page_count(domain, count)

    def _assert_page_id(self, domain, page_slug, page_id):
        if six.PY2:
            domain = str(domain)
        response = self.app.get(reverse('page', kwargs={'slug': page_slug}),
            extra_environ={'HTTP_HOST': domain})
        self.assertEqual(response.status_code, 200)

        if six.PY2:
            self.assertRegexpMatches(response.content.decode(),
                'class="page_id">{}<\/span'.format(page_id))
        else:
            self.assertRegex(response.content.decode(),
                'class="page_id">{}<\/span'.format(page_id))

    def testSiteFilteredViewMixinSameSlug(self):
        for site, page in [
                (self.site_a, self.hello_a),
                (self.site_b, self.hello_b),
                (self.alias_b, self.hello_b)
            ]:
            self._assert_page_id(site.domain, page.slug, page.pk)

    def testSiteFilteredViewMixinPagesStayOnTheirSite(self):
        if six.PY2:
            domain_a = str(self.site_a.domain)
            domain_b = str(self.site_b.domain)
            alias_b = str(self.alias_b.domain)
        else:
            domain_a = self.site_a.domain
            domain_b = self.site_b.domain
            alias_b = self.alias_b.domain

        response = self.app.get(reverse('page', kwargs={'slug': self.hello_world.slug}),
            extra_environ={'HTTP_HOST': domain_a})
        self.assertEqual(response.status_code, 200)
        response = self.app.get(reverse('page', kwargs={'slug': self.hello_world.slug}),
            extra_environ={'HTTP_HOST': domain_b}, status=404)
        self.assertEqual(response.status_code, 404)
        response = self.app.get(reverse('page', kwargs={'slug': self.hello_world.slug}),
            extra_environ={'HTTP_HOST': alias_b}, status=404)
        self.assertEqual(response.status_code, 404)
