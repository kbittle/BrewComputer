import os, serial, threading
import serial_io_lib
from time import *

inter = serial_io_lib.SerialInterface()
inter._start_reader()

sleep(1)

packet = inter.get_latest_packet()
print packet

sleep(1)

packet = inter.get_latest_packet()
print packet

if not packet:
	print "enpty packet"

if packet[0] == 15:
	print "found delimeter"
sleep(1)

inter._stop_reader()

print "exited.."
