import random
from django.db import models
from django import forms


class ValueFromListForm(forms.Form):
    lines = forms.CharField(widget=forms.Textarea)


class NotInitialized():
    pass


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
    lines_left = NotInitialized

    def save(self, obj, field, form_data):
        if field.unique:
            if self.lines_left == NotInitialized:
                self.lines_left = form_data.get('lines').split('\n')
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate(form_data.get('lines')))

    @classmethod
    def is_available(cls, field):
        return True

    def _generate(self, text):
        lines = text.split('\n')
        return random.choice(lines)

    def _generate_unique(self):
        if self.lines_left:
            value = random.choice(self.lines_left)
            self.lines_left = [x for x in self.lines_left if x != value]
            return value
