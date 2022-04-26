import socket
import time
import ubinascii
import encode
import pycom
import machine

from random import rand_byte
from network import LoRa

#Disable LED blink
pycom.heartbeat(False)

#Configure LoRa connection parameters and join network
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')


from network import LoRa
import socket
import ubinascii
import struct

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

dev_addr = struct.unpack(">l", ubinascii.unhexlify('260B26B8'))[0]
nwk_swkey = ubinascii.unhexlify('CFD2E8E7A6B86130F896DADE6495CB5D')
app_swkey = ubinascii.unhexlify('FBB6FBD7EC975D517A94CA5268C010C4')
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)

while True:
    for i in range(10):
        s.send( bytes([rand_byte() for _ in range((i+1) * 10)] ) )

        #Flash LED green and sleep for .5 seconds either side
        time.sleep(0.5)
        pycom.rgbled(0x007700) 
        time.sleep(0.5)
        pycom.rgbled(0)
        time.sleep(0.5)

    #Flash LED blue to indicate restarting, sleep for 5 seconds after
    time.sleep(0.5)
    pycom.rgbled(0x000077) 
    time.sleep(0.5)
    pycom.rgbled(0)
    time.sleep(5)
