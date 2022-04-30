'''imports'''
import os
import time
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
    Help as hl,
    User as u
)
from sty import fg

class SpeechIn:
    '''used to listen, hear and speak'''
    def __init__(self) -> None:
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
        filename = ("voice.mp3")
        with sr.Microphone() as source:
            if os.path.exists(filename):
                time.sleep(10)
            recon.adjust_for_ambient_noise(source, duration=0.5)
            audio = recon.listen(source)
            said = ""
            try:
                said = recon.recognize_google(audio)
                tm = tf.TimeFunction.print_time()
                print("")
                print(fg.green, tm, said, fg.rs)
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
                    tm = tf.TimeFunction.print_time()
                print(fg.blue, tm, said, fg.rs) #should be removed once tested
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


    @staticmethod
    def interpret(user, text):
        '''the intents engine neuralintents died - this is the result'''

        #remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        SpeechIn.log_command(text)

        status_strings = ["how are you",
                            "are you ok"]
        time_strings = ["what is the time",
                            "current time",
                            "time is it"]
        date_strings = ["what is today's date",
                            "what day is it",
                            "current date",
                            "the date"]
        alarm_strings = ["set an alarm",
                            "wake me up",
                            "wake up"]
        exit_strings = ["exit",
                            "end the program",
                            "I'd like to go",
                            "goodbye",
                            "good bye",
                            "bye bye",
                            "see you later"]
        shutdown_strings = ["turn off",
                            "shut down"]
        restart_strings = ["restart",
                            "reboot"]
        joke_strings = ["tell me a joke",
                            "something funny",
                            "make me laugh"]
        quote_strings = ["inspire me",
                            "give me a quote",
                            "something inspiring",
                            "inspirational"]
        show_todo_strings = ["show me my todo",
                            "show my todo",
                            "show the todo"]
        add_todo_strings = ["add an item",
                            "add a todo",
                            "add another item",
                            "add to my todo",
                            "add to the todo"]
        delete_todo_strings = ["delete an item",
                            "delete from the todo",
                            "delete from my todo",
                            "delete something from"]
        timer_strings = ["start a timer",
                        "start the time",
                        "start timing",
                        "set a timer",
                        "set the timer"]
        pomodoro_start_strings = ["start the pomodoro",
                            "begin a pomodoro",
                            "start pomodoro"]
        pomodoro_stop_strings = ["stop the pomodoro",
                            "stop pomodoro"]
        wikipedia_strings = ["search wikipedia",
                            "on wikipedia",
                            "query wikipedia"]
        translate_strings = ["to translate",
                            "a translation",
                            "google translate"]
        wolfram_strings = ["a question",
                            "wolfram",
                            "ask something"]
        email_strings = ["send an email",
                            "send a mail",
                            "send a message",
                            "write a mail",
                            "write an email",
                            "write a message"]
        change_email_strings = ["change my email",
                            "change my address",
                            "email address"]
        add_contact_strings = ["add a contact",
                            "a new contact"]
        modify_contact_strings = ["edit a contact",
                            "modify a contact"]
        delete_contact_strings = ["delete a contact",
                            "delete contact",
                            "remove a contact",
                            "remove contact",
                            "get rid of a contact"]
        show_all_contacts_strings = ["my contacts",
                            "all contacts"]
        help_strings = ["need some help",
                            "need help",
                            "what can I say",
                            "what can you do"]

        lists = []
        a = vars().copy()
        for i in a:
            if '_strings' in i:
                lists.append(a[i])

        number = 0

        for lst in (lists):
            for phrase in lst:
                if phrase in text:
                    number += 1
        if number == 0:
            out.Output.say("I'm sorry, I don't understand")

        for phrase in alarm_strings:
            if phrase in text:
                tf.TimeFunction.alarm_clock()

        for phrase in status_strings:
            if phrase in text:
                s = st.Status()
                s.give_status()

        for phrase in time_strings:
            if phrase in text:
                tf.TimeFunction.tell_time()

        for phrase in date_strings:
            if phrase in text:
                tf.TimeFunction.tell_date()

        for phrase in exit_strings:
            if phrase in text:
                sf.SystemFunction.exitapp(user.name)

        for phrase in shutdown_strings:
            if phrase in text:
                sf.SystemFunction.shutdown()

        for phrase in restart_strings:
            if phrase in text:
                sf.SystemFunction.restart()

        for phrase in joke_strings:
            if phrase in text:
                joke = sa.Joke()
                joke.get_joke()

        for phrase in quote_strings:
            if phrase in text:
                quote = sa.Quote()
                quote.get_quote()

        for phrase in show_todo_strings:
            if phrase in text:
                t = todo.Todo()
                t.show_todo_list()

        for phrase in add_todo_strings:
            if phrase in text:
                t = todo.Todo()
                t.add_todo()

        for phrase in delete_todo_strings:
            if phrase in text:
                t = todo.Todo()
                t.delete_todo()

        for phrase in timer_strings:
            if phrase in text:
                tf.TimeFunction.set_timer()

        for phrase in pomodoro_start_strings:
            if phrase in text:
                tf.TimeFunction.run_pomodoro()

        for phrase in pomodoro_stop_strings:
            if phrase in text:
                tf.TimeFunction.stop_pomodoro()

        for phrase in wikipedia_strings:
            if phrase in text:
                w = wp.SearchWikipedia()
                w.wikisearch()

        for phrase in translate_strings:
            if phrase in text:
                t = tr.Translate()
                t.get_source()

        for phrase in wolfram_strings:
            if phrase in text:
                w = wa.SearchWolfram()
                w.wolfsearch()

        for phrase in email_strings:
            if phrase in text:
                e = em.Email()
                e.get_mail_input(user.mail)

        for phrase in change_email_strings:
            if phrase in text:
                e = u.User()
                e.get_new_email()

        for phrase in add_contact_strings:
            if phrase in text:
                c = ct.Contact()
                c.add_contact()

        for phrase in modify_contact_strings:
            if phrase in text:
                c = ct.Contact()
                c.modify_contact()

        for phrase in delete_contact_strings:
            if phrase in text:
                c = ct.Contact()
                c.delete_contact()

        for phrase in show_all_contacts_strings:
            if phrase in text:
                c = ct.Contact()
                c.show_all_contacts()

        for phrase in help_strings:
            if phrase in text:
                h = hl.Help()
                h.give_help()
