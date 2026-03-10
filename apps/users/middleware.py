from django.shortcuts import redirect
from django.urls import reverse


class RoleSelectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated and not request.user.is_superuser:

            allowed_paths = [
                reverse('select_role'), reverse('signout'), reverse('signin'), reverse('signup')
            ]

            if not request.user.role and request.path not in allowed_paths:
                return redirect('select_role')

        response = self.get_response(request)
        return response