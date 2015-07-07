from urbanairship import common
from datetime import datetime


class IndividualResponseStats(object):
    """Information object for an individual push response

    :ivar push_uuid: Push ID
    :ivar push_time: UTC date and time of the push
    :ivar push_type: Describes the push operation, which is often comparable to
        the audience selection, e.g. BROADCAST_PUSH.
    :ivar direct_responses: Number of direct responses
    :ivar sends: Number of sends
    :ivar group_id: Group ID

    """
    push_uuid = None
    push_time = None
    push_type = None
    direct_responses = None
    sends = None
    group_id = None

    @classmethod
    def from_payload(cls, payload):
        """Create based on results from a ResponseList iterator."""
        obj = cls()
        for key in payload:
            if key in 'push_time':
                payload[key] = datetime.strptime(
                    payload[key], '%Y-%m-%d %H:%M:%S'
                )
            setattr(obj, key, payload[key])
        return obj

    @classmethod
    def get(cls, airship, push_id):
        """Fetch metadata from a push ID"""
        url = common.REPORTS_URL + 'responses/' + push_id
        response = airship._request('GET', None, url, version=3)
        payload = response.json()
        return cls.from_payload(payload)


class ResponseList(object):
    start_url = common.REPORTS_URL + 'responses/list'
    next_url = None
    start_date = None
    end_date = None
    limit = None
    start_id = None
    data_attribute = 'pushes'

    def __init__(self, airship, start_date, end_date, limit=None, start_id=None):
        self._airship = airship
        self.next_url = self.start_url
        self._token_iter = iter(())
        if not start_date or not end_date:
            raise TypeError('start_date and end_date cannot be empty')
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise ValueError(
                'start and end date must both be datetime objects')
        self.start_date = start_date
        self.end_date = end_date
        if limit is not None:
            self.limit = limit
        if start_id is not None:
            self.start_url = start_id

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return IndividualResponseStats.from_payload(next(self._token_iter))
        except StopIteration:
            self._fetch_next_page()
            return IndividualResponseStats.from_payload(next(self._token_iter))

    def next(self):
        """Necessary for iteration to work with Python 2.*."""
        return self.__next__()

    def _fetch_next_page(self):
        if not self.next_url:
            return
        self._load_page(self.next_url)
        self.next_url = self._page.get('next_page')

    def _load_page(self, url):
        params = {
            'start': self.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': self.end_date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        if self.limit is not None:
            params['limit'] = self.limit
        if self.start_id is not None:
            params['start_id'] = self.start_id

        response = self._airship._request(
            method='GET',
            body=None,
            url=url,
            version=3,
            params=params
        )
        self._page = page = response.json()
        self._token_iter = iter(page[self.data_attribute])
