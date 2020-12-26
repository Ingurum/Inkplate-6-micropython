import urequests as requests
import utime

from config import API_KEY
from utils import format_time, time, urlencode


class Calendar:
    '''
    A Google Calendar API Client
    '''

    def __init__(self, device_auth):
        self.device_auth = device_auth
        if not self.device_auth.authorized:
            raise RuntimeError('Unauthorized.')

    def events(self, limit=20):
        # Calendar id is part of the endpoint iself.
        endpoint = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
        start_time = format_time(time())
        token = self.device_auth.token()
        authorization = 'Bearer %s' % (token)
        headers = {
            'Authorization': authorization,
            'Accept': 'application/json'
        }
        payload = {
            'maxResults': limit,
            'orderBy': 'startTime',
            'singleEvents': 'true',
            'timeMin': start_time,
            'key': API_KEY
        }
        encoded = urlencode(payload)
        r = requests.request(
            'GET',
            endpoint,
            data=encoded,
            headers=headers
        )
        j = r.json()
        r.close()

        if 'error' in j:
            raise RuntimeError(j['message'])

        return self._parse_calendar_events(j)

    def _parse_calendar_events(self, j):
        events = list()
        if not 'items' in j:
            return events

        items = j['items']
        for i in range(len(items)):
            item = items[i]
            event = Event(item)
            events.append(event)

        return events


class Event:
    '''
    A Calendar Event
    '''

    def __init__(self, j):
        self.summary = j['summary']
        self.description = j['description']
        # 2020-11-18T01:17:18.000Z
        self.start_at = j['start']['dateTime']

    def _year(self):
        return int(self.start_at[0:4])

    def _month(self):
        return int(self.start_at[5:7])

    def _day(self):
        return int(self.start_at[8:10])

    def _hours(self):
        return int(self.start_at[11:13])

    def _minutes(self):
        return int(self.start_at[14:16])

    def _seconds(self):
        return int(self.start_at[17:19])

    def formatted_time(self):
        pass
