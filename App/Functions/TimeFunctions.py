'''imports'''
from datetime import date, datetime
import time
import threading
from playsound import playsound
import Communication.Output as out
import Communication.SpeechIn as ind
from base_logger import logger

pomodoro_stop = False #yes the use of globals sucks, but I couldn't find an alternative
is_started = False

class TimeFunction:
    '''used for telling time and alarms'''
    def __init__(self) -> None:
        pass

    @staticmethod
    def print_time():
        '''returns the time in text format'''
        now = datetime.now()
        current_time = now.strftime("%H:%M: ")
        return current_time

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
        a = threading.Thread(target = TimeFunction.alarm_function,
                            args = (alarm_hour, alarm_minute, text),
                            daemon = True)
        a.start()

    @staticmethod
    def get_time_input():
        '''get the desired alarm time'''
        # Only works with 24-hour format
        exmessage = "I'm sorry, that was some weird input."
        alarm_time = ind.SpeechIn.listen().replace(":","").replace("/","")
        try:
            int(alarm_time)
        except ValueError as ex:
            logger.error(repr(ex))
            out.Output.say(exmessage)
            return
        try:
            len(str(alarm_time)) > 4
        except ValueError as ex:
            logger.error(repr(ex))
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
        except ValueError as ex:
            logger.error(repr(ex))
            out.Output.say(exmessage)
            return
        try:
            int(alarm_minute) < 60
        except ValueError as ex:
            logger.error(repr(ex))
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
                    playsound("App/Ressources/alarmClock.mp3")
                    break

    @staticmethod
    def pomodoro_timer():
        '''pomodoro timer'''
        alarm = "App/Ressources/Timer.mp3"
        count = 0
        while True:
            count += 1
            if count == 1:
                out.Output.say("Your pomodoro session starts now. "
                                "Work for 25 minutes, then we'll take a short break.")
            else:
                playsound(alarm)
                out.Output.say("\nTime to get back to work!")
            for _ in range(300):
                time.sleep(5)
                if pomodoro_stop:
                    return
            if count % 4 != 0:
                playsound(alarm)
                out.Output.say("Now it's time for a 5 minute break! "
                                f"\nYou have completed {count} pomodoros so far.")
                for _ in range(60):
                    time.sleep(5)
                    if pomodoro_stop:
                        return
            else:
                playsound(alarm)
                out.Output.say(f"\nThat was your {count}th pomodoro! "
                                "Stretch your legs for 20 minutes this time.")
                for _ in range(240):
                    time.sleep(5)
                    if pomodoro_stop:
                        return

    @staticmethod
    def run_pomodoro():
        '''start the pomodoro timer'''
        global is_started #pylint: disable=global-statement
        global pomodoro_stop #pylint: disable=global-statement
        pomodoro_stop = False
        # Because this time should not be run more than once
        if not is_started:
            is_started = True
            p = threading.Thread(target = TimeFunction.pomodoro_timer,
                            daemon = True)
            p.start()
        else:
            out.Output.say("I'm sorry, you can only run one pomodoro timer session at a time.")

    @staticmethod
    def stop_pomodoro():
        '''stop the pomodoro timer'''
        global pomodoro_stop #pylint: disable=global-statement
        pomodoro_stop = True
        global is_started #pylint: disable=global-statement
        is_started = False
        out.Output.say("Your pomodoro session has been stopped.")

    @staticmethod
    def timer(minutes):
        '''kitchen timer'''
        alarm = "App/Ressources/Timer.mp3"
        time.sleep(minutes)
        playsound(alarm)
        out.Output.say("\nYour timer is finished.")


    @staticmethod
    def set_timer():
        '''kitchen timer function'''
        exmessage = "Sorry, that was some weird input"

        out.Output.say("How many minutes would you like to set the timer for?")
        minutes = ind.SpeechIn.listen()
        try:
            int(minutes)
        except ValueError as ex:
            logger.error(repr(ex))
            out.Output.say(exmessage)
            return
        out.Output.say(f"I have set your timer for {minutes} minutes")
        t = threading.Thread(target = TimeFunction.timer,
                            args = (int(minutes) * 60),
                            daemon = True)
        t.start()
