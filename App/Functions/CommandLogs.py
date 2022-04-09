'''imports'''
from Communication.DbController import CommandLogController as db

class CommandLog:
    '''CommandLog object'''
    def __init__(self) -> None:
        '''constructor'''
        self.s = db()
        self.table = "command_log"
        self.columns = "(command, time)"
    def get_command_list(self):
        '''get the list from the db'''
        command_list = self.s.get(self.table)
        self.s.close()
        return command_list
    def add_command(self, comm):
        '''add todo to list'''
        self.s.add(self.table, comm)
        