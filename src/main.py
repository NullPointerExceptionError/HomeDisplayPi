from display_controllers import display_controller

def main():
    # data sources names and units
    data_sources_info:dict[str:dict[str:any]] = {"total_dcpower" : {"name" : "PV-in",
                                                                        "alias_and_unit" : "P W",
                                                                        "is_inverter_item" : True,
                                                                        "duration": 20},
                                                "load_total_active_power" : {"name" : "Verbrauch",
                                                                            "alias_and_unit" : "V W",
                                                                            "is_inverter_item" : True,
                                                                            "duration": 20},
                                                "battery_soc" : {"name" : "Batterie",
                                                                "alias_and_unit" : "B %",
                                                                "is_inverter_item" : True,
                                                                "duration": 5},
                                                "temperature" : {"name" : "Temperatur",
                                                                        "alias_and_unit" : "T C",
                                                                        "is_inverter_item" : False,
                                                                        "duration": 5},
                                                "humidity" : {"name" : "Luftfeuchtigkeit",
                                                                        "alias_and_unit" : "L %",
                                                                        "is_inverter_item" : False,
                                                                        "duration": 5}}
                                                # Key: name of data source (same name as inverter-item if inverter_item!)
                                                # Value: list of information concerning data source
                                                # name: name to show on display ("" for default name)
                                                # alias_and_unit: alias of data source with unit (showed after full name scrolled) - e.g. "B %" for Battery charge level in percent
                                                # is_inverter_item: bool if source from inverter (sources from inverter dont need changes in another script)
                                                # duration: how long source is displayed

    # inverter information (type in your inverter ip address, username and passwort if changed from default)
    inverter_ip = "192.168.178.47"
    username = "user"
    password = "pw1111"
    port = 443
    inverter_locale = "en_US" # language for data source keys

    # matrix adjustments
    n_cascading_matrix:int = 2 # number of cascaded matrices (MAX7219) - [>=1]
    block_orientation_matrix:int = 0 # Corrects block orientation when wired vertically - [0, 90, -90]
    rotation_matrix:int = 2 # Rotate display - [0=0°, 1=90°, 2=180°, 3=270°]
    inreverse_matrix:bool = False # Set to true if blocks are in reverse order - [True, False]

    # seven segment adjustments
    n_cascading_segment = 1 # number of cascaded seven segment displays - [>=1]
    
    display_controller_obj = display_controller.DisplayController(data_sources_info,
                                                                  inverter_ip,
                                                                  username,
                                                                  password,
                                                                  port,
                                                                  inverter_locale=inverter_locale,
                                                                  n_cascading_matrix=n_cascading_matrix,
                                                                  block_orientation_matrix=block_orientation_matrix,
                                                                  rotation_matrix=rotation_matrix,
                                                                  inreverse_matrix=inreverse_matrix,
                                                                  n_cascading_segment=n_cascading_segment) # init display controller object

    display_controller_obj.start_auto_update_thread() # starts auto changing data sources thread
    display_controller_obj.start_update_thread() # starts thread for update values every second

if __name__ == "__main__":
    main()
