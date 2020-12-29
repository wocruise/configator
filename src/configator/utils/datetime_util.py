#!/usr/bin/env python3

from datetime import datetime

def strftime(date_time=None, timeformat='%Y-%m-%dT%H:%M:%S.%f%z'):
    if date_time is None:
        date_time = datetime.utcnow()
    return date_time.strftime(timeformat)

def fromtimestamp(timestamp, unixtime=False):
    try:
        if unixtime:
            return datetime.utcfromtimestamp(timestamp/1000)
        else:
            return datetime.utcfromtimestamp(timestamp)
    except Exception as err:
        return None
