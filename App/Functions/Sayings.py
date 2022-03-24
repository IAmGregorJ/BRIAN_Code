'''imports'''
from Communication.Data import SayingController as db
import Communication.Output as out

class Saying:
    '''parent'''
    def __init__(self):
        pass
    def get_saying(self, table, m):
        '''get the saying from db'''
        s = db()
        saying = s.get_saying(table, m)
        x = out.Output()
        x.say(saying)


class Joke(Saying):
    '''tell me a joke'''
    def get_joke(self):
        '''get the joke from db'''
        self.get_saying("jokes", 670)

class Quote(Saying):
    '''tell me a joke'''
    def get_quote(self):
        '''get the joke from db'''
        self.get_saying("quotes", 369)
