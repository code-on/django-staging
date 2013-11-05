import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class M2MForm(forms.Form):
    min_objects = forms.IntegerField()
    max_objects = forms.IntegerField()

    def clean(self):
        data = super(M2MForm, self).clean()
        if data.get('min_objects') > data.get('max_objects'):
            raise ValidationError('Min objects value can not be bigger than max objects')
        return data


class Generator(BaseGenerator):
    name = 'Multiple random objects from queryset'
    slug = 'multiple-random-objects'
    for_fields = [models.ManyToManyField]
    options_form = M2MForm

    def save(self, obj, field, form_data):
        objects_count = random.randint(form_data.get('min_objects', 1), form_data.get('max_objects', 1))
        m2m_dict = getattr(obj, '_m2m', {})
        m2m_dict[field.name] = []
        for x in xrange(objects_count):
            m2m_dict[field.name].append(self._generate(obj, field.name))
        setattr(obj, '_m2m', m2m_dict)

    def _generate(self, obj, field_name):
        qs = getattr(obj.__class__, field_name).field.related.parent_model.objects.all()
        return random.choice(qs)
