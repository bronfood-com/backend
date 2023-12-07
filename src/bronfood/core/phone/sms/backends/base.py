from abc import ABC, abstractmethod


class BaseSmsBackend(ABC):
    """Базовый смс бекэнд класс."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def send_message(self, phone_number: int, message: str):
        """Отправляет сообщение на определенный номер."""
        raise NotImplementedError()
