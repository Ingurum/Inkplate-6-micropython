import urequests as requests

from config import API_KEY
from utils import DateTime, today_rfc3339, urlencode


class Calendar:
    '''
    A Google Calendar API Client
    '''

    def __init__(self, device_auth):
        self.device_auth = device_auth
        if not self.device_auth.authorized:
            raise RuntimeError('Unauthorized.')

    def events(self, limit=5):
        # Calendar id is part of the endpoint iself.
        endpoint = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
        start_time = today_rfc3339(hours_offset=-1)
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
        full_url = '%s?%s' % (endpoint, encoded)
        r = requests.request(
            'GET',
            full_url,
            headers=headers
        )
        j = r.json()
        r.close()

        if 'error' in j:
            raise RuntimeError(j)

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

        self.description = None
        self.start_at = None
        self.end_at = None

        if 'description' in j:
            self.description = j['description']
        if 'start' in j and 'dateTime' in j['start']:
            # 2020-12-24T18:30:00-08:00
            formatted = j['start']['dateTime']
            self.start_at = DateTime.from_str(formatted)
        if 'end' in j and 'date' in j['end']:
            # '2021-01-02'
            formatted = j['end']['date']
            self.end_at = DateTime.from_str(formatted)
