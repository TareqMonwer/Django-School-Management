from django import template

register = template.Library()

@register.filter(name='str_replace')
def str_replace(value, args):
    replace_char, replace_by = args.split(',')
    return value.replace(replace_char, replace_by).title()