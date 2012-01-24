from django.core.management import BaseCommand
from staging.data_generator import get_generator
from django.db import models


class Command(BaseCommand):
    requires_model_validation = True

    def handle(self, *app_labels, **options):
        for app_label in app_labels:
            try:
                app_label, model_label = app_label.split('.')
                models_list = [models.get_model(app_label, model_label)]
            except ValueError:
                app = models.get_app(app_label)
                models_list = models.get_models(app)

            for model in models_list:
                #model.objects.all().delete()
                opt = model._meta
                obj = model()
                for field in opt.fields:
                    self.fill_field(obj, field, model)
                obj.save()
                #obj = model.objects.get(pk=obj.pk)
                #print obj.title

    def fill_field(self, obj, field, model):
        get_generator(field, model).set_value(obj)
