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


class NotInitialized():
    pass


class Generator(object):
    name = 'Random number'
    slug = 'random-number'
    for_fields = [models.BigIntegerField, models.DecimalField, models.FloatField, models.IntegerField,
                  models.PositiveIntegerField, models.PositiveSmallIntegerField, models.SmallIntegerField]
    options_form = RandomNumberForm
    numbers_left = NotInitialized

    def save(self, obj, field, form_data):
        if field.unique:
            if self.numbers_left_left == NotInitialized:
                self.numbers_left = range(form_data.get('min_number', 1), form_data.get('max_number', 1))
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate(form_data.get('min_number', 1), form_data.get('max_number', 1)))

    @classmethod
    def is_available(cls, field):
        return True

    def _generate(self, min_number, max_number):
        return random.randint(min_number, max_number)

    def _generate_unique(self):
        if self.numbers_left:
            value = random.choice(self.numbers_left)
            self.numbers_left = [x for x in self.numbers_left if x != value]
            return value
