from __future__ import print_function
import BlynkLib
from time import *

BLYNK_AUTH = 'p8nCrE5Ttk4a-hU61r0NpNgWhQFHLibR'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    print('Current V1 value: {}'.format(value))

@blynk.ON("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')

@blynk.ON("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')

@blynk.ON("V*")
def blynk_handle_vpins(pin, value):
    print("V{} value: {}".format(pin, value))

@blynk.ON("readV*")
def blynk_handle_vpins_read(pin):
    print("Server asks a value for V{}".format(pin))
    blynk.virtual_write(pin, 0)

while True:
    blynk.run()
    sleep(5)
