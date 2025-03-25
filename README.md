# HomeDisplayPi
Displays data from Sungrow inverter and some temperature data on LED matrix and 7-segment display with Raspberry Pi.

# Overview
HomeDisplayPi is a Python based project which runs on a Raspberry Pi. It displays sensor data from your solar plant and temperature sensors if you have on an LED-matrix and seven segment display. The program updates sensor values in real-time and switches automatically between them.

# Features
- Display of solar and temperature data on an led matrix and a seven segment display
- Switchung data sources automatically
- Adjustment of display brightness based on current time (dimming at night, 8 pm to 8 am)
- Support of Raspberry Pi with configurable number of cascading for each display

# Requirements
If you don't have all sensors or more than these sensors, you can also use this program.
- Raspberry Pi (tested with Raspberry Pi 3B+)
- Network connection (same network as your inverter or VPN)
- Enabled SPI in raspi-config
- Enabled one-wire in raspi-config (only for DS18B20)
- Python 3 (tested with Python 3.12.6)
- Pip (tested with pip 24.2)
- Sungrow inverter with WiNet-S Communication Dongle
- DS18B20 sensor for precise temperature measurement (one decimal place, technically three decimal places possible)
- DHT11 sensor for temperature and humidity (without decimal places)
- Installed libraries (see requirements.txt)

# Installation
1. Connect your displays and sensors exactly as described below
2. Enable SPI and one-wire in your Raspberry configurations
   ```bash
   sudo raspi-config
   ```
   Navigate to `Interface Options` > `SPI` > `Enable` and `Interface Options` > `1-Wire` > `Enable` and reboot your Raspberry Pi.
3. Clone this repository (just download it if you haven't installed git)
   ```bash
   git clone https://github.com/NullPointerExceptionError/HomeDisplayPi.git
   ```
4. Navigate into the HomeDisplayPi folder
5. Create and activate virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
6. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
7. Navigate into the `main.py` file in the src folder and type in your inverter ip address (`inverter_ip = ""`). You can find your inverters' ip-address simply by using apps like [WIFIman](https://play.google.com/store/apps/details?id=com.ubnt.usurvey&hl=en). Then type in your username (`username = "user"`) and password (`password = "your-password"`) for the WiNet-S interface. Please note: this isn't normally the same account as for the iSolarCloud app. If you have never changed this password, leave the default values as they are.

# Wiring
Note: The programm works also without the more accurate DS18B20 sensor.
| GPIO- 	| PIN on Raspberry 	| port on device | device  	                     |
| :-:	   | :-:	               | :-:	           | :-:                             |
| 2     	| 5V    	            | VCC	           | LED-Matrix 8x8 module           |
| 6     	| GND   	            | GND	           | "                               |
| 19     | MOSI (GPIO-10)    	| DIN            | "                               |
| 24     | CE0 (GPIO-8)    	| CS 	           | "                               |
| 23     | SCLK (GPIO-11)   	| CLK	           | "                               |
| 4     	| 5V                	| VCC            | seven segment 8-digit module    |
| 25     | GND             	| GND	           | "                               |
| 19     | MOSI (GPIO-10)    	| DIN	           | "                               |
| 26     | CE1 (GPIO-7)    	| CS 	           | "                               |
| 23     | SCLK (GPIO-11)    	| CLK	           | "                               |
| 1     	| 3.3V             	| red wire       | DS18B20 temperature sensor      |
| 9     	| GND             	| black wire     | "                               |
| 7     	| GPCLK0 (GPIO-4)   	| yellow wire    | "                               |
| 1     	| 3.3V              	| 1. PIN         | DHT-11 temperature and humidity |
| 11     | GPIO-17          	| 2. PIN         | "                               |
| 9     	| GND             	| 4. PIN         | "                               |

# How to use
1. Activate virtual environment in the HomeDisplayPi folder
   ```bash
   source venv/bin/activate
   ```
2. Start the program
   ```bash
   python3 src/main.py &
   ```
   If you want to have a log file with errors, use the following command instead (also possible via ssh).
   ```bash
   nohup python3 src/main.py > output.log 2>&1 &
   ```
To stop the program use
```bash
ps aux | grep main.py
kill -2 <PID>
```
replace `<PID>` with the far left number of the correct process (something like `src/main.py`).

# Adjustments
Basic adjustments are in `main.py` in the src folder. If you have advanced knowledge, you can also adjust a few things in the `display_controller.py`
### Data sources
- You can add or remove inverter items by addind or removing a block in the `data_sources_info` variable. Make sure that you use the correct item name when adding an inverter item (e.g. "battery_soc" for charge level of your battery. You can find the correct keys by printing out the `data` variable in `solar_data.py`).
- By changing the `"name" : ""`, the scrolling text (LED matrix) of the data source will be customized.
- By changing the `"alias_and_unit" : ""`, the text showed after full name scrolled can be customized - (e.g. "B %" for Battery charge level in percent)
- By changing the `"is_inverter_item" : `, you can toggle if this item needs to request the inverter or if its a sensor (if you add sensors, you have to change more in the code)
- By changing the `"duration" : `, you can set the duration in seconds for which the data of a data source should be displayed
### Inverter
- `inverter_ip = ""`: ip address of the network module of your inverter
- `inverter_locale = ""`: this affects the data language of the inverter
### LED Matrix (8x8 modules)
- `n_cascading_matrix = `: number of cascaded matrices - e.g. 4 if you have 4 matrices
- `block_orientation_matrix = `: Corrects block orientation when wired vertically (0, 90 or -90)
- `rotation_matrix = `: rotate display (0=0°, 1=90°, 2=180°, 3=270°)
- `inreverse_matrx = `: toggle if blocks are in reverse order (True, False)
### Seven segment display (8-digit modules)
- `n_cascading_segment = `: number of cascaded seven segment modules - e.g. 2 if you have 2 8-digit modules

# Button for restarting HomeDisplayPi
If you want to have a button to easier restart HomeDisplayPi, take a look at [Restart Button (Addon for HomeDisplayPi)](https://github.com/NullPointerExceptionError/Restart-Button-for-HomeDisplayPi/).

## Troubleshooting
If you find bugs, errors, have suggestions for improvement or would like to suggest new features, feel free to open an [issue](https://github.com/NullPointerExceptionError/HomeDisplayPi/issues) or [pull request](https://github.com/NullPointerExceptionError/HomeDisplayPi/pulls).
