import time

import network
import ntptime
import utime

from config import WLAN_PASSWORD, WLAN_SSID, UTC_OFFSET
from inkplate import Inkplate

display = Inkplate(Inkplate.INKPLATE_1BIT)
width = display.width()
height = display.height()


def time_stamp(year, month, day, hours=0, minutes=0, seconds=0):
    # RFC 3339 Timestamp
    # 2011-06-03T10:00:00Z
    return '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z'.format(year, month, day, hours, minutes, seconds)


def initialize():
    # Must be called before using, line in Arduino
    display.begin()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WLAN_SSID, WLAN_PASSWORD)
    delay = 0
    while not wlan.isconnected() and delay < 50:
        time.sleep_ms(200)
        delay += 1

    ntptime.settime()


def draw_grid():
    for i in range(0, height, 10):
        display.drawFastHLine(0, i, width, display.BLACK)

    for i in range(0, width, 10):
        display.drawFastVLine(i, 0, height, display.BLACK)

    y = 10
    for i in range(1, 11, 1):
        display.setTextSize(i)
        display.printText(10, y, 'Hello World'.upper())
        y += 9 * i

    display.display()


def rfc_3339_offset(year, month, day, hours=0, minutes=0, seconds=0):
    t = utime.mktime((year, month, day, hours, minutes, seconds, 0, 0))
    t += UTC_OFFSET * 3600  # 1 hr in seconds
    a_year, a_month, a_day, a_hours, a_minutes, a_seconds, _, _ = utime.localtime(
        t
    )
    return time_stamp(a_year, a_month, a_day, a_hours, a_minutes, a_seconds)


if __name__ == "__main__":
    initialize()
    draw_grid()
