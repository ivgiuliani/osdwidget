import time
import re
import pyosd

BAT_INFO = "/proc/acpi/battery/BAT0/info"
BAT_STATE = "/proc/acpi/battery/BAT0/state"
TEMPERATURE = "/proc/acpi/thermal_zone/THM0/temperature"
CPUSPEED = "/proc/cpuinfo"
FONT_FACE = "-*-fixed-medium-r-*-*-12-*-*-*-*-*-*-*"
INTERVAL = 5

# common regexps
present_re = re.compile("^present:[ ]+no$")
full_capacity_re = re.compile("^last full capacity:[ ]+(?P<capacity>[\d]+) mWh$")
remaining_capacity_re = re.compile("^remaining capacity:[ ]+(?P<remaining>[\d]+) mWh$")
temp_re = re.compile("^temperature:[ ]+(?P<temperature>[\d]+) C$")
cpu_re = re.compile("^cpu MHz[\t ]+: (?P<cpu_speed>[\d]+)[.\d]*$")

def handle():
    osd_batt = pyosd.osd()
    osd_temp = pyosd.osd()
    osd_cpu = pyosd.osd()

    for osd in [ osd_batt, osd_temp, osd_cpu ]:
        # set common stuff
        osd.set_font(FONT_FACE)
        osd.set_outline_offset(1)
        osd.set_timeout(0)
        osd.set_vertical_offset(2)
        osd.set_align(pyosd.ALIGN_RIGHT)
        osd.set_pos(pyosd.POS_TOP)
        osd.set_colour("yellow")

    osd_batt.set_horizontal_offset(230)
    osd_temp.set_horizontal_offset(120)
    osd_cpu.set_horizontal_offset(5)

    while True:
        batt = get_battery_level()
        temp = get_temperature_level()
        cpu = get_cpu_level()

        if not batt:
            osd_batt.set_colour("red")
            osd_batt.display("Battery Not Found")
        else:
            if batt > 50:
                osd_batt.set_colour("green")
            elif batt > 10:
                osd_batt.set_colour("yellow")
            else:
                osd_batt.set_colour("red")

            osd_batt.display("Battery level: %d%%" % batt)

        if temp > 60:
            osd_temp.set_colour("red")
        elif temp > 45:
            osd_temp.set_colour("yellow")
        else:
            osd_temp.set_colour("green")


        osd_temp.display("Temperature: %d C" % temp)
        osd_cpu.display("CPU Speed: %dMHz" % cpu)

        time.sleep(INTERVAL)

def get_battery_level():
    """
    Returns the % of the battery level or None if the battery
    is not present
    """
    battery = None
    batt_inserted = True

    batt_capacity = 0
    f = open(BAT_INFO, "r")
    for line in f.readlines():
        if present_re.match(line.strip()):
            batt_inserted = False
            break
        else:
            mo = full_capacity_re.match(line.strip())
            if not mo:
                continue
            batt_capacity = mo.group("capacity")
    f.close()

    if not batt_inserted:
        return None

    batt_remaining = 0
    f = open(BAT_STATE, "r")
    for line in f.readlines():
        mo = remaining_capacity_re.match(line.strip())
        if not mo:
            continue

        batt_remaining = mo.group("remaining")
    f.close()

    battery = (int(batt_remaining) * 100) / int(batt_capacity)
    return battery

def get_temperature_level():
    """
    Returns the current temperature in Celsius
    """
    f = open(TEMPERATURE, "r")
    line = f.readline().strip()
    mo = temp_re.match(line)
    if mo:
        temp = int(mo.group("temperature"))
    else:
        temp = 0
    f.close()

    return temp

def get_cpu_level():
    """
    Returns the CPU actual speed
    """

    speed = 0
    f = open(CPUSPEED, "r")
    for line in f.readlines():
        mo = cpu_re.match(line.strip())
        if mo:
            speed = int(mo.group("cpu_speed"))
            break
    f.close()

    return speed
