'''imports'''
from datetime import date, datetime
import time
import threading
import playsound
import Communication.Output as out
import Communication.SpeechIn as ind

thread_status = False #yes the use of globals sucks, but I couldn't find an alternative

class TimeFunction:
    '''used for telling time and alarms'''
    def __init__(self) -> None:
        pass

    @staticmethod
    def tell_time():
        '''what time is it'''
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        out.Output.say(f"The current time is {current_time}")

    @staticmethod
    def tell_date():
        '''what is the date'''
        today = date.today()
        out.Output.say(f"Today's date is {today}")

    @staticmethod
    def alarm_clock():
        '''alarm clock function'''
        text = "\nWake up!"
        out.Output.say("What time would you like your alarm to ring?")
        done = False
        while not done:
            alarm_hour, alarm_minute = TimeFunction.get_time_input()
            done = True
        out.Output.say(f"I have set your alarm to {alarm_hour} {alarm_minute}")
        x = threading.Thread(target = TimeFunction.alarm_function,
                            args = (alarm_hour, alarm_minute, text),
                            daemon = True)
        x.start()

    @staticmethod
    def get_time_input():
        '''get the desired alarm time'''
        exmessage = "I'm sorry, that was some weird input."
        alarm_time = ind.SpeechIn.listen().replace(":","").replace("/","")
        try:
            int(alarm_time)
        except ValueError:
            out.Output.say(exmessage)
            return
        try:
            len(str(alarm_time)) > 4
        except ValueError:
            out.Output.say(exmessage)
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
            out.Output.say(exmessage)
            return
        try:
            int(alarm_minute) < 60
        except ValueError:
            out.Output.say(exmessage)
            return
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

    @staticmethod
    def pomodoro_timer():
        '''pomodoro timer'''
        #global thread_status
        count = 0
        while True:
            count += 1
            if count == 1:
                out.Output.say("Your pomodoro session starts now. "
                                "Work for 25 minutes, then we'll take a short break.")
            else:
                out.Output.say("Time to get back to work!")
            for _ in range(300):
                time.sleep(5)
                if thread_status:
                    return
            if count % 4 != 0:
                out.Output.say("Now it's time for a 5 minute break! "
                                f"You have completed {count} pomodoros so far.")
                for _ in range(60):
                    time.sleep(5)
                    if thread_status:
                        return
            else:
                out.Output.say(f"That was your {count}th pomodoro! "
                                "Stretch your legs for 20 minutes this time.")
                for _ in range(240):
                    time.sleep(5)
                    if thread_status:
                        return

    @staticmethod
    def run_pomodoro():
        '''start the pomodoro timer'''
        global thread_status #pylint: disable=global-statement
        thread_status = False
        x = threading.Thread(target = TimeFunction.pomodoro_timer,
                            daemon = True)
        x.start()

    @staticmethod
    def stop_pomodoro():
        '''stop the pomodoro timer'''
        global thread_status #pylint: disable=global-statement
        thread_status = True
        out.Output.say("Your pomodoro session has been stopped.")
