import time
import ubinascii
import encode
import pycom
import machine
from network import LoRa


SENDING_INTERVAL = 10 #Interval at which to send data messages to the server, (seconds)

#Disable LED blink
pycom.heartbeat(False)


#Configure LoRa connection parameters and join network
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

t1 = time.ticks_ms()
print(str(t1) + ": Joining LoRaWAN")
while not lora.has_joined():
    try:
        lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=30_000)
    except OSError:
        t3 = time.ticks_ms()
        print(str(t3) + ": Timeout joining LoRaWAN")
        pass

t2 = time.ticks_ms()
dt = t2 - t1
print(str(t2) + ": Joined LoRaWAN in time=" + str(dt))

machine.deepsleep(SENDING_INTERVAL * 1_000)
