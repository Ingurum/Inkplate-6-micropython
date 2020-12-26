import time

import network
import ntptime

from config import (
    CLIENT_ID,
    CLIENT_SECRET,
    DISCOVERY_ENDPOINT,
    SAVED_LOCATION,
    SCOPES,
    WLAN_PASSWORD,
    WLAN_SSID
)
from images import CALENDAR_40_40
from inkplate import Inkplate
from layout import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT, Column, Row
from device import DeviceAuth

# Shell
'''
picocom /dev/ttyUSB0 -b115200
'''

# Copy files.
'''
python pyboard.py --device /dev/ttyUSB0 -f cp app.py config.py device.py images.py layout.py path.py text.py urlencode.py :
python pyboard.py --device /dev/ttyUSB0 app.py
'''


class App:
    '''
    The Calendar App.
    '''

    def __init__(self):
        self.display = Inkplate(Inkplate.INKPLATE_1BIT)
        self.display.begin()
        self.width = self.display.width()
        self.height = self.display.height()
        # Connection state.
        self.connecting = False
        self.connected = False
        # Auth state
        self.authorizing = False
        self.authorized = False

    def connect_to_network(self):
        '''
        Connects to WiFi, and sync-s Network time
        '''

        self._notify('Initializing', messages=[
            'Connecting to %s' % (WLAN_SSID)
        ])
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        delay = 0
        if not wlan.isconnected():
            self.connecting = True
            wlan.connect(WLAN_SSID, WLAN_PASSWORD)
            while not wlan.isconnected() and delay < 50:
                time.sleep_ms(200)
                delay += 1

        if not wlan.isconnected():
            message = 'Cannot connect to WiFi SSID %s' % (WLAN_SSID)
            self._error(message)
            return

        config = wlan.ifconfig()
        print('Connected with config', config)
        self._notify('Initializing', messages=[
            'Sync-ing real time clocks with Network'
        ])
        print('Sync-ing network time.')
        ntptime.settime()
        self.connecting = False
        self.connected = True

    def initialize(self):
        '''
        Initialize App.
        '''
        self.connect_to_network()
        self.device_auth = DeviceAuth.from_file(SAVED_LOCATION)
        if not self.device_auth or self.device_auth.authorized == False:
            #  Initialize auth
            self.device_auth = DeviceAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                discovery_endpoint=DISCOVERY_ENDPOINT,
                scopes=SCOPES,
                saved_location=SAVED_LOCATION
            )

            self.device_auth.discover()
            self.authorizing = True
            self.device_auth.authorize()
            user_code = self.device_auth.user_code
            verification_url = self.device_auth.verification_url
            current_attempt = 0
            max_attempts = 20
            while not self.device_auth.authorized and current_attempt < max_attempts:
                messages = [
                    '%s to continue' % (verification_url),
                    'Attempt %s of %s' % (current_attempt + 1, max_attempts)
                ]
                self._notify(user_code, messages=messages)
                self.device_auth.check_authorization_complete(max_attempts=1)
                time.sleep(5)  # Sleep duration in seconds.
                current_attempt += 1

            if not self.device_auth.authorized:
                message = 'Unable to authorize the application.'
                self._error(message=message)
                return

        self._notify('Syncing', messages=[
            'Updating calendar events'
        ])

    def _error(self, message):
        messages = [message]
        print(message)
        self._notify('Error', messages=messages)

    def _notify(self, title, messages=list()):
        root = Column(
            layout_width=self.width,
            layout_height=self.height,
            padding=10
        )
        header = Row(
            parent=root,
            layout_height=40,
            wrap_content=False
        )
        header.add_text_content('Calendar', text_size=4)
        header.add_image(CALENDAR_40_40, 40, 40, align=ALIGN_RIGHT)
        content_root = Row(
            parent=root,
            layout_height=520,
            wrap_content=False,
            outline=True
        )
        content = Column(
            parent=content_root,
            wrap_content=False
        )
        content.add_spacer(10, outline=True)
        content.add_spacer(self.width // 4)
        content.add_text_content(title, text_size=6, align=ALIGN_CENTER)
        for message in messages:
            content.add_text_content(message, align=ALIGN_CENTER)
        content_root.add_node(content)
        root.add_node(header)
        root.add_node(content_root)
        self._draw(root)

    def _draw(self, node):
        self.display.clearDisplay()
        node.draw(self.display, 0, 0)
        self.display.display()


if __name__ == '__main__':
    app = App()
    print('Initializing app.')
    app.initialize()
