import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


class BtToMqtt:
    '''Une application qui attend un ordre sur un GPIO
    et envoie un message mqtt
    '''
    def __init__(self, gpio_pin, topic, payload, mqtt_host = "localhost", mqtt_port = 1883):
        self.mqtt_client = mqtt.Client("gpio_sender")
        self.mqtt_client.connect(mqtt_host, mqtt_port)#, keepalive = 60)
        self.gpio_pin = gpio_pin
        self.payload = payload
        self.topic = topic
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin,GPIO.IN)
        GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=self.on_action, bouncetime= 500)

    def on_action(self):
        self.mqtt_client.publish(self.topic, payload = self.payload)

    def run(self):
        while True:
            time.sleep(0.1)

if __name__ == "__main__":
    app = BtToMqtt(22, "A700/SendKeys", "^'")
    app.run()
