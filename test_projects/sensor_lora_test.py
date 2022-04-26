import time
import pycom
import machine

from pycoproc_2 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01

from network import LoRa
import socket
import time
import ubinascii

import encode

#Disable blinking LED
pycom.heartbeat(False)

#Configure LoRa connection parameters and join network
pycom.rgbled(0x070000) # red
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("Joining LoRa", end="")
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
while not lora.has_joined():
    time.sleep(2.5)
    print('.', end="")

print('\nSuccessfully joined LoRa network.')
pycom.rgbled(0x000700) # green

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

#Configure the temperature module
pycoproc = Pycoproc()
si = SI7006A20(pycoproc)
temp = si.temperature()
encoded_temp = encode.float_to_fixed_point(temp, 4)
print("Temperature is: ", temp, "ºC")
print("Sending:", encoded_temp)

s.send(encoded_temp)
