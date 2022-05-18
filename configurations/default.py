import socket
import time
import ubinascii
import encode
import pycom
from machine import Timer
from network import LoRa
from SI7006A20 import SI7006A20 #Temperature/Humidity sensor
from pycoproc import Pycoproc

#Start timer
chrono = Timer.Chrono()
chrono.start()

MESSAGE_INTERVAl = 30 #Interval at which to send data messages to the server, (seconds)

#Disable LED blink
pycom.heartbeat(False)


#Configure LoRa connection parameters and join network
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
lora.nvram_restore()

if not lora.has_joined():
    print("Rejoining LoRa")
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    while not lora.has_joined():
        print("Attempting to join...")
        time.sleep(2)
else:
    print('Restored saved connection')


# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

pycp = Pycoproc()

si = SI7006A20(pycp) #temperature / humiditiy
temp = si.temperature()

encoded_temp = encode.float_to_fixed_point(temp, 5)

s.send(encoded_temp)

lora.nvram_save()

chrono.stop()
elapsed = chrono.read() + 1 #1 accounts for about 1s of wakeup time.
pycp.setup_sleep(MESSAGE_INTERVAl)
pycp.go_to_sleep(False)