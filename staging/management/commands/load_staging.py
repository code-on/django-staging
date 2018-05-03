from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.apps import apps as django_apps
from optparse import make_option
from staging.signals import on_load_staging
import os
import re


def get_apps():
    for i in django_apps.get_app_configs():
        yield i.module


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
            if input('Database engine is not SQLite. Do you wish load staging data? [y/N]') != 'y':
                return

        options = kwargs.get('options', {})

        app_fixtures = []
        for app in get_apps():
            #print app
            if hasattr(app, '__path__'):
                # It's a 'models/' subpackage
                for path in app.__path__:
                    path = os.path.join(path, 'fixtures')
                    app_fixtures.append(path)
            else:
                # It's a models.py module
                path = os.path.join(os.path.dirname(app.__file__), 'fixtures')
                app_fixtures.append(path)
        
        app_fixtures += settings.FIXTURE_DIRS

        fixtures = []

        for app in app_fixtures:
            if os.path.exists(app):
                fixtures.extend(self.load_path(app, options))

        call_command('loaddata', *fixtures, **options)

        on_load_staging.send(self)

    def load_path(self, path, options):
        fixture_pattern = re.compile(r'^staging_.+\.(json|yaml|xml)$')
        fixtures = sorted([i for i in os.listdir(path) if fixture_pattern.match(i)])

        return fixtures
