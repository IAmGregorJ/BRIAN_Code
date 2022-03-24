'''imports'''
import sys
import Communication.Output as out

class SystemFunction:
    '''system functions'''
    def __init__(self) -> None:
        pass

    @staticmethod
    def exitapp():
        '''exit the app'''
        t = out.Output()
        t.say("I hope to see you again soon!")
        del t
        sys.exit()

    @staticmethod
    def shutdown():
        '''shut down the computer'''
        pass
