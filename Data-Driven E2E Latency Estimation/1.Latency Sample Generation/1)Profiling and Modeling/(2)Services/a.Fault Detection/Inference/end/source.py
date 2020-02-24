
import paho.mqtt.client as mqtt
import sys
from  opPub import pub
import logging
import pickle
import time
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
#--------------------------------------------------------------------------------data source---------------------------

#-----------------------------------------------------------sys input content----------

#10 fault-losso 192.168.0.135
txtF=sys.argv[1]
#pubtopic
topic=sys.argv[2]
#pubip
IP=sys.argv[3]
#--------------------------------------------------------sourceStream------------------------
# Loading Data-Set
label = pd.read_csv("secom_labels"+str(txtF)+".txt", delim_whitespace=True, header=None)
features = pd.read_csv("secom_data"+str(txtF)+".txt", delim_whitespace=True,header=None)

features = features.rename(columns={features.columns[i]: 'F'+ str(i) for i in range (590)}) # adding name to feature columns
label = label.rename(columns={0: 'L0', 1 :'date'})   # adding name to label column
############################################################
# Concatinating to separate files
df = pd.concat([features,label],axis=1, ignore_index=False)

# compact features
def on_message(client, userdata, msg):
    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    pubTim = time.time()
    pubTime = [pubTim]
    payload = [df, payload_decoded, pubTime]
    payload = pickle.dumps(payload)
    pub(topic, IP, payload)


client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect("192.168.0.91", 1883, 60)
client.subscribe(topic="source", qos=2)
client.loop_forever()





