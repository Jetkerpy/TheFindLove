import threading

from django.utils.deprecation import MiddlewareMixin

_thread_locals = threading.local()


def get_current_request():
    return getattr(_thread_locals, 'request', None)



class SessionMiddleWare(MiddlewareMixin):
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    
    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response
    

    def process_exception(self, request, exception):
        _thread_locals.request = None
