# coding=utf8
import paho.mqtt.client as mqtt
import datetime
import sys
from opPub import pub
import logging
import pickle
import numpy as np
import time
import torch
from PIL import Image
from bitarray import bitarray
from torchvision.transforms.functional import to_tensor


logging.basicConfig(level=logging.DEBUG)
#-------------sys parameter----------

#Downstream of the topic
pubTopic=sys.argv[1]
#Downstream of the IP
pubIp=sys.argv[2]

subTopic=sys.argv[3]
subIp=sys.argv[4]


# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = 'cpu'

mask = 4
codir = str(mask)
mapping_type = {0:'Center', 1:'Donut', 2:'Edge-Loc', 3:'Edge-Ring', 4:'Loc', 5:'Near-full', 6:'Random', 7:'Scratch', 8:'none'}

coder = torch.load('encoder_'+codir+'.pth').to(device)

# Image features are extracted from the encoder and converted into compressed bitmaps for transmission
def feature_extract(img):
    # Get single image input

    input = to_tensor(img).unsqueeze(0)

    # Get a single image feature extraction
  
    feature = coder(input)

    wafermap = np.array(feature.cpu().detach(), dtype='int8')
    bitmaps = []
    for _ in range(5 - mask):
        bitmap = wafermap % 2
        wafermap = wafermap // 2
        bitmaps.append(bitmap)
    bitmaps = np.array(bitmaps[::-1])
    bitarrs = bitarray(bitmaps.flatten().tolist())
    return bitarrs

#compact features
def on_message(client, userdata, msg):
    # -------Receive a message----------------
    subTim =time.time()
    
    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    #print(payload_decoded)
    imageArray =payload_decoded[0]
    frame=payload_decoded[1]
    pubTime=payload_decoded[2]

    newAttribute=[]
    for image in imageArray:
        newAttribute.append(feature_extract(image))
    payload = [newAttribute,frame]

    j=0

    thetime = time.time()
    pubTime.append(subTim)
    pubTime.append(thetime)
    payload.append(pubTime)
    payload = pickle.dumps(payload)
    pub(pubTopic, pubIp, payload)

client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(subIp, 1883, 60)
client.subscribe(topic=subTopic, qos=2)
client.loop_forever()





	
