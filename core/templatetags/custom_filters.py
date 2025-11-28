# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    return float(value) * float(arg)


# 🔹 add_class (ajout de classe CSS à un champ de formulaire)
@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})




@register.filter
def get_item(dictionary, key):
    """Permet d'accéder à dictionary[key] depuis le template"""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def dict_get(d, key):
    return d.get(key, 0)