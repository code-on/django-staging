import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.contrib.webdesign import lorem_ipsum


class LoremIpsumForm(forms.Form):
    min_paragraphs = forms.IntegerField()
    max_paragraphs = forms.IntegerField()

    def clean(self):
        data = super(LoremIpsumForm, self).clean()
        if data.get('min_paragraphs') > data.get('max_paragraphs'):
            raise ValidationError('Min paragraphs value can not be bigger than max paragraphs')
        return data


class Generator(object):
    name = 'Lorem ipsum paragraphs'
    slug = 'lorem-ipsum-paragraph'
    for_fields = [models.TextField]
    options_form = LoremIpsumForm

    @classmethod
    def save(cls, obj, field_name, form_data):
        setattr(obj, field_name, cls.generate(form_data.get('min_paragraphs', 1), form_data.get('max_paragraphs', 1)))

    @classmethod
    def generate(cls, min_paragraphs, max_paragraphs):
        paragraphs_count = random.randint(min_paragraphs, max_paragraphs)
        return '\n\n'.join(lorem_ipsum.paragraphs(paragraphs_count))
