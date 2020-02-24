import paho.mqtt.client as mqtt
import datetime
import sys
from  opPub import pub
import numpy as np
import logging
import pickle
import time
import schedule
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

i=0

def f():
    global i
    print("frame", i)
    payload = i
    payload = pickle.dumps(payload)
    pub("source", "192.168.0.91", payload)
    i = i + 1

schedule.every(1).seconds.do(f)

while True:
    schedule.run_pending()

