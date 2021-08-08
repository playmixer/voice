import speech_recognition as sr
from abc import ABC, abstractmethod
from typing import List, NoReturn
import importlib
from . import voice

__all__ = ['Listener', 'HandleInterface', 'urls']


def urls(imprt: str):
    mod = importlib.import_module(imprt)
    url_voices = mod.url_voices
    return url_voices


TEXT = 1
VOICE = 2


class HandleInterface(ABC):
    said = None
    owner = None
    response_success = None
    response_error = 'Ошибка выполнения операции'
    response_type = VOICE + TEXT

    def set_owner(self, owner):
        self.owner = owner

    def talk_response(self, response: str):
        if response:
            if self.response_type & TEXT:
                print(f'Ответ: {response}')
            if self.response_type & VOICE:
                voice.voice_p(response)

    def on_finish(self):
        """
        Ответ при успешном выполнении
        :return:
        """
        self.talk_response(self.response_success)

    def on_error(self, err):
        """
        Ответ при не успешном выполнении
        :param err:
        :return:
        """
        print(err)
        self.talk_response(self.response_error)

    def do(self, phrase: List[str]) -> bool:
        """
        Запускает хендл
        :param phrase:
        :return:
        """
        phrase = [word.lower() for word in phrase]
        if self.phrase_comparison(phrase):
            try:
                self.action()
                self.on_finish()
            except Exception as err:
                self.on_error(err)

            return True

        return False

    def phrase_comparison(self, phrase: List[str]) -> bool:
        """
        Проверка, вызывается ли текущий хендл
        :param phrase:
        :return:
        """
        # for _p in self.phrase:
        for _p in self.said:
            if HandleInterface.find_in_phrase(phrase, _p.split()):
                return True

        return False

    @classmethod
    def find_in_phrase(cls, phrase_i, phrase_h):
        for word in phrase_h:
            if word not in phrase_i:
                return False

        return True

    @abstractmethod
    def action(self):
        pass


def appeal(name: str, handle: HandleInterface, said: List[str] or None = None):
    if name:
        phrases = said if said else handle.said
        handle.said = [' '.join([name.lower(), s]) for s in phrases]
    return handle


class Listener:
    handlers = list()
    name = None
    speech_interface = None

    def __init__(self, names: List[str] = None, recognizer='google'):
        self.name = names
        exec(f'from .speech.{recognizer} import Speech')
        self.speech_interface = eval('Speech')

    def __talk_me__(self, talk) -> List[str]:
        """
        Проверка обращается ли пользователь к программе
        если задано имя
        :param talk:
        :return:
        """

        if self.name is None:
            return talk

        index = None
        for name in self.name:
            try:
                index = talk.index(name)
                if index is not None:
                    break
            except ValueError:
                pass

        return [] if index is None else talk[index + 1:]

    def start(self):
        while True:
            self.__record_handler__()

    def recognize_file(self, file, language='ru-Ru'):
        """
        Распознать из файла
        :param file:
        :param language:
        :return:
        """
        # r = sr.Recognizer()
        # with sr.AudioFile(file) as source:
        #     audio = r.record(source)
        # query = r.recognize_google(audio, language=language)
        # text = query.lower()
        # self.__check_handles__(text)
        # speech = self.speech_interface()

    def __check_handles__(self, text):
        """
        Проверка хендлов
        :param text:
        :return:
        """
        text_to_app = self.__talk_me__(text.split())
        if text_to_app:
            for handle in self.handlers:
                if handle.do(text_to_app):
                    return True

            return False

    def __record_handler__(self) -> None:
        """
        Слушать микрофон
        :return:
        """
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            print('Настраиваюсь.')
            r.adjust_for_ambient_noise(source, duration=0.5)  # настройка посторонних шумов
            print('Слушаю...')
            audio = r.listen(source)
            print('Услышала.')
            try:
                speech = self.speech_interface
                query = speech.recognize(audio)
                if query:
                    text = query.lower()
                    print(f'Вы сказали: {text}')
                    if not self.__check_handles__(text):
                        pass
                        # voice.voice_p('Простите. Я вас не поняла')

            except Exception as err:
                print('Error', err)

    def init_handle(self, app: HandleInterface):
        self.handlers.append(app)

    def init_handles(self, handlers: List[HandleInterface]):
        for handle in handlers:
            self.handlers.append(handle)
