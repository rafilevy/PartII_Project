from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from dateutil.parser import isoparse
import os
import json
import lib.encode as encode
from sys import argv
from timeloop import Timeloop

tl = Timeloop()


if len(argv) == 0:
    print("Please specify the output directory as the first argument")
    exit(1)

OUT_DIR = argv[0]

predictor_a = None
predictor_b = None
prev_timestamp = None
MESSAGE_INTERVAL = 30 #Interval to expect messages it in s

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

def decode_payload(devid, payload):
    if devid == "rl630-lopy4-d68a88":
        if not ("uplink_message" in payload and "decoded_payload" in payload["uplink_message"] and "bytes" in payload["uplink_message"]["decoded_payload"]):
            return
        b = payload["uplink_message"]["decoded_payload"]["bytes"]

        n_data_points = len(b) / 2
        temps = [encode.fixed_point_to_float(b[i:i+2], 5) for i in range(n_data_points)]
        payload["uplink_message"]["decoded_payload"]["temperature"] = temps

def on_message(client, userdata, msg):
    devid, msg_type = decode_device(msg.topic)
    if (msg_type != "up"):
        return

    data = json.loads(msg.payload)
    d = isoparse(data["received_at"])

    global prev_timestamp
    prev_timestamp = d

    decode_payload(devid, data)
    global predictor_a, predictor_b
    temps = data["uplink_message"]["decoded_payload"]["temperature"]
    if predictor_a == None:
        predictor_a = Predictor(temps[-1], 1.)
        predictor_b = Predictor(temps[-1], 1.)

    process_temp_data(temps)

def decode_device(topic):
    parts = topic.split("/")
    if (len(parts) > 1):
        return parts[-2], parts[-1]
    else:
        return None, None

def process_temp_data(data):
    print(datetime.now().strftime("%d-%m-%y %H:%M:%S"), data)

class Predictor:
    def __init__(self, x_0, P_0, Q=0., R=1., error_threshold=0.05, ):
        self.Q = Q
        self.R = R
        self.threshold = error_threshold
        
        self.x = x_0
        self.P = P_0

    def predict(self):
        x = self.x
        self.P = self.P + self.Q
        return self.x
    
    def update(self, z):
        KG = self.P/(self.P + self.R)
        self.P = self.P * (1 - KG)
        self.x = self.x + KG*(z - self.x)
        return self.x

    def clone(self):
        return Predictor(self.x, self.p, self.Q, self.R, self.threshold)

@tl.job(interval=timedelta(seconds=MESSAGE_INTERVAL))
def predict_messages():
    global prev_timestamp, predictor_a
    current_ts = datetime.now()
    if (prev_timestamp == None or predictor_a == None):
        return
    
    dt = current_ts - prev_timestamp
    if (dt.seconds > MESSAGE_INTERVAL):
        x = predictor_a.predict()
        process_temp_data(x)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("part-ii-project@ttn", "NNSXS.3VHGS2ILBQ6V2TWX27KLKS4NYK7JJCNPROMPQJY.VVHZBB2QLPJRZDFPM3WF74BERMCRJW27YDTMJJZFGHQKTJLUOKYQ")
client.connect("eu1.cloud.thethings.network")

client.loop_forever()

