'''imports'''
#import time

import Communication.Input as ind
import Communication.output as out


i = ind.Input()

WAKE = "hey brian"
print("BRIAN initialized")

while True:
    x = range(3)
    text = i.listen()
    print("text: " + text)
    if text.count(WAKE) > 0:
        out = out.Output()
        out.say("Yes?")
        # now add the recognizer to listen/execute command
        text = i.listen()
        i.interpret(text)
