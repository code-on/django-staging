import random
from string import ascii_lowercase
from django.db import models
from django import forms


class Generator(object):
    name = 'Random email'
    slug = 'random-email'
    for_fields = [models.EmailField]
    options_form = None

    @classmethod
    def save(cls, obj, field_name, form_data):
        setattr(obj, field_name, cls.generate())

    @classmethod
    def generate(cls):
        return '%s@%s.com' % (cls.get_name(random.randint(5, 20)), cls.get_name(random.randint(5, 20)))

    @classmethod
    def get_name(cls, length):
        return ''.join(random.choice(ascii_lowercase) for x in xrange(length))
