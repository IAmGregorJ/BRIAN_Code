'''imports'''
import sqlite3
import unittest

from Communication.DbController import (
    CommandLogController,
    SayingController,
    TodoController,
    UserInfoController
)

# THESE MIGHT NOT BE RUN IN ORDER - THEY NEED TO BE INDEPENDENT OF ONE ANOTHER
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
        cursor.execute("""CREATE TABLE testcommand_log
                            (command text, time real)""")
        conn.commit()
        cursor.execute("""CREATE TABLE testuser_empty
                            (name text, passphrase text)""")
        conn.commit()
        cursor.execute("""CREATE TABLE testuser_populated
                            (name text, passphrase text)""")
        haha = [(1, 'First joke'),
                  (2, 'Second joke'),
                  (3, 'Third joke'),
                  (4, 'Fourth joke')]
        stuff = [('Something', 20200326153202),
                  ('Something else', 20220327091225),
                  ('Third thing', 20220327120014),
                  ('4th thing', 20220327124545)]
        commands = [('First command', 20200326153202),
                  ('Second command', 20220327091225),
                  ('Third command', 20220327120014),
                  ('4th command', 20220327124545)]
        user = [('tomato', 'paste')]
        cursor.executemany("INSERT INTO testjokes VALUES (?,?)",
                           haha)
        conn.commit()
        cursor.executemany("INSERT INTO testtodos (todo, added) VALUES (?,?)",
                           stuff)
        conn.commit()
        cursor.executemany("INSERT INTO testcommand_log (command, time) VALUES (?,?)", commands)
        conn.commit()
        cursor.executemany("INSERT INTO testuser_populated (name, passphrase) VALUES (?, ?)", user)

    def tearDown(self):
        '''drop the temp tables'''
        conn = sqlite3.connect("App/Ressources/BRIAN.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE testjokes")
        conn.commit()
        cursor.execute("DROP TABLE testtodos")
        conn.commit()
        cursor.execute("DROP TABLE testcommand_log")
        conn.commit()
        cursor.execute("DROP TABLE testuser_empty")
        conn.commit()
        cursor.execute("DROP TABLE testuser_populated")
        conn.commit()
        conn.close()

    def test_get_joke(self):
        '''testing getting a joke'''
        haha = ('First joke',
                  2, 'Second joke',
                  3, 'Third joke',
                  4, 'Fourth joke')
        #passing max and table variable so that
        #method can be reused for quotes
        table = "testjokes"
        m = 4
        s = SayingController()
        saying = s.get(table, m)
        # check if the random saying is in the list
        self.assertTrue(saying in haha)
        del s

    def test_get_todos(self):
        '''testing getting todo list'''
        stuff = ('Something',
                  'Something else',
                  'Third thing',
                  '4th thing')
        table = "testtodos"
        t = TodoController()
        todo_list = t.get(table)
        #check if all elements of stuff is in to_do_list
        self.assertTrue(all(elem in dict(todo_list).values() for elem in stuff))
        del t

    def test_add_todo(self):
        '''testing adding to todo list'''
        table = "testtodos"
        t = TodoController()
        number = len(t.get(table))
        new_item = "Go shopping"
        t.add(table, new_item)
        self.assertTrue(len(t.get(table)), number + 1)
        del t

    def test_delete_todo(self):
        '''testing deleting something from todo list'''
        table = "testtodos"
        t = TodoController()
        number = len(t.get(table))
        t.delete(table, number)
        self.assertTrue(len(t.get(table)), number - 1)
        del t

    def test_add_command(self):
        '''testing adding to command log'''
        table = "testcommand_log"
        t = CommandLogController()
        number = len(t.get(table))
        new_command = "Fifth command"
        t.add(table, new_command)
        self.assertTrue(len(t.get(table)), number + 1)
        del t

    def test_count_user(self):
        '''testing to see that user count works'''
        table = "testuser_empty"
        t = UserInfoController()
        number = t.count(table)
        self.assertTrue(number == 0)
        del t

    def test_add_user(self):
        '''testing to see that adding a user works'''
        table = "testuser_empty"
        t = UserInfoController()
        number = t.count(table)
        name = "rando"
        passhash = "anotherrando"
        t.add(table, name, passhash)
        self.assertTrue(t.count(table) == number + 1)
        del t

    def test_get_user(self):
        '''testing to see that getting a user works'''
        table = "testuser_populated"
        t = UserInfoController()
        name, passphrase = t.get(table)
        self.assertTrue(name == "tomato" & passphrase == "paste")

if __name__ == '__main__':
    unittest.main()
