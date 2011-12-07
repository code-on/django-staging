import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for db_key in settings.DATABASES.keys():
            db_file = settings.DATABASES[db_key]['NAME']
            if os.path.exists(db_file):
                if not 'nodelete' in args:
                    os.unlink(db_file)
            
            kwargs = dict(database=db_key, interactive=False)
            if 'south' in settings.INSTALLED_APPS:
                kwargs['migrate_all'] = True
            
            call_command('syncdb', **kwargs)
        call_command('load_staging')

