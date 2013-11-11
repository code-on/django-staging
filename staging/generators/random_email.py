import random
from string import ascii_lowercase
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class Generator(BaseGenerator):
    name = 'Random email'
    slug = 'random-email'
    for_fields = [models.EmailField]
    options_form = None

    def __init__(self):
        self.generated = []
        self.domains = self._get_domains()
        self.first_names = self._get_first_names()
        self.last_names = self._get_last_names()

    def save(self, obj, field, form_data):
        if field.unique:
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate())

    def _generate(self):
        return '%s.%s@%s' % (random.choice(self.first_names), random.choice(self.last_names), random.choice(self.domains))

    def _generate_unique(self):
        for _ in range(10000):
            value = self._generate()
            if value not in self.generated:
                self.generated.append(value)
                return value

    def _get_name(self, length):
        return ''.join(random.choice(ascii_lowercase) for x in xrange(length))

    def _get_domains(self):
        with open(self.rel_path('_email_domains.txt'), 'r') as f:
            return f.read().split()

    def _get_first_names(self):
        with open(self.rel_path('_first_names.txt'), 'r') as f:
            return f.read().split()

    def _get_last_names(self):
        with open(self.rel_path('_last_names.txt'), 'r') as f:
            return f.read().split()
