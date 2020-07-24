import ds2482_lib
from time import *

# DS18B20 ROM Command
SEARCH_ROM = 0xF0
READ_ROM = 0x33
MATCH_ROM = 0x55
SKIP_ROM = 0xCC

# DS18B20 Function Command
CONVERT_T = 0x44
READ_SCRATCHPAD = 0xBE
WRITE_SCRATCHPAD = 0x4E
COPY_SCRATCHPAD = 0x48
RECALL_E = 0xB8
READ_POWER_SUPPLY = 0xB4

crctab = [
    0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
    157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
    35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
    190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
    70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
    219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
    101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
    248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
    140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
    17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
    175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
    50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
    202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
    87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
    233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
    116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53]

class ds18b20: 
    def __init__(self, smbusNum):
        self.sensor = ds2482_lib.ds2482(smbusNum)
        self.scratchpad = []
        self.ROM_ADDRESS = []
        self.LastDiscrepancy = 0
        self.LastFamilyDiscrepancy = 0
        self.LastDeviceFlag = False
        
    def calc_crc(self, *args):
        accum = 0
        args = list(args)[0]
        for x in args:
            accum = crctab[accum ^ x]
        return accum        

    # Scratchpad Memory Mapping
    # Temp LSB
    # Temp MSB
    # T(H) Reg
    # T(L) Reg
    # Configuration Reg
    # Reserved
    # Reserved
    # Reserved
    # CRC
    def read_temp_single_sensor(self):
        self.sensor.busReset()
        self.sensor.busWriteByte(SKIP_ROM)
        self.sensor.busWriteByte(CONVERT_T)
        
        sleep(0.5) # Time needed to Convert, 750ms Max
        
        self.sensor.busReset()
        self.sensor.busWriteByte(SKIP_ROM)
        self.sensor.busWriteByte(READ_SCRATCHPAD)

        for c in range (9):
            self.scratchpad.append(self.sensor.busReadByte())        

        # Check CRC value
        if self.calc_crc(self.scratchpad) == 0:
            temp_reading = ((self.scratchpad[1] << 8) | self.scratchpad[0]) / 16
        else:
            temp_reading = 0
            #print "CRC ERROR"
        
        return temp_reading
    
    def Search_ROM(self):        
        self.ROM_ADDRESS = [0] * 8
        id_bit_number = 1
        last_zero = 0
        rom_byte_number = 0
        rom_byte_mask = 1
        search_result = False        
        search_direction = 0

        if not(self.LastDeviceFlag):
            if not self.sensor.busReset():
                self.LastDiscrepancy = 0
                self.LastFamilyDiscrepancy = 0
                self.LastDeviceFlag = False
                return False
                
            self.sensor.busWriteByte(SEARCH_ROM)
        
            while rom_byte_number < 8:
                if (id_bit_number < self.LastDiscrepancy):
                    if((self.ROM_ADDRESS[rom_byte_number] & rom_byte_mask) > 0):
                        search_direction = 1
                    else:
                        search_direction = 0
                else:
                    if (id_bit_number == self.LastDiscrepancy):
                        search_direction = 1
                    else:
                        search_direction = 0
                        
                read_status_bits = self.sensor.busTriplet(search_direction)
            
                id_bit = (read_status_bits & 1)
                comp_id_bit = int((read_status_bits & 2) == 2)
                search_direction = int((read_status_bits & 4) == 4)
            
                if (id_bit == 1) and (comp_id_bit == 1):
                    break 
                else:
                    if (id_bit == 0) and (comp_id_bit == 0) and (search_direction == 0):
                        last_zero = id_bit_number
                        if (last_zero < 9):
                            self.LastFamilyDiscrepancy = last_zero 
                            
                    if (search_direction == 1):
                        self.ROM_ADDRESS[rom_byte_number] |= rom_byte_mask
                    else:
                        self.ROM_ADDRESS[rom_byte_number] &= ~rom_byte_mask
       
                    id_bit_number += 1
                    rom_byte_mask *= 2

                    if (rom_byte_mask > 0x80):
                        rom_byte_number += 1
                        rom_byte_mask = 1

            if not(id_bit_number < 65):
                self.LastDiscrepancy = last_zero
                if (self.LastDiscrepancy == 0):
                    self.LastDeviceFlag = True
                search_result = True

            if not(search_result) or (self.ROM_ADDRESS[0] == 0):
                self.LastDiscrepancy = 0
                self.LastDeviceFlag = False
                self.LastFamilyDiscrepancy = 0
                search_result = False
            
        return search_result
            
    def Read_ROM(self):
        self.ROM_ADDRESS = []
        self.sensor.busReset()
        self.sensor.busWriteByte(READ_ROM)
        
        for c in range (8):
            self.ROM_ADDRESS.append(self.sensor.busReadByte())
        return self.ROM_ADDRESS

    def Match_ROM(self, ROM_ADDRESS):
        self.sensor.busReset()
        self.sensor.busWriteByte(MATCH_ROM)
        
        for c in range (8):
            self.sensor.busWriteByte(ROM_ADDRESS[c])
            
    def Print_ROM(self):
        print self.ROM_ADDRESS

    def Sensor_Convert(self, ROM_ADDRESS):        
        self.sensor.busReset()
        self.Match_ROM(ROM_ADDRESS)
        self.sensor.busWriteByte(CONVERT_T)
        
    def Sensor_Read_Temp(self, ROM_ADDRESS):
        self.scratchpad = [] # reset scratchpad
        raw_temp = 0
        temp_c = 0
        temp_f = 0
        
        self.sensor.busReset()
        self.Match_ROM(ROM_ADDRESS)
        self.sensor.busWriteByte(READ_SCRATCHPAD)

        for c in range (9):
            self.scratchpad.append(self.sensor.busReadByte())

        # Check CRC value
        if self.calc_crc(self.scratchpad) == 0:
            raw_temp = ((self.scratchpad[1] << 8) | self.scratchpad[0])
            temp_c = (raw_temp >> 4) & 0x00FF 
            if(raw_temp & 0x0001)==0x0001:
                temp_c += 0.06250
            if(raw_temp & 0x0002)==0x0002:
                temp_c += 0.12500
            if(raw_temp & 0x0004)==0x0004:
                temp_c += 0.25000
            if(raw_temp & 0x0008)==0x0008:
                temp_c += 0.50000
            temp_f = (temp_c * 9/5) + 32
        
        return temp_f

    def Sensor_Recall_EE(self, ROM_ADDRESS):
        self.sensor.busReset()
        self.Match_ROM(ROM_ADDRESS)
        self.sensor.busWriteByte(RECALL_E)

    def Sensor_Read_Power_Supply(self, ROM_ADDRESS):
        self.sensor.busReset()
        self.Match_ROM(ROM_ADDRESS)
        self.sensor.busWriteByte(READ_POWER_SUPPLY)
        return self.sensor.busReadByte()

    def Test(self):
        addr = []
        counter = 0

        self.sensor.busConfigure("SPU")

        while (self.Search_ROM() and (counter < 10)):
            counter += 1

            if self.ROM_ADDRESS not in addr:
                addr.append(self.ROM_ADDRESS)

        print addr

        for ra in addr:
            self.Sensor_Convert(ra)

        sleep(0.5)

        for rb in addr:
            print (float(self.Sensor_Read_Temp(rb)) * 9/5) + 32
            print self.scratchpad

    def getI2cErrors(self):
        return self.sensor.getI2cErrors()
