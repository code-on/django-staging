import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.transaction import commit_on_success
from django.db.models.loading import get_apps
from staging.signals import on_load_staging

class Command(BaseCommand):

    @commit_on_success
    def handle(self, *args, **kwargs):
        #NOTE: in order to avoid conflicts with other fixtures
        #      all fixtures in staging should starts with "staging_" prefix
        options = kwargs.get('options', {})
        app_module_paths = []
        for app in get_apps():
            if hasattr(app, '__path__'):
                # It's a 'models/' subpackage
                for path in app.__path__:
                    app_module_paths.append(path)
            else:
                # It's a models.py module
                app_module_paths.append(app.__file__)

        app_fixtures = [os.path.join(os.path.dirname(path), 'fixtures') for path in app_module_paths]
        for app in app_fixtures:
            if os.path.exists(app):
                self.load_path(app, options)
        
        on_load_staging.send(app_fixtures)

    
    def load_path(self, path, options):
        fixtures = sorted([i for i in os.listdir(path) if i.startswith('staging_')])
        for fx in fixtures:
            call_command('loaddata', fx, **options)