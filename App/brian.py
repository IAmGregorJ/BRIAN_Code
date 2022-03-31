# Make sure to run this like: brian.py 2>/dev/null
'''imports'''
import traceback
import Communication.SpeechIn as ind
import Communication.Output as out

i = ind.SpeechIn()

WAKE = "hey brian"
print("BRIAN initialized")

while True:
    print("Listening...")
    #x = range(3)
    text = i.listen()
    if text.count(WAKE) > 0:
        try:
            del text
            o = out.Output()
            o.say("Yes?")
        except AttributeError:
            print("Attribute Error")
        # now add the recognizer to listen/execute command
        try:
            command = i.listen()
            i.interpret(command)
        except Exception as ex:
            print(f"Unknown Error: {ex}")
            print(traceback.format_exc())
