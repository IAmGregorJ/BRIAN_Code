# remember that espeak package needs to be installed on the system
# also, pip install --upgrade pyaudio
# the webcam mic does NOT work, but the onboard does no problem
# pip install speechrecognition
# pip install gtts
# pip install neuralintents
# pip install pocketsphinx
# pip install playsound


from basic_functions import *

import speech_recognition as sr
from neuralintents import GenericAssistant

# The assistant analyses what it hears
mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "time": tell_time,
    "alarm": alarm_clock,
    "reminder": reminder,
    "exit": quit
}

assistant = GenericAssistant('intents.json', intent_methods = mappings)
assistant.train_model()
# end of analysing
"""
It's also possibile with the following neuralintents methods to save and load the model
so that we don't have to do it every time.
In the interest of saving time and keeping the program as simple as possible, I won't do this
It's a small model with few lines, so training it doesn't "cost" anything anyway


assistant.save_model()
assistant.load_model()
"""

WAKE = "hey brian"
print("Start")

while True:
    print("Listening")
    text = listen()

    if text.count(WAKE) > 0:
        say("Yes Sir?")
        try:
            text = listen()
            assistant.request(text)
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            print("Exception: at the end of this file.")
