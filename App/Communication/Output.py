'''imports'''
import os
import sys
from gtts import gTTS
import playsound
from sty import fg

class Output:
    '''used for speaking results'''
    def __init__(self):
        self.filename = "voice.mp3"

    @staticmethod
    def remove_voicefile():
        '''remove the file after output'''
        filename = "voice.mp3"
        if filename:
            os.remove(filename)

    @staticmethod
    def create_output(text, lang):
        '''create the output sound file'''
        filename = "voice.mp3"
        if lang == "en":
            tts = gTTS(text = text, lang = "en", tld = "ca")
        else:
            tts = gTTS(text = text, lang = f"{lang}")
        tts.save(filename)
        print(fg.li_red, text, fg.rs)

    @staticmethod
    def say(text, *args):
        '''the actual speech'''
        if not args:
            lang = "en"
        else:
            for val in args:
                l = val
            lang = l
        filename = "voice.mp3"
        Output.create_output(text, lang)
        playsound.playsound(filename)
        Output.remove_voicefile()

    @staticmethod
    def no_connection():
        '''if there is no connection'''
        filename = "App/Ressources/no_connection.mp3"
        playsound.playsound(filename)
        sys.exit()
