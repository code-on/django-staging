from django.db import models
from django import forms
from django.db.models.fields import NOT_PROVIDED


class Generator(object):
    name = 'Default value'
    slug = 'default-value'
    for_fields = [models.BigIntegerField, models.BooleanField, models.CharField, models.DateField, models.DateTimeField,
                  models.DecimalField, models.EmailField, models.FileField, models.FilePathField, models.FloatField,
                  models.ImageField, models.IntegerField, models.IPAddressField, models.GenericIPAddressField,
                  models.NullBooleanField, models.PositiveIntegerField, models.PositiveSmallIntegerField,
                  models.SlugField, models.SmallIntegerField, models.TextField, models.TimeField, models.URLField,
                  models.ForeignKey, models.ManyToManyField, models.OneToOneField]
    options_form = None

    def save(self, obj, field, form_data):
        pass

    @classmethod
    def is_available(cls, field):
        return field.blank or field.default != NOT_PROVIDED
