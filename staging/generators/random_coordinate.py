import decimal
import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class RandomCoordinateForm(forms.Form):
    base_coordinate = forms.DecimalField(help_text='center location latitude or longitude in degrees')
    max_distance = forms.DecimalField(help_text='max shift to latitude or longitude in degrees')

    def clean(self):
        data = super(RandomCoordinateForm, self).clean()
        if data.get('max_distance') < 0:
            raise ValidationError('Max distance should be positive')
        return data


class NotInitialized():
    pass


class Generator(BaseGenerator):
    name = 'Random coordinate'
    slug = 'random-coordinate'
    for_fields = [models.DecimalField]
    options_form = RandomCoordinateForm

    def __init__(self):
        self.numbers_left = NotInitialized

    def save(self, obj, field, form_data):
        setattr(obj, field.name, self._generate(form_data.get('base_coordinate', 0), form_data.get('max_distance', 1)))

    def _generate(self, base_coordinate, max_distance):
        max_distance = int(max_distance) * 1000000
        value = decimal.Decimal(base_coordinate) + decimal.Decimal(random.randrange(max_distance * 2) - max_distance) / 1000000
        if value > 180:
            value = 180
        if value < -180:
            value = -180
        return value
