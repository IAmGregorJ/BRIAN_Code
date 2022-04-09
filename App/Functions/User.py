'''imports'''
import datetime
import sys
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
        hashed_passphrase = argon2.using(rounds=4).hash(__passphrase)
        self.s.add("user", name, hashed_passphrase)
        out.Output.say("Now you're all set up. Just tell me the passphrase next time I ask you.")
        return name

    def verify_user(self):
        '''verify the user's passphrase'''
        data = self.get_user()
        for item in data:
            name = item[0]
            __passphrase = item[1]
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
                        out.Output.say(f"I'm so glad you've joined me {name}. "
                                        "Just let me know if you need anything.")
                        return name
                out.Output.say("I'm sorry, that was not the correct passphrase. "
                                "Try again some other time.")
                sys.exit()

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
                        "Give me four random words that you will remember")
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
