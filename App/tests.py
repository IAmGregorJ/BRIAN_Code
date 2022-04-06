'''imports'''
import sqlite3
import unittest

from Communication.DbController import SayingController, TodoController

class TestDatabase(unittest.TestCase):
    '''test the temp database'''

    def setUp(self):
        '''setting up the temp database'''
        conn = sqlite3.connect("App/Ressources/BRIAN.db")
        cursor = conn.cursor()

        #create a table
        cursor.execute("""CREATE TABLE testjokes
                          (id integer, text text)""")
        conn.commit()
        cursor.execute("""CREATE TABLE testtodos
                            (
                                "todo"	TEXT NOT NULL,
                                "added"	INTEGER NOT NULL,
                                "id"	INTEGER NOT NULL,
                                PRIMARY KEY("id" AUTOINCREMENT)
                            );""")
        conn.commit()
        haha = [(1, 'First joke'),
                  (2, 'Second joke'),
                  (3, 'Third joke'),
                  (4, 'Fourth joke')]
        stuff = [('Something', 20200326153202),
                  ('Something else', 20220327091225),
                  ('Third thing', 20220327120014),
                  ('4th thing', 20220327124545)]
        cursor.executemany("INSERT INTO testjokes VALUES (?,?)",
                           haha)
        conn.commit()
        cursor.executemany("INSERT INTO testtodos (todo, added) VALUES (?,?)",
                           stuff)
        conn.commit()

    def tearDown(self):
        '''drop the temp tables'''
        conn = sqlite3.connect("App/Ressources/BRIAN.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE testjokes")
        conn.commit()
        cursor.execute("DROP TABLE testtodos")
        conn.commit()
        conn.close()

    def test_get_joke(self):
        '''testing getting a joke'''
        #passing max and table variable so that
        #method can be reused for quotes
        table = "testjokes"
        m = 4
        s = SayingController()
        saying = s.get(table, m)
        self.assertTrue(isinstance(saying ,str))
        del s

    def test_get_todos(self):
        '''testing getting todo list'''
        table = "testtodos"
        t = TodoController()
        todo_list = t.get(table)
        self.assertTrue(isinstance(todo_list, list))
        del t

    def test_add_todo(self):
        '''testing adding to todo list'''
        table = "testtodos"
        t = TodoController()
        new_item = "Go shopping"
        t.add(table, new_item)
        self.assertTrue(len(t.get(table)), 5)
        del t

    def test_delete_todo(self):
        '''testing deleting something from todo list'''
        table = "testtodos"
        t = TodoController()
        number = 5
        t.delete(table, number)
        self.assertTrue(len(t.get(table)), 4)
        del t

if __name__ == '__main__':
    unittest.main()
