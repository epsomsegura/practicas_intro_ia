from gtts import gTTS
import os
tts = gTTS(text='Hello world', lang='en')
tts.save("good.mp3")
#os.system("mpg321 good.mp3")	