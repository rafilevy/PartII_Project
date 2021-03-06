"""
Config 5 - Data prediction and batching 

Config 5 uses a prediction algorithm to predict sensor values in step with the server.
If a prediction is correctly made the data is saved and nothing is sent.
If a prediction fails the device will retreive all the batched data from storage and send this to the server
"""

from platform import machine
import socket
import math
import ubinascii
import encode
import time
import pycom
from machine import Timer
from network import LoRa
from SI7006A20 import SI7006A20 #Temperature/Humidity sensor
from pycoproc import Pycoproc

#Begin timer
chrono = Timer.Chrono()
chrono.start()

MESSAGE_INTERVAL = 30 #Interval at which to send data messages to the server, (seconds)

pycom.heartbeat(False)

pycp = Pycoproc()
si = SI7006A20(pycp) #temperature / humiditiy

#Kalman filter constants, prediction and update functions
Q = 0.
R = 1.
threshold = 0.05

def k_predict(x, P, Q):
    x_ = x
    P_ = P + Q
    return x_, P_

def k_update(z, x, P, R):
    KG = P/(P + R)
    P_ = P * (1 - KG)
    x_ = x + KG*(z - x)
    return x_, P_

#Save and retreive Kalman filter params from non-volatile storage
def save_x_P(key, x, P):
    x_enc = encode.float_to_int(x)
    P_enc = encode.float_to_int(P)
    pycom.nvs_set(key + "_x", x_enc)
    pycom.nvs_set(key + "_P", P_enc)

def retreive_x_P(key):
    try:
        x_bytes = pycom.nvs_get(key + "_x")
        P_bytes = pycom.nvs_get(key + "_P")
    except ValueError as e:
        return None, None
    
    x = encode.int_to_float(x_bytes)
    P = encode.int_to_float(P_bytes)
    return x, P

#Push and pop all data points to non-volatile memory
def push_x_val(key, data_head, x):
    x_enc = encode.float_to_int(x)
    pycom.nvs_set(key + "_INDEX_" + str(data_head), x_enc)
    pycom.nvs_set(key + "_HEAD", data_head+1)

def pop_x_vals(key, data_head):
    x_vals = []
    for i in range(data_head):
        x_enc = pycom.nvs_get(key + "_INDEX_" + str(i))
        x = encode.int_to_float(x_enc)
        x_vals.append(x)
        pycom.nvs_erase(key + "_INDEX_" + str(i))
    pycom.nvs_set(key + "_HEAD", 0)
    return x_vals

#Send data points over LoRaWAN
def send_data(x_vals):
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    lora.nvram_restore()
    if not lora.has_joined():
        print("Rejoining LoRa")
        app_eui = ubinascii.unhexlify('0000000000000000')
        app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')
        lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
        while not lora.has_joined():
            print("Attempting to join...")
            time.sleep(2)
    else:
        print('Restored saved connection')

    # Create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setblocking(True)

    data = bytes()
    for x in x_vals:
        data += encode.float_to_byte_array(x)

    print("Sending {}|{}".format(x_vals, data))
    s.send(data)

    s.setblocking(False)
    lora.nvram_save()

#Take a temperature measurement
z = si.temperature()

try:
    data_head = pycom.nvs_get("TEMP_HEAD")
except ValueError as e:
    data_head = None

print("Data head = {}".format(data_head))

if data_head == None:
    #First run, set head to 0, Save initial values and send first data point to server.
    pycom.nvs_set("TEMP_HEAD", 0)
    save_x_P("Act_x_P", z, 1.)
    save_x_P("Pred_x_P", z, 1.)
    print("Sending value: {}".format(z))
    send_data([z])
else:
    Act_x, Act_P = retreive_x_P("Act_x_P")
    Pred_x, Pred_P = retreive_x_P("Pred_x_P")
    
    x, P   = k_predict(Act_x, Act_P, Q) #Prediction made using actual data values
    x_, P_ = k_predict(Pred_x, Pred_P, Q) #Prediction made using predicted data values
    e_measurement = math.fabs(x_ - z)
    e_cumulative  = math.fabs(x_ - x)

    print("z = {}".format(z))
    print("x_ = {}".format(x_))
    if e_measurement > threshold or e_cumulative > threshold:
        print("Error threshold crossed.")
        #Error threshold was hit, pop all previous data values and send to server
        data = pop_x_vals("TEMP", data_head)
        data.append(z)
        send_data(data)
        #Update both predicted and actual models with all the actual data values
        _, P = k_update(z, Act_x, Act_P, R)
        save_x_P("Act_x_P", z, P)
        save_x_P("Pred_x_P", z, P)
    else:
        #Save actual data value but don't send to server
        push_x_val("TEMP", data_head, z)

        #Update predicted and actual models with predicted and actual data respectively
        _, P = k_update(z, Act_x, Act_P, R)
        _, P_ = k_update(x_, Pred_x, Pred_P, R)
        save_x_P("Act_x_P", z, P)
        save_x_P("Pred_x_P", x_, P_)

#Calculate sleep time and enter deep sleep
chrono.stop()
elapsed = chrono.read() + 1 #1 accounts for about 1s of wakeup time.
print("Sleeping for {}s".format(MESSAGE_INTERVAL - elapsed))
pycp.setup_sleep(MESSAGE_INTERVAL - elapsed)
pycp.go_to_sleep(False)