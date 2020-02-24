# coding=utf8
import paho.mqtt.client as mqtt
import sys
import pickle
import logging
from opPub import pub
import time
import datetime
from keras.models import load_model
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
logging.basicConfig(level=logging.DEBUG)
subTopic=sys.argv[1]
subIp=sys.argv[2]
decisionNum = sys.argv[3]
def on_message(client, userdata, msg):
    subtime = time.time()
    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    newAttribute=payload_decoded[0]
    #print("att:",newAttribute[:2])
    i=payload_decoded[1]
    pubTime=payload_decoded[2]
    #加载模型，得到预测结果
    clf2 =  load_model("binary_model.h5")
    #print("loadmodel")
    LSTMResult = clf2.predict_classes(newAttribute)
    print(LSTMResult)
    payload = [decisionNum,LSTMResult, i]
    thetime =time.time()
    pubTime.append(subtime)
    pubTime.append(thetime)
    payload.append(pubTime)
    payload = pickle.dumps(payload)
    #pub(pubTopic, pubIp, payload)
    pub('alarm', "39.100.79.76", payload)
client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(subIp,1883,60)
client.subscribe(topic=subTopic,qos=2)
client.loop_forever()


	
