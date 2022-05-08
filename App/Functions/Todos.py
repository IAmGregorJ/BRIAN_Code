'''imports'''
from Communication.DbController import TodoController as db
import Communication.Output as out
import Communication.SpeechIn as ind
from base_logger import logger

class Todo:
    '''Todo object'''
    def __init__(self) -> None:
        '''constructor'''
        self.s = db()
        self.table = "todos"
        self.columns = "(todo, added)"

    def get_todo_list(self):
        '''get the list from the db'''
        todo_list = self.s.get(self.table)
        self.s.close()
        return todo_list

    def show_todo_list(self):
        '''display todo list'''
        todo_list = self.get_todo_list()
        if todo_list == 0:
            out.Output.say("There is nothing on your todo list.")
        else:
            for item in todo_list:
                out.Output.say(str(item[0]) + ". " + item[1])
        self.s.close()

    def add_todo(self):
        '''add todo to list'''
        text = self.input_todo_text()
        self.s.add(self.table, text)
        self.show_todo_list()

    def delete_todo(self):
        '''delete todo from list'''
        number = ind.SpeechIn.listen()
        try:
            int(number)
        except ValueError as ex:
            logger.error(repr(ex))
            out.Output.say("You had one chance. Boom.")
            return
        self.s.delete(self.table, int(number))
        self.show_todo_list()

    def input_todo_text(self):
        '''get input related to the todo item'''
        out.Output.say("What would you like to add to the list?")
        todo_text = ind.SpeechIn.dictate()
        return todo_text
        
    def input_todo_number(self):
        '''get input related to the line number to delete'''
        out.Output.say("What is the number of the item you want removed?")
        number = ind.SpeechIn.listen()
        return number
