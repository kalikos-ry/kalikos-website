from django.template.defaulttags import register

@register.filter
def get_stock(dictionary, key):
    if dictionary == '':
        return None
    return dictionary.get(key)
