import paho.mqtt.client as mqtt
import time
import os
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)


@app.route('/')
def home():
    global soundValue
    return render_template("index.html", sound = soundValue)

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == "POST":
        if 'manual' in request.form.keys():
            client.publish("MONIPET/manual", "true")
        else:
            client.publish("MONIPET/manual", "false")
        r = request.form["red"]
        b = request.form["blue"]
        g = request.form["green"]
        client.publish("MONIPET/ledR", r)
        client.publish("MONIPET/ledG", g)
        client.publish("MONIPET/ledB", b)
    return redirect(url_for('home'))
    
def custom_callback(client, userdata, message):
    # prints the ultrasonic ranger value 
    print("VM: " + str(message.payload, "utf-8"))
    global soundValue
    soundValue = int(float(str(message.payload, "utf-8")))
   
    
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to interested topics here
    client.subscribe("MONIPET/soundSensor")
    client.message_callback_add("MONIPET/soundSensor", custom_callback)


if __name__ == "__main__":
    client = mqtt.Client()
    #client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    soundValue = 0
    app.secret_key = os.urandom(12)
    app.run(debug=True)