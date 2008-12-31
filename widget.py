import re

from base import BaseWidget
from settings import *

class BatteryWidget(BaseWidget):
    present_re = re.compile("^present:[ ]+no$")
    full_capacity_re = re.compile("^last full capacity:[ ]+(?P<capacity>[\d]+) mWh$")
    remaining_capacity_re = re.compile("^remaining capacity:[ ]+(?P<remaining>[\d]+) mWh$")

    def __init__(self):
        super(BatteryWidget, self).__init__()
        self.set_horizontal_offset(230)

    def get_msg(self):
        level = self.get_battery_level()
        
        if not level:
            return ("Battery Not Found", "red")

        if level > 50:
            color = "green"
        elif level > 20:
            color = "yellow"
        else:
            color = "red"

        return ("Battery level: %d%%" % level, color)

    def get_battery_level(self):
        """
        Returns the % of the battery level or None if the battery
        is not present
        """
        batt_inserted = True
    
        batt_capacity = 0
        f = open(BAT_INFO, "r")
        for line in f.readlines():
            if self.present_re.match(line.strip()):
                batt_inserted = False
                break
            else:
                mo = self.full_capacity_re.match(line.strip())
                if not mo:
                    continue
    
                batt_capacity = mo.group("capacity")
        f.close()
    
        if not batt_inserted:
            return None
    
        batt_remaining = 0
        f = open(BAT_STATE, "r")
        for line in f.readlines():
            mo = self.remaining_capacity_re.match(line.strip())
            if not mo:
                continue
    
            batt_remaining = mo.group("remaining")
        f.close()
    
        return (int(batt_remaining) * 100) / int(batt_capacity)


class TemperatureWidget(BaseWidget):
    temp_re = re.compile("^temperature:[ ]+(?P<temperature>[\d]+) C$")

    def __init__(self):
        super(TemperatureWidget, self).__init__()
        self.set_horizontal_offset(120)

    def get_msg(self):
        temp = self.get_temperature_level()

        if temp > 60:
            color = "red"
        elif temp > 50:
            color = "yellow"
        else:
            color = "green"

        return ("Temperature %d C" % temp, color)

    def get_temperature_level(self):
        """
        Returns the current temperature in Celsius
        """
        f = open(TEMPERATURE, "r")
        line = f.readline().strip()
        mo = self.temp_re.match(line)
        if mo:
            temp = int(mo.group("temperature"))
        else:
            temp = 0
        f.close()
    
        return temp
    

class CPUWidget(BaseWidget):
    cpu_re = re.compile("^cpu MHz[\t ]+: (?P<cpu_speed>[\d]+)[.\d]*$")

    def __init__(self):
        super(CPUWidget, self).__init__()
        self.set_horizontal_offset(5)

    def get_msg(self):
        level = self.get_cpu_level()
        return ("CPU Speed: %dMHz" % level, "yellow")

    def get_cpu_level(self):
        """
        Returns the CPU actual speed
        """
    
        speed = 0
        f = open(CPUSPEED, "r")
        for line in f.readlines():
            mo = self.cpu_re.match(line.strip())
            if mo:
                speed = mo.group("cpu_speed")
                break
        f.close()
    
        return int(speed)
