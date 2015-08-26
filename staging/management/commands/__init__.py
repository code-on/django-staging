from django.core.management import BaseCommand


class StagingBaseCommand(BaseCommand):
    do_system_checks = False

    def __init__(self):
        super(StagingBaseCommand, self).__init__()

        # `requires_model_validation` is deprecated in favor of
        # `requires_system_checks`. If both options are present, an error is
        # raised. StagingBaseCommand sets requires_system_checks in >= Django 1.7.

        if hasattr(self, 'requires_system_checks'):
            self.requires_system_checks = self.do_system_checks
        else:
            self.requires_model_validation = self.do_system_checks  # Django < 1.7

    def handle(self, *args, **options):
        pass
