# coding=utf8
import paho.mqtt.client as mqtt
import sys
import numpy as np
from opPub import pub
import logging
import pickle
import time
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.externals import joblib

logging.basicConfig(level=logging.DEBUG)
# -------------sys parameter------------------


subTopic=sys.argv[1]
subIp=sys.argv[2]
decisionNum = sys.argv[3]
cnnList = []
svmList=[]

model = ExtraTreesClassifier(bootstrap=True, class_weight=None, criterion='gini',
                     max_depth=None, max_features=None, max_leaf_nodes=None,
                     min_impurity_decrease=0.0, min_impurity_split=None,
                     min_samples_leaf=1, min_samples_split=2,
                     min_weight_fraction_leaf=0.0, n_estimators=905, n_jobs=1,
                     oob_score=False, random_state=2, verbose=False,
                     warm_start=False)


# compact features
def on_message(client, userdata, msg):

    # ------Receive a message----------------
    global cnnList,svmList
    topic = msg.topic
    payload=msg.payload

    payload_decoded = pickle.loads(payload)

    if topic == 'wafer-ensemble/cnn':
        cnnList.append(payload_decoded)

    elif topic == 'wafer-ensemble/svm':
        svmList.append(payload_decoded)
    print(len(cnnList),len(svmList))
    if(len(cnnList)!=0 and len(svmList)!=0):
        print(cnnList[0][1])
        print(svmList[0][1])
        subTim = time.time()
        cnnResult = np.array(cnnList[0][0])
        cnnResult = np.transpose([cnnResult])
        # print(cnnResult)
        svmResult = svmList[0][0]
        svmResult = np.transpose([svmResult])
        # print(svmResult)

        attribute = np.concatenate((cnnResult, svmResult), axis=1)
        # 
        RF = joblib.load('ensembleTree4.m')
        result = RF.predict(attribute)
        result = result.tolist()
        print("result", result)
        pubtime = time.time()
        payload = [decisionNum, result, cnnList[0][1], svmList[0][1],cnnList[0][2], svmList[0][2], [subTim, pubtime]]

        payload = pickle.dumps(payload)
        pub('waferalarm', "39.100.79.76", payload)
        # for re in result:
        #     if re != "none":
        #         pubtime = time.time()
        #         payload = [decisionNum, result, cnnList[0][1], cnnList[0][2], svmList[0][2], [subTim, pubtime]]
        #
        #         payload = pickle.dumps(payload)
        #         pub('alarm', "192.168.0.135", payload)
        #         break;

        del cnnList[0]
        del svmList[0]

client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(subIp, 1883, 60)
client.subscribe(topic=subTopic, qos=2)
client.loop_forever()
