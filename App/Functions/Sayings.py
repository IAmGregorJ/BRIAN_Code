'''imports'''
from Communication.DbController import SayingController as db
import Communication.Output as out

class Saying:
    '''parent'''
    def __init__(self):
        '''parent constructor'''
        self.s = db()
    def get_saying(self, table, m):
        '''get the saying from db'''
        saying = self.s.get(table, m)
        self.s.close()
        return saying

class Joke(Saying):
    '''tell me a joke'''
    def __init__(self):
        '''child constructor'''
        Saying.__init__(self)
        table = "jokes"
        m = 670
        self.joke = self.get_saying(table, m)
    def get_joke(self):
        '''get the joke from db'''
        out.Output.say(self.joke)
        del self.s

class Quote(Saying):
    '''tell me a joke'''
    def __init__(self):
        '''child constructor'''
        Saying.__init__(self)
        table = "quotes"
        m = 369
        self.quote = self.get_saying(table, m)
    def get_quote(self):
        '''get the joke from db'''
        out.Output.say(self.quote)
        del self.s
