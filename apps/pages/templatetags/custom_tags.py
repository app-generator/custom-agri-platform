from django import template
from apps.users.models import UserRole
from apps.common.models import Role, TabFields, Tab

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


@register.filter
def get_first_tab(sheet):
    tabs = Tab.objects.filter(sheet=sheet)
    if tabs.exists():
        return tabs.first().pk
    else:
        tab = Tab.objects.create(
            sheet=sheet,
            name="Tab 1"
        )
        return tab.pk