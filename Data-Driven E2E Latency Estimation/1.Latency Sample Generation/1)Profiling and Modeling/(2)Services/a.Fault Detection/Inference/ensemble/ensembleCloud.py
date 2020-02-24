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
from sklearn.ensemble import AdaBoostClassifier
logging.basicConfig(level=logging.DEBUG)
# -------------sys------------------


subTopic=sys.argv[1]
subIp=sys.argv[2]
decisionNum = sys.argv[3]
knnList = []
svmList=[]
xgboostList=[]

#model = ExtraTreesClassifier(bootstrap=True, class_weight=None, criterion='gini',
     #                max_depth=None, max_features=None, max_leaf_nodes=None,
        #             min_impurity_decrease=0.0, min_impurity_split=None,
        #             min_samples_leaf=1, min_samples_split=2,
        #             min_weight_fraction_leaf=0.0, n_estimators=905, n_jobs=1,
        #             oob_score=False, random_state=2, verbose=False,
       #              warm_start=False)
model=AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
                   learning_rate=0.05368617271410339, n_estimators=883,
                   random_state=4)

# 特征压缩
def on_message(client, userdata, msg):
    #subTim = time.time()
   
    global knnList,svmList,xgboostList
    topic = msg.topic
    payload=msg.payload

    payload_decoded = pickle.loads(payload)

    if topic == 'fault-ensemble/knn':
        knnList.append(payload_decoded)

    elif  topic == 'fault-ensemble/svm':
        svmList.append(payload_decoded)
    elif topic == 'fault-ensemble/xgboost':
        xgboostList.append(payload_decoded)
    print(len(knnList),len(svmList),len(xgboostList))
    if(len(knnList)!=0 and len(svmList)!=0 and len(xgboostList)!=0):
        print(knnList[0][1])
        print(svmList[0][1])
        print(xgboostList[0][1])
        if ((knnList[0][1] == svmList[0][1]) and (svmList[0][1]==xgboostList[0][1])):
            subTim=time.time()
            knnResult = np.array(knnList[0][0])
            knnResult = np.transpose([knnResult])
            # print(cnnResult)
            svmResult = svmList[0][0]
            svmResult = np.transpose([svmResult])
            # print(svmResult)
            xgboostResult = xgboostList[0][0]
            xgboostResult = np.transpose([xgboostResult])

            attribute = np.concatenate((knnResult, svmResult,xgboostResult), axis=1)
            
            RF = joblib.load('ensembleTree4.m')
            result = RF.predict(attribute)
            result = result.tolist()
            print("result", result)
            pubtime = time.time()
            payload = [decisionNum, result, knnList[0][1], svmList[0][1],xgboostList[0][1],knnList[0][2], svmList[0][2], xgboostList[0][2],[subTim, pubtime]]

            payload = pickle.dumps(payload)
            pub('alarm', "192.168.0.135", payload)
            print("success")

            del knnList[0]
            del svmList[0]
            del xgboostList[0]
        else:
            print("bupipei")

          

client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(subIp, 1883, 60)
client.subscribe(topic=subTopic, qos=2)
client.loop_forever()
