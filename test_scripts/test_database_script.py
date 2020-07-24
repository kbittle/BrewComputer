import interfaces.sql_database_lib as sql_database_lib
from time import *

# Load Library
db_lib = sql_database_lib.sql_database_lib()

ROM1 = [0x28,0xAD,0xCA,0x2B,0x04,0x00,0x00,0xED]
ROM2 = [0x28,0xA3,0xF6,0x2A,0x04,0x00,0x00,0xD4]
ROM3 = [0x28,0x80,0x49,0x2B,0x04,0x00,0x00,0x94]

print "Before adding sensors {0}".format(ROM1)

db_lib.add_sensor_to_db(ROM1, "test1")
db_lib.add_sensor_to_db(ROM2, "test2")
db_lib.add_sensor_to_db(ROM3, "test3")
db_lib.add_sensor_to_db(ROM1, "test4")

print "Before first print"

db_lib.print_everything()

print "Before first update"

db_lib.update_temperature(1,65)

db_lib.print_everything()

print "Before second update"

db_lib.update_temperature(1,11)
db_lib.update_temperature(2,22)
db_lib.update_temperature(3,33)

db_lib.print_everything()
