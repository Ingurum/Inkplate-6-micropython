import urequests as requests
import utime

from device import DeviceAuth


class Calendar:
    '''
    A Google Calendar API Client
    '''

    def __init__(self, device_auth):
        self.device_auth = device_auth
        if not self.device_auth.authorized:
            raise RuntimeError('Unauthorized.')
