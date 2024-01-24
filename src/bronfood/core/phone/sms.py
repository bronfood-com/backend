from urllib.parse import urlencode, urljoin

from django.conf import settings
from requests import Response, post


class SMSMessage:
    """
    Class for creating SMS messages.
    Usage:
        >>> SMSMessage('76665554433', 'Your code: 0001').send()
    """
    URL = settings.VENDORS.get('URL')
    ORIGINATOR = settings.VENDORS.get('ORIGINATOR')
    USERNAME = settings.VENDORS.get('USERNAME')
    PASSWORD = settings.VENDORS.get('PASSWORD')

    def __init__(self, phone_number: str, message: str):
        self.phone_number = phone_number
        self.message = message
        self.parameters = {
            'action': 'sendmessage', 'username': self.USERNAME,
            'password': self.PASSWORD, 'recipient': self.phone_number,
            'messagetype': 'SMS:TEXT', 'originator': self.ORIGINATOR,
            'messagedata': self.message
        }

    def _make_request(self, method, url) -> Response:
        return method(url)

    def send(self):
        """Sends a message to the specified numbers."""
        if settings.ENV_NAME == 'local':
            return
        self._make_request(
            post, urljoin(self.URL, urlencode(self.parameters))
        )
