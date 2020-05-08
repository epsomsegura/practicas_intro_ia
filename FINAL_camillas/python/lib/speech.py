# Librerias
from gtts import gTTS
import os
import platform

class speech:
    # Constantes
    PATH = 'audio/voice.mp3'
    PLAYER = 'cmdmp3' if platform.system() == 'Windows' else 'mpg321' if platform.system() == 'Darwin' else 'mpg321'

    # Constructor
    def __init__(self):
        self.PATH
        self.PLAYER

    # Función que convierte una cadena de texto a voz sintética
    def speech(self,texto):
        print(texto)
        tts = gTTS(text=texto, lang='es')
        tts.save(self.PATH)
        os.system(self.PLAYER+" "+self.PATH)