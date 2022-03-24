'''imports'''
import os
import psutil
import Communication.Output as out


class Status():
    '''answer to the question how are you?'''
    def __init__(self) -> None:
        status = out.Output()
        cpu = self.get_cpu_usage_pct()
        temp = self.get_cpu_temp()
        ram = round(self.get_ram_usage() / 1024 / 1024, 2)
        status.say(f"I'm doing just fine, thanks. My cpu load is at {cpu} percent"
                    f" and my temperature is {temp} degrees."
                    f" RAM usage is at {ram} megabytes."
                    "The sun is shining somewhere in the world"
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
