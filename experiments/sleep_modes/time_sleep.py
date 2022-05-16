import pycom
import time
import math

pycom.heartbeat(False)

while True:
    i = 0
    while i < 100_000:
        i += 1

    time.sleep(3) #Sleep for 3 seconds
    
