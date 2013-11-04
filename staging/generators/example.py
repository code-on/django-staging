import random
from django.db import models
from django import forms
from django.db.models.fields import NOT_PROVIDED


class ExampleForm(forms.Form):
    min_number = forms.IntegerField()
    max_number = forms.IntegerField()


# Valid generator file should contain declaration of Generator object with this parameters

class Generator(object):
    """
    In order to use your generator, please add it to GENERATORS tuple in __init__.py of generators package.
    This example generator will return unique number in the chosen range
    """

    # displayed name
    name = 'Example generator'

    # slug should be unique for each generator
    slug = 'example-generator'

    # field types for which it will be displayed
    for_fields = [models.CharField]

    # form for extra parameters, can be None
    options_form = ExampleForm

    # method executed for obj instance
    # field will contain django.db.models.fields.CharField instance in this example
    # form_data will contain cleaned_data from form specified in options_form
    def save(self, obj, field, form_data):
        setattr(obj, field.name, self._generate(form_data.get('min_words'), form_data.get('max_words')))

    # method executed for each model field in "for_fields" to check if this generator supports such field
    # e.g. we check there that default value for the field is not specified
    @classmethod
    def is_available(cls, field):
        return field.default == NOT_PROVIDED

    # helper function. It's not required.
    def _generate(self, min_words, max_words):
        words = random.randint(min_words, max_words)
        return ', '.join('example' for _ in range(words))
