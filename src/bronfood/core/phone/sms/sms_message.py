from bronfood.core.phone.sms.backends import get_sms_backend
from bronfood.core.phone.sms.backends.base import BaseSmsBackend


class SMSMessage:
    """Класс для создания смс сообщения."""

    def __init__(self, phone_number: int, message: str):
        self.phone_number = phone_number
        self.message = message
        self._provider: BaseSmsBackend = get_sms_backend()

    def send(self):
        """Отправляет смс сообщение на определенный номер."""
        self._provider.send_message(
            phone_number=self.phone_number, message=self.message
        )
