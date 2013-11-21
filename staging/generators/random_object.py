import random
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from staging.generators import BaseGenerator


class RandomObjectFilterForm(forms.Form):
    filter_name = forms.CharField(label=u'queryset filter name', required=False)
    filter_value = forms.CharField(label=u'queryset filter value', required=False)

    def clean(self):
        data = super(RandomObjectFilterForm, self).clean()
        if (data.get('filter_name') or data.get('filter_value')) and (not data.get('filter_name') or not data.get('filter_value')):
            raise ValidationError('Filter name and value must be specified both or omitted')
        return data



class NotInitialized():
    pass


class Generator(BaseGenerator):
    name = 'Random object from queryset'
    slug = 'random-object'
    for_fields = [models.ForeignKey, models.OneToOneField]
    options_form = RandomObjectFilterForm

    def __init__(self):
        self.objects_left = NotInitialized

    def save(self, obj, field, form_data):
        if field.unique:
            if self.objects_left == NotInitialized:
                self.objects_left = self._get_qs(getattr(obj.__class__, field.name).field, form_data)
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate(obj, field.name, form_data))

    def _get_qs(self, field, form_data):
        filter_name = form_data.get('filter_name')
        filter_value = form_data.get('filter_value')
        if filter_name and filter_value:
            args = {filter_name: filter_value}
            return list(field.related.parent_model.objects.filter(**args))
        return list(field.related.parent_model.objects.all())

    def _generate(self, obj, field_name, form_data):
        qs = self._get_qs(getattr(obj.__class__, field_name).field, form_data)
        return random.choice(qs)

    def _generate_unique(self):
        if self.objects_left:
            object_ = random.choice(self.objects_left)
            self.objects_left = [x for x in self.objects_left if x != object_]
            return object_
