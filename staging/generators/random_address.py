import random
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class Generator(BaseGenerator):
    name = 'Random address'
    slug = 'random-address'
    for_fields = [models.CharField]
    options_form = None

    def __init__(self):
        self.generated = []
        self.streats = self._get_streats()

    def save(self, obj, field, form_data):
        if field.unique:
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate())

    def _generate(self):
        return '%s %s' % (random.randint(1, 1000), random.choice(self.streats))

    def _generate_unique(self):
        for _ in range(10000):
            value = self._generate()
            if value not in self.generated:
                self.generated.append(value)
                return value

    def _get_streats(self):
        with open(self.rel_path('_streats.txt'), 'r') as f:
            return f.read().split()
