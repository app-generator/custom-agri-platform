from apps.common.models import Role, Farm
from django.contrib.auth import get_user_model

User = get_user_model()

def agri_context(request):
    role = None
    user_roles = []
    farms = []

    if request.user.is_authenticated:
        user_roles = Role.objects.filter(user=request.user)
        user_role = Role.objects.filter(user=request.user, farm=request.user.active_farm, active=True)
        if user_role.exists():
            role = user_role.first()

        farms = Farm.objects.filter(
            farm_role__user=request.user,
            farm_role__active=True
        ).distinct()

    return {
        'role': role,
        'farms': farms,
        'user_roles': user_roles,
        'users': User.objects.all()
    }