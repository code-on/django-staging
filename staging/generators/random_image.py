from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
import requests


class RandomImageForm(forms.Form):
    THEME_CHOICES = (
        ('', _(u'Any')),
        ('abstract', _(u'Abstract')),
        ('animals', _(u'Animals')),
        ('business', _(u'Business')),
        ('cats', _(u'Cats')),
        ('city', _(u'City')),
        ('fashion', _(u'Fashion')),
        ('food', _(u'Food')),
        ('nature', _(u'Nature')),
        ('nightlife', _(u'Nightlife')),
        ('people', _(u'People')),
        ('sports', _(u'Sports')),
        ('technics', _(u'Technics')),
        ('transport', _(u'Transport')),
    )

    width = forms.IntegerField()
    height = forms.IntegerField()
    theme = forms.ChoiceField(choices=THEME_CHOICES, required=False)


class Generator(object):
    name = 'Random image'
    slug = 'random-image'
    for_fields = [models.FileField, models.ImageField]
    options_form = RandomImageForm

    def save(self, obj, field, form_data):
        name, file_ = self._generate(form_data.get('width', 800), form_data.get('height', 600), form_data.get('theme'))
        getattr(obj, field.name).save(name, file_, save=False)

    @classmethod
    def is_available(cls, field):
        return True

    def _generate(self, width, height, theme):
        url = 'http://lorempixel.com/%s/%s/' % (width, height)
        if theme:
            url += '%s/' % theme
        response = requests.get(url)

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()

        return 'lorem_ipsum.jpg', File(img_temp)
