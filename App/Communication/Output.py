'''imports'''
import os
from gtts import gTTS
import playsound

class Output:
    '''used for speaking results'''
    def __init__(self):
        pass
    def say(self, text):
        '''the actual speech'''
        tts = gTTS(text=text, lang="en", tld="ca")
        filename = "voice.mp3"
        tts.save(filename)
        print(text)
        playsound.playsound(filename)
        os.remove("voice.mp3")
    def no_connection(self):
        '''if there is no connection'''
        filename = "App/Ressources/no_connection.mp3"
        playsound.playsound(filename)
        exit()
