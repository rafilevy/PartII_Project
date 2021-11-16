"""
Collects all sensor data and sends it via LoraWan at 1 minute intervals

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
import machine

from network import LoRa
from pycoproc import Pycoproc
from SI7006A20 import SI7006A20 #Temperature/Humidity sensor
from MPL3115A2 import PRESSURE, ALTITUDE, MPL3115A2 #Altitude/Pressure sensor
from LTR329ALS01 import LTR329ALS01

SENDING_INTERVAL = 60 #Interval at which to send data messages to the server, (seconds)

#Disable LED blink
pycom.heartbeat(False)

#Configure LoRa connection parameters and join network
pycom.rgbled(0x070000) # LED red
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("Joining LoRa", end="")
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
tries = 0
while not lora.has_joined():
    time.sleep(2.5)
    print('.', end="")
    tries += 1
    if tries > 8:
        machine.reset()

print('\nSuccessfully joined LoRa network.')
pycom.rgbled(0x000007) # LED blue

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

pycom.rgbled(0x000700) #LED green

#Configure temperature sensor
pycoproc = Pycoproc()
si = SI7006A20(pycoproc) #temperature / humiditiy
mpl = MPL3115A2(pycoproc, mode=PRESSURE) #altitude / pressure
ltr = LTR329ALS01(pycoproc)

temp = si.temperature()
humidity = si.humidity()
pressure = mpl.pressure()
illuminance = ltr.lux()
print(temp)
print(humidity)
print(pressure)
print(illuminance)

encoded_temp = encode.float_to_fixed_point(temp, 8, max_size=2)
encoded_humidity = encode.float_to_fixed_point(humidity, 1, max_size=1)
encoded_pressure = encode.float_to_fixed_point(pressure, 0, max_size=3)
encoded_illuminance = encode.float_to_fixed_point(illuminance, 0, max_size=2)

s.send(encoded_temp + encoded_humidity + encoded_pressure + encoded_illuminance)
print("Successfully sent")
print()
machine.deepsleep(SENDING_INTERVAL * 1000)