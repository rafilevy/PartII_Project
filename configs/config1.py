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
import ubinascii
import encode
import pycom

from network import LoRa

SENDING_INTERVAL = 10 #Interval at which to send data messages to the server, s

#Disable LED blink
pycom.heartbeat(False)

app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("Joining LoRa", end="")
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
while not lora.has_joined():
    time.sleep(2.5)
    print('.', end="")

print('\nSuccessfully joined LoRa network.')

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)

#Main sending loop
while True:
    temp = 27.96
    encoded_temp = encode.float_to_fixed_point(temp, 5)

    time.sleep(0.5)
    pycom.rgbled(0x00ff00) #LED green
    time.sleep(0.5)
    pycom.rgbled(0)
    time.sleep(0.5)

    s.send(encoded_temp)
    
    time.sleep(0.5)
    pycom.rgbled(0x00ff00) #LED green
    time.sleep(0.5)
    pycom.rgbled(0)
    time.sleep(0.5)

    time.sleep(SENDING_INTERVAL)