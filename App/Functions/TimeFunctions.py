'''imports'''
from datetime import date, datetime
import Communication.Output as out


class TimeFunction:
    '''used for telling time and alarm'''
    def __init__(self) -> None:
        pass

    @staticmethod
    def tell_time():
        '''what time is it'''
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        t = out.Output()
        t.say(f"The current time is {current_time}")
        del t
        return None

    @staticmethod
    def tell_date():
        '''what is the date'''
        today = date.today()
        t = out.Output()
        t.say(f"Today's date is {today}")
        del t
        return None
