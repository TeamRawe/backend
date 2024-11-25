from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.conf import settings

class LANAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.path.startswith('admin/'):
            ip = request.META.get('REMOTE_ADDR')
            if not any(ip.startswith(prefix) for prefix in settings.INTERNAL_IPS):
                print('skibidi')
                return HttpResponseNotFound()
        response = self.get_response(request)
        return response

