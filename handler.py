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

    widgets = [ osd_gmail, osd_batt, osd_temp, osd_cpu ]

    while True:
        [osd.display() for osd in widgets]
        time.sleep(settings.INTERVAL)

