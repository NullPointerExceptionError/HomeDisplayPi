import threading
import time
from displays import matrix_display
from displays import sevensegment_display

class DisplayController:
    def __init__(self, data_sources:list[str], n_cascading_matrix:int=1, block_orientation_matrix:int=0, rotation_matrix:int=0, inreverse_matrix:bool=False):
        """
        Args:
            data_sources (list): all data sources as string
            n_cascading_matrix (int): number of cascaded matrices (MAX7219) - [>=1]
            block_orientation_matrix (int): Corrects block orientation when wired vertically - [0, 90, -90]
            rotation_matrix (int): Rotate display - [0=0°, 1=90°, 2=180°, 3=270°]
            inreverse_matrix (bool): Set to true if blocks are in reverse order - [True, False]
        """
        self.data_sources:list = data_sources # all data sources as string
        self.current_index:int = 0 # index of currently showed data source
        self.auto_change_interval = 10 # delay before next data source change
        self.auto_change_thread = None # thread for changing datasources automatically
        self.lock = threading.Lock() # locks thread
        self.paused_auto_change = False # indicates whether auto change is running
        self.reset_event = threading.Event() # starts auto change thrad
        self.update_thread = None # thread for value updates of current data source
        self.running = True # flag for thread if system is running

        self.matrix_display = matrix_display(n_cascading_matrix, block_orientation_matrix, rotation_matrix, inreverse_matrix) # init matrix object
        self.seven_segment_display = sevensegment_display() # init seven segment object