from datetime import date, datetime, timedelta
from django.contrib.webdesign import lorem_ipsum
from django.core.files.base import ContentFile
from django.db import models
import random
import sys
import urllib2

BLANK_PROBABILITY = 0.5
DEFAULT_PROBABILITY = 0.5
MAX_TRIES = 50


class GeneratorException(object):
    pass


class CantGenerateException(object):
    pass


class BaseGenerator(object):
    blank_value = None

    def __init__(self, field, model):
        # shortcuts for commot fields attributes
        self.null = field.null
        self.blank = field.blank
        self.choices = field.choices
        self.default = field.default
        self.unique = field.unique
        self.primary_key = field.primary_key

        self.attname = field.attname
        self.field = field
        self.model = model

        self.blank_probability = BLANK_PROBABILITY
        self.default_probabity = DEFAULT_PROBABILITY

    def get(self):
        if self.primary_key:
            return None

        # pay attention to field.null
        if self.blank and random.random() < self.blank_probability:
            return self.has_default() and self.default or self.blank_value

        if self.has_default() and random.random() < self.default_probabity:
            return self.default

        if self.choices:
            return random.choice(self.choices)[0]

        return self.generate()

    def set_value(self, obj):
        setattr(obj, self.field.attname, self.get())

    def has_default(self):
        "Returns a boolean of whether this field has a default value."
        return self.default is not models.fields.NOT_PROVIDED

    def generate(self):
        tries = 0
        while True:
            if tries > MAX_TRIES:
                raise CantGenerateException('Too many tries')

            value = self.generate_value()

            if self.unique:
                try:
                    self.model._default_manager.get(**{self.attname: value}).query
                    tries += 1
                    continue
                except self.model.DoesNotExist:
                    pass

            return value

    def generate_value(self):
        raise GeneratorException('generate_value is not implemented')


class BigIntegerFieldGenerator(BaseGenerator):

    def generate_value(self):
        return int(sys.maxint * random.random())


class BooleanFieldGenerator(BaseGenerator):

    def generate_value(self):
        return random.choice([True, False])


class CharFieldGenerator(BaseGenerator):
    blank_value = ''

    def generate_value(self):
        length = random.randint(self.field.max_length / 2, self.field.max_length)
        return lorem_ipsum.words(100)[:length]


class CommaSeparatedIntegerFieldGenerator(BaseGenerator):

    def generate_value(self):
        raise GeneratorException('TODO')


class DateFieldGenerator(BaseGenerator):

    def generate_value(self):
        return date.today() - timedelta(days=random.randint(0, 5))


class DateTimeFieldGenerator(BaseGenerator):

    def generate_value(self):
        return datetime.now() - timedelta(days=random.randint(0, 5))


class DecimalFieldGenerator(BaseGenerator):

    def generate_value(self):
        # TODO: fix this
        return random.randing(0, 100)


class EmailFieldGenerator(BaseGenerator):

    def generate_value(self):
        return 'test_%s@test.com' % random.randing(0, 1000)


class FileFieldGenerator(BaseGenerator):

    def generate(self):
        return self.generate_value()

    def generate_value(self):
        return ('some_name.txt', ContentFile('content'))

    def set_value(self, obj):
        value = self.get()
        # TODO: little hacky
        if isinstance(value, tuple):
            getattr(obj, self.field.attname).save(value[0], value[1], save=False)
        else:
            setattr(obj, self.field.attname, value)


class ImageFieldGenerator(FileFieldGenerator):

    def generate_value(self):
        width = random.randint(500, 1000)
        height = random.randint(500, 1000)
        url = 'http://lorempixel.com/%s/%s/' % (width, height)
        f = ContentFile(urllib2.urlopen(url).read())
        f_name = '%s_%s.jpg' % (width, height)
        return (f_name, f)


class IntegerFieldGenerator(BaseGenerator):

    def generate_value(self):
        return int(100000 * random.random())


class IPAddressFieldGenerator(BaseGenerator):

    def generate_value(self):
        return ".".join(str(random.randint(1, 255)) for i in range(4))


class NullBooleanFieldGenerator(BaseGenerator):

    def generate_value(self):
        return random.choice([True, False, None])

generators = {
    models.CharField: CharFieldGenerator,
    models.BigIntegerField: BigIntegerFieldGenerator,
    models.BooleanField: BooleanFieldGenerator,
    models.CommaSeparatedIntegerField: CommaSeparatedIntegerFieldGenerator,
    models.DateField: DateFieldGenerator,
    models.DateTimeField: DateTimeFieldGenerator,
    models.DecimalField: DecimalFieldGenerator,
    models.EmailField: EmailFieldGenerator,
    models.FileField: FileFieldGenerator,
    models.ImageField: ImageFieldGenerator,
    models.IntegerField: IntegerFieldGenerator,
    models.NullBooleanField: NullBooleanFieldGenerator
}


def get_generator(field, model):
    return generators.get(field.__class__, BaseGenerator)(field, model)
