# Librerias del proyecto
import speech_recognition as sr
from gtts import gTTS
import os

# Funciones
# Función que almacena el archivo de audio a reproducir
def hacerEco(texto):
	if(texto == ""):
		texto == "No pude reconocer tu voz"	
	tts = gTTS(text=texto, lang='es')
	tts.save("echo.mp3")
	os.system("mpg321 echo.mp3")

def reconocerVoz():
	texto = ""
	r = sr.Recognizer()
	mic = sr.Microphone()
	with mic as source:
	    r.adjust_for_ambient_noise(source)
	    audio = r.listen(source)

	try:
		texto = r.recognize_google(audio, language="es-MX")
	except sr.UnknownValueError:
		hacerEco('No pude reconocer lo que dijiste, intenta de nuevo')
		operaciones()
	except sr.RequestError as e:
		hacerEco('No pude procesar tu voz')
	return texto 


def operaciones():
	texto = ""
	# Ejecución de la función
	while(texto != "adiós"):
		texto = reconocerVoz()
		hacerEco(texto)


# Instrucciones
print('Menciona algo y lo repetiré, para salir solo dí adios\n\n')
hacerEco('Menciona algo y lo repetiré, para salir solo dí adios')
operaciones()

