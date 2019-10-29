#!/usr/bin/python3
# -*-coding:Utf-8 -*

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time


class BtToMqtt:
    '''Une application qui attend un ordre sur un GPIO
    et envoie un message mqtt
    '''
    def __init__(self, bt_main, topic, payload, mqtt_host = "localhost", mqtt_port = 1883, buzzer = None, led = None):
        self.mqtt_client = mqtt.Client("gpio_sender")
        self.mqtt_client.connect(mqtt_host, mqtt_port)#, keepalive = 60)
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.bt_main = bt_main
        self.buzzer = buzzer
        self.led = led
        self.payload = payload
        self.topic = topic
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bt_main,GPIO.IN)
        GPIO.add_event_detect(self.bt_main, GPIO.RISING, callback=self.on_action, bouncetime= 1000)
        if self.buzzer:
            GPIO.setup(self.buzzer, GPIO.OUT)
            GPIO.output(self.buzzer, GPIO.LOW)
        if self.led:
            GPIO.setup(self.led, GPIO.OUT)
            GPIO.output(self.led, GPIO.LOW)

    def on_action(self, channel):
        if self.buzzer:
            GPIO.output(self.buzzer, GPIO.HIGH)
        if self.led:
            GPIO.output(self.led, GPIO.HIGH)
        print("Bt %s pressed"%channel)
        self.mqtt_client.publish(self.topic, payload = self.payload)
        print("%s => %s"%(self.topic, self.payload))
        time.sleep(0.5)
        if self.buzzer:
            GPIO.output(self.buzzer, GPIO.LOW)
        if self.led:
            GPIO.output(self.led, GPIO.LOW)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def run(self):
        print("Wait for button %s presses"%self.bt_main)
        self.mqtt_client.loop_forever()

if __name__ == "__main__":
    bt_bleu = 26
    bt_vert = 19
    led = 27
    buzzer = 18
    bt_main = 17
    app = BtToMqtt(bt_main, "A700/SendKeys", "^'", buzzer = buzzer, led = led)
    app.run()
