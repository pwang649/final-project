"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

def custom_callback(client, userdata, message):
    # prints the ultrasonic ranger value 
    print("VM: " + str(message.payload, "utf-8") + " cm")
   
def button_callback(client, userdata, message):
    m = str(message.payload, "utf-8")
    print(str(m))
    
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    
    #subscribe to interested topics here
    client.subscribe("MONIPET/soundSensor")
    client.message_callback_add("MONIPET/soundSensor", custom_callback)


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
