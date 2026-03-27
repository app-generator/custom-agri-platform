from apps.common.models import Role, Farm
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def agri_context(request):
    role = None
    user_roles = []
    nav_farms = []

    if request.user.is_authenticated:
        user_roles = Role.objects.filter(user=request.user).select_related('farm')
        role = user_roles.filter(
            farm=request.user.active_farm,
            active=True
        ).first()

        nav_farms = Farm.objects.filter(
            farm_role__user=request.user,
            farm_role__active=True
        ).distinct()

    return {
        'role': role,
        'nav_farms': nav_farms,
        'user_roles': user_roles,
        'users': User.objects.all(),
        'version': getattr(settings, 'VERSION')
    }