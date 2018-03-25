from django.utils.deprecation import MiddlewareMixin


class AllowMiddleware(MiddlewareMixin):
    def process_request(self,request):
        pass
    def process_response(self, request, response):
        return response
