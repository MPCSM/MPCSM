# coding=utf8
import paho.mqtt.client as mqtt
import datetime
import sys
import pickle
import logging
import numpy as np
from opPub import pub
import torch
import time
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = 'cpu'

mask = 4
codir = str(mask)
mapping_type = {0:'Center', 1:'Donut', 2:'Edge-Loc', 3:'Edge-Ring', 4:'Loc', 5:'Near-full', 6:'Random', 7:'Scratch', 8:'none'}


logging.basicConfig(level=logging.DEBUG)

#Downstream of the topic
pubTopic=sys.argv[1]
#Downstream of the IP
pubIp=sys.argv[2]

subTopic=sys.argv[3]
subIp=sys.argv[4]

classifier = torch.load('classifier_'+codir+'.pth').to(device)

# Decode bitmaps and classify them
def classify(feature_bitarrs):
    print("in")

    wafer = np.array(feature_bitarrs.tolist())

    wafer.resize((5 - mask, 6, 7, 7))
    feature = np.zeros((6, 7, 7))
    for index in wafer:
        feature = feature * 2 + index
    feature = torch.Tensor(feature).unsqueeze(0)
   
    y = classifier(feature).detach()
    label = int(np.argmax(y.data.numpy()[0]))
    print(label)
    return label

def on_message(client, userdata, msg):
    subtime = time.time()
    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    newAttribute=payload_decoded[0]
    i=payload_decoded[1]
    pubTime=payload_decoded[2]
    #Load the model and get the predicted results
    labels=[]
    for newAtt in newAttribute:
        labels.append(classify(newAtt))
    print("iii")
    print(labels)
    payload = [labels, i]
    thetime = time.time()
    pubTime.append(subtime)
    pubTime.append(thetime)
    payload.append(pubTime)
    payload = pickle.dumps(payload)
    pub(pubTopic, pubIp, payload)

client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(subIp,1883,60)
client.subscribe(topic=subTopic,qos=2)
client.loop_forever()


	
