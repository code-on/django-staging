import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.contrib.webdesign import lorem_ipsum


class LoremIpsumForm(forms.Form):
    min_words = forms.IntegerField()
    max_words = forms.IntegerField()
    capitalize_first_character = forms.BooleanField(required=False)

    def clean(self):
        data = super(LoremIpsumForm, self).clean()
        if data.get('min_words') > data.get('max_words'):
            raise ValidationError('Min words value can not be bigger than max words')
        return data


class Generator(object):
    name = 'Lorem ipsum line'
    slug = 'lorem-ipsum-line'
    for_fields = [models.CharField]
    options_form = LoremIpsumForm

    @classmethod
    def save(cls, obj, field_name, form_data):
         setattr(obj, field_name, cls.generate(form_data.get('min_words', 1), form_data.get('max_words', 1), form_data.get('capitalize_first_character', False)))

    @classmethod
    def generate(cls, min_words, max_words, capitalize_first_character):
        words_count = random.randint(min_words, max_words)
        result = lorem_ipsum.words(words_count, common=False)
        if capitalize_first_character:
            return '%s%s' % (result[0].upper(), result[1:])
        return result
