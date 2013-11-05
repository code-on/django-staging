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

    def save(self, obj, field, form_data):
        if field.unique:
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate())

    def _generate(self):
        return '%s@%s.com' % (self._get_name(random.randint(5, 20)), self._get_name(random.randint(5, 20)))

    def _generate_unique(self):
        for _ in range(10000):
            value = '%s@%s.com' % (self._get_name(random.randint(5, 20)), self._get_name(random.randint(5, 20)))
            if value not in self.generated:
                self.generated.append(value)
                return value

    def _get_name(self, length):
        return ''.join(random.choice(ascii_lowercase) for x in xrange(length))
