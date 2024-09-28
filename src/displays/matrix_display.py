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
    def __init__(self, n_cascading:int=1, block_orientation:int=0, rotation:int=0, inreverse:bool=False):
        self.current_text:str = None # currently showed text
        self.font = proportional(LCD_FONT) # default font
        self.scroll_delay = 0.08 # default scroll speed lower=faster

        # create matrix device
        self.serial = spi(port=0, device=0, gpio=noop()) # device 0 = CE0
        self.device = max7219(self.serial, cascaded=n_cascading, block_orientation=block_orientation,
                              rotate=rotation, blocks_arranged_in_reverse_order=inreverse)
        self.device.contrast(0) # darkest property
        
    
    def update_display(self, data:str, unit:str):
        """Changes text on matrix

        Args:
            data (str): text to update matrix
            unit (str): unit of updated data
        """
        show_message(self.device, data, fill="white", font=self.font, scroll_delay=self.scroll_delay)
        with canvas(self.device) as draw:
            if unit=="T C":
                draw.point((8,0), fill="white") # dot for degree sign (font doesn't contain degree char)
            text(draw, (0, 0), unit, fill="white", font=self.font)
        # time.sleep(10)


####### TODO: just for testing #######
matrix = MatrixDisplay(n_cascading=2, rotation=2)
matrix.device.contrast(0)
matrix.update_display("PV-in", "P W")


