# coding=utf8
import paho.mqtt.client as mqtt
import datetime
import sys
from  opPub import pub
import numpy as np
import logging
import pickle
import pandas as pd
import time
from sklearn import preprocessing
logging.basicConfig(level=logging.DEBUG)
#-------------sys parameter---------

#Downstream of the topic
pubTopic=sys.argv[1]
#Downstream of the ip
pubIp=sys.argv[2]

subTopic=sys.argv[3]
subIp=sys.argv[4]

#Data preprocess guiyihua
def gen_sequence(id_df, seq_length, seq_cols):
    """ Only sequences that meet the window-length are considered, no padding is used. This means for testing
    we need to drop those which are below the window-length. An alternative would be to pad sequences so that
    we can use shorter ones """
    data_matrix = id_df[seq_cols].values
    num_elements = data_matrix.shape[0]

    for start, stop in zip(range(0, num_elements-seq_length), range(seq_length, num_elements)):
        yield data_matrix[start:stop, :]
def Darapreprocessing(train_df):
    rul = pd.DataFrame(train_df.groupby('id')['cycle'].max()).reset_index()
    rul.columns = ['id', 'max']
    train_df = train_df.merge(rul, on=['id'], how='left')
    train_df['RUL'] = train_df['max'] - train_df['cycle']
    train_df.drop('max', axis=1, inplace=True)
    train_df.head()
    w1 = 30
    w0 = 15
    train_df['label1'] = np.where(train_df['RUL'] <= w1, 1, 0 )
    train_df['label2'] = train_df['label1']
    train_df.loc[train_df['RUL'] <= w0, 'label2'] = 2
    train_df.head()
    train_df['cycle_norm'] = train_df['cycle']
    cols_normalize = train_df.columns.difference(['id','cycle','RUL','label1','label2'])
    min_max_scaler = preprocessing.MinMaxScaler()
    norm_train_df = pd.DataFrame(min_max_scaler.fit_transform(train_df[cols_normalize]), 
                             columns=cols_normalize, 
                             index=train_df.index)
    join_df = train_df[train_df.columns.difference(cols_normalize)].join(norm_train_df)
    train_df = join_df.reindex(columns = train_df.columns)
    sequence_length = 50
    sensor_cols = ['s' + str(i) for i in range(1,22)]
    sequence_cols = ['setting1', 'setting2', 'setting3', 'cycle_norm']
    sequence_cols.extend(sensor_cols)
# generator for the sequences
    seq_gen = (list(gen_sequence(train_df[train_df['id']==id], sequence_length, sequence_cols)) 
           for id in train_df['id'].unique())
# generate sequences and convert to numpy array
    seq_array = np.concatenate(list(seq_gen)).astype(np.float32)
    return seq_array
def on_message(client, userdata, msg):
    subtime = time.time()
    payload = msg.payload
    payload_decoded = pickle.loads(payload)
    train_df=payload_decoded[0]#data
    frame=payload_decoded[1]
    pubTime=payload_decoded[2]
    df=Darapreprocessing(train_df)#data chuli
    payload = [df,frame]
    thetime =time.time()
    pubTime.append(subtime)
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

	
