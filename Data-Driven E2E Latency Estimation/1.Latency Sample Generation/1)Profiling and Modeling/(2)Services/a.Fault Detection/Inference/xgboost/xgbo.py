# coding=utf8
import paho.mqtt.client as mqtt
import sys
import pickle
import logging
from opPub import pub
import time
from xgboost.sklearn import XGBClassifier
import xgboost as xgb
from sklearn.externals import joblib

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

logging.basicConfig(level=logging.DEBUG)

# Downstream of the topic
pubTopic = sys.argv[1]
# Downstream of the ip
pubIp = sys.argv[2]

subTopic = sys.argv[3]
subIp = sys.argv[4]


def on_message(client, userdata, msg):
    subtime = time.time()
    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    print("abc:",len(payload_decoded))
    newAttribute = payload_decoded[0]
    newAttribute=newAttribute.as_matrix()
    #print("att:",newAttribute)
    i = payload_decoded[1]
    pubTime = payload_decoded[2]

    # Load the model and get the predicted results

    clf2 = pickle.load(open("xbg.pickle.dat","rb"))
    #print("loadmodel")
    xgbResult = clf2.predict(newAttribute)
    print(xgbResult)
    payload = [xgbResult, i]

    thetime = time.time()
    pubTime.append(subtime)
    pubTime.append(thetime)
    payload.append(pubTime)
    payload = pickle.dumps(payload)
    pub(pubTopic, pubIp, payload)
    print("to ensemble success")


client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(subIp, 1883, 60)
client.subscribe(topic=subTopic, qos=2)
client.loop_forever()



