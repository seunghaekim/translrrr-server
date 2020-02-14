from django.db import models
from django.utils import timezone
from django.utils import dateparse

def default_id(models):
    return models.AutoField(primary_key=True)


def default_deletetime(models):
    return models.DateTimeField(auto_now=False, auto_now_add=False, null=True, default=None)


def default_updatetime(models):
    return models.DateTimeField(auto_now=True, null=True)


def default_createtime(models):
    return models.DateTimeField(auto_now=False, auto_now_add=True, null=False, blank=False)


def datetimenow():
    return timezone.now()


# 2019-12-26T14:16:00.000Z
def default_datetime_value(datetimestr):
    dt = dateparse.parse_datetime(datetimestr).replace()
    dtnow = datetimenow()

    if dt.second < 1:
        dt.replace(second=dtnow.second)

    if dt.microsecond < 1:
        dt.replace(microsecond=dtnow.microsecond)

    return dt
