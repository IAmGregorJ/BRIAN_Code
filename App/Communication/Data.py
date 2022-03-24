'''imports'''
import sqlite3
import random

# connection = sqlite3.connect("App/Ressources/BRIAN.db")

# #test to see if the connection is working

# cursor = connection.cursor()
# random = random.randint(1, 670)
# cursor.execute("SELECT text FROM jokes WHERE id = ?",(random,),)
# joke = cursor.fetchone()[0]
# print(joke)
# connection.close()
# # jokes max index = 670
# # quotes max index = 369

class DbController:
    '''class defining the connection and cursor'''
    def __init__(self):
        self.db = sqlite3.connect("App/Ressources/BRIAN.db")
        self.cursor = self.db.cursor()

    def close(self):
        '''closing the connection'''
        self.cursor.close()

class SayingController(DbController):
    '''controller to get saying from the db'''
    m = None
    table = None
    def get_saying(self, table, m):
        '''the actual controller'''
        rand = random.randint(1, m)
        sql = "SELECT text FROM ? WHERE id = ?", (table, rand)
        self.cursor.execute(sql)
        saying = self.cursor.fetchone()[0]
        self.close()
        return saying
        