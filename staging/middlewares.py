import re
from .views import data_generator


GENERATOR_URL_REGEXP = r'^/admin/([^/]+)/([^/]+)/generate/$'


class GeneratorPagesMiddleware(object):
    """
    Adds generator view
    """
    def process_request(self, request):
        check_url = re.compile(GENERATOR_URL_REGEXP)
        if check_url.match(request.path):
            _module, _class = check_url.match(request.path).groups()
            return data_generator(request, _module, _class)
