import paho.mqtt.client as mqtt
import time
from grovepi import *
from grove_rgb_lcd import *

set_bus("RPI_1")
# Connect the Grove LED to digital port D2, D3, and D4; Sound sensor to port A0
ledG = 2
ledB = 3
ledR = 4
soundSensor = 0

# set input and outputs
pinMode(soundSensor,"INPUT")
pinMode(ledG,"OUTPUT")
pinMode(ledB,"OUTPUT")
pinMode(ledR,"OUTPUT")

time.sleep(1)

manual_control_mode = False

def ledR_callback(client, userdata, message):
    # record publisher's message
    if manual_control_mode:
        m = str(message.payload, "utf-8")
        print("ledR_callback: " + message.topic + " " + "\"" + m + "\"")
        if m == "LED_ON":
            digitalWrite(ledR,1)		# Send HIGH to switch on LED
            print ("LED ON!")
        elif m == "LED_OFF":
            digitalWrite(ledR,0)		# Send LOW to switch off LED
            print ("LED OFF!")

def ledG_callback(client, userdata, message):
    # record publisher's message
    if manual_control_mode:
        m = str(message.payload, "utf-8")
        print("ledG_callback: " + message.topic + " " + "\"" + m + "\"")
        if m == "LED_ON":
            digitalWrite(ledG,1)		# Send HIGH to switch on LED
            print ("LED ON!")
        elif m == "LED_OFF":
            digitalWrite(ledG,0)		# Send LOW to switch off LED
            print ("LED OFF!")

def ledB_callback(client, userdata, message):
    # record publisher's message
    if manual_control_mode:
        m = str(message.payload, "utf-8")
        print("ledB_callback: " + message.topic + " " + "\"" + m + "\"")
        if m == "LED_ON":
            digitalWrite(ledB,1)		# Send HIGH to switch on LED
            print ("LED ON!")
        elif m == "LED_OFF":
            digitalWrite(ledB,0)		# Send LOW to switch off LED
            print ("LED OFF!")

def manual_callback(client, userdata, message):
    m = str(message.payload, "utf-8")
    print("manual_mode_callback: " + message.topic + " " + "\"" + m + "\"")
    if m == "true":
        manual_control_mode = True
        print("Switching to manual control mode")
    else:
        manual_control_mode = False
        print("Switching to auto control mode")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("MONIPET/ledR")
    client.message_callback_add("MONIPET/ledR", ledR_callback)
    client.subscribe("MONIPET/ledG")
    client.message_callback_add("MONIPET/ledG", ledG_callback)
    client.subscribe("MONIPET/ledB")
    client.message_callback_add("MONIPET/ledB", ledB_callback)
    client.subscribe("MONIPET/manual")
    client.message_callback_add("MONIPET/manual", manual_mode_callback)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    # client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        digitalWrite(ledR,1)
        digitalWrite(ledG,1)
        digitalWrite(ledB,1)
        soundValue = analogRead(soundSensor)
        print(soundValue)
        # publish the ultrasonic reading
        client.publish("MONIPET/soundSensor", soundValue)
        time.sleep(1)