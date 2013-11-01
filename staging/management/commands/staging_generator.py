import os
from django.core.management import BaseCommand, call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from django.conf import settings


def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        settings.TEMPLATE_CONTEXT_PROCESSORS += ('staging.contexts.data_generator_enabled',)
        settings.TEMPLATE_DIRS += (rel('..', '..', 'templates'),)
        settings.MIDDLEWARE_CLASSES += ('staging.middlewares.GeneratorPagesMiddleware',)
        call_command('runserver')
