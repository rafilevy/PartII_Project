"""
Config 4: pysense deepsleep
This config uses the deep sleep from the pycoproc library to have the pysense shield
    put the lopy into a deep sleep between sending data
It sends it's temperature data to the server at a specified interval 

LED KEY:
    RED - Connecting to LORA
    OFF - Sleeping
    GREEN - Sending data
"""

import socket
import time
import ubinascii
import encode
import pycom

from network import LoRa
from pycoproc import Pycoproc
# from SI7006A20 import SI7006A20 #Temperature/Humidity sensor


SENDING_INTERVAL = 60 #Interval at which to send data messages to the server, (seconds)

#Disable LED blink
pycom.heartbeat(False)


#Configure LoRa connection parameters and join network
# pycom.rgbled(0x070000) # LED red
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("Joining LoRa", end="")
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
while not lora.has_joined():
    time.sleep(2.5)
    print('.', end="")

print('\nSuccessfully joined LoRa network.')
# pycom.rgbled(0x000007) # LED blue

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

#Configure temperature sensor
pycoproc = Pycoproc()
# si = SI7006A20(pycoproc)

# pycom.rgbled(0x000700) #LED green
# temp = si.temperature()
temp = 26.221
encoded_temp = encode.float_to_fixed_point(temp, 5)
print("Temperature:", str(temp) + "ºC")
print("Sending:", encoded_temp)
s.send(encoded_temp)
print("Successfully sent")
print()

pycoproc.setup_sleep(SENDING_INTERVAL)
pycoproc.go_to_sleep()