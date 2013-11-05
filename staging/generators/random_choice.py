import random
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class NotInitialized():
    pass


class Generator(BaseGenerator):
    name = 'Random choice'
    slug = 'random-choice'
    for_fields = [models.BigIntegerField, models.CharField, models.DecimalField, models.EmailField, models.FloatField,
                  models.IntegerField, models.IPAddressField, models.GenericIPAddressField, models.PositiveIntegerField,
                  models.PositiveSmallIntegerField, models.SmallIntegerField, models.URLField]
    options_form = None

    def __init__(self):
        self.choices_left = NotInitialized

    def save(self, obj, field, form_data):
        if field.unique:
            if self.choices_left == NotInitialized:
                self.choices_left = [x[0] for x in field.choices]
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate(obj, field))

    @classmethod
    def is_available(cls, field):
        return bool(field.choices)

    def _generate(self, obj, field):
        choices = [x[0] for x in field.choices]
        return random.choice(choices)

    def _generate_unique(self):
        if self.choices_left:
            choice = random.choice(self.choices_left)
            self.choices_left = [x for x in self.choices_left if x != choice]
            return choice
