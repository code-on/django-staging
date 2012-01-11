from django.db import models
from django.contrib.webdesign import lorem_ipsum
import random

BLANK_PROBABILITY = 0.25
DEFAULT_PROBABILITY = 0.2
MAX_TRIES = 50


class GeneratorException(object):
    pass


class CantGenerateException(object):
    pass


class BaseGenerator(object):

    def __init__(self, field, model):
        # shortcuts for commot fields attributes
        self.null = field.null
        self.blank = field.blank
        self.choices = field.choices
        self.default = field.default
        self.unique = field.unique

        self.attname = field.attname
        self.field = field
        self.model = model

        self.blank_probability = BLANK_PROBABILITY
        self.default_probabity = DEFAULT_PROBABILITY

    def get(self):
        return None

    def has_default(self):
        "Returns a boolean of whether this field has a default value."
        return self.default is not models.fields.NOT_PROVIDED


class CharFieldGenerator(BaseGenerator):

    def get(self):
        if self.blank and random.random() < self.blank_probability:
            return self.has_default() and self.default or ''

        if self.has_default() and random.random() < self.default_probabity:
            return self.default

        if self.choices:
            return random.choice(self.choices)[0]

        return self._generate()

    def _generate(self):
        tries = 0
        while True:
            if tries > MAX_TRIES:
                raise CantGenerateException('Too many tries')

            length = random.randint(self.field.max_length / 2, self.field.max_length)
            value = lorem_ipsum.words(100)[:length]

            if self.unique:
                try:
                    self.model._default_manager.get(**{self.attname: value}).query
                    tries += 1
                    continue
                except self.model.DoesNotExist:
                    pass

            return value


generators = {
    models.CharField: CharFieldGenerator
}


def get_generator(field, model):
    return generators.get(field.__class__, BaseGenerator)(field, model)
