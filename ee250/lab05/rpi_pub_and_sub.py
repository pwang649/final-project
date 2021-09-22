"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
from grovepi import *

# Connect the Grove LED to digital port D4
led = 4

pinMode(led,"OUTPUT")
time.sleep(1)
def custom_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    m = str(message.payload, "utf-8")
    print("custom_callback: " + message.topic + " " + "\"" + 
        m + "\"")
    if m == "LED_ON":
        digitalWrite(led,1)		# Send HIGH to switch on LED
        print ("LED ON!")
    elif m == "LED_OFF":
        digitalWrite(led,0)		# Send LOW to switch on LED
        print ("LED OFF!")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("MONIPET/led")
# #Default message callback. Please use custom callbacks.
# def on_message(client, userdata, msg):
#     print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    # client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
            

