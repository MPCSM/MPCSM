# coding=utf8
import paho.mqtt.client as mqtt
import datetime
import sys
from  opPub import pub
import numpy as np
import logging
import pickle
import time
from sklearn.linear_model import Lasso

logging.basicConfig(level=logging.DEBUG)
#-------------sys parameter--------

#operator下游的数目
num= int(sys.argv[1])
#Downstream of the topic
topic1=sys.argv[2]
ip1=sys.argv[3]
topic2=sys.argv[4]
ip2=sys.argv[5]
topic3=sys.argv[6]
ip3=sys.argv[7]
#Downstream of the ip
#IPList=sys.argv[3]
subTopic=sys.argv[8]
subIp=sys.argv[9]
#Feature extraction function
def extractFeature(df):
    df = df.dropna(thresh=len(df) - int(0.1 * len(df)), axis=1)
    df = df.fillna(df.median())
    df.L0.replace(-1, 0, inplace=True)  # Converting label column to binary [0,1]

    # Building label vectore (y) and feature matrix(X)
    y = df['L0']
    X = df.drop(['L0', 'date'], axis=1)

    # ----------------------------------------------02----------------------------------------------------------
    # Employing Lasso regularization approach to reduce feature matrix dimenssion
    lasso = Lasso(alpha=0.2, normalize=False)
    lasso_coef = lasso.fit(X, y).coef_
    #print('Total number of remaining features:')
    #print(len(lasso_coef[lasso_coef != 0.0]))

    # Making a list from selected features
    val = lasso_coef[lasso_coef != 0.0]
    key, = np.where(lasso_coef != 0.0)
    feature_list = X.columns[key]
    val_plt = np.multiply(val, 1000)
    feature_list = feature_list.tolist()
    feature_column = key.tolist()
    val = val.tolist()
    ##print('List of selected features via Lasso dimenssion reduction:')
    #print(feature_list)

    # revising feature matrix based on LASSO features reduction
    X = X[feature_list]
    #print("X:",X)
    return X

def on_message(client, userdata, msg):
    # -------Receive a message----------------
    subTim = time.time()

    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    # print(payload_decoded)
    df = payload_decoded[0]
    frame = payload_decoded[1]
    pubTime = payload_decoded[2]

    #-------------------------------------------Feature extraction----------------------------------------
    new_x = extractFeature(df)
    #------------------------------------------pub message--------------------------------------
    payload = [new_x, frame]

    thetime = time.time()
    pubTime.append(subTim)
    pubTime.append(thetime)
    payload.append(pubTime)
    payload = pickle.dumps(payload)
    pub(topic1, ip1, payload)
    print("knn success")

    # Transfer data to SVM

    pub(topic2, ip2, payload)
    print("svm success")
    #xgb

    pub(topic3, ip3, payload)
    print("xgb success")
client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(subIp, 1883, 60)
client.subscribe(topic=subTopic, qos=2)
client.loop_forever()

	
