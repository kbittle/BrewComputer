import hw_lib.serial_io_lib as serial_io_lib
import os
from constants import *

class arduinoMMI:
    def __init__(self):
        # Initialize comm lass vars
        self.commLoss = True
        self.commLossCountdown = 0

        # Initialize data vars
        self.gasSwitchState = 0
        self.pumpSwitchState = 0
        self.target_temperature = 0

        # Assign serial port data
        if (os.name == 'nt'):
            self.portNum = 'COM10'
        else:
            self.portNum = '/dev/ttyUSB0'

        self.baudrate = 9600

        # Open serial port
        self.serial = serial_io_lib.SerialInterface(False, self.portNum, self.baudrate)
        self.serial.openPort()

        # If we were able to find the serial port
        if self.serial.isPortOpen():
            # Start thread to read serial port
            self.serial._start_reader()

    # Decode Serial packet and pull switch settings and target temp
    def decode_display_packet(self, packet):

        # Ensure at least 1 packet has been recieved
        if not packet:
            print(">> MMI Packet is null")
            return
        
        # Ensure its the correct pack, at this time there is only
        # one packet.
        if packet[0] == 15:
            # We are not doing any length checks at this time
            
            # Read in on/off/auto switch 1
            if packet[2] == 0:
                self.gasSwitchState = FIRE_SWITCH_AUTO
            elif packet[2] == 1:
                self.gasSwitchState = FIRE_SWITCH_ON
            elif packet[2] == 2:
                self.gasSwitchState = FIRE_SWITCH_OFF
                
            # Read in on/off/auto switch 2
            if packet[3] == 0:
                self.pumpSwitchState = PUMP_SWITCH_AUTO
            elif packet[3] == 1:
                self.pumpSwitchState = PUMP_SWITCH_ON
            elif packet[3] == 2:
                self.pumpSwitchState = PUMP_SWITCH_OFF

            # Read in rotary switch
            if packet[4] == 0:
                self.target_temperature = 0
            elif packet[4] == 1:
                self.target_temperature = 168
            elif packet[4] == 2:
                self.target_temperature = 170
            elif packet[4] == 3:
                self.target_temperature = 172
            elif packet[4] == 4:
                self.target_temperature = 208
            elif packet[4] == 5:
                self.target_temperature = 210
            elif packet[4] == 6:
                self.target_temperature = 212
            elif packet[4] == 7:
                self.target_temperature = 214
            elif packet[4] == 8:
                self.target_temperature = 216

            print(">> Gas={0}, Pump={1}, Target={2}".format(packet[2], packet[3], packet[4]))  

    def doWork(self):
        if self.serial.isPortOpen():
            # Decode latest serial packet to determine target temp
            packet = self.serial.get_latest_packet()
            self.decode_display_packet(packet)

            # If we have received at least one packet, restart comm loss countdown
            if self.serial.get_packet_count() > 0:
                self.commLossCountdown = 5
                self.commLoss = False
        else:
            # Retry to open serial port
            self.serial.openPort()

            # If we were able to find the serial port
            if self.serial.isPortOpen():
                # Start thread to read serial port
                self.serial._start_reader()

        if self.commLossCountdown > 0:
            self.commLossCountdown -= 1

            if self.commLossCountdown == 0:
                self.commLoss = True
                print("Comm Loss with MMI arduino")

    def close(self):
        self.serial._stop_reader()

    def getCommStatus(self):
        return self.commLoss

    def getGasSwitchState(self):
        return self.gasSwitchState

    def getPumpSwitchState(self):
        return self.pumpSwitchState

    def getTargetTempState(self):
        return self.target_temperature
