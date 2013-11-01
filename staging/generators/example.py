from django.db import models
from django import forms


class LoremIpsumForm(forms.Form):
    min_words = forms.IntegerField()
    max_words = forms.IntegerField()


# Valid generator file should contain declaration of Generator object with this parameters

class Generator(object):
    # name
    name = 'Lorem ipsum line'
    # should be unique for each generator
    slug = 'lorem-ipsum-line'
    # field types for which it will be displayed
    for_fields = [models.CharField]
    # form for extra parameters
    options_form = LoremIpsumForm

    # method executed for obj instance field
    @classmethod
    def save(cls, obj, field_name, form_data):
         setattr(obj, field_name, cls.generate(form_data.get('min_words'), form_data.get('max_words')))

    @classmethod
    def generate(cls, min_words, max_words):
        return 'Lorem ipsum [%s - %s]' % (min_words, max_words)
