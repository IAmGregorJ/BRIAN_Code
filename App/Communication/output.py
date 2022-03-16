'''imports'''
import os
from gtts import gTTS
import playsound

class Output():
    '''used for speaking results'''
    def __init__(self):
        pass
    def say(self, text):
        '''the actual speech'''
        tts = gTTS(text=text, lang="en", tld="ca")
        filename = "voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        print(text)
        os.remove("voice.mp3")
