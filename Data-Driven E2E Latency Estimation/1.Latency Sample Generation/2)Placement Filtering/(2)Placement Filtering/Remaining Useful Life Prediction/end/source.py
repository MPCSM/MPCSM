import schedule
import datetime
import sys
from opPub import pub
import pickle
import logging
#from PIL import Image
import time
import numpy as np
import pandas as pd
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.DEBUG)

#10 fault-losso 192.168.0.135
txtF=sys.argv[1]
#下游的主题
topic=sys.argv[2]
#下游的IP地址
IP=sys.argv[3]
#--------------------------------------------------------sourceStream------------------------
# Loading Data-Set
train_df = pd.read_csv("PM_train"+str(txtF)+".txt", sep=" ", header=None)
train_df.drop(train_df.columns[[26, 27]], axis=1, inplace=True)
train_df.columns = ['id', 'cycle', 'setting1', 'setting2', 'setting3', 's1', 's2', 's3',
                     's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14',
                     's15', 's16', 's17', 's18', 's19', 's20', 's21']
# 特征压缩
def on_message(client, userdata, msg):
    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    pubTim = time.time()
    pubTime = [pubTim]
    payload = [train_df, payload_decoded, pubTime]
    payload = pickle.dumps(payload)
    pub(topic, IP, payload)


client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect("192.168.0.91", 1883, 60)
client.subscribe(topic="source", qos=2)
client.loop_forever()
