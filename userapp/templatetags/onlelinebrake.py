from django import template

import math

register = template.Library()

@register.filter(name="onlelinebrake")
def onlelinebrake(value):
    a = value
    b = a.split(maxsplit=1)

    c = "<br>".join(b)
    return c



@register.filter()
def multiply(value, arg):
    return float(value) * arg


@register.simple_tag()
def calculate_progress_bar(total_quantity,stock):
    try:
        progressbar = total_quantity*(100/stock)
    except:
        progressbar = 0
    return math.floor(progressbar)


