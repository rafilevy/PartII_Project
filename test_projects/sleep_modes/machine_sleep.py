import machine
import pycom
import time

pycom.heartbeat(False)

while True:
    pycom.rgbled(0x000700) #Green LED
    print("Awoken from sleep")
    time.sleep(3) #Idle for 3 seconds

    pycom.rgbled(0x070000) #Red LED
    print("Going to sleep")
    machine.sleep(1000*3) #Sleep for 3 seconds
    
