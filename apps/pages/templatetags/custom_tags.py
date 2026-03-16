from django import template
from apps.users.models import UserRole
from apps.common.models import Role, TabFields

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

@register.filter
def get_cell(cells, field_id):
    for cell in cells:
        if cell.field_id == field_id:
            return cell
    return None

@register.filter
def is_col_exists(tab):
    return TabFields.objects.filter(tab=tab).exists()