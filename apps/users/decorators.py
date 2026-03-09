from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/users/signin/')

            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to access this page.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator