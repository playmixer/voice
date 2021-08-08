from . import SpeechInterface
import speech_recognition as sr


class Speech(SpeechInterface):
    @classmethod
    def recognize(cls, audio) -> str or bool:
        r = sr.Recognizer()
        try:
            query = r.recognize_google(audio, language='ru-RU')
            text = query.lower()
            return text

        except Exception as err:
            print(err)
        return False

    @classmethod
    def recognize_from_file(cls, audio):
        pass
