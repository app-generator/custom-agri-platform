from apps.common.models import Role

def agri_context(request):
    role = None
    user_roles = []
    if request.user.is_authenticated:
        user_roles = Role.objects.filter(user=request.user)
        user_role = Role.objects.filter(user=request.user, active=True)
        if user_role.exists():
            role = user_role.first()

    return {
        'role': role,
        'user_roles': user_roles
    }