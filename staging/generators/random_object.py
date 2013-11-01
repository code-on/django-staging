import random
from django.db import models
from django import forms


class Generator(object):
    name = 'Random object from queryset'
    slug = 'random-object'
    for_fields = [models.ForeignKey, models.OneToOneField]
    options_form = None

    @classmethod
    def save(cls, obj, field_name, form_data):
        setattr(obj, field_name, cls.generate(obj, field_name))

    @classmethod
    def generate(cls, obj, field_name):
        qs = getattr(obj.__class__, field_name).field.related.parent_model.objects.all()
        return random.choice(qs)
