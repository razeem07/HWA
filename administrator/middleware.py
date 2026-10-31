from .decorators import admin_required


class AdminAccessMiddleware:
    """Require an admin login for every URL under /administrator/."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path_info.startswith("/administrator/"):
            return admin_required(lambda req: None)(request)
        return None
