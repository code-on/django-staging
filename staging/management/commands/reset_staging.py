from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from optparse import make_option
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        for db_key in settings.DATABASES.keys():
            if settings.DATABASES[db_key]['ENGINE'] != 'django.db.backends.sqlite3':
                if raw_input('Database engine is not SQLite. Do you wish run reset? [y/N]') != 'y':
                    continue
            db_file = settings.DATABASES[db_key]['NAME']
            if os.path.exists(db_file):
                if 'nodelete' not in args:
                    os.unlink(db_file)

            kwargs = dict(database=db_key, interactive=False)
            kwargs['run_syncdb'] = True

            call_command('migrate', **kwargs)

        call_command('load_staging')
