from django import template

register = template.Library()

def parse_query(value):
    return