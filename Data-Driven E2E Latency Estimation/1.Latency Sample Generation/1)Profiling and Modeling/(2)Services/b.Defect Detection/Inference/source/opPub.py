import paho.mqtt.client as mqtt
import logging

logging.basicConfig(level=logging.DEBUG)
MQTT_PORT = 1883

def pub(topic,MQTT_IP,payload):
    client = mqtt.Client()
    client.enable_logger(logging.getLogger(__name__))
    client.connect(MQTT_IP, MQTT_PORT, 60)
    client.loop_start()
    client.publish(topic,payload,2)
    client.loop_stop()
