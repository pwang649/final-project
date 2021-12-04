import paho.mqtt.client as mqtt
import time
from grovepi import *
from grove_rgb_lcd import *
from collections import deque 

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
    global manual_control_mode
    if manual_control_mode:
        m = str(message.payload, "utf-8")
        print("ledR_callback: " + message.topic + " " + "\"" + m + "\"")
        if m == "on":
            digitalWrite(ledR,1)		# Send HIGH to switch on LED
            print ("LED ON!")
        elif m == "off":
            digitalWrite(ledR,0)		# Send LOW to switch off LED
            print ("LED OFF!")

def ledG_callback(client, userdata, message):
    # record publisher's message
    global manual_control_mode
    if manual_control_mode:
        m = str(message.payload, "utf-8")
        print("ledG_callback: " + message.topic + " " + "\"" + m + "\"")
        if m == "on":
            digitalWrite(ledG,1)		# Send HIGH to switch on LED
            print ("LED ON!")
        elif m == "off":
            digitalWrite(ledG,0)		# Send LOW to switch off LED
            print ("LED OFF!")

def ledB_callback(client, userdata, message):
    # record publisher's message
    global manual_control_mode
    if manual_control_mode:
        m = str(message.payload, "utf-8")
        print("ledB_callback: " + message.topic + " " + "\"" + m + "\"")
        if m == "on":
            digitalWrite(ledB,1)		# Send HIGH to switch on LED
            print ("LED ON!")
        elif m == "off":
            digitalWrite(ledB,0)		# Send LOW to switch off LED
            print ("LED OFF!")

def manual_mode_callback(client, userdata, message):
    global manual_control_mode
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
    digitalWrite(ledR,1)
    digitalWrite(ledG,1)
    digitalWrite(ledB,1)
    # Use a moving average filter if L=5
    # Initializa a deque
    deck = deque([0, 0, 0, 0, 0])  
    while True:
        soundValue = analogRead(soundSensor)
        deck.popleft()
        deck.append(soundValue)
        avg = sum(deck)/5
        print(avg)
        # publish the ultrasonic reading
        client.publish("MONIPET/soundSensor", avg)
        if not manual_control_mode:
            if soundValue > 500:
                digitalWrite(ledR,1)
                digitalWrite(ledG,0)
                digitalWrite(ledB,0)
            elif soundValue > 400:
                digitalWrite(ledR,0)
                digitalWrite(ledG,0)
                digitalWrite(ledB,1)
            else:
                digitalWrite(ledR,0)
                digitalWrite(ledG,1)
                digitalWrite(ledB,0)
        time.sleep(1)
