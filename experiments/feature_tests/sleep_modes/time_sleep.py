import pycom
import time
import math

pycom.heartbeat(False)

while True:
    for i in range(10_000):
        x = math.sqrt(float(i))

    time.sleep(3) #Sleep for 3 seconds
    
