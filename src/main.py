from display_controllers import display_controller
import time

def main():
    # data sources and units
    data_sources:list[str] = ["total_active_power",
                              "load_total_active_power",
                              "battery_soc",
                              "temperature_corridor",
                              "humidity_corridor"] # name of all data sources
    data_units:dict[str:str] = {"total_active_power" : "P W",
                                "load_total_active_power" : "V W",
                                "battery_soc" : "B %",
                                "temperature_corridor" : "T C",
                                "humidity_corridor" : "L %"} # Key: name of data source, Value: alias of data source with unit

    # matrix adjustments
    n_cascading_matrix:int = 2 # number of cascaded matrices (MAX7219) - [>=1]
    block_orientation_matrix:int = 0 # Corrects block orientation when wired vertically - [0, 90, -90]
    rotation_matrix:int = 2 # Rotate display - [0=0°, 1=90°, 2=180°, 3=270°]
    inreverse_matrix:bool = False # Set to true if blocks are in reverse order - [True, False]

    display_controller_obj = display_controller(data_sources,
                                                n_cascading_matrix=n_cascading_matrix,
                                                block_orientation_matrix=block_orientation_matrix,
                                                rotation_matrix=rotation_matrix,
                                                inreverse_matrix=inreverse_matrix) # init display controller object

if __name__ == "__main__":
    main()