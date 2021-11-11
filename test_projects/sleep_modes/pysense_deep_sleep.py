from pycoproc import Pycoproc
import time
import pycom

pycom.heartbeat(False)
pycom.rgbled(0x000700) #Green LED
print("Awoken from sleep")
time.sleep(3) #idle for 3 seconds

pysense = Pycoproc()
pysense.setup_sleep(3)
print("Going into deep sleep for 3 seconds")
pysense.go_to_sleep()

print("This should never be printed...")