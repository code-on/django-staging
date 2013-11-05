import os
import imp
from django.conf import settings



GENERATORS_CACHE_BY_SLUG = {}
GENERATORS_CACHE_BY_FIELD = {}


def init_generators():
    for directory in settings.GENERATORS_DIRS:
        if os.path.isdir(directory):
            for file_name in os.listdir(directory):
                try:
                    generator_module = imp.load_source('staging.generators.%s' % file_name, os.path.join(directory, file_name))
                    generator_class = generator_module.Generator
                    GENERATORS_CACHE_BY_SLUG[generator_class.slug] = generator_class
                    for field in generator_class.for_fields:
                        if field not in GENERATORS_CACHE_BY_FIELD:
                            GENERATORS_CACHE_BY_FIELD[field] = []
                        GENERATORS_CACHE_BY_FIELD[field].append(generator_class)
                except:
                    pass


init_generators()


def get_options_form(generator, field_name, data=None):
    """
    Returns option form for the specified generator with field_name prefix. Initializes it with data dict if given.
    """
    if generator.options_form:
        return generator.options_form(data=data, prefix='%s-%s' % (field_name, generator.slug))


def get_generator_instance(slug):
    """
    Returns generator instance by specified slug.
    """
    generator_class = GENERATORS_CACHE_BY_SLUG.get(slug)
    if generator_class:
        return generator_class()


def get_available_generators():
    """
    Returns dict with lists of all available generators for each model field.
    """
    return GENERATORS_CACHE_BY_FIELD
