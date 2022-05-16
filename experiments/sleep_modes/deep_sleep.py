import time
import pycom
import machine

pycom.heartbeat(False)
pycom.heartbeat_on_boot(False)

time.sleep(0.5)
pycom.rgbled(0x007700)
time.sleep(0.5)
pycom.rgbled(0)
time.sleep(0.5)

machine.deepsleep(30 * 1000)