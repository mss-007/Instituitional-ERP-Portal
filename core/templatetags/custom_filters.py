from django import template

register = template.Library()

# CLEAN FILTER (for None / empty values)
@register.filter
def clean(value):
    if value is None or value == "":
        return "-"
    return value

# OPTIONAL (if you actually need dict access)
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)