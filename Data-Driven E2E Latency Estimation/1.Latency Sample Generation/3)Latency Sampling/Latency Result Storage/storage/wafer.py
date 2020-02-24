import paho.mqtt.client as mqtt
import pickle
import sys
import logging
import datetime
import time
import pymongo

logging.basicConfig(level=logging.DEBUG)


db_name = sys.argv[2]
mongoAddress=sys.argv[1]


myclient = pymongo.MongoClient("mongodb://"+mongoAddress+":27017/")
mydb = myclient[db_name]

def on_message(client, userdata, message):
    #print("sub success!")
    subtime = time.time()
    payload = message.payload
    print(payload)
    payload_decoded = pickle.loads(payload)
    print(payload_decoded)
    decisionNum = payload_decoded[0]
    mycol = mydb[decisionNum]
    result=payload_decoded[1]
    cnnframe=payload_decoded[2]
    svmframe=payload_decoded[3]
    cnnTime=payload_decoded[4]
    svmTime=payload_decoded[5]
    ensembleTime=payload_decoded[6]
    #print("result",payload_decoded)
    #decisionNum, result, cnnList[0][1], svmList[0][1],cnnList[0][2], svmList[0][2], [subTim, pubtime]
    mydict ={"cnnframe":cnnframe,"svmframe":svmframe,"cnnTime":cnnTime,"svmTime":svmTime,"ensembleTime":ensembleTime}
    x = mycol.insert_one(mydict)

client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(mongoAddress, 1883, 60)
client.subscribe(topic="waferalarm", qos=2)
client.loop_forever()
