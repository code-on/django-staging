import random
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class Generator(BaseGenerator):
    name = 'Random first name'
    slug = 'random-first-name'
    for_fields = [models.CharField]
    options_form = None

    def __init__(self):
        self.names = self._get_first_names()

    def save(self, obj, field, form_data):
        if field.unique:
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate())

    def _generate(self):
        return random.choice(self.names)

    def _generate_unique(self):
        if self.names:
            name = random.choice(self.names)
            self.names = [x for x in self.names if x != name]
            return name

    def _get_first_names(self):
        with open(self.rel_path('_first_names.txt'), 'r') as f:
            return f.read().split()
