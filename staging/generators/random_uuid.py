import uuid
from django.db import models
from django import forms


class Generator(object):
    name = 'Random uuid'
    slug = 'random-uuid'
    for_fields = [models.CharField, models.SlugField]
    options_form = None

    @classmethod
    def save(cls, obj, field_name, form_data):
        setattr(obj, field_name, cls.generate())

    @classmethod
    def generate(cls):
        return uuid.uuid4()
