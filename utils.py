import math
import utime


always_safe = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-'


def quote(s):
    res = []
    for c in s:
        if c in always_safe:
            res.append(c)
            continue
        res.append('%%%x' % ord(c))
    return ''.join(res)


def urlencode(query):
    if isinstance(query, dict):
        query = query.items()
    l = []
    for k, v in query:
        if not isinstance(v, list):
            v = [v]
        for value in v:
            k = quote(str(k))
            v = quote(str(value))
            l.append(k + '=' + v)
    return '&'.join(l)


def time(offset=0):
    '''
    Returns the number of seconds since UTC epoch adjusted to the 
    calendar timezone.
    '''

    t = utime.mktime(utime.localtime())  # Seconds since UTC Epoch
    t += int(offset * 3600)  # 3600 = 1 hr in seconds
    # Convert it back to epoch for roll over
    return utime.mktime(utime.localtime(t))


def format_time(t, tz=0.):
    '''
    Formats a timestamp based on RFC 3339
    '''
    year, month, day, hours, minutes, seconds,  _, _ = utime.localtime(t)
    f_tz = format_tz(tz)
    # RFC 3339 Timestamp
    # 2011-06-03T10:00:00-07:00
    # 2011-06-03T10:00:00Z
    return '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}{:s}'.format(year, month, day, hours, minutes, seconds, f_tz)


def format_tz(tz):
    '''
    Formats the `tz` offset to a string.
    '''
    a = abs(tz)
    f = math.floor(a)
    d = a - f

    hours = int(f)
    minutes = int(d * 60)

    if tz == 0:
        return 'Z'

    sign = '+' if tz > 0 else '-'
    return '{:s}{:02d}:{:02d}'.format(sign, hours, minutes)
