import random
from django.db import models
from django import forms


class ValueFromListForm(forms.Form):
    lines = forms.CharField(widget=forms.Textarea)


class Generator(object):
    name = 'Value from list'
    slug = 'value-from-list'
    for_fields = [models.BigIntegerField, models.BooleanField, models.CharField, models.DateField, models.DateTimeField,
                  models.DecimalField, models.EmailField, models.FileField, models.FilePathField, models.FloatField,
                  models.ImageField, models.IntegerField, models.IPAddressField, models.GenericIPAddressField,
                  models.NullBooleanField, models.PositiveIntegerField, models.PositiveSmallIntegerField,
                  models.SlugField, models.SmallIntegerField, models.TextField, models.TimeField, models.URLField,
                  models.ForeignKey, models.OneToOneField]
    options_form = ValueFromListForm

    @classmethod
    def save(cls, obj, field_name, form_data):
        setattr(obj, field_name, cls.generate(form_data.get('lines')))

    @classmethod
    def generate(cls, text):
        lines = text.split('\n')
        return random.choice(lines)
