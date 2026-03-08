from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    item = dictionary.get(key)
    return item.value if item else ""