from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from generators import GENERATORS


class GeneratorForm(forms.Form):
    number_to_generate = forms.IntegerField(label=_(u'number of objects to create'))

    def __init__(self, *args, **kwargs):
        try:
            self.model = kwargs.pop('model')
        except KeyError:
            self.model = None
        super(GeneratorForm, self).__init__(*args, **kwargs)

        self.generators_by_slug, self.generators_by_field = self.get_generators()
        if self.model:
            fields_list = list(self.model._meta.fields)
            fields_list.extend(list(self.model._meta.many_to_many))
            for field in fields_list:
                # ignoring model translation fields and auto-increment fields
                if not hasattr(field, 'translated_field') and not field.auto_created:
                    generators_for_class = self.generators_by_field.get(field.__class__, [])

                    # creating choice field for model attribute
                    choices = [(x.slug, x.name) for x in generators_for_class]
                    self.fields[field.name] = forms.ChoiceField(choices=choices, label=field.name, required=bool(choices))

                    # adding options forms for the field
                    generator_slug = self.data.get(field.name)
                    if generator_slug:
                        generator = self.generators_by_slug.get(generator_slug)
                        if generator and generator.options_form:
                            self.fields[field.name].options_form = generator.options_form(self.data, prefix='%s-%s' % (field.name, generator.slug))

    def is_valid(self):
        result = True
        for field in self.fields.values():
            options_form = getattr(field, 'options_form', None)
            if options_form and not options_form.is_valid():
                result = False
                break
        return super(GeneratorForm, self).is_valid() and result

    def generate(self):
        number_to_generate = self.cleaned_data.get('number_to_generate')
        objects = []
        for count in range(number_to_generate):
            obj = self.model()
            for field_name, field in self.fields.items():
                if field_name != 'number_to_generate':
                    generator = self.generators_by_slug.get(self.cleaned_data.get(field_name))
                    if generator:
                        data = {}
                        options_form = getattr(field, 'options_form', None)
                        if options_form:
                            data = getattr(options_form, 'cleaned_data', {})
                        generator.save(obj, field_name, data)
            objects.append(obj)
        #try:
        for object_ in objects:
            object_.save()

            # adding m2m objects
            m2m_dict = getattr(object_, '_m2m', {})
            for key, value in m2m_dict.items():
                for item in value:
                    getattr(object_, key).add(item)
        return len(objects), False
        #except Exception, e:
        #    return e, True

    def get_generators(self):
        generators_by_field = {}
        generators_by_slug = {}
        for generator_name in GENERATORS:
            generator = getattr(getattr(getattr(__import__('staging.generators.%s' % generator_name, 'Generator'), 'generators'), generator_name), 'Generator')
            for field in generator.for_fields:
                if field not in generators_by_field:
                    generators_by_field[field] = []
                generators_by_field[field].append(generator)
            generators_by_slug[generator.slug] = generator
        return generators_by_slug, generators_by_field
