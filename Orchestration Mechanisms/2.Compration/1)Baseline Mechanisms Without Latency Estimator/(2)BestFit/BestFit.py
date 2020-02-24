


faultDetectionCPU=[2,2,2,2,2]

waferInspectionCPU=[3,3,3,1,2]

rulPredictionCPU=[1,3]
serviceCpuDemand=[2,3,3,2,2,3,2,2,3]

services=[
    "fault-losso", "wafer-auto", "wafer-statis", "fault-knn",
    "fault-svm","wafer-cnn","fault-ensemble", "wafer-ensemble"]


newService=[]
serviceDeviceMap = {"fault-source": 0,"wafer-source":0,"fault-xgboost":2,"wafer-svm":0}


devicesCPU={0:3,
            1:12,
            2:6,
            3:24}

def sortedDictValues1(adict):
    items = adict.items()
    print(items)
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0, len(backitems))]

i=0
j=0
devichName=["edge0","edge1","edge2","cloud"]
for service in services:
    deviceIDAs = sortedDictValues1(devicesCPU)
    print(devicesCPU,deviceIDAs)
    for deviceId in deviceIDAs:
        if(serviceCpuDemand[i]<=devicesCPU[deviceId]):
            devicesCPU[deviceId]=devicesCPU[deviceId]-serviceCpuDemand[i]
            serviceDeviceMap[service]=deviceId
            break;
    i=i+1

print(serviceDeviceMap)






