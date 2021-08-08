import settings
from . import SpeechInterface
import requests
import json
import os

FOLDER_ID = settings.YANDEX_FOLDER_ID


class Speech(SpeechInterface):
    token = None

    @classmethod
    def recognize(cls, audio) -> str or bool:
        if cls.token is None:
            cls.token = cls.get_iam_token()

        data = audio.get_wav_data(
            convert_rate=8000,  # audio samples must be 8kHz or 16 kHz
            convert_width=2  # audio samples should be 16-bit
        )

        params = "&".join([
            "topic=general",
            "folderId=%s" % FOLDER_ID,
            "lang=ru-RU",
            "format=lpcm",
            "sampleRateHertz=8000"
        ])

        try:
            res = requests.post("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data,
                                headers={"Authorization": "Bearer %s" % cls.token})

            responseData = res.json()
            decodedData = responseData

            if decodedData.get("error_code") is None:
                text = decodedData.get("result")
                return text
            else:
                if decodedData.get("error_message").find("The token has expired") + 1:
                    cls.token = cls.get_iam_token()

        except Exception as err:
            print(err)
        return False

    @classmethod
    def recognize_from_file(cls, audio):
        pass

    @classmethod
    def get_iam_token(cls):
        PATH = './cache/yandex_weather_token.json'
        token = None
        data = {}

        if os.path.exists(PATH):
            with open(PATH, 'r') as f:
                text = f.read()
                data = json.loads(text)

        if token is None:
            params = {
                "yandexPassportOauthToken": settings.YANDEX_OAUTH_TOKEN
            }
            url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"

            response = requests.post(url, params=params)
            data = response.json()
            with open(PATH, 'w' if os.path.exists(PATH) else 'x') as f:
                f.write(json.dumps(data))

        try:
            token = data.get("iamToken")
            print("->\tПолучен iam yandex token")
        except Exception as err:
            print(err)
            print(data)

        return token
