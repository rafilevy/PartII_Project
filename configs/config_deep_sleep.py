"""
Config Wake Sleep

Randomly chooses wether to send the data or go back to sleep
"""

import socket
import time
import ubinascii
import encode
import pycom
import machine

from network import LoRa

pycom.heartbeat(False)
pycom.heartbeat_on_boot(False)

pycom.rgbled(0x00ff00) #LED green
time.sleep(0.5)
pycom.rgbled(0)
time.sleep(0.5)

machine.deepsleep(30 * 1000)