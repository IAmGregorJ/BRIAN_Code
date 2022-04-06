# Make sure to run this like: brian.py 2>/dev/null
'''imports'''
import traceback
import os
import Communication.SpeechIn as ind
import Communication.Output as out
from sty import fg, bg

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
            ind.SpeechIn.interpret(command)
        except Exception as ex: #pylint: disable=broad-except
            print(f"Unknown Error: {ex}")
            print(traceback.format_exc())
