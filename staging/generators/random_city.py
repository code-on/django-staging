import random
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class Generator(BaseGenerator):
    name = 'Random city'
    slug = 'random-city'
    for_fields = [models.CharField]
    options_form = None

    def __init__(self):
        self.cities = self._get_cities()

    def save(self, obj, field, form_data):
        if field.unique:
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate())

    def _generate(self):
        return random.choice(self.cities)

    def _generate_unique(self):
        if self.cities:
            city = random.choice(self.cities)
            self.cities = [x for x in self.cities if x != city]
            return city

    def _get_cities(self):
        with open(self.rel_path('_capitals.txt'), 'r') as f:
            return f.read().split()
