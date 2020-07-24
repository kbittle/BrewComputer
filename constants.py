import os

# Define ROM Addresses
ROM1 = [0x28,0xAD,0xCA,0x2B,0x04,0x00,0x00,0xED]
ROM2 = [0x28,0xA3,0xF6,0x2A,0x04,0x00,0x00,0xD4]
ROM3 = [0x28,0x80,0x49,0x2B,0x04,0x00,0x00,0x94]

# Define Pins
SOLENOID_PIN = 11
PUMP_PIN = 13

# Define MMI defs
FIRE_SWITCH_ON = 2
FIRE_SWITCH_AUTO = 1
FIRE_SWITCH_OFF = 0

PUMP_SWITCH_ON = 2
PUMP_SWITCH_AUTO = 1
PUMP_SWITCH_OFF = 0

# Resource Paths
if (os.name != 'nt'):
    SEVEN_SEGMENT_FONT_PATH = "/home/pi/BrewComputer/resources/7segment.ttf"
    BLYNK_ICON_PATH = '/home/pi/BrewComputer/resources/blynk.png'
    WIFI_ICON_PATH = '/home/pi/BrewComputer/resources/wifi.png'
    DATABASE_ICON_PATH = '/home/pi/BrewComputer/resources/database.png'
    AMERICAN_FLAG_PATH = '/home/pi/BrewComputer/resources/americanFlag.png'
    BREWERY_PNG_PATH = '/home/pi/BrewComputer/resources/breweryLayout.png'
    OLD_BREWERY_PNG_PATH = '/home/pi/BrewComputer/resources/baseSetup.png'
else:
    SEVEN_SEGMENT_FONT_PATH = "resources/7segment.ttf"
    BLYNK_ICON_PATH = 'resources/blynk.png'
    WIFI_ICON_PATH = 'resources/wifi.png'
    DATABASE_ICON_PATH = 'resources/database.png'
    AMERICAN_FLAG_PATH = 'resources/americanFlag.png'
    BREWERY_PNG_PATH = 'resources/breweryLayout.png'
    OLD_BREWERY_PNG_PATH = 'resources/baseSetup.png'
