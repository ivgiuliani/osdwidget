import time
import re
import pyosd

import settings
import widget

def handle():
    w = {
        'batt':     widget.BatteryWidget,
        'temp':     widget.TemperatureWidget,
        'cpu':      widget.CPUWidget,
    }

    widgets = [w[widget_name]() for widget_name in settings.widgets if widget_name in w.keys()]

    while True:
        [osd.display() for osd in widgets]
        time.sleep(settings.INTERVAL)

