"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

def custom_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print("custom_callback: " + message.topic + " " + "\"" + 
        str(message.payload, "utf-8") + "\"")
def button_callback(client, userdata, message):
    m = str(message.payload, "utf-8")
    if m == "pressed":
        print("Button pressed!")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    
    #subscribe to the ultrasonic ranger topic here
    client.subscribe("MONIPET/ultrasonicRanger")
    client.subscribe("MONIPET/button")
    client.message_callback_add("MONIPET/ultrasonicRanger", custom_callback)
    client.message_callback_add("MONIPET/button", button_callback)
#Default message callback. Please use custom callbacks.
#
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    #client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        time.sleep(1)
            

