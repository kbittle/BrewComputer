# -*- coding: cp1252 -*-
import time, sys, select, math, os, threading, random
from datetime import datetime
import pygame
import utility
from widgets.colors import *
from widgets.tempController import paintTempController
from widgets.brewSetup import paintBreweryDiagram
from widgets.menuStrip import drawMenuStrip
from widgets.oldGuiDisplay import guiDisplay
from widgets.switch import paintSwitch
from widgets.graph import graph_display
import interfaces.arduinoMMI as arduinoMMI
import interfaces.arduinoWaterLevel as arduinoWaterLevel
from constants import *
from simple_pid import PID

# Debug feature to run sw without the correct hardware
_DEBUG_ = False
_BLYNK_ = True

if _BLYNK_:    
    import interfaces.blynk_lib as blynk_lib

if (os.name == 'nt') or (_DEBUG_):
    _ENABLE_EXTERNAL_IO_ = False
else:
    _ENABLE_EXTERNAL_IO_ = True

if _ENABLE_EXTERNAL_IO_:
    import hw_lib.ds1307_lib as ds1307_lib  
    import hw_lib.ds18b20_lib as ds18b20_lib
    import hw_lib.lcd_lib as lcd_lib    
    import RPi.GPIO as GPIO
    import interfaces.sql_database_lib as sql_database_lib

# Pygame frame variables
frame_count = 0
frame_rate = 100
start_time = 90

# Global Variables
indicatorFlashState = ['0', 125]
sensor_number = 0
sensor_temperature = [0,0,0]
temperature_log = [[0,0]]
heatOutput = False
current_time = datetime.now()
current_time_in_seconds = 0
power_up_time = datetime.now()
first_conversion_complete_flag = False
conversion_event = 0
current_temperature = 0
target_temperature = 212
waterLevelValue = 0
countdownTimerSeconds = 3600
gasSwitchState = 0
gasLedValue = False
pumpSwitchState = 0

# LCD variables
ipAddress = "0.0.0.0"

# Icon indicator vars
blynkConnected  = False
wifiConnected   = False
databaseSetup   = False

# Fault indicator vars
mmiError        = True
waterLevelError = True
rtcError        = True
i2cError        = True

##-----------------------------------------------------------------

# Configure this 0 for RPI B and 1 for RPI A
if (os.name != 'nt'):
    if utility.isRpiA():
        print(">> RPI Model A Detected")
        smbusNumber = 1
    else:
        print(">> RPI Model B/C Detected")
        smbusNumber = 0

# For use when debuggin code and a monitor is not connected
if (os.name != 'nt') and (_DEBUG_):
    os.environ["SDL_VIDEODRIVER"] = "fbcon"

print(">> Pre Screen Init")

pygame.init()
pygame.display.set_caption("Temperature Controller")

# Init Libraries and Widgets
screen         = pygame.display.set_mode([full_screen_width, full_screen_height])

print(">> Post Screen Init")

if _ENABLE_EXTERNAL_IO_:
    realTime   = ds1307_lib.ds1307(smbusNumber)
    oneWireBus = ds18b20_lib.ds18b20(smbusNumber)
    lcd        = lcd_lib.lcd(smbusNumber)
    #adc        = ads1015_lib.ads1015()
    database   = sql_database_lib.sql_database_lib()

mmi        = arduinoMMI.arduinoMMI()
waterLevel = arduinoWaterLevel.arduinoWaterLevel()

# Setup GPIO to control the mosfet
if _ENABLE_EXTERNAL_IO_:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(PUMP_PIN, GPIO.OUT)
 
#Loop until the user clicks the close button.
done=False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

heat_font = pygame.font.Font(None, 100)

# Initialize BLYNK library
if _BLYNK_:
    blynkLib = blynk_lib.blynk_lib()
    blynkLib.run()

# Initialize PID algorithm for SSR control
pid = PID(0.5, 1, 1, setpoint=target_temperature)
# Only want to output a 0 or a 1
pid.output_limits = (0, 1)
# Set sample time to 0.5 seconds
pid.sample_time = 0.5

##-----------------------------------------------------------------

# Calculates the furute linear temperature
def calc_future_temp(prev_temp, current_temp):
    #####change this to effect how soon to shut off burner
    multiplier = 2
    #####
    slope = float(current_temp-prev_temp)
    return ((multiplier * slope) + current_temp)

# Grab time before stepping into the main program loop
if _ENABLE_EXTERNAL_IO_:
    try:
        tmpTime = realTime.getDateDs1307()
        power_up_time = time.mktime(tmpTime.timetuple())
        rtcError = False
    except:
        # Might want to figure out a better way to come up with an RTC error??
        rtcError = True

