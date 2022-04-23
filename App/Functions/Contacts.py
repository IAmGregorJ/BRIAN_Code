'''imports'''
import rsa
from Communication.DbController import ContactsInfoController as db
import Communication.Output as out
import Communication.SpeechIn as ind

class Contact():
    '''Class to hold the mail object and the functions'''
    def __init__(self) -> None:
        '''Constructor'''
        self.name = ""
        self.email = ""
        self.s = db()
        with open("App/public_key", "rb") as pbf:
            self.publicKey = rsa.PublicKey.load_pkcs1(pbf.read())
        with open("App/private_key", "rb") as pvf:
            self.privateKey = rsa.PrivateKey.load_pkcs1(pvf.read())

    def get_all_contacts(self):
        '''get the entire contact list'''
        table = "contacts"
        contacts = self.s.get_all(table)
        self.s.close()
        return contacts

    def show_all_contacts(self):
        '''print out the contact list to the console'''
        contacts = self.get_all_contacts()
        if contacts == 0:
            out.Output.say("You have no contacts.")
        else:
            out.Output.say("Here you go.")
            for item in contacts:
                print(str(item[0]) + ": " +
                    rsa.decrypt(item[1], self.privateKey).decode())
        self.s.close()

    def get_contact(self):
        '''get method'''
        table = "contacts"
        while self.email is None or self.email == "":
            out.Output.say("What is the name of the contact?")
            self.name = ind.SpeechIn.listen()
            self.email = self.s.get(table, self.name)
            if self.email is None or self.email =="":
                out.Output.say("I'm sorry, there is no contact by that name."
                                "Try again.")
        self.s.close()
        self.email = rsa.decrypt(self.email, self.privateKey).decode()
        return self.email

    def add_contact(self):
        '''add method'''
        table = "contacts"
        out.Output.say("What is the name of the contact you'd like to add?")
        self.name = ind.SpeechIn.listen()
        out.Output.say("Please type their email address in the window.")
        self.email = input("> ")
        self.email = rsa.encrypt(self.email.encode(), self.publicKey)
        self.s.add(table, self.name, self.email)
        out.Output.say(f"I have added {self.name} to your contacts.")
        self.s.close()
        return self.name

    def delete_contact(self):
        '''delete method'''
        table = "contacts"
        while True:
            out.Output.say("What is the name of the contact you'd like to delete?")
            self.name = ind.SpeechIn.listen()
            out.Output.say(f"You said {self.name}, is that correct?")
            verify = ind.SpeechIn.listen()
            affirmative = ["yes", "yeah", "yep"]
            for phrase in affirmative:
                if phrase in verify:
                    self.s.delete(table, self.name)
                    out.Output.say(f"{self.name} has been deleted.")

    def modify_contact(self):
        '''modify method'''
        table = "contacts"
        while self.email is None or self.email == "":
            out.Output.say("What is the name of the contact who's email you'd like to change?")
            self.name = ind.SpeechIn.listen()
            self.email = self.s.get(table, self.name)
            if self.email is None or self.email =="":
                out.Output.say("I'm sorry, there is no contact by that name."
                                "Try again.")
        out.Output.say("Please enter their new email address.")
        self.email = input("> ")
        self.email = rsa.encrypt(self.email.encode(), self.publicKey)
        self.s.modify(table, self.email, self.name)
        out.Output.say("Their email has now been changed.")
        self.s.close()
