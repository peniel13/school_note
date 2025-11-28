# yourapp/templatetags/custom_tags.py

from django import template

register = template.Library()

# @register.filter
# def get_item(dictionary, key):
#     """Récupère un élément d'un dictionnaire par clé."""
#     return dictionary.get(key)
@register.filter
def get_item(dictionary, key):
    """Récupère un élément d'un dictionnaire par clé, si c'est un dict."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def sum_by_key(notations, key):
    """Calcule la somme d'une clé spécifique dans une liste d'objets."""
    return sum(getattr(nota, key, 0) for nota in notations if getattr(nota, key, 0) is not None)

@register.filter
def dict_get(d, key):
    """Récupère la valeur d'un dictionnaire avec la clé."""
    if not d:
        return None
    return d.get(key)



@register.filter
def floatdivide(value, divisor):
    try:
        return float(value) / float(divisor)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0
    



@register.filter
def sum_group_obtenu(period_list, group_periodes_data):
    """
    Calcule la somme des points obtenus pour les périodes d'un semestre
    dans le contexte d'un groupe Maxima.
    """
    total = 0.0
    for p in period_list:
        data = group_periodes_data.get(p)
        if data and 'obtenu' in data:
            total += data['obtenu']
    return total


@register.filter
def calculate_percentage(numerator, denominator):
    """
    Calcule le pourcentage entre deux nombres.
    """
    try:
        numerator = float(numerator)
        denominator = float(denominator)
    except (ValueError, TypeError):
        return 0.0

    if denominator == 0:
        return 0.0

    return (numerator / denominator) * 100



@register.filter
def mul_100(value):
    """Multiplie la valeur par 100."""
    try:
        return float(value) * 100
    except (ValueError, TypeError):
        return 0.0




@register.filter
def multiply(value, arg):
    """Multiplie la valeur par l'argument (ex: value|multiply:4)"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def add(value, arg):
    """Ajoute l'argument à la valeur (ex: value|add:3)"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return ''




@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
    

@register.filter
def times(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
# @register.filter
# def sum_by_key(dict_of_objects, key):
#     """
#     Additionne la valeur de l'attribut `key` pour chaque valeur dans le dictionnaire.
#     Exemple : {{ notations_par_matiere|get_item:matiere|sum_by_key:"note_obtenue" }}
#     """
#     if not dict_of_objects:
#         return 0
#     total = 0
#     for value in dict_of_objects.values():
#         if value:  # Ignore None
#             total += getattr(value, key, 0) or 0
#     return total


# from django import template

# register = template.Library()

# @register.filter
# def get_item(dictionary, key):
#     """Retourne la valeur pour la clé donnée dans un dictionnaire."""
#     if dictionary is None:
#         return None
#     return dictionary.get(key)
