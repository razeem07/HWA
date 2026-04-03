from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/admin-login/')

        if request.user.is_superuser or request.user.is_admin:
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden("You are not allowed to access this page")

    return wrapper