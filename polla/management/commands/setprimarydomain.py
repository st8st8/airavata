from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db.models import Q

from django.contrib.sites.models import Site
from ...models import SiteAlias


class Command(BaseCommand):
    help = 'Sets the primary domain name (and optionnally localhost alias)'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.domain_field = Site._meta.get_field('domain')

    def add_arguments(self, parser):
        parser.add_argument('domain_name', nargs='?', type=str, default='')
        parser.add_argument('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.')
        parser.add_argument('--localhost-alias', dest='do_alias',
            default=None, action='store_true',
            help='Create localhost alias if localhost is not configured')

    def get_input_data(self, field, message, default=None):
        raw_value = input(message)
        if default and raw_value == '':
             raw_value = default
        try:
             val = field.clean(raw_value, None)
        except ValidationError as e:
             self.stderr.write("Error: %s" % '; '.join(e.messages))
             val = None

        return val

    def handle(self, **options):
        domain = options.get('domain_name', None)
        if options.get('interactive', True):
            while domain is None or domain == '':
                domain = self.get_input_data(self.domain_field, 'Enter the main domain name [localhost]: ', 'localhost')
        elif domain is None or domain == '':
            raise CommandError('Please supply a domain name when using --noinput')

        # Try to find the default example.com
        # Fallback to the first site created or None
        try:
            site = Site.objects.get(domain='example.com')
        except Site.DoesNotExist:
            try:
                site = Site.objects.order_by('id').first()
            except Site.DoesNotExist:
                site = None

        if site is None:
            site = Site.objects.create(domain=domain, name=domain)
        else:
            site.domain = domain
            site.save()

        if domain != 'localhost':
            found = Site.objects.filter(Q(domain__iexact='localhost') |
                Q(aliases__domain__iexact='localhost')).count()
            if found == 0:
                do_alias = options.get('do_alias', None)
                if do_alias is None and options.get('interactive', True):
                    while do_alias is None:
                        do_create = input('No site found for loclhost would you like to create and alias? [y/N] ')
                        if do_create.lower() in 'yn':
                            do_alias = True if do_create.lower() else False
                if do_alias is not None and do_alias:
                    SiteAlias.objects.create(site=site, domain='localhost')

        self.stdout.write('Successfully updated site "{}"'.format(site))
