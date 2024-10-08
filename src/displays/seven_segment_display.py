import time
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

class SevenSegmentDisplay:
    def __init__(self, n_cascading:int=1):
        """
        Args:
            n_cascading (int): number of cascaded seven segment displays - [>=1]
        """
        # create seven segment device
        self.serial = spi(port=0, device=1, gpio=noop()) # device 1 = CE1
        self.device = max7219(self.serial, cascaded=n_cascading)
        self.segment = sevensegment(self.device)
        self.segment.device.contrast(0) # darkest property
    
    def update_display(self, value:float):
        """Changes value on seven segment display
        Args:
            value (float): value to update seven segment display
        """
        num_spaces = self.segment.device.cascaded * 8 - len(str(value).replace(".", "")) # available digits - required digits (without dots)
        right_aligned_text = " " * num_spaces + str(value)
        self.segment.text = right_aligned_text # draws value

    def set_brightness(self, level:int):
        """Brightness property
        Args:
            level (int): numeric value from 0 up to 15
        """
        # set min and max value if param out of brightness range
        if level < 0:
            level = 0
        elif level > 15:
            level = 15
        self.segment.device.contrast(level * 16) # set brightness