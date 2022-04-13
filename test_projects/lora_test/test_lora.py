from network import LoRa
import socket
import time
import ubinascii

print("Creating LoRa instance: LORAWAN / EU868")
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print("LoRa instance created for dev_eui: "+ubinascii.hexlify(lora.mac()).decode('utf-8'))

app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('9BE36B464B60455F8CC3760BAFB46F98')

print("Joining Lora network OTAA with app_eui zeroes and app_key: "+ubinascii.hexlify(app_key).decode('utf-8'))
# join a network using OTAA (Over the Air Activation)
#uncomment below to use LoRaWAN application provided dev_eui
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

print("Sending 0x010203 to LoRaWAN network")

# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print("Optional received data:" + ubinascii.hexlify(data).decode('utf-8'))
