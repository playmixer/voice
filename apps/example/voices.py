from listener import HandleInterface, TEXT
from listener.voice import voice_p
from datetime import datetime
import requests
from functools import lru_cache


class Hello(HandleInterface):
    said = ["привет", "здравствуй"]

    def action(self):
        voice_p("привет")


class CurrentTime(HandleInterface):
    said = [
        "текущее время",
        "который час",
        "сколько времени"
    ]

    response_success = f'текущее время {datetime.now().strftime("%H %M")}'

    def action(self):
        pass


class OpenNotePad(HandleInterface):
    said = ["открой блокнот"]
    response_success = 'открываю'
    response_type = TEXT

    def action(self):
        import subprocess
        subprocess.Popen(["notepad.exe"])


class TestRunScript(HandleInterface):
    said = ["тест скрипт", "test script"]

    def action(self):
        import subprocess
        subprocess.Popen(["pypy3", "F:\\downloads\\pytest.py"])


class Weather(HandleInterface):
    said = ["какая погода", "скажи погоду", "сколько градусов", "текущая температура"]
    API_KEY = '6c82976e-2775-4f53-a53f-35d278239501'
    cities = {
        'Омск': (54.97484764801261, 73.4775385177515)
    }

    @staticmethod
    @lru_cache(maxsize=32)
    def get_weather(cls, coord: tuple):
        lat, lon = coord
        data = requests.get(f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}",
                            headers={
                                'X-Yandex-API-Key': cls.API_KEY
                            }).json()
        # import json
        # with open('./apps/example/weather.json') as file:
        #     data = json.loads(file.read())
        temp = data["fact"]["temp"]
        feels_like = data["fact"]["feels_like"]
        return f"Температура {temp}, ощущается как {feels_like}"

    def action(self):
        res = Weather.get_weather(self, self.cities['Омск'])
        self.response_success = res
