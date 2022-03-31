'''imports'''
import os
import sys
import Communication.Output as out
import Communication.SpeechIn as ind

class SystemFunction:
    '''system functions'''
    def __init__(self) -> None:
        pass
    def say(self, message):
        '''output message'''
        t = out.Output()
        t.say(message)
        del t
    def hear(self):
        '''hear secondary input'''
        i = ind.SpeechIn()
        text = i.listen()
        del i
        return text
    # @staticmethod doesn't work here because
    # I need to call the say() method
    # and a static method wouldn't have access
    # even though I HATE having to create an object for this
    def exitapp(self):
        '''exit the app'''
        message = "I hope do see you again soon"
        self.say(message)
        sys.exit()

    # see comment about @staticmethod here
    def shutdown(self):
        '''shut down the computer'''
        message = "Are you sure you want to shut down the computer?"
        self.say(message)
        answer = self.hear()
        if answer == "yes":
            os.system("shutdown /s /t 1")
        else:
            self.say("Ok, we'll stay right where we are then")
