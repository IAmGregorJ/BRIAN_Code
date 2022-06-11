'''imports'''
import os
import sys
from datetime import datetime
import Communication.Output as out
import Communication.SpeechIn as ind

class SystemFunction:
    '''system functions'''
    def __init__(self) -> None:
        pass

    @staticmethod
    def exitapp(name):
        '''exit the app'''
        d_day = datetime(2022,6,14)
        if datetime.today().date() == d_day.date():
            message = f"Super, {name}. Good luck, I hope you get a 12!"
        else:
            message = f"I hope do see you again soon {name}"
        out.Output.say(message)
        sys.exit()

    @staticmethod
    def shutdown():
        '''shut down the computer'''
        message = "Are you sure you want to shut down the computer?"
        out.Output.say(message)
        answer = ind.SpeechIn.listen()
        if answer == "yes":
            os.system("shutdown /s /t 1")
        else:
            out.Output.say("Ok, we'll stay right where we are then")

    @staticmethod
    def restart():
        '''restart the computer'''
        message = "Are you sure you want to restart the computer?"
        out.Output.say(message)
        answer = ind.SpeechIn.listen()
        if answer == "yes":
            os.system("shutdown /r /t 1")
        else:
            out.Output.say("Ok, we'll wait with that then")
            