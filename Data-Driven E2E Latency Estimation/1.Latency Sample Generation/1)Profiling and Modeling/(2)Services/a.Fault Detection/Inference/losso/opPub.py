import paho.mqtt.client as mqtt
MQTT_PORT = 1883

def pub(topic,MQTT_IP,payload):
    client = mqtt.Client()
    client.connect(MQTT_IP, MQTT_PORT, 60)
    client.loop_start()
    client.publish(topic,payload,2)
    client.loop_stop()