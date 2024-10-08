import threading
import time
from displays import matrix_display
from displays import seven_segment_display
from data_sources import solar_data
from data_sources import temperature_and_humidity_data

class DisplayController:
    def __init__(self, data_sources_info:dict[str:dict[str:str]],
                 inverter_ip:str,
                 inverter_locale:str="en_US",
                 n_cascading_matrix:int=1,
                 block_orientation_matrix:int=0,
                 rotation_matrix:int=0,
                 inreverse_matrix:bool=False,
                 n_cascading_segment=1):
        """
        Args:
            data_sources_info (dict[str:dict[str:str]]): all data sources and their characteristics as string
            n_cascading_matrix (int): number of cascaded matrices (MAX7219) - [>=1]
            block_orientation_matrix (int): Corrects block orientation when wired vertically - [0, 90, -90]
            rotation_matrix (int): Rotate display - [0=0°, 1=90°, 2=180°, 3=270°]
            inreverse_matrix (bool): Set to true if blocks are in reverse order - [True, False]
        """
        self.data_sources_info:dict[str:dict[str:str]] = data_sources_info # all data source info
        self.data_sources:list = list(data_sources_info.keys()) # all data sources as string (unique name)
        self.current_index:int = 0 # index of currently showed data source
        self.auto_change_interval = 10 # delay before next data source change
        self.auto_change_thread = None # thread for changing datasources automatically
        self.lock = threading.Lock() # locks thread
        self.paused_auto_change:bool = False # indicates whether auto change is running
        self.reset_event = threading.Event() # starts auto change thrad
        self.update_thread = None # thread for value updates of current data source
        self.running:bool = True # flag for thread if system is running

        self.matrix_display_obj = matrix_display.MatrixDisplay(n_cascading_matrix, block_orientation_matrix, rotation_matrix, inreverse_matrix) # init matrix object
        self.seven_segment_display_obj = seven_segment_display.SevenSegmentDisplay(n_cascading_segment) # init seven segment object
        self.matrix_display_obj.set_brightness(1) # brightness level 2
        self.seven_segment_display_obj.set_brightness(4)

        self.solar_obj = solar_data.SolarData(inverter_ip, locale=inverter_locale) # init inverter object
        self.climate_obj = temperature_and_humidity_data.TemperatureAndHumidity() # init climate data object
        

    def switch_data_source(self):
        """switches data source to next source
        """
        self.current_index = (self.current_index + 1) % len(self.data_sources) # index++
        self.update_displays()
    
    def get_value_from_source(self, source:str) -> float:
        """returns value of given source
        Args:
            source (str): unique name of source which is equal to data_sources_info key
        
        Returns:
            float: currently measured value of source (int if no decimal places)
        """
        try:
            if self.data_sources_info[source]["is_inverter_item"]: # if item to request inverter
                value = self.solar_obj.get_data(source) # get value from source, None if error
            else: # if item to request climate sensors
                if source == "temperature":
                    value = self.climate_obj.get_temperature()
                elif source == "humidity":
                    value = self.climate_obj.get_humidity()
                else:
                    value = None
            # expand if-condition here if you have another data source library/file

            if value == None:
                return None
            else: # returns float if value has decimal places !=0
                if float(value) == round(float(value)): # if integer value (without decimal places)
                    return int(float(value))
                else:
                    return float(value)
        except KeyError as e:
            print("KeyError:", e)
    
    def update_displays(self):
        """updates text and value from displays to next data source
        """
        source = self.data_sources[self.current_index] # source key
        value = self.get_value_from_source(source) # numeric value
        source_name = self.data_sources_info[source]["name"] # name to show for scrolling text
        source_unit = self.data_sources_info[source]["alias_and_unit"] # unit to show as static display on matrix
        self.seven_segment_display_obj.update_display("") # clear sevensegment first
        self.matrix_display_obj.update_display(source_name, source_unit) # scrolling text, then alias + unit
        self.seven_segment_display_obj.update_display(value) # show numeric value
        time.sleep(5)