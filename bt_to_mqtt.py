#!/usr/bin/python3
# -*-coding:Utf-8 -*

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time


class BtToMqtt:
    '''Une application qui attend un ordre sur un GPIO
    et envoie un message mqtt
    '''
    def __init__(self, gpio_pin, topic, payload, mqtt_host = "localhost", mqtt_port = 1883):
        self.mqtt_client = mqtt.Client("gpio_sender")
        self.mqtt_client.connect(mqtt_host, mqtt_port)#, keepalive = 60)
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.gpio_pin = gpio_pin
        self.payload = payload
        self.topic = topic
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin,GPIO.IN)
        GPIO.add_event_detect(self.gpio_pin, GPIO.FALLING, callback=self.on_action, bouncetime= 1000)

    def on_action(self, channel):
        print("Bt %s pressed"%channel)
        self.mqtt_client.publish(self.topic, payload = self.payload)
        print("%s => %s"%(self.topic, self.payload))

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def run(self):
        print("Wait for button %s presses"%self.gpio_pin)
        self.mqtt_client.loop_forever()

if __name__ == "__main__":
    app = BtToMqtt(17, "A700/SendKeys", "^'")
    app.run()
