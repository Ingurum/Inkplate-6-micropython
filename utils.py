import math

import utime

from config import UTC_OFFSET

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


def time_as_utime(offset=0):
    '''
    Returns the number of seconds since UTC epoch adjusted to the 
    calendar timezone.
    '''

    t = utime.mktime(utime.localtime())  # Seconds since UTC Epoch
    t += int(offset * 3600)  # 3600 = 1 hr in seconds
    # Convert it back to epoch for roll over
    return utime.mktime(utime.localtime(t))


def today_rfc3339(hours_offset=0):
    '''
    Return `today`s date
    '''

    now = time_as_utime(offset=UTC_OFFSET)
    (year, month, day, hours, _, _, _, _) = utime.localtime(now)
    hours += hours_offset
    t = utime.mktime((year, month, day, hours, 0, 0, 0, 0))
    return format_time(t, tz=UTC_OFFSET)


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


class DateTime:
    '''
    Represents a date and time with a UTF offset.
    '''

    def __init__(self, epoch_s, tz=0.):
        self.epoch_s = epoch_s
        self.tz = tz

    def is_today(self):
        today = time_as_utime(self.tz)
        year1, month1, day1, _, _, _, _, _ = utime.localtime(today)
        year2, month2, day2, _, _, _, _, _ = utime.localtime(self.epoch_s)
        return (
            year1 == year2 and
            month1 == month2 and
            day1 == day2
        )

    def formatted(self, include_day=False, include_time=True):
        year, month, day, hours, minutes, _, _, _ = utime.localtime(
            self.epoch_s
        )
        y_m_d = '{:04d}-{:02d}-{:02d} '.format(year, month, day) if include_day == True else ''
        suffix = 'PM' if hours >= 12 else 'AM'
        f_hours = hours % 12
        h_m = '{:02d}:{:02d} {:s}'.format(f_hours, minutes, suffix) if include_time else ''
        return '%s%s' % (y_m_d, h_m)

    @classmethod
    def from_str(cls, formatted):
        '''
        Creates an instance of DateTime using a formatted string.
        '''
        # 0123456790123456789012345
        # 2020-12-24T18:30:00-08:00
        if len(formatted) < 20:
            raise RuntimeError('Invalid formatted string')

        year = int(formatted[0:4])
        month = int(formatted[5:7])
        day = int(formatted[8:10])
        hours = int(formatted[11:13])
        minutes = int(formatted[14:16])
        seconds = int(formatted[17:19])

        epoch_s = utime.mktime(
            (year, month, day, hours, minutes, seconds, 0, 0)
        )

        tz = 0.
        sign = formatted[19]
        # Multiplicative factor
        m = 1.
        hour_offset = 0
        minutes_offset = 0
        if sign != 'Z' and len(formatted[19:]) == 6:
            m = -1. if sign == '-' else 1
            hour_offset = int(formatted[20:22])
            minutes_offset = int(formatted[23:])
            minutes_f = minutes_offset / 60.
            tz = m * (hour_offset + minutes_f)

        return DateTime(epoch_s, tz)

    @classmethod
    def today(cls, tz=UTC_OFFSET):
        epoch_s = time_as_utime(tz)
        return DateTime(epoch_s=epoch_s)
