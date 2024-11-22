from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT

class MatrixDisplay:
    def __init__(self, n_cascading:int=1, block_orientation:int=0, rotation:int=0, inreverse:bool=False):
        """
        Args:
            n_cascading (int): number of cascaded matrices (MAX7219) - [>=1]
            block_orientation (int): Corrects block orientation when wired vertically - [0, 90, -90]
            rotation (int): Rotate display - [0=0°, 1=90°, 2=180°, 3=270°]
            inreverse (bool): Set to true if blocks are in reverse order - [True, False]
        """
        self.current_text:str = None # currently showed text
        self.font = proportional(LCD_FONT) # default font
        self.scroll_delay = 0.08 # default scroll speed lower=faster

        # create matrix device
        self.serial = spi(port=0, device=0, gpio=noop()) # device 0 = CE0
        self.device = max7219(self.serial, cascaded=n_cascading, block_orientation=block_orientation,
                              rotate=rotation, blocks_arranged_in_reverse_order=inreverse)
        self.device.contrast(0) # brightness
        
    
    def update_display(self, source_name:str, unit:str):
        """Changes text on matrix
        Args:
            source_name (str): text to update matrix
            unit (str): unit of updated data
        """
        ##### show_message(self.device, source_name, fill="white", font=self.font, scroll_delay=self.scroll_delay)
        with canvas(self.device) as draw:
            # TODO: alias flush left, unit flush right without creating new character set
            if unit[-1] == "C": # Celsius as unit (last letter is "C")
                # TODO: dot position in relative distance to the "C"
                draw.point((8,0), fill="white") # dot for degree sign (font doesn't contain degree char)
            text(draw, (0, 0), unit, fill="white", font=self.font)
    
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
        self.device.contrast(level * 16) # set brightness

