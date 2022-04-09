'''imports'''
import os
import sys
import Communication.Output as out
import Communication.SpeechIn as ind

class SystemFunction:
    '''system functions'''
    def __init__(self) -> None:
        pass

    @staticmethod
    def exitapp():
        '''exit the app'''
        message = "I hope do see you again soon"
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
            