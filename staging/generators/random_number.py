import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms


class RandomNumberForm(forms.Form):
    min_number = forms.IntegerField()
    max_number = forms.IntegerField()

    def clean(self):
        data = super(RandomNumberForm, self).clean()
        if data.get('min_number') > data.get('max_number'):
            raise ValidationError('Min number value can not be bigger than max number')
        return data


class Generator(object):
    name = 'Random number'
    slug = 'random-number'
    for_fields = [models.BigIntegerField, models.DecimalField, models.FloatField, models.IntegerField,
                  models.PositiveIntegerField, models.PositiveSmallIntegerField, models.SmallIntegerField]
    options_form = RandomNumberForm

    @classmethod
    def save(cls, obj, field_name, form_data):
        setattr(obj, field_name, cls.generate(form_data.get('min_number', 1), form_data.get('max_number', 1)))

    @classmethod
    def generate(cls, min_number, max_number):
        return random.randint(min_number, max_number)
