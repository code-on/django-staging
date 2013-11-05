

class BaseGenerator(object):
    """
    In order to create your own generator, please subclass this base class implementing "save" method
    """

    # displayed name
    name = 'Not implemented generator'

    # slug should be unique for each generator
    slug = 'not-implemented-generator'

    # field types for which it will be displayed
    for_fields = []

    # form for extra parameters, can be None
    options_form = None

    # method executed for obj instance
    def save(self, obj, field, form_data):
        raise NotImplemented

    # method executed for each model field in "for_fields" to check if this generator supports such field
    # can be overridden
    @classmethod
    def is_available(cls, field):
        return True
