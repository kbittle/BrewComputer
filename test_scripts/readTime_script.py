import hw_lib.ds1307_lib as ds1307_lib
from time import *

# Load Library
real_time = ds1307_lib.ds1307()

print "Current Time = " + real_time.getDateDs1307Str()

