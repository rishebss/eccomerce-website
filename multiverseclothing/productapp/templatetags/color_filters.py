from django import template

register = template.Library()

@register.filter
def text_color(bg_color):
    light_colors = ['#FFFFFF', '#FFFDD0', '#E6E6FA', '#FFC0CB']
    return 'black' if bg_color in light_colors else 'white'