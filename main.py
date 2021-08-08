import listener
import urls

app = listener.Listener(recognizer='yandex')

app.init_handles(urls.url_voices)

if __name__ == '__main__':
    app.start()
    # audio = './listener/examples_audio/what_is_time.wav'
    # app.recognize_audio(audio)

    # from listener.speech.yandex import Speech
    #
    # speech = Speech('./listener/examples_audio/what_is_time.ogg')
    # text = speech.speech()
    # print(text)
