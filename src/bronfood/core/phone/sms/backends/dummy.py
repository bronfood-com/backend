from .base import BaseSmsBackend


class SmsBackend(BaseSmsBackend):
    """Фиктивный смс бэкенд для отладки"""

    def send_message(self, phone_number: int, message: str):
        """Собственная реализация метода отправки смс, фиктивным классом."""
        pass
