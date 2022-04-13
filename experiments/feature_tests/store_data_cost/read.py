import time
import pycom
from random import randint_32

#Disable LED blink
pycom.heartbeat(False)

for i in range(10):
    for j in range(10*(i+1)):
        key = str(i) + "-" + str(j)
        pycom.nvs_set(key, randint_32())

while True:
    for i in range(10):
        for j in range(10*(i+1)):
            key = str(i) + "-" + str(j)
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
