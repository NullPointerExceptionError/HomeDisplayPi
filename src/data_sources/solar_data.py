from sungrow_websocket import SungrowWebsocket
from aiohttp import ClientConnectorError # to catch connection error
from websockets import ConnectionClosedError, InvalidMessage

class SolarData:
    def __init__(self, ip_address:str, locale:str="en_US"):
        """
        Args:
            ip_address (str): IP-address of host (sungrow-inverter)
            locale(str): language specifications
        """
        self.ip_address = ip_address
        self.locale = locale
        try:
            self.sungrow = SungrowWebsocket(self.ip_address, locale=self.locale) # inverter object
        except Exception as e:
            self.sungrow = None

    def reconnect(self):
        """tries reconnecting to inverter once
        """
        self.sungrow = SungrowWebsocket(self.ip_address, locale=self.locale)


    def get_data(self, item_name:str) -> float:
        """requets data from inverter and returns its value
        Args:
            item_name (str): unique name of item to get data of it (key of requested item from SungrowWebsocket)

        Returns:
            float: value of requested data (uses default unit of inverter, except of watts (kW instead of W))
        """
        try:
            if not self.sungrow:
                self.reconnect()

            data = self.sungrow.get_data()
            value = data[item_name].value
            if data[item_name].unit == "kW":
                value = float(value) * 1000 # unit kW -> W
            return value
        except ClientConnectorError as e: # no connection to inverter
            print("ClientConnectionError:", e)
            self.sungrow = None
            return None
        except KeyError as e:
            print("KeyError: Key", e, "is no item of inverter")
            self.sungrow = None
            return None
        except ConnectionClosedError as e:
            print("ConnectionClosedError:", e, "- please check if another device is currently accessing inverter host")
            self.sungrow = None
            return None
        except InvalidMessage as e:
            print("InvalidMessageError:", e, "- please check if another device is currently accessing inverter host")
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


        
