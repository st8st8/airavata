from django.core.management import call_command
from django.test import TestCase
from django.db.models import Q
from django.utils.six import StringIO

from django.contrib.sites.models import Site

from airavata.models import SiteAlias


class CommandTest(TestCase):

    def setUp(self):
        ## Make sure db is empty
        Site.objects.all().delete()

        self.test_name = 'brol.net'
        self.out = StringIO()

    def _setup_example(self):
        return Site.objects.create(domain='example.com', name='example.com')

    def _find_localhost(self):
        return Site.objects.get(Q(domain='localhost') | Q(aliases__domain='localhost'))

    def test_no_site_no_localhost(self):
        call_command('setprimarydomain', interactive=False, domain_name=self.test_name, stdout=self.out)
        self.assertEqual(Site.objects.filter(domain=self.test_name).count(), 1)
        self.assertRaises(Site.DoesNotExist, self._find_localhost)

    def test_no_site_with_localhost(self):
        call_command('setprimarydomain', interactive=False, domain_name=self.test_name, do_alias=True, stdout=self.out)
        self.assertEqual(Site.objects.filter(domain=self.test_name).count(), 1)
        try:
            self._find_localhost()
            self.assertTrue(True)
        except Site.DoesNotExist:
            self.assertTrue(False, 'Could not find localhost')

    def test_no_site_localhost_as_main(self):
        call_command('setprimarydomain', interactive=False, domain_name='localhost', stdout=self.out)
        self.assertEqual(Site.objects.filter(domain='localhost').count(), 1)
        try:
            site = self._find_localhost()
            self.assertEqual(site.domain, 'localhost')
        except Site.DoesNotExist:
            self.assertTrue(False, 'Could not find localhost')

        self.assertRaises(SiteAlias.DoesNotExist, SiteAlias.objects.get, domain='localhost')

    def test_no_site_localhost_as_main_no_alias(self):
        call_command('setprimarydomain', interactive=False, domain_name='localhost', do_alias=True, stdout=self.out)
        self.assertRaises(SiteAlias.DoesNotExist, SiteAlias.objects.get, domain='localhost')

    def test_example_no_localhost(self):
        self._setup_example()
        self.test_no_site_no_localhost()

    def test_example_with_localhost(self):
        self._setup_example()
        self.test_no_site_with_localhost()

    def test_exemple_localhost_as_main(self):
        self._setup_example()
        self.test_no_site_localhost_as_main()

    def test_no_duplicate_localhost_alias(self):
        site = self._setup_example()
        SiteAlias.objects.create(domain='localhost', site=site)
        call_command('setprimarydomain', interactive=False, domain_name=self.test_name, do_alias=True, stdout=self.out)
        self.assertEqual(SiteAlias.objects.filter(domain='localhost').count(), 1)

    def test_no_duplicate_localhost_main(self):
        Site.objects.create(domain='localhost', name='localhost')
        call_command('setprimarydomain', interactive=False, domain_name='localhost', do_alias=True, stdout=self.out)
        self.assertRaises(SiteAlias.DoesNotExist, SiteAlias.objects.get, domain='localhost')
