'''imports'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from configparser import ConfigParser
import Communication.Output as out
import Communication.SpeechIn as ind
from Functions import Contacts

# pylint: disable=consider-using-f-string

class Email():
    '''Class to hold the mail object and the functions'''
    def __init__(self) -> None:
        '''Constructor'''
        config = ConfigParser()
        config.read("App/secrets.ini")
        self.mail_password = config.get("smtp", "smtp_pass")
        self.mail_user = config.get("smtp", "smtp_user")
        self.mail_server = config.get("smtp", "smtp_server")
        self.mail_port = config.get("smtp", "smtp_port")
        self.sent_from = ""
        self.send_to = ""
        self.subject = ""
        self.body = ""

    def get_mail_input(self, usermail):
        '''get the information about the mail to be sent from the user'''
        sent_from = usermail
        out.Output.say("Are you writing to someone who is already in your contacts list?")
        answer = ind.SpeechIn.listen()
        if "no" in answer:
            out.Output.say("Let's add a new contact then.")
            recipient = Contacts.Contact()
            send_to = recipient.add_contact()
        else:
            recipient = Contacts.Contact()
            send_to = recipient.get_contact()
        to = send_to
        out.Output.say("What is the subject of this mail?")
        email_subject = ind.SpeechIn.dictate()
        out.Output.say("And what do you want to write in the mail?")
        body = ind.SpeechIn.dictate()
        self.send_email(sent_from, to, email_subject, body)

    def send_email(self, sent_from, receiver, subject, body):
        '''sending the actual message'''
        message = MIMEMultipart()
        #Setup the MIME
        message['From'] = sent_from
        message['To'] = receiver
        message['Subject'] = subject
        #The body and the attachments for the mail
        message.attach(MIMEText(body, 'plain'))
        #Create SMTP session for sending the mail
        try:
            session = smtplib.SMTP(self.mail_server, self.mail_port)
            session.starttls() #enable security
            session.login(self.mail_user, self.mail_password)
            text = message.as_string()
            session.sendmail(sent_from, receiver, text)
            session.quit()
            out.Output.say("Your email has been sent.")
        except smtplib.SMTPAuthenticationError:
            out.Output.say("There is something wrong with your smtp username or password")
        except Exception as ex: #pylint: disable=broad-except
            out.Output.say("An error occured while trying to send your mail.")
            print(ex)
        