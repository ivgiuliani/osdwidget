import time
import re
import pyosd
from gmail import GmailOsd

import widget
from settings import *

# common regexps

def handle():
    osd_gmail = pyosd.osd()
    osd_batt = widget.BatteryWidget()
    osd_temp = widget.TemperatureWidget()
    osd_cpu = widget.CPUWidget()

    for osd in [ osd_gmail ]:
        # set common stuff
        osd.set_font(FONT_FACE)
        osd.set_outline_offset(1)
        osd.set_timeout(0)
        osd.set_vertical_offset(2)
        osd.set_align(pyosd.ALIGN_RIGHT)
        osd.set_pos(pyosd.POS_TOP)
        osd.set_colour("yellow")

    osd_gmail.set_horizontal_offset(350)

    # start the GMail thread
    gmail = GmailOsd(osd_gmail)
    gmail.start()

    while True:
        osd_batt.display()
        osd_temp.display()
        osd_cpu.display()

        gmail.refresh()

        time.sleep(INTERVAL)

