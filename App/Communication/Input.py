'''imports'''
import speech_recognition as sr
from neuralintents import GenericAssistant

class Input():
    '''used to listen, hear and speak'''
    def __init__(self) -> None:
        pass
    def listen(self):
        '''listen'''
        recon = sr.Recognizer()
        print("Listening...")
        with sr.Microphone() as source:
            recon.adjust_for_ambient_noise(source, duration = 0.2)
            audio = recon.listen(source)
            said = ""
            try:
                said = recon.recognize_google(audio)
                print(said) #should be removed once tested
            except sr.UnknownValueError as ex:
                print("No sound received: " + str(ex))
            return said.lower()
    def dictate(self, recon, audio):
        '''same as hear but with better text recognition'''
        recon = sr.Recognizer()
        print("Listening...")
        with sr.Microphone() as source:
            recon.adjust_for_ambient_noise(source, duration = 0.2)
            audio = recon.listen(source)
            said = ""
            try:
                said = recon.recognize_google(audio, language="en-CA")
                for punct in ((" comma", ","),
                            (" period", "."),
                            (" exclamation point", "!"),
                            (" question mark", "?")):
                    said = said.replace(*punct)
                print(said) #should be removed once tested
            except sr.UnknownValueError as ex:
                print("No sound received: " + str(ex))
            return said
    def interpret(self, text):
        '''use intents engine to find out what function should be called'''
        mappings = {'''
            "greeting": hello,
            "create_note": create_note,
            "add_todo": add_todo,
            "show_todos": show_todos,
            "time": tell_time,
            "alarm": alarm_clock,
            "reminder": reminder,
            "exit": quit'''
        }
        assistant = GenericAssistant(
            '.Ressources/intents.json',
            intent_methods = mappings,
            model_name="brian_model"
            )
        assistant.train_model()
        assistant.save_model()
        assistant.request(text)
