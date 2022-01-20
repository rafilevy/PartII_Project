import time
import pycom

#Disable LED blink
pycom.heartbeat(False)

while True:
    pycom.rgbled(0xff0000)
    time.sleep(0.5)
    pycom.rgbled(0)
    time.sleep(0.5)