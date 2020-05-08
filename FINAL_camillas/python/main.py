# Librerias
import threading
import time
from lib.speech import speech as sp
from lib.voicerecognition import voicerecognition as vr
from lib.python_arduino import arduino_serial as ard
from lib.grammars import grammar_eval as gram
from lib.mongo_con import mongo_con as con
from lib.webserver import webserver as websvr
import requests

class main:
    # Instancias
    conexion = con()
    arduino = ard(conexion)
    hablar = sp()
    escuchar = vr()
    gram = gram()
    URL = "http://127.0.0.1:5000/preferences/update"
  

    # Función para ejecutar las acciones de comunicación serial con el microcontrolador Arduino
    def start_arduino(self):
        self.arduino.arduino_worker()
    
    # Función para ejecutar la interacción con la interfaz inteligente
    def start_voice(self):
        while(True):
            str_escuchar = self.escuchar.getVoice()

            if(str_escuchar != "&%&"):
                reqGrammar = self.gram.evalSemantics(str_escuchar)
                # Sin semántica
                if(reqGrammar=="NOSEMANTICS"):
                    str_voz = "No pude comprender lo que dijiste"
                # Semántica encontrada - Temperatura
                if(reqGrammar[0] == 'getTemp'):
                    if(reqGrammar[2]=="actual"):
                        str_voz = "La temperatura actual es de "+str(self.arduino.temp_sens)+" grados centígrados"
                    elif(reqGrammar[2]=="min"):
                        str_voz = "La temperatura mínima configurada es de "+str(self.arduino.temp_min)+" grados centígrados"
                    elif(reqGrammar[2]=="max"):
                        str_voz = "La temperatura máxima configurada es de "+str(self.arduino.temp_max)+" grados centígrados"
                
                if (reqGrammar[0] == 'modtemp'):
                    if (reqGrammar[1]=="up"):
                        str_voz = "aumentando la temperatura un grado"
                        db = self.conexion.conexion()
                        coleccion = db['sensor_temp']
                        query = {"activo" : "t"}
                        req = list(coleccion.find(query))[0]
                        data = {"$set":{"temp_pref" : req["temp_pref"]+1}}
                        coleccion.update_one(query, data)
                        #Reflejar cambios en KB
                        requests.get(url = self.URL)
                    elif (reqGrammar[1]=="down"):
                        str_voz = "disminuyendo la temperatura un grado"
                        db = self.conexion.conexion()
                        coleccion = db['sensor_temp']
                        query = {"activo" : "t"}
                        req = list(coleccion.find(query))[0]
                        data = {"$set":{"temp_pref" : req["temp_pref"]-1}}
                        coleccion.update_one(query, data)
                        #Reflejar cambios en KB
                        requests.get(url = self.URL)
            
            self.hablar.speech(str_voz)

    def start_websrv(self):
        websvr()

    # Constructor
    def __init__(self):
        # Declaración de hilos necesarios para la ejecución paralela de las funciones
        # de comunicación con microcontrolador Arduino e interfaz inteligente
        thread_arduino = threading.Thread(target=self.start_arduino, name="Arduino thread")
        thread_voice = threading.Thread(target=self.start_voice, name="Voice thread")
        thread_websrv = threading.Thread(target=self.start_websrv, name="WebServer thread")

        # Inicialización de los hilos
        thread_arduino.start()
        thread_voice.start()
        thread_websrv.start()


# Inicializar asistente
if __name__ == '__main__':
    main()