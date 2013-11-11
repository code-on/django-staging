from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import get_model
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from staging.forms import GeneratorForm
from staging.utils import get_options_form, get_generator_instance


@staff_member_required
def data_generator(request, _module, _class):
    model = get_model(_module, _class)

    initial = {
        'number_to_generate': 10,
    }
    main_form = GeneratorForm(request.POST or None, model=model, initial=initial)
    all_valid = main_form.is_valid()

    extra_forms = {}
    options = {}
    # checking generator option forms
    for field_name, generator in main_form.get_chosen_generators():
        if generator:
            options_form = get_options_form(generator, field_name, request.POST or None)
            extra_forms[field_name] = options_form

            if options_form:
                if options_form.is_valid():
                    options[field_name] = options_form.cleaned_data
                else:
                    all_valid = False

    # if main form and all option forms are valid, generate objects or show error notification in case of exception
    if all_valid:
        info, is_error = main_form.generate(options)
        if is_error:
            messages.error(request, unicode(info))
        else:
            messages.success(request, _(u'Generated %s objects' % info))
            return redirect('admin:%s_%s_changelist' % (_module, _class))

    return render_to_response('admin/generator.html', {
        'cl': model._meta,
        'main_form': main_form,
        'extra_forms': extra_forms,
    }, RequestContext(request))


def ajax_options(request, field_name, generator_slug):
    """
    Returns option form for the specified generator and field.
    """
    generator = get_generator_instance(generator_slug)
    form = get_options_form(generator, field_name)
    return HttpResponse(unicode(form or ''))
