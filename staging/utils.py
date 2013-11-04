from staging.generators import GENERATORS


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
    for generator_name in GENERATORS:
        generator = getattr(getattr(getattr(__import__('staging.generators.%s' % generator_name, 'Generator'), 'generators'), generator_name), 'Generator')
        if generator.slug == slug:
            return generator()
