# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

# import speech_recognition as sr

# sr.__version__
# r = sr.Recognizer()
# harvard = sr.AudioFile('harvard.wav')
# with harvard as source:
#    audio = r.record(source)   

# HOUNDIFY_CLIENT_ID = "MVuLCSm0xbs7Iu0Potd_-Q=="  # Houndify client IDs are Base64-encoded strings
# HOUNDIFY_CLIENT_KEY = "_i1hm1GMJgynzaM8d35EGoA520IEgacOIpncH23JyYnOqTqcsW0pO5BVx-bSmOQa2JNcyPkZ_-Zy822F65mtIQ=="  # Houndify client keys are Base64-encoded strings
# try:
#     print("Houndify: " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
# except sr.UnknownValueError:
#     print("Houndify could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Houndify service; {0}".format(e))

# print('\n\n')
# print('Google:', r.recognize_google(audio))


# with harvard as source:
#    audio1 = r.record(source, duration=5)
#    audio2 = r.record(source, duration=5)
   
# print('audio1:', r.recognize_google(audio1))
# print('audio2:', r.recognize_google(audio2))


import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()

print("speak:")
with mic as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
        
print(r.recognize_google(audio, language="es-MX"))
