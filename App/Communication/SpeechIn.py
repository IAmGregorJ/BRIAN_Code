'''imports'''
import string
import speech_recognition as sr
import requests
import Communication.Output as out
from Functions import (
    Status as st,
    TimeFunctions as tf,
    SystemFunctions as sf,
    Sayings as sa,
    Todos as todo,
    SearchWikipedia as wp,
    Translation as tr,
    SearchWolfram as wa,
    CommandLogs as cl,
    Email as em,
    Contacts as ct,
    Help as hl
)
from sty import fg

class SpeechIn:
    '''used to listen, hear and speak'''
    def __init__(self, usermail) -> None:
        self.mail = usermail
        url = "http://www.google.com"
        timeout = 5
        self.recon = sr.Recognizer()
        try:
            requests.get(url, timeout = timeout)
        except(requests.ConnectionError, requests.Timeout) as ex:
            print("There is no internet connection: " + str(ex))
            out.Output.no_connection()

    @staticmethod
    def listen():
        '''listen'''
        recon = sr.Recognizer()
        with sr.Microphone() as source:
            recon.adjust_for_ambient_noise(source, duration=0.5)
            audio = recon.listen(source)
            said = ""
            try:
                said = recon.recognize_google(audio)
                time = tf.TimeFunction.print_time()
                print("")
                print(fg.green, time, said, fg.rs)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as ex:
                print(f"The Google speech recognition API was unreachable; {format(ex)}")
            return said.lower()

    @staticmethod
    def dictate():
        '''same as hear but with better text recognition'''
        recon = sr.Recognizer()
        with sr.Microphone() as source:
            recon.adjust_for_ambient_noise(source, duration=0.5)
            audio = recon.listen(source)
            said = ""
            try:
                said = recon.recognize_google(audio, language="en-CA")
                for punct in ((" comma", ","),
                            (" period", "."),
                            (" exclamation point", "!"),
                            (" question mark", "?"),
                            (" new line", "\n")):
                    said = said.replace(*punct)
                    time = tf.TimeFunction.print_time()
                print(fg.blue, time, said, fg.rs) #should be removed once tested
            except sr.UnknownValueError as ex:
                print("No sound received: " + str(ex))
            except sr.RequestError as ex:
                print(f"The Google speech recognition API was unreachable; {format(ex)}")
            return said

    @staticmethod
    def log_command(text):
        '''logs the commands'''
        c = cl.CommandLog()
        c.add_command(text)
        del c


    @classmethod
    def interpret(cls, text):
        '''the intents engine neuralintents died - this is the result'''

        # What happens if you use two "code words" in the same sentence??
        # "Multiple if's means your code would go and check all the if conditions,
        # where as in case of elif, if one if condition satisfies
        # it would not check other conditions.."

        #remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        SpeechIn.log_command(text)

        status_strings = ["how are you",
                            "are you ok"]
        for phrase in status_strings:
            if phrase in text:
                s = st.Status()
                s.give_status()

        time_strings = ["what is the time",
                            "current time",
                            "time is it"]
        for phrase in time_strings:
            if phrase in text:
                tf.TimeFunction.tell_time()

        date_strings = ["what is today's date",
                            "what day is it",
                            "current date",
                            "the date"]
        for phrase in date_strings:
            if phrase in text:
                tf.TimeFunction.tell_date()

        alarm_strings = ["set an alarm",
                            "wake me up",
                            "wake up"]
        for phrase in alarm_strings:
            if phrase in text:
                tf.TimeFunction.alarm_clock()

        exit_strings = ["exit",
                            "end the program",
                            "I'd like to go",
                            "goodbye",
                            "good bye",
                            "bye bye",
                            "see you later"]
        for phrase in exit_strings:
            if phrase in text:
                sf.SystemFunction.exitapp()

        shutdown_strings = ["turn off",
                            "shut down"]
        for phrase in shutdown_strings:
            if phrase in text:
                sf.SystemFunction.shutdown()

        joke_strings = ["tell me a joke",
                            "something funny",
                            "make me laugh"]
        for phrase in joke_strings:
            if phrase in text:
                joke = sa.Joke()
                joke.get_joke()

        quote_strings = ["inspire me",
                            "give me a quote",
                            "something inspiring",
                            "inspirational"]
        for phrase in quote_strings:
            if phrase in text:
                quote = sa.Quote()
                quote.get_quote()

        show_todo_strings = ["show me my todo",
                            "show my todo",
                            "show the todo"]
        for phrase in show_todo_strings:
            if phrase in text:
                t = todo.Todo()
                t.show_todo_list()

        add_todo_strings = ["add an item",
                            "add a todo",
                            "add another item",
                            "add to my todo",
                            "add to the todo"]
        for phrase in add_todo_strings:
            if phrase in text:
                t = todo.Todo()
                t.add_todo()

        delete_todo_strings = ["delete an item",
                            "delete from the todo",
                            "delete from my todo",
                            "delete something from"]
        for phrase in delete_todo_strings:
            if phrase in text:
                t = todo.Todo()
                t.delete_todo()

        timer_strings = ["start a timer",
                        "start the time",
                        "start timing",
                        "set a timer",
                        "set the timer"]
        for phrase in timer_strings:
            if phrase in text:
                tf.TimeFunction.set_timer()

        pomodoro_start_strings = ["start the pomodoro",
                            "begin a pomodoro",
                            "start pomodoro"]
        for phrase in pomodoro_start_strings:
            if phrase in text:
                tf.TimeFunction.run_pomodoro()

        pomodoro_stop_strings = ["stop the pomodoro",
                            "stop pomodoro"]
        for phrase in pomodoro_stop_strings:
            if phrase in text:
                tf.TimeFunction.stop_pomodoro()

        wikipedia_strings = ["search wikipedia",
                            "search on wikipedia"
                            "query wikipedia"]
        for phrase in wikipedia_strings:
            if phrase in text:
                w = wp.SearchWikipedia()
                w.wikisearch()

        translate_strings = ["translate something",
                            "to translate",
                            "a translation",
                            "google translate"]
        for phrase in translate_strings:
            if phrase in text:
                t = tr.Translate()
                t.get_source()

        wolfram_strings = ["a question",
                            "wolfram",
                            "ask something"]
        for phrase in wolfram_strings:
            if phrase in text:
                w = wa.SearchWolfram()
                w.wolfsearch()

        email_strings = ["send an email",
                            "send a message",
                            "write a mail",
                            "write an email",
                            "write a message"]
        for phrase in email_strings:
            if phrase in text:
                e = em.Email()
                mail = cls(mail)
                e.get_mail_input(mail)

        add_contact_strings = ["add a contact",
                            "a new contact"]
        for phrase in add_contact_strings:
            if phrase in text:
                c = ct.Contact()
                c.add_contact()

        delete_contact_strings = ["delete a contact",
                            "delete contact",
                            "remove a contact",
                            "remove contact",
                            "get rid of a contact"]
        for phrase in delete_contact_strings:
            if phrase in text:
                c = ct.Contact()
                c.delete_contact()

        show_all_contacts_strings = ["my contacts",
                            "all contacts"]
        for phrase in show_all_contacts_strings:
            if phrase in text:
                c = ct.Contact()
                c.show_all_contacts()

        help_strings = ["need some help",
                            "need help",
                            "what can I say"
                            "what can you do"]
        for phrase in help_strings:
            if phrase in text:
                hl.Help()
