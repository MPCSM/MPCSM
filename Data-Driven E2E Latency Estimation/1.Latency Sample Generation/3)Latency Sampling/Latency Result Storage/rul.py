import paho.mqtt.client as mqtt
import pickle
import sys
import logging
import datetime
import time
import pymongo

logging.basicConfig(level=logging.DEBUG)

#db_name = 'faultAutoTest'
#col_name = 'latency'
db_name = 'rul131'
mongoAddress=sys.argv[1]


myclient = pymongo.MongoClient("mongodb://"+mongoAddress+":27017/")
mydb = myclient[db_name]
#mycol = mydb[col_name]

def on_message(client, userdata, message):
    #print("sub success!")
    subtime = time.time()
    payload = message.payload
    #print(payload)
    payload_decoded = pickle.loads(payload)
    #print(payload_decoded)
    decisionNum = payload_decoded[0]
    mycol = mydb[decisionNum]
    result=payload_decoded[1]
   # frame=payload_decoded[2]

    theTime=payload_decoded[3]

    mydict ={"theTime":theTime}
    print(mydict)
    x = mycol.insert_one(mydict)

client = mqtt.Client()
client.enable_logger(logging.getLogger(__name__))
client.on_message = on_message
client.connect(mongoAddress, 1883, 60)
client.subscribe(topic="rulalarm", qos=2)
client.loop_forever()
