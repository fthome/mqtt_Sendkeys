import win32com.client
import time
import paho.mqtt.client as mqtt

class MqttSendKeys:
    '''Une application qui attend des ordres issu de messages mqtt
    pour les envoyer vers une application windows
    '''
    def __init__(self, application_name, mqtt_topic, mqtt_host = "localhost", mqtt_port = 1883):
        self.mqtt_client = mqtt.Client("Sendkeys")
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.connect(mqtt_host, mqtt_port)#, keepalive = 60)
        self.mqtt_client.subscribe(mqtt_topic, qos = 0)
        self.application_name = application_name
        self.shell = win32com.client.Dispatch("WScript.Shell")

    def run(self):
        self.mqtt_client.loop_forever()

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        if self.shell.AppActivate(self.application_name):
            print("Send : %s send to %s"%(message.payload, self.application_name))
            self.shell.SendKeys(message.payload.decode("utf-8"),1)
        else:
            print("Oups, application not active!")


if __name__ == "__main__":
    print('Start Send keys....')
    app = MqttSendKeys("RasterLinkPro5IP", "A700/SendKeys", mqtt_host = "192.9.200.170")
    app.run()
