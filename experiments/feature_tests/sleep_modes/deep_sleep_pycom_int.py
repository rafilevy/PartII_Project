import time
import pycom
from pycoproc import Pycoproc

pycom.heartbeat(False)
pycom.heartbeat_on_boot(False)

time.sleep(0.5)
pycom.rgbled(0x007700)
time.sleep(0.5)
pycom.rgbled(0)
time.sleep(0.5)

pycp = Pycoproc()
pycp.setup_sleep(30)
pycp.go_to_sleep(pycom_module_off=True)