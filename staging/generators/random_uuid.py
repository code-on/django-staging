import uuid
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class Generator(BaseGenerator):
    name = 'Random uuid'
    slug = 'random-uuid'
    for_fields = [models.CharField, models.SlugField]
    options_form = None

    def __init__(self):
        self.generated = []

    def save(self, obj, field, form_data):
        if field.unique:
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate())

    def _generate(self):
        return uuid.uuid4()

    def _generate_unique(self):
        for _ in range(10000):
            value = uuid.uuid4()
            if value not in self.generated:
                self.generated.append(value)
                return value
