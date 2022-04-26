import machine
import pycom
import time

pycom.heartbeat(False)

while True:
    time.sleep(0.5)
    pycom.rgbled(0x007700)
    time.sleep(0.5)
    pycom.rgbled(0)
    time.sleep(0.5)
    
    machine.sleep(1000*3) #Sleep for 3 seconds
    
