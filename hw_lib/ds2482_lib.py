import i2c_lib.i2c_lib as i2c_lib

# DS2482-100 i2c address
ADDRESS = 0x18

# DS2482-100 Commands
DEVICE_RESET = 0xF0
SET_READ_POINTER = 0xE1
WRITE_CONFIG = 0xD2
ONE_WIRE_RESET = 0xB4
ONE_WIRE_SINGLE_BIT = 0x87
ONE_WIRE_WRITE_BYTE = 0xA5
ONE_WIRE_READ_BYTE = 0x96
ONE_WIRE_TRIPLET = 0x78

# DS2482-100 Read Pointer Register Codes
STATUS_REGISTER = 0xF0
READ_DATA_REGISTER = 0xE1
CONFIG_REGISTER = 0xC3

# DS2482-100 Config Register Codes
ACTIVE_PULL_UP = 0x01
PRESENSE_PULSE_MASKING = 0x02
STRONG_PULL_UP = 0x04
ONE_WIRE_SPEED = 0x08

# DS2482-100 Status Register Codes
ONE_WIRE_BUSY = 0x01
PRESENCE_PULSE_DETECT = 0x02
SHORT_DETECTED = 0x04
ONE_WIRE_LOGIC_LEVEL = 0x08
DEVICE_RESET = 0x10
SINGLE_BIT_RESULT = 0x20
TRIPLET_SECOND_BIT = 0x40
BRANCH_DIRECTION_TAKEN = 0x80

class ds2482:
    def __init__(self, smbusNum):
        self.device = i2c_lib.i2c_device(ADDRESS, smbusNum)
        
    def busyWait(self):
        self.device.write_cmd_arg(SET_READ_POINTER, STATUS_REGISTER)
        status = self.device.read()
        while ((status & ONE_WIRE_BUSY) == ONE_WIRE_BUSY):
            status = self.device.read()
        return status

    def busReset(self):
        self.device.write_cmd(ONE_WIRE_RESET)
        status = self.busyWait()
        return ((status & PRESENCE_PULSE_DETECT) == PRESENCE_PULSE_DETECT)

    def busWriteByte(self, data):
        self.busyWait()
        self.device.write_cmd_arg(ONE_WIRE_WRITE_BYTE, data)

    def busReadByte(self):
        self.busyWait()
        self.device.write_cmd(ONE_WIRE_READ_BYTE)
        self.busyWait()
        self.device.write_cmd_arg(SET_READ_POINTER, READ_DATA_REGISTER)
        return self.device.read()

    def busSingleBit(self, bit):
        self.busyWait()
        if(bit == 1):
            self.device.write_cmd_arg(ONE_WIRE_SINGLE_BIT, 0x80)
        else:
            self.device.write_cmd_arg(ONE_WIRE_SINGLE_BIT, 0x00)
        status = self.busyWait()
        return ((status & SINGLE_BIT_RESULT) == SINGLE_BIT_RESULT)

    def busTriplet(self, direction):
        self.busyWait()
        if(direction == 1):
            self.device.write_cmd_arg(ONE_WIRE_TRIPLET, 0x80)
        else:
            self.device.write_cmd_arg(ONE_WIRE_TRIPLET, 0x00)
        status = self.busyWait()
        return ((status & (BRANCH_DIRECTION_TAKEN | SINGLE_BIT_RESULT | TRIPLET_SECOND_BIT)) >> 5)

    # APU - Active Pullup
    # SPU - Strong Pullup
    # WS  - 1-Wire Speed
    def busConfigure(self, config):
        self.busyWait()
        if config == "APU":
            self.device.write_cmd_arg(WRITE_CONFIG, 0xE1)
        elif config == "SPU":
            self.device.write_cmd_arg(WRITE_CONFIG, 0xB4)
        elif config == "WS":
            self.device.write_cmd_arg(WRITE_CONFIG, 0x78)

    def getI2cErrors(self):
        return self.device.getErrors()
