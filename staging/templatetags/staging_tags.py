from django import template

register = template.Library()

@register.filter
def get_form_for_field(extra_forms, field_name):
    return extra_forms.get(field_name)
