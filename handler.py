import time
import re
import pyosd

import settings
import widget
import gmail

def handle():
    osd_gmail = gmail.GMailWidget()
    osd_batt = widget.BatteryWidget()
    osd_temp = widget.TemperatureWidget()
    osd_cpu = widget.CPUWidget()

    while True:
        osd_batt.display()
        osd_temp.display()
        osd_cpu.display()
        osd_gmail.display()

        time.sleep(settings.INTERVAL)

