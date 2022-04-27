import time
import pycom
from random import randint_32

#Disable LED blink
pycom.heartbeat(False)

while True:
    time.sleep(5)
    for i in range(5):
        for j in range(50*(i+1)):
            key = str(j)
            result = pycom.nvs_get(key)
        
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
