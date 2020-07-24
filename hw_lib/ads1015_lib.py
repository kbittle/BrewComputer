import i2c_lib.i2c_lib as i2c_lib

# ADS1015 i2c address
ADS1015_I2C_ADDRESS = 0x48

# ADS1015 Registers
ADS1015_CONFIG_REGISTER = 0x01
ADS1015_POINTER_REGISTER = 0x00

# ADS1015 Config Register(16-bit)
ADS1015_CONFIG_BEGIN_CONVERSION	= 0x8000	
ADS1015_CONFIG_INPUT_MUX_0 = 0x4000
ADS1015_CONFIG_INPUT_MUX_1 = 0x5000	
ADS1015_CONFIG_INPUT_MUX_2 = 0x6000
ADS1015_CONFIG_INPUT_MUX_3 = 0x7000
ADS1015_CONFIG_MODE_CONTINUOUS= 0x0000
ADS1015_CONFIG_MODE_SINGLE_SHOT	= 0x0100
ADS1015_CONFIG_DR_1600SPS = 0x0080
ADS1015_CONFIG_DISABLE_COMPARATOR = 0x0003

class ads1015:
    def __init__(self):
        self.device = i2c_lib.i2c_device(ADS1015_I2C_ADDRESS)

    def write_config(self, input_port=0):
        
        config_data_buildr = 0;
        config_data_buildr += ADS1015_CONFIG_BEGIN_CONVERSION
        
        if input_port == 0:
            config_data_buildr += ADS1015_CONFIG_INPUT_MUX_0
        elif input_port == 1:
            config_data_buildr += ADS1015_CONFIG_INPUT_MUX_1
        elif input_port == 2:
            config_data_buildr += ADS1015_CONFIG_INPUT_MUX_2
        elif input_port == 3:
            config_data_buildr += ADS1015_CONFIG_INPUT_MUX_3
        else:
            return
            
        config_data_buildr += ADS1015_CONFIG_MODE_CONTINUOUS
        config_data_buildr += ADS1015_CONFIG_MODE_SINGLE_SHOT
        config_data_buildr += ADS1015_CONFIG_DR_1600SPS
        config_data_buildr += ADS1015_CONFIG_DISABLE_COMPARATOR

       # self.device.write_cmd(ADS1015_CONFIG_REGISTER)

        config_block = [(config_data_buildr >> 8 & 0xFF),(config_data_buildr & 0xFF)]
        self.device.write_block_data(ADS1015_CONFIG_REGISTER, config_block)

    def read_ADC_value(self, input_port=0):
        #Configure ADS1015 to read from the correct input
        self.write_config(input_port)
        
        #Read from the  pointer register, where the conversion is stored
        self.device.write_cmd(ADS1015_POINTER_REGISTER)

        byte1 = self.device.read()
        byte2 = self.device.read()
        return (byte1 << 4) + (byte2 >> 4)
    
    def read_ADC_block(self, input_port=0):
        #Configure ADS1015 to read from the correct input
        self.write_config(input_port)

        #Read from the  pointer register, where the conversion is stored
	blk = [0,0]
	blk = self.device.read_block_data(ADS1015_POINTER_REGISTER)
             
	return (blk[0] << 4) + (blk[1] >> 4)
