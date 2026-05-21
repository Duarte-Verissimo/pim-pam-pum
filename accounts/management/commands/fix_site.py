"""
Management command to fix the Django Site domain for allauth OAuth.
Usage: python manage.py fix_site
"""

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Updates the Site object (SITE_ID=1) to use the production domain.'

    def handle(self, *args, **options):
        domain = 'duarte-verissimo-22303434.pw.deisi.ulusofona.pt'
        display_name = 'Duarte Verissimo Portfolio'

        site, created = Site.objects.get_or_create(id=settings.SITE_ID)

        old_domain = site.domain
        old_name = site.name

        site.domain = domain
        site.name = display_name
        site.save()

        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Created Site (id={settings.SITE_ID}): '
                f'domain="{domain}", name="{display_name}"'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Updated Site (id={settings.SITE_ID}):\n'
                f'  domain: "{old_domain}" -> "{domain}"\n'
                f'  name:   "{old_name}" -> "{display_name}"'
            ))
