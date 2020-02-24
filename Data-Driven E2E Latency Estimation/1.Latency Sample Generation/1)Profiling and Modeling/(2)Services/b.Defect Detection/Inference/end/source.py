
import paho.mqtt.client as mqtt
import sys
from  opPub import pub
import logging
import pickle
import time
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
#--------------------------------------------------------------------------------data source---------------------------

#-----------------------------------------------------------sys input content--------------------
#10 fault-losso 192.168.0.135
txtF=sys.argv[1]
#pubtopic
topic1=sys.argv[2]
topic2=sys.argv[3]
#pubip
IP1=sys.argv[4]
IP2=sys.argv[5]
#--------------------------------------------------------sourceStream------------------------
# 	compact features
def on_message(client, userdata, msg):
    payload = msg.payload
    payload_decoded = pickle.loads(payload)

    auto_file = open('./imageArray'+str(txtF)+'/' + str(payload_decoded) + '.pkl', 'rb')
    imageArray = pickle.load(auto_file)

    statis_file = open('./txtArray'+str(txtF)+'/' + str(payload_decoded) + '.pkl', 'rb')
    txtArray = pickle.load(statis_file)

    
    # Transfer data to auto
    autoTime = time.time()
    autopubTime = [autoTime]
    payload = [imageArray, payload_decoded, autopubTime]
    payload = pickle.dumps(payload)
    pub(topic1, IP1, payload)

    # Transfer data to statis
    statisTime = time.time()
    statispubTime = [statisTime]
    payload = [txtArray, payload_decoded, statispubTime]
    payload = pickle.dumps(payload)
    pub(topic2, IP2, payload)


client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect("192.168.0.91", 1883, 60) #source ip
client.subscribe(topic="source", qos=2)
client.loop_forever()





