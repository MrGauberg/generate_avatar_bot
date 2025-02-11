from django.shortcuts import redirect

# Надстройка для редиректа с http://127.0.0.1:8000/ на http://127.0.0.1:8000/admin/

class RedirectToAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/':
            return redirect('/admin/')
        response = self.get_response(request)
        return response
