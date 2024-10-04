from display_controllers import display_controller
import time

def main():
    # data sources names and units
    data_sources_info:dict[str:dict[str:str]] = {"total_active_power" : {"name" : "PV-in",
                                                                        "alias_and_unit" : "P W",
                                                                        "is_inverter_item" : True},
                                                "load_total_active_power" : {"name" : "Verbrauch",
                                                                            "alias_and_unit" : "V W",
                                                                            "is_inverter_item" : True},
                                                "battery_soc" : {"name" : "Batterie",
                                                                "alias_and_unit" : "B %",
                                                                "is_inverter_item" : True},
                                                "temperature_corridor" : {"name" : "Temperatur",
                                                                        "alias_and_unit" : "T C",
                                                                        "is_inverter_item" : False},
                                                "humidity_corridor" : {"name" : "Luftfeuchtigkeit",
                                                                        "alias_and_unit" : "L %",
                                                                        "is_inverter_item" : False}}
                                                # Key: name of data source (same name as inverter-item if inverter_item!)
                                                # Value: list of information concerning data source
                                                # name: name to show on display ("" for default name)
                                                # alias_and_unit: alias of data source with unit (showed after full name scrolled) - e.g. "B %" for Battery charge level in percent
                                                # is_inverter_item: bool if source from inverter (sources from inverter dont need changes in another script)

    # matrix adjustments
    n_cascading_matrix:int = 2 # number of cascaded matrices (MAX7219) - [>=1]
    block_orientation_matrix:int = 0 # Corrects block orientation when wired vertically - [0, 90, -90]
    rotation_matrix:int = 2 # Rotate display - [0=0°, 1=90°, 2=180°, 3=270°]
    inreverse_matrix:bool = False # Set to true if blocks are in reverse order - [True, False]
    
    display_controller_obj = display_controller.DisplayController(data_sources_info,
                                                                  n_cascading_matrix=n_cascading_matrix,
                                                                  block_orientation_matrix=block_orientation_matrix,
                                                                  rotation_matrix=rotation_matrix,
                                                                  inreverse_matrix=inreverse_matrix) # init display controller object


if __name__ == "__main__":
    main()