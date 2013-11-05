import os
import sys
from optparse import make_option
from django.core.management import BaseCommand, call_command
from django.conf import settings


def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--generators-dir',
            action='store',
            dest='generators_dir',
            type='string',
            default=0,
            help='Specify directory where to look for generators'),
    )

    def handle(self, *app_labels, **options):
        settings.TEMPLATE_CONTEXT_PROCESSORS += ('staging.contexts.data_generator_enabled',)
        settings.TEMPLATE_DIRS += (rel('..', '..', 'templates'),)
        settings.MIDDLEWARE_CLASSES += ('staging.middlewares.GeneratorPagesMiddleware',)
        settings.GENERATORS_DIRS = [rel('..', '..', 'generators')]
        if os.environ.get('GENERATORS_DIR'):
            settings.GENERATORS_DIRS.append(os.environ.get('GENERATORS_DIR'))
        if options.get('generators_dir'):
            settings.GENERATORS_DIRS.append(options.get('generators_dir'))
        for directory in settings.GENERATORS_DIRS:
            if not os.path.isdir(directory):
                print '%s generators directory does not exist' % directory
        call_command('runserver')
