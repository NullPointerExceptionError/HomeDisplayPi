import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class MatrixDisplay:
    def __init__(self):
        self.current_text:str = None # currently showed text
    
    def update_display(self, data:str):
        """Changes text on matrix

        Args:
            data (str): text to update matrix
        """

