import pycom
import time
import machine

pycom.heartbeat(False)
pycom.rgbled(0x000700) #Green LED
print("Awoken from sleep")
time.sleep(3) #idle for 3 seconds

print("Going into deep sleep for 3 seconds")
machine.deepsleep(1000 * 3)

print("This should never be printed...")