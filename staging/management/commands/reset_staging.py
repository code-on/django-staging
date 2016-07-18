from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
import os

from staging.management.commands import StagingBaseCommand


class Command(StagingBaseCommand):
    do_system_checks = True
    option_list = BaseCommand.option_list + (
        make_option('--env', '-e', dest='env',
                    help='enviroment'),
    )

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

            try:
                from django.db import migrations
            except ImportError:
                # Django <= 1.6 with South
                call_command('syncdb', **kwargs)
                if 'south' in settings.INSTALLED_APPS:
                    call_command('migrate', fake=True)
            else:
                # Django >= 1.7
                call_command('migrate')

        call_command('load_staging', env=options.get('env'))
