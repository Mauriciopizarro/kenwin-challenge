from abc import ABC, abstractmethod


class Publisher(ABC):
    @abstractmethod
    def send_message(self, message: dict, topic: str):
        pass
