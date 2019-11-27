from django import template

register = template.Library()


@register.filter(name='num_suffix')
def num_suffix(number):
    if number == 1:
        return '1st'
    if number == 2:
        return '2nd'
    if number == 3:
        return '3rd'
    if 3 < number <= 12:
        return '%sth' % number
