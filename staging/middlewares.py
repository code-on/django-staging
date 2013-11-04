import re
from .views import data_generator, ajax_options


GENERATOR_URL_REGEXP = r'^/admin/([^/]+)/([^/]+)/generate/$'
GENERATOR_AJAX_URL_REGEXP = r'^/admin/ajax/generate/([^/]+)/([^/]+)/$'

urls = {
    re.compile(r'^/admin/([^/]+)/([^/]+)/generate/$'): data_generator,
    re.compile(r'^/admin/ajax/generate/([^/]+)/([^/]+)/$'): ajax_options,
}


class GeneratorPagesMiddleware(object):
    """
    Processes generator views
    """
    def process_request(self, request):
        for regexp, view in urls.items():
            match = regexp.match(request.path)
            if match:
                attrs = match.groups()
                return view(request, *attrs)
