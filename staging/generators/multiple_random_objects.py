import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms


class M2MForm(forms.Form):
    min_objects = forms.IntegerField()
    max_objects = forms.IntegerField()

    def clean(self):
        data = super(M2MForm, self).clean()
        if data.get('min_objects') > data.get('max_objects'):
            raise ValidationError('Min objects value can not be bigger than max objects')
        return data


class Generator(object):
    name = 'Multiple random objects from queryset'
    slug = 'multiple-random-objects'
    for_fields = [models.ManyToManyField]
    options_form = M2MForm

    @classmethod
    def save(cls, obj, field_name, form_data):
        objects_count = random.randint(form_data.get('min_objects', 1), form_data.get('max_objects', 1))
        m2m_dict = getattr(obj, '_m2m', {})
        m2m_dict[field_name] = []
        for x in xrange(objects_count):
            m2m_dict[field_name].append(cls.generate(obj, field_name))
        setattr(obj, '_m2m', m2m_dict)

    @classmethod
    def generate(cls, obj, field_name):
        qs = getattr(obj.__class__, field_name).field.related.parent_model.objects.all()
        return random.choice(qs)
