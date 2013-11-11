import random
from string import ascii_lowercase
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class Generator(BaseGenerator):
    name = 'Random full name'
    slug = 'random-full-name'
    for_fields = [models.CharField]
    options_form = None

    def __init__(self):
        self.generated = []
        self.first_names = self._get_first_names()
        self.last_names = self._get_last_names()

    def save(self, obj, field, form_data):
        if field.unique:
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate())

    def _generate(self):
        return '%s %s' % (random.choice(self.first_names), random.choice(self.last_names))

    def _generate_unique(self):
        for _ in range(10000):
            value = self._generate()
            if value not in self.generated:
                self.generated.append(value)
                return value

    def _get_first_names(self):
        with open(self.rel_path('_first_names.txt'), 'r') as f:
            return f.read().split()

    def _get_last_names(self):
        with open(self.rel_path('_last_names.txt'), 'r') as f:
            return f.read().split()
