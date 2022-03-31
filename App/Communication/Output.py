'''imports'''
import os
import sys
from gtts import gTTS
import playsound

class Output:
    '''used for speaking results'''
    def __init__(self):
        self.filename = "voice.mp3"
    def remove_voicefile(self):
        '''remove the file after output'''
        os.remove(self.filename)
    def create_output(self, text):
        '''create the output sound file'''
        tts = gTTS(text = text, lang = "en", tld = "ca")
        tts.save(self.filename)
        print(text)
    def say(self, text):
        '''the actual speech'''
        self.create_output(text)
        playsound.playsound(self.filename)
        self.remove_voicefile()
    def no_connection(self):
        '''if there is no connection'''
        filename = "App/Ressources/no_connection.mp3"
        playsound.playsound(filename)
        sys.exit()
