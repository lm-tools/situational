import datetime

from django import template

register = template.Library()


def human_time(value):
    time_away = int(value)
    seconds_elapsed = datetime.timedelta(minutes=time_away).seconds
    if seconds_elapsed < 60:
        return "now"
    if seconds_elapsed < 3300:
      minutes = round(seconds_elapsed/60)
      return "{0} minute{1}".format(minutes, "s"[minutes==1:])
    if seconds_elapsed < 86400:
        hours = round(seconds_elapsed/3600)
        return "{0} hour{1}".format(hours, "s"[hours==1:])

    days = round(seconds_elapsed/86400)
    return "{0} day".format(days, "s"[days==1:])


register.filter('human_time', human_time)

