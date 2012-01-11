from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from optparse import make_option
import os


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--env', '-e', dest='env',
            help='enviroment'),
    )

    def handle(self, *args, **kwargs):
        for db_key in settings.DATABASES.keys():
            db_file = settings.DATABASES[db_key]['NAME']
            if os.path.exists(db_file):
                if not 'nodelete' in args:
                    os.unlink(db_file)
            call_command('syncdb', database=db_key, interactive=False, migrate_all=True)
        call_command('load_staging', env=kwargs.get('env'))
