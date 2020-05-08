#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 00:30:50 2018

@author: ebenitez
"""

from gtts import gTTS
import os
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='es')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
    
if __name__ == "__main__":

    # print(os.environ['PATH'])
    # os.environ['PATH'] += ":"+"/Users/epsegura/Google Drive/MSICU/Semestre 2/msicu_s2_inteligenciaartificial/actividades/Actividad_5/src/"
    # print(os.environ['PATH'])
    # print(os.getcwd())
            
    #text to speech    
    speak('Hola, ¡soy goku!')

        
    
    
    
        