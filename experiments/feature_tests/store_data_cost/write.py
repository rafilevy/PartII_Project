import time
import pycom
from random import randint_32

#Disable LED blink
pycom.heartbeat(False)
pycom.nvs_erase_all()
while True:
    for i in range(5):
        for j in range(20*(i+1)):
            key = str(i) + "-" + str(j)
            pycom.nvs_set(key, randint_32())
        
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
