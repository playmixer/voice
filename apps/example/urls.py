from .voices import *
from listener import appeal

url_voices = [
    appeal('компьютер', Hello(), ['привет']),
    appeal('компьютер', CurrentTime()),
    appeal('компьютер', OpenNotePad()),
    appeal('компьютер', TestRunScript()),
    appeal('компьютер', Weather())
]
