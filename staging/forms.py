import traceback
from django import forms
from django.utils.translation import ugettext_lazy as _
from generators import GENERATORS
from staging.utils import get_generator_instance


class GeneratorForm(forms.Form):
    number_to_generate = forms.IntegerField(label=_(u'number of objects to create'))

    def __init__(self, *args, **kwargs):
        try:
            self.model = kwargs.pop('model')
        except KeyError:
            self.model = None
        super(GeneratorForm, self).__init__(*args, **kwargs)

        generators_by_field = self._get_available_generators()
        if self.model:
            fields_list = list(self.model._meta.fields)
            fields_list.extend(list(self.model._meta.many_to_many))
            self.model_fields = {}
            # creating fields with choice of generators for each model field
            for field in fields_list:
                # ignoring model translation fields and auto-increment fields
                if not hasattr(field, 'translated_field') and not field.auto_created:
                    self.model_fields[field.name] = field

                    class_ = field.__class__
                    if not field.__class__ in generators_by_field.keys():
                        # probably some subclass like tinymce.models.HTMLField or ckeditor.fields.RichTextField
                        for parent_class in generators_by_field.keys():
                            if issubclass(field.__class__, parent_class):
                                class_ = parent_class
                                break

                    choices = [(x.slug, x.name) for x in generators_by_field.get(class_, []) if x().is_available(field)]
                    self.fields[field.name] = forms.ChoiceField(choices=choices, label=field.name, required=bool(choices))

    def generate(self, options):
        """
        If form is valid, creates the specified number of model instances using chosen generators and options data specified for them.
        """
        try:
            number_to_generate = self.cleaned_data.get('number_to_generate')
            objects = []
            generators = {}

            for count in range(number_to_generate):
                obj = self.model()
                for field_name, field in self.fields.items():
                    if field_name != 'number_to_generate':
                        generator_slug = self.cleaned_data.get(field_name)
                        if not generators.get(field_name):
                            # saving generator instance for the field, so it can be reused later
                            generators[field_name] = get_generator_instance(generator_slug)

                        generator = generators.get(field_name)
                        if generator:
                            generator.save(obj, self.model_fields.get(field_name), options.get(field_name))
                objects.append(obj)
            for object_ in objects:
                object_.save()

                # adding m2m objects
                m2m_dict = getattr(object_, '_m2m', {})
                for key, value in m2m_dict.items():
                    for item in value:
                        getattr(object_, key).add(item)
            return len(objects), False
        except:
            return traceback.format_exc(), True

    def _get_available_generators(self):
        """
        Returns dict with lists of all available generators for each model field.
        """
        generators = {}
        for generator_name in GENERATORS:
            generator = getattr(getattr(getattr(__import__('staging.generators.%s' % generator_name, 'Generator'), 'generators'), generator_name), 'Generator')
            for field in generator.for_fields:
                if field not in generators:
                    generators[field] = []
                generators[field].append(generator)
        return generators

    def get_chosen_generators(self):
        """
        Returns tuples of field name and generator instance for it.
        """
        for field_name, field in self.fields.items():
            if field_name != 'number_to_generate':
                try:
                    initial = field.choices[0][0]
                except IndexError:
                    initial = None
                yield field_name, get_generator_instance(self.data.get(field_name, initial))
