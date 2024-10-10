import os
import glob
import Adafruit_DHT

class TemperatureAndHumidity:
    def __init__(self):
        # load 1-wire modules
        try:
            os.system("modprobe w1-gpio")
            os.system("modprobe w1-therm")

        base_dir = "/sys/bus/w1/devices/"
        device_folder = glob.glob(base_dir + "28*") # search for DS18B20 device

        # check if DS18B20 connected
        self.ds18_connected = False # DS18B20 connected
        if device_folder:
            self.device_file = device_folder[0] + "/w1_slave" # use first device (if multiple DS18B20 connected)
            raw_ds18 = self.read_raw_ds18()
            self.ds18_connected = self.is_valid_ds18(raw_ds18) # checks if sensor dekivers valid values


        self.sensor_dht11 = Adafruit_DHT.DHT11
        self.pin = 17

        # check if DHT11 connected
        self.dht11_connected = False
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_dht11, self.pin)
        if humidity or temperature: # if one of both values id valid
            self.dht11_connected = True
    
    def read_raw_ds18(self) -> list[str]:
        """returns array of lines from the DS18B20 file
        Returns:
            list[str]: array of lines from file
        """
        try:
            with open(self.device_file, "r") as d_file:
                lines = d_file.readlines()
            return lines
        except FileNotFoundError as e:
            print("FileNotFoundError:", e)
            return[". crc=00", ". t=0"]
    
    def is_valid_ds18(self, lines) -> bool:
        """returns if ds18 returns valid values
        Args:
            lines (list[str]): DS18B20 file as array
        
        Returns:
            bool: if DS18B20 returns valid values
        """
        if (int(lines[0].strip().split("crc=")[-1][:2], 16) == 0) and (int(lines[1].strip().split("t=")[-1]) == 0): # if crc and temperature are both zero
            return False
        return True
    
    def get_temperature(self):
        """measures current temperature from preferred DS18B20-sensor and secondly from DHT11-sensor.
        Sensors that weren't connected at program start are no longer checked for connection.
        Reason for this is too bad running time if every update the program checks for cinnected sensors.
        However, sensors that have brief interruptions during the course of the program are checked for
        connection each time.

        Returns:
            float: temperature value, accurate to 1 decimal places (3 decimal places technically possible)
        """
        if self.ds18_connected: # checks whether it has been connected once from init
            # value of DS18B20
            lines = self.read_raw_ds18()
            if self.is_valid_ds18(lines): # checks if still connected
                value = float(lines[1].strip().split("t=")[-1]) / 1000 # temperature value
                return round(value, 1)
        
        if self.dht11_connected: # checks whether it has been connected once from init
            # value of DHT11
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor_dht11, self.pin, retries=3, delay_seconds=1) # gets current data from sensor
            if temperature == None:
                return None
            else:
                return int(temperature) # sensor is not able to measure decimal places
        
        return None # none of them connected
    
    def get_humidity(self):
        """measures current humidity from DHT11-sensor
        Returns:
            int: humidity value as Integer
        """
        if self.dht11_connected:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor_dht11, self.pin, retries=3, delay_seconds=1) # gets current data from sensor
            if humidity == None:
                return None
            else:
                return int(humidity)
        return None
