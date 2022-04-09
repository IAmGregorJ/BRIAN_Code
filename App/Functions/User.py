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
        self.name = ""
        self.passphrase = ""
        self.is_logged_in = False

    def check_user(self):
        '''to see if a user exists'''
        table = "user"
        s = db()
        number = s.count(table)
        del s
        return number

    def get_user(self):
        '''to get the user object from the db'''
        table = "user"
        s = db()
        data = s.get(table)
        return data

    def create_user(self):
        '''create a user if needed'''
        out.Output.say("Hey, a new friend! What's your name?")
        name = self.get_new_username()
        out.Output.say("Now we have to make a passphrase. "
                        "Give me four random words that you will remember")
        passphrase = self.get_new_passphrase()
        hashed_passphrase = argon2.using(rounds=4).hash(passphrase)
        s = db()
        s.add("user", name, hashed_passphrase)
        out.Output.say("Now you're all set up. Just tell me the passphrase next time I ask you.")

    def verify_user(self):
        '''verify the user's passphrase'''
        data = self.get_user()
        for item in data:
            name = item[0]
            passphrase = item[1]
        self.hello(name)
        out.Output.say("Can you plase tell me your passphase before we get started?")
        while True:
            passinput = ind.SpeechIn.listen()
            out.Output.say(f"You said {passinput}, is that correct?")
            verify = ind.SpeechIn.listen()
            affirmative = ["yes", "yeah", "yep"]
            for phrase in affirmative:
                if phrase in verify:
                    if argon2.verify(passinput, passphrase):
                        out.Output.say(f"I'm so glad you've joined me {name}. "
                                        "Just let me know if you need anything.")
                        return name
                out.Output.say("I'm sorry, that was not the correct passphrase. "
                                "Try again some other time.")
                sys.exit()

    def hello(self, user):
        '''greet the user differently depending on when'''
        now = datetime.datetime.now()
        if now < now.replace(hour=8, minute=00):
            out.Output.say(f"Good morning {user}!")
        elif now < now.replace(hour=12, minute=00):
            out.Output.say(f"Hello {user}")
        elif now < now.replace(hour=17, minute=00):
            out.Output.say(f"Good afternoon {user}.")
        else:
            out.Output.say(f"Good evening {user}.")


    def get_new_username(self):
        '''collect the new user's name'''
        while True:
            name = ind.SpeechIn.listen()
            out.Output.say(f"You said your name is {name}, did I get that right?")
            verify = ind.SpeechIn.listen()
            affirmative = ["yes", "yeah", "yep", "you did"]
            for phrase in affirmative:
                if phrase in verify:
                    out.Output.say(f"Nice to meet you {name}")
                    return name

    def get_new_passphrase(self):
        '''collect the new user's passphrase'''
        while True:
            passphrase = ""
            while len(passphrase.split()) != 4:
                passphrase = ind.SpeechIn.listen()
                out.Output.say("I'm sorry, we wanted four words, right? Try again.")
            out.Output.say(f"You said {passphrase}, is that right?")
            verify = ind.SpeechIn.listen()
            affirmative = ["yes", "yeah", "yep", "you did"]
            for phrase in affirmative:
                if phrase in verify:
                    out.Output.say("Awesome, your passphrase is all set up.")
                    return passphrase
