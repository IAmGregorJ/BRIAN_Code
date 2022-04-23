'''imports'''
import datetime
import os
import re
import shutil
import sys
from pathlib import Path
import Communication.Output as out
import Communication.SpeechIn as ind
from Communication.DbController import UserInfoController as db
from passlib.hash import argon2


class User():
    '''Functions related to the user'''
    def __init__(self):
        self.s = db()
        self.name = ""
        self.passphrase = ""
        self.is_logged_in = False
        self.mail = ""

    def check_user(self):
        '''to see if a user exists'''
        table = "user"
        number = self.s.count(table)
        return number

    def get_user(self):
        '''to get the user object from the db'''
        table = "user"
        data = self.s.get(table)
        return data

    def create_user(self):
        '''create a user if needed'''
        name = self.get_new_username()
        __passphrase = self.get_new_passphrase()
        mail = self.get_new_email()
        hashed_passphrase = argon2.using(rounds=4).hash(__passphrase)
        self.s.add("user", name, hashed_passphrase, mail)
        out.Output.say("Now you're all set up. Just tell me the passphrase next time I ask you.")
        return name, mail

    def verify_user(self):
        '''verify the user's passphrase'''
        data = self.get_user()
        (name, __passphrase, mail) = data
        d_day = datetime.date(2022,6,14)
        self.greet(name)
        out.Output.say("Can you please tell me your passphrase before we get started?")
        while True:
            __passinput = ind.SpeechIn.listen()
            out.Output.say(f"You said {__passinput}, is that correct?")
            verify = ind.SpeechIn.listen()
            affirmative = ["yes", "yeah", "yep"]
            for phrase in affirmative:
                if phrase in verify:
                    if argon2.verify(__passinput, __passphrase):
                        if datetime.date.today() == d_day:
                            out.Output.say(f"Welcome {name}. "
                                            "Today's session is sponsored by the number 12.")
                        else:
                            out.Output.say(f"I'm so glad you've joined me {name}. "
                                            "Just let me know if you need anything.")
                        return name, mail
                    out.Output.say("I'm sorry, that was not the correct passphrase. "
                            "Try again some other time.")
                    sys.exit()
            out.Output.say("Go ahead and try again.")

    def greet(self, username):
        '''greet the user differently depending on when'''
        now = datetime.datetime.now()
        if now < now.replace(hour=8, minute=00):
            out.Output.say(f"Good morning {username}!")
        elif now < now.replace(hour=12, minute=00):
            out.Output.say(f"Hi {username}")
        elif now < now.replace(hour=17, minute=00):
            out.Output.say(f"Good afternoon {username}.")
        else:
            out.Output.say(f"Good evening {username}.")


    def get_new_username(self):
        '''collect the new user's name'''
        out.Output.say("Hey, a new friend! What's your name?")
        while True:
            name = ind.SpeechIn.dictate()
            out.Output.say(f"You said your name is {name}, did I get that right?")
            verify = ind.SpeechIn.listen()
            affirmative = ["yes", "yeah", "yep", "you did"]
            for phrase in affirmative:
                if phrase in verify:
                    out.Output.say(f"Nice to meet you {name}")
                    return name
            out.Output.say("So try again and I'll see if I can understand you better.")

    def get_new_passphrase(self):
        '''collect the new user's passphrase'''
        out.Output.say("Now we have to make a passphrase. "
                        "Give me four random words that you will remember.")
        while True:
            __pphrase = ind.SpeechIn.listen()
            while len(__pphrase.split()) != 4:
                out.Output.say("I'm sorry, we wanted four words, right? Try again.")
                __pphrase = ind.SpeechIn.listen()
            out.Output.say(f"You said {__pphrase}, is that right?")
            verify = ind.SpeechIn.listen()
            affirmative = ["yes", "yeah", "yep", "you did"]
            for phrase in affirmative:
                if phrase in verify:
                    return __pphrase

    def get_new_email(self):
        '''collect the new user's passphrase'''
        out.Output.say("Ok, I need your email address. "
                        "Don't worry, I won't be sharing it with anyone. \n"
                        "Please type it in the console so that I get it correct the first time.")
        email = input("> ")
        self.get_smtp_info()
        return email

    def get_smtp_info(self):
        '''collect smtp credentials'''
        out.Output.say("Please write the address to your smtp server.")
        smtp = input("> ")
        out.Output.say("Which port number does your smtp server use?")
        port = input("> ")
        out.Output.say("Now I need your smtp username.")
        username = input("> ")
        out.Output.say("And finally, please type your smtp password.")
        passwd = input("> ")
        self.write_smtp_info(smtp, port, username, passwd)

    def write_smtp_info(self, smtp, port, username, passwd):
        '''write smtp credentials'''
        tf = open('tmp', 'a+') #pylint:disable=unspecified-encoding
        f = Path(__file__).resolve().parents[1]
        f= f / 'secrets.ini'

        with open(f) as x: #pylint:disable=unspecified-encoding
            for line in x.readlines():
                line = re.sub('smtp_server=.*', 'smtp_server='+smtp, line)
                line = re.sub('smtp_port=.*', 'smtp_port='+port, line)
                line = re.sub('smtp_user.*', 'smtp_user='+username, line)
                line = re.sub('smtp_pass.*', 'smtp_pass='+passwd, line)
                tf.write(line)
        tf.close()
        x.close()
        shutil.copy('tmp', f)
        os.remove('tmp')
