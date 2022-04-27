"""
Config 5 - Data prediction and batching 

Config 5 uses a prediction algorithm to predict sensor values in step with the server.
If a prediction is correctly made the data is saved and nothing is sent.
If a prediction fails the device will retreive all the batched data from storage and send this to the server
"""

import socket
import math
import ubinascii
import encode
import struct
import pycom
import machine
from machine import Timer
from network import LoRa
from SI7006A20 import SI7006A20 #Temperature/Humidity sensor
from pycoproc import Pycoproc

chrono = Timer.Chrono()
chrono.start()
SENDING_INTERVAL = 10 #Interval at which to send data messages to the server, (seconds)

#Disable LED blink
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
    x = encode.byte_array_to_int(encode.float_to_fixed_point(x, 5, max_size=2))
    P = encode.byte_array_to_int(encode.float_to_fixed_point(x, 5, max_size=2))

    data = ((x & 0xffff) << 16) | (P & 0x0000ffff)
    pycom.nvs_set(key, data)

def retreive_x_P(key):
    data = pycom.nvs_get(key)
    if data == None:
        return None, None
    
    x = encode.fixed_point_to_float(encode.int_to_byte_array((data & 0xffff0000) >> 16, 2), 5)
    P = encode.fixed_point_to_float(encode.int_to_byte_array(data & 0x0000ffff, 2), 5)
    return x, P

#Push and pop all data points to non-volatile memory
def push_x_val(key, data_head, x):
    data = encode.byte_array_to_int(encode.float_to_fixed_point(x, 5, min_size=2, max_size=2))
    pycom.nvs_set(key + "_INDEX_" + str(data_head), data)
    pycom.nvs_set(key + "_HEAD", data_head+1)

def pop_x_vals(key, data_head):
    x_vals = []
    for i in range(data_head):
        data = pycom.nvs_get(key + "_INDEX_" + str(i))
        x = encode.fixed_point_to_float(encode.int_to_byte_array(data, 2), 5)
        x_vals.append(x)
        pycom.nvs_erase(key + "_INDEX_" + str(i))
    pycom.nvs_set(key + "_HEAD", 0)
    return x_vals

#Send data points over LoRaWAN
def send_data(x_vals):
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    dev_addr = struct.unpack(">l", ubinascii.unhexlify('260BF2DE'))[0]
    app_swkey = ubinascii.unhexlify('FBB6FBD7EC975D517A94CA5268C010C4')
    nwk_swkey = ubinascii.unhexlify('CFD2E8E7A6B86130F896DADE6495CB5D')
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

    # Create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setblocking(True)

    data = bytes()
    for x in x_vals:
        data += encode.float_to_fixed_point(x, 5, min_size=2, max_size=2)

    print("Sending {}|{}".format(x_vals, data))
    s.send(data)
    s.setblocking(False)

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

chrono.stop()
elapsed = chrono.read() + 1 #1 accounts for about 1s of wakeup time.
print("Sleeping for {}s".format(SENDING_INTERVAL - elapsed))
pycp.setup_sleep(SENDING_INTERVAL - elapsed)
pycp.go_to_sleep(False)