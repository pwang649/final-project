"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""


import paho.mqtt.client as mqtt
import time
from grovepi import *
from grove_rgb_lcd import *

set_bus("RPI_1")
# Connect the Grove LED to digital port D4, Ultrasonic ranger to port D3, button to D2
led = 4
ultrasonic_ranger = 3
button = 2

# set input and outputs
pinMode(button,"INPUT")
pinMode(led,"OUTPUT")

time.sleep(1)

def custom_callback(client, userdata, message):
    # record publisher's message
    m = str(message.payload, "utf-8")
    print("custom_callback: " + message.topic + " " + "\"" + m + "\"")
    if m == "LED_ON":
        digitalWrite(led,1)		# Send HIGH to switch on LED
        print ("LED ON!")
    elif m == "LED_OFF":
        digitalWrite(led,0)		# Send LOW to switch off LED
        print ("LED OFF!")

def lcd_callback(client, userdata, message):
    msg = str(message.payload, "utf-8")
    setRGB(0,255,0) # set to green color
    setText_norefresh(str(msg))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("MONIPET/led")
    client.message_callback_add("MONIPET/led", custom_callback)
    client.subscribe("MONIPET/lcd")
    client.message_callback_add("MONIPET/lcd", lcd_callback)

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    # client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:e
        # if the button is pressed
        if digitalRead(button) == 1:
            client.publish("MONIPET/button", "Button pressed!") # publish message
        
        # publish the ultrasonic reading
        client.publish("MONIPET/ultrasonicRanger", ultrasonicRead(ultrasonic_ranger))
        time.sleep(1)