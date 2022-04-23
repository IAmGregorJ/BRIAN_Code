'''imports'''
from Communication import Output as out

class Help():
    '''The help "object"'''
    def __init__(self) -> None:
        self.time_string = ["Get the current time or date",
                            "Set an alarm",
                            "Set a kitchen timer",
                            "Start or stop a pomodoro timer"]
        self.todo_string = ["Add items to your to-do list",
                            "Delete items from your to-do list",
                            "See your entire to-do list"]
        self.sayings_string = ["I can tell you a joke",
                            "I can also give you an inspirational quote"]
        self.questions_string = ["Search for information in Wikipedia",
                            "Ask me any question"]
        self.translate_string = ["Translate phrases from English to several different languages"]
        self.shutdown_string = ["Close this program",
                            "Shut down your computer"]
        self.contacts_string = ["Add people to your contacts list",
                            "Delete people from your contacts list",
                            "Modify a contact",
                            "See all your contacts"]
        self.status_string = ["Ask me how I'm feeling"]

    def give_help(self):
        '''the actual help function'''
        out.Output.say("There are many things you can ask me.")
        out.Output.say("For example, you can use several timer functions, such as:")
        for i in self.time_string:
            out.Output.say(f"\t{i}")
        out.Output.say("You can also manage your to-do list:")
        for i in self.todo_string:
            out.Output.say(f"\t{i}")
        out.Output.say("You can manage a contact list:")
        for i in self.contacts_string:
            out.Output.say(f"\t{i}")
        out.Output.say("And you can also send an email to anyone on your contact list.")
        out.Output.say("There are also many other things you can do, like:")
        for i in self.sayings_string:
            out.Output.say(f"\t{i}")
        for i in self.questions_string:
            out.Output.say(f"\t{i}")
        for i in self.translate_string:
            out.Output.say(f"\t{i}")
        for i in self.shutdown_string:
            out.Output.say(f"\t{i}")
        out.Output.say("And finally, you can also just ask me how I'm feeling.")