if _ENABLE_EXTERNAL_IO_:
    # Get local IP Address
    ipAddress = utility.get_ip_address()

if (os.name != 'nt'):
    # Chech wifi connection
    wifiConnected = utility.isWifiConnected()
    # Check if database is configured
    databaseSetup = utility.doesDatabaseExist()
     
# -------- Main Program Loop --------------------------------------
while done==False:

    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done=True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                done=True
            elif event.key == pygame.K_ESCAPE:
                done=True            
            elif event.key == pygame.K_1:
                sensor_number = 0
            elif event.key == pygame.K_2:
                sensor_number = 1
            elif event.key == pygame.K_3:
                sensor_number = 2
            elif event.key == pygame.K_4:
                sensor_temperature[1] = 120
            elif event.key == pygame.K_UP:
                sensor_temperature[sensor_number] += 1                
            elif event.key == pygame.K_DOWN:
                sensor_temperature[sensor_number] -= 1
        #elif event.type == pygame.MOUSEBUTTONDOWN:
        #    if button_1.pressed(pygame.mouse.get_pos()):
        #        sensor_temperature[sensor_number] += 5
        #    elif button_2.pressed(pygame.mouse.get_pos()):
        #        sensor_temperature[sensor_number] = 10

    if _ENABLE_EXTERNAL_IO_:
        # Due to not knowing how fast the temp readings are made and knowing
        # that temperature conversions can take almost a second. The readings
        # are staggered.
        if first_conversion_complete_flag:
            if conversion_event == 0:
                # Read temperature sesnor
                sensor_temperature[0] = oneWireBus.Sensor_Read_Temp(ROM1)
                # Start next temp conversion
                oneWireBus.Sensor_Convert(ROM1)
            elif conversion_event == 1:
                # Read temperature sesnor
                sensor_temperature[1] = oneWireBus.Sensor_Read_Temp(ROM2)   
                # Start next temp conversion
                oneWireBus.Sensor_Convert(ROM2)
            elif conversion_event == 2:
                # Read temperature sesnor
                sensor_temperature[2] = oneWireBus.Sensor_Read_Temp(ROM3)
                # Start next temp conversion
                oneWireBus.Sensor_Convert(ROM3)
        
            try:
                # Get RTC time in string format
                current_time = realTime.getDateDs1307()        
                # Convert to seconds
                current_time_in_seconds = time.mktime(current_time.timetuple())
                rtcError = False
            except:
                print("RTC Error")
                rtcError = True
            
            # Update database with newest temp
            database.update_temperature(1, sensor_temperature[0])
            database.update_temperature(2, sensor_temperature[1])
            database.update_temperature(3, sensor_temperature[2])
        else:
            if conversion_event == 0:
                oneWireBus.Sensor_Convert(ROM1)
                database.add_sensor_to_db(ROM1, "Sensor 1")
            elif conversion_event == 1:
                oneWireBus.Sensor_Convert(ROM2)
                database.add_sensor_to_db(ROM2, "Sensor 2")
            elif conversion_event == 2:
                oneWireBus.Sensor_Convert(ROM3)
                database.add_sensor_to_db(ROM3, "Sensor 3")
            first_conversion_complete_flag = True

        # Cycle through temp calculations on all the sensors
        conversion_event += 1
        if conversion_event > 3:
            conversion_event = 0
    else:
        # Test scenario, using fake data
        first_conversion_complete_flag = True

    #---------------------- Serial Device Logic -----------------------
    # Check serial threads for new messages and process them
    if _ENABLE_EXTERNAL_IO_:
        mmi.doWork()
        gasSwitchState = mmi.getGasSwitchState()
        pumpSwitchState = mmi.getPumpSwitchState()
        target_temperature = mmi.getTargetTempState()
        mmiError = mmi.getCommStatus()

    if _ENABLE_EXTERNAL_IO_:
        waterLevel.doWork()
        waterLevelError = waterLevel.getCommStatus()

    #------------------------------------------------------------------
    # I2c error is evaluated by checking all i2c devices
    if _ENABLE_EXTERNAL_IO_:
        if (realTime.getI2cErrors() > 0) or (oneWireBus.getI2cErrors() > 0) or (lcd.getI2cErrors() > 0):
            # Print debug for diagnosing errors
            print(">> rtc={0}, 1wire={1}, lcd={2}".format(
                realTime.getI2cErrors(), oneWireBus.getI2cErrors(), lcd.getI2cErrors()))
            # Set error flag for GUI
            i2cError = True
        else:
            i2cError = False
    
    #----------------------- Gas Controll Logic -----------------------
    # Determine if the gas solenoid valve should be activated
    if gasSwitchState == FIRE_SWITCH_AUTO:
        # Automatic Gas Fire operation
        if first_conversion_complete_flag:
            # Update PID setpoint if needed
            if not target_temperature == pid.setpoint:
                pid.setpoint = target_temperature

            # Translate current temp from sensors
            current_temperature = sensor_temperature[0]

            # Run algorithm
            heatOutput = pid(current_temperature) 
            print(">> PID=" + str(heatOutput))
    elif gasSwitchState == FIRE_SWITCH_ON:
        heatOutput = True
    else:
        heatOutput = False

    # Set indicator value
    gasLedValue = heatOutput

    # Set pin output state for mosfet controlling gas solenoid
    if _ENABLE_EXTERNAL_IO_:
        if heatOutput:
            GPIO.output(SOLENOID_PIN, GPIO.HIGH)
        else:
            GPIO.output(SOLENOID_PIN, GPIO.LOW)

    #----------------------- Update LCD Strings -----------------------
    if _ENABLE_EXTERNAL_IO_:
        lcd.lcd_display_string(ipAddress, 1)
        lcd.lcd_display_string("Error: {0}".format(False), 2)

    #----------------------- Update pump output -----------------------
    if _ENABLE_EXTERNAL_IO_:
        if (pumpSwitchState == PUMP_SWITCH_ON) or (pumpSwitchState == PUMP_SWITCH_AUTO):
            GPIO.output(PUMP_PIN, GPIO.HIGH)
        else:
            GPIO.output(PUMP_PIN, GPIO.LOW)

    #----------------------- Handle Timer logic -----------------------
    if _BLYNK_:
        if blynkConnected:
            data = blynkLib.getTimerData()
            # If the countdown timer is enabled, start decrementing the 
            # counter. Otherwise set the timer to whatever is enabled in 
            # blynk terminal
            if data[0] == True:
                countdownTimerSeconds = countdownTimerSeconds - 1                
            else:
                countdownTimerSeconds = int(data[1])
    else:
        countdownTimerSeconds = countdownTimerSeconds - 1

    #if (frame_count % 60) == 0:
    if _BLYNK_:
        # Check Blynk connection to cloud
        blynkConnected = blynkLib.isAppConnected()

        # Try to write data to the cloud
        blynkLib.writeDataToServer(sensor_temperature[0],
                                   sensor_temperature[1], 
                                   sensor_temperature[2],
                                   gasLedValue,
                                   pumpSwitchState,
                                   target_temperature,
                                   countdownTimerSeconds)
    
    # Add this in for windows testsing
    if not _ENABLE_EXTERNAL_IO_:
        if (frame_count % 30) == 0:
            #sensor_temperature[0] = random.uniform(1, 250)
            #sensor_temperature[1] = random.uniform(1, 250)
            #sensor_temperature[2] = random.uniform(1, 250)
            #switch_heat = random.randint(0,1)
            #waterLevelValue = random.randint(0,100)
            #gasSwitchState = random.randint(0,2)
            gasSwitchState = FIRE_SWITCH_AUTO
            pumpSwitchState = random.randint(0,2)
    
    #
    #------------------- Rendering From Here Below --------------------
    #
    screen.fill(grey1)

    drawMenuStrip(pygame, screen, 0, 0, 65, current_time, blynkConnected, databaseSetup, 
        wifiConnected, countdownTimerSeconds, mmiError, waterLevelError, 
        rtcError, i2cError, indicatorFlashState)
    paintTempController(pygame, screen, 0, 68, sensor_temperature[0], target_temperature, gasLedValue)
    paintSwitch(pygame, screen, 0 , 374, "Gas", gasSwitchState)
    paintSwitch(pygame, screen, 0 , 580, "Pump", pumpSwitchState)
    paintBreweryDiagram(pygame, screen, 305, 66, sensor_temperature[1], sensor_temperature[2], 
        pumpSwitchState, True, True, waterLevelValue);

    graph_display(pygame, screen, 304, 565, full_screen_width-308, 200, 
        int(round(current_temperature)), target_temperature, temperature_log)
  

    # If blynk features are turned on, consistently cal the run() function to handle socket traffic.
    if _BLYNK_:            
        blynkLib.run()

    #print("frame_count = {0}".format(frame_count))

    frame_count += 1
    pygame.display.flip()      
    clock.tick(frame_rate)    

# Kill serial thread
mmi.close()
waterLevel.close()

# Stop pygame
pygame.quit()
