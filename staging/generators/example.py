import random
from django.db import models
from django import forms
from django.db.models.fields import NOT_PROVIDED
from staging.generators import BaseGenerator


class ExampleForm(forms.Form):
    min_number = forms.IntegerField()
    max_number = forms.IntegerField()


class NotInitialized():
    pass


# Valid generator file should contain declaration of Generator object with this parameters


class Generator(BaseGenerator):
    """
    This example generator will return unique number in the chosen range
    """

    # displayed name
    name = 'Example generator'

    # slug should be unique for each generator
    slug = 'example-generator'

    # field types for which it will be displayed (commented out so this generator is not automatically loaded each time)
    # for_fields = [models.IntegerField, models.DecimalField]

    # form for extra parameters, can be None
    options_form = ExampleForm

    def __init__(self):
        self.numbers_left = NotInitialized

    # field will contain django.db.models.fields.IntegerField or django.db.models.fields.DecimalField instance
    # form_data will contain cleaned_data from the form specified in options_form
    def save(self, obj, field, form_data):
        if self.numbers_left == NotInitialized:
            self.numbers_left = range(form_data.get('min_number', 1), form_data.get('max_number', 1))
        setattr(obj, field.name, self._generate())

    # conditions for field to have this generator
    # for example we check there that default value for the field is not specified
    @classmethod
    def is_available(cls, field):
        return field.default == NOT_PROVIDED

    # helper function
    def _generate(self):
        if self.numbers_left:
            value = random.choice(self.numbers_left)
            self.numbers_left = [x for x in self.numbers_left if x != value]
            return value
