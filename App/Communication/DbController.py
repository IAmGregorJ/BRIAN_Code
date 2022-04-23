'''imports'''
import sqlite3
import random
import datetime
from abc import ABC, abstractmethod

# pylint: disable=consider-using-f-string
class DbController(ABC):
    '''class defining the connection and cursor'''
    def __init__(self):
        self.db = sqlite3.connect("App/Ressources/BRIAN.db")
        self.cursor = self.db.cursor()

    def close(self):
        '''closing the connection'''
        self.cursor.close()

    @abstractmethod
    def get(self):
        '''get method'''
    @abstractmethod
    def add(self):
        '''add method'''
    @abstractmethod
    def delete(self):
        '''delete method'''

# class DbController:
#     '''class defining the connection and cursor'''
#     __instance__ = None

#     def __init__(self):
#         '''Constructor'''
#         if DbController.__instance__ is None:
#             DbController.__instance__ = self
#             self.db = sqlite3.connect("App/Ressources/BRIAN.db")
#             self.cursor = self.db.cursor()
#         else:
#             raise Exception("You cannot create another DbController class")
#     def close(self):
#         '''closing the connection'''
#         self.cursor.close()
#     @staticmethod
#     def get_instance():
#         ''' Static method to fetch the current instance. '''
#         if not DbController.__instance__:
#             DbController()
#             return DbController.__instance__

class SayingController(DbController):
    '''controller to get saying from the db'''
    #pylint: disable=arguments-differ
    def get(self, table, m):
        '''the actual controller'''
        rand = random.randint(1, m)
        self.cursor.execute("SELECT text FROM {} WHERE id = ?".format(table), (rand,))
        saying = self.cursor.fetchone()[0]
        return saying
    def add(self):
        '''add method'''
    def delete(self):
        '''delete method'''


class TodoController(DbController):
    '''controller to CRUD todo list'''
    #pylint: disable=arguments-differ
    def get(self, table):
        '''get todo list from db'''
        self.cursor.execute("""SELECT id, todo FROM {}""".format(table))
        try:
            data = self.cursor.fetchall()
        except TypeError:
            return 0
        return data

    def add(self, table, text):
        '''add todo to db'''
        # current date formatted: int(current_date.strftime("%Y%m%d%H%M%S")
        added = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.cursor.execute("INSERT INTO {} (todo, added) VALUES (?, ?)".format(table),
                           (text, added))
        self.db.commit()

    def delete(self, table, row_number):
        '''delete todo from db'''
        self.cursor.execute("DELETE FROM {} WHERE id = ?;".format(table), (row_number,))
        self.db.commit()
        new_row = row_number - 1
        self.cursor.execute("SELECT COUNT(*) FROM {}".format(table))
        m = self.cursor.fetchone()[0]
        if new_row < m:
            self.cursor.execute("""update todos
                                    set id = (id - 1)
                                    where id > ?""", (new_row,))
        self.db.commit()
        self.cursor.execute("delete from sqlite_sequence where name='{}';".format(table))
        self.db.commit()

class CommandLogController(DbController):
    '''controller to log all commands to the db'''
    #pylint: disable=arguments-differ
    def get(self, table):
        '''get method'''
        self.cursor.execute("""SELECT command, time FROM {}""".format(table))
        try:
            data = self.cursor.fetchall()
        except TypeError:
            return 0
        return data
    def add(self, table, comm):
        '''add method'''
        added = datetime.datetime.now()
        self.cursor.execute("INSERT INTO {} (command, time) VALUES (?, ?)".format(table),
                            (comm, added))
        self.db.commit()
    def delete(self):
        '''delete method'''

class UserInfoController(DbController):
    '''controller to register and verify the user'''
    #pylint: disable=arguments-differ
    def count(self, table):
        '''count to see if there is a user'''
        self.cursor.execute("""SELECT COUNT(*) from {}""".format(table))
        count = self.cursor.fetchone()[0]
        return count
    def get(self, table):
        '''get method'''
        cursor = self.cursor
        cursor.execute("""SELECT name, passphrase, email from {}""".format(table))
        data = self.cursor.fetchone()
        return data

    def add(self, table, name, val, mail):
        '''add method'''
        self.cursor.execute("INSERT INTO {} (name, passphrase, email)"
                            " VALUES (?, ?, ?)".format(table), (name, val, mail))
        self.db.commit()

    def delete(self):
        '''delete method'''

class ContactsInfoController(DbController):
    '''controller to register and get contacts to sent emails to'''
    #pylint: disable=arguments-differ
    def count(self,table):
        '''count to see how many contacts there are'''
        self.cursor.execute("""SELECT COUNT(*) from {}""".format(table))
        count = self.cursor.fetchone()[0]
        return count

    def get_all(self, table):
        '''get contact list from db'''
        self.cursor.execute("""SELECT name, email FROM {}""".format(table))
        try:
            data = self.cursor.fetchall()
        except TypeError:
            return 0
        return data

    def get(self, table, name):
        '''get method'''
        cursor = self.cursor
        cursor.execute("""SELECT email from {} WHERE name = ?""".format(table), (name,))
        contact_mail = self.cursor.fetchone()[0]
        return contact_mail

    def add(self, table, name, mail):
        '''add method'''
        self.cursor.execute("INSERT INTO {} (name, email)"
                            " VALUES (?, ?)".format(table), (name, mail))
        self.db.commit()

    def delete(self, table, name):
        '''delete method'''
        self.cursor.execute("DELETE FROM {} WHERE name = ?".format(table), (name,))
        self.db.commit()

    def modify(self, table, mail, name):
        '''modify method'''
        self.cursor.execute("UPDATE {} SET email = ? WHERE name = ?".format(table), (mail, name))
        self.db.commit()
        