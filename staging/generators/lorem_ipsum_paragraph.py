import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.contrib.webdesign import lorem_ipsum
from staging.generators import BaseGenerator


class LoremIpsumForm(forms.Form):
    min_paragraphs = forms.IntegerField()
    max_paragraphs = forms.IntegerField()

    def clean(self):
        data = super(LoremIpsumForm, self).clean()
        if data.get('min_paragraphs') > data.get('max_paragraphs'):
            raise ValidationError('Min paragraphs value can not be bigger than max paragraphs')
        return data


class Generator(BaseGenerator):
    name = 'Lorem ipsum paragraphs'
    slug = 'lorem-ipsum-paragraph'
    for_fields = [models.TextField]
    options_form = LoremIpsumForm

    def __init__(self):
        self.generated = []

    def save(self, obj, field, form_data):
        if field.unique:
            setattr(obj, field.name, self._generate_unique(form_data.get('min_paragraphs', 1), form_data.get('max_paragraphs', 1)))
        else:
            setattr(obj, field.name, self._generate(form_data.get('min_paragraphs', 1), form_data.get('max_paragraphs', 1)))

    def _generate(self, min_paragraphs, max_paragraphs):
        paragraphs_count = random.randint(min_paragraphs, max_paragraphs)
        return '\n\n'.join(lorem_ipsum.paragraphs(paragraphs_count, common=False))

    def _generate_unique(self, min_paragraphs, max_paragraphs):
        for _ in range(10000):
            paragraphs_count = random.randint(min_paragraphs, max_paragraphs)
            value = '\n\n'.join(lorem_ipsum.paragraphs(paragraphs_count, common=False))
            if value not in self.generated:
                self.generated.append(value)
                return value
