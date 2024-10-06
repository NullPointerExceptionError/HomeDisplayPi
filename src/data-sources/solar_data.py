from sungrow_websocket import SungrowWebsocket

class SolarData:
    def __init__(self, ip_address:str, locale:str="en_US"):
        """
        Args:
            ip_address (str): IP-address of host (sungrow-inverter)
            locale(str): language specifications
        """
        self.ip_address = ip_address
        self.locale = locale
        self.sungrow = SungrowWebsocket(ip_address, locale) # inverter object

    def get_data(self, item_name:str) -> float:
        """requets data from inverter and returns its value
        Args:
            item_name (str): unique name of item to get data of it (key of requested item from SungrowWebsocket)

        Returns:
            float: value of requested data (uses default unit of inverter, except of watts (kW instead of W))
        """
        data = self.sungrow.get_data()
        