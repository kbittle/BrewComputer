import hw_lib.serial_io_lib as serial_io_lib
import os

class arduinoWaterLevel:
    def __init__(self):
        # Initialize comm lass vars
        self.commLoss = True
        self.commLossCountdown = 0

        # Assign serial port data
        if (os.name == 'nt'):
            self.portNum = 'COM9'
        else:
            self.portNum = '/dev/ttyUSB1'

        self.baudrate = 9600

        # Open serial port
        self.serial = serial_io_lib.SerialInterface(False, self.portNum, self.baudrate)
        self.serial.openPort()

        # If we were able to find the serial port
        if self.serial.isPortOpen():
            # Start thread to read serial port
            self.serial._start_reader()

    # Decode Serial packet and pull switch settings and target temp
    def decode_packet(self, packet):
        
        # Ensure at least 1 packet has been recieved
        if not packet:
            print(">> WLS Packet is null")
            return
        
        # Ensure its the correct pack, at this time there is only
        # one packet.
        if packet[0] == 1:
            print("Received packet")
               
    def doWork(self):
        if self.serial.isPortOpen():
            # Decode latest serial packet to determine target temp
            packet = self.serial.get_latest_packet()
            self.decode_packet(packet)

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
                print("Comm Loss with Water Level Sensor")

    def close(self):
        self.serial._stop_reader()

    def getCommStatus(self):
        return self.commLoss
