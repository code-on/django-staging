import random
import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.contrib.admin import widgets
from staging.generators import BaseGenerator


class DateForm(forms.Form):
    min_date = forms.DateTimeField(widget=widgets.AdminSplitDateTime)
    max_date = forms.DateTimeField(widget=widgets.AdminSplitDateTime)

    def clean(self):
        data = super(DateForm, self).clean()
        if data.get('min_date') and data.get('max_date') and data.get('min_date') > data.get('max_date'):
            raise ValidationError('Min date can not be later than max date')
        return data


class NotInitialized():
    pass


class Generator(BaseGenerator):
    name = 'Random date'
    slug = 'random-date'
    for_fields = [models.DateField, models.DateTimeField]
    options_form = DateForm

    def save(self, obj, field, form_data):
        setattr(obj, field.name, self._generate(form_data.get('min_date'), form_data.get('max_date')))

    def _generate(self, min_date, max_date):
        delta = max_date - min_date
        total_seconds = delta.seconds + delta.days * 24 * 3600
        return min_date + datetime.timedelta(seconds=random.randint(0, total_seconds))
