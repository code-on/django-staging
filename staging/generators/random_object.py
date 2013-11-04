import random
from django.db import models
from django import forms


class NotInitialized():
    pass


class Generator(object):
    name = 'Random object from queryset'
    slug = 'random-object'
    for_fields = [models.ForeignKey, models.OneToOneField]
    options_form = None
    objects_left = NotInitialized

    def save(self, obj, field, form_data):
        if field.unique:
            if self.objects_left == NotInitialized:
                self.objects_left = list(getattr(obj.__class__, field.name).field.related.parent_model.objects.all())
            setattr(obj, field.name, self._generate_unique())
        else:
            setattr(obj, field.name, self._generate(obj, field.name))

    @classmethod
    def is_available(cls, field):
        return True

    def _generate(self, obj, field_name):
        qs = getattr(obj.__class__, field_name).field.related.parent_model.objects.all()
        return random.choice(qs)

    def _generate_unique(self):
        if self.objects_left:
            object_ = random.choice(self.objects_left)
            self.objects_left = [x for x in self.objects_left if x != object_]
            return object_
