import socket
import time
import ubinascii
import encode
import pycom
import machine
from network import LoRa
from SI7006A20 import SI7006A20 #Temperature/Humidity sensor
from pycoproc import Pycoproc

pycom.heartbeat(False)

CYCLE_SEND_INTERVAL = 4
SLEEP_DURATION = 10

try:
    cycle_num = pycom.nvs_get("cycle_num")
except ValueError:
    cycle_num = 0

if cycle_num == (CYCLE_SEND_INTERVAL - 1):
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

    data = bytes()
    for i in range((CYCLE_SEND_INTERVAL // 4) + 1):
        data = data + pycom.nvs_get("data_" + str(i))
        pycom.nvs_erase("data_" + str(i))

    s.send(data)
    lora.nvram_save()

else:
    pycp = Pycoproc()
    si = SI7006A20(pycp) #temperature / humiditiy
    temp = si.temperature()
    encoded_temp = encode.float_to_fixed_point(temp, min_size=2, max_size=2)
    int_encoded = encode.byte_array_to_int(encoded_temp)

    nvs_loc = cycle_num // 4
    nvs_byte_pos = (cycle_num % 4) * 2
    try:
        dat = pycom.nvs_get("data_" + str(nvs_loc))
    except ValueError:
        dat = 0
    dat = dat | (int_encoded << (nvs_byte_pos * 8))
    pycom.nvs_set("data_" + str(nvs_loc), dat)

cycle_num = (cycle_num + 1) % CYCLE_SEND_INTERVAL
pycom.nvs_set("cycle_num", cycle_num)

pycp.setup_sleep(SLEEP_DURATION)
pycp.go_to_sleep(False)