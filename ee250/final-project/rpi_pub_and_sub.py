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

    while True:
        digitalWrite(ledR,1)
        digitalWrite(ledG,1)
        digitalWrite(ledB,1)
        print(analogRead(soundSensor))
        # publish the ultrasonic reading
        client.publish("MONIPET/soundSensor", ultrasonicRead(ultrasonic_ranger))
        time.sleep(1)