from operator import truediv
import sys
import os, subprocess, platform
from re import sub
from pathlib import Path
import threading
from tkinter import E
import speech_recognition as sr
from gtts import gTTS
import playsound
from datetime import date, datetime

home = str(Path.home())
todo_list = ['Go shopping', 'Clean room', 'Record video']

def say(text):
    tts = gTTS(text=text, lang="en", tld="ca")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove("voice.mp3")


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 0.2)
        audio = r.listen(source)
        said = ""
    try:
        said = r.recognize_google(audio)
        print(said)
    except Exception as e:
        print("No sound received: " + str(e))
    return said.lower()


def listen_caps():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 0.2)
        audio = r.listen(source)
        said = ""
    try:
        said = r.recognize_google(audio, language="en-CA")
        for r in ((" comma", ","), (" period", "."), (" exclamation point", "!"), (" question mark", "?")):
            said = said.replace(*r)
            print(said)
    except Exception as e:
        print("Exception: " + str(e))
    return said


def oopen(file):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', file))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(file)
    else:                                   # linux variants
        subprocess.call(('xdg-open', file))


def create_note():
    say("What do you want to write onto your note?")
    done = False
    while not done:
        try:
            note = listen_caps()
            say("Choose a filename!")
            filename = listen()
            # converts to PascalCase
            filename = sub(r"(_|-)+", " ", filename).title().replace(" ", "")
            # converts to camelCase
            filename = filename[0].lower() + filename[1:]
            path = f"{home}/{filename}.txt"
            # convert to snake case??? re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
            with open(path, 'w') as f:
                f.write(note)
                done = True
                say(f"Your note {filename} was successfully created and saved to your home directory")
                oopen(path)
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            say("Sorry, I didn't catch that?")


def add_todo():
    say("What todo do you want to do?")
    done = False
    while not done:
        try:
            item = listen_caps()
            todo_list.append(item)
            done = True
            say(f"I added {item} to your todo list")
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            say("Sorry, come again?")


def show_todos():
    say("Your todo list has the following items:")
    for item in todo_list:
        say(item)


def tell_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    say(f"The current time is {current_time}")


def alarm_clock():
    text = "Wake up!"
    say("What time would you like your alarm to ring?")
    done = False
    while not done:
        try:
            alarm_time = listen().replace(":","").replace("/","")
            alarm_hour = alarm_time[0:2]
            alarm_minute = alarm_time[2:4]
            try:
                val = int(alarm_hour)
            except:
                recognizer = sr.Recognizer()
                say("I'm sorry, that was some weird input.")
                break
            try:
                val = int(alarm_minute)
            except:
                recognizer = sr.Recognizer()
                say("I'm sorry, that was some weird input.")
                break
            if len(alarm_minute) == 1:
                alarm_minute = alarm_time[3:5]
            done = True
            say(f"I have set your alarm to {alarm_time}")
            now = datetime.now()
            print(now.strftime("%H"), now.strftime("%M"))
            print(alarm_hour, alarm_minute)
            x = threading.Thread(target=alarm_function, args = (alarm_hour, alarm_minute, text), daemon=True)
            x.start()
            #alarm_function(alarm_hour, alarm_minute)
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            say("Excuse me?")


def reminder():
    text = "This is your reminder"
    say("What would you like me to remind you?")
    done = False
    while not done:
        try:
            reminder = listen_caps()
            say("When would you like me to remind you about that?")
            try:
                reminder_time = listen().replace(":","").replace("/","")
                reminder_hour = reminder_time[0:2]
                reminder_minute = reminder_time[2:4]
                try:
                    val = int(reminder_hour)
                except:
                    recognizer = sr.Recognizer()
                    say("I'm sorry, that was some weird input.")
                    break
                try:
                    val = int(reminder_minute)
                except:
                    recognizer = sr.Recognizer()
                    say("I'm sorry, that was some weird input.")
                    break
                if len(reminder_minute) == 1:
                    reminder_minute = reminder_time[3:5]
                done = True
                say(f"I will remind you at {reminder_time}")
                now = datetime.now()
                print(now.strftime("%H"), now.strftime("%M"))
                print(reminder_hour, reminder_minute)
                x = threading.Thread(target=reminder_function, args = (reminder_hour, reminder_minute, reminder), daemon=True)
                x.start()
                #alarm_function(alarm_hour, alarm_minute)
            except sr.UnknownValueError:
                recognizer = sr.Recognizer()
                say("Excuse me?")
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            say("I'm sorry, I didn't quite catch that.")


def play_alarm():
    playsound.playsound("alarmClock.mp3")


def reminder_text(reminder):
    say(reminder)


def reminder_function(reminder_hour, reminder_minute, text):
    while True:
        reminder_hour = reminder_hour
        reminder_minute = reminder_minute
        now = datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
        if(reminder_hour == current_hour):
            if(reminder_minute == current_minute):
                print(text)
                reminder_text(f"This is your reminder: {text}")
                break



def alarm_function(alarm_hour, alarm_minute, text):
    while True:
        alarm_hour = alarm_hour
        alarm_minute = alarm_minute
        now = datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
        if(alarm_hour == current_hour):
            if(alarm_minute == current_minute):
                print(text)
                play_alarm()
                break


def hello():
    now = datetime.now()
    if now < now.replace(hour=8, minute=00):
        say("Good morning Sir!")
        # morning_routine()
    elif now < now.replace(hour=12, minute=00):
        say("Hello Sir, how may I serve you?")
    elif now < now.replace(hour=17, minute=00):
        say("Good afternoon Sir.")
    else:
        say("Good evening Sir.")


def quit():
    say("I hope to be able to serve you again soon.")
    sys.exit(0)
