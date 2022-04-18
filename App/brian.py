# Make sure to run this like: exec python brian.py 2>/dev/null
'''imports'''
import traceback
import os
import Communication.SpeechIn as ind
import Communication.Output as out
import Functions.User as u
from sty import fg, bg

os.system('clear')
user = u.User()
if user.check_user() == 0:
    user.username, user.mail = user.create_user()
    user.is_logged_in = True
else:
    user.username, user.mail = user.verify_user()
    user.is_logged_in = True

while user.is_logged_in:
    os.system('clear')
    print(bg.blue, fg.yellow, "BRIAN initialized", fg.rs, bg.rs)
    i = ind.SpeechIn()
    WAKE = "ok brian"

    while True:
        print(".", end = "", flush=True)
        text = ind.SpeechIn.listen()
        if text.count(WAKE) > 0:
            try:
                del text
                out.Output.say("Yes?")
            except AttributeError:
                print("Attribute Error")
            # now add the recognizer to listen/execute command
            try:
                command = ind.SpeechIn.listen()
                ind.SpeechIn.interpret(user, command)
            except Exception as ex: #pylint: disable=broad-except
                print(f"Unknown Error: {ex}")
                print(traceback.format_exc())
                