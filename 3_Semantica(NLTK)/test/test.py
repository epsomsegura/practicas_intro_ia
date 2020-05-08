import speech_recognition as sr
from gtts import gTTS
import os
import nltk
from nltk import grammar, parse
from nltk import load_parser 

from nltk.parse.generate import generate

# def hacerEco(texto):
# 	tts = gTTS(text=texto, lang='es')
# 	tts.save("voz.mp3")
# 	os.system("mpg321 voz.mp3")

# def reconocerVoz():
# 	texto = ""
# 	r = sr.Recognizer()
# 	mic = sr.Microphone()
# 	print("Habla ahora o calla para siempre")
# 	with mic as source:
# 	    r.adjust_for_ambient_noise(source)
# 	    audio = r.listen(source)
	
# 	texto = r.recognize_google(audio, language="es-MX")
# 	print(texto)
# 	return texto

# gramatica = nltk.CFG.fromstring("""
# 	S -> VP NP
# 	VP -> V Det1 Det2
# 	V -> "tirar" | "jugar" | "poner"
# 	Det1 -> "en" 
# 	Det2 -> "el" | "la"
# 	NP -> N Numero
# 	N -> "posición" | "casilla" | "espacio" | "número"
# 	Numero -> "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "uno" | "dos" | "tres" | "cuatro" | "cinco" | "seis" | "siete" | "ocho" | "nueve"
# 	""")

# x = "";
# text = reconocerVoz()
# tokens = text.split()
# rd_parser = nltk.RecursiveDescentParser(gramatica)
# for tree in rd_parser.parse(tokens):
# 	x = tree[1][1].leaves()[0]

# x = "Usted jugó en la posición disponible número "+x
# hacerEco(x)


# SEMANTICA
gramatica2 = grammar.FeatureGrammar.fromstring("""
		% start S
		S[SEM=<?vp(?np)>] -> VP[SEM=?vp] NP[SEM=?np]
		S[SEM=<jugar(?np)>] -> NP[SEM=?np]
		
		VP[SEM=?v] -> V[SEM=?v] PREPO
		V[SEM=<\\x.jugar(x)>] -> "tirar" | "jugar" | "poner" 
		PREPO -> "en"
		
		NP[SEM=?num] -> ARTICULO SUSTANTIVO NUM[SEM=?num]
		NP[SEM=?num] -> PREPO ARTICULO NUM[SEM=?num]
		NP[SEM=?num] -> ARTICULO NUM[SEM=?num]
		ARTICULO -> "el" | "la"
		SUSTANTIVO -> "casilla" | "posición" | "número" | "espacio"
		
		NUM[SEM=<1>] -> "1" | "uno"
		NUM[SEM=<2>] -> "2" | "dos"
		NUM[SEM=<3>] -> "3" | "tres"
		NUM[SEM=<4>] -> "4" | "cuatro"
		NUM[SEM=<5>] -> "5" | "cinco"
		NUM[SEM=<6>] -> "6" | "seis"
		NUM[SEM=<7>] -> "7" | "siete"
		NUM[SEM=<8>] -> "8" | "ocho"
		NUM[SEM=<9>] -> "9" | "nueve"
	""")

parser = parse.FeatureEarleyChartParser(gramatica2)

text = "jugar en la casilla 9"
tokens = text.split()
trees = parser.parse(tokens)
semantica = tree.label()['SEM']

