from django import template

register = template.Library()


def friendly_adzuna_location(location):
    return location.split(",")[-1]

register.filter('friendly_adzuna_location', friendly_adzuna_location)
