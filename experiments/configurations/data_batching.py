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

pycom.heartbeat(False)

BATCH_SIZE = 4
MESSAGE_INTERVAL = 10

#Join the LoRaWAN network and return the lora object.
def join_lorawan():
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
    return lora

#Get the number of messages which have been batched but not sent
try:
    cycle_num = pycom.nvs_get("cycle_num")
except ValueError:
    cycle_num = 0

#Take a temperature measurement
pycp = Pycoproc()
si = SI7006A20(pycp) #temperature / humiditiy
temp = si.temperature()
encoded_temp = encode.float_to_fixed_point(temp, min_size=2, max_size=2)

if cycle_num == (BATCH_SIZE - 1): #Batch size reached, send batched measurements
    data = bytes()
    for i in range(BATCH_SIZE - 1):
        t = pycom.nvs_get("data_" + str(i))
        data += encode.int_to_byte_array(t, 2)
    data += encoded_temp

    lora = join_lorawan()
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setblocking(True)
    s.send(data)
    lora.nvram_save()
else: #Batch size not yet reached Save measured data to NVRAM
    int_encoded = encode.byte_array_to_int(encoded_temp)
    pycom.nvs_set("data_" + str(cycle_num), int_encoded)

#Update number of messages which have been batched 
cycle_num = (cycle_num + 1) % BATCH_SIZE
pycom.nvs_set("cycle_num", cycle_num)

#Calculate sleep time from timer and enter deep sleep
chrono.stop()
elapsed = chrono.read() + 1 #1 accounts for about 1s of wakeup time.
pycp.setup_sleep(MESSAGE_INTERVAL - elapsed)
pycp.go_to_sleep(False)