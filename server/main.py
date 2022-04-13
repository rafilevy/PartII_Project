import paho.mqtt.client as mqtt
import datetime
from dateutil.parser import isoparse
import os
import json
import lib.encode as encode
from sys import argv


if len(argv) == 0:
    print("Please specify the output directory as the first argument")
    exit(1)

OUT_DIR = argv[0]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

def decode_payload(devid, payload):
    if devid == "rl630-lopy4-d68a88":
        if not ("uplink_message" in payload and "decoded_payload" in payload["uplink_message"] and "bytes" in payload["uplink_message"]["decoded_payload"]):
            return
        b = payload["uplink_message"]["decoded_payload"]["bytes"]
        temperature_bytes = b[:2]
        humidity_bytes = b[2:3]
        pressure_bytes = b[3:6]
        illuminance_bytes = b[6:8]
        payload["uplink_message"]["decoded_payload"]["temperature"] = encode.fixed_point_to_float(temperature_bytes, 8)
        payload["uplink_message"]["decoded_payload"]["humidity"] = encode.fixed_point_to_float(humidity_bytes, 1)
        payload["uplink_message"]["decoded_payload"]["pressure"] = encode.fixed_point_to_float(pressure_bytes, 0)
        payload["uplink_message"]["decoded_payload"]["illuminance"] = encode.fixed_point_to_float(illuminance_bytes, 0)

def on_message(client, userdata, msg):
    devid, msg_type = decode_device(msg.topic)
    if (msg_type != "up"):
        return

    data = json.loads(msg.payload)
    d = isoparse(data["received_at"])
    time_str = d.strftime("%H:%M:%S")
    date_str = d.strftime("%d-%m-%y")
    decode_payload(devid, data)

    filepath = OUT_DIR + "/" + devid + "." + date_str + "." + time_str + ".json"
    i = 0
    while os.path.isfile(filepath):
        filepath = OUT_DIR + "/" + devid + "." + date_str + "." + time_str + i + ".json"
        i += 1
    
    with open(filepath, "w") as f:
        json.dump(data, f)

def decode_device(topic):
    parts = topic.split("/")
    if (len(parts) > 1):
        return parts[-2], parts[-1]
    else:
        return None, None

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("part-ii-project@ttn", "NNSXS.3VHGS2ILBQ6V2TWX27KLKS4NYK7JJCNPROMPQJY.VVHZBB2QLPJRZDFPM3WF74BERMCRJW27YDTMJJZFGHQKTJLUOKYQ")
client.connect("eu1.cloud.thethings.network")

client.loop_forever()