'''imports'''
import os
import time
import Communication.Output as out
import psutil


class Status():
    '''answer to the question how are you?'''
    def __init__(self):
        self.cpu = self.get_cpu_usage_pct()
        self.temp = self.get_cpu_temp()
        self.ram = round(self.get_ram_usage() / 1024 / 1024 / 1024, 2)
        self.uptime = self.get_uptime()
        self.free = self.get_disk_free_percent()
        self.battery = self.get_battery_status()

    def give_status(self):
        '''give an output of the current status'''

        out.Output.say(f"I'm doing just fine thanks."
                    f"It has been {self.sec_to_hours(self.uptime)} since boot.\n"
                    f"My cpu load is at {self.cpu} percent"
                    f" and my temperature is {self.temp} degrees.\n"
                    f"{self.free} percent of the main drive is free.\n"
                    f" RAM usage is at {self.ram} gigabytes.\n"
                    f"There is {self.sec_to_hours(self.battery)} battery time left"
                    " and you're here with me. I'm happy!")
    def get_cpu_usage_pct(self):
        '''the system's average CPU load as measured over a period of 500 ms'''
        return psutil.cpu_percent(interval=0.5)
    def get_cpu_temp(self):
        '''Obtains the current value of the CPU temperature'''
        # Initialize the result.
        result = 0.0
        # The first line in this file holds the CPU temperature as an integer times 1000.
        # Read the first line and remove the newline character at the end of the string.
        if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
            with open('/sys/class/thermal/thermal_zone0/temp', encoding='utf8') as f:
                line = f.readline().strip()
            # Test if the string is an integer as expected.
            if line.isdigit():
                # Convert the string with the CPU temperature to a float in degrees Celsius.
                result = float(line) / 1000
        # Give the result back to the caller.
        return result
    def get_ram_usage(self):
        '''Obtains the absolute number of RAM bytes currently in use by the system'''
        return int(psutil.virtual_memory().total - psutil.virtual_memory().available)
    ## NEW FUNCTION
    def get_uptime(self):
        '''Gets the total time that the computer has been running since boot'''
        return time.time() - psutil.boot_time()
    def sec_to_hours(self, seconds):
        '''convert seconds to hours'''
        hours=str(round(seconds//3600))
        minutes=str((round(seconds%3600)//60))
        scnds=str((round(seconds%3600)%60))
        d = f"{hours} hours, {minutes} minutes and {scnds} seconds"
        return d
    def get_disk_free_percent(self):
        '''get percent of free disk space'''
        disk = psutil.disk_usage('/')
        percent_free = 100 - disk.percent
        return percent_free
    def get_battery_status(self):
        '''Get battery power left'''
        battery = psutil.sensors_battery()
        return battery.secsleft
