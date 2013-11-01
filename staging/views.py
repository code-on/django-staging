from django.contrib import messages
from django.db.models import get_model
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from staging.forms import GeneratorForm


def data_generator(request, _module, _class):
    model = get_model(_module, _class)

    initial = {
        'number_to_generate': 10,
    }
    form = GeneratorForm(request.POST or None, model=model, initial=initial)
    if form.is_valid():
        info, is_error = form.generate()
        if is_error:
            messages.error(request, unicode(info))
        else:
            messages.success(request, _(u'Generated %s objects' % info))
            return redirect('admin:%s_%s_changelist' % (_module, _class))

    return render_to_response('admin/generator.html', {
        'cl': model._meta,
        'form': form
    }, RequestContext(request))
