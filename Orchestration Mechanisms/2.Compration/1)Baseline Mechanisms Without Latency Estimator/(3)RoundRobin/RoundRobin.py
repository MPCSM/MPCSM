import pandas as pd
from sklearn.externals import joblib
import xgboost as xgb
faultDetectionCPU=[2,2,2,2,2]
waferInspectionCPU=[3,3,3,1,2]
rulPredictionCPU=[1,3]
serviceCpuDemand=[2,3,3,2,2,3,2,2,3]

services=[
    "fault-losso", "wafer-auto", "wafer-statis", "fault-knn",
    "fault-svm","wafer-cnn","fault-ensemble", "wafer-ensemble", "rul-prediction"]
newService=[]
serviceDeviceMap = {"fault-source": 0,"wafer-source":0,"fault-xgboost":2,"wafer-svm":0}

devicesCPU=[3,12,6,24]


i=0
j=0
ids=[0,1,2,3]
j=0
for service in services:
    for id in ids:
        deviceId=j%4
        if deviceId == 0 and (service == "fault-losso"
                              or
                              service == "fault-ensemble"
                              or service == "wafer-statis" or service == "wafer-ensemble"):
            j=j+1
            continue;

        if deviceId == 2 and service == "wafer-auto":
            j = j + 1;
            continue;
        if(serviceCpuDemand[i]<=devicesCPU[deviceId]):
            devicesCPU[deviceId]=devicesCPU[deviceId]-serviceCpuDemand[i]
            serviceDeviceMap[service]=deviceId
            print(service,deviceId)
            j=j+1
            break;


print(len(serviceDeviceMap),serviceDeviceMap)





