"""
Config 2: machine.sleep idle
This config uses machine.sleep to go into a light sleep between sending data
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
import machine

from network import LoRa



SENDING_INTERVAL = 10 #Interval at which to send data messages to the server, s

#Disable LED blink
pycom.heartbeat(False)


#Configure LoRa connection parameters and join network
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
s.setblocking(True)


#Main sending loop
while True:
    time.sleep(0.5)

    temp = 26.291
    encoded_temp = encode.float_to_fixed_point(temp, 5)


    s.send(encoded_temp)

    machine.sleep(SENDING_INTERVAL * 1000)