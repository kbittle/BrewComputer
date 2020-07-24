import hw_lib.i2c_lib.i2c_lib as i2c_lib
from datetime import datetime

# DS1307 i2c address
ADDRESS = 0x68

#Starting Adress of 0x00
DS1307_CMD = 0x00

class ds1307:
    def __init__(self, smbusNum):
        self.device = i2c_lib.i2c_device(ADDRESS, smbusNum)
        self.second = 0
        self.minute = 0
        self.hour = 0
        self.dayOfWeek = 0
        self.dayOfMonth = 0
        self.month = 0
        self.year = 0

    def start_clock(self):
        self.device.write_cmd_arg(DS1307_CMD, 0x00)

    def stop_clock(self):
        self.device.write_cmd_arg(DS1307_CMD, 0x80)

    def clock_status(self):
        self.device.write_cmd(DS1307_CMD)
        return (self.device.read() >> 7)

    def decToBcd(self, val):
        return val+6*(val/10)
        #return ((val/10*16) + (val%10))
    
    def bcdToDec(self, val):
        return val-6*(val>>4)
        #return ((val/16*10) + (val%16))

    def setDateDs1307(self, second, minute, hour, dayOfWeek, dayOfMonth, month, year):
	   #Ensure the block data is in the correct order liek this.
        time_block_data = [(self.decToBcd(second)),(self.decToBcd(minute)),(self.decToBcd(hour)),(self.decToBcd(dayOfWeek)),(self.decToBcd(dayOfMonth)),(self.decToBcd(month)),(self.decToBcd(year))]
        self.device.write_block_data(DS1307_CMD, time_block_data)

       #Probably dont need to do this, but were overwriting the seconds, may try removing
        self.device.write_cmd_arg(DS1307_CMD, (self.decToBcd(second) & 0x7F))

    def getDateDs1307Str(self):
        self.device.write_cmd(DS1307_CMD)
        self.second = self.bcdToDec(self.device.read() & 0x7f)
        self.minute = self.bcdToDec(self.device.read())
        self.hour = self.bcdToDec(self.device.read() & 0x3f)
        self.dayOfWeek = self.bcdToDec(self.device.read())
        self.dayOfMonth = self.bcdToDec(self.device.read())
        self.month = self.bcdToDec(self.device.read())
        self.year = self.bcdToDec(self.device.read())
        
        return "{0}/{1}/20{2} {3}:{4}:{5}".format(self.month, self.dayOfMonth, self.year, self.hour, self.minute, self.second)
        
    # Get in datetime format
    def getDateDs1307(self):
        tmpStr = self.getDateDs1307Str()
        return datetime.strptime(tmpStr,"%m/%d/%Y %H:%M:%S")

    def getI2cErrors(self):
        return self.device.getErrors()