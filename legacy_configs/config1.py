"""
Config 1: time.sleep idle
This config uses time.sleep to idle between sending data
It sends it's temperature data to the server at a specified interval 

LED KEY:
    RED - Connecting to LORA
    BLUE - Idle
    GREEN - Sending data
"""

import socket
import time
from ubinascii import unhexlify
import encode
import pycom
import struct
from network import LoRa


SENDING_INTERVAL = 30 #Interval at which to send data messages to the server, s

#Disable LED blink
pycom.heartbeat(False)

dev_addr = struct.unpack(">l", unhexlify("260BCA4A"))[0]
app_swkey = unhexlify("3F84C8BD492EBEBD3E47FF4588F31EF7")
nwk_swkey = unhexlify("060B0AA9631D10A05A7253AA6198B244")

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('\nSuccessfully joined LoRa network.')

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

#Main sending loop
while True:
    temp = 27.96
    encoded_temp = encode.float_to_fixed_point(temp, 5)
 
    time.sleep(0.5)
    pycom.rgbled(0x00ff00) #LED green
    time.sleep(0.5)
    pycom.rgbled(0)
    time.sleep(0.5)

    s.setblocking(True)

    s.send(encoded_temp)

    s.setblocking(False)
    
    time.sleep(0.5)
    pycom.rgbled(0x00ff00) #LED green
    time.sleep(0.5)
    pycom.rgbled(0x00ff00) #LED green
    time.sleep(0.5)
    pycom.rgbled(0)
    time.sleep(0.5)

    time.sleep(SENDING_INTERVAL)