from apps.common.models import Role, Farm, SheetChat
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Count

User = get_user_model()

def agri_context(request):
    role = None
    pending_requests = 0
    user_roles = []
    nav_farms = []
    pending_counts = []
    total_unread_messages = 0
    total_notifications = 0

    if request.user.is_authenticated:
        user_roles = Role.objects.filter(user=request.user).select_related('farm')
        user_roles_qs = user_roles.filter(
            farm=request.user.active_farm
        )
        role = user_roles_qs.filter(active=True).first()

        nav_farms = Farm.objects.filter(
            farm_role__user=request.user,
            farm_role__active=True
        ).distinct()

        active_farm = request.user.active_farm
        pending_requests = Role.objects.filter(farm=active_farm, active=False).count()
        chats = SheetChat.objects.filter(sheet__farm=active_farm)
        pending_counts = chats.filter(is_read=False).exclude(sender=request.user).values('sheet', 'sheet__name').annotate(unread_count=Count('id'))

        total_unread_messages = sum(item['unread_count'] for item in pending_counts)
        total_notifications = pending_requests + total_unread_messages

    return {
        'role': role,
        'nav_farms': nav_farms,
        'user_roles': user_roles,
        'users': User.objects.all(),
        'version': getattr(settings, 'VERSION'),
        'pending_requests_count': pending_requests,
        'pending_counts': pending_counts,
        'total_unread_messages': total_unread_messages,
        'total_notifications': total_notifications
    }