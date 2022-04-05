'''imports'''
from Communication.Data import TodoController as db
import Communication.Output as out
import Communication.SpeechIn as ind

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
    def speak(self, message):
        '''output'''
        x = out.Output()
        x.say(message)
        del x
    def get_input(self):
        '''get input from user'''
        i = ind.SpeechIn()
        message = i.dictate()
        del i
        return message
    def show_todo_list(self):
        '''display todo list'''
        todo_list = self.get_todo_list()
        if todo_list == 0:
            self.speak("There is nothing on your todo list.")
        else:
            for item in todo_list:
                self.speak(str(item[0]) + ". " + item[1])
    def add_todo(self):
        '''add todo to list'''
        text = self.input_todo_text()
        self.s.add(self.table, text)
        self.show_todo_list()
    def delete_todo(self):
        '''delete todo from list'''
        number = self.input_todo_number()
        try:
            int(number)
        except ValueError:
            self.speak("You had one chance. Boom.")
            return
        self.s.delete(self.table, int(number))
        self.show_todo_list()
    def input_todo_text(self):
        '''get input related to the todo item'''
        self.speak("What would you like to add to the list?")
        todo_text = self.get_input()
        return todo_text
    def input_todo_number(self):
        '''get input related to the line number to delete'''
        self.speak("What is the number of the item you want removed?")
        number = self.get_input()
        return number