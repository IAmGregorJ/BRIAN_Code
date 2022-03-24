'''imports'''
import string
import speech_recognition as sr
import requests
import Communication.Output as out
from Functions import Status as st, TimeFunctions as tf, SystemFunctions as sf, Sayings as sa

class SpeechIn:
    '''used to listen, hear and speak'''
    def __init__(self) -> None:
        url = "http://www.google.com"
        timeout = 5
        try:
            requests.get(url, timeout = timeout)
        except(requests.ConnectionError, requests.Timeout) as ex:
            print("There is no internet connection: " + str(ex))
            nc = out.Output()
            nc.no_connection()
        print("Listening...")
    def listen(self):
        '''listen'''
        recon = sr.Recognizer()
        #print("Listening...")
        with sr.Microphone() as source:
            recon.adjust_for_ambient_noise(source)
            audio = recon.listen(source)
            said = ""
            try:
                said = recon.recognize_google(audio)
                print(said) #should be removed once tested
            except sr.UnknownValueError as ex:
                print("No sound received: " + str(ex))
            except sr.RequestError as ex:
                print(f"The Google speech recognition API was unreachable; {format(ex)}")
            return said.lower()
    def dictate(self):
        '''same as hear but with better text recognition'''
        recon = sr.Recognizer()
        #print("Listening...")
        with sr.Microphone() as source:
            recon.adjust_for_ambient_noise(source)
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
            except sr.RequestError as ex:
                print(f"The Google speech recognition API was unreachable; {format(ex)}")
            return said
    def interpret(self, text):
        '''the intents engine neuralintents died - this is the result'''
        # What happens if you use two "code words" in the same sentence??
        # "Multiple if's means your code would go and check all the if conditions,
        # where as in case of elif, if one if condition satisfies
        # it would not check other conditions.."

        #remove punctuation
        text = text.translate(None, string.punctuation)
        # text = text.translate(None, string.punctuation) # removes eventual punctuation
        # text = text.split() # to catch whole words, and not just substrings
        status_strings = ["how are you",
                            "are you ok",
                            "are you feeling"]
        time_strings = ["what time",
                            "what is the time",
                            "time is it"]
        date_strings = ["what is today's date",
                            "what is the date",
                            "what day is it",
                            "the date"]
        exit_strings = ["exit",
                            "end the program",
                            "I'd like to go",
                            "goodbye",
                            "good bye",
                            "bye bye",
                            "see you later"]
        joke_strings = ["tell me a joke",
                            "something funny",
                            "make me laugh"]
        quote_strings = ["inspire me",
                            "give me a quote",
                            "something inspiring",
                            "inspirational"]

        for phrase in status_strings:
            if phrase in text:
                st.Status()
        for phrase in time_strings:
            if phrase in text:
                tf.TimeFunction.tell_time()
        for phrase in date_strings:
            if phrase in text:
                tf.TimeFunction.tell_date()
        for phrase in exit_strings:
            if phrase in text:
                sf.SystemFunction.exitapp()
        for phrase in joke_strings:
            if phrase in text:
                joke = sa.Joke()
                joke.get_joke()
        for phrase in quote_strings:
            if phrase in text:
                quote = sa.Quote()
                quote.get_quote()
