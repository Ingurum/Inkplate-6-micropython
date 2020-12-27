import time

import network
import ntptime

from calendar_api import Calendar
from config import (
    CLIENT_ID,
    CLIENT_SECRET,
    DISCOVERY_ENDPOINT,
    SAVED_LOCATION,
    SCOPES,
    UTC_OFFSET,
    WLAN_PASSWORD,
    WLAN_SSID
)
from device import DeviceAuth
from images import CALENDAR_40_40
from inkplate import Inkplate
from layout import ALIGN_CENTER, ALIGN_RIGHT, Column, Row
from utils import DateTime

# Shell
'''
picocom /dev/ttyUSB0 -b115200
'''

# Copy files.
'''
python pyboard.py --device /dev/ttyUSB0 -f cp app.py config.py calendar_api.py device.py images.py layout.py path.py text.py utils.py :
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
        # Calender
        self.calendar = None

    def connect_to_network(self, notify=True):
        '''
        Connects to WiFi, and sync-s Network time
        '''

        if notify:
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

        if notify:
            self._notify('Initializing', messages=[
                'Sync-ing real time clocks with Network'
            ])

        print('Sync-ing network time.')
        delay = 0
        time_set = False
        while wlan.isconnected() and not time_set and delay < 10:
            try:
                ntptime.settime()
                time_set = True
            except Exception:
                time.sleep_ms(200)
                delay += 1

        self.connecting = False
        self.connected = wlan.isconnected() and time_set

    def initialize(self, notify=True):
        '''
        Initialize App.
        '''
        self.connect_to_network(notify=notify)
        if not self.connected:
            return

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
        self.build_calendar_ui()


    def build_calendar_ui(self):
        '''
        Builds the actual Calendar UI after making the RESTful request.
        '''
        if not self.device_auth.authorized:
            self._error('Need to authorize first.')

        if not self.calendar:
            self.calendar = Calendar(self.device_auth)

        events = self.calendar.events()
        date_today = DateTime.today()
        sync_at = date_today.formatted()
        sync_at_message = 'Last updated at %s' % (sync_at)
        if len(events) <= 0:
            messages = [
                sync_at_message
            ]
            self._notify('No events.', messages=messages)
        else:
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
            f_date_today = date_today.formatted(include_day=True, include_time=False)
            header.add_text_content('Today - %s' % (f_date_today), text_size=4)
            header.add_image(CALENDAR_40_40, 40, 40, align=ALIGN_RIGHT)
            content_root = Row(
                parent=root,
                layout_height=480,
                wrap_content=False,
                outline=True
            )
            content = Column(
                parent=content_root,
                wrap_content=False
            )
            content.add_spacer(10, outline=True)
            content.add_spacer(20)
            for event in events:
                summary = event.summary
                include_day = not event.start_at.is_today()
                at = 'At %s' % (
                    event.start_at.formatted(include_day=include_day)
                )
                content.add_text_content(summary)
                content.add_text_content(at)
                content.add_spacer(height=15)
            content_root.add_node(content)
            status = Row(
                parent=root,
                layout_height=40,
                wrap_content=False,
                outline=True
            )
            status.add_text_content(sync_at_message, align=ALIGN_RIGHT)
            root.add_node(header)
            root.add_node(content_root)
            root.add_node(status)
            self._draw(root)

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
