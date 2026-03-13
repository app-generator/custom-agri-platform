from django import template
from apps.users.models import UserRole
from apps.common.models import Role

register = template.Library()


@register.filter
def get_item(dictionary, key):
    item = dictionary.get(key)
    return item.value if item else ""


@register.filter
def get_farm_manager(farm):
    role = Role.objects.filter(farm=farm, role=UserRole.FARMER).first()
    if role:
        return role.user.email
    
    return None