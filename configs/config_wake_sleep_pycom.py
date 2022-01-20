"""
Config Wake Sleep

Randomly chooses wether to send the data or go back to sleep
"""

import time
import pycom
from pycoproc import Pycoproc

#Disable LED blink
pycom.heartbeat(False)
pycom.heartbeat_on_boot(False)
pycom.wifi_on_boot(False)

pycom.rgbled(0x007700)
time.sleep(0.5)
pycom.rgbled(0)
time.sleep(5)

pycp = Pycoproc()
pycp.setup_sleep(30)
pycp.go_to_sleep()