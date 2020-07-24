import smbus
from time import *

class i2c_device:
    def __init__(self, addr, num=0):
        self.addr = addr
        self.bus = smbus.SMBus(num)
        self.i2cErrors = 0		

    # Write a single command
    def write_cmd(self, cmd):
        try:
            self.bus.write_byte(self.addr, cmd)
        except:
            self.i2cErrors += 1
            print("Failed to write over i2c:{0}".format(self.addr))
        sleep(0.0001)

    # Write a command and argument
    def write_cmd_arg(self, cmd, data):
        try:
            self.bus.write_byte_data(self.addr, cmd, data)
        except:
            self.i2cErrors += 1
            print("Failed to write over i2c:{0}".format(self.addr))
        sleep(0.0001)

    # Write a block of data
    def write_block_data(self, cmd, data):
        try:
            self.bus.write_i2c_block_data(self.addr, cmd, data)
        except:
            self.i2cErrors += 1
            print("Failed to write block over i2c:{0}".format(self.addr))
        sleep(0.0001)

    # Read a single byte
    def read(self):
        try:
            rtrn = self.bus.read_byte(self.addr)
        except:
            self.i2cErrors += 1
            print("Failed to read over i2c:{0}".format(self.addr))
            rtrn = 0
        return rtrn

    # Read 
    def read_data(self, cmd):
        try:
            rtrn = self.bus.read_byte_data(self.addr, cmd)
        except:
            self.i2cErrors += 1
            print("Failed to read over i2c:{0}".format(self.addr))
            rtrn = 0
        return rtrn

    # Read a block of data
    def read_block_data(self, cmd):
        try:
            rtrn = self.bus.read_i2c_block_data(self.addr, cmd)
        except:
            self.i2cErrors += 1
            print("Failed to read block over i2c:{0}".format(self.addr))
            rtrn = 0
        return rtrn

    def getErrors(self):
        return self.i2cErrors