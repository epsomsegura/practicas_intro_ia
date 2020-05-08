import speech_recognition as sr

class voicerecognition():
    # constructor
    def __init__(self):
        print("Reconocedor de voz en español")

    # Función recursiva para detección de voz y conversión a cadena de texto
    def getVoice(self):
        flag=True
        texto = "&%&"

        while(flag):
            r = sr.Recognizer()
            r.dynamic_energy_threshold = True
            mic = sr.Microphone()
            try:
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, timeout=None, phrase_time_limit=3)
                texto = r.recognize_google(audio, language="es-MX")
                flag = False
            except sr.UnknownValueError:
                texto = '&%&'
            except sr.RequestError as e:
                texto = '&%&'  
        return texto