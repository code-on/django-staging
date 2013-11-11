import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.contrib.webdesign import lorem_ipsum
from staging.generators import BaseGenerator


class LoremIpsumForm(forms.Form):
    min_paragraphs = forms.IntegerField()
    max_paragraphs = forms.IntegerField()
    html = forms.BooleanField()

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
            setattr(obj, field.name, self._generate_unique(form_data.get('min_paragraphs', 1), form_data.get('max_paragraphs', 1), form_data.get('html', False)))
        else:
            setattr(obj, field.name, self._generate(form_data.get('min_paragraphs', 1), form_data.get('max_paragraphs', 1), form_data.get('html', False)))

    def _generate(self, min_paragraphs, max_paragraphs, html):
        paragraphs_count = random.randint(min_paragraphs, max_paragraphs)
        paragraphs = lorem_ipsum.paragraphs(paragraphs_count, common=False)
        if html:
            paragraphs = ['<p>%s</p>' % x for x in paragraphs]
        return '\n\n'.join(paragraphs)

    def _generate_unique(self, min_paragraphs, max_paragraphs, html):
        for _ in range(10000):
            value = self._generate(min_paragraphs, max_paragraphs, html)
            if value not in self.generated:
                self.generated.append(value)
                return value
