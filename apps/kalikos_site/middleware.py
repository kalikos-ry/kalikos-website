from django.http import HttpResponse
import logging

class KalikosMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # handle exceptions and write the exception to stdout
    def process_exception(self, request, exception):
        logging.error(exception)
        return None