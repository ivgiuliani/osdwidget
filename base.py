import pyosd

from settings import FONT_FACE

class BaseWidget(object):
    """
    The base class for the OSD widgets. Every widget should extend
    this class to do its dirty stuff.
    """

    def __init__(self):
        osd = pyosd.osd()
        self.msg = ""

        # set common stuff
        osd.set_font(FONT_FACE)
        osd.set_outline_offset(1)
        osd.set_timeout(0)
        osd.set_vertical_offset(2)
        osd.set_align(pyosd.ALIGN_RIGHT)
        osd.set_pos(pyosd.POS_TOP)
        osd.set_colour("yellow")

        self.osd = osd

    def update(self, text, color):
        self.msg = (text, color)

    def get_msg(self):
        """
        Returns the tuple in the format (message, color) where message
        is the text that should be shown on OSD and color the text's
        color.

        In most cases, when extending this class you may want to override
        only this method.
        """
        return self.msg

    def display(self):
        """
        Display the text through OSD
        """
        msg = self.get_msg()
        self.osd.set_colour(msg[1])
        self.osd.display(msg[0])

    def set_horizontal_offset(self, offset):
        """
        Set the OSD horizontal offset
        """
        self.osd.set_horizontal_offset(offset)
