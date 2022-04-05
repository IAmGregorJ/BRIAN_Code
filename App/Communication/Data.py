'''imports'''
import sqlite3
import random
import datetime

# pylint: disable=consider-using-f-string
class DbController:
    '''class defining the connection and cursor'''
    def __init__(self):
        self.db = sqlite3.connect("App/Ressources/BRIAN.db")
        self.cursor = self.db.cursor()
    def close(self):
        '''closing the connection'''
        self.cursor.close()

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
    def get(self, table, m):
        '''the actual controller'''
        rand = random.randint(1, m)
        self.cursor.execute("SELECT text FROM {} WHERE id = ?".format(table), (rand,))
        saying = self.cursor.fetchone()[0]
        return saying

class TodoController(DbController):
    '''controller to CRUD todo list'''
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