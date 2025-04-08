from sungrowinverter import SungrowInverter
import asyncio

class SolarData:
    def __init__(self, ip_address:str, timeout:int, port:int=502):
        """
        Args:
            ip_address (str): IP-address of host (sungrow-inverter)
            username(str): username to WiNet-S
            password(str): password to WiNet-S
            locale(str): language specifications
            port(int): port to WiNet-S
        """
        self.ip_address = ip_address
        self.timeout = timeout
        self.port = port
        try:
            self.sungrow = SungrowInverter(self.ip_address, timeout=self.timeout, port=self.port) # inverter object
        except Exception as e:
            self.sungrow = None

    def reconnect(self):
        """tries reconnecting to inverter once
        """
        self.sungrow = SungrowInverter(self.ip_address, timeout=self.timeout, port=self.port)
        print("Reconnecting to inverter:", self.ip_address)


    def get_data(self, item_name:str) -> float:
        """requets data from inverter and returns its value
        Args:
            item_name (str): unique name of item to get data of it (key of requested item from SungrowWebsocket)

        Returns:
            float: value of requested data
        """
        try:
            result = asyncio.run(self.sungrow.async_update())

            if not result:
                self.reconnect()
                result = asyncio.run(self.sungrow.async_update())
            
            data = self.sungrow.data
            value = data[item_name]
            return value
        except KeyError as e:
            print("KeyError: Key", e, "is no item of inverter")
            self.sungrow = None
            return None
        except TimeoutError as e:
            print("TimeoutError:", e)
            self.sungrow = None
            return None
        except OSError as e:
            if e.errno == 113:
                print("Host unreachable:", self.ip_address, ", check network connection")
                self.sungrow = None
                return None
            else:
                print("OSError with Code", e.errno, ":", e)
                self.sungrow = None
                return None
        except Exception as e:
            print("Unknown Error:", e)
            self.sungrow = None
            return None


if __name__ == "__main__":
    sungrow = SolarData("192.168.178.47", 5, 502)
    for i in range(20):
        print("---", i, "---")
        print("PV-in:", sungrow.get_data("total_dc_power"))
        import time
        # time.sleep(5)
        print("Verbrauch", ":", sungrow.get_data("load_power"))
        # time.sleep(5)
        print("Batterie", ":", sungrow.get_data("battery_level"))
        # time.sleep(5)
