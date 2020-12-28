import time

import machine
import network
import ntptime
import utime

from config import WLAN_PASSWORD, WLAN_SSID
from inkplate import Inkplate

display = Inkplate(Inkplate.INKPLATE_1BIT)
width = display.width()
height = display.height()


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

def deep_sleep():
    print('About to deep sleep')
    machine.deepsleep(10 * 1000)


if __name__ == "__main__":
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('Waking up.')

    deep_sleep()

    
