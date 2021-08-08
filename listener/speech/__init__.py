from abc import ABC, abstractmethod


class SpeechInterface(ABC):
    @classmethod
    @abstractmethod
    def recognize(cls, audio) -> str or bool:
        pass

    @classmethod
    @abstractmethod
    def recognize_from_file(cls, audio):
        pass
