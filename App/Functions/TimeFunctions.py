'''imports'''
from datetime import date, datetime
import threading
import playsound
import Communication.Output as out
import Communication.SpeechIn as ind


class TimeFunction:
    '''used for telling time and alarm'''
    def __init__(self) -> None:
        pass

    # I know I should be refactoring the output into another method
    # but I'm stumped on how to call a method from a static method
    @staticmethod
    def tell_time():
        '''what time is it'''
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        o = out.Output()
        o.say(f"The current time is {current_time}")
        del o
        #return None

    @staticmethod
    def tell_date():
        '''what is the date'''
        today = date.today()
        o = out.Output()
        o.say(f"Today's date is {today}")
        del o
        return None

    @staticmethod
    def alarm_clock():
        '''alarm clock function'''
        text = "Wake up!"
        o = out.Output()
        o.say("What time would you like your alarm to ring?")
        done = False
        while not done:
            alarm_hour, alarm_minute = TimeFunction.get_time_input()
            done = True
        o.say(f"I have set your alarm to {alarm_hour} {alarm_minute}")
        del o
        x = threading.Thread(target = TimeFunction.alarm_function,
                            args = (alarm_hour, alarm_minute, text),
                            daemon = True)
        x.start()

    @staticmethod
    def get_time_input():
        '''get the desired alarm time'''
        i = ind.SpeechIn()
        o = out.Output()
        exmessage = "I'm sorry, that was some weird input."
        alarm_time = i.listen().replace(":","").replace("/","")
        try:
            int(alarm_time)
        except ValueError:
            o.say(exmessage)
            return
        try:
            len(str(alarm_time)) > 4
        except ValueError:
            o.say(exmessage)
            return
        alarm_hour = alarm_time[0:2]
        if len(str(alarm_time)) == 3:
            alarm_hour = alarm_time[0:1]
        alarm_minute = alarm_time[2:4]
        if len(alarm_minute) == 1:
            alarm_minute = alarm_time[1:3]
        try:
            int(alarm_hour) < 25
        except ValueError:
            o.say(exmessage)
            return
        try:
            int(alarm_minute) < 60
        except ValueError:
            o.say(exmessage)
            return
        del o
        return alarm_hour, alarm_minute

    @staticmethod
    def alarm_function(alarm_hour, alarm_minute, text):
        '''after an alarm or reminder is set, this is the \"motor\"'''
        while True:
            now = datetime.now()
            current_hour = now.strftime("%H")
            current_minute = now.strftime("%M")
            if alarm_hour == current_hour:
                if alarm_minute == current_minute:
                    print(text)
                    playsound.playsound("App/Ressources/alarmClock.mp3")
                    break
